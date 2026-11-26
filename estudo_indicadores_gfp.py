"""Extração agregada do estudo GFP, executada no driver da sessão Spark."""

import csv
import io
import json
import re
from collections import Counter, defaultdict
from contextlib import contextmanager
from datetime import date, datetime, timedelta, timezone
from decimal import Decimal, localcontext
from pathlib import Path
from time import perf_counter
from uuid import uuid4

PRINCIPAIS = ("Q00", "Q01", "Q01B", "Q02", "Q03", "Q04", "Q05", "Q06", "Q07", "Q08", "Q11")
COMPLEMENTARES = ("Q09", "Q10")
INDICADORES = ("IN_VSLO_CSM", "IN_VSLO_CX", "IN_VSLO_EVT", "IN_DVS_LCTO", "IN_OCTR_TRAN", "IN_TRAN_IR")
METRICAS = ("QT_TRAN", "VL_TOTAL", "VL_ABS")
CADASTROS = ("Q01", "Q01B")
MANIFESTO = "Manifesto_Execucao.md"
FONTES_PACOTE = ("ESTUDO_RADAR.ipynb", "estudo_indicadores_gfp.py")
ZERO = (0, Decimal(0), Decimal(0))
CENARIOS_Q04 = (
    "ORIGINAL",
    "CSM",
    "CX",
    "EVT",
    "DVS",
    "OCTR",
    "IR",
    "RADAR",
    "CSM_D",
    "GFP_EVT_INST",
    "GFP_CX_INST",
    "GFP_CSM_INST",
)
ISOLAMENTO = "READ_COMMITTED"
COLUNAS_RESTRITAS = re.compile(
    r"^(CD_CLI(?:_|$)|NR_CPF|CD_CPF|NR_TRAN_(?:INST|INCD|RLZD)|"
    r"(?:NR|CD|DV)_(?:AG|CT)_|(?:CD|NR)_IDFR_|TX_(?:CMPR_)?DCR_TRAN)"
)


class ErroValidacao(ValueError):
    """Validação com mensagem controlada para o manifesto."""


def validar_periodo(inicio, fim, spark=None):
    """Confere [início, fim) e, no driver, o último dia incluído pelo calendário da sessão."""
    if not all(
        isinstance(valor, str) and re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}", valor)
        for valor in (inicio, fim)
    ):
        raise ValueError("Informe as duas datas no formato AAAA-MM-DD.")
    try:
        primeiro_dia, fim_exclusivo = date.fromisoformat(inicio), date.fromisoformat(fim)
    except ValueError:
        raise ValueError("Informe datas de calendário válidas no formato AAAA-MM-DD.") from None
    if primeiro_dia >= fim_exclusivo:
        raise ValueError("A data inicial deve ser anterior à data final exclusiva.")
    if spark is not None:
        hoje = spark.sql("SELECT CURRENT_DATE() AS HOJE").first()[0]
        if fim_exclusivo - timedelta(days=1) > hoje:
            raise ValueError("O período inclui um dia futuro segundo a data atual da sessão Spark.")


def preparar_consultas(pasta, inicio, fim, complementares=()):
    """Carrega as consultas previstas e parametriza seus limites."""
    validar_periodo(inicio, fim)
    complementares = tuple(complementares)
    if len(set(complementares)) != len(complementares) or set(complementares) - set(COMPLEMENTARES):
        raise ValueError("As únicas consultas complementares são Q09 e Q10.")

    consultas = {}
    for consulta in PRINCIPAIS + complementares:
        pasta_sql = "02_COMPLEMENTARES" if consulta in COMPLEMENTARES else "01_PRINCIPAIS"
        sql = (Path(pasta) / pasta_sql / f"{consulta}.sql").read_text(encoding="utf-8-sig")
        sql = re.sub(r"(?m)^--[^\n]*\n?", "", sql).strip()
        if sql.endswith(";"):
            sql = sql[:-1].rstrip()
        if not re.match(r"^(SELECT|WITH)\b", sql, re.I) or ";" in sql or re.search(r"\{[^}]*\}", sql):
            raise ValueError(f"{consulta} deve conter uma única consulta de leitura completa.")
        if consulta not in CADASTROS:
            for coluna, data in (("DT_INI", inicio), ("DT_FIM_EXCL", fim)):
                padrao = rf"DATE\('\d{{4}}-\d{{2}}-\d{{2}}'\)(\s+AS\s+{coluna}\b)"
                sql, substituicoes = re.subn(padrao, rf"DATE('{data}')\1", sql, flags=re.I)
                if substituicoes != 1:
                    raise ValueError(f"{consulta} precisa declarar exatamente um limite {coluna}.")
        consultas[consulta] = sql
    return consultas


