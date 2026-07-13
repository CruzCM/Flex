#!/usr/bin/env python3
"""Converte um subconjunto seguro de Markdown para PDF.

Dependência externa única:
    pip install reportlab

Recursos suportados:
- Títulos: # até ######
- Parágrafos
- Negrito: **texto**
- Itálico: *texto*
- Código inline: `codigo`
- Listas com -, * ou +
- Listas numeradas: 1. item
- Citações: > texto
- Blocos de código com ``` ou ~~~
- Linha horizontal: ---, *** ou ___

Deliberadamente não suporta HTML, imagens, links clicáveis, inclusões,
filtros, JavaScript ou carregamento de recursos externos.
"""

from __future__ import annotations

import argparse
import html
import os
import re
import tempfile
from pathlib import Path

from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    HRFlowable,
    Paragraph,
    Preformatted,
    SimpleDocTemplate,
    Spacer,
)

MAX_INPUT_BYTES = 2_000_000
MAX_LINES = 50_000
MAX_LINE_CHARS = 20_000

HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
BULLET_RE = re.compile(r"^\s{0,3}[-+*]\s+(.+)$")
NUMBERED_RE = re.compile(r"^\s{0,3}(\d{1,6})[.)]\s+(.+)$")
FENCE_RE = re.compile(r"^\s*(`{3,}|~{3,})(?:[^`]*)?$")
HR_RE = re.compile(r"^\s{0,3}((\*\s*){3,}|(-\s*){3,}|(_\s*){3,})$")


def safe_inline(text: str) -> str:
    """Escapa tudo e reintroduz apenas três marcações permitidas."""
    escaped = html.escape(text, quote=True)

    # O conteúdo já está escapado; as tags abaixo são criadas pelo programa.
    escaped = re.sub(
        r"`([^`\n]{1,10000})`",
        r'<font name="Courier">\1</font>',
        escaped,
    )
    escaped = re.sub(r"\*\*([^*\n]+?)\*\*", r"<b>\1</b>", escaped)
    escaped = re.sub(
        r"(?<!\*)\*([^*\n]+?)\*(?!\*)",
        r"<i>\1</i>",
        escaped,
    )
    return escaped


def make_styles() -> dict[str, ParagraphStyle]:
    base = getSampleStyleSheet()

    styles: dict[str, ParagraphStyle] = {
        "body": ParagraphStyle(
            "SafeBody",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=10.5,
            leading=15,
            spaceAfter=7,
            allowWidows=0,
            allowOrphans=0,
        ),
        "bullet": ParagraphStyle(
            "SafeBullet",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=10.5,
            leading=15,
            leftIndent=14,
            firstLineIndent=-10,
            spaceAfter=4,
        ),
        "quote": ParagraphStyle(
            "SafeQuote",
            parent=base["BodyText"],
            fontName="Helvetica-Oblique",
            fontSize=10.5,
            leading=15,
            leftIndent=16,
            rightIndent=8,
            borderWidth=0,
            spaceAfter=7,
        ),
        "code": ParagraphStyle(
            "SafeCode",
            parent=base["Code"],
            fontName="Courier",
            fontSize=8.5,
            leading=11,
            leftIndent=8,
            rightIndent=8,
            spaceBefore=4,
            spaceAfter=8,
        ),
    }

    heading_sizes = {1: 22, 2: 18, 3: 15, 4: 13, 5: 11.5, 6: 10.5}
    for level, size in heading_sizes.items():
        styles[f"h{level}"] = ParagraphStyle(
            f"SafeHeading{level}",
            parent=base[f"Heading{min(level, 4)}"],
            fontName="Helvetica-Bold",
            fontSize=size,
            leading=size * 1.25,
            spaceBefore=12 if level > 1 else 4,
            spaceAfter=7,
            alignment=TA_CENTER if level == 1 else 0,
            keepWithNext=1,
        )

    return styles


