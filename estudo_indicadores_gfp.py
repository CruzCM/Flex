"""Extração agregada do estudo GFP, executada no driver da sessão Spark."""

import csv
import hashlib
import hmac
import io
import json
import os
import random
import re
import sqlite3
import sys
from collections import Counter, defaultdict
from contextlib import closing, contextmanager, nullcontext, suppress
from datetime import date, datetime, timedelta, timezone
from decimal import Decimal, localcontext
from pathlib import Path
from tempfile import TemporaryDirectory
from time import perf_counter
from uuid import uuid4
from zipfile import ZIP_DEFLATED, ZipFile

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


PARAMETROS_PUBLICOS = 'revisao_notebook = "2026-11-lotes-gfp"\nmodo = "HOMOLOGACAO"\ndata_inicial = "2026-11-24"\ndata_final_exclusiva = "2026-11-25"\nconsultas_selecionadas = ("Q00", "Q01", "Q01B", "Q02", "Q03", "Q04", "Q05", "Q06", "Q07", "Q08", "Q09", "Q10", "Q11")\nmcis_autorizados = []\narquivo_populacao = None  # Arquivo UTF-8 no JupyterLab, um MCI por linha.\ntamanho_amostra = None\nsemente = 42\ntamanho_lote = 10\nparticoes = []  # Segmentos da tabela principal. Vazio usa todo o recorte solicitado.\nexperimentar_formula_particao = False\nautorizar_censo = False\ntimeout_transacoes_segundos = 300\ntimeout_cadastros_segundos = 60\norcamento_global_segundos = 900\nretomar_execucao = None  # Identificador exibido na execução anterior.\nbaixar_zip_jupyterlab = True\ncluster_bbmagic = "CDP"\ndestino_hdfs = None\n'

CELULAS_DISTRIBUIDAS = {
    "a203a0a8c7cc91e765d3e827ca775844978064a4c1d51a2658af2ac1b11c0fe0",
    "1eb87976887c7d6e08cb3c7bf772a8a261b0cecf051d86d00642df7b9dc5cd97",
    "0b8fce78ef791c591d32c24e591be98f0e6cc5aa2157f6eadc46deeef793d7c4",
    "f5832def3e55448a71fe67f5dfddba2ff50b6ee4959151e16042c113a985d479",
    "cf0d35e81f6c5adb6ff4f9003c08160b25193e50113c8f9d6e6c0616ff3442f5",
    "b01d508a24b7b638d1a2ba5307f8a1232e4c2ff4f5eb334d401d84ba47e18903",
    "3874ed609d776de213deb615945db6a2b70e545b2fcbb306d99d37e9eaa30036",
    "919d396d583e9d5a8f8c22648b74775bb741c62f667ebd1e401170a6f474bd4f",
    "0ac68bf9b691517dbe20ca8ea865bc084b18ab8f7c40c51ccdeb8b73e240d30c",
    "aa2d324efea9d5b43e049799c790fd30d78247835213d8f0838c3fc77a30c231",
}


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

    # Os parâmetros editáveis podem conter MCIs e caminhos privados. O exemplar
    # distribuído no ZIP abre em homologação. A configuração efetiva fica no manifesto.
    notebook = {
        "nbformat": 4,
        "nbformat_minor": 4,
        "metadata": {"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"}},
        "cells": notebook["cells"],
    }
    limpas = []
    for celula in notebook["cells"]:
        codigo = "".join(celula["source"])
        if marcador in codigo.splitlines():
            codigo = PARAMETROS_PUBLICOS
        elif hashlib.sha256(codigo.encode()).hexdigest() not in CELULAS_DISTRIBUIDAS:
            codigo = "# Célula adicional ou modificada omitida da cópia sanitizada.\n"
        copia = {"cell_type": celula["cell_type"], "metadata": {}, "source": codigo.splitlines(True)}
        if copia["cell_type"] == "code":
            copia.update(outputs=[], execution_count=None)
        limpas.append(copia)
    notebook["cells"] = limpas
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


TODAS = PRINCIPAIS + COMPLEMENTARES
COMPARTILHADAS = ("Q00", "Q02", "Q03", "Q04", "Q09", "Q11")
BASE_Q03 = ("CD_PRD", "CD_NTZ_CTB_TRAN", "CD_TIP_TRAN", "CD_CTGR_TRAN", "CD_CTGR_TRAN_OGNL", *INDICADORES)
DIMENSOES = {
    "Q00": (),
    "Q02": INDICADORES,
    "Q03": BASE_Q03,
    "Q04": ("CD_PRD", "CD_NTZ_CTB_TRAN", *INDICADORES),
    "Q09": ("CD_INST_PCT", "NR_MCA_PCT_OPB", *BASE_Q03),
    "Q11": (
        "CD_PRD",
        "CD_NTZ_CTB_TRAN",
        "CD_TRAN_IR",
        "CD_CTGR_TRAN",
        "CD_CTGR_TRAN_OGNL",
        "IN_TRAN_IR",
        "IN_OCTR_TRAN",
        "IN_VSLO_CSM",
        "IN_DVS_LCTO",
    ),
}
LIMITES = ("DT_MIN_OBS", "DT_MAX_OBS")
SINTETICO = "WITH P AS (SELECT DATE('2024-02-29') AS DT_TESTE, DECIMAL('12345678901234567890123456789.01',31,2) AS VL_TESTE FROM SYSIBM.SYSDUMMY1) SELECT * FROM P"


