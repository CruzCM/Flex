"""Experiencia guiada do notebook."""

from __future__ import annotations

import html
import importlib
import importlib.util
import json
import re
import sys
import textwrap
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Optional


DEPENDENCIAS_BASE = {"yaml": "PyYAML"}
DEPENDENCIAS_OFICIAIS = {
    "dotenv": "python-dotenv",
    "requests": "requests",
    "urllib3": "urllib3",
}
DEPENDENCIAS_OLLAMA = {"requests": "requests"}


try:
    from IPython.display import HTML, Markdown, display
    from IPython import get_ipython
except Exception:
    HTML = None
    Markdown = None
    display = None
    get_ipython = None


@dataclass
class StatusAmbiente:
    raiz: Path
    python: str
    provedor: str
    dependencias_ausentes: list[str] = field(default_factory=list)


def raiz_projeto(inicio: Optional[Path] = None) -> Path:
    atual = Path(inicio or Path.cwd()).resolve()

    for pasta in [atual] + list(atual.parents):
        if (
            (pasta / "produtos").exists()
            and (pasta / "publicos").exists()
            and (pasta / "prompts").exists()
        ):
            return pasta

    raise RuntimeError("Nao foi possivel localizar a raiz do projeto.")


def dependencias_ausentes(dependencias: dict[str, str]) -> list[str]:
    ausentes = []

    for modulo, pacote in dependencias.items():
        if importlib.util.find_spec(modulo) is None:
            ausentes.append(pacote)

    return sorted(set(ausentes))


def normalizar_provedor(provedor: Optional[str]) -> Optional[str]:
    if provedor is None:
        return None

    valor = str(provedor).strip().lower()

    if valor == "ollama":
        return "ollama"

    raise ValueError(
        "Provedor invalido: "
        + str(provedor)
        + "\n\nValores aceitos:\n"
        + "- nenhum argumento, para usar o Genera oficial;\n"
        + '- "ollama", para usar o testador local.'
    )


def preparar_ambiente(provedor: Optional[str]) -> StatusAmbiente:
    raiz = raiz_projeto()

    if str(raiz) not in sys.path:
        sys.path.insert(0, str(raiz))

    dependencias = dict(DEPENDENCIAS_BASE)
    nome_provedor = "Genera oficial"

    if provedor == "ollama":
        dependencias.update(DEPENDENCIAS_OLLAMA)
        nome_provedor = "Ollama local"
    else:
        dependencias.update(DEPENDENCIAS_OFICIAIS)

    return StatusAmbiente(
        raiz=raiz,
        python=".".join(str(parte) for parte in sys.version_info[:3]),
        provedor=nome_provedor,
        dependencias_ausentes=dependencias_ausentes(dependencias),
    )


def resolver_criador_provedor(provedor: Optional[str]) -> Any:
    if provedor is None:
        from .modelos import Genera

        return Genera

    if provedor == "ollama":
        try:
            modulo = importlib.import_module("src.ollama_local")
        except ModuleNotFoundError as erro:
            if erro.name == "src.ollama_local":
                raise RuntimeError(
                    "O testador local Ollama nao esta disponivel.\n\n"
                    "Arquivo esperado:\n"
                    "src/ollama_local.py\n\n"
                    "O fluxo oficial continua disponivel por meio de fluxo_geracao()."
                )
            raise

        if not hasattr(modulo, "ollama"):
            raise RuntimeError(
                "O arquivo src/ollama_local.py deve exportar um objeto chamado ollama."
            )

        if hasattr(modulo, "verificar_disponivel"):
            modulo.verificar_disponivel()

        return getattr(modulo, "ollama")

    raise ValueError("Provedor invalido.")


def em_notebook() -> bool:
    if display is None or get_ipython is None:
        return False

    shell = get_ipython()
    return shell is not None and shell.__class__.__name__ == "ZMQInteractiveShell"


def texto_curto(texto: Any, largura: int = 88) -> str:
    linhas = []

    for linha in str(texto or "").splitlines():
        valor = " ".join(linha.strip().split())

        if not valor:
            linhas.append("")
            continue

        indentacao = ""
        marcador = re.match(r"^(\s*(?:[-*]|\d+[.])\s+)", linha)
        if marcador:
            indentacao = " " * len(marcador.group(1))

        linhas.append(
            textwrap.fill(
                valor,
                width=largura,
                subsequent_indent=indentacao,
            )
        )

    return "\n".join(linhas).strip()