def preparar_notebook(pasta, revisao):
    """Localiza a revisão executada, inclusive se o download recebeu um sufixo."""
    marcador = f'revisao_notebook = "{revisao}"'
    caminhos = sorted(Path(pasta).glob("ESTUDO_RADAR*.ipynb"), key=lambda caminho: caminho.name)
    for caminho in caminhos:
        try:
            notebook = json.loads(caminho.read_text(encoding="utf-8-sig"))
        except (OSError, ValueError):
            continue
        if any(
            celula["cell_type"] == "code" and marcador in "".join(celula["source"]).splitlines()
            for celula in notebook["cells"]
        ):
            break
    else:
        raise ValueError(f"O arquivo do notebook da revisão {revisao} não foi localizado na raiz do projeto.")

    notebook["metadata"] = {
        nome: valor for nome, valor in notebook["metadata"].items() if nome in ("kernelspec", "language_info")
    }
    for celula in notebook["cells"]:
        celula["metadata"] = {
            nome: valor
            for nome, valor in celula.get("metadata", {}).items()
            if nome in ("deletable", "editable")
        }
        if celula["cell_type"] == "code":
            celula.update(outputs=[], execution_count=None)
    return json.dumps(notebook, ensure_ascii=False, indent=1) + "\n"


class PastaResultados:
    """Organiza o inventário da execução e delega as operações de arquivo ao HDFS V1."""

    def __init__(self, criar_hdfs, destino, identificador):
        base = criar_hdfs(diretorio_base=destino)
        if destino is None:
            projeto = base.criar_diretorio("ESTUDO_INDICADORES_GFP", existir_ok=True)
            resultados = base.criar_diretorio(f"{projeto}/04_RESULTADOS_DB2", existir_ok=True)
            identificador = f"{resultados}/{identificador}"
        self.pasta = base.criar_diretorio(identificador)
        self.hdfs = criar_hdfs(diretorio_base=self.pasta)
        self.publicados = set()

    @contextmanager
    def escrever(self, arquivo):
        with self.hdfs.abrir_escrita(arquivo) as saida:
            yield saida
        self.publicados.add(arquivo)

    def salvar_texto(self, arquivo, conteudo):
        self.hdfs.salvar_texto(arquivo, conteudo)
        self.publicados.add(arquivo)

    def publicar_zip(self, nome, esperados):
        if self.publicados != esperados or not esperados:
            raise ErroValidacao("Os arquivos produzidos divergem do inventário do ZIP.")
        info = self.hdfs.compactar_zip(sorted(esperados), nome)
        if (
            info["caminho"] != f"{self.pasta}/{nome}"
            or len(info["arquivos"]) != len(esperados)
            or set(info["arquivos"]) != esperados
            or not re.fullmatch(r"[a-f0-9]{64}", info["sha256"])
        ):
            raise ErroValidacao("O gerenciador HDFS retornou uma validação de ZIP inconsistente.")
        return info["caminho"], info["sha256"]

    def limpar_arquivos_avulsos(self):
        """Retira somente os arquivos escritos por esta execução após publicar o ZIP."""
        for arquivo in sorted(self.publicados):
            try:
                if not self.hdfs.remover(arquivo):
                    print(f"Arquivo avulso preservado no HDFS - {arquivo}")
            except Exception:
                print(f"Não foi possível retirar do HDFS o arquivo avulso {arquivo}.")


