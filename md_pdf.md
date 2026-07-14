#!/usr/bin/env python3
"""MD2PDF v7: conversor seguro de Markdown para PDF.

Fluxos públicos:
    python md2pdf_v7.py -help
    python md2pdf_v7.py -install
    python md2pdf_v7.py -use [tema] entrada.md [saida.pdf]

A única dependência externa é o ReportLab. A conversão é permitida apenas
pelo comando ``-use``. O PDF usa fundo uniforme, sem cabeçalho, rodapé ou
painel global de conteúdo.
"""

from __future__ import annotations

import argparse
from collections import defaultdict, deque
import html
import math
import importlib.util
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unicodedata
from urllib.parse import unquote
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Iterable, Sequence

SCRIPT_VERSION = "7.0.0-final"
SCRIPT_NAME = Path(__file__).name
MIN_PYTHON = (3, 9)
APP_NAME = "md2pdf"
MANAGED_VENV_NAME = ".venv"
RUNTIME_POINTER_NAME = "runtime_python.txt"
REPORTLAB_REQUIREMENT = "reportlab>=4.0,<5"
INSTALL_MIN_FREE_BYTES = 150 * 1024 * 1024

HELP_TEXT = fr"""
MD2PDF {SCRIPT_VERSION} - Markdown seguro para PDF

FLUXO OFICIAL

  1. Mostrar ajuda e exemplos:
     python md2pdf_v7.py -help

  2. Preparar o ambiente na primeira utilização:
     python md2pdf_v7.py -install

  3. Converter sempre usando -use:
     python md2pdf_v7.py -use [tema] entrada.md [saida.pdf]

TEMAS DISPONÍVEIS

  Padrão: bb-light-dark

  -l, --light
      Tema claro genérico, preservado para compatibilidade.

  -d, --dark
      Tema escuro genérico, preservado para compatibilidade.

  --bb-light
      Claro, formal e confortável. Indicado para leitura longa, impressão,
      manuais, documentação técnica, relatórios extensos e muitas tabelas.

  --bb-light-dark
      Claro com áreas técnicas escuras. É o padrão recomendado para operação,
      governança, tecnologia, projetos e documentos de uso geral.

  --bb-dark
      Escuro, executivo e de alto impacto. Indicado para PDFs digitais,
      resumos curtos, inovação e materiais próximos de apresentações.

  Também é possível selecionar pelo nome:
      -t bb-light
      -t bb-light-dark
      -t bb-dark
      -t light
      -t dark

EXEMPLOS DE TEMAS

  Tema padrão bb-light-dark:
     python md2pdf_v7.py -use documento.md

  Tema BB claro:
     python md2pdf_v7.py -use --bb-light documento.md

  Tema BB claro/escuro:
     python md2pdf_v7.py -use --bb-light-dark documento.md

  Tema BB escuro:
     python md2pdf_v7.py -use --bb-dark documento.md

  Seleção pelo nome:
     python md2pdf_v7.py -use -t bb-dark documento.md

  Temas antigos, mantidos por compatibilidade:
     python md2pdf_v7.py -use -l documento.md
     python md2pdf_v7.py -use -d documento.md

DOIS MODOS DE GERAÇÃO

  Modo 1 - saída informada pelo usuário:

     python md2pdf_v7.py -use --bb-dark entrada.md saida.pdf --force

  Você escolhe o nome e a pasta. Se o PDF já existir, use --force.

  Modo 2 - saída automática:

     python md2pdf_v7.py -use --bb-dark entrada.md

  O PDF é criado automaticamente:
  - na mesma pasta do Markdown;
  - com o mesmo nome do Markdown;
  - trocando .md ou .markdown por .pdf;
  - substituindo automaticamente o PDF existente.

COMANDO -INSTALL

  python md2pdf_v7.py -install

  Verifica Python, venv, pip, permissões, espaço livre, ReportLab e a geração
  real de um PDF de teste. Quando necessário, cria um ambiente virtual privado.
  Não é necessário ativar o ambiente manualmente.

COMANDO -USE

  Saída automática:
     python md2pdf_v7.py -use entrada.md
     python md2pdf_v7.py -use --bb-light entrada.md
     python md2pdf_v7.py -use --bb-dark entrada.md

  Saída explícita:
     python md2pdf_v7.py -use entrada.md saida.pdf
     python md2pdf_v7.py -use --bb-dark entrada.md saida.pdf --force

  Ocultar a barra de progresso:
     python md2pdf_v7.py -use entrada.md --no-progress

  Uso guiado:
     python md2pdf_v7.py -use

COMPONENTES TEMATIZADOS

  - fundo uniforme da página, sem cabeçalho, rodapé ou cartão global;
  - título principal, seções e subtítulos;
  - corpo, listas e marcadores;
  - tabelas e cabeçalhos repetidos;
  - citações com fundo e barra lateral;
  - blocos de texto e código com quebra automática pela largura real;
  - fluxogramas Mermaid do subconjunto seguro;
  - linhas horizontais e mensagens de aviso.

ÍNDICES E LINKS INTERNOS

  Links como [Seção](#secao) são convertidos em links internos para títulos.
  A sintaxe Markdown não aparece literalmente no PDF.

TABELAS MARKDOWN

  | Produto | Quantidade | Valor |
  |:--------|-----------:|------:|
  | Alpha   | 10         | 99,90 |

FLUXOGRAMAS MERMAID (SUBCONJUNTO SEGURO)

  ```mermaid
  flowchart TD
      A["Início"] --> B["Processamento"]
      B --> C["Fim"]
  ```

  Suporta flowchart/graph TD, TB, LR ou RL; subgraph; caixas [texto];
  nós arredondados (texto), estádios ([texto]), elipses ((texto)); decisões
  {{texto}}; <br/>; <b>...</b>; e conexões -->, ==> ou -.->. O motor Auto
  Layout avalia múltiplos candidatos, reduz cruzamentos, desvia setas de caixas
  e pagina grupos com indicação de continuação. Não executa JavaScript.

MOTOR MERMAID AUTOMÁTICO

  Padrão - analisa o grafo e escolhe o layout com menor penalidade:
     python md2pdf_v7.py -use --mermaid-auto documento.md

  Modo fiel - prioriza TD, TB, LR ou RL e a ordem declarada:
     python md2pdf_v7.py -use --mermaid-strict documento.md

  O modo automático avalia candidatos compactos, equilibrados, legíveis e
  horizontais. A pontuação considera número de páginas, grupos cortados,
  cruzamentos, conexões invertidas, altura dos nós e espaço desperdiçado.
  Também reordena nós equivalentes por baricentro e desvia setas de caixas.

OUTRAS OPÇÕES

  --force          Substitui uma saída explícita existente.
  --mermaid-auto  Usa o motor automático (padrão).
  --mermaid-strict Prioriza o layout declarado.
  --no-progress    Oculta a barra e o percentual de progresso.
  --version        Mostra a versão do MD2PDF.

REGRAS

  - A conversão só funciona com -use.
  - A entrada deve ser UTF-8 e terminar em .md ou .markdown.
  - A saída explícita deve terminar em .pdf.
  - Um tema desconhecido é rejeitado; o padrão é bb-light-dark.
  - A troca de tema não altera o conteúdo ou a ordem do Markdown.
  - Cada página possui um único fundo uniforme; superfícies são locais.
  - Cabeçalho e rodapé não são gerados.
  - HTML arbitrário, JavaScript, imagens e recursos externos não são processados.
  - Nenhum logotipo ou fonte proprietária é incorporado.
""".strip()


def _app_home() -> Path:
    """Diretório privado do usuário usado para o ambiente gerenciado."""
    override = os.environ.get("MD2PDF_HOME")
    if override:
        return Path(override).expanduser().resolve()

    if os.name == "nt":
        base = Path(os.environ.get("LOCALAPPDATA", Path.home() / "AppData" / "Local"))
    else:
        base = Path(os.environ.get("XDG_DATA_HOME", Path.home() / ".local" / "share"))
    return base / APP_NAME


def _managed_venv() -> Path:
    return _app_home() / MANAGED_VENV_NAME


def _venv_python(venv_path: Path | None = None) -> Path:
    venv = venv_path or _managed_venv()
    if os.name == "nt":
        return venv / "Scripts" / "python.exe"
    return venv / "bin" / "python"


def _runtime_pointer() -> Path:
    return _app_home() / RUNTIME_POINTER_NAME


def _selected_python() -> Path:
    pointer = _runtime_pointer()
    try:
        if pointer.is_file():
            value = pointer.read_text(encoding="utf-8").strip()
            if value:
                candidate = Path(value).expanduser()
                if candidate.is_file():
                    return candidate
    except (OSError, UnicodeError):
        pass
    return _venv_python()


def _write_runtime_pointer(python_path: Path) -> None:
    pointer = _runtime_pointer()
    pointer.parent.mkdir(parents=True, exist_ok=True)
    temporary = pointer.with_suffix(".tmp")
    temporary.write_text(str(python_path.resolve()), encoding="utf-8")
    os.replace(temporary, pointer)


def _python_version_text() -> str:
    return f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"


def _python_supported() -> bool:
    return sys.version_info >= MIN_PYTHON


def _reportlab_available_here() -> bool:
    """Valida os módulos realmente usados, incluindo dependências transitivas."""
    try:
        from reportlab.lib import colors as _colors
        from reportlab.platypus import SimpleDocTemplate as _simple_doc_template
        return _colors is not None and _simple_doc_template is not None
    except (ImportError, OSError, RuntimeError):
        return False


def _run_quiet(command: list[str], *, timeout: int = 30) -> subprocess.CompletedProcess[str] | None:
    try:
        return subprocess.run(
            command,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout,
            check=False,
            env={**os.environ, "PYTHONNOUSERSITE": "1", "PIP_NO_INPUT": "1"},
        )
    except (OSError, subprocess.SubprocessError):
        return None


def _runtime_environment_info(python_path: Path) -> tuple[bool, str]:
    """Valida um interpretador com importação e geração real de PDF."""
    if not python_path.is_file():
        return False, f"interpretador não encontrado: {python_path}"

    code = (
        "import sys, reportlab; "
        "from io import BytesIO; "
        "from reportlab.lib import colors; "
        "from reportlab.lib.styles import getSampleStyleSheet; "
        "from reportlab.platypus import SimpleDocTemplate, Paragraph, LongTable, TableStyle; "
        f"assert sys.version_info >= {MIN_PYTHON!r}; "
        "buf=BytesIO(); "
        "doc=SimpleDocTemplate(buf); "
        "styles=getSampleStyleSheet(); "
        "table=LongTable([[Paragraph('A', styles['BodyText']), Paragraph('B', styles['BodyText'])], "
        "[Paragraph('1', styles['BodyText']), Paragraph('2', styles['BodyText'])]], repeatRows=1); "
        "table.setStyle(TableStyle([('GRID',(0,0),(-1,-1),0.5,colors.black)])); "
        "doc.build([Paragraph('MD2PDF OK', styles['BodyText']), table]); "
        "assert buf.getvalue().startswith(b'%PDF') and len(buf.getvalue()) > 100; "
        "print(getattr(reportlab, '__version__', 'desconhecida'))"
    )
    result = _run_quiet([str(python_path), "-I", "-c", code], timeout=60)
    if result is None:
        return False, f"não foi possível executar {python_path}"
    if result.returncode != 0:
        detail = result.stderr.strip().splitlines()
        suffix = f": {detail[-1]}" if detail else ""
        return False, f"ambiente incompleto ou corrompido{suffix}"

    lines = [line.strip() for line in result.stdout.splitlines() if line.strip()]
    version = lines[-1] if lines else "desconhecida"
    return True, f"ReportLab {version}; teste real de PDF aprovado em {python_path}"


def _managed_environment_info() -> tuple[bool, str]:
    """Valida o interpretador selecionado pelo ambiente gerenciado."""
    python_path = _selected_python()
    if not python_path.is_file():
        return False, "ambiente gerenciado ainda não foi preparado"
    return _runtime_environment_info(python_path)


def _is_running_managed_python() -> bool:
    try:
        return Path(sys.executable).resolve() == _selected_python().resolve()
    except OSError:
        return False


def _check_directory_writable(directory: Path) -> tuple[bool, str]:
    try:
        directory.mkdir(parents=True, exist_ok=True)
        fd, name = tempfile.mkstemp(prefix=".md2pdf-write-test-", dir=directory)
        os.close(fd)
        Path(name).unlink(missing_ok=True)
        return True, "diretório gravável"
    except OSError as exc:
        return False, str(exc)


def _print_check(ok: bool, message: str) -> None:
    marker = "OK" if ok else "ERRO"
    print(f"[{marker}] {message}")


def _install_environment() -> int:
    print("MD2PDF — instalação e verificação do ambiente\n")

    version_ok = _python_supported()
    _print_check(
        version_ok,
        f"Python {_python_version_text()} "
        f"(mínimo: {MIN_PYTHON[0]}.{MIN_PYTHON[1]})",
    )
    if not version_ok:
        print("\nInstale uma versão compatível do Python antes de continuar.", file=sys.stderr)
        return 2

    venv_probe = _run_quiet([sys.executable, "-m", "venv", "--help"])
    venv_ok = venv_probe is not None and venv_probe.returncode == 0
    _print_check(venv_ok, "módulo venv disponível")
    if not venv_ok:
        print(
            "\nO Python instalado não possui o módulo venv. "
            "Reinstale o Python incluindo pip e venv.",
            file=sys.stderr,
        )
        return 2

    home = _app_home()
    writable, detail = _check_directory_writable(home)
    _print_check(writable, f"pasta do programa: {home} ({detail})")
    if not writable:
        return 2

    try:
        free_bytes = shutil.disk_usage(home).free
    except OSError as exc:
        print(f"[ERRO] Não foi possível verificar o espaço em disco: {exc}", file=sys.stderr)
        return 2
    enough_space = free_bytes >= INSTALL_MIN_FREE_BYTES
    _print_check(enough_space, f"espaço livre: {free_bytes / (1024 * 1024):.0f} MB")
    if not enough_space:
        print("São recomendados pelo menos 150 MB livres.", file=sys.stderr)
        return 2

    ready, detail = _managed_environment_info()
    if ready:
        _print_check(True, detail)
        print("\nA instalação já está pronta. Nenhuma alteração foi necessária.")
        print("Use: python md2pdf_v7.py -use entrada.md [saida.pdf]")
        return 0

    # Quando o próprio comando já está sendo executado dentro de um ambiente
    # virtual válido, ele pode ser registrado como runtime gerenciado. Isso
    # evita downloads desnecessários e mantém o funcionamento offline.
    if sys.prefix != sys.base_prefix and _reportlab_available_here():
        current_python = Path(sys.executable).resolve()
        current_ready, current_detail = _runtime_environment_info(current_python)
        if current_ready:
            _write_runtime_pointer(current_python)
            _print_check(True, current_detail)
            print("\nO ambiente virtual Python atual já possui tudo que o MD2PDF precisa.")
            print("Ele foi registrado como ambiente gerenciado; nenhuma instalação foi necessária.")
            print("Use: python md2pdf_v7.py -use entrada.md [saida.pdf]")
            return 0

    _runtime_pointer().unlink(missing_ok=True)
    venv_path = _managed_venv()
    python_path = _venv_python(venv_path)

    if venv_path.exists():
        print(f"[1/4] Removendo ambiente incompleto: {venv_path}")
        try:
            shutil.rmtree(venv_path)
        except OSError as exc:
            print(f"Erro ao remover o ambiente incompleto: {exc}", file=sys.stderr)
            return 2

    use_system_packages = _reportlab_available_here()
    print(f"[2/4] Criando ambiente virtual privado em: {venv_path}")
    create_command = [sys.executable, "-m", "venv"]
    if use_system_packages:
        # Reaproveita uma instalação global válida quando ela já existe. Isso
        # permite preparar o ambiente mesmo sem internet, sem copiar arquivos
        # manualmente nem instalar dependências adicionais.
        create_command.append("--system-site-packages")
        print("      ReportLab já encontrado no Python atual; será reaproveitado.")
    create_command.append(str(venv_path))
    create = subprocess.run(
        create_command,
        check=False,
        env={**os.environ, "PYTHONNOUSERSITE": "1"},
    )
    if create.returncode != 0 or not python_path.is_file():
        print("Erro ao criar o ambiente virtual.", file=sys.stderr)
        return 2

    print("[3/4] Verificando o pip")
    pip_check = _run_quiet([str(python_path), "-m", "pip", "--version"])
    if pip_check is None or pip_check.returncode != 0:
        ensure = subprocess.run(
            [str(python_path), "-m", "ensurepip", "--upgrade"],
            check=False,
            env={**os.environ, "PYTHONNOUSERSITE": "1", "PIP_NO_INPUT": "1"},
        )
        if ensure.returncode != 0:
            print("Erro ao preparar o pip no ambiente virtual.", file=sys.stderr)
            return 2

    ready_before_install, detail_before_install = _runtime_environment_info(python_path)
    if ready_before_install:
        print("[4/4] ReportLab já disponível no ambiente privado")
        _print_check(True, detail_before_install)
    else:
        print(f"[4/4] Instalando {REPORTLAB_REQUIREMENT}")
        install = subprocess.run(
            [
                str(python_path),
                "-m",
                "pip",
                "install",
                "--disable-pip-version-check",
                "--no-input",
                "--prefer-binary",
                "--index-url",
                "https://pypi.org/simple",
                REPORTLAB_REQUIREMENT,
            ],
            check=False,
            env={**os.environ, "PYTHONNOUSERSITE": "1", "PIP_NO_INPUT": "1"},
        )
        if install.returncode != 0:
            print(
                "\nNão foi possível instalar o ReportLab. Verifique internet, proxy, "
                "certificados ou bloqueios do antivírus e execute -install novamente.",
                file=sys.stderr,
            )
            return 2

    ready, detail = _runtime_environment_info(python_path)
    _print_check(ready, detail)
    if not ready:
        print("A instalação terminou, mas a validação final falhou.", file=sys.stderr)
        return 2
    _write_runtime_pointer(python_path)

    print("\nInstalação concluída com sucesso.")
    print("Não ative o ambiente manualmente; use o comando -use:")
    print("  python md2pdf_v7.py -use entrada.md [saida.pdf]")
    return 0