def selecionar_populacao(mcis, arquivo, tamanho, semente):
    if mcis and arquivo:
        raise ValueError("Escolha uma única fonte de população.")

    def inteiro(valor):
        if not re.fullmatch(r"[0-9]{1,10}", str(valor)) or not 0 < int(valor) <= 2147483647:
            raise ValueError("A população deve conter MCIs positivos compatíveis com INTEGER.")
        return int(valor)

    if arquivo:
        try:
            with open(arquivo, encoding="utf-8-sig") as f:
                universo = sorted({inteiro(linha.strip()) for linha in f if linha.strip()})
        except OSError:
            raise ValueError("Arquivo da população indisponível.") from None
    else:
        universo = sorted({inteiro(v) for v in mcis})
    if tamanho is not None:
        if type(tamanho) is not int or not 1 <= tamanho <= len(universo) or type(semente) is not int:
            raise ValueError("Verifique o tamanho da amostra e a semente inteira.")
        return sorted(random.Random(semente).sample(universo, tamanho))
    return universo


def validar_config(c, quantidade):
    validar_periodo(c["inicio"], c["fim"])
    modo, qs, partes = c["modo"], c["consultas"], c["particoes"]
    if any(type(c[k]) is not bool for k in ("experimental", "autorizar_censo")):
        raise ValueError("As opções de censo e experimento requerem True ou False.")
    if modo not in ("HOMOLOGACAO", "AMOSTRAL", "CENSITARIO", "AUDITORIA"):
        raise ValueError("Modo desconhecido.")
    if not qs or len(set(qs)) != len(qs) or set(qs) - set(TODAS):
        raise ValueError("Selecione consultas distintas entre Q00 e Q11, incluindo Q01B.")
    for k in ("lote", "timeout_transacoes", "timeout_cadastros", "orcamento"):
        if type(c[k]) is not int or not 1 <= c[k] <= 2147483647:
            raise ValueError(f"Informe um inteiro positivo para {k}.")
    if c["lote"] > 1000:
        raise ValueError("O limite operacional é 1.000 MCIs por lote.")
    if len(set(partes)) != len(partes) or any(type(i) is not int or not 1 <= i <= 100 for i in partes):
        raise ValueError("Segmentos distintos de 1 a 100 são aceitos.")
    if modo == "AMOSTRAL" and not quantidade:
        raise ValueError("O modo amostral requer uma população autorizada.")
    if modo in ("CENSITARIO", "HOMOLOGACAO") and quantidade:
        raise ValueError("A população informada é incompatível com o modo.")
    if modo == "HOMOLOGACAO" and (partes or c["retomar"]):
        raise ValueError("Homologação não aceita segmentos ou retomada.")
    if modo in ("CENSITARIO", "AUDITORIA") and not quantidade and c["autorizar_censo"] is not True:
        raise ValueError("O censo requer autorização explícita.")
    if partes and len(partes) != 100 and "Q07" in qs:
        raise ValueError("Q07 não tem NR_PTC. Para um recorte de segmentos, retire Q07 da seleção.")
    if c["experimental"] and (not quantidade or partes):
        raise ValueError("O teste MOD requer população amostral sem recorte de partição.")
    if c["retomar"] is not None and not re.fullmatch(r"[a-f0-9]{32}", str(c["retomar"])):
        raise ValueError("Informe o identificador de retomada de 32 caracteres.")
    return c


def preparar_plano(pasta, c):
    orig = preparar_consultas(pasta, c["inicio"], c["fim"], COMPLEMENTARES)
    qs = {q: orig[q] for q in c["consultas"]}
    pasta = Path(pasta) / "03_OTIMIZADAS"
    comuns = [q for q in qs if q in COMPARTILHADAS]
    plano = dict(qs)
    if len(comuns) >= 2:
        dims = list(dict.fromkeys(k for q in comuns for k in DIMENSOES[q]))
        proj = ["T." + k for k in dims]
        if "Q00" in comuns:
            proj += ["MIN(T.DT_TRAN) AS DT_MIN_OBS", "MAX(T.DT_TRAN) AS DT_MAX_OBS"]
        proj += [
            "COUNT_BIG(*) AS QT_TRAN",
            "SUM(DECIMAL(T.VL_TRAN,31,2)) AS VL_TOTAL",
            "SUM(ABS(DECIMAL(T.VL_TRAN,31,2))) AS VL_ABS",
        ]
        base = (
            (pasta / "Base_compartilhada.sql")
            .read_text(encoding="utf8")
            .format(
                **c, projecao=", ".join(proj), agrupamento="GROUP BY " + ", ".join("T." + k for k in dims)
            )
        )
        plano = {"BASE": base, **{q: s for q, s in qs.items() if q not in comuns}}
    if c["modo"] == "AUDITORIA":
        plano.update({"REF_" + q: s for q, s in qs.items()})
    extra = (
        ", COUNT_BIG(CASE WHEN T.NR_PTC <> CASE WHEN MOD(T.CD_CLI,100)=0 THEN 100 ELSE MOD(T.CD_CLI,100) END THEN 1 END) AS FORA_FORMULA"
        if c["experimental"]
        else ""
    )
    plano["COBERTURA"] = (pasta / "Cobertura.sql").read_text(encoding="utf8").format(**c, experimento=extra)
    return qs, plano