def codificar_campo(valor):
    if valor is None:
        return r"\N"
    return "\\" + valor if valor.startswith("\\") else valor


def ler_metricas(linha):
    quantidade = int(linha["QT_TRAN"])
    total, absoluto = (Decimal(linha[campo]) for campo in METRICAS[1:])
    if quantidade < 0 or not total.is_finite() or not absoluto.is_finite() or absoluto < abs(total):
        raise ErroValidacao("Contagem ou valores agregados inválidos.")
    return quantidade, total, absoluto


def somar_metricas(primeiro, segundo):
    return tuple(a + b for a, b in zip(primeiro, segundo))


def acumular(grupos, chave, valores):
    grupos[chave] = somar_metricas(grupos.get(chave, (0,) * len(valores)), valores)


class ResumoConsulta:
    """Guarda somente os subtotais usados nos controles cruzados."""

    def __init__(self, consulta, inicio, fim):
        self.consulta = consulta
        self.inicio = inicio
        self.fim = fim
        self.linhas = 0
        self.total = ZERO
        self.produtos = {}
        self.combinacoes = {}
        self.cenarios = defaultdict(dict)
        self.divididos = Counter()
        self.chaves = set()
        self.fora_dominio = Counter()

    def adicionar(self, linha):
        self.linhas += 1
        consulta = self.consulta
        if consulta in ("Q01", "Q01B"):
            coluna = "CD_CTGR_TRAN" if consulta == "Q01" else "CD_GR_CTGR_TRAN"
            chave = linha[coluna]
            if chave is None or chave in self.chaves:
                raise ErroValidacao("Chave ausente ou repetida no cadastro.")
            self.chaves.add(chave)
            return

        if consulta == "Q08":
            chave = tuple(linha[c] for c in ("CD_PRD", "CD_NTZ_CTB_TRAN", *INDICADORES[:3]))
            quantidade = int(linha["QT_ORIGINAIS"])
            if quantidade < 1 or int(linha["QT_DERIVADOS"]) < 0:
                raise ErroValidacao("Contagem inválida de originais ou derivados.")
            self.divididos[chave] += quantidade
            return

        if consulta == "Q04":
            chave = linha["CD_PRD"], linha["CD_NTZ_CTB_TRAN"]
            if chave in self.cenarios:
                raise ErroValidacao("Produto e natureza repetidos na Q04.")
            cenarios = {
                nome: (int(linha[f"QT_{nome}"]), Decimal(linha[f"VL_ABS_{nome}"])) for nome in CENARIOS_Q04
            }
            qt_base, vl_base = cenarios["ORIGINAL"]
            if any(not (0 <= qt <= qt_base and 0 <= vl <= vl_base) for qt, vl in cenarios.values()):
                raise ErroValidacao("O resultado de um cenário da Q04 excede seu universo.")
            self.cenarios[chave] = cenarios
            return

        metricas = ler_metricas(linha)
        if consulta == "Q00":
            dias = (date.fromisoformat(self.fim) - date.fromisoformat(self.inicio)).days
            if (
                self.linhas != 1
                or linha["DT_INI"] != self.inicio
                or linha["DT_FIM_EXCL"] != self.fim
                or int(linha["QT_DIAS"]) != dias
            ):
                raise ErroValidacao("A Q00 deve retornar uma linha para a janela selecionada.")
            minimo, maximo = linha["DT_MIN_OBS"], linha["DT_MAX_OBS"]
            if metricas[0]:
                if not minimo or not maximo or not self.inicio <= minimo <= maximo < self.fim:
                    raise ErroValidacao("A Q00 retornou datas observadas fora da janela.")
            elif minimo is not None or maximo is not None or metricas != ZERO:
                raise ErroValidacao("A Q00 retornou medidas incompatíveis com janela vazia.")

        produto = linha.get("CD_PRD")
        if consulta == "Q10" and (
            produto not in ("6", "9")
            or linha["CD_EST_TRAN_INST"] != "0"
            or (linha["CD_TIP_MOE_CRR"] or "").rstrip() != "BRL"
        ):
            return
        self.total = somar_metricas(self.total, metricas)
        if consulta in ("Q02", "Q03", "Q10"):
            indicadores = tuple(linha[nome] for nome in INDICADORES)
            acumular(self.combinacoes, indicadores, metricas)
        if consulta == "Q02":
            for nome, valor in zip(INDICADORES, indicadores):
                if valor not in ("S", "N"):
                    self.fora_dominio[nome] += metricas[0]
        if consulta == "Q03":
            acumular(self.produtos, produto, metricas)
            natureza = linha["CD_NTZ_CTB_TRAN"]
            csm, cx, evt, dvs, octr, ir = indicadores
            consumo_debito = natureza == "D" and csm == "S"
            condicoes = (
                True,
                csm == "S",
                cx == "S",
                evt == "S",
                dvs == "N",
                octr == "N",
                ir == "S",
                natureza == "C" or consumo_debito,
                consumo_debito,
                evt == "S" and dvs == "N",
                cx == "S" and dvs == "N",
                consumo_debito and dvs == "N",
            )
            grupo = self.cenarios[produto, natureza]
            for nome, condicao in zip(CENARIOS_Q04, condicoes):
                acumular(grupo, nome, (metricas[0], metricas[2]) if condicao else (0, Decimal(0)))
            if dvs == "S":
                self.divididos[produto, natureza, csm, cx, evt] += metricas[0]
        if (consulta == "Q05" and produto != "9") or (consulta == "Q06" and produto != "6"):
            raise ErroValidacao("A consulta retornou produto fora de seu recorte.")


