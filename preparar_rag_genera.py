"""Valida, transforma e empacota arquivos para RAG Azure no GENERA."""

from __future__ import annotations

import argparse
import json
import math
import os
import re
import tempfile
import unicodedata
import zipfile
from pathlib import Path


PERFIS = {
    "file": {".txt"},
    "vanilla-recursive": {".txt"},
    "vanilla-markdown": {".txt"},
}
ATALHOS = {
    "vanilla": "vanilla-recursive",
    "recursive": "vanilla-recursive",
    "markdown": "vanilla-markdown",
}
ARQUIVOS_DE_SISTEMA = {".ds_store", "desktop.ini", "thumbs.db"}
BULLET = re.compile(
    r"^(?P<recuo>\s*)(?:[\u2022\u25e6\u25aa\u2023\u2043\u2219\u00b7"
    r"\u25cf\u25cb\u25a0\u25a1]|[-*+])\s+"
)
CABECALHO_MARKDOWN = re.compile(r"^\s{0,3}#{1,6}\s+\S", re.MULTILINE)


def preparar_rag(
    entrada: str | Path,
    cenario: str = "file",
    saida: str | Path | None = None,
    limite_zip_mb: int = 100,
) -> dict:
    """Cria um ZIP plano e pronto para os cenários Azure do GENERA.

    Perfis aceitos: ``file``, ``vanilla-recursive`` e ``vanilla-markdown``.
    Todos aceitam exclusivamente arquivos ``.txt``. Os originais nunca são
    alterados.

    Extensões, nomes, conteúdo textual, limites e estruturas básicas dos
    formatos são validados. Toda transformação aparece no relatório retornado.
    """
    origem = Path(entrada).expanduser().resolve()
    perfil = ATALHOS.get(cenario.lower(), cenario.lower())

    if perfil not in PERFIS:
        raise ValueError(f"Cenário inválido: {cenario}. Use: {', '.join(PERFIS)}.")
    if limite_zip_mb <= 0:
        raise ValueError("O limite do ZIP deve ser maior que zero.")
    if not origem.exists():
        raise FileNotFoundError(f"Entrada não encontrada: {origem}")

    destino = (
        Path(saida).expanduser().resolve()
        if saida
        else origem.parent / f"{origem.stem}_{perfil}.zip"
    )
    if destino.suffix.lower() != ".zip":
        destino = destino.with_suffix(".zip")
    destino.parent.mkdir(parents=True, exist_ok=True)

    candidatos = (
        [origem]
        if origem.is_file()
        else sorted(
            (arquivo for arquivo in origem.rglob("*") if arquivo.is_file()),
            key=lambda arquivo: str(arquivo).casefold(),
        )
    )
    permitidos = PERFIS[perfil]
    arquivos: list[Path] = []
    ignorados: list[str] = []
    erros: list[str] = []

    for arquivo in candidatos:
        if arquivo.resolve() == destino:
            continue
        if arquivo.name.lower() in ARQUIVOS_DE_SISTEMA or arquivo.name.startswith("~$"):
            ignorados.append(str(arquivo))
            continue
        if arquivo.suffix.lower() not in permitidos:
            erros.append(
                f"Formato não aceito em {perfil}: {arquivo.name} ({arquivo.suffix or 'sem extensão'})."
            )
            continue
        arquivos.append(arquivo)

    if erros:
        raise ValueError("\n".join(erros))
    if not arquivos:
        raise ValueError(f"Nenhum arquivo compatível com {perfil} foi encontrado.")

    nomes: dict[str, Path] = {}
    for arquivo in arquivos:
        if len(arquivo.name) > 130:
            erros.append(f"Nome com mais de 130 caracteres: {arquivo.name}")
        chave = unicodedata.normalize("NFC", arquivo.name).casefold()
        if chave in nomes:
            erros.append(f"Nomes duplicados no ZIP plano: {nomes[chave]} e {arquivo}")
        else:
            nomes[chave] = arquivo
    if erros:
        raise ValueError("\n".join(erros))

    avisos: list[str] = []
    detalhes: dict[str, dict] = {}
    conteudos: dict[Path, bytes] = {}

    for arquivo in arquivos:
        bruto = arquivo.read_bytes()
        if not bruto:
            erros.append(f"Arquivo vazio: {arquivo.name}")
            continue

        transformacoes: list[str] = []
        validacoes: list[str] = ["Nome e extensão validados."]

        try:
            texto, codificacao = _decodificar(bruto)
        except UnicodeError as erro:
            erros.append(f"{arquivo.name}: {erro}")
            continue

        texto, transformacoes = _normalizar_texto(texto)
        if not texto:
            erros.append(f"Arquivo vazio após a normalização: {arquivo.name}")
            continue
        if codificacao != "utf-8":
            transformacoes.insert(0, f"Codificação {codificacao} convertida para UTF-8.")
        validacoes.append("Conteúdo textual válido e saída em UTF-8.")

        quantidade, metodo = _contar_tokens(texto)
        limite = 8000 if perfil == "file" else 8192
        detalhes_tokens = {
            "quantidade": quantidade,
            "metodo": metodo,
            "limite": limite,
        }
        if perfil == "file" and quantidade > 8000:
            erros.append(
                f"{arquivo.name}: {quantidade} tokens; limite File/Azure: 8000."
            )
        if perfil.startswith("vanilla"):
            maior_linha = max(
                (_contar_tokens(linha)[0] for linha in texto.splitlines()),
                default=0,
            )
            if maior_linha > 450:
                avisos.append(
                    f"{arquivo.name}: há linha com cerca de {maior_linha} tokens; "
                    "a recomendação é até 450."
                )
        if perfil == "vanilla-markdown" and not CABECALHO_MARKDOWN.search(texto):
            avisos.append(
                f"{arquivo.name}: nenhum cabeçalho Markdown (# Título) foi encontrado."
            )
        linhas_sem_pontuacao = _linhas_sem_pontuacao(texto)
        if linhas_sem_pontuacao:
            avisos.append(
                f"{arquivo.name}: {linhas_sem_pontuacao} linha(s) de texto podem "
                "precisar de pontuação final."
            )

        conteudos[arquivo] = texto.encode("utf-8")
        detalhes[arquivo.name] = {
            "formato": ".txt",
            "validacoes": validacoes,
            "transformacoes": transformacoes or ["Nenhuma transformação necessária."],
            "tokens": detalhes_tokens,
        }

    if erros:
        raise ValueError("\n".join(erros))

    temporario: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            prefix=f".{destino.stem}-", suffix=".tmp", dir=destino.parent, delete=False
        ) as arquivo_temporario:
            temporario = Path(arquivo_temporario.name)

        with zipfile.ZipFile(
            temporario, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9
        ) as pacote:
            for arquivo in arquivos:
                pacote.writestr(arquivo.name, conteudos[arquivo])

        tamanho = temporario.stat().st_size
        if tamanho > limite_zip_mb * 1024 * 1024:
            raise ValueError(
                f"ZIP com {tamanho / 1024 / 1024:.2f} MB; limite configurado: "
                f"{limite_zip_mb} MB."
            )
        os.replace(temporario, destino)
        temporario = None
    finally:
        if temporario is not None:
            temporario.unlink(missing_ok=True)

    if limite_zip_mb == 100:
        avisos.append(
            "Limite aplicado: 100 MB (documentação nova). O legado registra 9 MB; "
            "use limite_zip_mb=9 se o ambiente ainda aplicar o limite antigo."
        )

    return {
        "status": "PRONTO",
        "cenario": perfil,
        "modelo": "azure",
        "zip": str(destino),
        "tamanho_bytes": destino.stat().st_size,
        "arquivos": detalhes,
        "ignorados": ignorados,
        "avisos": avisos,
    }