def segmentar(sql, clientes, partes):
    """Insere os predicados junto ao intervalo, inclusive no ON da Q00 e nos dois ramos da Q08."""
    vinculos = []

    def predicado(m):
        tabela = re.findall(r"DB2GFP\.(TRAN_RLZD_INST_PCT|TRAN_INCD_CLI)\s+T\b", sql[: m.start()], re.I)[-1]
        filtros = []
        if clientes:
            filtros.append("T.CD_CLI IN (" + ", ".join("?" for _ in clientes) + ")")
            vinculos.extend(clientes)
        if partes and tabela.upper() == "TRAN_RLZD_INST_PCT":
            termos = [
                "T.NR_PTC <= 1" if p == 1 else "T.NR_PTC >= 100" if p == 100 else f"T.NR_PTC = {p}"
                for p in partes
            ]
            filtros.append("(" + " OR ".join(termos) + ")")
        return " AND ".join(filtros + [m.group()])

    return re.sub(r"T\.DT_TRAN\s*>=", predicado, sql), vinculos


@contextmanager
def ler_jdbc(conector, conexao, sql, parametros, timeout):
    if not parametros:
        with conector.blocos_nativos(
            sql, conexao=conexao, isolation_level=ISOLAMENTO, query_timeout=timeout
        ) as dados:
            yield dados
        return
    sql = conector._normalizar_sql(sql)
    stmt = conexao.prepareStatement(sql)
    rs = None
    try:
        stmt.setQueryTimeout(timeout)
        stmt.setFetchSize(1000)
        for indice, valor in enumerate(parametros, 1):
            stmt.setInt(indice, valor)
        rs = stmt.executeQuery()
        meta = rs.getMetaData()
        indices = range(1, meta.getColumnCount() + 1)
        colunas = tuple(meta.getColumnLabel(i) for i in indices)
        tipos = tuple(meta.getColumnType(i) for i in indices)

        def blocos():
            bloco = []
            while rs.next():
                bloco.append(tuple(conector._ler_campo_nativo(rs, i, t) for i, t in zip(indices, tipos)))
                if len(bloco) == 1000:
                    yield bloco
                    bloco = []
            if bloco:
                yield bloco

        yield colunas, blocos()
    finally:
        erro_ativo = sys.exc_info()[0] is not None
        try:
            if rs is not None:
                with suppress(Exception) if erro_ativo else nullcontext():
                    rs.close()
        finally:
            with suppress(Exception) if sys.exc_info()[0] is not None else nullcontext():
                stmt.close()


def texto(v):
    return format(v, "f") if isinstance(v, Decimal) else str(v) if v is not None else None