def exportar_consulta(conector, conexao, arquivos, consulta, sql, inicio, fim, timeout):
    resumo = ResumoConsulta(consulta, inicio, fim)
    arquivos.salvar_texto(f"{consulta}.sql", sql + "\n")
    with arquivos.escrever(f"{consulta}.csv") as saida:
        with conector.blocos_nativos(
            sql, conexao=conexao, isolation_level=ISOLAMENTO, query_timeout=timeout
        ) as (cabecalho, blocos):
            colunas = [nome.upper() for nome in cabecalho]
            if len(set(colunas)) != len(colunas) or any(COLUNAS_RESTRITAS.search(c) for c in colunas):
                raise ErroValidacao("Cabeçalho duplicado ou fora do contrato de exportação agregada.")
            if consulta not in ("Q00", "Q01", "Q01B", "Q04", "Q08") and not set(METRICAS) <= set(colunas):
                raise ErroValidacao("Faltam as medidas de agregação esperadas.")

            buffer_csv = io.StringIO()
            csv_saida = csv.writer(buffer_csv, delimiter=";")
            csv_saida.writerow(colunas)
            for bloco in blocos:
                for linha in bloco:
                    valores = [
                        format(v, "f") if isinstance(v, Decimal) else str(v) if v is not None else None
                        for v in linha
                    ]
                    resumo.adicionar(dict(zip(colunas, valores)))
                    csv_saida.writerow([codificar_campo(valor) for valor in valores])
                    if buffer_csv.tell() >= 65536:
                        saida.write(buffer_csv.getvalue())
                        buffer_csv.seek(0)
                        buffer_csv.truncate()
            if consulta == "Q00" and resumo.linhas != 1:
                raise ErroValidacao("A Q00 deve retornar o controle do período mesmo com janela vazia.")
            saida.write(buffer_csv.getvalue())
    return resumo


