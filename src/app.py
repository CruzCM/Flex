"""Orquestracao do dashboard ANA_EDU_FIN_CLI no Jupyter."""

from __future__ import annotations

import re
from numbers import Integral
from typing import Any
from uuid import uuid4

import pandas as pd
from IPython import get_ipython
from IPython.display import HTML, display

from .visual import render_dashboard


COLUNAS_DASHBOARD = (
    "CD_CLI",
    "TS_ATL_TRAN",
    "DD_INC_MM_CLC_BLC",
    "VL_REN_PRES",
    "CD_MAC_PRFL_CLI",
    "NM_MAC_PRFL_CLI",
    "CD_MIC_PRFL_CLI",
    "NM_MIC_PRFL_CLI",
    "NM_PRFL_FIN",
    "DT_REF_INI",
    "DT_REF_FIM",
    "DT_MES_EXEA",
    "DT_EXEA",
    "QT_TRANS_TOTAL",
    "QT_TRANS_ENT",
    "QT_TRANS_SAI",
    "VL_TRANS_ENT",
    "VL_TRANS_SAI",
    "VL_ENT_REN",
    "VL_ENT_EST",
    "VL_ENT_RESG",
    "VL_ENT_OUT",
    "VL_ENT_CRED",
    "VL_ENT_TOTAL",
    "VL_SAI_IND",
    "VL_SAI_ESS",
    "VL_SAI_FLEX",
    "VL_SAI_FUT",
    "VL_SAI_OBR",
    "VL_SAI_TOTAL",
    "VL_RES_ORC",
    "PC_SAI_ENT",
    "CD_RES_ORC",
    "TX_RES_ORC",
    "CD_FAIXA_ORC",
    "TX_STS_RES",
    "TX_STS_FINAL",
    "PC_SAI_IND",
    "PC_SAI_ESS",
    "PC_SAI_FLEX",
    "PC_SAI_FUT",
    "PC_SAI_OBR",
    "PC_REF_IND",
    "PC_REF_ESS",
    "PC_REF_FLEX",
    "PC_REF_FUT",
    "PC_REF_OBR",
    "NR_PONT_CONC_IND",
    "NR_PONT_CONC_ESS",
    "NR_PONT_CONC_FLEX",
    "NR_PONT_CONC_FUT",
    "NR_PONT_CONC_OBR",
    "NR_PONT_ORC_IND",
    "NR_PONT_ORC_ESS",
    "NR_PONT_ORC_FLEX",
    "NR_PONT_ORC_FUT",
    "NR_PONT_ORC_OBR",
    "NR_PONT_PRFL_IND",
    "NR_PONT_PRFL_ESS",
    "NR_PONT_PRFL_FLEX",
    "NR_PONT_PRFL_FUT",
    "NR_PONT_PRFL_OBR",
    "NR_PONT_IND_FIM",
    "NR_PONT_ESS_FIM",
    "NR_PONT_FLEX_FIM",
    "NR_PONT_FUT_FIM",
    "NR_PONT_OBR_FIM",
    "CD_TEMA_VENCEDOR",
    "TX_TEMA_VENCEDOR",
    "FL_TEM_MOV_AGRO",
    "FL_PARTICIPA_RADAR",
)


_IDENTIFICADOR_SQL = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")


class ErroDashboard(RuntimeError):
    """Erro de parametro, consulta ou contrato do dashboard."""


def _normalizar_identificador(valor: Any, nome: str) -> str:
    texto = str(valor or "").strip()
    if not texto or not _IDENTIFICADOR_SQL.fullmatch(texto):
        raise ErroDashboard(
            f"{nome} inválido: use apenas letras, números e sublinhado, "
            "iniciando por letra ou sublinhado."
        )
    return texto


def _normalizar_codigo_cliente(valor: Any) -> int | None:
    if valor is None:
        return None
    if isinstance(valor, str):
        texto = valor.strip()
        if not texto:
            return None
        if not texto.isdecimal():
            raise ErroDashboard("codigo_cliente deve ser um número inteiro positivo.")
        codigo = int(texto)
    elif isinstance(valor, bool) or not isinstance(valor, Integral):
        raise ErroDashboard("codigo_cliente deve ser um número inteiro positivo.")
    else:
        codigo = int(valor)

    if not 1 <= codigo <= 999_999_999:
        raise ErroDashboard("codigo_cliente deve estar entre 1 e 999999999.")
    return codigo


def _ipython_com_spark_magic():
    ipython = get_ipython()
    if ipython is None:
        raise ErroDashboard(
            "O dashboard deve ser executado dentro do notebook Jupyter."
        )
    localizar_magic = getattr(ipython, "find_cell_magic", None)
    if not callable(localizar_magic) or localizar_magic("spark") is None:
        raise ErroDashboard(
            "A cell magic %%spark não está disponível. "
            "Execute primeiro a célula de conexão Spark do notebook."
        )
    return ipython