def _clean_user_path(value: str) -> str:
    return value.strip().strip('"').strip("'")


def _interactive_use_arguments() -> list[str]:
    print("MD2PDF - uso guiado\n")
    entrada = _clean_user_path(input("Arquivo Markdown de entrada: "))
    if not entrada:
        raise ValueError("Nenhum arquivo de entrada foi informado.")

    entrada_path = Path(entrada).expanduser()
    default_output = str(entrada_path.with_suffix(".pdf"))
    saida = _clean_user_path(
        input(
            f"Arquivo PDF de saída [Enter = automático: {default_output}]: "
        )
    )

    print("Temas disponíveis:")
    print("  1. bb-light       - leitura longa e impressão")
    print("  2. bb-light-dark  - padrão, moderno e operacional")
    print("  3. bb-dark        - executivo e alto impacto")
    print("  4. light          - claro genérico")
    print("  5. dark           - escuro genérico")
    theme_answer = input("Tema [2]: ").strip().lower()
    theme_map = {
        "1": "bb-light", "bb-light": "bb-light",
        "2": "bb-light-dark", "": "bb-light-dark", "bb-light-dark": "bb-light-dark",
        "3": "bb-dark", "bb-dark": "bb-dark",
        "4": "light", "l": "light", "light": "light", "claro": "light",
        "5": "dark", "d": "dark", "dark": "dark", "escuro": "dark",
    }
    theme_name = theme_map.get(theme_answer)
    if theme_name is None:
        raise ValueError(f"Tema desconhecido: {theme_answer!r}.")

    # Sem saída explícita, o parser aplica o nome automático e o force implícito.
    arguments = ["--theme", theme_name, entrada]
    if saida:
        arguments.append(saida)
        if Path(saida).expanduser().exists():
            replace = input("O PDF já existe. Substituir? [s/N]: ").strip().lower()
            if replace in {"s", "sim", "y", "yes"}:
                arguments.append("--force")
    return arguments


def _prepare_use(arguments: list[str]) -> tuple[list[str], int | None]:
    """Executa todas as checagens obrigatórias antes da transformação."""
    print("MD2PDF - checagem obrigatória antes do uso\n")

    version_ok = _python_supported()
    _print_check(version_ok, f"Python {_python_version_text()} (mínimo 3.9)")
    if not version_ok:
        print("\nUse Python 3.9 ou superior e depois execute -install.", file=sys.stderr)
        return arguments, 2

    home = _app_home()
    writable, writable_detail = _check_directory_writable(home)
    _print_check(writable, f"pasta privada: {home} ({writable_detail})")
    if not writable:
        print("\nO ambiente não pode ser usado. Corrija a permissão e execute -install.", file=sys.stderr)
        return arguments, 2

    managed_ready, managed_detail = _managed_environment_info()
    _print_check(managed_ready, f"ambiente privado: {managed_detail}")

    if not managed_ready:
        print("\n[ACAO NECESSARIA] O MD2PDF ainda não está pronto para converter.")
        print("Execute primeiro:")
        print("  python md2pdf_v7.py -install")
        print("\nDepois execute a transformação com:")
        print("  python md2pdf_v7.py -use entrada.md [saida.pdf]")
        return arguments, 2

    if not arguments:
        try:
            arguments = _interactive_use_arguments()
        except (EOFError, KeyboardInterrupt, ValueError) as exc:
            print(f"Uso guiado cancelado: {exc}", file=sys.stderr)
            return [], 130 if isinstance(exc, KeyboardInterrupt) else 2

    if not _is_running_managed_python():
        python_path = _selected_python()
        print("\n[OK] Não é necessário executar -install.")
        print(f"[OK] Usando automaticamente o ambiente privado: {python_path}")
        sys.stdout.flush()
        sys.stderr.flush()
        command = [str(python_path), str(Path(__file__).resolve()), *arguments]
        environment = {
            **os.environ,
            "MD2PDF_INTERNAL_USE": "1",
            "PYTHONNOUSERSITE": "1",
        }
        try:
            result = subprocess.run(command, check=False, env=environment)
        except OSError as exc:
            print(f"Não foi possível iniciar o ambiente privado: {exc}", file=sys.stderr)
            return arguments, 2
        return arguments, result.returncode

    if not _reportlab_available_here():
        print("\n[ERRO] O ambiente privado falhou na checagem final.", file=sys.stderr)
        print("Execute novamente: python md2pdf_v7.py -install", file=sys.stderr)
        return arguments, 2

    print("\n[OK] Não é necessário executar -install.")
    print("[OK] Todas as verificações do ambiente passaram.")
    os.environ["MD2PDF_INTERNAL_USE"] = "1"
    return arguments, None


def _early_bootstrap(raw_arguments: list[str]) -> tuple[list[str], bool]:
    """Permite conversão somente pelo fluxo público -use."""
    arguments = list(raw_arguments)
    help_aliases = {"-help", "--help", "-h", "help", "ajuda"}
    install_aliases = {"-install", "--install", "install"}
    use_aliases = {"-use", "--use", "use"}
    version_aliases = {"--version", "-version", "version"}
    internal_use = os.environ.get("MD2PDF_INTERNAL_USE") == "1"

    if not arguments:
        print(HELP_TEXT)
        raise SystemExit(0)

    if arguments[0] in help_aliases:
        print(HELP_TEXT)
        raise SystemExit(0)

    if arguments[0] in version_aliases:
        print(f"{SCRIPT_NAME} {SCRIPT_VERSION}")
        raise SystemExit(0)

    if arguments[0] in install_aliases:
        if len(arguments) > 1:
            print("O comando -install não recebe outros argumentos.", file=sys.stderr)
            raise SystemExit(2)
        raise SystemExit(_install_environment())

    if arguments[0] in use_aliases:
        arguments = arguments[1:]
        arguments, return_code = _prepare_use(arguments)
        if return_code is not None:
            raise SystemExit(return_code)
        use_mode = True
    elif internal_use:
        # Processo reiniciado pelo próprio -use dentro do ambiente privado.
        use_mode = True
    else:
        print("Erro: a transformação só pode ser executada com o comando -use.", file=sys.stderr)
        print("\nForma correta:", file=sys.stderr)
        print("  python md2pdf_v7.py -use entrada.md [saida.pdf]", file=sys.stderr)
        print("  python md2pdf_v7.py -use --bb-light entrada.md saida.pdf", file=sys.stderr)
        print("  python md2pdf_v7.py -use --bb-dark entrada.md saida.pdf", file=sys.stderr)
        print("\nPara preparar o ambiente:", file=sys.stderr)
        print("  python md2pdf_v7.py -install", file=sys.stderr)
        print("\nPara ver exemplos:", file=sys.stderr)
        print("  python md2pdf_v7.py -help", file=sys.stderr)
        raise SystemExit(2)

    if not _reportlab_available_here():
        print("Erro: o ambiente de conversão está incompleto.", file=sys.stderr)
        print("Execute: python md2pdf_v7.py -install", file=sys.stderr)
        raise SystemExit(2)

    return arguments, use_mode