def verificar_resultados(resultados, consultas):
    verificacoes = []

    def conferir(nome, primeira, segunda, atributo, esperado=None):
        if primeira not in resultados or segunda not in resultados:
            verificacoes.append((nome, "PENDENTE"))
            return
        observado = getattr(resultados[primeira], atributo)
        comparavel = (
            getattr(resultados[segunda], atributo) if esperado is None else esperado(resultados[segunda])
        )
        verificacoes.append((nome, "OK" if observado == comparavel else "DIVERGÊNCIA"))

    conferir("Q00 × Q02 em quantidade, valor registrado e valor absoluto", "Q00", "Q02", "total")
    conferir("Q00 × Q03 em quantidade, valor registrado e valor absoluto", "Q00", "Q03", "total")
    conferir("Q02 × Q03 por combinação dos seis indicadores", "Q02", "Q03", "combinacoes")
    conferir("Q04 × Q03 por produto, natureza e cenário de retenção", "Q04", "Q03", "cenarios")
    for consulta, produto in (("Q05", "9"), ("Q06", "6")):
        conferir(
            f"{consulta} × Q03 para produto {produto}",
            consulta,
            "Q03",
            "total",
            lambda resumo, prd=produto: resumo.produtos.get(prd, ZERO),
        )
    conferir(
        "Q08 × Q03 para originais divididos por produto, natureza e visibilidade",
        "Q08",
        "Q03",
        "divididos",
    )
    for consulta in ("Q09", "Q11"):
        if consulta in consultas:
            conferir(f"{consulta} × Q03 para o universo principal", consulta, "Q03", "total")
    if "Q10" in consultas:
        conferir(
            "Q10 × Q02 por combinação, no recorte BRL efetivado de produtos 6 e 9",
            "Q10",
            "Q02",
            "combinacoes",
        )
    return verificacoes


def diagnostico_erro(conector, erro):
    if isinstance(erro, ErroValidacao):
        return str(erro)
    partes = [type(erro).__name__]
    try:
        diagnostico = conector.diagnosticar_erro(erro)
        estado, codigo = diagnostico["sqlstate"], diagnostico["sqlcode"]
        if isinstance(estado, str) and re.fullmatch(r"[A-Z0-9]{5}", estado) and type(codigo) is int:
            partes.extend((f"SQLSTATE {estado}", f"SQLCODE {codigo}"))
    except Exception:
        # Uma falha no diagnóstico não impede a publicação dos resultados já obtidos.
        pass
    return ", ".join(partes)


def escrever_manifesto(arquivos, configuracao, metadados, estados, resultados, verificacoes, situacao):
    inicio, fim = configuracao["inicio"], configuracao["fim"]
    linhas = [
        "# Manifesto de execução do estudo GFP",
        "",
        f"- Situação do pacote - {situacao}",
        f"- Início da execução em UTC — {metadados['inicio']}",
        f"- Fim da execução em UTC — {datetime.now(timezone.utc).isoformat(timespec='seconds')}",
        f"- Janela em DT_TRAN — {inicio} inclusiva a {fim} exclusiva",
        f"- DB2 — {metadados.get('versao', 'não verificado')}",
        f"- Isolamento JDBC — {metadados.get('isolamento', 'não verificado')}",
        f"- Limite JDBC para consultas transacionais - {configuracao['timeout_transacoes']} segundos",
        f"- Limite JDBC para os cadastros Q01 e Q01B - {configuracao['timeout_cadastros']} segundos",
        "- Consultas sequenciais em uma conexão JDBC de leitura com autocommit e sem snapshot comum",
        "- Universo principal — produtos 6 e 9, estado 0, BRL e população autorizada pela conexão",
        r"- CSV — UTF-8, cabeçalho, separador ponto e vírgula, decimal ponto e nulo \N. "
        r"Campo textual iniciado por \ recebe uma barra adicional no início",
        "- A coluna SQL identifica o texto arquivado para cada tentativa de consulta",
        "",
        "| Consulta | Estado | CSV | SQL | Linhas | Horário inicial UTC | Segundos | Observação |",
        "|---|---|---|---|---:|---|---:|---|",
    ]
    for consulta, estado in estados.items():
        csv_nome = f"{consulta}.csv" if consulta in resultados else ""
        sql_nome = f"{consulta}.sql" if f"{consulta}.sql" in arquivos.publicados else ""
        linhas.append(
            f"| {consulta} | {estado['estado']} | {csv_nome} | {sql_nome} | {estado.get('linhas', '')} | "
            f"{estado.get('inicio', '')} | {estado.get('segundos', '')} | {estado.get('obs', '')} |"
        )
    linhas.extend(("", "## Validações cruzadas", "", "| Controle | Resultado |", "|---|---|"))
    linhas.extend(f"| {controle} | {estado} |" for controle, estado in verificacoes)
    if "Q00" in resultados and resultados["Q00"].total[0] == 0:
        linhas.extend(("", "A Q00 retornou uma linha de controle com zero transações na janela."))
    if "Q02" in resultados:
        linhas.extend(("", "## Valores fora do domínio documentado na Q02", ""))
        for indicador in INDICADORES:
            linhas.append(f"- {indicador} — {resultados['Q02'].fora_dominio[indicador]} registros")
    if "erro_execucao" in metadados:
        linhas.extend(("", f"Falha na execução — {metadados['erro_execucao']}"))
    linhas.extend(("", "Os CSVs registram o comportamento observado na janela analisada."))
    arquivos.salvar_texto(MANIFESTO, "\n".join(linhas) + "\n")


