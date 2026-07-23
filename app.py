"""Experiencia visual do notebook."""

from __future__ import annotations

import html
import importlib
import importlib.util
import json
import subprocess
import sys
import textwrap
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Optional, Union


DEPENDENCIAS = {
    "yaml": "PyYAML",
    "dotenv": "python-dotenv",
    "requests": "requests",
    "urllib3": "urllib3",
}


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
    dependencias_ausentes: list[str] = field(default_factory=list)
    instalacao_executada: bool = False
    instalacao_ok: Optional[bool] = None
    mensagens: list[str] = field(default_factory=list)


def raiz_projeto(inicio: Optional[Union[str, Path]] = None) -> Path:
    atual = Path(inicio or Path.cwd()).resolve()

    for pasta in [atual, *atual.parents]:
        if (
            (pasta / "produtos").exists()
            and (pasta / "publicos").exists()
            and (pasta / "prompts").exists()
        ):
            return pasta

    raise RuntimeError("Nao foi possivel localizar a raiz do projeto.")


def dependencias_ausentes() -> list[str]:
    ausentes = []

    for modulo, pacote in DEPENDENCIAS.items():
        if importlib.util.find_spec(modulo) is None:
            ausentes.append(pacote)

    return sorted(set(ausentes))


def instalar_dependencias(raiz: Path) -> tuple[bool, str]:
    requirements = raiz / "requirements.txt"

    if not requirements.exists():
        return False, "requirements.txt nao encontrado."

    processo = subprocess.run(
        [
            sys.executable,
            "-m",
            "pip",
            "install",
            "-r",
            str(requirements),
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    saida = "\n".join(
        parte
        for parte in [processo.stdout, processo.stderr]
        if parte
    ).strip()

    return processo.returncode == 0, saida


def preparar_ambiente(instalar: bool = True) -> StatusAmbiente:
    raiz = raiz_projeto()

    if str(raiz) not in sys.path:
        sys.path.insert(0, str(raiz))

    status = StatusAmbiente(
        raiz=raiz,
        python=".".join(str(parte) for parte in sys.version_info[:3]),
    )
    status.dependencias_ausentes = dependencias_ausentes()

    if status.dependencias_ausentes and instalar:
        status.instalacao_executada = True
        status.instalacao_ok, saida = instalar_dependencias(raiz)

        if saida:
            status.mensagens.append(saida)

        status.dependencias_ausentes = dependencias_ausentes()

    return status


def em_notebook() -> bool:
    if display is None or get_ipython is None:
        return False

    shell = get_ipython()

    if shell is None:
        return False

    return shell.__class__.__name__ == "ZMQInteractiveShell"


def texto_curto(texto: Any, largura: int = 100) -> str:
    return textwrap.fill(" ".join(str(texto or "").split()), width=largura)


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
                    padding: 14px 16px;
                    margin: 10px 0;
                    background: #ffffff;
                }
                .pc-label {
                    font-size: 12px;
                    font-weight: 700;
                    letter-spacing: .02em;
                    text-transform: uppercase;
                    color: #52606d;
                    margin-bottom: 4px;
                }
                .pc-value {
                    white-space: pre-wrap;
                    line-height: 1.45;
                }
                .pc-muted {
                    color: #52606d;
                    font-size: 13px;
                }
                .pc-final {
                    border: 2px solid #f3c300;
                    border-radius: 8px;
                    padding: 16px;
                    margin: 14px 0;
                    background: #fffdf2;
                }
                </style>
                """
            )
        )

    def titulo(self, texto: str, apoio: Optional[str] = None) -> None:
        if em_notebook() and HTML is not None:
            apoio_html = (
                f"<div class='pc-muted'>{html.escape(apoio)}</div>"
                if apoio
                else ""
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

    def ficha(self, titulo: str, dados: dict[str, Any]) -> None:
        if em_notebook() and HTML is not None:
            partes = [f"<h3 style='margin:0 0 10px'>{html.escape(titulo)}</h3>"]

            for chave, valor in dados.items():
                partes.append(
                    "<div style='margin:10px 0'>"
                    f"<div class='pc-label'>{html.escape(str(chave))}</div>"
                    f"<div class='pc-value'>{html.escape(str(valor or ''))}</div>"
                    "</div>"
                )

            display(HTML("<div class='pc-wrap pc-card'>" + "".join(partes) + "</div>"))
            return

        print(f"\n{titulo}")
        for chave, valor in dados.items():
            print(f"\n{chave}")
            print(texto_curto(valor))

    def final(self, dados: dict[str, Any]) -> None:
        if em_notebook() and HTML is not None:
            partes = []

            for chave, valor in dados.items():
                partes.append(
                    "<div style='margin:12px 0'>"
                    f"<div class='pc-label'>{html.escape(str(chave))}</div>"
                    f"<div class='pc-value'>{html.escape(str(valor or ''))}</div>"
                    "</div>"
                )

            display(HTML("<div class='pc-wrap pc-final'>" + "".join(partes) + "</div>"))
            return

        self.ficha("Resultado final", dados)

    def opcoes(self, opcoes: list[str]) -> None:
        linhas = [
            f"{indice:>2}. {opcao.replace('_', ' ').title()}"
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

            print("Opção inválida.")

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

            print("Informe um número inteiro positivo.")

    def confirmar(self, mensagem: str, padrao: bool = True) -> bool:
        dica = "S/n" if padrao else "s/N"

        while True:
            valor = input(f"{mensagem} [{dica}]: ").strip().lower()

            if not valor:
                return padrao
            if valor in {"s", "sim", "y", "yes"}:
                return True
            if valor in {"n", "nao", "não", "no"}:
                return False

            print("Responda com sim ou não.")

    def debug_json(self, titulo: str, dados: dict[str, Any]) -> None:
        conteudo = json.dumps(dados, indent=2, ensure_ascii=False, default=str)

        if em_notebook() and Markdown is not None:
            display(Markdown(f"#### {titulo}\n```json\n{conteudo}\n```"))
            return

        print(f"\n{titulo}")
        print(conteudo)


class Experiencia:
    def __init__(
        self,
        motor: Any,
        status: StatusAmbiente,
        *,
        modo_padrao: str = "simulacao",
    ):
        self.motor = motor
        self.status = status
        self.modo_padrao = modo_padrao
        self.ui = Visual()

    def rodar(self) -> Any:
        self.ui.aplicar_estilo()
        self.ui.titulo(
            "Prompt Criativo",
            "Experiência guiada para montar, revisar e gerar peças de mensagem.",
        )
        self.mostrar_status()
        self.validar_catalogos()

        produto = self.selecionar_produto()
        publico = self.selecionar_publico()
        apresentacao = self.selecionar_apresentacao()
        cenario = self.selecionar_cenario()
        tendencia = self.selecionar_tendencia()
        prompt_revisor = self.selecionar_revisor()

        self.ui.secao("Parâmetros finais")
        modo = self.ui.escolher(
            "Modo de geração",
            ["simulacao", "real"],
            padrao=self.modo_padrao,
        )
        limite_tagline = self.ui.numero("Limite de caracteres da tagline", 120)
        limite_headline = self.ui.numero("Limite de caracteres da headline", 60)

        selecao = self.motor.Selecao(
            produto=produto.nome,
            publico=publico.nome,
            apresentacao=apresentacao.nome,
            cenario=cenario.nome,
            tendencia=tendencia.nome,
            prompt_revisor=prompt_revisor,
            limite_tagline=limite_tagline,
            limite_headline=limite_headline,
        )
        contexto, previa = self.motor.contexto_inicial(
            selecao,
            {
                "produto": produto,
                "publico": publico,
                "apresentacao": apresentacao,
                "cenario": cenario,
                "tendencia": tendencia,
            },
        )

        self.ui.secao("Preview da apresentação")
        self.ui.ficha(
            "Texto base",
            {
                "Visual": previa["visual"],
                "Texto final": previa["texto"],
            },
        )

        if not self.ui.confirmar("Executar fluxo completo", padrao=True):
            return {
                "selecao": selecao,
                "contexto": contexto,
                "apresentacao": previa,
                "executado": False,
            }

        resultado = self.motor.rodar_fluxo(selecao, modo=modo)
        self.mostrar_resultado(resultado)
        return resultado

    def mostrar_status(self) -> None:
        self.ui.secao("Ambiente")
        self.ui.ficha(
            "Status inicial",
            {
                "Raiz": self.status.raiz,
                "Python": self.status.python,
                "Dependências ausentes": (
                    ", ".join(self.status.dependencias_ausentes)
                    if self.status.dependencias_ausentes
                    else "Nenhuma"
                ),
                "Instalação executada": "Sim" if self.status.instalacao_executada else "Não",
            },
        )

    def validar_catalogos(self) -> None:
        erros = self.motor.validar_catalogos()

        if erros:
            self.ui.ficha(
                "Validação dos catálogos",
                {
                    "Status": "Encontramos ajustes pendentes.",
                    "Erros": "\n".join(erros),
                },
            )
            raise RuntimeError("Catálogos com erros de validação.")

        self.ui.ficha(
            "Validação dos catálogos",
            {"Status": "Todos os catálogos foram carregados."},
        )

    def selecionar_produto(self) -> Any:
        self.ui.secao("Produto")
        nome = self.ui.escolher("Escolha o produto", self.motor.Produto.listar())
        produto = self.motor.Produto(nome)
        self.ui.ficha(
            produto.rotulo,
            {
                "Descrição": produto.descricao,
                "Benefício racional": produto.beneficio_racional,
                "Benefício emocional": produto.beneficio_emocional,
            },
        )
        return produto

    def selecionar_publico(self) -> Any:
        self.ui.secao("Público")
        nome = self.ui.escolher("Escolha o público", self.motor.Publico.listar())
        publico = self.motor.Publico(nome)
        self.ui.ficha(
            publico.rotulo,
            {
                "Descrição": publico.descricao,
                "Necessidade racional": publico.necessidade_racional,
                "Necessidade emocional": publico.necessidade_emocional,
            },
        )
        return publico

    def selecionar_apresentacao(self) -> Any:
        self.ui.secao("Apresentação")
        nome = self.ui.escolher(
            "Escolha a apresentação",
            self.motor.Apresentacao.listar(),
        )
        apresentacao = self.motor.Apresentacao(nome)
        self.ui.ficha(
            apresentacao.rotulo,
            {
                "Descrição": apresentacao.descricao,
                "Template": apresentacao.template,
            },
        )
        return apresentacao

    def selecionar_cenario(self) -> Any:
        self.ui.secao("Cenário")
        nome = self.ui.escolher("Escolha o cenário", self.motor.Cenario.listar())
        cenario = self.motor.Cenario(nome)
        self.ui.ficha(
            cenario.rotulo,
            {
                "Função": cenario.funcao_prompt,
                "Estrutura": cenario.texto_prompt,
            },
        )
        return cenario

    def selecionar_tendencia(self) -> Any:
        self.ui.secao("Tendência cognitiva")
        nome = self.ui.escolher(
            "Escolha a tendência",
            self.motor.Tendencia.listar(),
        )
        tendencia = self.motor.Tendencia(nome)
        self.ui.ficha(
            tendencia.rotulo,
            {
                "Função": tendencia.funcao_prompt,
                "Descrição": tendencia.campo("not_prompt_descricao", ""),
                "Instrução de geração": tendencia.texto_prompt,
            },
        )
        return tendencia

    def selecionar_revisor(self) -> str:
        self.ui.secao("Revisão textual")
        prompts = self.motor.Prompt.listar("1_revisor_textual")
        nome = self.ui.escolher(
            "Escolha o prompt de revisão",
            prompts,
            padrao="p1",
        )
        prompt = self.motor.Prompt("1_revisor_textual", nome)
        self.ui.ficha(f"1_revisor_textual/{nome}", {"Template": prompt.template})
        return nome

    def mostrar_resultado(self, resultado: Any) -> None:
        modo = "simulação" if resultado.etapas and resultado.etapas[0].simulado else "real"

        self.ui.secao("Resultado")
        self.ui.final(
            {
                "Modo": modo,
                "Headline": resultado.headline,
                "Tagline": resultado.tagline,
                "CTA": resultado.cta,
                "Resumo institucional": resultado.resumo_institucional,
            }
        )

        self.ui.secao("Etapas")

        for etapa in resultado.etapas:
            self.ui.ficha(
                etapa.titulo,
                {
                    "Prompt": etapa.prompt,
                    "Entrada": etapa.entrada,
                    "Saída": etapa.output,
                },
            )


def fluxo_geracao(
    *,
    modo_padrao: str = "simulacao",
    instalar_dependencias: bool = True,
):
    """Entrada unica chamada pela rotina-principal.ipynb."""

    status = preparar_ambiente(instalar=instalar_dependencias)

    if status.dependencias_ausentes:
        raise RuntimeError(
            "Ainda há dependências ausentes: "
            + ", ".join(status.dependencias_ausentes)
            + ". Confira o requirements.txt e tente executar novamente."
        )

    motor = importlib.import_module("src.motor")

    return Experiencia(
        motor,
        status,
        modo_padrao=modo_padrao,
    ).rodar()
