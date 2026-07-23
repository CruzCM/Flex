"""Leitura de YAML, validacao simples e placeholders."""

from __future__ import annotations

import re
import textwrap
from pathlib import Path
from typing import Any, Optional, Union

import yaml


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


def limpar_texto(texto: Any) -> Any:
    if not isinstance(texto, str):
        return texto

    return textwrap.dedent(texto).strip()


def listar_yaml(pasta: Union[str, Path], raiz: Optional[Path] = None) -> list[str]:
    diretorio = (raiz or raiz_projeto()) / Path(pasta)

    if not diretorio.exists():
        return []

    return sorted(arquivo.stem for arquivo in diretorio.glob("*.yaml"))


def carregar_yaml(
    pasta: Union[str, Path],
    nome: str,
    raiz: Optional[Path] = None,
) -> dict[str, Any]:
    arquivo = (raiz or raiz_projeto()) / Path(pasta) / f"{nome}.yaml"

    if not arquivo.exists():
        raise FileNotFoundError(f"Arquivo nao encontrado: {arquivo}")

    with arquivo.open(encoding="utf-8") as stream:
        dados = yaml.safe_load(stream)

    if dados is None:
        dados = {}

    if not isinstance(dados, dict):
        raise ValueError(f"YAML invalido: {arquivo}")

    return {chave: limpar_texto(valor) for chave, valor in dados.items()}


def validar_campos(
    dados: dict[str, Any],
    obrigatorios: tuple[str, ...],
    origem: str,
) -> None:
    faltantes = [campo for campo in obrigatorios if campo not in dados]

    if faltantes:
        raise ValueError(
            f"{origem} sem campos obrigatorios: "
            + ", ".join(faltantes)
        )


def placeholders(texto: str) -> list[str]:
    if not isinstance(texto, str):
        return []

    return sorted(set(re.findall(r"\{\{?(PH_[A-Z0-9_]+)\}\}?", texto)))


def preencher(texto: str, valores: dict[str, Any]) -> str:
    faltantes = [
        chave
        for chave in placeholders(texto)
        if chave not in valores
    ]

    if faltantes:
        raise ValueError("Placeholders sem valor: " + ", ".join(faltantes))

    saida = texto

    for chave, valor in valores.items():
        valor_texto = "" if valor is None else str(valor)
        saida = saida.replace(f"{{{{{chave}}}}}", valor_texto)
        saida = saida.replace(f"{{{chave}}}", valor_texto)

    return saida


def rotulo(nome: str) -> str:
    return nome.replace("_", " ").title()