def publicar_pacote(
    arquivos, fontes, consultas, configuracao, metadados, estados, resultados, recibo_zip=None
):
    verificacoes = verificar_resultados(resultados, consultas)
    if not resultados:
        situacao = "SEM_RESULTADOS"
    elif "erro_execucao" in metadados or resultados.keys() != consultas.keys():
        situacao = "PARCIAL"
    elif any(estado == "DIVERGÊNCIA" for _, estado in verificacoes):
        situacao = "COMPLETO_COM_DIVERGENCIAS"
    else:
        situacao = "COMPLETO"
    sqls = {f"{consulta}.sql" for consulta in consultas} & arquivos.publicados
    if any(f"{consulta}.sql" not in sqls for consulta in resultados):
        raise ErroValidacao("Falta o SQL correspondente a um CSV publicado.")
    escrever_manifesto(arquivos, configuracao, metadados, estados, resultados, verificacoes, situacao)
    for arquivo in FONTES_PACOTE:
        arquivos.salvar_texto(arquivo, fontes[arquivo])

    esperados = set(FONTES_PACOTE) | {MANIFESTO} | sqls | {f"{consulta}.csv" for consulta in resultados}
    caminho, sha256 = arquivos.publicar_zip(f"ESTUDO_GFP_{situacao}.zip", esperados)
    if recibo_zip is not None:
        recibo_zip.update(caminho=caminho, sha256=sha256)
    print(f"Situação do pacote - {situacao}")
    print(f"ZIP para download - {caminho}")
    print(f"SHA-256 do ZIP - {sha256}")
    arquivos.limpar_arquivos_avulsos()
    return caminho, situacao


def testar_integracao_reduzida(conector, consultas, destino, criar_hdfs, recibo_zip):
    """Homologa o caminho técnico com uma linha sintética e um ZIP separado do estudo."""
    for sql in consultas.values():
        conector._normalizar_sql(sql)
    literal = conector._literal_data(date(2026, 10, 26))
    valor = Decimal("12345678901234567890123456789.01")
    sql = (
        f"WITH P AS (SELECT {literal} AS DT_TESTE, DECIMAL('{valor}', 31, 2) AS VL_TESTE "
        "FROM SYSIBM.SYSDUMMY1) SELECT DT_TESTE, VL_TESTE FROM P"
    )
    with conector.blocos_nativos(sql, isolation_level=ISOLAMENTO, query_timeout=60) as (colunas, blocos):
        linhas = [linha for bloco in blocos for linha in bloco]
    if colunas != ("DT_TESTE", "VL_TESTE") or linhas != [("2026-10-26", valor)]:
        raise ErroValidacao("A CTE de homologação retornou dados inesperados.")

    arquivos = PastaResultados(criar_hdfs, destino, f"HOMOLOGACAO_{uuid4().hex}")
    if not arquivos.hdfs.status()["modificado_utc"].endswith("+00:00"):
        raise ErroValidacao("O HDFS retornou uma data de modificação sem UTC.")
    arquivos.salvar_texto("teste.txt", "Data e decimal da CTE conferidos.\n")
    caminho, sha256 = arquivos.publicar_zip("HOMOLOGACAO_GFP.zip", {"teste.txt"})
    recibo_zip.update(caminho=caminho, sha256=sha256)
    arquivos.limpar_arquivos_avulsos()
    print(f"Teste reduzido aprovado no driver. SQLs triados: {len(consultas)}. Linhas da CTE: 1.")
    print(f"ZIP para download - {caminho}")
    print(f"SHA-256 do ZIP - {sha256}")