_EFFECTIVE_ARGUMENTS, USE_MODE = _early_bootstrap(sys.argv[1:])

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.platypus import (
    Flowable,
    HRFlowable,
    LongTable,
    Paragraph,
    PageBreak,
    Preformatted,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

MAX_INPUT_BYTES = 2_000_000
MAX_LINES = 50_000
MAX_LINE_CHARS = 20_000
MAX_TABLE_COLUMNS = 40
MAX_TABLE_ROWS = 10_000
MAX_TABLE_CELLS = 100_000
MAX_TABLE_CELL_CHARS = 20_000
MAX_MERMAID_NODES = 250
MAX_MERMAID_EDGES = 500
MAX_MERMAID_GROUPS = 80
MAX_MERMAID_LABEL_CHARS = 5_000

PAGE_LEFT_MARGIN = 20 * mm
PAGE_RIGHT_MARGIN = 20 * mm
PAGE_TOP_MARGIN = 18 * mm
PAGE_BOTTOM_MARGIN = 18 * mm
AVAILABLE_TABLE_WIDTH = A4[0] - PAGE_LEFT_MARGIN - PAGE_RIGHT_MARGIN

HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
BULLET_RE = re.compile(r"^\s{0,3}[-+*]\s+(.+)$")
NUMBERED_RE = re.compile(r"^\s{0,3}(\d{1,6})[.)]\s+(.+)$")
FENCE_RE = re.compile(r"^\s*(`{3,}|~{3,})\s*([A-Za-z0-9_-]*)\s*$")
HR_RE = re.compile(r"^\s{0,3}((\*\s*){3,}|(-\s*){3,}|(_\s*){3,})$")
TABLE_SEPARATOR_CELL_RE = re.compile(r"^:?-{3,}:?$")


@dataclass(frozen=True)
class PdfTheme:
    """Tokens visuais aplicados de forma independente do parser Markdown."""

    name: str
    display_name: str
    description: str

    page_background: colors.Color
    component_surface_primary: colors.Color
    component_surface_secondary: colors.Color
    text: colors.Color
    muted_text: colors.Color

    title: colors.Color
    heading: colors.Color
    subheading: colors.Color
    accent: colors.Color
    highlight: colors.Color
    bullet: colors.Color


    quote_text: colors.Color
    quote_background: colors.Color
    quote_bar: colors.Color

    code_text: colors.Color
    code_background: colors.Color
    code_border: colors.Color

    table_header_background: colors.Color
    table_header_text: colors.Color
    table_cell_background: colors.Color
    table_alternate_background: colors.Color
    table_grid: colors.Color
    table_accent: colors.Color

    mermaid_node_background: colors.Color
    mermaid_node_text: colors.Color
    mermaid_node_border: colors.Color
    mermaid_group_background: colors.Color
    mermaid_group_text: colors.Color
    mermaid_group_border: colors.Color
    mermaid_edge: colors.Color

    warning_background: colors.Color
    warning_text: colors.Color
    warning_border: colors.Color
    horizontal_rule: colors.Color

    status_approved: colors.Color
    status_waiting: colors.Color
    status_rejected: colors.Color
    status_active: colors.Color
    status_expired: colors.Color
    status_selected: colors.Color


def _hex(value: str) -> colors.Color:
    return colors.HexColor(value)


LIGHT_THEME = PdfTheme(
    name="light",
    display_name="Light",
    description="Tema claro genérico mantido por compatibilidade.",
    page_background=colors.white,
    component_surface_primary=colors.white,
    component_surface_secondary=_hex("#F5F7F9"),
    text=_hex("#202124"),
    muted_text=_hex("#4F5965"),
    title=_hex("#111827"),
    heading=_hex("#1F2937"),
    subheading=_hex("#374151"),
    accent=_hex("#2563EB"),
    highlight=_hex("#F4C430"),
    bullet=_hex("#2563EB"),
    quote_text=_hex("#374151"),
    quote_background=_hex("#EFF6FF"),
    quote_bar=_hex("#2563EB"),
    code_text=_hex("#202124"),
    code_background=_hex("#F5F7F9"),
    code_border=_hex("#D0D7DE"),
    table_header_background=_hex("#E9ECEF"),
    table_header_text=_hex("#202124"),
    table_cell_background=colors.white,
    table_alternate_background=_hex("#F8F9FA"),
    table_grid=_hex("#ADB5BD"),
    table_accent=_hex("#2563EB"),
    mermaid_node_background=_hex("#F5F7F9"),
    mermaid_node_text=_hex("#202124"),
    mermaid_node_border=_hex("#9CA3AF"),
    mermaid_group_background=_hex("#F8FAFC"),
    mermaid_group_text=_hex("#4B5563"),
    mermaid_group_border=_hex("#9CA3AF"),
    mermaid_edge=_hex("#6B7280"),
    warning_background=_hex("#FFF7ED"),
    warning_text=_hex("#9A3412"),
    warning_border=_hex("#FDBA74"),
    horizontal_rule=_hex("#8C959F"),
    status_approved=_hex("#217A50"),
    status_waiting=_hex("#A86600"),
    status_rejected=_hex("#C43D46"),
    status_active=_hex("#465EFF"),
    status_expired=_hex("#707786"),
    status_selected=_hex("#FCFC30"),
)


DARK_THEME = PdfTheme(
    name="dark",
    display_name="Dark",
    description="Tema escuro genérico mantido por compatibilidade.",
    page_background=_hex("#111827"),
    component_surface_primary=_hex("#172033"),
    component_surface_secondary=_hex("#1F2937"),
    text=_hex("#E5E7EB"),
    muted_text=_hex("#C7CDD6"),
    title=_hex("#F9FAFB"),
    heading=_hex("#F9FAFB"),
    subheading=_hex("#D1D5DB"),
    accent=_hex("#60A5FA"),
    highlight=_hex("#FACC15"),
    bullet=_hex("#60A5FA"),
    quote_text=_hex("#F3F4F6"),
    quote_background=_hex("#1F2937"),
    quote_bar=_hex("#60A5FA"),
    code_text=_hex("#F3F4F6"),
    code_background=_hex("#0B1220"),
    code_border=_hex("#4B5563"),
    table_header_background=_hex("#374151"),
    table_header_text=colors.white,
    table_cell_background=_hex("#1F2937"),
    table_alternate_background=_hex("#273244"),
    table_grid=_hex("#6B7280"),
    table_accent=_hex("#60A5FA"),
    mermaid_node_background=_hex("#1F2937"),
    mermaid_node_text=_hex("#F3F4F6"),
    mermaid_node_border=_hex("#6B7280"),
    mermaid_group_background=_hex("#172033"),
    mermaid_group_text=_hex("#D1D5DB"),
    mermaid_group_border=_hex("#4B5563"),
    mermaid_edge=_hex("#9CA3AF"),
    warning_background=_hex("#422006"),
    warning_text=_hex("#FED7AA"),
    warning_border=_hex("#C2410C"),
    horizontal_rule=_hex("#6B7280"),
    status_approved=_hex("#39A872"),
    status_waiting=_hex("#D39125"),
    status_rejected=_hex("#ED6670"),
    status_active=_hex("#7183FF"),
    status_expired=_hex("#9AA1AF"),
    status_selected=_hex("#FCFC30"),
)


BB_LIGHT_THEME = PdfTheme(
    name="bb-light",
    display_name="BB Light",
    description="Claro, formal e confortável para leitura longa e impressão.",
    page_background=_hex("#FFFFFF"),
    component_surface_primary=_hex("#FFFFFF"),
    component_surface_secondary=_hex("#F4F6FA"),
    text=_hex("#17234D"),
    muted_text=_hex("#596174"),
    title=_hex("#17234D"),
    heading=_hex("#465EFF"),
    subheading=_hex("#17234D"),
    accent=_hex("#465EFF"),
    highlight=_hex("#FCFC30"),
    bullet=_hex("#465EFF"),
    quote_text=_hex("#17234D"),
    quote_background=_hex("#F0F2FF"),
    quote_bar=_hex("#465EFF"),
    code_text=_hex("#161D33"),
    code_background=_hex("#F1F3F7"),
    code_border=_hex("#D9DEE8"),
    table_header_background=_hex("#465EFF"),
    table_header_text=_hex("#FFFFFF"),
    table_cell_background=_hex("#FFFFFF"),
    table_alternate_background=_hex("#F4F6FA"),
    table_grid=_hex("#D9DEE8"),
    table_accent=_hex("#FCFC30"),
    mermaid_node_background=_hex("#F4F6FA"),
    mermaid_node_text=_hex("#17234D"),
    mermaid_node_border=_hex("#465EFF"),
    mermaid_group_background=_hex("#F0F2FF"),
    mermaid_group_text=_hex("#17234D"),
    mermaid_group_border=_hex("#AAB4FF"),
    mermaid_edge=_hex("#465EFF"),
    warning_background=_hex("#FFFBE6"),
    warning_text=_hex("#5F5200"),
    warning_border=_hex("#D8C700"),
    horizontal_rule=_hex("#465EFF"),
    status_approved=_hex("#217A50"),
    status_waiting=_hex("#A86600"),
    status_rejected=_hex("#C43D46"),
    status_active=_hex("#465EFF"),
    status_expired=_hex("#707786"),
    status_selected=_hex("#FCFC30"),
)


BB_LIGHT_DARK_THEME = PdfTheme(
    name="bb-light-dark",
    display_name="BB Light Dark",
    description="Equilibrado, moderno e tecnológico; tema padrão recomendado.",
    page_background=_hex("#E9ECF3"),
    component_surface_primary=_hex("#F8F9FC"),
    component_surface_secondary=_hex("#DDE2EC"),
    text=_hex("#161D33"),
    muted_text=_hex("#596174"),
    title=_hex("#17234D"),
    heading=_hex("#465EFF"),
    subheading=_hex("#17234D"),
    accent=_hex("#465EFF"),
    highlight=_hex("#FCFC30"),
    bullet=_hex("#465EFF"),
    quote_text=_hex("#161D33"),
    quote_background=_hex("#DCE1FF"),
    quote_bar=_hex("#465EFF"),
    code_text=_hex("#F8F9FC"),
    code_background=_hex("#222B45"),
    code_border=_hex("#17234D"),
    table_header_background=_hex("#17234D"),
    table_header_text=_hex("#FFFFFF"),
    table_cell_background=_hex("#F8F9FC"),
    table_alternate_background=_hex("#E9ECF3"),
    table_grid=_hex("#C5CBD8"),
    table_accent=_hex("#FCFC30"),
    mermaid_node_background=_hex("#F8F9FC"),
    mermaid_node_text=_hex("#161D33"),
    mermaid_node_border=_hex("#465EFF"),
    mermaid_group_background=_hex("#DDE2EC"),
    mermaid_group_text=_hex("#17234D"),
    mermaid_group_border=_hex("#AAB2C4"),
    mermaid_edge=_hex("#17234D"),
    warning_background=_hex("#FFFBE6"),
    warning_text=_hex("#5F5200"),
    warning_border=_hex("#D8C700"),
    horizontal_rule=_hex("#17234D"),
    status_approved=_hex("#217A50"),
    status_waiting=_hex("#A86600"),
    status_rejected=_hex("#C43D46"),
    status_active=_hex("#465EFF"),
    status_expired=_hex("#707786"),
    status_selected=_hex("#FCFC30"),
)


BB_DARK_THEME = PdfTheme(
    name="bb-dark",
    display_name="BB Dark",
    description="Escuro, executivo e de alto impacto para uso digital.",
    page_background=_hex("#11182E"),
    component_surface_primary=_hex("#17234D"),
    component_surface_secondary=_hex("#222B45"),
    text=_hex("#FFFFFF"),
    muted_text=_hex("#D7DCEC"),
    title=_hex("#FCFC30"),
    heading=_hex("#FFFFFF"),
    subheading=_hex("#D7DCEC"),
    accent=_hex("#465EFF"),
    highlight=_hex("#FCFC30"),
    bullet=_hex("#FCFC30"),
    quote_text=_hex("#FFFFFF"),
    quote_background=_hex("#17234D"),
    quote_bar=_hex("#FCFC30"),
    code_text=_hex("#F8F9FC"),
    code_background=_hex("#0D1326"),
    code_border=_hex("#36405D"),
    table_header_background=_hex("#465EFF"),
    table_header_text=_hex("#FFFFFF"),
    table_cell_background=_hex("#17234D"),
    table_alternate_background=_hex("#202944"),
    table_grid=_hex("#36405D"),
    table_accent=_hex("#FCFC30"),
    mermaid_node_background=_hex("#222B45"),
    mermaid_node_text=_hex("#FFFFFF"),
    mermaid_node_border=_hex("#465EFF"),
    mermaid_group_background=_hex("#17234D"),
    mermaid_group_text=_hex("#D7DCEC"),
    mermaid_group_border=_hex("#36405D"),
    mermaid_edge=_hex("#D7DCEC"),
    warning_background=_hex("#3A3200"),
    warning_text=_hex("#FFFDB0"),
    warning_border=_hex("#FCFC30"),
    horizontal_rule=_hex("#465EFF"),
    status_approved=_hex("#3DAA75"),
    status_waiting=_hex("#D08B1D"),
    status_rejected=_hex("#E45A64"),
    status_active=_hex("#7183FF"),
    status_expired=_hex("#9AA1AF"),
    status_selected=_hex("#FCFC30"),
)


THEMES: dict[str, PdfTheme] = {
    theme.name: theme
    for theme in (
        LIGHT_THEME,
        DARK_THEME,
        BB_LIGHT_THEME,
        BB_LIGHT_DARK_THEME,
        BB_DARK_THEME,
    )
}


def _validate_theme_contract() -> None:
    """Valida tokens essenciais antes de construir qualquer documento."""
    required = {"light", "dark", "bb-light", "bb-light-dark", "bb-dark"}
    if set(THEMES) != required:
        missing = sorted(required - set(THEMES))
        extra = sorted(set(THEMES) - required)
        raise RuntimeError(f"Configuração de temas inválida; ausentes={missing}, extras={extra}.")
    for name, theme in THEMES.items():
        if theme.name != name:
            raise RuntimeError(f"Tema {name!r} possui nome interno inconsistente.")
        if theme.page_background is None:
            raise RuntimeError(f"Tema {name!r} não possui fundo de página.")


_validate_theme_contract()

DEFAULT_THEME_NAME = "bb-light-dark"


class ProgressBar:
    """Barra de progresso ASCII sem dependências adicionais."""

    def __init__(self, *, enabled: bool = True, width: int = 32) -> None:
        self.enabled = enabled
        self.width = width
        self.stream = os.sys.stdout
        self.interactive = bool(getattr(self.stream, "isatty", lambda: False)())
        self.last_percent = -1
        self.last_label = ""
        self.next_noninteractive_mark = 0

    def update(self, percent: float, label: str) -> None:
        if not self.enabled:
            return

        value = max(0, min(100, int(percent)))
        if self.interactive:
            if value == self.last_percent and label == self.last_label:
                return
            filled = int(self.width * value / 100)
            bar = "#" * filled + "-" * (self.width - filled)
            message = f"\r[{bar}] {value:3d}%  {label}"
            # Espaços extras apagam restos de uma mensagem anterior maior.
            self.stream.write(message.ljust(self.width + 70))
            self.stream.flush()
        else:
            # Em logs/redirecionamentos, evita centenas de linhas.
            if value < self.next_noninteractive_mark and value < 100:
                return
            self.stream.write(f"[{value:3d}%] {label}\n")
            self.stream.flush()
            self.next_noninteractive_mark = min(100, ((value // 10) + 1) * 10)

        self.last_percent = value
        self.last_label = label

    def stop(self) -> None:
        """Encerra a linha atual sem marcar a operação como concluída."""
        if self.enabled and self.interactive and self.last_percent < 100:
            self.stream.write("\n")
            self.stream.flush()

    def finish(self, label: str = "Concluído") -> None:
        self.update(100, label)
        if self.enabled and self.interactive:
            self.stream.write("\n")
            self.stream.flush()


class ProgressDocTemplate(SimpleDocTemplate):
    """Atualiza o progresso conforme o ReportLab processa conteúdo e páginas."""

    def __init__(
        self,
        *args,
        progress: ProgressBar,
        total_units: int,
        estimated_pages: int,
        **kwargs,
    ) -> None:
        super().__init__(*args, **kwargs)
        self._progress = progress
        self._total_units = max(1, total_units)
        self._completed_units = 0
        self._estimated_pages = max(1, estimated_pages)
        self._pages_done = 0
        self._render_percent = 42.0

    @staticmethod
    def _flowable_units(flowable) -> int:
        if isinstance(flowable, LongTable):
            rows = getattr(flowable, "_cellvalues", None)
            return max(1, len(rows) if rows is not None else 1)
        if isinstance(flowable, MermaidFlowchart):
            return max(1, flowable.node_count)
        if isinstance(flowable, Preformatted):
            text = getattr(flowable, "text", "")
            return max(1, str(text).count("\n") + 1)
        return 1

    def _show_render_progress(self, candidate: float, label: str) -> None:
        self._render_percent = max(self._render_percent, min(95.0, candidate))
        self._progress.update(self._render_percent, label)

    def afterFlowable(self, flowable) -> None:
        self._completed_units += self._flowable_units(flowable)
        fraction = min(1.0, self._completed_units / self._total_units)
        self._show_render_progress(42.0 + 52.0 * fraction, "Gerando páginas do PDF")

    def afterPage(self) -> None:
        self._pages_done += 1
        fraction = min(1.0, self._pages_done / self._estimated_pages)
        self._show_render_progress(42.0 + 50.0 * fraction, f"Gerando página {self._pages_done}")


class MarkdownTableError(ValueError):
    """Erro de estrutura em uma tabela Markdown."""


class MermaidSyntaxError(ValueError):
    """Erro em um bloco Mermaid fora do subconjunto seguro suportado."""


@dataclass
class MermaidNode:
    node_id: str
    label: str
    shape: str = "box"
    group_id: str | None = None
    order: int = 0


@dataclass
class MermaidGroup:
    group_id: str
    label: str
    order: int = 0


@dataclass
class MermaidGraph:
    direction: str
    nodes: dict[str, MermaidNode]
    edges: list[tuple[str, str]]
    groups: dict[str, MermaidGroup]
    node_order: list[str]


@dataclass(frozen=True)
class MermaidLayoutPlan:
    """Configuração imutável de um candidato de layout Mermaid."""

    name: str
    orientation: str = "vertical"
    density: str = "balanced"
    reorder_nodes: bool = True
    reorder_stages: bool = True
    max_columns: int | None = None
    node_min_width: float = 96.0
    node_max_width: float = 224.0
    column_gap: float = 16.0
    row_gap: float = 12.0
    group_gap: float = 14.0
    reverse: bool = False


_MERMAID_ID = r"[A-Za-z_][A-Za-z0-9_-]*"
_MERMAID_HEADER_RE = re.compile(
    r"^(?:flowchart|graph)\s+(TD|TB|LR|RL)\s*$", re.IGNORECASE
)
_MERMAID_SUBGRAPH_RE = re.compile(
    rf'^subgraph\s+({_MERMAID_ID})(?:\s*\[\s*"((?:[^"\\]|\\.)*)"\s*\])?\s*$',
    re.IGNORECASE,
)
_MERMAID_DIRECTION_RE = re.compile(r"^direction\s+(TD|TB|LR|RL)\s*$", re.IGNORECASE)
_MERMAID_UNSUPPORTED_RE = re.compile(
    r"^(?:classDef|class|style|linkStyle|click|%%\{|init|sequenceDiagram|"
    r"stateDiagram|erDiagram|gantt|pie|journey|mindmap|timeline|gitGraph)\b",
    re.IGNORECASE,
)
_MERMAID_ARROW_RE = re.compile(r"\s*(?:-->|==>|-\.->)\s*")
_MERMAID_EDGE_LABEL_PREFIX_RE = re.compile(r"^\|[^|]{0,200}\|\s*")


def _mermaid_unescape_label(value: str) -> str:
    return value.replace(r'\"', '"').replace(r"\\", "\\").strip()


def _unwrap_mermaid_label(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] == '"':
        value = value[1:-1]
    return _mermaid_unescape_label(value)


def _parse_mermaid_node_token(token: str) -> tuple[str, str | None, str]:
    """Analisa formas comuns de nós sem executar sintaxe Mermaid externa.

    Formas aceitas:
    ``A[texto]`` caixa, ``A(texto)`` arredondada, ``A([texto])`` estádio,
    ``A((texto))`` elipse e ``A{texto}`` decisão.
    """
    cleaned = token.strip().rstrip(";").strip()
    id_match = re.match(rf"^({_MERMAID_ID})(.*)$", cleaned, re.DOTALL)
    if not id_match:
        raise MermaidSyntaxError(f"Nó Mermaid não suportado: {cleaned!r}.")

    node_id = id_match.group(1)
    suffix = id_match.group(2).strip()
    if not suffix:
        return node_id, None, "box"

    wrappers = (
        ("((", "))", "ellipse"),
        ("([", "])", "stadium"),
        ("[", "]", "box"),
        ("{", "}", "decision"),
        ("(", ")", "rounded"),
    )
    label: str | None = None
    shape = "box"
    for opening, closing, candidate_shape in wrappers:
        if suffix.startswith(opening) and suffix.endswith(closing):
            label = _unwrap_mermaid_label(suffix[len(opening):-len(closing)])
            shape = candidate_shape
            break
    if label is None:
        raise MermaidSyntaxError(f"Nó Mermaid não suportado: {cleaned!r}.")
    if len(label) > MAX_MERMAID_LABEL_CHARS:
        raise MermaidSyntaxError(
            f"O texto do nó {node_id!r} excede {MAX_MERMAID_LABEL_CHARS} caracteres."
        )
    return node_id, label, shape


def parse_mermaid(source: str) -> MermaidGraph:
    """Analisa um subconjunto seguro de Mermaid sem JavaScript ou rede."""
    raw_lines = source.splitlines()
    lines = [
        line.strip()
        for line in raw_lines
        if line.strip() and not line.lstrip().startswith("%%")
    ]
    if not lines:
        raise MermaidSyntaxError("O bloco Mermaid está vazio.")
    header = _MERMAID_HEADER_RE.fullmatch(lines[0])
    if not header:
        raise MermaidSyntaxError(
            "Use flowchart/graph com direção TD, TB, LR ou RL."
        )
    direction = header.group(1).upper()

    nodes: dict[str, MermaidNode] = {}
    edges: list[tuple[str, str]] = []
    groups: dict[str, MermaidGroup] = {}
    node_order: list[str] = []
    group_stack: list[str] = []

    def ensure_node(node_id: str, label: str | None, shape: str = "box") -> MermaidNode:
        current_group = group_stack[-1] if group_stack else None
        if node_id not in nodes:
            if len(nodes) >= MAX_MERMAID_NODES:
                raise MermaidSyntaxError(f"O fluxograma excede {MAX_MERMAID_NODES} nós.")
            nodes[node_id] = MermaidNode(
                node_id=node_id,
                label=label if label is not None else node_id,
                shape=shape,
                group_id=current_group,
                order=len(node_order),
            )
            node_order.append(node_id)
        else:
            node = nodes[node_id]
            if label is not None:
                node.label = label
            if shape != "box" or node.shape == "box":
                node.shape = shape
            if node.group_id is None and current_group is not None:
                node.group_id = current_group
        return nodes[node_id]

    for line_number, original_line in enumerate(lines[1:], start=2):
        line = original_line.rstrip(";").strip()
        if not line:
            continue
        if _MERMAID_UNSUPPORTED_RE.match(line):
            raise MermaidSyntaxError(
                f"Linha {line_number}: recurso Mermaid avançado não suportado: {line!r}."
            )

        # Direções locais de subgraph são aceitas como dica editorial. O motor
        # automático escolhe o layout global mais legível para a página A4.
        if _MERMAID_DIRECTION_RE.fullmatch(line):
            continue

        subgraph_match = _MERMAID_SUBGRAPH_RE.fullmatch(line)
        if subgraph_match:
            if len(group_stack) >= 8:
                raise MermaidSyntaxError("Subgraphs aninhados excedem o limite de segurança.")
            group_id = subgraph_match.group(1)
            label = _mermaid_unescape_label(subgraph_match.group(2) or group_id)
            if group_id not in groups:
                if len(groups) >= MAX_MERMAID_GROUPS:
                    raise MermaidSyntaxError(
                        f"O fluxograma excede {MAX_MERMAID_GROUPS} subgraphs."
                    )
                groups[group_id] = MermaidGroup(group_id, label, len(groups))
            group_stack.append(group_id)
            continue

        if line.lower() == "end":
            if not group_stack:
                raise MermaidSyntaxError(f"Linha {line_number}: 'end' sem 'subgraph'.")
            group_stack.pop()
            continue

        if _MERMAID_ARROW_RE.search(line):
            parts = _MERMAID_ARROW_RE.split(line)
            if len(parts) < 2 or any(not part.strip() for part in parts):
                raise MermaidSyntaxError(f"Linha {line_number}: conexão Mermaid inválida.")
            cleaned_parts = [parts[0]]
            for part in parts[1:]:
                cleaned_parts.append(_MERMAID_EDGE_LABEL_PREFIX_RE.sub("", part).strip())
            parsed = [_parse_mermaid_node_token(part) for part in cleaned_parts]
            for node_id, label, shape in parsed:
                ensure_node(node_id, label, shape)
            for (source_id, _, _), (target_id, _, _) in zip(parsed, parsed[1:]):
                if len(edges) >= MAX_MERMAID_EDGES:
                    raise MermaidSyntaxError(
                        f"O fluxograma excede {MAX_MERMAID_EDGES} conexões."
                    )
                edge = (source_id, target_id)
                if edge not in edges:
                    edges.append(edge)
            continue

        node_id, label, shape = _parse_mermaid_node_token(line)
        ensure_node(node_id, label, shape)

    if group_stack:
        raise MermaidSyntaxError("Existe um 'subgraph' sem o respectivo 'end'.")
    if not nodes:
        raise MermaidSyntaxError("O fluxograma não possui nós.")

    return MermaidGraph(
        direction=direction,
        nodes=nodes,
        edges=edges,
        groups=groups,
        node_order=node_order,
    )


def safe_mermaid_label(text: str) -> str:
    """Escapa a etiqueta e permite apenas <br/> e negrito balanceado."""
    token_re = re.compile(r"<\s*(/?)\s*(b|br)\s*/?\s*>", re.IGNORECASE)
    output: list[str] = []
    position = 0
    bold_open = False
    for match in token_re.finditer(text):
        output.append(html.escape(text[position:match.start()], quote=True))
        closing = bool(match.group(1))
        tag = match.group(2).lower()
        if tag == "br":
            output.append("<br/>")
        elif closing:
            if bold_open:
                output.append("</b>")
                bold_open = False
        elif not bold_open:
            output.append("<b>")
            bold_open = True
        position = match.end()
    output.append(html.escape(text[position:], quote=True))
    if bold_open:
        output.append("</b>")
    return "".join(output)


def _mermaid_predecessors(graph: MermaidGraph) -> dict[str, list[str]]:
    result: dict[str, list[str]] = defaultdict(list)
    for source_id, target_id in graph.edges:
        result[target_id].append(source_id)
    return result


def _mermaid_successors(graph: MermaidGraph) -> dict[str, list[str]]:
    result: dict[str, list[str]] = defaultdict(list)
    for source_id, target_id in graph.edges:
        result[source_id].append(target_id)
    return result


def _mermaid_layers_for_nodes(
    graph: MermaidGraph,
    node_ids: Sequence[str],
    *,
    reorder: bool = True,
) -> list[list[str]]:
    """Cria camadas topológicas e reduz cruzamentos por varredura baricêntrica."""
    node_set = set(node_ids)
    order_index = {node_id: index for index, node_id in enumerate(graph.node_order)}
    successors: dict[str, list[str]] = defaultdict(list)
    predecessors: dict[str, list[str]] = defaultdict(list)
    indegree = {node_id: 0 for node_id in node_ids}

    for source_id, target_id in graph.edges:
        if source_id in node_set and target_id in node_set:
            successors[source_id].append(target_id)
            predecessors[target_id].append(source_id)
            indegree[target_id] += 1

    queue = deque(
        sorted(
            (node_id for node_id, degree in indegree.items() if degree == 0),
            key=order_index.get,
        )
    )
    depth = {node_id: 0 for node_id in node_ids}
    visited: list[str] = []

    while queue:
        node_id = queue.popleft()
        visited.append(node_id)
        for target_id in successors.get(node_id, []):
            depth[target_id] = max(depth[target_id], depth[node_id] + 1)
            indegree[target_id] -= 1
            if indegree[target_id] == 0:
                queue.append(target_id)

    # Ciclos são mantidos de forma determinística, sem recursão infinita.
    if len(visited) < len(node_ids):
        next_depth = max(depth.values(), default=-1) + 1
        for node_id in node_ids:
            if node_id not in visited:
                depth[node_id] = next_depth
                next_depth += 1

    grouped: dict[int, list[str]] = defaultdict(list)
    for node_id in node_ids:
        grouped[depth[node_id]].append(node_id)
    layers = [grouped[key] for key in sorted(grouped)]

    if not reorder or len(layers) < 2:
        return layers

    # Quatro varreduras são suficientes para fluxogramas editoriais e mantêm
    # custo previsível mesmo no limite de segurança de 250 nós.
    for _ in range(4):
        for layer_index in range(1, len(layers)):
            previous_positions = {
                node_id: index for index, node_id in enumerate(layers[layer_index - 1])
            }

            def forward_key(node_id: str) -> tuple[float, int]:
                linked = [
                    previous_positions[parent]
                    for parent in predecessors.get(node_id, [])
                    if parent in previous_positions
                ]
                barycenter = sum(linked) / len(linked) if linked else float(order_index[node_id])
                return barycenter, order_index[node_id]

            layers[layer_index].sort(key=forward_key)

        for layer_index in range(len(layers) - 2, -1, -1):
            next_positions = {
                node_id: index for index, node_id in enumerate(layers[layer_index + 1])
            }

            def backward_key(node_id: str) -> tuple[float, int]:
                linked = [
                    next_positions[child]
                    for child in successors.get(node_id, [])
                    if child in next_positions
                ]
                barycenter = sum(linked) / len(linked) if linked else float(order_index[node_id])
                return barycenter, order_index[node_id]

            layers[layer_index].sort(key=backward_key)
    return layers


def _mermaid_declared_stages(graph: MermaidGraph) -> list[tuple[str | None, list[str]]]:
    stages: list[tuple[str | None, list[str]]] = []
    current_group: str | None | object = object()
    current_nodes: list[str] = []

    for node_id in graph.node_order:
        group_id = graph.nodes[node_id].group_id
        same_stage = bool(current_nodes) and current_group == group_id
        if not same_stage:
            if current_nodes:
                stages.append(
                    (current_group if isinstance(current_group, str) else None, current_nodes)
                )
            current_nodes = []
            current_group = group_id
        current_nodes.append(node_id)

    if current_nodes:
        stages.append((current_group if isinstance(current_group, str) else None, current_nodes))
    return stages


def _mermaid_stages(
    graph: MermaidGraph,
    *,
    topological: bool = False,
) -> list[tuple[str | None, list[str]]]:
    """Ordena etapas declaradas ou, no modo automático, por dependências."""
    stages = _mermaid_declared_stages(graph)
    if not topological or len(stages) < 2:
        return stages

    node_stage: dict[str, int] = {}
    for stage_index, (_, node_ids) in enumerate(stages):
        for node_id in node_ids:
            node_stage[node_id] = stage_index

    successors: dict[int, set[int]] = defaultdict(set)
    indegree = {index: 0 for index in range(len(stages))}
    for source_id, target_id in graph.edges:
        source_stage = node_stage.get(source_id)
        target_stage = node_stage.get(target_id)
        if source_stage is None or target_stage is None or source_stage == target_stage:
            continue
        if target_stage not in successors[source_stage]:
            successors[source_stage].add(target_stage)
            indegree[target_stage] += 1

    queue = deque(index for index in range(len(stages)) if indegree[index] == 0)
    ordered: list[int] = []
    while queue:
        stage_index = min(queue)
        queue.remove(stage_index)
        ordered.append(stage_index)
        for target_stage in sorted(successors.get(stage_index, set())):
            indegree[target_stage] -= 1
            if indegree[target_stage] == 0:
                queue.append(target_stage)

    if len(ordered) != len(stages):
        return stages
    return [stages[index] for index in ordered]


def _mermaid_plan_candidates(graph: MermaidGraph, mode: str) -> list[MermaidLayoutPlan]:
    declared_horizontal = graph.direction in {"LR", "RL"}
    reverse = graph.direction == "RL"

    balanced_vertical = MermaidLayoutPlan(
        "vertical-balanced",
        orientation="vertical",
        density="balanced",
        reorder_nodes=True,
        reorder_stages=True,
    )
    if mode == "strict":
        if declared_horizontal:
            return [
                MermaidLayoutPlan(
                    "strict-horizontal",
                    orientation="horizontal",
                    density="balanced",
                    reorder_nodes=True,
                    reorder_stages=False,
                    node_min_width=60.0,
                    node_max_width=180.0,
                    column_gap=8.0,
                    row_gap=10.0,
                    group_gap=12.0,
                    reverse=reverse,
                )
            ]
        return [
            MermaidLayoutPlan(
                "strict-vertical",
                orientation="vertical",
                density="balanced",
                reorder_nodes=False,
                reorder_stages=False,
            )
        ]

    candidates = [
        balanced_vertical,
        MermaidLayoutPlan(
            "vertical-compact",
            orientation="vertical",
            density="compact",
            reorder_nodes=True,
            reorder_stages=True,
            node_min_width=78.0,
            node_max_width=190.0,
            column_gap=10.0,
            row_gap=9.0,
            group_gap=11.0,
        ),
        MermaidLayoutPlan(
            "vertical-readable",
            orientation="vertical",
            density="readable",
            reorder_nodes=True,
            reorder_stages=True,
            node_min_width=118.0,
            node_max_width=250.0,
            column_gap=18.0,
            row_gap=15.0,
            group_gap=17.0,
        ),
        MermaidLayoutPlan(
            "vertical-declared",
            orientation="vertical",
            density="balanced",
            reorder_nodes=False,
            reorder_stages=False,
        ),
    ]

    average_label = sum(len(node.label) for node in graph.nodes.values()) / max(1, len(graph.nodes))
    if average_label > 90:
        candidates.append(
            MermaidLayoutPlan(
                "vertical-long-labels",
                orientation="vertical",
                density="readable",
                reorder_nodes=True,
                reorder_stages=True,
                max_columns=2,
                node_min_width=150.0,
                node_max_width=280.0,
                column_gap=16.0,
                row_gap=14.0,
                group_gap=16.0,
            )
        )

    # O candidato horizontal é avaliado apenas em grafos de porte controlado.
    # Diagramas grandes continuam pagináveis e legíveis no eixo vertical.
    if len(graph.nodes) <= 24 and len(graph.groups) <= 8:
        candidates.extend(
            [
                MermaidLayoutPlan(
                    "horizontal-balanced",
                    orientation="horizontal",
                    density="balanced",
                    reorder_nodes=True,
                    reorder_stages=True,
                    node_min_width=72.0,
                    node_max_width=180.0,
                    column_gap=10.0,
                    row_gap=10.0,
                    group_gap=12.0,
                    reverse=reverse,
                ),
                MermaidLayoutPlan(
                    "horizontal-compact",
                    orientation="horizontal",
                    density="compact",
                    reorder_nodes=True,
                    reorder_stages=True,
                    node_min_width=62.0,
                    node_max_width=160.0,
                    column_gap=8.0,
                    row_gap=8.0,
                    group_gap=9.0,
                    reverse=reverse,
                ),
            ]
        )
    return candidates


class MermaidFlowchart(Flowable):
    """Fluxograma vetorial com seleção automática de layout e paginação."""

    SIDE_PADDING = 9.0
    GROUP_TITLE_HEIGHT = 19.0
    GROUP_BOTTOM_PADDING = 9.0
    TOP_PADDING = 2.0
    BOTTOM_PADDING = 2.0
    FULL_PAGE_HEIGHT = A4[1] - PAGE_TOP_MARGIN - PAGE_BOTTOM_MARGIN

    def __init__(
        self,
        graph: MermaidGraph,
        theme: PdfTheme,
        node_style: ParagraphStyle,
        group_style: ParagraphStyle,
        *,
        plan: MermaidLayoutPlan,
        slice_start: int = 0,
        slice_end: int | None = None,
    ) -> None:
        super().__init__()
        self.graph = graph
        self.theme = theme
        self.node_style = node_style
        self.group_style = group_style
        self.plan = plan
        self.slice_start = slice_start
        self.slice_end = slice_end
        self.spaceBefore = 5 * mm
        self.spaceAfter = 6 * mm
        self._cached_key: tuple[float, float] | None = None
        self._cached_layout: dict | None = None

    @property
    def node_count(self) -> int:
        return len(self.graph.nodes)

    def _paragraph_for(self, node_id: str) -> Paragraph:
        return Paragraph(safe_mermaid_label(self.graph.nodes[node_id].label), self.node_style)

    def _visual_rows(self, avail_width: float) -> list[dict]:
        computed_columns = max(
            1,
            int(
                (avail_width + self.plan.column_gap)
                // (self.plan.node_min_width + self.plan.column_gap)
            ),
        )
        max_columns = self.plan.max_columns or computed_columns
        max_columns = max(1, min(max_columns, computed_columns))
        rows: list[dict] = []
        stages = _mermaid_stages(
            self.graph,
            topological=self.plan.reorder_stages,
        )
        for stage_index, (group_id, stage_nodes) in enumerate(stages):
            stage_layers = _mermaid_layers_for_nodes(
                self.graph,
                stage_nodes,
                reorder=self.plan.reorder_nodes,
            )
            group_row_index = 0
            for layer in stage_layers:
                for start in range(0, len(layer), max_columns):
                    rows.append(
                        {
                            "nodes": layer[start:start + max_columns],
                            "group_id": group_id,
                            "stage_index": stage_index,
                            "group_row_index": group_row_index,
                        }
                    )
                    group_row_index += 1
        return rows

    def _visual_columns(self) -> list[dict]:
        columns: list[dict] = []
        stages = _mermaid_stages(
            self.graph,
            topological=self.plan.reorder_stages,
        )
        for stage_index, (group_id, stage_nodes) in enumerate(stages):
            stage_layers = _mermaid_layers_for_nodes(
                self.graph,
                stage_nodes,
                reorder=self.plan.reorder_nodes,
            )
            for group_column_index, layer in enumerate(stage_layers):
                columns.append(
                    {
                        "nodes": list(layer),
                        "group_id": group_id,
                        "stage_index": stage_index,
                        "group_column_index": group_column_index,
                    }
                )
        if self.plan.reverse:
            columns.reverse()
        return columns

    def _node_dimensions(self, node_id: str, node_width: float) -> tuple[Paragraph, float]:
        paragraph = self._paragraph_for(node_id)
        node = self.graph.nodes[node_id]
        horizontal_padding = 44.0 if node.shape == "decision" else 18.0
        _, paragraph_height = paragraph.wrap(max(20.0, node_width - horizontal_padding), 10_000)
        base_height = 44.0 if node.shape == "decision" else 34.0
        extra_height = 22.0 if node.shape == "decision" else 12.0
        if node.shape in {"ellipse", "stadium"}:
            extra_height += 4.0
        return paragraph, max(base_height, paragraph_height + extra_height)

    def _layout_vertical(self, avail_width: float) -> dict:
        all_rows = self._visual_rows(avail_width)
        end = len(all_rows) if self.slice_end is None else min(self.slice_end, len(all_rows))
        rows = all_rows[self.slice_start:end]
        row_data: list[dict] = []
        group_segments: list[dict] = []
        y_cursor = self.TOP_PADDING
        active_segment: dict | None = None

        for local_index, row_info in enumerate(rows):
            group_id = row_info["group_id"]
            previous_group = rows[local_index - 1]["group_id"] if local_index > 0 else object()
            next_group = rows[local_index + 1]["group_id"] if local_index + 1 < len(rows) else object()
            starts_segment = local_index == 0 or group_id != previous_group
            ends_segment = local_index + 1 == len(rows) or group_id != next_group

            if starts_segment:
                if row_data:
                    y_cursor += self.plan.group_gap
                active_segment = {
                    "group_id": group_id,
                    "top": y_cursor,
                    "continued": row_info["group_row_index"] > 0,
                    "row_indexes": [],
                }
                if group_id is not None:
                    y_cursor += self.GROUP_TITLE_HEIGHT

            row = row_info["nodes"]
            count = max(1, len(row))
            available_for_nodes = (
                avail_width - 2 * self.SIDE_PADDING - self.plan.column_gap * (count - 1)
            )
            node_width = max(58.0, min(self.plan.node_max_width, available_for_nodes / count))
            total_width = node_width * count + self.plan.column_gap * (count - 1)
            first_x = (avail_width - total_width) / 2.0
            node_entries: list[dict] = []
            row_height = 0.0

            for index, node_id in enumerate(row):
                paragraph, node_height = self._node_dimensions(node_id, node_width)
                row_height = max(row_height, node_height)
                node_entries.append(
                    {
                        "id": node_id,
                        "x": first_x + index * (node_width + self.plan.column_gap),
                        "width": node_width,
                        "height": node_height,
                        "paragraph": paragraph,
                    }
                )

            row_record = {
                "top": y_cursor,
                "height": row_height,
                "nodes": node_entries,
                "group_id": group_id,
                "global_index": self.slice_start + local_index,
            }
            row_data.append(row_record)
            if active_segment is not None:
                active_segment["row_indexes"].append(len(row_data) - 1)

            y_cursor += row_height
            if not ends_segment:
                y_cursor += self.plan.row_gap
            else:
                if group_id is not None:
                    y_cursor += self.GROUP_BOTTOM_PADDING
                if active_segment is not None:
                    active_segment["bottom"] = y_cursor
                    group_segments.append(active_segment)
                    active_segment = None

        total_height = max(self.TOP_PADDING + self.BOTTOM_PADDING, y_cursor + self.BOTTOM_PADDING)
        positions: dict[str, tuple[float, float, float, float, Paragraph]] = {}
        for row in row_data:
            for entry in row["nodes"]:
                x = entry["x"]
                y = total_height - row["top"] - entry["height"]
                positions[entry["id"]] = (
                    x, y, entry["width"], entry["height"], entry["paragraph"]
                )

        global_index: dict[str, int] = {}
        for index, row in enumerate(all_rows):
            for node_id in row["nodes"]:
                global_index[node_id] = index

        for segment in group_segments:
            visible_boxes = [
                positions[entry["id"]]
                for row_index in segment["row_indexes"]
                for entry in row_data[row_index]["nodes"]
            ]
            if visible_boxes:
                segment["left"] = max(1.0, min(box[0] for box in visible_boxes) - 9.0)
                segment["right"] = min(
                    avail_width - 1.0,
                    max(box[0] + box[2] for box in visible_boxes) + 9.0,
                )
                segment["pdf_bottom"] = total_height - segment["bottom"]
                segment["pdf_top"] = total_height - segment["top"]

        return {
            "axis": "vertical",
            "all_items": all_rows,
            "items": rows,
            "item_data": row_data,
            "height": total_height,
            "positions": positions,
            "global_index": global_index,
            "groups": group_segments,
            "end": end,
            "overflow": False,
        }

    def _horizontal_columns_fit(self, avail_width: float) -> int:
        return max(
            1,
            int(
                (avail_width - 2 * self.SIDE_PADDING + self.plan.column_gap)
                // (self.plan.node_min_width + self.plan.column_gap)
            ),
        )

    def _layout_horizontal(self, avail_width: float) -> dict:
        all_columns = self._visual_columns()
        end = len(all_columns) if self.slice_end is None else min(self.slice_end, len(all_columns))
        columns = all_columns[self.slice_start:end]
        count = max(1, len(columns))
        available_for_nodes = (
            avail_width - 2 * self.SIDE_PADDING - self.plan.column_gap * (count - 1)
        )
        node_width = max(58.0, min(self.plan.node_max_width, available_for_nodes / count))
        total_width = node_width * count + self.plan.column_gap * (count - 1)
        first_x = (avail_width - total_width) / 2.0

        column_data: list[dict] = []
        max_height = 0.0
        for column_index, column in enumerate(columns):
            entries: list[dict] = []
            content_height = 0.0
            for node_id in column["nodes"]:
                paragraph, node_height = self._node_dimensions(node_id, node_width)
                if entries:
                    content_height += self.plan.row_gap
                entries.append(
                    {
                        "id": node_id,
                        "height": node_height,
                        "width": node_width,
                        "paragraph": paragraph,
                    }
                )
                content_height += node_height
            title_space = self.GROUP_TITLE_HEIGHT if column["group_id"] is not None else 0.0
            column_height = content_height + title_space + 2 * self.GROUP_BOTTOM_PADDING
            max_height = max(max_height, column_height)
            column_data.append(
                {
                    **column,
                    "x": first_x + column_index * (node_width + self.plan.column_gap),
                    "width": node_width,
                    "entries": entries,
                    "content_height": content_height,
                    "height": column_height,
                    "global_index": self.slice_start + column_index,
                }
            )

        total_height = max(48.0, max_height + self.TOP_PADDING + self.BOTTOM_PADDING)
        positions: dict[str, tuple[float, float, float, float, Paragraph]] = {}
        group_segments: list[dict] = []
        active: dict | None = None

        for local_index, column in enumerate(column_data):
            group_id = column["group_id"]
            previous_group = column_data[local_index - 1]["group_id"] if local_index > 0 else object()
            next_group = column_data[local_index + 1]["group_id"] if local_index + 1 < len(column_data) else object()
            starts = local_index == 0 or group_id != previous_group
            ends = local_index + 1 == len(column_data) or group_id != next_group
            if starts:
                active = {
                    "group_id": group_id,
                    "left": column["x"] - 7.0,
                    "continued": column["group_column_index"] > 0,
                }

            title_space = self.GROUP_TITLE_HEIGHT if group_id is not None else 0.0
            content_top = total_height - self.TOP_PADDING - title_space - self.GROUP_BOTTOM_PADDING
            y_cursor = content_top
            for entry in column["entries"]:
                y_cursor -= entry["height"]
                positions[entry["id"]] = (
                    column["x"], y_cursor, entry["width"], entry["height"], entry["paragraph"]
                )
                y_cursor -= self.plan.row_gap

            if ends and active is not None:
                active["right"] = column["x"] + column["width"] + 7.0
                active["pdf_bottom"] = 1.0
                active["pdf_top"] = total_height - 1.0
                group_segments.append(active)
                active = None

        global_index: dict[str, int] = {}
        for index, column in enumerate(all_columns):
            for node_id in column["nodes"]:
                global_index[node_id] = index

        return {
            "axis": "horizontal",
            "all_items": all_columns,
            "items": columns,
            "item_data": column_data,
            "height": total_height,
            "positions": positions,
            "global_index": global_index,
            "groups": group_segments,
            "end": end,
            "overflow": self.slice_end is None
            and len(all_columns) > self._horizontal_columns_fit(avail_width),
        }

    def _layout(self, avail_width: float, avail_height: float | None = None) -> dict:
        height_key = round(avail_height or self.FULL_PAGE_HEIGHT, 1)
        key = (round(avail_width, 1), height_key)
        if self._cached_layout is not None and self._cached_key == key:
            return self._cached_layout
        if self.plan.orientation == "horizontal":
            layout = self._layout_horizontal(avail_width)
        else:
            layout = self._layout_vertical(avail_width)
        self._cached_key = key
        self._cached_layout = layout
        return layout

    def wrap(self, availWidth: float, availHeight: float) -> tuple[float, float]:
        layout = self._layout(availWidth, availHeight)
        self.width = availWidth
        if layout.get("overflow"):
            # Força o ReportLab a chamar split(), que pagina o eixo horizontal.
            self.height = max(availHeight + 1.0, self.FULL_PAGE_HEIGHT + 1.0)
        else:
            self.height = layout["height"]
        return self.width, self.height

    def _height_for_range(self, avail_width: float, start: int, end: int) -> float:
        candidate = MermaidFlowchart(
            self.graph,
            self.theme,
            self.node_style,
            self.group_style,
            plan=self.plan,
            slice_start=start,
            slice_end=end,
        )
        return candidate._layout(avail_width, self.FULL_PAGE_HEIGHT)["height"]

    def _vertical_split(self, availWidth: float, availHeight: float) -> list[Flowable]:
        layout = self._layout_vertical(availWidth)
        if layout["height"] <= availHeight:
            return [self]
        all_rows = layout["all_items"]
        end = len(all_rows) if self.slice_end is None else min(self.slice_end, len(all_rows))
        if self.slice_start >= end:
            return []

        best_end = self.slice_start
        for candidate_end in range(self.slice_start + 1, end + 1):
            if self._height_for_range(availWidth, self.slice_start, candidate_end) <= availHeight:
                best_end = candidate_end
            else:
                break
        if best_end == self.slice_start:
            return []

        boundary_candidates = [
            index
            for index in range(self.slice_start + 1, best_end + 1)
            if index == end
            or all_rows[index - 1]["group_id"] != all_rows[index]["group_id"]
        ]
        for boundary in reversed(boundary_candidates):
            remainder_height = self._height_for_range(availWidth, boundary, end)
            if remainder_height <= self.FULL_PAGE_HEIGHT:
                best_end = boundary
                break

        first = MermaidFlowchart(
            self.graph,
            self.theme,
            self.node_style,
            self.group_style,
            plan=self.plan,
            slice_start=self.slice_start,
            slice_end=best_end,
        )
        if best_end >= end:
            return [first]
        remainder = MermaidFlowchart(
            self.graph,
            self.theme,
            self.node_style,
            self.group_style,
            plan=self.plan,
            slice_start=best_end,
            slice_end=end,
        )
        return [first, remainder]

    def _horizontal_split(self, availWidth: float, availHeight: float) -> list[Flowable]:
        all_columns = self._visual_columns()
        end = len(all_columns) if self.slice_end is None else min(self.slice_end, len(all_columns))
        if self.slice_start >= end:
            return []
        fit = self._horizontal_columns_fit(availWidth)
        best_end = min(end, self.slice_start + fit)

        boundary_candidates = [
            index
            for index in range(self.slice_start + 1, best_end + 1)
            if index == end
            or all_columns[index - 1]["group_id"] != all_columns[index]["group_id"]
        ]
        if boundary_candidates:
            candidate = boundary_candidates[-1]
            if candidate > self.slice_start:
                best_end = candidate

        first = MermaidFlowchart(
            self.graph,
            self.theme,
            self.node_style,
            self.group_style,
            plan=self.plan,
            slice_start=self.slice_start,
            slice_end=best_end,
        )
        first_height = first._layout(availWidth, availHeight)["height"]
        if first_height > availHeight:
            if first_height <= self.FULL_PAGE_HEIGHT:
                return []
            # Um eixo horizontal com paralelismo excessivo não cabe de forma
            # legível. O modo estrito usa fallback vertical somente nesse caso.
            fallback = MermaidLayoutPlan(
                "horizontal-overflow-fallback",
                orientation="vertical",
                density="compact",
                reorder_nodes=True,
                reorder_stages=True,
                node_min_width=78.0,
                node_max_width=190.0,
                column_gap=10.0,
                row_gap=9.0,
                group_gap=11.0,
            )
            return [
                MermaidFlowchart(
                    self.graph,
                    self.theme,
                    self.node_style,
                    self.group_style,
                    plan=fallback,
                )
            ]

        if best_end >= end:
            return [first]
        remainder = MermaidFlowchart(
            self.graph,
            self.theme,
            self.node_style,
            self.group_style,
            plan=self.plan,
            slice_start=best_end,
            slice_end=end,
        )
        return [first, PageBreak(), remainder]

    def split(self, availWidth: float, availHeight: float) -> list[Flowable]:
        if self.plan.orientation == "horizontal":
            return self._horizontal_split(availWidth, availHeight)
        return self._vertical_split(availWidth, availHeight)

    @staticmethod
    def _draw_arrowhead(canvas, x1: float, y1: float, x2: float, y2: float) -> None:
        angle = math.atan2(y2 - y1, x2 - x1)
        size = 5.0
        for offset in (2.55, -2.55):
            canvas.line(
                x2,
                y2,
                x2 + size * math.cos(angle + offset),
                y2 + size * math.sin(angle + offset),
            )

    @classmethod
    def _draw_polyline_arrow(cls, canvas, points: Sequence[tuple[float, float]]) -> None:
        if len(points) < 2:
            return
        for (x1, y1), (x2, y2) in zip(points, points[1:]):
            canvas.line(x1, y1, x2, y2)
        cls._draw_arrowhead(canvas, *points[-2], *points[-1])

    @staticmethod
    def _segment_hits_box(
        p1: tuple[float, float],
        p2: tuple[float, float],
        box: tuple[float, float, float, float, Paragraph],
        margin: float = 3.0,
    ) -> bool:
        x, y, width, height, _ = box
        left, right = x - margin, x + width + margin
        bottom, top = y - margin, y + height + margin
        x1, y1 = p1
        x2, y2 = p2
        if abs(x1 - x2) < 0.1:
            return left <= x1 <= right and max(min(y1, y2), bottom) <= min(max(y1, y2), top)
        if abs(y1 - y2) < 0.1:
            return bottom <= y1 <= top and max(min(x1, x2), left) <= min(max(x1, x2), right)
        return False

    @classmethod
    def _route_vertical(
        cls,
        source_id: str,
        target_id: str,
        source,
        target,
        positions,
        width: float,
        edge_index: int,
    ) -> list[tuple[float, float]]:
        sx, sy, sw, sh, _ = source
        tx, ty, tw, th, _ = target
        start = (sx + sw / 2, sy)
        finish = (tx + tw / 2, ty + th)
        middle_y = (start[1] + finish[1]) / 2
        direct = [start, (start[0], middle_y), (finish[0], middle_y), finish]

        def collisions(points: Sequence[tuple[float, float]]) -> int:
            count = 0
            for node_id, box in positions.items():
                if node_id in {source_id, target_id}:
                    continue
                for first, second in zip(points, points[1:]):
                    if cls._segment_hits_box(first, second, box):
                        count += 1
                        break
            return count

        track = 6.0 + (edge_index % 5) * 5.0
        left_x = track
        right_x = width - track
        left = [start, (start[0], start[1] - 5), (left_x, start[1] - 5), (left_x, finish[1] + 5), (finish[0], finish[1] + 5), finish]
        right = [start, (start[0], start[1] - 5), (right_x, start[1] - 5), (right_x, finish[1] + 5), (finish[0], finish[1] + 5), finish]
        candidates = (direct, left, right)
        return min(
            candidates,
            key=lambda points: (
                collisions(points),
                sum(abs(a[0] - b[0]) + abs(a[1] - b[1]) for a, b in zip(points, points[1:])),
            ),
        )

    @classmethod
    def _route_horizontal(
        cls,
        source_id: str,
        target_id: str,
        source,
        target,
        positions,
        height: float,
        edge_index: int,
    ) -> list[tuple[float, float]]:
        sx, sy, sw, sh, _ = source
        tx, ty, tw, th, _ = target
        if tx >= sx:
            start = (sx + sw, sy + sh / 2)
            finish = (tx, ty + th / 2)
        else:
            start = (sx, sy + sh / 2)
            finish = (tx + tw, ty + th / 2)
        middle_x = (start[0] + finish[0]) / 2
        direct = [start, (middle_x, start[1]), (middle_x, finish[1]), finish]

        def collisions(points: Sequence[tuple[float, float]]) -> int:
            count = 0
            for node_id, box in positions.items():
                if node_id in {source_id, target_id}:
                    continue
                for first, second in zip(points, points[1:]):
                    if cls._segment_hits_box(first, second, box):
                        count += 1
                        break
            return count

        track = 6.0 + (edge_index % 5) * 5.0
        bottom_y = track
        top_y = height - track
        bottom = [start, (start[0] + 5, start[1]), (start[0] + 5, bottom_y), (finish[0] - 5, bottom_y), (finish[0] - 5, finish[1]), finish]
        top = [start, (start[0] + 5, start[1]), (start[0] + 5, top_y), (finish[0] - 5, top_y), (finish[0] - 5, finish[1]), finish]
        candidates = (direct, bottom, top)
        return min(
            candidates,
            key=lambda points: (
                collisions(points),
                sum(abs(a[0] - b[0]) + abs(a[1] - b[1]) for a, b in zip(points, points[1:])),
            ),
        )

    def _draw_groups(self, canvas, layout: dict) -> None:
        for segment in layout["groups"]:
            group_id = segment["group_id"]
            if group_id is None:
                continue
            group = self.graph.groups.get(group_id)
            if group is None:
                continue
            left = segment["left"]
            right = segment["right"]
            bottom = segment["pdf_bottom"]
            top = segment["pdf_top"]
            canvas.setFillColor(self.theme.mermaid_group_background)
            canvas.setStrokeColor(self.theme.mermaid_group_border)
            canvas.setLineWidth(0.7)
            canvas.setDash(3, 2)
            canvas.roundRect(left, bottom, right - left, top - bottom, 6, stroke=1, fill=1)
            canvas.setDash()
            label = group.label + (" (continuação)" if segment["continued"] else "")
            caption = Paragraph(safe_mermaid_label(label), self.group_style)
            _, caption_height = caption.wrap(max(30, right - left - 12), 40)
            caption.drawOn(canvas, left + 6, top - caption_height - 2)

    def _draw_edges(self, canvas, layout: dict) -> None:
        positions = layout["positions"]
        global_index = layout["global_index"]
        fragment_start = self.slice_start
        fragment_end = layout["end"]
        canvas.setStrokeColor(self.theme.mermaid_edge)
        canvas.setLineWidth(0.9)

        for edge_index, (source_id, target_id) in enumerate(self.graph.edges):
            source = positions.get(source_id)
            target = positions.get(target_id)
            if source and target:
                if layout["axis"] == "horizontal":
                    points = self._route_horizontal(
                        source_id, target_id, source, target, positions, self.height, edge_index
                    )
                else:
                    points = self._route_vertical(
                        source_id, target_id, source, target, positions, self.width, edge_index
                    )
                self._draw_polyline_arrow(canvas, points)
                continue

            source_index = global_index.get(source_id)
            target_index = global_index.get(target_id)
            if layout["axis"] == "vertical":
                if source and target_index is not None and target_index >= fragment_end:
                    sx, sy, sw, _, _ = source
                    self._draw_polyline_arrow(canvas, [(sx + sw / 2, sy), (sx + sw / 2, 3)])
                elif target and source_index is not None and source_index < fragment_start:
                    tx, ty, tw, th, _ = target
                    self._draw_polyline_arrow(
                        canvas, [(tx + tw / 2, self.height - 3), (tx + tw / 2, ty + th)]
                    )
            else:
                if source and target_index is not None and target_index >= fragment_end:
                    sx, sy, sw, sh, _ = source
                    self._draw_polyline_arrow(
                        canvas, [(sx + sw, sy + sh / 2), (self.width - 3, sy + sh / 2)]
                    )
                elif target and source_index is not None and source_index < fragment_start:
                    tx, ty, _, th, _ = target
                    self._draw_polyline_arrow(
                        canvas, [(3, ty + th / 2), (tx, ty + th / 2)]
                    )

    def _draw_nodes(self, canvas, positions: dict) -> None:
        for node_id in self.graph.node_order:
            box = positions.get(node_id)
            if box is None:
                continue
            x, y, width, height, paragraph = box
            canvas.setFillColor(self.theme.mermaid_node_background)
            canvas.setStrokeColor(self.theme.mermaid_node_border)
            canvas.setLineWidth(0.85)
            node = self.graph.nodes[node_id]
            if node.shape == "decision":
                path = canvas.beginPath()
                path.moveTo(x + width / 2, y + height)
                path.lineTo(x + width, y + height / 2)
                path.lineTo(x + width / 2, y)
                path.lineTo(x, y + height / 2)
                path.close()
                canvas.drawPath(path, stroke=1, fill=1)
                text_width = max(20, width - 44)
                text_height = max(20, height - 18)
            elif node.shape == "ellipse":
                canvas.ellipse(x, y, x + width, y + height, stroke=1, fill=1)
                text_width = max(20, width - 28)
                text_height = max(20, height - 14)
            elif node.shape == "stadium":
                canvas.roundRect(x, y, width, height, height / 2, stroke=1, fill=1)
                text_width = max(20, width - 24)
                text_height = max(20, height - 10)
            elif node.shape == "rounded":
                canvas.roundRect(x, y, width, height, min(14, height / 3), stroke=1, fill=1)
                text_width = max(20, width - 18)
                text_height = max(20, height - 10)
            else:
                canvas.roundRect(x, y, width, height, 7, stroke=1, fill=1)
                text_width = max(20, width - 18)
                text_height = max(20, height - 10)
            paragraph_width, paragraph_height = paragraph.wrap(text_width, text_height)
            paragraph.drawOn(
                canvas,
                x + (width - paragraph_width) / 2,
                y + (height - paragraph_height) / 2,
            )

    def draw(self) -> None:
        layout = self._layout(self.width, self.height)
        canvas = self.canv
        canvas.saveState()
        self._draw_groups(canvas, layout)
        self._draw_edges(canvas, layout)
        self._draw_nodes(canvas, layout["positions"])
        canvas.restoreState()

    def quality_score(self, avail_width: float, page_height: float) -> float:
        """Pontua legibilidade, paginação, cruzamentos e aproveitamento."""
        if self.plan.orientation == "horizontal":
            columns = self._visual_columns()
            fit = self._horizontal_columns_fit(avail_width)
            chunks = max(1, math.ceil(len(columns) / fit))
            heights: list[float] = []
            group_splits = 0
            for start in range(0, len(columns), fit):
                end = min(len(columns), start + fit)
                fragment = MermaidFlowchart(
                    self.graph,
                    self.theme,
                    self.node_style,
                    self.group_style,
                    plan=self.plan,
                    slice_start=start,
                    slice_end=end,
                )
                heights.append(fragment._layout_horizontal(avail_width)["height"])
                if end < len(columns) and columns[end - 1]["group_id"] == columns[end]["group_id"]:
                    group_splits += 1
            overflow = sum(max(0.0, height - page_height) for height in heights)
            wasted = sum(max(0.0, page_height - min(page_height, height)) for height in heights)
            score = chunks * 10_000 + overflow * 500 + group_splits * 700 + wasted * 0.12
            if self.graph.direction in {"LR", "RL"}:
                score -= 450
            else:
                score += 180
            if self.plan.density == "compact":
                score += 80
            return score

        layout = self._layout_vertical(avail_width)
        height = layout["height"]
        pages = max(1, math.ceil(height / page_height))
        rows = layout["all_items"]
        row_by_node: dict[str, int] = {}
        order_by_node: dict[str, int] = {}
        for row_index, row in enumerate(rows):
            for order, node_id in enumerate(row["nodes"]):
                row_by_node[node_id] = row_index
                order_by_node[node_id] = order

        edge_span = 0
        backward_edges = 0
        crossings = 0
        comparable: dict[tuple[int, int], list[tuple[int, int]]] = defaultdict(list)
        for source_id, target_id in self.graph.edges:
            source_row = row_by_node.get(source_id, 0)
            target_row = row_by_node.get(target_id, source_row)
            if target_row <= source_row:
                backward_edges += 1
            edge_span += abs(target_row - source_row)
            comparable[(source_row, target_row)].append(
                (order_by_node.get(source_id, 0), order_by_node.get(target_id, 0))
            )
        for edges in comparable.values():
            for index, first in enumerate(edges):
                for second in edges[index + 1:]:
                    if (first[0] - second[0]) * (first[1] - second[1]) < 0:
                        crossings += 1

        group_splits = 0
        for group in self.graph.groups:
            group_rows = [
                row_by_node[node_id]
                for node_id, node in self.graph.nodes.items()
                if node.group_id == group and node_id in row_by_node
            ]
            if group_rows:
                first_page = int((min(group_rows) / max(1, len(rows))) * pages)
                last_page = int((max(group_rows) / max(1, len(rows))) * pages)
                group_splits += max(0, last_page - first_page)

        tall_penalty = 0.0
        narrow_penalty = 0.0
        for box in layout["positions"].values():
            _, _, width, node_height, _ = box
            tall_penalty += max(0.0, node_height - 72.0)
            narrow_penalty += max(0.0, 90.0 - width)
        last_fill = (height % page_height) / page_height if pages > 1 else min(1.0, height / page_height)
        orphan_penalty = max(0.0, 0.28 - last_fill) * 1_800
        score = (
            pages * 10_000
            + crossings * 320
            + backward_edges * 260
            + group_splits * 650
            + edge_span * 9
            + tall_penalty * 7
            + narrow_penalty * 12
            + orphan_penalty
        )
        if self.graph.direction in {"TD", "TB"}:
            score -= 220
        else:
            score += 120
        if self.plan.density == "compact":
            score += 90
        elif self.plan.density == "readable":
            score -= 35
        return score


def choose_mermaid_plan(
    graph: MermaidGraph,
    theme: PdfTheme,
    node_style: ParagraphStyle,
    group_style: ParagraphStyle,
    mode: str,
) -> MermaidLayoutPlan:
    candidates = _mermaid_plan_candidates(graph, mode)
    if len(candidates) == 1:
        return candidates[0]
    scored: list[tuple[float, int, MermaidLayoutPlan]] = []
    for index, plan in enumerate(candidates):
        flowable = MermaidFlowchart(
            graph,
            theme,
            node_style,
            group_style,
            plan=plan,
        )
        score = flowable.quality_score(AVAILABLE_TABLE_WIDTH, MermaidFlowchart.FULL_PAGE_HEIGHT)
        scored.append((score, index, plan))
    scored.sort(key=lambda item: (item[0], item[1]))
    return scored[0][2]


def build_mermaid_flowable(
    source: str,
    theme: PdfTheme,
    styles: dict[str, ParagraphStyle],
    *,
    mode: str = "auto",
) -> MermaidFlowchart:
    graph = parse_mermaid(source)
    if mode not in {"auto", "strict"}:
        raise ValueError(f"Modo Mermaid desconhecido: {mode!r}.")
    plan = choose_mermaid_plan(
        graph,
        theme,
        styles["mermaid_node"],
        styles["mermaid_group"],
        mode,
    )
    return MermaidFlowchart(
        graph,
        theme,
        styles["mermaid_node"],
        styles["mermaid_group"],
        plan=plan,
    )

def _anchor_slug(value: str) -> str:
    """Normaliza títulos e destinos de links para âncoras internas seguras."""
    value = unquote(html.unescape(value)).strip().lower()
    value = re.sub(r"[*_`#<>]", "", value)
    normalized = unicodedata.normalize("NFKD", value)
    ascii_value = "".join(char for char in normalized if not unicodedata.combining(char))
    ascii_value = re.sub(r"[^a-z0-9\s-]", "", ascii_value)
    ascii_value = re.sub(r"[\s-]+", "-", ascii_value).strip("-")
    return ascii_value or "secao"


def safe_inline(text: str) -> str:
    """Escapa tudo e reintroduz somente marcações inline permitidas.

    Links externos continuam não clicáveis. Links Markdown internos no formato
    ``[rótulo](#destino)`` são transformados em navegação dentro do próprio PDF.
    """
    escaped = html.escape(text, quote=True)

    internal_link_re = re.compile(
        r"\[([^\]\n]{1,2000})\]\(\s*#([^\)\s]{1,1000})\s*\)"
    )

    def replace_internal_link(match: re.Match[str]) -> str:
        label = match.group(1)
        destination = _anchor_slug(match.group(2))
        return f'<a href="#{destination}"><u>{label}</u></a>'

    escaped = internal_link_re.sub(replace_internal_link, escaped)
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

def make_styles(theme: PdfTheme) -> dict[str, ParagraphStyle]:
    base = getSampleStyleSheet()

    styles: dict[str, ParagraphStyle] = {
        "body": ParagraphStyle(
            "SafeBody",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=10.5,
            leading=15.2,
            spaceAfter=7,
            allowWidows=0,
            allowOrphans=0,
            splitLongWords=1,
            wordWrap="LTR",
            textColor=theme.text,
        ),
        "bullet": ParagraphStyle(
            "SafeBullet",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=10.5,
            leading=15.2,
            leftIndent=14,
            firstLineIndent=-10,
            bulletIndent=2,
            bulletColor=theme.bullet,
            spaceAfter=4,
            splitLongWords=1,
            wordWrap="LTR",
            textColor=theme.text,
        ),
        "quote": ParagraphStyle(
            "SafeQuote",
            parent=base["BodyText"],
            fontName="Helvetica-Oblique",
            fontSize=10.5,
            leading=15.2,
            spaceBefore=0,
            spaceAfter=0,
            splitLongWords=1,
            wordWrap="LTR",
            textColor=theme.quote_text,
        ),
        "code": ParagraphStyle(
            "SafeCode",
            parent=base["Code"],
            fontName="Courier",
            fontSize=8.5,
            leading=11,
            leftIndent=0,
            rightIndent=0,
            spaceBefore=0,
            spaceAfter=0,
            textColor=theme.code_text,
        ),
        "table_header": ParagraphStyle(
            "SafeTableHeader",
            parent=base["BodyText"],
            fontName="Helvetica-Bold",
            fontSize=8.5,
            leading=11,
            spaceBefore=0,
            spaceAfter=0,
            splitLongWords=1,
            wordWrap="LTR",
            textColor=theme.table_header_text,
        ),
        "table_cell": ParagraphStyle(
            "SafeTableCell",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=8.5,
            leading=11,
            spaceBefore=0,
            spaceAfter=0,
            splitLongWords=1,
            wordWrap="LTR",
            textColor=theme.text,
        ),
        "mermaid_node": ParagraphStyle(
            "SafeMermaidNode",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=8.2,
            leading=10.2,
            alignment=TA_CENTER,
            spaceBefore=0,
            spaceAfter=0,
            splitLongWords=1,
            wordWrap="LTR",
            textColor=theme.mermaid_node_text,
        ),
        "mermaid_group": ParagraphStyle(
            "SafeMermaidGroup",
            parent=base["BodyText"],
            fontName="Helvetica-Bold",
            fontSize=8.0,
            leading=9.5,
            alignment=TA_LEFT,
            spaceBefore=0,
            spaceAfter=0,
            splitLongWords=1,
            wordWrap="LTR",
            textColor=theme.mermaid_group_text,
        ),
        "warning": ParagraphStyle(
            "SafeWarning",
            parent=base["BodyText"],
            fontName="Helvetica-Bold",
            fontSize=9,
            leading=12,
            leftIndent=8,
            rightIndent=8,
            borderWidth=0.6,
            borderPadding=7,
            borderColor=theme.warning_border,
            backColor=theme.warning_background,
            textColor=theme.warning_text,
            spaceBefore=4,
            spaceAfter=5,
        ),
    }

    heading_sizes = {1: 22, 2: 18, 3: 15, 4: 13, 5: 11.5, 6: 10.5}
    for level, size in heading_sizes.items():
        if level == 1:
            heading_color = theme.title
        elif level == 2:
            heading_color = theme.heading
        else:
            heading_color = theme.subheading
        styles[f"h{level}"] = ParagraphStyle(
            f"SafeHeading{level}",
            parent=base[f"Heading{min(level, 4)}"],
            fontName="Helvetica-Bold",
            fontSize=size,
            leading=size * 1.25,
            spaceBefore=12 if level > 1 else 4,
            spaceAfter=7,
            alignment=TA_CENTER if level == 1 else TA_LEFT,
            keepWithNext=1,
            splitLongWords=1,
            wordWrap="LTR",
            textColor=heading_color,
        )

    return styles


def build_quote_flowable(
    quote_text: str,
    styles: dict[str, ParagraphStyle],
    theme: PdfTheme,
) -> Table:
    """Cria citação com fundo e barra lateral, sem interpretar HTML arbitrário."""
    table = Table(
        [[Paragraph(safe_inline(quote_text), styles["quote"])]],
        colWidths=[AVAILABLE_TABLE_WIDTH],
        hAlign="LEFT",
        spaceBefore=2 * mm,
        spaceAfter=4 * mm,
    )
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), theme.quote_background),
                ("LINEBEFORE", (0, 0), (0, -1), 3.0, theme.quote_bar),
                ("LEFTPADDING", (0, 0), (-1, -1), 10),
                ("RIGHTPADDING", (0, 0), (-1, -1), 9),
                ("TOPPADDING", (0, 0), (-1, -1), 7),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ]
        )
    )
    return table