class Visual:
    def aplicar_estilo(self) -> None:
        if not em_notebook() or HTML is None:
            return

        display(
            HTML(
                """
                <style>
                .pc-wrap {
                    max-width: 980px;
                    font-family: Arial, sans-serif;
                    color: #1f2933;
                }
                .pc-hero {
                    border-left: 6px solid #f3c300;
                    padding: 14px 18px;
                    background: #f7f9fc;
                    margin: 8px 0 18px;
                }
                .pc-section {
                    margin: 18px 0 8px;
                    padding-bottom: 4px;
                    border-bottom: 1px solid #d8dee9;
                    font-size: 20px;
                    font-weight: 700;
                }
                .pc-card {
                    border: 1px solid #d8dee9;
                    border-radius: 8px;
                    margin: 32px 0;
                    background: #ffffff;
                    box-shadow: 0 1px 2px rgba(16, 42, 67, .06);
                }
                .pc-card-title {
                    padding: 16px 18px 6px;
                    font-size: 20px;
                    font-weight: 800;
                    line-height: 1.3;
                    color: #102a43;
                }
                .pc-card-body {
                    padding: 0 18px 18px;
                }
                .pc-card-highlight {
                    border: 2px solid #f3c300;
                    background: #fffdf2;
                }
                .pc-field {
                    margin: 16px 0 0;
                }
                .pc-field:first-child {
                    margin-top: 8px;
                }
                .pc-lead {
                    font-size: 17px;
                    font-weight: 800;
                    line-height: 1.45;
                    color: #102a43;
                    margin: 8px 0 16px;
                }
                .pc-label {
                    font-size: 12px;
                    font-weight: 700;
                    letter-spacing: 0;
                    text-transform: uppercase;
                    color: #52606d;
                    margin-bottom: 6px;
                }
                .pc-value {
                    white-space: pre-wrap;
                    line-height: 1.55;
                    max-width: 88ch;
                }
                .pc-muted {
                    color: #52606d;
                    font-size: 13px;
                }
                .pc-inner {
                    border-top: 1px solid #e4e7eb;
                    padding: 16px 0 0;
                    margin: 18px 0 0;
                }
                .pc-inner > summary,
                .pc-technical > summary {
                    cursor: pointer;
                    font-weight: 700;
                    list-style: none;
                    color: #102a43;
                }
                .pc-inner > summary::-webkit-details-marker,
                .pc-technical > summary::-webkit-details-marker {
                    display: none;
                }
                .pc-inner > summary:before,
                .pc-technical > summary:before {
                    content: "+";
                    display: inline-block;
                    width: 18px;
                    color: #52606d;
                }
                .pc-inner[open] > summary:before,
                .pc-technical[open] > summary:before {
                    content: "-";
                }
                .pc-technical {
                    border-top: 1px solid #d8dee9;
                    margin: 22px 0 0;
                    padding: 16px 0 0;
                }
                .pc-technical .pc-hide {
                    display: none;
                }
                .pc-technical[open] .pc-show {
                    display: none;
                }
                .pc-technical[open] .pc-hide {
                    display: inline;
                }
                .pc-subsection {
                    border-top: 1px solid #e4e7eb;
                    margin-top: 18px;
                    padding-top: 18px;
                }
                .pc-subsection:first-child {
                    border-top: 0;
                    margin-top: 8px;
                    padding-top: 0;
                }
                .pc-subtitle {
                    font-size: 16px;
                    font-weight: 800;
                    color: #102a43;
                    margin: 0 0 10px;
                }
                .pc-stage {
                    border-left: 3px solid #d8dee9;
                    padding-left: 12px;
                    margin: 14px 0;
                }
                .pc-stage-title {
                    font-weight: 700;
                    margin-bottom: 8px;
                }
                .pc-output-list {
                    padding-top: 2px;
                }
                .pc-output-item {
                    border-top: 1px solid #e4e7eb;
                    padding: 18px 0 20px;
                    margin: 0;
                }
                .pc-output-item:first-child {
                    border-top: 0;
                    padding-top: 8px;
                }
                .pc-output-title {
                    font-size: 18px;
                    font-weight: 800;
                    line-height: 1.3;
                    color: #102a43;
                    margin: 0 0 12px;
                }
                .pc-output-text {
                    white-space: pre-wrap;
                    line-height: 1.55;
                    font-size: 15px;
                    color: #1f2933;
                    max-width: 88ch;
                }
                .pc-output-main .pc-output-title {
                    font-size: 20px;
                    margin-bottom: 14px;
                }
                .pc-output-main .pc-output-text {
                    font-size: 16px;
                }
                .pc-output-compact {
                    background: #f7f9fc;
                    border: 1px solid #d8dee9;
                    border-radius: 8px;
                    padding: 12px 14px;
                    margin: 12px 0;
                }
                .pc-output-compact .pc-output-title {
                    font-size: 14px;
                    margin-bottom: 6px;
                }
                .pc-pipeline {
                    display: grid;
                    gap: 7px;
                    margin-top: 6px;
                    max-width: 48ch;
                }
                .pc-pipeline-step {
                    display: grid;
                    grid-template-columns: 22px 1fr;
                    align-items: start;
                    line-height: 1.45;
                }
                .pc-pipeline-marker {
                    color: #52606d;
                }
                .pc-json {
                    max-width: 100%;
                    overflow: auto;
                    white-space: pre-wrap;
                    background: #111827;
                    color: #f9fafb;
                    padding: 12px;
                    border-radius: 8px;
                    line-height: 1.45;
                }
                code {
                    background: #eef2f7;
                    border-radius: 4px;
                    padding: 1px 4px;
                    font-family: Consolas, Monaco, monospace;
                    font-size: .95em;
                }
                .pc-progress {
                    border: 1px solid #d8dee9;
                    border-radius: 8px;
                    margin: 10px 0;
                    padding: 14px 16px;
                    background: #ffffff;
                }
                .pc-progress-title {
                    font-weight: 700;
                    margin-bottom: 4px;
                }
                .pc-progress-status {
                    color: #52606d;
                    font-size: 13px;
                    margin-bottom: 10px;
                    line-height: 1.45;
                }
                .pc-progress-track {
                    height: 10px;
                    border-radius: 999px;
                    background: #e4e7eb;
                    overflow: hidden;
                }
                .pc-progress-fill {
                    height: 100%;
                    border-radius: 999px;
                    background: #f3c300;
                    transition: width .25s ease;
                }
                .pc-progress-count {
                    color: #52606d;
                    font-size: 12px;
                    margin-top: 8px;
                }
                </style>
                """
            )
        )

    def titulo(self, texto: str, apoio: Optional[str] = None) -> None:
        if em_notebook() and HTML is not None:
            apoio_html = (
                f"<div class='pc-muted'>{html.escape(apoio)}</div>" if apoio else ""
            )
            display(
                HTML(
                    "<div class='pc-wrap pc-hero'>"
                    f"<h1 style='margin:0 0 6px'>{html.escape(texto)}</h1>"
                    f"{apoio_html}"
                    "</div>"
                )
            )
            return

        print("\n" + "=" * 80)
        print(texto.upper())
        if apoio:
            print(apoio)
        print("=" * 80)

    def secao(self, texto: str) -> None:
        if em_notebook() and HTML is not None:
            display(HTML(f"<div class='pc-wrap pc-section'>{html.escape(texto)}</div>"))
            return

        print("\n" + texto.upper())
        print("-" * len(texto))

    def _lista_campos(
        self,
        campos: Optional[Any],
    ) -> list[tuple[Optional[str], Any]]:
        if not campos:
            return []
        if isinstance(campos, dict):
            return list(campos.items())
        return list(campos)

    def _valor_html(self, valor: Any) -> str:
        conteudo = html.escape(str(valor or ""))

        def codigo(encontrado: re.Match[str]) -> str:
            return f"<code>{encontrado.group(1)}</code>"

        return re.sub(r"`([^`]+)`", codigo, conteudo)

    def _html_campos(self, campos: Optional[Any]) -> str:
        partes = []

        for chave, valor in self._lista_campos(campos):
            if chave in {None, ""}:
                partes.append(
                    "<div class='pc-lead'>"
                    + self._valor_html(valor)
                    + "</div>"
                )
                continue

            partes.append(
                "<div class='pc-field'>"
                f"<div class='pc-label'>{html.escape(str(chave))}</div>"
                f"<div class='pc-value'>{self._valor_html(valor)}</div>"
                "</div>"
            )

        return "".join(partes)

    def _html_secao(self, titulo: str, conteudo: Any, *, compacto: bool = False) -> str:
        if compacto:
            return self.saida_item(titulo, conteudo, compacto=True)

        return (
            "<div class='pc-subsection'>"
            f"<div class='pc-subtitle'>{html.escape(str(titulo))}</div>"
            f"<div class='pc-value'>{self._valor_html(conteudo)}</div>"
            "</div>"
        )

    def html_card(
        self,
        titulo: str,
        campos: Optional[Any] = None,
        *,
        destaque: bool = False,
    ) -> str:
        classe = "pc-wrap pc-card"
        if destaque:
            classe += " pc-card-highlight"

        return (
            f"<div class='{classe}'>"
            f"<div class='pc-card-title'>{html.escape(str(titulo))}</div>"
            "<div class='pc-card-body'>"
            + self._html_campos(campos)
            + "</div></div>"
        )

    def card(
        self,
        titulo: str,
        campos: Optional[Any] = None,
        *,
        aberto: bool = True,
        destaque: bool = False,
    ) -> None:
        if em_notebook() and HTML is not None:
            display(HTML(self.html_card(titulo, campos, destaque=destaque)))
            return

        self._imprimir_card(titulo, campos, destaque=destaque)

    def _imprimir_card(
        self,
        titulo: str,
        campos: Optional[Any] = None,
        *,
        destaque: bool = False,
    ) -> None:
        marcador = "=" if destaque else "-"
        print("\n" + marcador * 80)
        print(str(titulo).upper())
        print(marcador * 80)

        for chave, valor in self._lista_campos(campos):
            if chave in {None, ""}:
                print("\n" + texto_curto(valor))
                continue

            print(f"\n{chave}")
            print()
            print(texto_curto(valor))

    def _secoes_ordenadas(self, secoes: Optional[Any]) -> list[dict[str, Any]]:
        itens = []
        for secao in secoes or []:
            if isinstance(secao, dict):
                itens.append(dict(secao))
            else:
                titulo, conteudo = secao
                itens.append({"titulo": titulo, "conteudo": conteudo})
        return itens

    def texto_json(self, dados: Any) -> str:
        return json.dumps(dados, indent=2, ensure_ascii=False, default=str)

    def json_bloco(self, dados: Any) -> str:
        return (
            "<pre class='pc-json'>"
            + html.escape(self.texto_json(dados))
            + "</pre>"
        )

    def _detalhes_ordenados(self, conteudo: Optional[Any]) -> list[dict[str, Any]]:
        secoes = self._secoes_ordenadas(conteudo)
        payloads = [
            secao
            for secao in secoes
            if str(secao.get("titulo", "")).strip().lower() == "payload llm"
        ]
        outros = [secao for secao in secoes if secao not in payloads]
        return outros + payloads

    def detalhes_tecnicos(self, conteudo: Optional[Any]) -> str:
        secoes = self._detalhes_ordenados(conteudo)
        if not secoes:
            return ""

        partes = []
        for secao in secoes:
            titulo = str(secao.get("titulo", ""))
            valor = secao.get("conteudo", "")
            if titulo == "Payload LLM":
                corpo = self.json_bloco(valor)
                partes.append(
                    "<div class='pc-subsection'>"
                    f"<div class='pc-subtitle'>{html.escape(titulo)}</div>"
                    + corpo
                    + "</div>"
                )
                continue

            partes.append(self._html_secao(titulo, valor))

        return (
            "<details class='pc-technical'>"
            "<summary>"
            "<span class='pc-show'>Ver detalhes técnicos</span>"
            "<span class='pc-hide'>Ocultar detalhes técnicos</span>"
            "</summary>"
            + "".join(partes)
            + "</details>"
        )

    def html_card_com_secoes(
        self,
        titulo: str,
        campos_topo: Optional[Any] = None,
        secoes: Optional[Any] = None,
        detalhes_tecnicos: Optional[Any] = None,
        *,
        destaque: bool = False,
    ) -> str:
        classe = "pc-wrap pc-card"
        if destaque:
            classe += " pc-card-highlight"

        partes = [self._html_campos(campos_topo)]

        for secao in self._secoes_ordenadas(secoes):
            partes.append(
                self._html_secao(
                    str(secao.get("titulo", "")),
                    secao.get("conteudo", ""),
                    compacto=bool(secao.get("compacto")),
                )
            )

        partes.append(self.detalhes_tecnicos(detalhes_tecnicos))

        return (
            f"<div class='{classe}'>"
            f"<div class='pc-card-title'>{html.escape(str(titulo))}</div>"
            "<div class='pc-card-body'>"
            + "".join(partes)
            + "</div></div>"
        )

    def card_com_secoes(
        self,
        titulo: str,
        campos_topo: Optional[Any] = None,
        secoes: Optional[Any] = None,
        detalhes_tecnicos: Optional[Any] = None,
        *,
        destaque: bool = False,
    ) -> None:
        if em_notebook() and HTML is not None:
            display(
                HTML(
                    self.html_card_com_secoes(
                        titulo,
                        campos_topo,
                        secoes,
                        detalhes_tecnicos,
                        destaque=destaque,
                    )
                )
            )
            return

        self._imprimir_card(titulo, campos_topo, destaque=destaque)
        for secao in self._secoes_ordenadas(secoes):
            print(f"\n{secao.get('titulo', '')}")
            print()
            print(texto_curto(secao.get("conteudo", "")))

        detalhes = self._detalhes_ordenados(detalhes_tecnicos)
        if detalhes:
            print("\nVer detalhes técnicos")
            for secao in detalhes:
                print(f"\n{secao.get('titulo', '')}")
                print()
                valor = secao.get("conteudo", "")
                if secao.get("titulo") == "Payload LLM":
                    print(self.texto_json(valor))
                else:
                    print(texto_curto(valor))

    def ficha(self, titulo: str, dados: dict[str, Any]) -> None:
        self.card(titulo, dados)

    def bloco(self, titulo: str, texto: Any) -> None:
        self.card(titulo, [(None, texto)])

    def bloco_partes(self, titulo: str, partes: list[dict[str, str]]) -> None:
        texto = "".join(str(parte.get("texto", "")) for parte in partes)
        self.card(titulo, [(None, texto)])

    def final(self, dados: dict[str, Any]) -> None:
        self.card("Resultado Final", dados, destaque=True)

    def status(self, valor: Any) -> str:
        texto = " ".join(str(valor or "").strip().lower().split())
        mapa = {
            "pronto": "Pronto",
            "pronta": "Pronto",
            "concluido": "Pronto",
            "concluído": "Pronto",
            "concluida": "Pronto",
            "concluída": "Pronto",
            "tudo pronto": "Pronto",
            "processando": "Processando",
            "gerando": "Processando",
            "pendente": "Pendente",
            "selecionado": "Selecionado",
            "selecionada": "Selecionado",
            "erro": "Erro",
            "nao concluida": "Erro",
            "não concluída": "Erro",
            "nao concluido": "Erro",
            "não concluído": "Erro",
        }
        return mapa.get(texto, str(valor or "").strip() or "Pendente")

    def pipeline(self, titulo: str, etapas: list[str]) -> str:
        if not etapas:
            return ""

        return "\n".join(
            str(etapa) if indice == 0 else "-> " + str(etapa)
            for indice, etapa in enumerate(etapas)
        )

    def saida_item(
        self,
        titulo: str,
        valor: Any,
        *,
        compacto: bool = False,
    ) -> str:
        classe = "pc-output-item"
        if compacto:
            classe += " pc-output-compact"

        return (
            f"<div class='{classe}'>"
            f"<div class='pc-output-title'>{html.escape(str(titulo))}</div>"
            f"<div class='pc-output-text'>{self._valor_html(valor)}</div>"
            "</div>"
        )

    def progresso(
        self,
        titulo: str,
        atual: int,
        total: int,
        status: str,
        *,
        detalhe: str = "",
        handle: Any = None,
    ) -> Any:
        total_seguro = max(int(total or 1), 1)
        atual_seguro = max(0, min(int(atual), total_seguro))
        porcentagem = int((atual_seguro / total_seguro) * 100)

        if em_notebook() and HTML is not None:
            detalhe_html = (
                f"<br>{html.escape(detalhe)}"
                if detalhe
                else ""
            )
            conteudo = HTML(
                "<div class='pc-wrap pc-progress'>"
                f"<div class='pc-progress-title'>{html.escape(titulo)}</div>"
                "<div class='pc-progress-status'>"
                f"{html.escape(status)}{detalhe_html}"
                "</div>"
                "<div class='pc-progress-track'>"
                "<div class='pc-progress-fill' "
                f"style='width:{porcentagem}%'></div>"
                "</div>"
                "<div class='pc-progress-count'>"
                f"{atual_seguro}/{total_seguro} etapas concluídas"
                "</div>"
                "</div>"
            )

            if handle is not None and hasattr(handle, "update"):
                handle.update(conteudo)
                return handle

            return display(conteudo, display_id=True)

        print(f"{titulo}: {atual_seguro}/{total_seguro} - {status}")
        if detalhe:
            print(detalhe)
        return handle

    def limpar(self, handle: Any = None) -> None:
        if em_notebook() and HTML is not None:
            vazio = HTML("<div style='display:none'></div>")

            if handle is not None and hasattr(handle, "update"):
                handle.update(vazio)

    def opcoes(self, opcoes: list[str]) -> None:
        linhas = [
            f"{indice:>2}. {str(opcao).replace('_', ' ')}"
            for indice, opcao in enumerate(opcoes, start=1)
        ]

        if em_notebook() and Markdown is not None:
            display(Markdown("```text\n" + "\n".join(linhas) + "\n```"))
            return

        print("\n".join(linhas))

    def escolher(
        self,
        mensagem: str,
        opcoes: list[str],
        *,
        padrao: Optional[str] = None,
    ) -> str:
        if not opcoes:
            raise ValueError(f"Nenhuma opcao disponivel para: {mensagem}")

        self.opcoes(opcoes)

        indice_padrao = None
        if padrao in opcoes:
            indice_padrao = opcoes.index(padrao) + 1

        while True:
            sufixo = f" [{indice_padrao}]" if indice_padrao else ""
            valor = input(f"{mensagem}{sufixo}: ").strip()

            if not valor and indice_padrao:
                return opcoes[indice_padrao - 1]

            try:
                indice = int(valor)
                if 1 <= indice <= len(opcoes):
                    return opcoes[indice - 1]
            except ValueError:
                if valor in opcoes:
                    return valor

            print("Opcao invalida.")

    def escolher_mapeado(
        self,
        mensagem: str,
        opcoes: list[tuple[str, str]],
        *,
        padrao: Optional[str] = None,
    ) -> str:
        if not opcoes:
            raise ValueError(f"Nenhuma opcao disponivel para: {mensagem}")

        rotulos = [rotulo for rotulo, _ in opcoes]
        valores = [valor for _, valor in opcoes]
        self.opcoes(rotulos)

        indice_padrao = None
        if padrao in valores:
            indice_padrao = valores.index(padrao) + 1

        while True:
            sufixo = f" [{indice_padrao}]" if indice_padrao else ""
            valor_digitado = input(f"{mensagem}{sufixo}: ").strip()

            if not valor_digitado and indice_padrao:
                return valores[indice_padrao - 1]

            try:
                indice = int(valor_digitado)
                if 1 <= indice <= len(opcoes):
                    return valores[indice - 1]
            except ValueError:
                pass

            for rotulo, valor in opcoes:
                if valor_digitado in {rotulo, valor}:
                    return valor

            print("Opcao invalida.")

    def numero(self, mensagem: str, padrao: int) -> int:
        while True:
            valor = input(f"{mensagem} [{padrao}]: ").strip()

            if not valor:
                return padrao

            try:
                numero = int(valor)
                if numero > 0:
                    return numero
            except ValueError:
                pass

            print("Informe um numero inteiro positivo.")

    def decimal(self, mensagem: str, padrao: float) -> float:
        while True:
            valor = input(f"{mensagem} [{padrao}]: ").strip()

            if not valor:
                return padrao

            try:
                numero = float(valor.replace(",", "."))
                if numero >= 0:
                    return numero
            except ValueError:
                pass

            print("Informe um numero decimal maior ou igual a zero.")

    def confirmar(self, mensagem: str, padrao: bool = True) -> bool:
        dica = "S/n" if padrao else "s/N"

        while True:
            valor = input(f"{mensagem} [{dica}]: ").strip().lower()

            if not valor:
                return padrao
            if valor in {"s", "sim", "y", "yes"}:
                return True
            if valor in {"n", "nao", "no"}:
                return False

            print("Responda com sim ou nao.")

    def debug_json(self, titulo: str, dados: dict[str, Any]) -> None:
        conteudo = json.dumps(dados, indent=2, ensure_ascii=False, default=str)

        if em_notebook() and HTML is not None:
            display(
                HTML(
                    "<details class='pc-wrap pc-card'>"
                    f"<summary>{html.escape(titulo)}</summary>"
                    "<div class='pc-card-body'>"
                    "<pre class='pc-value'>"
                    + html.escape(conteudo)
                    + "</pre></div></details>"
                )
            )
            return

        print(f"\n{titulo}")
        print(conteudo)