def _decodificar(conteudo: bytes) -> tuple[str, str]:
    if conteudo.startswith((b"\xff\xfe\x00\x00", b"\x00\x00\xfe\xff")):
        return conteudo.decode("utf-32"), "utf-32"
    if conteudo.startswith((b"\xff\xfe", b"\xfe\xff")):
        return conteudo.decode("utf-16"), "utf-16"
    if conteudo.startswith(b"\xef\xbb\xbf"):
        return conteudo.decode("utf-8-sig"), "utf-8 com BOM"
    for codificacao in ("utf-8", "cp1252", "latin-1"):
        try:
            return conteudo.decode(codificacao), codificacao
        except UnicodeDecodeError:
            continue
    raise UnicodeError("não foi possível identificar a codificação textual.")


def _normalizar_texto(texto: str) -> tuple[str, list[str]]:
    transformacoes: list[str] = []

    normalizado = unicodedata.normalize("NFC", texto)
    if normalizado != texto:
        transformacoes.append("Unicode normalizado para NFC.")
    texto = normalizado

    quantidade_bom = texto.count("\ufeff")
    if quantidade_bom:
        texto = texto.replace("\ufeff", "")
        transformacoes.append(f"{quantidade_bom} marcador(es) BOM removido(s).")

    if "\r" in texto:
        texto = texto.replace("\r\n", "\n").replace("\r", "\n")
        transformacoes.append("Quebras de linha normalizadas para LF.")

    quantidade_tabs = texto.count("\t")
    if quantidade_tabs:
        texto = texto.replace("\t", " ")
        transformacoes.append(f"{quantidade_tabs} tabulação(ões) substituída(s) por espaço.")

    quantidade_controles = sum(
        caractere != "\n" and unicodedata.category(caractere) in {"Cc", "Cf"}
        for caractere in texto
    )
    if quantidade_controles:
        texto = "".join(
            caractere
            for caractere in texto
            if caractere == "\n" or unicodedata.category(caractere) not in {"Cc", "Cf"}
        )
        transformacoes.append(
            f"{quantidade_controles} caractere(s) oculto(s)/de controle removido(s)."
        )

    linhas = texto.split("\n")
    quantidade_bullets = sum(bool(BULLET.match(linha)) for linha in linhas)
    if quantidade_bullets:
        linhas = [BULLET.sub(r"\g<recuo>", linha) for linha in linhas]
        transformacoes.append(f"{quantidade_bullets} marcador(es) de bullet removido(s).")

    sem_espacos_finais = [linha.rstrip() for linha in linhas]
    if sem_espacos_finais != linhas:
        transformacoes.append("Espaços no final das linhas removidos.")
    texto = "\n".join(sem_espacos_finais)

    texto_sem_excesso, substituicoes = re.subn(r"\n[ \t]*\n(?:[ \t]*\n)+", "\n\n", texto)
    if substituicoes:
        transformacoes.append("Linhas em branco consecutivas reduzidas a uma.")
    texto = texto_sem_excesso.strip()
    return texto, transformacoes