def _fit_prefix_by_width(
    text: str,
    *,
    font_name: str,
    font_size: float,
    max_width: float,
) -> int:
    """Retorna o maior prefixo que cabe na largura disponível."""
    if not text:
        return 0
    if pdfmetrics.stringWidth(text, font_name, font_size) <= max_width:
        return len(text)

    low, high = 1, len(text)
    best = 1
    while low <= high:
        middle = (low + high) // 2
        width = pdfmetrics.stringWidth(text[:middle], font_name, font_size)
        if width <= max_width:
            best = middle
            low = middle + 1
        else:
            high = middle - 1
    return max(1, best)


def _wrap_preformatted_line(
    line: str,
    *,
    font_name: str,
    font_size: float,
    max_width: float,
    prose_mode: bool,
) -> list[str]:
    """Quebra uma linha pré-formatada sem permitir corte horizontal no PDF.

    Em blocos ``text``/``txt``/``plaintext``, prioriza espaços entre palavras.
    Nos demais blocos, preserva a indentação e também procura pontos seguros
    de quebra antes de recorrer à divisão rígida de uma palavra muito longa.
    """
    expanded = line.expandtabs(4)
    if not expanded:
        return [" "]

    result: list[str] = []
    remaining = expanded
    original_indent_match = re.match(r"^\s*", expanded)
    original_indent = original_indent_match.group(0) if original_indent_match else ""
    continuation_indent = "" if prose_mode else original_indent

    while remaining:
        if pdfmetrics.stringWidth(remaining, font_name, font_size) <= max_width:
            result.append(remaining or " ")
            break

        fit = _fit_prefix_by_width(
            remaining,
            font_name=font_name,
            font_size=font_size,
            max_width=max_width,
        )

        # Prefere quebrar em espaço. Para código, aceita também pontuação
        # comum para evitar cortar identificadores quando há alternativa.
        search = remaining[: fit + 1]
        break_at = max(search.rfind(" "), search.rfind("\t"))
        if not prose_mode:
            for token in (",", ";", ":", "/", "\\", "-", "_", "=", "+", ")", "]", "}"):
                position = search.rfind(token)
                if position >= 0:
                    break_at = max(break_at, position + 1)

        # Não usa uma quebra excessivamente curta; nesse caso divide no
        # limite calculado, garantindo avanço e ausência de clipping.
        minimum_useful = max(1, fit // 3)
        if break_at < minimum_useful:
            break_at = fit

        chunk = remaining[:break_at].rstrip()
        if not chunk:
            chunk = remaining[:fit]
            break_at = fit
        result.append(chunk)

        remaining = remaining[break_at:]
        if prose_mode:
            remaining = remaining.lstrip()
        else:
            remaining = remaining.lstrip(" ")
            if remaining and continuation_indent:
                candidate = continuation_indent + remaining
                # Evita que uma indentação enorme impeça qualquer conteúdo
                # de caber na linha de continuação.
                if pdfmetrics.stringWidth(candidate, font_name, font_size) < max_width:
                    remaining = candidate

    return result or [" "]


def build_code_flowable(
    code: str,
    styles: dict[str, ParagraphStyle],
    theme: PdfTheme,
    *,
    language: str = "",
) -> LongTable:
    """Cria bloco pré-formatado divisível e sem corte horizontal.

    A quebra é calculada pela largura real da fonte, e não por uma quantidade
    fixa de caracteres. Assim, frases longas em blocos ``text`` e linhas de
    código extensas continuam integralmente visíveis no PDF.
    """
    raw_lines = code.splitlines() or [""]
    code_style = styles["code"]
    font_name = code_style.fontName or "Courier"
    font_size = float(code_style.fontSize or 8.5)
    # Desconta os paddings esquerdo e direito usados na tabela.
    content_width = max(20.0, AVAILABLE_TABLE_WIDTH - 16.0)
    prose_mode = language.lower() in {"text", "txt", "plaintext", "plain"}

    wrapped_lines: list[str] = []
    for raw_line in raw_lines:
        wrapped_lines.extend(
            _wrap_preformatted_line(
                raw_line,
                font_name=font_name,
                font_size=font_size,
                max_width=content_width,
                prose_mode=prose_mode,
            )
        )

    rows = [
        [Preformatted(line if line else " ", code_style, maxLineLength=None)]
        for line in wrapped_lines
    ]
    table = LongTable(
        rows,
        colWidths=[AVAILABLE_TABLE_WIDTH],
        hAlign="LEFT",
        splitByRow=1,
        splitInRow=1,
        spaceBefore=3 * mm,
        spaceAfter=5 * mm,
    )
    commands: list[tuple] = [
        ("BACKGROUND", (0, 0), (-1, -1), theme.code_background),
        ("BOX", (0, 0), (-1, -1), 0.6, theme.code_border),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]
    if rows:
        commands.extend(
            [
                ("TOPPADDING", (0, 0), (-1, 0), 7),
                ("BOTTOMPADDING", (0, -1), (-1, -1), 7),
            ]
        )
    table.setStyle(TableStyle(commands))
    return table


def _count_backticks(text: str, start: int) -> int:
    end = start
    while end < len(text) and text[end] == "`":
        end += 1
    return end - start


def split_table_row(line: str) -> list[str]:
    r"""Divide uma linha de tabela sem quebrar em \| ou dentro de código inline.

    O tratamento é intencionalmente limitado e seguro:
    - ``\|`` vira um pipe literal na célula;
    - pipes dentro de spans delimitados por crases não separam colunas;
    - pipes externos delimitam colunas.
    """
    cells: list[str] = []
    current: list[str] = []
    active_code_ticks: int | None = None
    index = 0

    while index < len(line):
        char = line[index]

        if char == "\\" and index + 1 < len(line) and line[index + 1] == "|":
            current.append("|")
            index += 2
            continue

        if char == "`":
            run = _count_backticks(line, index)
            current.append("`" * run)
            if active_code_ticks is None:
                active_code_ticks = run
            elif active_code_ticks == run:
                active_code_ticks = None
            index += run
            continue

        if char == "|" and active_code_ticks is None:
            cells.append("".join(current).strip())
            current = []
        else:
            current.append(char)
        index += 1

    cells.append("".join(current).strip())

    stripped = line.strip()
    if stripped.startswith("|") and cells and cells[0] == "":
        cells.pop(0)
    if cells and cells[-1] == "" and _has_unescaped_trailing_pipe(stripped):
        cells.pop()

    return cells


def _has_unescaped_trailing_pipe(text: str) -> bool:
    if not text.endswith("|"):
        return False
    backslashes = 0
    index = len(text) - 2
    while index >= 0 and text[index] == "\\":
        backslashes += 1
        index -= 1
    return backslashes % 2 == 0


def _contains_table_pipe(line: str) -> bool:
    """Retorna True quando existe pipe delimitador fora de código inline."""
    active_code_ticks: int | None = None
    index = 0
    while index < len(line):
        char = line[index]
        if char == "\\" and index + 1 < len(line) and line[index + 1] == "|":
            index += 2
            continue
        if char == "`":
            run = _count_backticks(line, index)
            if active_code_ticks is None:
                active_code_ticks = run
            elif active_code_ticks == run:
                active_code_ticks = None
            index += run
            continue
        if char == "|" and active_code_ticks is None:
            return True
        index += 1
    return False


def parse_table_separator(line: str) -> list[str] | None:
    """Lê a linha ``--- | :---: | ---:`` e retorna alinhamentos."""
    cells = split_table_row(line)
    if not cells:
        return None

    alignments: list[str] = []
    for cell in cells:
        compact = re.sub(r"\s+", "", cell)
        if not TABLE_SEPARATOR_CELL_RE.fullmatch(compact):
            return None
        if compact.startswith(":") and compact.endswith(":"):
            alignments.append("CENTER")
        elif compact.endswith(":"):
            alignments.append("RIGHT")
        else:
            alignments.append("LEFT")
    return alignments


def is_table_start(header_line: str, separator_line: str) -> bool:
    alignments = parse_table_separator(separator_line)
    if alignments is None:
        return False

    header_cells = split_table_row(header_line)
    if len(header_cells) != len(alignments):
        return False

    # Evita interpretar "texto" seguido de "---" como tabela de uma coluna.
    if len(header_cells) == 1 and not (
        _contains_table_pipe(header_line) or _contains_table_pipe(separator_line)
    ):
        return False
    return True


def _visible_cell_length(text: str) -> int:
    """Estimativa simples para distribuir a largura das colunas."""
    plain = re.sub(r"`+", "", text)
    plain = plain.replace("**", "").replace("*", "")
    lines = plain.splitlines() or [plain]
    return max(1, min(80, max(len(part) for part in lines)))


def calculate_column_widths(rows: Iterable[list[str]], column_count: int) -> list[float]:
    """Distribui a largura disponível sem permitir estouro horizontal."""
    weights = [4.0] * column_count
    for row in rows:
        for index, cell in enumerate(row[:column_count]):
            weights[index] = max(weights[index], float(_visible_cell_length(cell)))

    # Limita a influência de células enormes para que uma coluna não consuma tudo.
    weights = [min(weight, 48.0) for weight in weights]
    total = sum(weights) or float(column_count)
    widths = [AVAILABLE_TABLE_WIDTH * weight / total for weight in weights]

    # Para poucas colunas, aplica um piso legível e redistribui o restante.
    if column_count <= 8:
        minimum = 15 * mm
        fixed = [width < minimum for width in widths]
        required = sum(minimum for is_fixed in fixed if is_fixed)
        if required < AVAILABLE_TABLE_WIDTH:
            flexible_weight = sum(
                weight for weight, is_fixed in zip(weights, fixed) if not is_fixed
            )
            remaining = AVAILABLE_TABLE_WIDTH - required
            widths = [
                minimum
                if is_fixed
                else remaining * weight / flexible_weight
                for width, weight, is_fixed in zip(widths, weights, fixed)
            ]

    correction = AVAILABLE_TABLE_WIDTH - sum(widths)
    widths[-1] += correction
    return widths


def build_table_flowable(
    header: list[str],
    body_rows: list[list[str]],
    alignments: list[str],
    styles: dict[str, ParagraphStyle],
    theme: PdfTheme,
) -> LongTable:
    column_count = len(header)
    all_raw_rows = [header, *body_rows]
    col_widths = calculate_column_widths(all_raw_rows, column_count)

    alignment_values = {
        "LEFT": TA_LEFT,
        "CENTER": TA_CENTER,
        "RIGHT": TA_RIGHT,
    }
    header_styles = [
        ParagraphStyle(
            f"SafeTableHeaderColumn{index}",
            parent=styles["table_header"],
            alignment=alignment_values[alignment],
        )
        for index, alignment in enumerate(alignments)
    ]
    cell_styles = [
        ParagraphStyle(
            f"SafeTableCellColumn{index}",
            parent=styles["table_cell"],
            alignment=alignment_values[alignment],
        )
        for index, alignment in enumerate(alignments)
    ]

    table_data = [
        [
            Paragraph(safe_inline(cell), header_styles[index])
            for index, cell in enumerate(header)
        ]
    ]
    for row in body_rows:
        table_data.append(
            [
                Paragraph(safe_inline(cell), cell_styles[index])
                for index, cell in enumerate(row)
            ]
        )

    commands: list[tuple] = [
        ("BACKGROUND", (0, 0), (-1, 0), theme.table_header_background),
        ("TEXTCOLOR", (0, 0), (-1, 0), theme.table_header_text),
        ("LINEBELOW", (0, 0), (-1, 0), 1.2, theme.table_accent),
        ("GRID", (0, 0), (-1, -1), 0.45, theme.table_grid),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]

    if body_rows:
        commands.append(
            (
                "ROWBACKGROUNDS",
                (0, 1),
                (-1, -1),
                [theme.table_cell_background, theme.table_alternate_background],
            )
        )

    for column_index, alignment in enumerate(alignments):
        commands.append(
            ("ALIGN", (column_index, 0), (column_index, -1), alignment)
        )

    table = LongTable(
        table_data,
        colWidths=col_widths,
        repeatRows=1,
        hAlign="LEFT",
        splitByRow=1,
        splitInRow=1,
        spaceBefore=4 * mm,
        spaceAfter=5 * mm,
    )
    table.setStyle(TableStyle(commands))
    return table


def read_table(
    lines: list[str],
    start_index: int,
    styles: dict[str, ParagraphStyle],
    theme: PdfTheme,
    line_progress: Callable[[int], None] | None = None,
) -> tuple[LongTable, int]:
    """Lê uma tabela iniciada em ``start_index``.

    Retorna o flowable e o índice da próxima linha ainda não consumida.
    """
    header = split_table_row(lines[start_index])
    alignments = parse_table_separator(lines[start_index + 1])
    if alignments is None or len(header) != len(alignments):
        raise MarkdownTableError(
            f"Tabela inválida próxima da linha {start_index + 1}."
        )

    column_count = len(header)
    if column_count > MAX_TABLE_COLUMNS:
        raise MarkdownTableError(
            f"Tabela na linha {start_index + 1} tem {column_count} colunas; "
            f"limite: {MAX_TABLE_COLUMNS}."
        )

    body_rows: list[list[str]] = []
    index = start_index + 2

    while index < len(lines):
        if line_progress is not None:
            line_progress(index)
        line = lines[index]
        if not line.strip():
            break

        # Exigimos ao menos um pipe delimitador em cada linha do corpo.
        # Isso impede que uma tabela de uma coluna absorva parágrafos seguintes.
        if not _contains_table_pipe(line):
            break

        row = split_table_row(line)
        if len(row) > column_count:
            raise MarkdownTableError(
                f"Linha {index + 1} tem {len(row)} células, mas o cabeçalho "
                f"define {column_count}. Escape pipes literais como \\|."
            )
        if len(row) < column_count:
            row.extend([""] * (column_count - len(row)))

        if any(len(cell) > MAX_TABLE_CELL_CHARS for cell in row):
            raise MarkdownTableError(
                f"Uma célula da linha {index + 1} excedeu "
                f"{MAX_TABLE_CELL_CHARS} caracteres."
            )

        body_rows.append(row)
        if len(body_rows) > MAX_TABLE_ROWS:
            raise MarkdownTableError(
                f"Tabela na linha {start_index + 1} excedeu "
                f"{MAX_TABLE_ROWS} linhas."
            )
        if (len(body_rows) + 1) * column_count > MAX_TABLE_CELLS:
            raise MarkdownTableError(
                f"Tabela na linha {start_index + 1} excedeu "
                f"{MAX_TABLE_CELLS} células."
            )
        index += 1
        if line_progress is not None:
            line_progress(index)

    return build_table_flowable(header, body_rows, alignments, styles, theme), index


def markdown_to_story(
    markdown: str,
    theme: PdfTheme,
    progress: ProgressBar | None = None,
    *,
    mermaid_mode: str = "auto",
):
    styles = make_styles(theme)
    story = []
    heading_counts: dict[str, int] = defaultdict(int)
    paragraph_lines: list[str] = []
    code_lines: list[str] = []
    fence_char: str | None = None
    fence_len = 0
    fence_language = ""
    lines = markdown.splitlines()
    index = 0
    total_lines = max(1, len(lines))

    def report_line(position: int) -> None:
        if progress is not None:
            progress.update(5.0 + 35.0 * min(position, total_lines) / total_lines, "Analisando Markdown")

    def flush_paragraph() -> None:
        nonlocal paragraph_lines
        if paragraph_lines:
            text = " ".join(part.strip() for part in paragraph_lines).strip()
            if text:
                story.append(Paragraph(safe_inline(text), styles["body"]))
            paragraph_lines = []

    def flush_code() -> None:
        nonlocal code_lines, fence_language
        code = "\n".join(code_lines)
        if fence_language == "mermaid":
            try:
                story.append(build_mermaid_flowable(code, theme, styles, mode=mermaid_mode))
            except MermaidSyntaxError as exc:
                warning = (
                    "Bloco Mermaid preservado como código: "
                    + html.escape(str(exc), quote=True)
                )
                story.append(Paragraph(warning, styles["warning"]))
                story.append(build_code_flowable(code, styles, theme, language=fence_language))
        else:
            story.append(build_code_flowable(code, styles, theme, language=fence_language))
        code_lines = []
        fence_language = ""

    while index < len(lines):
        report_line(index)
        line = lines[index]

        if fence_char is not None:
            stripped = line.lstrip()
            closing = stripped.startswith(fence_char * fence_len)
            if closing:
                flush_code()
                fence_char = None
                fence_len = 0
            else:
                code_lines.append(line)
            index += 1
            continue

        fence_match = FENCE_RE.match(line)
        if fence_match:
            flush_paragraph()
            marker = fence_match.group(1)
            fence_char = marker[0]
            fence_len = len(marker)
            fence_language = (fence_match.group(2) or "").lower()
            index += 1
            continue

        if not line.strip():
            flush_paragraph()
            index += 1
            continue

        if index + 1 < len(lines) and is_table_start(line, lines[index + 1]):
            flush_paragraph()
            table, next_index = read_table(
                lines, index, styles, theme, line_progress=report_line
            )
            story.append(table)
            index = next_index
            continue

        heading_match = HEADING_RE.match(line)
        if heading_match:
            flush_paragraph()
            level = len(heading_match.group(1))
            heading_text = heading_match.group(2)
            base_anchor = _anchor_slug(heading_text)
            heading_counts[base_anchor] += 1
            anchor = (
                base_anchor
                if heading_counts[base_anchor] == 1
                else f"{base_anchor}-{heading_counts[base_anchor]}"
            )
            story.append(
                Paragraph(
                    f'<a name="{anchor}"/>{safe_inline(heading_text)}',
                    styles[f"h{level}"],
                )
            )
            index += 1
            continue

        if HR_RE.match(line):
            flush_paragraph()
            story.append(Spacer(1, 3 * mm))
            story.append(
                HRFlowable(width="100%", thickness=0.6, color=theme.horizontal_rule)
            )
            story.append(Spacer(1, 3 * mm))
            index += 1
            continue

        bullet_match = BULLET_RE.match(line)
        if bullet_match:
            flush_paragraph()
            story.append(
                Paragraph(
                    safe_inline(bullet_match.group(1)),
                    styles["bullet"],
                    bulletText="-",
                )
            )
            index += 1
            continue

        numbered_match = NUMBERED_RE.match(line)
        if numbered_match:
            flush_paragraph()
            number = numbered_match.group(1)
            item = numbered_match.group(2)
            story.append(
                Paragraph(
                    safe_inline(item),
                    styles["bullet"],
                    bulletText=f"{number}.",
                )
            )
            index += 1
            continue

        if line.lstrip().startswith(">"):
            flush_paragraph()
            quote_lines: list[str] = []
            while index < len(lines) and lines[index].lstrip().startswith(">"):
                quote_lines.append(lines[index].lstrip()[1:].lstrip())
                report_line(index)
                index += 1
            quote = " ".join(part for part in quote_lines if part).strip()
            story.append(build_quote_flowable(quote or " ", styles, theme))
            continue

        paragraph_lines.append(line)
        index += 1

    flush_paragraph()
    if fence_char is not None:
        flush_code()

    if not story:
        story.append(Paragraph("Documento vazio.", styles["body"]))

    report_line(total_lines)
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


def _story_units(story: list) -> int:
    total = 0
    for flowable in story:
        if isinstance(flowable, LongTable):
            rows = getattr(flowable, "_cellvalues", None)
            total += max(1, len(rows) if rows is not None else 1)
        elif isinstance(flowable, MermaidFlowchart):
            total += max(1, flowable.node_count)
        elif isinstance(flowable, Preformatted):
            text = getattr(flowable, "text", "")
            total += max(1, str(text).count("\n") + 1)
        else:
            total += 1
    return max(1, total)


def _paint_page(theme: PdfTheme):
    """Preenche a página com um único fundo uniforme.

    Não cria cabeçalho, rodapé, numeração, título repetido nem um grande
    painel interno. As superfícies adicionais pertencem exclusivamente aos
    componentes (tabelas, citações, código, Mermaid e avisos).
    """

    def paint(canvas, document) -> None:
        page_width, page_height = document.pagesize
        canvas.saveState()
        canvas.setFillColor(theme.page_background)
        canvas.rect(0, 0, page_width, page_height, stroke=0, fill=1)
        canvas.restoreState()

    return paint

def build_pdf(
    markdown: str,
    output_path: Path,
    *,
    force: bool = False,
    theme: PdfTheme = BB_LIGHT_DARK_THEME,
    progress: ProgressBar | None = None,
    mermaid_mode: str = "auto",
) -> None:
    progress = progress or ProgressBar(enabled=False)
    progress.update(2, "Validando arquivo de saída")

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
        story = markdown_to_story(markdown, theme, progress, mermaid_mode=mermaid_mode)
        progress.update(41, "Preparando o documento")
        total_units = _story_units(story)
        estimated_pages = max(1, round(total_units / 34))

        document = ProgressDocTemplate(
            str(temporary),
            progress=progress,
            total_units=total_units,
            estimated_pages=estimated_pages,
            pagesize=A4,
            rightMargin=PAGE_RIGHT_MARGIN,
            leftMargin=PAGE_LEFT_MARGIN,
            topMargin=PAGE_TOP_MARGIN,
            bottomMargin=PAGE_BOTTOM_MARGIN,
            title=output.stem,
            author=SCRIPT_NAME,
            pageCompression=1,
        )
        paint_page = _paint_page(theme)
        document.build(story, onFirstPage=paint_page, onLaterPages=paint_page)

        progress.update(97, "Validando o PDF gerado")
        if temporary.stat().st_size == 0:
            raise RuntimeError("O PDF temporário foi criado vazio.")

        progress.update(99, "Gravando o arquivo final")
        os.replace(temporary, output)
        progress.finish("PDF criado")
    finally:
        temporary.unlink(missing_ok=True)


HELP_EPILOG = r"""
Use "python md2pdf_v7.py -help" para ver o manual completo, os cinco temas, os dois modos de saída e exemplos para Windows.
"""


def make_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="python md2pdf_v7.py -use",
        add_help=False,
        description=(
            "Converte um subconjunto seguro de Markdown para PDF, "
            "incluindo links internos, tabelas Markdown e Mermaid com Auto Layout seguro."
        ),
        epilog=HELP_EPILOG,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("-h", "--help", "-help", action="help", help="Mostra a ajuda.")
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {SCRIPT_VERSION} (links internos, tabelas, blocos sem corte, Mermaid Auto Layout, 5 temas e fundo uniforme: habilitados)",
    )
    parser.set_defaults(theme_name=DEFAULT_THEME_NAME)
    theme_group = parser.add_mutually_exclusive_group()
    theme_group.add_argument(
        "-l",
        "--light",
        dest="theme_name",
        action="store_const",
        const="light",
        help="Tema claro genérico, mantido por compatibilidade.",
    )
    theme_group.add_argument(
        "-d",
        "--dark",
        dest="theme_name",
        action="store_const",
        const="dark",
        help="Tema escuro genérico, mantido por compatibilidade.",
    )
    theme_group.add_argument(
        "--bb-light",
        dest="theme_name",
        action="store_const",
        const="bb-light",
        help="Tema BB claro para leitura longa, impressão e documentação.",
    )
    theme_group.add_argument(
        "--bb-light-dark",
        dest="theme_name",
        action="store_const",
        const="bb-light-dark",
        help="Tema BB equilibrado e tecnológico; padrão recomendado.",
    )
    theme_group.add_argument(
        "--bb-dark",
        dest="theme_name",
        action="store_const",
        const="bb-dark",
        help="Tema BB escuro, executivo e de alto impacto.",
    )
    theme_group.add_argument(
        "-t",
        "--theme",
        dest="theme_name",
        choices=tuple(THEMES),
        help="Seleciona o tema pelo nome.",
    )
    parser.set_defaults(mermaid_mode="auto")
    mermaid_group = parser.add_mutually_exclusive_group()
    mermaid_group.add_argument(
        "--mermaid-auto",
        dest="mermaid_mode",
        action="store_const",
        const="auto",
        help="Escolhe automaticamente direção, densidade, ordem e paginação do Mermaid (padrão).",
    )
    mermaid_group.add_argument(
        "--mermaid-strict",
        dest="mermaid_mode",
        action="store_const",
        const="strict",
        help="Prioriza a direção e a ordem declaradas no bloco Mermaid.",
    )
    parser.add_argument(
        "--no-progress",
        action="store_true",
        help="Oculta a barra de progresso da conversão.",
    )
    parser.add_argument("entrada", type=Path, help="Arquivo Markdown UTF-8 de entrada")
    parser.add_argument(
        "saida",
        type=Path,
        nargs="?",
        help=(
            "Arquivo PDF de saída. Se omitido, usa o nome da entrada e "
            "substitui automaticamente um PDF existente."
        ),
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Permite substituir um PDF existente.",
    )
    return parser


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = make_argument_parser()
    return parser.parse_args(_EFFECTIVE_ARGUMENTS if argv is None else argv)