def _executar_sql_pandas(sql: str, maximo_linhas: int) -> pd.DataFrame:
    ipython = _ipython_com_spark_magic()
    nome_variavel = f"_radar_dashboard_{uuid4().hex}"
    ipython.user_ns.pop(nome_variavel, None)
    argumentos = f"-c sql -q -n {int(maximo_linhas)} -o {nome_variavel}"

    try:
        retorno = ipython.run_cell_magic("spark", argumentos, sql)
        frame = ipython.user_ns.get(nome_variavel)
        if frame is None and isinstance(retorno, pd.DataFrame):
            frame = retorno
        if not isinstance(frame, pd.DataFrame):
            raise ErroDashboard(
                "A consulta Spark não retornou um DataFrame Pandas para o kernel local."
            )
        resultado = frame.copy()
        resultado.columns = [str(coluna).upper() for coluna in resultado.columns]
        return resultado
    except ErroDashboard:
        raise
    except Exception as exc:
        raise ErroDashboard(
            "Falha ao consultar a tabela pelo Spark. "
            "Verifique a sessão, a permissão e o nome informado."
        ) from exc
    finally:
        ipython.user_ns.pop(nome_variavel, None)


def _nome_tabela_sql(schema: str, tabela: str) -> str:
    return f"`{schema}`.`{tabela}`"


def _selecionar_cliente_aleatorio(tabela_sql: str) -> int:
    consulta = f"""
SELECT CD_CLI
FROM {tabela_sql}
WHERE CD_CLI IS NOT NULL
ORDER BY RAND()
LIMIT 1
""".strip()
    frame = _executar_sql_pandas(consulta, maximo_linhas=1)
    if frame.empty or "CD_CLI" not in frame.columns:
        raise ErroDashboard("A tabela não possui clientes disponíveis para seleção.")
    try:
        codigo = int(frame.iloc[0]["CD_CLI"])
    except (TypeError, ValueError, OverflowError) as exc:
        raise ErroDashboard("O CD_CLI selecionado pela tabela é inválido.") from exc
    if not 1 <= codigo <= 999_999_999:
        raise ErroDashboard("O CD_CLI selecionado está fora do domínio esperado.")
    return codigo


def _consultar_registro(
    codigo_cliente: int,
    schema: str,
    tabela: str,
) -> dict[str, Any]:
    tabela_sql = _nome_tabela_sql(schema, tabela)
    colunas_sql = ",\n    ".join(COLUNAS_DASHBOARD)
    consulta = f"""
SELECT
    {colunas_sql}
FROM {tabela_sql}
WHERE CD_CLI = {codigo_cliente}
LIMIT 2
""".strip()
    frame = _executar_sql_pandas(consulta, maximo_linhas=2)

    ausentes = [coluna for coluna in COLUNAS_DASHBOARD if coluna not in frame.columns]
    if ausentes:
        raise ErroDashboard(
            "A tabela não atende ao contrato de 71 campos. "
            f"Campos ausentes: {', '.join(ausentes)}."
        )
    if frame.empty:
        raise ErroDashboard(
            f"Cliente {codigo_cliente} não encontrado em {schema}.{tabela}."
        )
    if len(frame) > 1:
        raise ErroDashboard(
            f"Cliente {codigo_cliente} possui mais de uma linha em {schema}.{tabela}."
        )
    return frame.loc[:, list(COLUNAS_DASHBOARD)].iloc[0].to_dict()


def gerar_dashboard(
    codigo_cliente: Any = None,
    schema: str = "sbx_t2i2016",
    tabela: str = "ana_edu_fin_cli",
    exibir: bool = True,
) -> dict[str, Any]:
    """Consulta um cliente e exibe sua visão única na saída do notebook."""
    schema_normalizado = _normalizar_identificador(schema, "schema")
    tabela_normalizada = _normalizar_identificador(tabela, "tabela")
    codigo_normalizado = _normalizar_codigo_cliente(codigo_cliente)
    origem_cliente = "informado"

    if codigo_normalizado is None:
        origem_cliente = "aleatorio"
        codigo_normalizado = _selecionar_cliente_aleatorio(
            _nome_tabela_sql(schema_normalizado, tabela_normalizada)
        )

    registro = _consultar_registro(
        codigo_normalizado,
        schema_normalizado,
        tabela_normalizada,
    )
    html_dashboard = render_dashboard(registro)
    if exibir:
        display(HTML(html_dashboard))

    return {
        "codigo_cliente": codigo_normalizado,
        "origem_cliente": origem_cliente,
        "tabela": f"{schema_normalizado}.{tabela_normalizada}",
        "dados": registro,
        "html": html_dashboard,
    }


__all__ = [
    "COLUNAS_DASHBOARD",
    "ErroDashboard",
    "gerar_dashboard",
]