def _linhas_sem_pontuacao(texto: str) -> int:
    total = 0
    for linha in texto.splitlines():
        linha = linha.strip()
        if not linha or linha.startswith("#") or len(linha.split()) < 3:
            continue
        if linha[-1] not in ".?!:;":
            total += 1
    return total


def _contar_tokens(texto: str) -> tuple[int, str]:
    try:
        import tiktoken  # type: ignore

        return len(tiktoken.get_encoding("cl100k_base").encode(texto)), "cl100k_base"
    except (ImportError, ModuleNotFoundError):
        return math.ceil(len(texto) / 3.5), "aproximação por caracteres"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("entrada", help="Arquivo ou pasta do corpus.")
    parser.add_argument(
        "--cenario", default="file", choices=sorted(set(PERFIS) | set(ATALHOS))
    )
    parser.add_argument("--saida", help="Caminho do ZIP de saída.")
    parser.add_argument("--limite-zip-mb", type=int, default=100)
    args = parser.parse_args()

    try:
        relatorio = preparar_rag(
            args.entrada,
            cenario=args.cenario,
            saida=args.saida,
            limite_zip_mb=args.limite_zip_mb,
        )
    except (FileNotFoundError, OSError, ValueError) as erro:
        parser.exit(1, f"ERRO: {erro}\n")

    print(json.dumps(relatorio, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