def _preflight_conversion(
    args: argparse.Namespace,
) -> tuple[Path, Path, str, bool, bool]:
    input_path = args.entrada.expanduser()
    automatic_output = args.saida is None
    output_path = input_path.with_suffix(".pdf") if automatic_output else args.saida.expanduser()
    effective_force = True if automatic_output else args.force

    if input_path.suffix.lower() not in {".md", ".markdown"}:
        raise ValueError("A entrada deve terminar em .md ou .markdown.")
    if output_path.suffix.lower() != ".pdf":
        raise ValueError("O arquivo de saída deve terminar em .pdf.")

    input_resolved = input_path.resolve(strict=True)
    output_parent = output_path.parent.resolve(strict=True)
    output_resolved = output_parent / output_path.name

    if input_resolved == output_resolved:
        raise ValueError("Entrada e saída não podem apontar para o mesmo arquivo.")
    if output_resolved.exists() and output_resolved.is_symlink():
        raise ValueError("Por segurança, a saída não pode ser um link simbólico.")
    if output_resolved.exists() and not effective_force:
        raise FileExistsError(
            f"A saída já existe: {output_resolved}. Use --force para substituir."
        )

    writable, detail = _check_directory_writable(output_parent)
    if not writable:
        raise ValueError(f"A pasta de saída não permite gravação: {detail}")

    free_bytes = shutil.disk_usage(output_parent).free
    required_bytes = max(10 * 1024 * 1024, input_resolved.stat().st_size * 5)
    if free_bytes < required_bytes:
        raise ValueError(
            f"Espaço insuficiente na saída: {free_bytes} bytes livres; "
            f"mínimo estimado: {required_bytes} bytes."
        )

    if USE_MODE:
        try:
            import reportlab
            reportlab_version = getattr(reportlab, "__version__", "desconhecida")
        except ImportError:
            reportlab_version = "indisponível"
        print("\nChecagens da conversão:")
        _print_check(True, f"Python: {sys.executable}")
        _print_check(True, f"ReportLab: {reportlab_version}")
        _print_check(True, f"entrada: {input_resolved}")
        _print_check(True, f"saída: {output_resolved}")
        if automatic_output:
            _print_check(True, "modo de saída: automático (force automático ativado)")
        else:
            _print_check(
                True,
                "modo de saída: explícito "
                f"({'force ativado' if effective_force else 'sem force'})",
            )
        _print_check(True, f"tema solicitado: {args.theme_name}")
        _print_check(True, f"layout Mermaid: {args.mermaid_mode}")
        _print_check(True, f"espaço livre: {free_bytes / (1024 * 1024):.0f} MB")
        print("[OK] Todas as checagens passaram. Iniciando a transformação.\n")

    markdown = validate_input(input_resolved)
    return input_resolved, output_resolved, markdown, effective_force, automatic_output


def main() -> int:
    args = parse_args()
    progress: ProgressBar | None = None

    try:
        _, output_path, markdown, effective_force, automatic_output = _preflight_conversion(args)
        theme = THEMES.get(args.theme_name)
        if theme is None:
            raise ValueError(f"Tema desconhecido: {args.theme_name!r}.")
        progress = ProgressBar(enabled=not args.no_progress)
        progress.update(0, f"Iniciando conversão - tema {theme.name}")
        build_pdf(
            markdown,
            output_path,
            force=effective_force,
            theme=theme,
            progress=progress,
            mermaid_mode=args.mermaid_mode,
        )
        mode_text = "saída automática" if automatic_output else "saída explícita"
        print(
            f"PDF criado com sucesso: {output_path} "
            f"(tema: {theme.name}; Mermaid: {args.mermaid_mode}; {mode_text})"
        )
        return 0
    except KeyboardInterrupt:
        if progress is not None:
            progress.stop()
        print("Conversão cancelada pelo usuário.", file=sys.stderr)
        return 130
    except (OSError, UnicodeError, ValueError, RuntimeError) as exc:
        if progress is not None:
            progress.stop()
        print(f"Erro: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