class Experiencia:
    def __init__(
        self,
        motor: Any,
        status: StatusAmbiente,
        provedor: Optional[str],
    ):
        self.motor = motor
        self.status = status
        self.provedor = provedor
        self.criador_provedor = None
        self.parametros_por_etapa: dict[str, dict[str, Any]] = {}
        self.parametros_automaticos = True
        self.grupo_execucao_atual = ""
        self.fluxo_linear_iniciado = False
        self.loop_iniciado = False
        self.progresso_chamadas: dict[int, Any] = {}
        self.progresso_fluxo_handle = None
        self.progresso_fluxo_tendencia = ""
        self.progresso_fluxo_concluidas: dict[str, Any] = {}
        self.progresso_fluxo_prompts: dict[str, str] = {}
        self.resultado_tendencia_base = None
        self.fluxos_por_tendencia: dict[str, int] = {}
        self.tendencias_exibidas: set[str] = set()
        self.fluxos_exibidos_ao_vivo = 0
        self.fluxos_lineares: dict[str, int] = {}
        self.ui = Visual()

    def rotulo_nome(self, nome: Any) -> str:
        texto = str(nome or "").replace("_", " ").strip()
        if not texto:
            return ""

        palavras_especiais = {
            "aida": "AIDA",
            "bab": "BAB",
            "bb": "BB",
            "cta": "CTA",
            "fab": "FAB",
            "cartao": "Cartão",
            "catalogos": "Catálogos",
            "cenario": "Cenário",
            "familia": "Família",
            "publico": "Público",
            "tendencia": "Tendência",
            "tendencias": "Tendências",
            "transformacao": "Transformação",
        }
        palavras = []

        for palavra in texto.split():
            chave = palavra.lower()
            if chave in palavras_especiais:
                palavras.append(palavras_especiais[chave])
            elif palavra.isupper() and len(palavra) <= 4:
                palavras.append(palavra)
            else:
                palavras.append(palavra[:1].upper() + palavra[1:].lower())

        return " ".join(palavras)

    def rotulo_prompt(self, nome: Any) -> str:
        valor = str(nome or "").strip()
        if "/" in valor:
            valor = valor.rsplit("/", 1)[-1]
        if re.fullmatch(r"p\d+", valor.lower()):
            return valor.upper()
        return self.rotulo_nome(valor)

    def rotulo_etapa(self, etapa_id: str) -> str:
        rotulos = {
            "tendencia_cognitiva": "Tendência",
            "voz_bb": "Voz BB",
            "tagline": "Tagline",
            "headline": "Headline",
            "cta": "CTA",
            "revisor_textual": "Revisão Textual",
            "copywriter": "Copywriter",
        }
        return rotulos.get(etapa_id, self.rotulo_nome(etapa_id))

    def rotulo_prompt_utilizado(self, etapa: Any, resultado: Any) -> str:
        nomes = {
            "revisor_textual": "Revisor textual",
            "copywriter": "Copywriter",
            "tendencia_cognitiva": "Tendência",
            "voz_bb": "Voz BB",
            "tagline": "Tagline",
            "headline": "Headline",
            "cta": "CTA",
        }
        return (
            nomes.get(etapa.id, self.rotulo_etapa(etapa.id))
            + " "
            + self.rotulo_prompt(resultado.prompt.nome)
        )

    def sim_nao(self, valor: bool) -> str:
        return "Sim" if valor else "Não"

    def limites_automaticos(self, limite_tagline: int, limite_headline: int) -> bool:
        return int(limite_tagline) == 100 and int(limite_headline) == 25

    def opcoes_catalogo(self, nomes: list[str]) -> list[tuple[str, str]]:
        return [(self.rotulo_nome(nome), nome) for nome in nomes]

    def rodar(self) -> Any:
        self.ui.aplicar_estilo()
        self.ui.titulo(
            "Prompt Criativo",
            "Experiência guiada para montar, comparar prompts e gerar mensagens.",
        )
        self.criador_provedor = resolver_criador_provedor(self.provedor)
        self.validar_catalogos()
        self.mostrar_status()

        produto = self.selecionar_produto()
        publico = self.selecionar_publico()
        apresentacao = self.selecionar_apresentacao(produto, publico)
        cenario = self.selecionar_cenario()

        self.ui.secao("Ajustes de geração")
        limite_tagline = self.ui.numero("Limite de caracteres da tagline", 100)
        limite_headline = self.ui.numero("Limite de caracteres da headline", 25)

        selecao = self.motor.Selecao(
            produto=produto.nome,
            publico=publico.nome,
            apresentacao=apresentacao.nome,
            cenario=cenario.nome,
            limite_tagline=limite_tagline,
            limite_headline=limite_headline,
        )

        self.parametros_automaticos = self.ui.confirmar(
            "Usar parâmetros automáticos?",
            padrao=True,
        )

        self.mostrar_parametros_geracao(limite_tagline, limite_headline)
        self.mostrar_configuracao(
            produto,
            publico,
            apresentacao,
            cenario,
            limite_tagline,
            limite_headline,
            self.parametros_automaticos,
        )

        resultado = self.motor.rodar_fluxo(
            selecao,
            criador_provedor=self.criador_provedor,
            configurar_chamada=self.configurar_chamada,
            escolher_resultado=self.escolher_resultado,
            ao_resultado_etapa=self.mostrar_etapa_concluida,
            ao_inicio_prompt=self.mostrar_inicio_prompt,
            ao_fim_prompt=self.mostrar_fim_prompt,
            ao_conjunto_final=self.mostrar_conjunto_final_ao_vivo,
        )
        self.mostrar_resultado(resultado)
        return resultado

    def mostrar_status(self) -> None:
        self.ui.card(
            "Preparação",
            {
                "Provedor": self.rotulo_nome(self.status.provedor),
                "Status": self.ui.status("pronto"),
                "Catálogos": "Carregados",
            },
        )

    def validar_catalogos(self) -> None:
        erros = self.motor.validar_catalogos()

        if erros:
            self.ui.card(
                "Preparação",
                {
                    "Status": self.ui.status("erro"),
                    "Erros": "\n".join(erros),
                },
            )
            raise RuntimeError("Catalogos com erros de validacao.")

    def selecionar_produto(self) -> Any:
        self.ui.secao("Produto")
        nome = self.ui.escolher_mapeado(
            "Escolha o produto",
            self.opcoes_catalogo(self.motor.listar_produtos()),
        )
        produto = self.motor.carregar_produto(nome)
        self.ui.card(
            "Produto",
            [
                (None, self.rotulo_nome(produto.nome)),
                ("Descrição", produto.descricao),
                ("Benefício racional", produto.beneficio_racional),
                ("Benefício emocional", produto.beneficio_emocional),
            ],
        )
        return produto

    def selecionar_publico(self) -> Any:
        self.ui.secao("Público")
        nome = self.ui.escolher_mapeado(
            "Escolha o público",
            self.opcoes_catalogo(self.motor.listar_publicos()),
        )
        publico = self.motor.carregar_publico(nome)
        self.ui.card(
            "Público",
            [
                (None, self.rotulo_nome(publico.nome)),
                ("Descrição", publico.descricao),
                ("Necessidade racional", publico.necessidade_racional),
                ("Necessidade emocional", publico.necessidade_emocional),
            ],
        )
        return publico

    def selecionar_apresentacao(self, produto: Any, publico: Any) -> Any:
        self.ui.secao("Apresentação")
        nome = self.ui.escolher_mapeado(
            "Escolha a apresentação",
            self.opcoes_catalogo(self.motor.listar_apresentacoes()),
        )
        apresentacao = self.motor.carregar_apresentacao(nome)
        previa = apresentacao.montar(produto, publico)

        self.ui.card(
            "Apresentação",
            [
                (None, self.rotulo_nome(apresentacao.nome)),
                ("Template padrão", apresentacao.template),
                ("Template preenchido", previa["texto"]),
            ],
        )

        return apresentacao

    def selecionar_cenario(self) -> Any:
        self.ui.secao("Cenário")
        nome = self.ui.escolher_mapeado(
            "Escolha o cenário",
            self.opcoes_catalogo(self.motor.listar_cenarios()),
        )
        cenario = self.motor.carregar_cenario(nome)
        estrutura = str(cenario.exibir_usuario or "").strip()
        if estrutura.lower() in {"", "null", "none"}:
            estrutura = cenario.texto_prompt

        self.ui.card(
            "Cenário",
            [
                (None, self.rotulo_nome(cenario.nome)),
                ("Função", cenario.funcao_prompt),
                ("Estrutura", estrutura),
            ],
        )
        return cenario

    def mostrar_configuracao(
        self,
        produto: Any,
        publico: Any,
        apresentacao: Any,
        cenario: Any,
        limite_tagline: int,
        limite_headline: int,
        parametros_automaticos: bool,
    ) -> None:
        limites_automaticos = self.limites_automaticos(
            limite_tagline,
            limite_headline,
        )
        self.ui.card_com_secoes(
            "Resumo da Geração",
            secoes=[
                (
                    "Contexto",
                    "\n\n".join(
                        [
                            "Produto\n\n" + self.rotulo_nome(produto.nome),
                            "Público\n\n" + self.rotulo_nome(publico.nome),
                        ]
                    ),
                ),
                (
                    "Estratégia",
                    "\n\n".join(
                        [
                            "Apresentação\n\n"
                            + self.rotulo_nome(apresentacao.nome),
                            "Cenário\n\n" + self.rotulo_nome(cenario.nome),
                        ]
                    ),
                ),
                (
                    "Limites",
                    "\n\n".join(
                        [
                            f"Tagline\n\n{limite_tagline} caracteres",
                            f"Headline\n\n{limite_headline} caracteres",
                        ]
                    ),
                ),
                (
                    "Configurações",
                    "\n\n".join(
                        [
                            "Limites automáticos\n\n"
                            + self.sim_nao(limites_automaticos),
                            "Prompt automático\n\n"
                            + self.sim_nao(parametros_automaticos),
                        ]
                    ),
                ),
            ],
        )

    def mostrar_parametros_geracao(
        self,
        limite_tagline: int,
        limite_headline: int,
    ) -> None:
        limites_automaticos = self.limites_automaticos(
            limite_tagline,
            limite_headline,
        )
        self.ui.card(
            "Parâmetros de Geração",
            {
                "Limites automáticos": self.sim_nao(limites_automaticos),
                "Tagline": f"{limite_tagline} caracteres",
                "Headline": f"{limite_headline} caracteres",
                "Configuração automática de prompt": self.sim_nao(
                    self.parametros_automaticos
                ),
            },
        )

    def escolher_resultado(self, etapa: Any, validos: list[Any]) -> str:
        self.ui.secao("Seleção")
        opcoes = [
            (
                f"Alternativa {indice} - Prompt "
                + self.rotulo_prompt(resultado.prompt.nome),
                resultado.identificador,
            )
            for indice, resultado in enumerate(validos, start=1)
        ]
        return self.ui.escolher_mapeado(
            "Escolha a alternativa que deve seguir no fluxo",
            opcoes,
            padrao=opcoes[0][1],
        )

    def titulo_execucao(self, etapa: Any, resultado: Any) -> str:
        if resultado.opcao and etapa.id == "tendencia_cognitiva":
            return (
                self.rotulo_etapa(etapa.id)
                + " - "
                + self.rotulo_nome(resultado.opcao)
                + " - "
                + self.rotulo_prompt(resultado.prompt.nome)
            )

        if resultado.opcao:
            return self.rotulo_prompt(resultado.prompt.nome)

        return (
            self.rotulo_etapa(etapa.id)
            + " - "
            + self.rotulo_prompt(resultado.prompt.nome)
        )

    def grupo_execucao(self, etapa: Any, resultado: Any) -> str:
        if resultado.opcao:
            return (
                "Tendência cognitiva - "
                + self.rotulo_nome(resultado.opcao)
            )

        return self.rotulo_etapa(etapa.id)

    def dados_entrada_execucao(self, resultado: Any) -> dict[str, Any]:
        dados = {
            "Template preenchido": resultado.template_preenchido,
            "System": resultado.system,
        }

        if resultado.opcao:
            dados["Opção"] = self.rotulo_nome(resultado.opcao)

        return dados

    def mostrar_entrada_execucao(
        self,
        resultado: Any,
        titulo: Optional[str] = None,
    ) -> None:
        self.ui.card(
            "Entrada",
            [(None, titulo or resultado.identificador)]
            + list(self.dados_entrada_execucao(resultado).items()),
        )

    def mostrar_saida_execucao(
        self,
        resultado: Any,
        titulo: Optional[str] = None,
    ) -> None:
        titulo = titulo or resultado.identificador

        if resultado.valido:
            self.ui.card(
                "Resultado",
                {
                    "Texto gerado": resultado.output,
                },
            )
            return

        self.ui.card(
            "Resultado",
            {
                "Erro": resultado.erro,
            },
        )

    def mostrar_cards_execucao(self, resultado: Any, titulo: Optional[str] = None) -> None:
        titulo = titulo or resultado.identificador
        self.mostrar_entrada_execucao(resultado, titulo)
        self.mostrar_saida_execucao(resultado, titulo)

    def quantidade_prompts(self, grupo: str) -> int:
        try:
            return len(self.motor.listar_prompts(grupo))
        except Exception:
            return 0

    def mostrar_inicio_fluxo_linear(self) -> None:
        if self.fluxo_linear_iniciado:
            return

        self.ui.card(
            "Base Criativa",
            {
                "Plano da base criativa": (
                    "As duas primeiras etapas criam a base textual e permitem "
                    "selecionar a alternativa que seguirá no fluxo."
                ),
                "Revisão Textual": (
                    str(self.quantidade_prompts("1_revisor_textual"))
                    + " prompts disponíveis"
                ),
                "Copywriter": (
                    str(self.quantidade_prompts("2_copywriter"))
                    + " prompts disponíveis"
                ),
                "Regra": (
                    "Quando houver mais de um resultado válido, o usuário "
                    "escolhe qual seguirá no fluxo."
                ),
            },
        )
        self.fluxo_linear_iniciado = True

    def mostrar_inicio_loop(self, resultado: Any = None) -> None:
        if self.loop_iniciado:
            return

        tendencias = self.motor.listar_tendencias()
        total_tendencias = len(tendencias)
        prompts_tendencia = self.quantidade_prompts("3_tendencia_cognitiva")
        prompts_voz = self.quantidade_prompts("4_voz_BB")
        prompts_tagline = self.quantidade_prompts("5_tagline")
        prompts_headline = self.quantidade_prompts("6_headline")
        prompts_cta = self.quantidade_prompts("7_cta")
        previstos = (
            total_tendencias
            * max(prompts_tendencia, 1)
            * max(prompts_voz, 1)
            * max(prompts_tagline, 1)
            * max(prompts_headline, 1)
            * max(prompts_cta, 1)
        )

        plano_tendencias = "\n".join(
            f"{indice}. {self.rotulo_nome(tendencia)}"
            for indice, tendencia in enumerate(tendencias, start=1)
        )
        self.ui.card(
            "Tendências",
            {
                "Plano de Tendências": plano_tendencias,
                "Conjuntos finais previstos": previstos,
                "Regra": "Cada tendência inicia um ramo independente.",
            },
        )
        self.loop_iniciado = True

    def configurar_parametros_variacoes(self) -> None:
        etapas = [
            etapa
            for etapa in self.motor.ETAPAS
            if self.etapa_automatica(etapa)
        ]

        if all(etapa.id in self.parametros_por_etapa for etapa in etapas):
            return

        self.ui.card(
            "Parâmetros de Geração",
            {
                "Configuração": "Manual para variações por tendência",
                "Aplicação": (
                    "Os valores abaixo serão usados em todos os fluxos "
                    "automáticos por tendência."
                ),
            },
        )

        for etapa in etapas:
            temperatura = self.ui.decimal(
                f"{self.rotulo_etapa(etapa.id)} - temperatura",
                float(etapa.temperature),
            )
            max_tokens = self.ui.numero(
                f"{self.rotulo_etapa(etapa.id)} - máximo de tokens",
                int(etapa.max_tokens),
            )
            self.parametros_por_etapa[etapa.id] = {
                "temperature": temperatura,
                "max_tokens": max_tokens,
            }

        campos = {
            self.rotulo_etapa(etapa.id): (
                "Temperatura "
                + str(self.parametros_por_etapa[etapa.id]["temperature"])
                + " | Máximo de tokens "
                + str(self.parametros_por_etapa[etapa.id]["max_tokens"])
            )
            for etapa in etapas
        }
        campos["Status"] = self.ui.status("selecionado")
        self.ui.card("Parâmetros de Geração", campos)

    def etapa_automatica(self, etapa: Any) -> bool:
        return etapa.id in {
            "tendencia_cognitiva",
            "voz_bb",
            "tagline",
            "headline",
            "cta",
        }

    def mostrar_tendencia(self, tendencia: str) -> None:
        nome = tendencia or "Sem tendencia"

        if nome in self.tendencias_exibidas:
            return

        self.tendencias_exibidas.add(nome)

    def caminho_progresso_fluxo(self) -> str:
        partes = []

        for etapa_id, _, _ in self.etapas_fluxo_final():
            prompt = self.progresso_fluxo_prompts.get(etapa_id)
            if prompt:
                partes.append(
                    f"{self.rotulo_etapa(etapa_id)} {self.rotulo_prompt(prompt)}"
                )

        return " -> ".join(partes)

    def preparar_progresso_automatico(self, etapa: Any, resultado: Any) -> None:
        if etapa.id == "tendencia_cognitiva":
            self.progresso_fluxo_handle = None
            self.progresso_fluxo_tendencia = resultado.opcao
            self.progresso_fluxo_concluidas = {}
            self.progresso_fluxo_prompts = {
                etapa.id: resultado.prompt.nome,
            }
            return

        if self.progresso_fluxo_handle is None:
            self.progresso_fluxo_tendencia = resultado.opcao
            self.progresso_fluxo_concluidas = {}
            self.progresso_fluxo_prompts = {}

            if (
                self.resultado_tendencia_base is not None
                and self.resultado_tendencia_base.opcao == resultado.opcao
            ):
                self.progresso_fluxo_concluidas["tendencia_cognitiva"] = (
                    self.resultado_tendencia_base
                )
                self.progresso_fluxo_prompts["tendencia_cognitiva"] = (
                    self.resultado_tendencia_base.prompt.nome
                )

        self.progresso_fluxo_prompts[etapa.id] = resultado.prompt.nome

    def atualizar_progresso_automatico(
        self,
        etapa: Any,
        resultado: Any,
        status: str,
    ) -> None:
        titulo = (
            "Gerando "
            + str(self.progresso_fluxo_tendencia or resultado.opcao)
            .replace("_", " ")
            .title()
        )
        detalhe = self.caminho_progresso_fluxo()
        atual = len(self.progresso_fluxo_concluidas)

        self.progresso_fluxo_handle = self.ui.progresso(
            titulo,
            atual,
            5,
            status,
            detalhe=detalhe,
            handle=self.progresso_fluxo_handle,
        )

    def mostrar_inicio_prompt(self, etapa: Any, resultado: Any) -> None:
        if etapa.id in {"revisor_textual", "copywriter"}:
            self.mostrar_inicio_fluxo_linear()

        if self.etapa_automatica(etapa):
            self.mostrar_inicio_loop(resultado)
            self.mostrar_tendencia(resultado.opcao)
            self.preparar_progresso_automatico(etapa, resultado)
            self.atualizar_progresso_automatico(
                etapa,
                resultado,
                (
                    "Gerando "
                    + self.rotulo_etapa(etapa.id)
                    + " "
                    + self.rotulo_prompt(resultado.prompt.nome)
                    + "..."
                ),
            )
            return

        titulo = self.titulo_execucao(etapa, resultado)
        self.progresso_chamadas[id(resultado)] = self.ui.progresso(
            titulo,
            0,
            1,
            "Gerando resultado...",
        )

    def mostrar_fim_prompt(self, etapa: Any, resultado: Any) -> None:
        if self.etapa_automatica(etapa):
            if resultado.valido:
                self.progresso_fluxo_concluidas[etapa.id] = resultado
                self.progresso_fluxo_prompts[etapa.id] = resultado.prompt.nome

                if etapa.id == "tendencia_cognitiva":
                    self.resultado_tendencia_base = resultado

            self.atualizar_progresso_automatico(
                etapa,
                resultado,
                (
                    f"{self.rotulo_etapa(etapa.id)} concluída."
                    if resultado.valido
                    else f"{self.rotulo_etapa(etapa.id)} não concluída."
                ),
            )
            return

        titulo = self.titulo_execucao(etapa, resultado)
        handle = self.progresso_chamadas.pop(id(resultado), None)
        self.ui.limpar(handle)
        self.mostrar_fluxo_linear(etapa, resultado)

    def configurar_chamada(
        self,
        etapa: Any,
        prompt: Any,
        opcao: str,
        parametros: dict[str, Any],
    ) -> dict[str, Any]:
        if self.parametros_automaticos:
            return dict(parametros)

        if self.etapa_automatica(etapa):
            self.mostrar_inicio_loop()
            self.configurar_parametros_variacoes()
            return dict(self.parametros_por_etapa[etapa.id])

        if etapa.id in self.parametros_por_etapa:
            return dict(self.parametros_por_etapa[etapa.id])

        vinculo = {
            "Etapa": self.rotulo_etapa(etapa.id),
            "Prompt inicial": self.rotulo_prompt(prompt.nome),
            "Aplicação": "Todos os prompts desta etapa",
            "Valores padrão": (
                f"Temperatura {parametros['temperature']} | "
                f"Máximo de tokens {parametros['max_tokens']}"
            ),
        }

        if opcao:
            vinculo["Primeira variação"] = self.rotulo_nome(opcao)

        self.ui.card("Parâmetros de Geração", vinculo)
        temperatura = self.ui.decimal(
            f"Temperatura - {self.rotulo_etapa(etapa.id)}",
            float(parametros["temperature"]),
        )
        max_tokens = self.ui.numero(
            f"Quantidade máxima de tokens - {self.rotulo_etapa(etapa.id)}",
            int(parametros["max_tokens"]),
        )

        ajustes = {
            "temperature": temperatura,
            "max_tokens": max_tokens,
        }
        self.parametros_por_etapa[etapa.id] = ajustes
        self.ui.card(
            "Parâmetros de Geração",
            {
                "Etapa": self.rotulo_etapa(etapa.id),
                "Temperatura": temperatura,
                "Máximo de tokens": max_tokens,
                "Status": self.ui.status("selecionado"),
            },
        )
        return dict(ajustes)

    def mostrar_etapa_concluida(self, etapa: Any) -> None:
        selecionado = etapa.resultado_selecionado()

        if selecionado is None:
            return

        alternativa = 1
        for indice, resultado in enumerate(etapa.validos(), start=1):
            if resultado is selecionado:
                alternativa = indice
                break

        self.ui.card(
            "Seleção",
            {
                "Etapa": self.rotulo_etapa(etapa.id),
                "Alternativa selecionada": alternativa,
                "Prompt": self.rotulo_prompt(selecionado.prompt.nome),
                "Status": self.ui.status("selecionado"),
            },
        )

    def prompt_oficial_resultado(self, etapa: Any, resultado: Any) -> dict[str, Any]:
        return {
            "etapa": etapa.titulo,
            "prompt": resultado.prompt.nome,
            "arquivo_prompt": resultado.prompt.identificador,
            "opcao": resultado.opcao,
            "mensagens_enviadas": [
                {
                    "role": "system",
                    "content": resultado.system,
                },
                {
                    "role": "user",
                    "tipo": "template",
                    "content": resultado.template_preenchido,
                },
                {
                    "role": "user",
                    "tipo": "entrada",
                    "content": resultado.entrada,
                },
            ],
            "parametros": {
                "temperature": resultado.parametros.get("temperature"),
                "max_tokens": resultado.parametros.get("max_tokens"),
                "top_p": resultado.parametros.get("top_p"),
                "frequency_penalty": resultado.parametros.get("frequency_penalty"),
                "presence_penalty": resultado.parametros.get("presence_penalty"),
                "best_of": resultado.parametros.get("best_of"),
            },
        }

    def html_prompt_oficial_resultado(self, etapa: Any, resultado: Any) -> str:
        return self.ui.json_bloco(self.prompt_oficial_resultado(etapa, resultado))

    def detalhes_tecnicos_resultado(
        self,
        etapa: Any,
        resultado: Any,
    ) -> list[dict[str, Any]]:
        return [
            {
                "titulo": "Prompt utilizado",
                "conteudo": self.rotulo_prompt_utilizado(etapa, resultado),
            },
            {
                "titulo": "Entrada",
                "conteudo": resultado.entrada,
            },
            {
                "titulo": "Template preenchido",
                "conteudo": resultado.template_preenchido,
            },
            {
                "titulo": "System",
                "conteudo": resultado.system,
            },
            {
                "titulo": "Payload LLM",
                "conteudo": self.prompt_oficial_resultado(etapa, resultado),
            },
        ]

    def mostrar_fluxo_linear(self, etapa: Any, resultado: Any) -> None:
        numero = self.fluxos_lineares.get(etapa.id, 0) + 1
        self.fluxos_lineares[etapa.id] = numero
        self.ui.card_com_secoes(
            self.rotulo_etapa(etapa.id),
            {
                "Alternativa": numero,
                "Prompt": self.rotulo_prompt(resultado.prompt.nome),
                "Status": self.ui.status("pronto" if resultado.valido else "erro"),
            },
            secoes=[
                (
                    "Resultado",
                    resultado.output if resultado.valido else resultado.erro,
                )
            ],
            detalhes_tecnicos=self.detalhes_tecnicos_resultado(etapa, resultado),
        )

    def mostrar_conjunto_final_ao_vivo(self, conjunto: Any) -> None:
        tendencia = conjunto.tendencia or "Sem tendencia"
        numero = self.fluxos_por_tendencia.get(tendencia, 0) + 1
        self.fluxos_por_tendencia[tendencia] = numero

        self.progresso_fluxo_concluidas = {
            resultado.prompt.grupo: resultado
            for resultado in conjunto.resultados
        }
        self.progresso_fluxo_prompts = {
            etapa_id: self.prompt_do_conjunto(conjunto, etapa_id)
            for etapa_id, _, _ in self.etapas_fluxo_final()
        }
        self.progresso_fluxo_tendencia = tendencia

        self.ui.progresso(
            "Variação: " + self.rotulo_nome(tendencia),
            5,
            5,
            f"Fluxo {numero} pronto.",
            detalhe=self.caminho_fluxo(conjunto),
            handle=self.progresso_fluxo_handle,
        )
        self.ui.limpar(self.progresso_fluxo_handle)
        self.mostrar_fluxo_conjunto(conjunto, numero)
        self.fluxos_exibidos_ao_vivo += 1
        self.progresso_fluxo_handle = None
        self.progresso_fluxo_concluidas = {}
        self.progresso_fluxo_prompts = {}

    def mostrar_resultado(self, resultado: Any) -> None:
        if resultado.conjuntos:
            if self.fluxos_exibidos_ao_vivo == 0:
                self.mostrar_conjuntos(resultado.conjuntos)

            self.ui.final(
                {
                    "Total de conjuntos gerados": len(resultado.conjuntos),
                    "Regra": "Cada conjunto representa uma tendência.",
                }
            )
        else:
            self.ui.final(
                {
                    "Headline": resultado.headline,
                    "Tagline": resultado.tagline,
                    "CTA": resultado.cta,
                    "Texto final": resultado.resumo_institucional,
                }
            )

    def prompt_do_conjunto(self, conjunto: Any, etapa_id: str) -> str:
        valor = str(conjunto.prompts.get(etapa_id, ""))
        valor = valor.split(" - ")[0]

        if "/" in valor:
            return valor.rsplit("/", 1)[-1]

        return valor

    def etapas_fluxo_final(self) -> list[tuple[str, str, str]]:
        return [
            ("tendencia_cognitiva", "Tendência cognitiva", "3_tendencia_cognitiva"),
            ("voz_bb", "Voz Institucional BB", "4_voz_BB"),
            ("tagline", "Tagline", "5_tagline"),
            ("headline", "Headline", "6_headline"),
            ("cta", "CTA", "7_cta"),
        ]

    def resultado_conjunto_etapa(self, conjunto: Any, grupo_prompt: str) -> Any:
        for resultado in conjunto.resultados:
            if resultado.prompt.grupo == grupo_prompt:
                return resultado

        return None

    def caminho_fluxo(self, conjunto: Any) -> str:
        partes = []
        rotulos = {
            "tendencia_cognitiva": "Tendência",
            "voz_bb": "Voz BB",
            "tagline": "Tagline",
            "headline": "Headline",
            "cta": "CTA",
        }

        for etapa_id, _, _ in self.etapas_fluxo_final():
            prompt = self.prompt_do_conjunto(conjunto, etapa_id)
            if prompt:
                partes.append(f"{rotulos[etapa_id]} {self.rotulo_prompt(prompt)}")

        return " -> ".join(partes)

    def html_valor(self, chave: str, valor: Any) -> str:
        return (
            "<div style='margin:8px 0'>"
            f"<div class='pc-label'>{html.escape(str(chave))}</div>"
            f"<div class='pc-value'>{html.escape(str(valor or ''))}</div>"
            "</div>"
        )

    def html_saida_valor(
        self,
        titulo: str,
        valor: Any,
        *,
        destaque: bool = False,
    ) -> str:
        classe = "pc-output-item pc-output-main" if destaque else "pc-output-item"
        return (
            f"<div class='{classe}'>"
            f"<div class='pc-output-title'>{html.escape(str(titulo))}</div>"
            f"<div class='pc-output-text'>{html.escape(str(valor or ''))}</div>"
            "</div>"
        )

    def html_saida_lista(
        self,
        itens: list[tuple[str, Any]],
        *,
        destaque_primeiro: bool = False,
    ) -> str:
        partes = []

        for indice, (titulo, valor) in enumerate(itens):
            partes.append(
                self.html_saida_valor(
                    titulo,
                    valor,
                    destaque=destaque_primeiro and indice == 0,
                )
            )

        return "<div class='pc-output-list'>" + "".join(partes) + "</div>"

    def html_templates_resultados(
        self,
        resultados: list[Any],
    ) -> str:
        partes = []

        for indice, resultado in enumerate(resultados, start=1):
            partes.append(
                "<div class='pc-stage'>"
                f"<div class='pc-stage-title'>{indice}. "
                f"{html.escape(resultado.prompt.identificador)}</div>"
                + self.html_valor(
                    "Template preenchido",
                    resultado.template_preenchido,
                )
                + "</div>"
            )

        return "".join(partes)

    def html_system_resultados(
        self,
        resultados: list[Any],
    ) -> str:
        vistos: dict[str, list[str]] = {}

        for resultado in resultados:
            vistos.setdefault(str(resultado.system or ""), []).append(
                resultado.prompt.identificador
            )

        partes = []

        for indice, (system, prompts) in enumerate(vistos.items(), start=1):
            titulo = (
                "System"
                if len(vistos) == 1
                else f"System {indice}"
            )
            partes.append(
                "<div class='pc-stage'>"
                f"<div class='pc-stage-title'>{html.escape(titulo)}</div>"
                + self.html_valor("Usado em", ", ".join(prompts))
                + self.html_valor("Conteudo", system)
                + "</div>"
            )

        return "".join(partes)

    def html_entrada_resultados(self, resultados: list[Any]) -> str:
        return (
            "<details class='pc-inner'>"
            "<summary>Templates com placeholders preenchidos</summary>"
            + self.html_templates_resultados(resultados)
            + "</details>"
            "<details class='pc-inner'>"
            "<summary>System enviado</summary>"
            + self.html_system_resultados(resultados)
            + "</details>"
        )

    def html_entrada_fluxo(self, conjunto: Any) -> str:
        resultados = []

        for _, _, grupo_prompt in self.etapas_fluxo_final():
            resultado = self.resultado_conjunto_etapa(conjunto, grupo_prompt)
            if resultado is not None:
                resultados.append(resultado)

        return self.html_entrada_resultados(resultados)

    def html_saida_fluxo(self, conjunto: Any) -> str:
        saidas = [
            ("3_tendencia_cognitiva", "Texto com Tendência"),
            ("4_voz_BB", "Texto com Voz BB"),
            ("5_tagline", "Tagline"),
            ("6_headline", "Headline"),
            ("7_cta", "CTA"),
        ]
        itens = []

        for grupo_prompt, titulo in saidas:
            resultado = self.resultado_conjunto_etapa(conjunto, grupo_prompt)
            if resultado is None:
                continue

            itens.append((titulo, resultado.output))

        return self.html_saida_lista(itens, destaque_primeiro=True)

    def resultados_do_conjunto(self, conjunto: Any) -> list[Any]:
        resultados = []

        for _, _, grupo_prompt in self.etapas_fluxo_final():
            resultado = self.resultado_conjunto_etapa(conjunto, grupo_prompt)
            if resultado is not None:
                resultados.append(resultado)

        return resultados

    def texto_templates_resultados(self, resultados: list[Any]) -> str:
        partes = []

        for indice, resultado in enumerate(resultados, start=1):
            partes.append(
                "\n\n".join(
                    [
                        f"{indice}. `{resultado.prompt.identificador}`",
                        "Template preenchido",
                        resultado.template_preenchido,
                    ]
                )
            )

        return "\n\n---\n\n".join(partes)

    def texto_system_resultados(self, resultados: list[Any]) -> str:
        vistos: dict[str, list[str]] = {}

        for resultado in resultados:
            vistos.setdefault(str(resultado.system or ""), []).append(
                resultado.prompt.identificador
            )

        partes = []
        for indice, (system, prompts) in enumerate(vistos.items(), start=1):
            campos = ["Usado em", ", ".join(prompts), "Conteúdo", system]
            if len(vistos) > 1:
                campos = [f"System {indice}"] + campos

            partes.append("\n\n".join(campos))

        return "\n\n---\n\n".join(partes)

    def pipeline_conjunto(self, conjunto: Any) -> str:
        etapas = []

        for etapa_id, _, _ in self.etapas_fluxo_final():
            prompt = self.prompt_do_conjunto(conjunto, etapa_id)
            if prompt:
                etapas.append(
                    f"{self.rotulo_etapa(etapa_id)} {self.rotulo_prompt(prompt)}"
                )

        return self.ui.pipeline("Pipeline", etapas)

    def detalhes_tecnicos_conjunto(self, conjunto: Any) -> list[dict[str, Any]]:
        resultados = self.resultados_do_conjunto(conjunto)
        return [
            {
                "titulo": "Entrada",
                "conteudo": self.texto_templates_resultados(resultados),
            },
            {
                "titulo": "System",
                "conteudo": self.texto_system_resultados(resultados),
            },
            {
                "titulo": "Payload LLM",
                "conteudo": self.prompt_oficial_fluxo(conjunto),
            },
        ]

    def prompt_oficial_fluxo(self, conjunto: Any) -> dict[str, Any]:
        etapas = []

        for _, titulo, grupo_prompt in self.etapas_fluxo_final():
            resultado = self.resultado_conjunto_etapa(conjunto, grupo_prompt)
            if resultado is None:
                continue

            etapas.append(
                {
                    "etapa": titulo,
                    "prompt": resultado.prompt.nome,
                    "arquivo_prompt": resultado.prompt.identificador,
                    "opcao": resultado.opcao,
                    "mensagens_enviadas": [
                        {
                            "role": "system",
                            "content": resultado.system,
                        },
                        {
                            "role": "user",
                            "tipo": "template",
                            "content": resultado.template_preenchido,
                        },
                        {
                            "role": "user",
                            "tipo": "entrada",
                            "content": resultado.entrada,
                        },
                    ],
                    "parametros": {
                        "temperature": resultado.parametros.get("temperature"),
                        "max_tokens": resultado.parametros.get("max_tokens"),
                        "top_p": resultado.parametros.get("top_p"),
                        "frequency_penalty": resultado.parametros.get(
                            "frequency_penalty"
                        ),
                        "presence_penalty": resultado.parametros.get(
                            "presence_penalty"
                        ),
                        "best_of": resultado.parametros.get("best_of"),
                    },
                }
            )

        return {
            "tendencia": conjunto.tendencia,
            "caminho": self.caminho_fluxo(conjunto),
            "etapas": etapas,
        }

    def html_prompt_oficial_fluxo(self, conjunto: Any) -> str:
        return self.ui.json_bloco(self.prompt_oficial_fluxo(conjunto))

    def mostrar_fluxo_conjunto(
        self,
        conjunto: Any,
        numero: int,
    ) -> None:
        tendencia = self.rotulo_nome(conjunto.tendencia or "Sem tendencia")
        self.ui.card(
            tendencia,
            {
                "Fluxo": numero,
                "Status": self.ui.status("pronto"),
                "Pipeline": self.pipeline_conjunto(conjunto),
            },
        )
        self.ui.card_com_secoes(
            "Resultado da Tendência - " + tendencia,
            secoes=[
                (
                    "Texto com Tendência",
                    (
                        self.resultado_conjunto_etapa(
                            conjunto,
                            "3_tendencia_cognitiva",
                        ).output
                    ),
                ),
                ("Texto na Voz BB", conjunto.texto_institucional),
                {"titulo": "Tagline", "conteudo": conjunto.tagline, "compacto": True},
                {"titulo": "Headline", "conteudo": conjunto.headline, "compacto": True},
                {"titulo": "CTA", "conteudo": conjunto.cta, "compacto": True},
            ],
            detalhes_tecnicos=self.detalhes_tecnicos_conjunto(conjunto),
        )

    def mostrar_conjuntos(self, conjuntos: list[Any]) -> None:
        grupos: dict[str, list[Any]] = {}

        for conjunto in conjuntos:
            grupos.setdefault(conjunto.tendencia or "Sem tendencia", []).append(conjunto)

        for tendencia, conjuntos_tendencia in grupos.items():
            self.mostrar_tendencia(tendencia)

            for numero, conjunto in enumerate(conjuntos_tendencia, start=1):
                self.mostrar_fluxo_conjunto(conjunto, numero)


def fluxo_geracao(provedor: Optional[str] = None) -> Any:
    """Entrada unica chamada pela rotina-principal.ipynb."""

    provedor_normalizado = normalizar_provedor(provedor)
    status = preparar_ambiente(provedor_normalizado)

    if status.dependencias_ausentes:
        raise RuntimeError(
            "Dependencias ausentes: "
            + ", ".join(status.dependencias_ausentes)
            + "\n\nInstale as dependencias do projeto antes de executar o fluxo."
        )

    motor = importlib.import_module("src.motor")

    return Experiencia(
        motor=motor,
        status=status,
        provedor=provedor_normalizado,
    ).rodar()