def agora():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def resumo_hash(dados):
    return hashlib.sha256(json.dumps(dados, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def unidades(plano, c, clientes):
    if c["modo"] == "HOMOLOGACAO":
        yield 0, "TESTE", SINTETICO, [], 0
        return
    trans = [q for q in plano if q.split("_", 1)[-1] not in CADASTROS and q != "COBERTURA"]
    for op in plano:
        if op.split("_", 1)[-1] in CADASTROS:
            yield 0, op, plano[op], [], 0
    if not trans:
        return
    if clientes:
        for pos in range(0, len(clientes), c["lote"]):
            lote = clientes[pos : pos + c["lote"]]
            for op in ["COBERTURA", *trans]:
                sql, binds = segmentar(plano[op], lote, c["particoes"])
                yield pos // c["lote"] + 1, op, sql, binds, len(lote)
                if op == "COBERTURA" and c["experimental"]:
                    candidatos = sorted({mci % 100 or 100 for mci in lote})
                    filtros = ",".join("?" for n in candidatos)
                    yield (
                        pos // c["lote"] + 1,
                        "TESTE_MOD",
                        sql.replace("T.DT_TRAN >=", f"T.NR_PTC IN ({filtros}) AND T.DT_TRAN >="),
                        binds + candidatos,
                        len(lote),
                    )
    else:
        for op in trans:
            if op.split("_", 1)[-1] == "Q07":
                yield 0, op, plano[op], [], 0
        for parte in sorted(c["particoes"] or range(1, 101)):
            for op in trans:
                if op.split("_", 1)[-1] != "Q07":
                    sql, binds = segmentar(plano[op], [], [parte])
                    yield parte, op, sql, binds, 0


def quantidade_lotes(c, clientes):
    if c["modo"] == "HOMOLOGACAO" or set(c["consultas"]) <= set(CADASTROS):
        return 0
    if clientes:
        return (len(clientes) + c["lote"] - 1) // c["lote"]
    if set(c["consultas"]) <= {*CADASTROS, "Q07"}:
        return 1
    return len(c["particoes"]) or 100


def checar_colunas(op, colunas):
    if (
        not colunas
        or len(set(colunas)) != len(colunas)
        or any(not re.fullmatch("[A-Z][A-Z0-9_]*", k) or COLUNAS_RESTRITAS.search(k) for k in colunas)
    ):
        raise ErroValidacao("Cabeçalho inseguro ou duplicado.")
    if op == "TESTE" and colunas != ["DT_TESTE", "VL_TESTE"]:
        raise ErroValidacao("Cabeçalho da CTE sintética divergente.")


class SomaExata:
    def __init__(self):
        self.valor = None

    def step(self, v):
        if v is not None:
            self.valor = Decimal(v) if self.valor is None else self.valor + Decimal(v)

    def finalize(self):
        return texto(self.valor.normalize()) if self.valor is not None else None


def reduzir(op, cols, tabela, cfg, compartilhada=False):
    """As dimensões são TEXT (incluindo NULL); SOMA usa Decimal, nunca REAL."""
    q = op.split("_", 1)[-1]

    def agrupar(dimensoes, medidas):
        return (
            "SELECT "
            + ", ".join([*dimensoes, *medidas])
            + " FROM "
            + tabela
            + (" GROUP BY " + ", ".join(dimensoes) if dimensoes else "")
        )

    if q == "Q00":
        ini, fim = cfg["inicio"], cfg["fim"]
        dias = (date.fromisoformat(fim) - date.fromisoformat(ini)).days
        return agrupar(
            [],
            [
                f"'{ini}' AS DT_INI",
                f"'{fim}' AS DT_FIM_EXCL",
                f"'{dias}' AS QT_DIAS",
                "MIN(DT_MIN_OBS) AS DT_MIN_OBS",
                "MAX(DT_MAX_OBS) AS DT_MAX_OBS",
                *(f"COALESCE(SOMA({k}),'0') AS {k}" for k in METRICAS),
            ],
        )
    if q in CADASTROS:
        return f"SELECT * FROM {tabela} ORDER BY CAST({cols[0]} AS INTEGER)"
    if compartilhada and q == "Q04":
        # Reutiliza os CASE originais, substituindo a unidade de contagem pela multiplicidade.
        s = cfg["sql_q04"].rsplit("SELECT ", 1)[1].split("FROM B")[0]
        s = (
            s.replace("COUNT_BIG(*)", "SOMA(QT_TRAN)")
            .replace("COUNT_BIG(CASE", "SOMA(CASE")
            .replace("THEN 1 END", "THEN QT_TRAN ELSE '0' END")
        )
        s = re.sub(r"ABS\(DECIMAL\(VL_TRAN,\s*31,\s*2\)\)", "VL_ABS", s)
        s = re.sub(r"DECIMAL\(0,\s*31,\s*2\)", "'0'", s).replace("SUM(", "SOMA(")
        return f"SELECT {s} FROM {tabela} GROUP BY CD_PRD, CD_NTZ_CTB_TRAN"
    if q == "Q04":
        medidas = [k for k in cols if k.startswith(("QT_", "VL_"))]
    elif q == "Q08":
        medidas = ["QT_ORIGINAIS", "QT_DERIVADOS", "VL_ORIGINAIS", "VL_DERIVADOS"]
    else:
        medidas = METRICAS
    dims = DIMENSOES[q] if compartilhada else [k for k in cols if k not in medidas]
    return agrupar(dims, [f"SOMA({k}) AS {k}" for k in medidas])


class OrcamentoEsgotado(Exception):
    pass


def produzir_checkpoint(local, conector, sql, binds, limite, op, c, etapa, prazo, chave):
    etapa[0] = "conexão"
    inicio_leitura, tic = agora(), perf_counter()
    with conector.conexao_nativa_leitura(ISOLAMENTO) as conn:
        # A V3 aplica setReadOnly(True), setAutoCommit(True) e confirma o nível JDBC.
        if not conn.isReadOnly() or not conn.getAutoCommit() or conn.getTransactionIsolation() != 2:
            raise ErroValidacao("Somente leitura, autocommit ou READ_COMMITTED não confirmado.")
        restante = int(prazo - perf_counter())
        if restante < 1:
            raise OrcamentoEsgotado()
        limite = min(limite, restante)
        etapa[0] = "execução JDBC"
        with ler_jdbc(conector, conn, sql, binds, limite) as (cabecalho, blocos), ZipFile(
            local, "w", ZIP_DEFLATED
        ) as z:
            cols = [k.upper() for k in cabecalho]
            checar_colunas(op, cols)
            numero = 0
            bytes_dados = 0
            base = op.split("_", 1)[-1]
            controle = ResumoConsulta(base, c["inicio"], c["fim"]) if base in TODAS else None
            with z.open("linhas.jsonl", "w", force_zip64=True) as out:
                for bloco in blocos:
                    for r in bloco:
                        valores = [texto(v) for v in r]
                        if len(valores) != len(cols):
                            raise ErroValidacao("Quantidade de campos incompatível.")
                        linha = dict(zip(cols, valores))
                        if controle:
                            controle.adicionar(linha)
                        elif base == "BASE":
                            ler_metricas(linha)
                        elif base == "TESTE" and valores != [
                            "2024-02-29",
                            "12345678901234567890123456789.01",
                        ]:
                            raise ErroValidacao("Data ou decimal divergiu na CTE sintética.")
                        registro = (
                            json.dumps(valores, ensure_ascii=False, separators=(",", ":")) + "\n"
                        ).encode()
                        out.write(registro)
                        bytes_dados += len(registro)
                        numero += 1
            if op in ("TESTE", "TESTE_MOD", "COBERTURA", "Q00", "REF_Q00") and numero != 1:
                raise ErroValidacao("Esperada uma linha de controle.")
            meta = {
                "chave": chave,
                "colunas": cols,
                "linhas": numero,
                "bytes_serializados": bytes_dados,
                "inicio_leitura_utc": inicio_leitura,
                "segundos_leitura": round(perf_counter() - tic, 3),
            }
            z.writestr("meta.json", json.dumps(meta))
    return meta


def incorporar(banco, local, op, chave):
    with ZipFile(local) as z, banco:
        meta = json.loads(z.read("meta.json"))
        if meta["chave"] != chave:
            raise ErroValidacao("Checkpoint de outra unidade ou revisão.")
        cols = meta["colunas"]
        checar_colunas(op, cols)
        tabela = "dados_" + op
        # O Db2 compara chaves de caracteres preenchendo à direita com espaços.
        banco.execute(
            f"CREATE TABLE IF NOT EXISTS {tabela} ("
            + ", ".join(k + " TEXT COLLATE RTRIM" for k in cols)
            + ")"
        )
        if [r[1] for r in banco.execute("PRAGMA table_info(" + tabela + ")")] != cols:
            raise ErroValidacao("Cabeçalhos incompatíveis entre lotes.")
        with z.open("linhas.jsonl") as entrada:
            antes = banco.total_changes
            banco.executemany(
                f"INSERT INTO {tabela} VALUES (" + ", ".join("?" for k in cols) + ")",
                (json.loads(linha) for linha in entrada),
            )
        if banco.total_changes - antes != meta["linhas"]:
            raise ErroValidacao("Contagem do checkpoint divergente.")
    return meta


def escrever_csv(arquivos, q, cursor, c, nome=None):
    cols = [d[0] for d in cursor.description]
    checar_colunas(q, cols)
    resumo = ResumoConsulta(q, c["inicio"], c["fim"])
    with arquivos.escrever(nome or q + ".csv") as out:
        buffer = io.StringIO()
        escritor = csv.writer(buffer, delimiter=";")
        escritor.writerow(cols)
        for r in cursor:
            valores = [
                format(Decimal(v), ".2f") if k.startswith("VL_") and v is not None else texto(v)
                for k, v in zip(cols, r)
            ]
            resumo.adicionar(dict(zip(cols, valores)))
            escritor.writerow([codificar_campo(v) for v in valores])
            if buffer.tell() >= 65536:
                out.write(buffer.getvalue())
                buffer.seek(0)
                buffer.truncate()
        out.write(buffer.getvalue())
    return resumo


def carregar_populacao_driver(criar_hdfs, pasta):
    if pasta is None:
        return []
    h = criar_hdfs(diretorio_base=pasta)
    with TemporaryDirectory() as d:
        arquivo = Path(d) / "populacao"
        try:
            h.copiar_para_driver("entrada", arquivo)
            return selecionar_populacao([], arquivo, None, 0)
        finally:
            if h.existe("entrada"):
                h.remover("entrada")
            criar_hdfs().remover(pasta)


def executar_estudo(
    conector,
    consultas,
    configuracao,
    fontes,
    criar_hdfs,
    recibo_zip=None,
    *,
    plano=None,
    clientes=(),
    sessao_spark=None,
):
    """Cada unidade tem conexão e checkpoint próprios. Publicação funcionalmente parcial é recuperável."""
    c = dict(configuracao)
    # O calendário do driver governa também homologações e chamadas diretas.
    t0 = perf_counter()
    spark = sessao_spark if sessao_spark is not None else conector.spark
    validar_periodo(c["inicio"], c["fim"], spark)
    if plano is None:
        raise ValueError("Prepare um plano com modo de execução explícito.")
    validar_config(c, len(clientes))
    if clientes and (
        list(clientes) != sorted(set(clientes))
        or any(type(v) is not int or not 0 < v <= 2147483647 for v in clientes)
    ):
        raise ValueError("A população selecionada deve conter MCIs INTEGER únicos em ordem crescente.")
    if set(consultas) != set(c["consultas"]) or set(fontes) != set(FONTES_PACOTE):
        raise ValueError("Fontes ou seleção inconsistentes.")
    c["sql_q04"] = consultas.get("Q04")
    base = criar_hdfs(diretorio_base=c["destino"])
    if c["destino"] is None:
        projeto = base.criar_diretorio("ESTUDO_INDICADORES_GFP", existir_ok=True)
        diretorio = base.criar_diretorio(f"{projeto}/04_RESULTADOS_DB2", existir_ok=True)
    else:
        diretorio = base.base
    id_plano = c["retomar"] or uuid4().hex
    caminho = f"{diretorio}/{id_plano}"
    if not c["retomar"]:
        base.criar_diretorio(caminho)
    h = criar_hdfs(diretorio_base=caminho)
    identidade = {
        k: c[k] for k in ("modo", "inicio", "fim", "consultas", "lote", "particoes", "experimental")
    }
    if c["retomar"]:
        contrato = json.loads(h.ler_texto("contrato.json"))
    else:
        contrato = {"sal": uuid4().hex}
    assinatura = hmac.new(
        contrato["sal"].encode(),
        resumo_hash(
            [
                identidade,
                clientes,
                consultas,
                plano,
                fontes["estudo_indicadores_gfp.py"],
                [os.getenv(k) for k in ("DB2_HOST", "DB2_PORTA", "DB2_DATABASE", "DB2_USER")],
            ]
        ).encode(),
        "sha256",
    ).hexdigest()
    if c["retomar"]:
        if not hmac.compare_digest(contrato["assinatura"], assinatura):
            raise ValueError("Retomada incompatível com população, revisão, SQL ou parâmetros.")
    else:
        h.salvar_texto("contrato.json", json.dumps(dict(contrato, assinatura=assinatura)))
    arquivos = PastaResultados(criar_hdfs, caminho, "tentativa_" + uuid4().hex)
    lotes = quantidade_lotes(c, clientes)
    populacao = len(clientes) if clientes or c["modo"] == "HOMOLOGACAO" else "censo sem enumeração"
    print(
        f"Modo {c['modo']} | {c['inicio']} até {c['fim']} exclusivo | clientes {populacao} | lotes {lotes} | retomada {id_plano}"
    )
    print("Resultados", arquivos.pasta)
    eventos = []
    colunas = {}
    esperados = Counter()
    concluidos = Counter()
    sqls = set()
    interrompido = False
    with TemporaryDirectory() as d, closing(
        sqlite3.connect(str(Path(d) / "agregados.sqlite"))
    ) as banco, localcontext() as precisao:
        precisao.prec = 64
        banco.create_aggregate("SOMA", 1, SomaExata)
        local = Path(d) / "unidade.zip"
        for lote, op, sql, binds, nclientes in unidades(plano, c, clientes):
            esperado = f"L{lote}_{op}.zip"
            chave = resumo_hash([assinatura, lote, op, sql])
            esperados[op] += 1
            ev = {"lote": lote, "operacao": op, "inicio": agora(), "clientes": nclientes}
            eventos.append(ev)
            tic = perf_counter()
            etapa = ["checkpoint"]
            db = None
            try:
                if local.exists():
                    local.unlink()
                if c["retomar"] and h.existe(esperado):
                    h.copiar_para_driver(esperado, local)
                    ev["origem"] = "checkpoint"
                else:
                    restante = c["orcamento"] - (perf_counter() - t0)
                    if interrompido or restante < 1:
                        ev["estado"] = (
                            "Interrompida" if interrompido else "Não executada por orçamento de tempo"
                        )
                        continue
                    print(f"{ev['inicio']} | lote {lote}/{lotes} | {op} em execução")
                    limite = min(
                        int(restante),
                        c["timeout_cadastros"]
                        if op.split("_", 1)[-1] in CADASTROS
                        else c["timeout_transacoes"],
                    )
                    etapa[0] = "conexão"
                    db = conector() if callable(conector) else conector
                    if op == "TESTE":
                        etapa[0] = "homologação da parametrização"
                        if db._literal_data(date(2024, 2, 29)) != "DATE('2024-02-29')":
                            raise ErroValidacao(
                                "Normalização DATE divergente após carregar os gerenciadores."
                            )
                        for modelo in {*plano.values(), *consultas.values()}:
                            modelo, marcadores = segmentar(modelo, [1], [])
                            if db._normalizar_sql(modelo).count("?") != len(marcadores):
                                raise ErroValidacao("Aridade de parâmetros divergente.")
                    produzir_checkpoint(
                        local, db, sql, binds, limite, op, c, etapa, t0 + c["orcamento"], chave
                    )
                    etapa[0] = "publicação do checkpoint"
                    h.copiar_do_driver(local, esperado)
                    ev["origem"] = "JDBC"
                etapa[0] = "validação do checkpoint"
                meta = incorporar(banco, local, op, chave)
                colunas[op] = meta["colunas"]
                concluidos[op] += 1
                ev.update(
                    estado="Concluída" if meta["linhas"] else "Vazia",
                    linhas=meta["linhas"],
                    bytes_serializados=meta["bytes_serializados"],
                )
                ev.update(
                    inicio_leitura_utc=meta["inicio_leitura_utc"], segundos_leitura=meta["segundos_leitura"]
                )
                if op in ("COBERTURA", "TESTE_MOD"):
                    ev["medidas"] = dict(
                        zip(
                            meta["colunas"],
                            banco.execute(f"SELECT * FROM dados_{op} ORDER BY rowid DESC LIMIT 1").fetchone(),
                        )
                    )
            except OrcamentoEsgotado:
                ev["estado"] = "Não executada por orçamento de tempo"
            except KeyboardInterrupt:
                interrompido = True
                ev.update(estado="Interrompida", etapa=etapa[0])
            except Exception as erro:
                diag = diagnostico_erro(db, erro)
                ev.update(
                    estado="Timeout"
                    if re.search(r"Timeout|57014|HYT0[01]|SQLCODE -905", diag, re.I)
                    else "Erro",
                    etapa=etapa[0],
                    diagnostico=diag,
                )
            finally:
                if etapa[0] != "conexão" and (
                    ev.get("origem") or etapa[0] == "execução JDBC" or etapa[0] == "publicação do checkpoint"
                ):
                    nome = op + "_" + hashlib.sha256(sql.encode()).hexdigest()[:16] + ".sql"
                    try:
                        if nome not in sqls:
                            arquivos.salvar_texto(nome, sql + "\n")
                            sqls.add(nome)
                        ev["sql"] = nome
                    except Exception as erro:
                        ev.update(estado="Erro", etapa="arquivo SQL", diagnostico=type(erro).__name__)
                ev.update(
                    fim=agora(),
                    segundos=round(perf_counter() - tic, 3),
                    acumulado=round(perf_counter() - t0, 3),
                )
                print(
                    f"{ev['fim']} | lote {lote} {op} | {ev['estado']} | {ev.get('linhas', 0)} linhas | {ev['segundos']} s | acumulado {ev['acumulado']} s"
                )
        caminho_zip = finalizar(
            banco,
            arquivos,
            c,
            fontes,
            consultas,
            plano,
            eventos,
            colunas,
            esperados,
            concluidos,
            clientes,
            id_plano,
            recibo_zip,
            sqls,
        )
        print(f"Conclusão {agora()} | duração da execução no driver {perf_counter() - t0:.2f} s")
        return caminho_zip


def finalizar(
    banco,
    arquivos,
    c,
    fontes,
    consultas,
    plano,
    eventos,
    colunas,
    esperados,
    concluidos,
    clientes,
    id_plano,
    recibo,
    sqls,
):
    estados = {q: "Não solicitada" for q in TODAS}
    estados["Q12"] = "Fora do escopo"
    resultados = {}
    comparacoes = {}
    erros = {}
    csvs = set()
    homo = c["modo"] == "HOMOLOGACAO"
    for q in () if homo else consultas:
        op = q if q in plano else "BASE"
        ref = "REF_" + q
        original = None
        if c["modo"] == "AUDITORIA":
            comparacoes[q] = "PENDENTE"
            if concluidos[ref]:
                try:
                    sql_ref = reduzir(ref, colunas[ref], "dados_" + ref, c)
                    nome_ref = ref + "_consolidacao_driver.sql"
                    arquivos.salvar_texto(nome_ref, sql_ref + "\n")
                    sqls.add(nome_ref)
                    banco.execute(f"CREATE TABLE final_{ref} AS " + sql_ref)
                    original = f"SELECT * FROM final_{ref}"
                    if q in CADASTROS:
                        original += f" ORDER BY CAST({colunas[ref][0]} AS INTEGER)"
                    escrever_csv(arquivos, q, banco.execute(original), c, nome=ref + ".csv")
                    csvs.add(ref + ".csv")
                except Exception as erro:
                    erros[ref] = type(erro).__name__
                    original = None
        if not concluidos[op]:
            motivos = {e["estado"] for e in eventos if e["operacao"] == op}
            estados[q] = next(iter(motivos)) if len(motivos) == 1 else "Parcial"
            continue
        try:
            sql = reduzir(q, colunas[op], "dados_" + op, c, op == "BASE")
            nome_local = q + "_consolidacao_driver.sql"
            arquivos.salvar_texto(nome_local, sql + "\n")
            sqls.add(nome_local)
            if c["modo"] == "AUDITORIA":
                banco.execute(f"CREATE TABLE final_{q} AS " + sql)
                sql = f"SELECT * FROM final_{q}"
                if q in CADASTROS:
                    sql += f" ORDER BY CAST({colunas[op][0]} AS INTEGER)"
            resumo = escrever_csv(arquivos, q, banco.execute(sql), c)
            csvs.add(q + ".csv")
            estados[q] = (
                "Parcial" if concluidos[op] != esperados[op] else "Concluída" if resumo.linhas else "Vazia"
            )
            if estados[q] != "Parcial":
                resultados[q] = resumo
            if original and concluidos[ref] == esperados[ref] and estados[q] != "Parcial":
                if [d[0] for d in banco.execute(original).description] != [
                    d[0] for d in banco.execute(sql).description
                ]:
                    raise ErroValidacao("Cabeçalhos divergentes na auditoria.")
                campos_cmp = (
                    ", ".join(colunas[ref])
                    if q in CADASTROS
                    else ", ".join(k + " COLLATE RTRIM" for k in colunas[ref])
                )
                difere = any(
                    banco.execute(
                        "SELECT 1 FROM (" + a + " EXCEPT SELECT * FROM (" + b + ")) LIMIT 1"
                    ).fetchone()
                    for a, b in (
                        (f"SELECT {campos_cmp} FROM ({sql})", original),
                        (f"SELECT {campos_cmp} FROM ({original})", sql),
                    )
                )
                comparacoes[q] = "DIVERGÊNCIA" if difere else "OK"
        except Exception as erro:
            estados[q] = "Erro"
            erros[q] = type(erro).__name__
            resultados.pop(q, None)
    if homo and concluidos["TESTE"]:
        arquivos.salvar_texto("teste.txt", "CTE de data e DECIMAL(31,2) conferida em JDBC de leitura.\n")
        csvs.add("teste.txt")
    controles = [] if homo else verificar_resultados(resultados, consultas)
    cobertura = {}
    if clientes:
        lotes = {}
        for e in eventos:
            if e["clientes"]:
                lotes.setdefault(e["lote"], []).append(e)
        ok = {"Vazia", "Concluída"}
        processados = sum(es[0]["clientes"] for es in lotes.values() if all(e["estado"] in ok for e in es))
        falhas = sum(
            es[0]["clientes"]
            for es in lotes.values()
            if any(e["estado"] in ("Timeout", "Erro", "Interrompida") for e in es)
        )
        conhecidos = sum(e["clientes"] for e in eventos if e["operacao"] == "COBERTURA" and e["estado"] in ok)
        dados = 0
        if "COBERTURA" in colunas:
            dados = int(banco.execute("SELECT SOMA(COM_DADOS) FROM dados_COBERTURA").fetchone()[0])
            cobertura["transacoes_no_periodo"] = int(
                banco.execute("SELECT SOMA(TRANSACOES) FROM dados_COBERTURA").fetchone()[0]
            )
            if c["experimental"]:
                cobertura["linhas_fora_da_formula"] = int(
                    banco.execute("SELECT SOMA(FORA_FORMULA) FROM dados_COBERTURA").fetchone()[0]
                )
                for lote, es in lotes.items():
                    par = {e["operacao"]: e.get("medidas") for e in es}
                    antes, depois = par.get("COBERTURA"), par.get("TESTE_MOD")
                    if antes is None or depois is None:
                        comparacoes[f"MOD lote {lote}"] = "PENDENTE"
                    else:
                        comparacoes[f"MOD lote {lote}"] = (
                            "OK" if antes == depois and int(antes["FORA_FORMULA"]) == 0 else "DIVERGÊNCIA"
                        )
        cobertura.update(
            solicitados=len(clientes),
            processados=processados,
            com_falhas=falhas,
            pendentes=len(clientes) - processados - falhas,
            com_dados=dados,
            sem_dados=conhecidos - dados,
            presenca_desconhecida=len(clientes) - conhecidos,
        )
    if not csvs:
        situacao = "SEM_RESULTADOS"
    elif erros or any(estado not in ("Concluída", "Vazia") for estado in (e["estado"] for e in eventos)):
        situacao = "PARCIAL"
    elif "DIVERGÊNCIA" in [*comparacoes.values(), *(v for _, v in controles)]:
        situacao = "COMPLETO_COM_DIVERGENCIAS"
    else:
        situacao = "COMPLETO"
    publico = {
        k: c[k]
        for k in (
            "modo",
            "inicio",
            "fim",
            "consultas",
            "particoes",
            "lote",
            "orcamento",
            "timeout_transacoes",
            "timeout_cadastros",
            "experimental",
        )
    }
    for k in ("semente", "tamanho_amostra"):
        if type(c.get(k)) is int:
            publico[k] = c[k]
    if c.get("fonte") in ("arquivo autorizado", "lista explícita", "sem lista"):
        publico["fonte"] = c["fonte"]
    diagnostico = {
        "configuracao": publico,
        "leituras_por_consulta": {
            q: {
                "operacao": q if q in plano else "BASE",
                "unidades_previstas": esperados[q if q in plano else "BASE"],
                "unidades_concluidas": concluidos[q if q in plano else "BASE"],
            }
            for q in consultas
            if not homo
        },
        "desempenho_por_lote": {},
        "retomada": id_plano,
        "situacao_funcional": situacao,
        "consultas": estados,
        "cobertura": cobertura,
        "controles": controles,
        "comparacao_independente": comparacoes,
        "erros_consolidacao": erros,
        "operacoes": eventos,
        "inventario": sorted(set(FONTES_PACOTE) | csvs | sqls | {MANIFESTO, "Execucao.json"}),
    }
    for e in eventos:
        lote = diagnostico["desempenho_por_lote"].setdefault(
            e["lote"],
            {
                "segundos": 0,
                "tentativas_sql": 0,
                "checkpoints_recuperados": 0,
                "linhas_agregadas": 0,
                "bytes_serializados": 0,
                "falhas": 0,
            },
        )
        lote["segundos"] = round(lote["segundos"] + e["segundos"], 3)
        lote["tentativas_sql"] += int("sql" in e and e.get("origem") != "checkpoint")
        lote["checkpoints_recuperados"] += int(
            e.get("origem") == "checkpoint" and e["estado"] in ("Concluída", "Vazia")
        )
        lote["linhas_agregadas"] += e.get("linhas", 0)
        lote["bytes_serializados"] += e.get("bytes_serializados", 0)
        lote["falhas"] += int(e["estado"] in ("Erro", "Timeout", "Interrompida"))
    arquivos.salvar_texto("Execucao.json", json.dumps(diagnostico, ensure_ascii=False, indent=1))
    linhas = [
        "# Manifesto de execução",
        "",
        f"Modo {c['modo']} · {situacao}",
        f"Janela [{c['inicio']}, {c['fim']})",
        f"Identificador para retomada {id_plano}",
        "",
        "O arquivo Execucao.json registra população agregada, cobertura por unidade, verificações, SQL utilizado e tempos UTC.",
        "Cada leitura usa READ_COMMITTED com autocommit e conexão própria. A execução e a retomada não compartilham snapshot.",
        r"CSV UTF-8, separador ponto e vírgula, nulo \N e escape de barra inicial.",
        "Cobertura de clientes considera a tabela principal no período e nos segmentos selecionados, antes de produto, estado e moeda.",
        "Resultados parciais incluem apenas unidades concluídas. Controles entre saídas de BASE compartilham a mesma leitura.",
        "",
    ]
    linhas += [f"- {q} — {s}" for q, s in estados.items()]
    if "Q02" in resultados:
        linhas += ["", "Valores fora do domínio na Q02"] + [
            f"- {k} — {resultados['Q02'].fora_dominio[k]}" for k in INDICADORES
        ]
    arquivos.salvar_texto(MANIFESTO, "\n".join(linhas) + "\n")
    for nome in FONTES_PACOTE:
        arquivos.salvar_texto(nome, fontes[nome])
    caminho, sha = arquivos.publicar_zip(
        "ESTUDO_GFP_" + c["modo"] + "_" + situacao + ".zip", set(diagnostico["inventario"])
    )
    if recibo is not None:
        recibo.update(
            caminho=caminho, sha256=sha, situacao=situacao, publicacao="PUBLICADO", retomada=id_plano
        )
    print(f"{situacao} | ZIP publicado {caminho} | SHA-256 {sha}")
    arquivos.limpar_arquivos_avulsos()
    return caminho
