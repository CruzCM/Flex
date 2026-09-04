#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
preparar_rag_genera_simples.py

USO:
1. Informe CAMINHO_BASE abaixo.
2. Clique em "Start" / "Run Python File" no VS Code.
3. O script gera automaticamente:
   - um .zip pronto para indexação;
   - um relatório .txt de validação.

DETECÇÃO AUTOMÁTICA:
- CAMINHO_BASE = pasta  -> modalidade FILE.
- CAMINHO_BASE = .txt   -> modalidade VANILLA.
- No VANILLA:
    - se houver cabeçalhos Markdown (#, ##, ###...), considera MarkdownHeaderTextSplitter;
    - caso contrário, considera RecursiveCharacterTextSplitter.

O script NÃO altera os arquivos originais.
"""

from pathlib import Path
from datetime import datetime
import hashlib
import re
import unicodedata
import zipfile
import tempfile
import shutil


# =============================================================================
# ÚNICA CONFIGURAÇÃO NECESSÁRIA
# =============================================================================

CAMINHO_BASE = r""  # Ex.: r"C:\Users\meu_usuario\Desktop\base_rag"

# Se deixar vazio, o ZIP será criado ao lado da pasta/arquivo de entrada.
PASTA_SAIDA = r""


# =============================================================================
# LIMITES E REGRAS DOCUMENTADAS
# =============================================================================

MAX_NOME_ARQUIVO = 130
MAX_ZIP_MB = 100

# Referência documentada para FILE no modelo indicado:
MAX_FILE_CARACTERES_APROX = 28_000

# Aviso preventivo antes do limite.
ALERTA_FILE_CARACTERES = 25_000

ARQUIVOS_SISTEMA = {".ds_store", "thumbs.db", "desktop.ini"}

RE_CABECALHO_MD = re.compile(r"^\s{0,3}(#{1,6})\s+(.+?)\s*$")
RE_BULLET = re.compile(r"^(\s*)(?:[•◦▪‣⁃∙·●○■□]|[-*+])\s+")


# =============================================================================
# FUNÇÕES
# =============================================================================

def ler_texto(path: Path):
    """Lê texto e converte codificações comuns para Unicode."""
    raw = path.read_bytes()

    # UTF-8 com ou sem BOM.
    try:
        texto = raw.decode("utf-8-sig")
        origem = "UTF-8"
        if raw.startswith(b"\xef\xbb\xbf"):
            origem = "UTF-8 com BOM"
        return texto, origem
    except UnicodeDecodeError:
        pass

    # Fallbacks comuns em arquivos Windows/legados.
    for encoding, nome in (
        ("cp1252", "Windows-1252"),
        ("latin-1", "Latin-1"),
    ):
        try:
            return raw.decode(encoding), nome
        except UnicodeDecodeError:
            pass

    raise UnicodeError("Não foi possível identificar uma codificação textual válida.")


def remover_controles(texto: str):
    """Remove caracteres invisíveis/de controle, preservando quebras de linha."""
    saida = []
    removidos = 0

    for ch in texto:
        if ch == "\n":
            saida.append(ch)
            continue

        categoria = unicodedata.category(ch)
        if categoria in {"Cc", "Cf"}:
            removidos += 1
            continue

        saida.append(ch)

    return "".join(saida), removidos


def normalizar_texto(texto: str, markdown: bool):
    """Aplica somente transformações seguras de formatação."""
    ajustes = []

    original = texto

    # Unicode canônico.
    novo = unicodedata.normalize("NFC", texto)
    if novo != texto:
        ajustes.append("Unicode normalizado.")
    texto = novo

    # Quebras de linha padronizadas.
    novo = texto.replace("\r\n", "\n").replace("\r", "\n")
    if novo != texto:
        ajustes.append("Quebras de linha normalizadas.")
    texto = novo

    # Tabs.
    qtd_tabs = texto.count("\t")
    if qtd_tabs:
        texto = texto.replace("\t", "    ")
        ajustes.append(f"{qtd_tabs} tabulação(ões) convertida(s) em espaços.")

    # Caracteres ocultos.
    texto, removidos = remover_controles(texto)
    if removidos:
        ajustes.append(f"{removidos} caractere(s) oculto(s) removido(s).")

    linhas = []
    bullets = 0

    for linha in texto.split("\n"):
        linha = linha.rstrip()

        # Preserva cabeçalhos Markdown.
        if not (markdown and RE_CABECALHO_MD.match(linha)):
            m = RE_BULLET.match(linha)
            if m:
                linha = m.group(1) + linha[m.end():]
                bullets += 1

        linhas.append(linha)

    if bullets:
        ajustes.append(f"{bullets} marcador(es) de lista removido(s).")

    # Mantém no máximo uma linha vazia entre blocos.
    compactadas = []
    anterior_vazia = False
    removidas = 0

    for linha in linhas:
        vazia = not linha.strip()

        if vazia and anterior_vazia:
            removidas += 1
            continue

        compactadas.append(linha)
        anterior_vazia = vazia

    if removidas:
        ajustes.append(f"{removidas} linha(s) em branco consecutiva(s) removida(s).")

    texto = "\n".join(compactadas).strip() + "\n"

    if texto != original and not ajustes:
        ajustes.append("Formatação normalizada.")

    return texto, ajustes


def detectar_markdown(texto: str):
    return any(RE_CABECALHO_MD.match(linha) for linha in texto.splitlines())


def validar_markdown(texto: str):
    avisos = []
    cabecalhos = []

    for numero, linha in enumerate(texto.splitlines(), start=1):
        m = RE_CABECALHO_MD.match(linha)
        if m:
            cabecalhos.append((numero, len(m.group(1)), m.group(2).strip()))

    if not cabecalhos:
        return ["Nenhum cabeçalho Markdown foi encontrado."]

    nivel_anterior = None

    for numero, nivel, titulo in cabecalhos:
        if not titulo:
            avisos.append(f"Cabeçalho vazio na linha {numero}.")

        if nivel_anterior is not None and nivel > nivel_anterior + 1:
            avisos.append(
                f"Hierarquia Markdown salta de H{nivel_anterior} para H{nivel} "
                f"na linha {numero}."
            )

        nivel_anterior = nivel

    if not any(nivel == 1 for _, nivel, _ in cabecalhos):
        avisos.append("Não foi encontrado cabeçalho principal H1 (#).")

    return avisos


def validar_pontuacao(texto: str, markdown: bool):
    """
    Apenas avisa.
    Não adiciona pontuação automaticamente para não alterar significado.
    """
    avisos = []
    finais_validos = (".", "!", "?", ":", ";", "…", ")", "]", "}", '"', "'")

    for numero, linha in enumerate(texto.splitlines(), start=1):
        s = linha.strip()

        if not s:
            continue

        if markdown and RE_CABECALHO_MD.match(s):
            continue

        # Ignora linhas curtas/títulos e URLs.
        if len(s) < 50:
            continue

        if s.lower().startswith(("http://", "https://", "www.")):
            continue

        if not s.endswith(finais_validos):
            avisos.append(
                f"Linha {numero} pode estar sem pontuação final: {s[:90]}"
            )

    return avisos


def nome_saida_seguro(nome: str, nomes_usados: set):
    """Garante nome <=130 caracteres e evita colisões."""
    ajustes = []

    nome = unicodedata.normalize("NFC", nome).strip()
    nome = "".join(
        ch for ch in nome
        if unicodedata.category(ch) not in {"Cc", "Cf"}
    )

    if not nome.lower().endswith(".txt"):
        nome += ".txt"

    if len(nome) > MAX_NOME_ARQUIVO:
        stem = Path(nome).stem
        digest = hashlib.sha1(nome.encode("utf-8")).hexdigest()[:8]
        sufixo = ".txt"
        reserva = len(digest) + len(sufixo) + 1
        stem = stem[: MAX_NOME_ARQUIVO - reserva]
        nome = f"{stem}-{digest}{sufixo}"
        ajustes.append("Nome reduzido para respeitar o limite de 130 caracteres.")

    candidato = nome
    contador = 2

    while candidato.lower() in nomes_usados:
        stem = Path(nome).stem
        sufixo = Path(nome).suffix
        extra = f"-{contador}"
        max_stem = MAX_NOME_ARQUIVO - len(sufixo) - len(extra)
        candidato = f"{stem[:max_stem]}{extra}{sufixo}"
        contador += 1

    if candidato != nome:
        ajustes.append("Nome ajustado para evitar duplicidade no ZIP.")

    nomes_usados.add(candidato.lower())
    return candidato, ajustes


def localizar_arquivos(caminho: Path, modo: str):
    """
    FILE: lê todos os .txt da pasta e subpastas e achata o ZIP.
    VANILLA: usa somente o .txt informado.
    """
    ignorados = []

    if modo == "VANILLA":
        return [caminho], ignorados

    arquivos = []

    for item in sorted(caminho.rglob("*"), key=lambda p: str(p).lower()):
        if not item.is_file():
            continue

        if item.name.lower() in ARQUIVOS_SISTEMA or item.name.startswith("~$"):
            ignorados.append(f"Arquivo de sistema ignorado: {item}")
            continue

        if item.suffix.lower() == ".txt":
            arquivos.append(item)
        else:
            ignorados.append(f"Arquivo não .txt ignorado: {item}")

    return arquivos, ignorados


def tamanho_mb(path: Path):
    return path.stat().st_size / (1024 * 1024)


# =============================================================================
# EXECUÇÃO
# =============================================================================

def main():
    print("\n=== PREPARADOR RAG GENERA ===\n")

    caminho_digitado = CAMINHO_BASE.strip()

    if not caminho_digitado:
        caminho_digitado = input(
            "Informe o caminho da pasta (File) ou do .txt (Vanilla):\n> "
        ).strip().strip('"')

    caminho = Path(caminho_digitado).expanduser().resolve()

    if not caminho.exists():
        print(f"\nERRO: caminho não encontrado:\n{caminho}")
        return

    # Detecção automática de modalidade.
    if caminho.is_dir():
        modo = "FILE"
    elif caminho.is_file() and caminho.suffix.lower() == ".txt":
        modo = "VANILLA"
    else:
        print("\nERRO: informe uma pasta ou um único arquivo .txt.")
        return

    # Saída.
    if PASTA_SAIDA.strip():
        pasta_saida = Path(PASTA_SAIDA).expanduser().resolve()
    else:
        pasta_saida = caminho.parent if caminho.is_file() else caminho.parent

    pasta_saida.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    zip_final = pasta_saida / f"RAG_PRONTO_{modo}_{timestamp}.zip"
    relatorio_final = pasta_saida / f"RAG_RELATORIO_{modo}_{timestamp}.txt"

    arquivos, ignorados = localizar_arquivos(caminho, modo)

    if not arquivos:
        print("\nERRO: nenhum arquivo .txt encontrado.")
        return

    nomes_usados = set()
    processados = []
    erros = []
    avisos_gerais = []
    relatorio_arquivos = []

    with tempfile.TemporaryDirectory(prefix="rag_genera_") as temp_dir:
        temp_path = Path(temp_dir)

        for arquivo in arquivos:
            item = {
                "origem": str(arquivo),
                "nome_final": "",
                "ajustes": [],
                "avisos": [],
                "erros": [],
            }

            try:
                texto, encoding = ler_texto(arquivo)
                item["encoding"] = encoding
            except Exception as e:
                item["erros"].append(f"Falha na leitura: {e}")
                relatorio_arquivos.append(item)
                continue

            markdown = detectar_markdown(texto) if modo == "VANILLA" else False

            texto, ajustes = normalizar_texto(texto, markdown)
            item["ajustes"].extend(ajustes)

            if not texto.strip():
                item["erros"].append("Arquivo vazio após normalização.")
                relatorio_arquivos.append(item)
                continue

            nome_final, ajustes_nome = nome_saida_seguro(
                arquivo.name,
                nomes_usados,
            )
            item["nome_final"] = nome_final
            item["ajustes"].extend(ajustes_nome)

            # Validações de File.
            if modo == "FILE":
                qtd_chars = len(texto)

                if qtd_chars > MAX_FILE_CARACTERES_APROX:
                    item["erros"].append(
                        f"Arquivo possui {qtd_chars:,} caracteres e excede a "
                        f"referência aproximada de {MAX_FILE_CARACTERES_APROX:,} "
                        "caracteres para File."
                    )
                elif qtd_chars >= ALERTA_FILE_CARACTERES:
                    item["avisos"].append(
                        f"Arquivo possui {qtd_chars:,} caracteres e está próximo "
                        "do limite de referência do modo File."
                    )

            # Validações de Vanilla.
            else:
                if markdown:
                    item["tipo_vanilla"] = "MarkdownHeaderTextSplitter"
                    item["avisos"].extend(validar_markdown(texto))
                else:
                    item["tipo_vanilla"] = "RecursiveCharacterTextSplitter"

            # Pontuação é recomendação: apenas aviso.
            pontuacao = validar_pontuacao(texto, markdown)
            if pontuacao:
                item["avisos"].append(
                    f"{len(pontuacao)} possível(is) problema(s) de pontuação final."
                )
                item["avisos"].extend(pontuacao[:8])
                if len(pontuacao) > 8:
                    item["avisos"].append(
                        f"... e mais {len(pontuacao) - 8} ocorrência(s)."
                    )

            if item["erros"]:
                relatorio_arquivos.append(item)
                continue

            destino = temp_path / nome_final
            destino.write_text(texto, encoding="utf-8", newline="\n")

            processados.append(destino)
            relatorio_arquivos.append(item)

        # Consolida erros.
        for item in relatorio_arquivos:
            for erro in item["erros"]:
                erros.append(f"{item['origem']}: {erro}")

        if erros:
            status = "BLOQUEADO"
        else:
            status = "PRONTO"

        # Gera ZIP somente se não houver erro bloqueante.
        if status == "PRONTO":
            with zipfile.ZipFile(
                zip_final,
                "w",
                compression=zipfile.ZIP_DEFLATED,
                compresslevel=9,
            ) as zf:
                for arquivo in processados:
                    zf.write(arquivo, arcname=arquivo.name)

            if tamanho_mb(zip_final) > MAX_ZIP_MB:
                erros.append(
                    f"ZIP final possui {tamanho_mb(zip_final):.2f} MB e excede "
                    f"o limite de {MAX_ZIP_MB} MB."
                )
                zip_final.unlink(missing_ok=True)
                status = "BLOQUEADO"

    # Relatório.
    linhas = [
        "RELATÓRIO DE PREPARAÇÃO RAG — GENERA",
        "",
        f"Status: {status}",
        f"Entrada: {caminho}",
        f"Modalidade detectada: {modo}",
    ]

    if modo == "VANILLA" and relatorio_arquivos:
        tipo = relatorio_arquivos[0].get("tipo_vanilla", "")
        if tipo:
            linhas.append(f"Splitter detectado: {tipo}")

    linhas.extend(
        [
            f"Arquivos .txt encontrados: {len(arquivos)}",
            f"Arquivos preparados: {len(processados) if status == 'PRONTO' else 0}",
            "",
        ]
    )

    if ignorados:
        linhas.append("ITENS IGNORADOS")
        linhas.extend(f"- {x}" for x in ignorados)
        linhas.append("")

    if erros:
        linhas.append("ERROS BLOQUEANTES")
        linhas.extend(f"- {x}" for x in erros)
        linhas.append("")

    for item in relatorio_arquivos:
        linhas.append(f"ARQUIVO: {item['origem']}")

        if item.get("nome_final"):
            linhas.append(f"Nome no ZIP: {item['nome_final']}")

        if item.get("encoding"):
            linhas.append(f"Codificação original detectada: {item['encoding']}")

        if item.get("tipo_vanilla"):
            linhas.append(f"Splitter: {item['tipo_vanilla']}")

        if item["ajustes"]:
            linhas.append("Ajustes automáticos:")
            linhas.extend(f"- {x}" for x in item["ajustes"])

        if item["avisos"]:
            linhas.append("Avisos:")
            linhas.extend(f"- {x}" for x in item["avisos"])

        if item["erros"]:
            linhas.append("Erros:")
            linhas.extend(f"- {x}" for x in item["erros"])

        linhas.append("")

    if status == "PRONTO":
        linhas.append(f"ZIP final: {zip_final}")
        linhas.append(f"Tamanho do ZIP: {tamanho_mb(zip_final):.2f} MB")

    relatorio_final.write_text("\n".join(linhas) + "\n", encoding="utf-8")

    # Resultado na tela.
    print(f"Modalidade: {modo}")

    if modo == "VANILLA" and relatorio_arquivos:
        tipo = relatorio_arquivos[0].get("tipo_vanilla", "")
        if tipo:
            print(f"Splitter: {tipo}")

    if status == "PRONTO":
        print("\nOK — base preparada com sucesso.")
        print(f"ZIP: {zip_final}")
        print(f"Relatório: {relatorio_final}")
    else:
        print("\nBASE BLOQUEADA — existem erros que não podem ser corrigidos automaticamente.")
        print(f"Relatório: {relatorio_final}")


if __name__ == "__main__":
    main()