def executar_estudo(conector, consultas, configuracao, fontes, criar_hdfs, recibo_zip=None):
    """Executa a extração e registra o resultado dos controles no manifesto."""
    inicio, fim = configuracao["inicio"], configuracao["fim"]
    validar_periodo(inicio, fim, conector.spark)
    transacoes = configuracao["timeout_transacoes"]
    cadastros = configuracao["timeout_cadastros"]
    if any(type(limite) is not int or limite <= 0 for limite in (transacoes, cadastros)):
        raise ValueError("Os limites JDBC devem ser números inteiros positivos de segundos.")
    if set(fontes) != set(FONTES_PACOTE) or any(not conteudo.strip() for conteudo in fontes.values()):
        raise ValueError("O empacotamento requer o notebook e o módulo desta execução.")

    agora = datetime.now(timezone.utc)
    identificador = f"{agora:%Y%m%dT%H%M%SZ}_{uuid4().hex}"
    try:
        arquivos = PastaResultados(criar_hdfs, configuracao["destino"], identificador)
    except Exception as erro:
        raise RuntimeError(
            f"Falha ao preparar o destino dos resultados. Verifique a base no HDFS da sessão. "
            f"{diagnostico_erro(conector, erro)}."
        ) from None
    print(f"Resultados do estudo em {arquivos.pasta}")
    resultados = {}
    estados = {
        consulta: {"estado": "Pendente" if consulta in consultas else "Não solicitada"}
        for consulta in PRINCIPAIS + COMPLEMENTARES
    }
    estados["Q12"] = {"estado": "Fora do escopo"}
    metadados = {"inicio": agora.isoformat(timespec="seconds")}
    try:
        with conector.conexao_nativa_leitura(ISOLAMENTO) as conexao, localcontext() as precisao:
            precisao.prec = 50
            metadados["isolamento"] = ISOLAMENTO
            versao = conexao.getMetaData().getDatabaseProductVersion()
            metadados["versao"] = re.sub(r"[\r\n|]", " ", versao)
            for consulta, sql in consultas.items():
                cronometro = perf_counter()
                estado = estados[consulta]
                estado.update(
                    estado="Em execução", inicio=datetime.now(timezone.utc).isoformat(timespec="seconds")
                )
                print(f"{consulta} em execução")
                try:
                    timeout = cadastros if consulta in CADASTROS else transacoes
                    resumo = exportar_consulta(
                        conector, conexao, arquivos, consulta, sql, inicio, fim, timeout
                    )
                    resultados[consulta] = resumo
                    estado.update(estado="Concluída" if resumo.linhas else "Vazia", linhas=resumo.linhas)
                except KeyboardInterrupt:
                    estado.update(estado="Interrompida")
                    raise
                except Exception as erro:
                    estado.update(estado="Erro", obs=diagnostico_erro(conector, erro))
                    print(f"{consulta} registrou erro no manifesto")
                finally:
                    estado["segundos"] = round(perf_counter() - cronometro, 2)
    except KeyboardInterrupt:
        metadados["erro_execucao"] = "Interrompida"
        raise
    except Exception as erro:
        metadados["erro_execucao"] = diagnostico_erro(conector, erro)
    finally:
        try:
            caminho, situacao = publicar_pacote(
                arquivos, fontes, consultas, configuracao, metadados, estados, resultados, recibo_zip
            )
        except Exception as erro:
            raise RuntimeError(
                f"O ZIP não foi publicado. Os arquivos avulsos foram preservados em {arquivos.pasta}. "
                f"Diagnóstico - {diagnostico_erro(conector, erro)}."
            ) from None

    if situacao != "COMPLETO":
        raise RuntimeError(f"Execução com pendências. Consulte o manifesto no ZIP {caminho}.")
    return caminho
