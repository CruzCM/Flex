"""Classes e estruturas de dados do projeto."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Optional

from .yaml_utils import (
    carregar_yaml,
    listar_yaml,
    placeholders,
    preencher,
    raiz_projeto,
    rotulo,
    validar_campos,
)


class RegistroYaml:
    pasta = ""
    obrigatorios: tuple[str, ...] = ()

    def __init__(self, nome: str, raiz: Optional[Path] = None):
        self.nome = nome
        self.raiz = raiz or raiz_projeto()
        self.dados = carregar_yaml(self.pasta, nome, self.raiz)

        validar_campos(
            self.dados,
            self.obrigatorios,
            f"{self.__class__.__name__} '{nome}'",
        )

        for chave, valor in self.dados.items():
            setattr(self, chave, valor)

    @classmethod
    def listar(cls, raiz: Optional[Path] = None) -> list[str]:
        return listar_yaml(cls.pasta, raiz)

    @property
    def rotulo(self) -> str:
        return rotulo(self.nome)

    def campo(self, nome: str, padrao: Any = "") -> Any:
        return self.dados.get(nome, padrao)

    def __repr__(self) -> str:
        return self.nome


class Produto(RegistroYaml):
    pasta = "produtos"
    obrigatorios = (
        "descricao",
        "beneficio_racional",
        "beneficio_emocional",
    )


class Publico(RegistroYaml):
    pasta = "publicos"
    obrigatorios = (
        "descricao",
        "necessidade_racional",
        "necessidade_emocional",
    )


class Apresentacao(RegistroYaml):
    pasta = "apresentacoes"
    obrigatorios = ("template", "descricao")

    def __init__(self, nome: str, raiz: Optional[Path] = None):
        super().__init__(nome, raiz)
        self.placeholders = placeholders(self.template)

    def montar(self, produto: Produto, publico: Publico) -> dict[str, Any]:
        def compacto(texto: Any) -> str:
            return " ".join(str(texto).split())

        valores = {
            "PH_PBCO_DESCRICAO": compacto(publico.descricao),
            "PH_PBCO_NEC_RACIONAL": compacto(publico.necessidade_racional),
            "PH_PBCO_NEC_EMOCIONAL": compacto(publico.necessidade_emocional),
            "PH_PROD_DESCRICAO": compacto(produto.descricao),
            "PH_PROD_BEN_RACIONAL": compacto(produto.beneficio_racional),
            "PH_PROD_BEN_EMOCIONAL": compacto(produto.beneficio_emocional),
        }

        texto_final = " ".join(preencher(self.template, valores).split())
        visual = self.template

        for chave, valor in valores.items():
            visual = visual.replace(f"{{{chave}}}", f"\n\n{valor}\n\n")

        visual = "\n".join(linha.rstrip() for linha in visual.splitlines())

        return {
            "texto": texto_final,
            "visual": visual,
            "placeholders": valores,
        }


class Cenario(RegistroYaml):
    pasta = "cenarios"
    obrigatorios = ("texto_prompt", "funcao_prompt")


class Tendencia(RegistroYaml):
    pasta = "tendencias"
    obrigatorios = ("texto_prompt", "funcao_prompt")


class Prompt:
    obrigatorios = ("template", "system")

    def __init__(
        self,
        grupo: str,
        nome: str = "p1",
        raiz: Optional[Path] = None,
    ):
        self.grupo = grupo
        self.nome = nome
        self.pasta = Path("prompts") / grupo
        self.raiz = raiz or raiz_projeto()
        self.dados = carregar_yaml(self.pasta, nome, self.raiz)

        validar_campos(
            self.dados,
            self.obrigatorios,
            f"Prompt '{grupo}/{nome}'",
        )

        self.template = self.dados["template"]
        self.system = self.dados["system"]

    @classmethod
    def listar_grupos(cls, raiz: Optional[Path] = None) -> list[str]:
        pasta = (raiz or raiz_projeto()) / "prompts"

        if not pasta.exists():
            return []

        return sorted(item.name for item in pasta.iterdir() if item.is_dir())

    @classmethod
    def listar(cls, grupo: str, raiz: Optional[Path] = None) -> list[str]:
        return listar_yaml(Path("prompts") / grupo, raiz)

    def montar(self, valores: dict[str, Any]) -> str:
        return preencher(self.template, valores)

    def __repr__(self) -> str:
        return f"{self.grupo}/{self.nome}"


@dataclass
class Selecao:
    produto: str
    publico: str
    apresentacao: str
    cenario: str
    tendencia: str
    prompt_revisor: str = "p1"
    limite_tagline: int = 120
    limite_headline: int = 60


@dataclass
class Etapa:
    id: str
    titulo: str
    grupo_prompt: str
    saida: str
    entrada: str
    prompt_nome: str = "p1"
    temperature: float = 0.5
    max_tokens: int = 512


@dataclass
class ResultadoEtapa:
    id: str
    titulo: str
    prompt: str
    system: str
    template: str
    entrada: str
    output: str
    bruto: dict[str, Any]
    simulado: bool


@dataclass
class Resultado:
    selecao: Selecao
    apresentacao_visual: str
    apresentacao_texto: str
    placeholders: dict[str, str]
    contexto: dict[str, Any]
    etapas: list[ResultadoEtapa] = field(default_factory=list)

    @property
    def headline(self) -> str:
        return str(self.contexto.get("PH_TITULO", ""))

    @property
    def tagline(self) -> str:
        return str(self.contexto.get("PH_TEXTO", ""))

    @property
    def cta(self) -> str:
        return str(self.contexto.get("PH_CTA", ""))

    @property
    def resumo_institucional(self) -> str:
        return str(self.contexto.get("PH_BASE_BB", ""))


def validar_catalogos(raiz: Optional[Path] = None) -> list[str]:
    raiz = raiz or raiz_projeto()
    erros: list[str] = []

    for classe in [Produto, Publico, Apresentacao, Cenario, Tendencia]:
        for nome in classe.listar(raiz):
            try:
                classe(nome, raiz)
            except Exception as erro:
                erros.append(f"{classe.__name__}/{nome}: {erro}")

    for grupo in Prompt.listar_grupos(raiz):
        for nome in Prompt.listar(grupo, raiz):
            try:
                Prompt(grupo, nome, raiz)
            except Exception as erro:
                erros.append(f"Prompt/{grupo}/{nome}: {erro}")

    return erros