def markdown_to_story(markdown: str):
    styles = make_styles()
    story = []
    paragraph_lines: list[str] = []
    code_lines: list[str] = []
    fence_char: str | None = None
    fence_len = 0

    def flush_paragraph() -> None:
        nonlocal paragraph_lines
        if paragraph_lines:
            text = " ".join(part.strip() for part in paragraph_lines).strip()
            if text:
                story.append(Paragraph(safe_inline(text), styles["body"]))
            paragraph_lines = []

    def flush_code() -> None:
        nonlocal code_lines
        # Preformatted trata o conteúdo como texto, sem interpretar XML/HTML.
        code = "\n".join(code_lines)
        story.append(Preformatted(code, styles["code"], maxLineLength=100))
        code_lines = []

    for line in markdown.splitlines():
        if fence_char is not None:
            stripped = line.lstrip()
            if stripped.startswith(fence_char * fence_len):
                flush_code()
                fence_char = None
                fence_len = 0
            else:
                code_lines.append(line)
            continue

        fence_match = FENCE_RE.match(line)
        if fence_match:
            flush_paragraph()
            marker = fence_match.group(1)
            fence_char = marker[0]
            fence_len = len(marker)
            continue

        if not line.strip():
            flush_paragraph()
            continue

        heading_match = HEADING_RE.match(line)
        if heading_match:
            flush_paragraph()
            level = len(heading_match.group(1))
            story.append(
                Paragraph(safe_inline(heading_match.group(2)), styles[f"h{level}"])
            )
            continue

        if HR_RE.match(line):
            flush_paragraph()
            story.append(Spacer(1, 3 * mm))
            story.append(HRFlowable(width="100%", thickness=0.6))
            story.append(Spacer(1, 3 * mm))
            continue

        bullet_match = BULLET_RE.match(line)
        if bullet_match:
            flush_paragraph()
            story.append(
                Paragraph(safe_inline(bullet_match.group(1)), styles["bullet"], bulletText="-")
            )
            continue

        numbered_match = NUMBERED_RE.match(line)
        if numbered_match:
            flush_paragraph()
            number = numbered_match.group(1)
            item = numbered_match.group(2)
            story.append(
                Paragraph(safe_inline(item), styles["bullet"], bulletText=f"{number}.")
            )
            continue

        if line.lstrip().startswith(">"):
            flush_paragraph()
            quote = line.lstrip()[1:].lstrip()
            story.append(Paragraph(safe_inline(quote), styles["quote"]))
            continue

        paragraph_lines.append(line)

    flush_paragraph()
    if fence_char is not None:
        # Bloco não fechado continua sendo tratado como texto de código.
        flush_code()

    if not story:
        story.append(Paragraph("Documento vazio.", styles["body"]))

    return story


def validate_input(path: Path) -> str:
    if path.is_symlink():
        raise ValueError("Por segurança, o arquivo de entrada não pode ser um link simbólico.")
    if not path.is_file():
        raise ValueError("O arquivo de entrada não existe ou não é um arquivo regular.")

    size = path.stat().st_size
    if size > MAX_INPUT_BYTES:
        raise ValueError(
            f"Arquivo grande demais: {size} bytes; limite: {MAX_INPUT_BYTES} bytes."
        )

    data = path.read_text(encoding="utf-8", errors="strict")
    lines = data.splitlines()
    if len(lines) > MAX_LINES:
        raise ValueError(f"Linhas demais; limite: {MAX_LINES}.")
    if any(len(line) > MAX_LINE_CHARS for line in lines):
        raise ValueError(f"Uma linha excedeu o limite de {MAX_LINE_CHARS} caracteres.")
    return data


def build_pdf(markdown: str, output_path: Path, *, force: bool = False) -> None:
    parent = output_path.parent.resolve(strict=True)
    output = parent / output_path.name

    if output.exists():
        if output.is_symlink():
            raise ValueError("Por segurança, a saída não pode ser um link simbólico.")
        if not force:
            raise FileExistsError(
                f"A saída já existe: {output}. Use --force para substituir."
            )

    fd, temporary_name = tempfile.mkstemp(
        prefix=f".{output.name}.", suffix=".tmp", dir=parent
    )
    os.close(fd)
    temporary = Path(temporary_name)

    try:
        document = SimpleDocTemplate(
            str(temporary),
            pagesize=A4,
            rightMargin=20 * mm,
            leftMargin=20 * mm,
            topMargin=18 * mm,
            bottomMargin=18 * mm,
            title=output.stem,
            author="markdown_seguro_pdf.py",
            pageCompression=1,
        )
        document.build(markdown_to_story(markdown))

        if temporary.stat().st_size == 0:
            raise RuntimeError("O PDF temporário foi criado vazio.")

        os.replace(temporary, output)
    finally:
        temporary.unlink(missing_ok=True)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Converte um subconjunto seguro de Markdown para PDF."
    )
    parser.add_argument("entrada", type=Path, help="Arquivo Markdown UTF-8")
    parser.add_argument("saida", type=Path, help="Arquivo PDF de saída")
    parser.add_argument(
        "--force",
        action="store_true",
        help="Permite substituir um PDF existente.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    try:
        input_path = args.entrada.expanduser()
        output_path = args.saida.expanduser()

        if output_path.suffix.lower() != ".pdf":
            raise ValueError("O arquivo de saída deve terminar em .pdf.")

        markdown = validate_input(input_path)
        build_pdf(markdown, output_path, force=args.force)
        print(f"PDF criado com sucesso: {output_path}")
        return 0
    except (OSError, UnicodeError, ValueError, RuntimeError) as exc:
        print(f"Erro: {exc}", file=os.sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
