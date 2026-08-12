"""Contrato local e payload do Dashboard Financeiro V1.

Este modulo recebe exclusivamente os DataFrames Pandas ja calculados e
validados pelo notebook. Nenhuma consulta ou regra de classificacao financeira
e executada aqui.
"""
from __future__ import annotations

from decimal import Decimal, InvalidOperation
from numbers import Integral
from typing import Any, Iterable

import pandas as pd
from IPython.display import HTML, display

from .visual import render_dashboard


class ErroContratoDashboard(RuntimeError):
    """Falha de contrato entre os resultados financeiros e a interface."""


COLUNAS_RADAR = {
    "NR_TRAN_INST_PCT",
    "CD_CLI",
    "NR_PERIODO",
    "REF_PERIODO",
    "NR_MCA_PCT_OPB",
    "DT_TRAN",
    "CD_NTZ_CTB_TRAN",
    "CD_EST_TRAN_INST",
    "TX_EST_TRAN_INST",
    "CD_GR_CTGR_TRAN",
    "TX_DCR_GR_CTGR",
    "CD_CTGR_TRAN",
    "TX_DCR_CTGR_TRAN",
    "CD_TIP_MOE_CRR",
    "VL_TRAN",
    "TX_DCR_TRAN",
    "CD_CLASSIFICACAO_RADAR",
    "TX_DCR_CLASSIFICACAO_RADAR",
    "FL_AGRO",
    "FL_MOVIMENTACAO_PROPRIA",
}

COLUNAS_ESTUDO_ENTRADAS = {
    "CD_CLI",
    "NR_TRAN_CREDITO",
    "NR_PERIODO",
    "REF_PERIODO",
    "NR_MCA_PCT_OPB",
    "DT_TRAN",
    "CD_TIP_MOE_CRR",
    "VL_TRAN",
    "FL_SANEADO",
    "NIVEL_EVIDENCIA",
    "QT_CANDIDATOS",
    "NR_TRAN_DEBITO_SELECIONADO",
    "DIFERENCA_DIAS",
    "MOTIVO_CLASSIFICACAO",
}

COLUNAS_RESUMO_ENTRADAS = {
    "CD_CLI",
    "NR_PERIODO",
    "REF_PERIODO",
    "CD_TIP_MOE_CRR",
    "QT_ENTRADAS",
    "ENTRADAS_TOTAIS_IDENTIFICADAS",
    "QT_MOVIMENTACOES_PROPRIAS",
    "VALOR_TRANSACAO_PROPRIA",
    "ENTRADAS_TOTAIS_CORRIGIDAS",
}

CHAVES_RESUMO = [
    "CD_CLI",
    "NR_PERIODO",
    "REF_PERIODO",
    "CD_TIP_MOE_CRR",
]


def _exigir_dataframe(nome: str, frame: Any, colunas: Iterable[str]) -> pd.DataFrame:
    if not isinstance(frame, pd.DataFrame):
        raise ErroContratoDashboard(f"{nome} deve ser um DataFrame Pandas.")
    ausentes = sorted(set(colunas) - set(frame.columns))
    if ausentes:
        raise ErroContratoDashboard(
            f"{nome} nao possui as colunas obrigatorias: {', '.join(ausentes)}."
        )
    return frame.copy()


def _decimal_exato(valor: Any, campo: str) -> Decimal:
    if isinstance(valor, bool) or isinstance(valor, float):
        raise ErroContratoDashboard(f"{campo} nao pode usar bool ou float.")
    if isinstance(valor, Decimal):
        resultado = valor
    elif isinstance(valor, Integral):
        resultado = Decimal(int(valor))
    elif isinstance(valor, str):
        try:
            resultado = Decimal(valor.strip())
        except InvalidOperation as exc:
            raise ErroContratoDashboard(f"{campo} possui decimal invalido.") from exc
    else:
        raise ErroContratoDashboard(
            f"{campo} deve ser Decimal, inteiro ou texto decimal exato."
        )
    if not resultado.is_finite():
        raise ErroContratoDashboard(f"{campo} deve ser um decimal finito.")
    if resultado < 0:
        raise ErroContratoDashboard(f"{campo} nao pode ser negativo.")
    return resultado


def _texto(valor: Any) -> str:
    if pd.isna(valor):
        return ""
    return str(valor).strip()


def _inteiro(valor: Any, campo: str) -> int:
    if isinstance(valor, bool) or pd.isna(valor):
        raise ErroContratoDashboard(f"{campo} deve ser um inteiro preenchido.")
    try:
        convertido = int(valor)
    except (TypeError, ValueError) as exc:
        raise ErroContratoDashboard(f"{campo} deve ser inteiro.") from exc
    try:
        if Decimal(str(valor)) != Decimal(convertido):
            raise ErroContratoDashboard(f"{campo} deve ser inteiro.")
    except InvalidOperation as exc:
        raise ErroContratoDashboard(f"{campo} deve ser inteiro.") from exc
    return convertido


def _data_iso(valor: Any, campo: str) -> str:
    try:
        data = pd.Timestamp(valor)
    except (TypeError, ValueError) as exc:
        raise ErroContratoDashboard(f"{campo} possui data invalida.") from exc
    if pd.isna(data):
        raise ErroContratoDashboard(f"{campo} deve estar preenchida.")
    return data.date().isoformat()


def _escala_decimal(valor: Decimal) -> int:
    return max(0, -valor.as_tuple().exponent)


def _unidades(valor: Decimal, escala: int, campo: str) -> str:
    fator = Decimal(10) ** escala
    unidades = valor * fator
    if unidades != unidades.to_integral_value():
        raise ErroContratoDashboard(
            f"{campo} possui casas superiores a escala {escala}."
        )
    return str(int(unidades))


def _somar_decimal(valores: Iterable[Any], campo: str) -> Decimal:
    total = Decimal("0")
    for valor in valores:
        total += _decimal_exato(valor, campo)
    return total


def _registro_por_chave(frame: pd.DataFrame, chaves: list[str]) -> dict[tuple[Any, ...], Any]:
    saida: dict[tuple[Any, ...], Any] = {}
    for linha in frame.to_dict("records"):
        chave = tuple(linha[item] for item in chaves)
        if chave in saida:
            raise ErroContratoDashboard(
                f"Chave duplicada no resumo: {', '.join(chaves)}."
            )
        saida[chave] = linha
    return saida


def _validar_resumo_entradas(
    estudo: pd.DataFrame,
    resumo: pd.DataFrame,
) -> None:
    esperado: dict[tuple[Any, ...], dict[str, Any]] = {}
    for chave, grupo in estudo.groupby(CHAVES_RESUMO, dropna=False, sort=False):
        chave_tupla = chave if isinstance(chave, tuple) else (chave,)
        valores = [_decimal_exato(v, "VL_TRAN") for v in grupo["VL_TRAN"]]
        saneados = grupo[grupo["FL_SANEADO"].eq("S")]
        esperado[chave_tupla] = {
            "QT_ENTRADAS": int(len(grupo)),
            "ENTRADAS_TOTAIS_IDENTIFICADAS": sum(valores, Decimal("0")),
            "QT_MOVIMENTACOES_PROPRIAS": int(len(saneados)),
            "VALOR_TRANSACAO_PROPRIA": _somar_decimal(
                saneados["VL_TRAN"], "VALOR_TRANSACAO_PROPRIA"
            ),
        }

    observado = _registro_por_chave(resumo, CHAVES_RESUMO)
    if set(esperado) != set(observado):
        raise ErroContratoDashboard(
            "df_resumo_entradas diverge do detalhe no grao periodo e moeda."
        )

    for chave, valores_esperados in esperado.items():
        linha = observado[chave]
        identificadas = _decimal_exato(
            linha["ENTRADAS_TOTAIS_IDENTIFICADAS"],
            "ENTRADAS_TOTAIS_IDENTIFICADAS",
        )
        propria = _decimal_exato(
            linha["VALOR_TRANSACAO_PROPRIA"], "VALOR_TRANSACAO_PROPRIA"
        )
        corrigidas = _decimal_exato(
            linha["ENTRADAS_TOTAIS_CORRIGIDAS"],
            "ENTRADAS_TOTAIS_CORRIGIDAS",
        )
        if identificadas != propria + corrigidas:
            raise ErroContratoDashboard(
                "Resumo de entradas nao reconcilia na mesma moeda."
            )
        for campo, esperado_campo in valores_esperados.items():
            observado_campo = linha[campo]
            if campo.startswith("QT_"):
                observado_campo = _inteiro(observado_campo, campo)
            else:
                observado_campo = _decimal_exato(observado_campo, campo)
            if observado_campo != esperado_campo:
                raise ErroContratoDashboard(
                    f"Resumo de entradas diverge no campo {campo}."
                )


def _chave_resumo_normalizada(linha: dict[str, Any]) -> tuple[Any, ...]:
    return (
        _inteiro(linha["CD_CLI"], "CD_CLI"),
        _inteiro(linha["NR_PERIODO"], "NR_PERIODO"),
        _texto(linha["REF_PERIODO"]),
        _texto(linha["CD_TIP_MOE_CRR"]).upper(),
    )


def _validar_creditos_radar(
    radar: pd.DataFrame,
    estudo: pd.DataFrame,
    resumo: pd.DataFrame,
) -> None:
    creditos_radar = radar[
        radar["CD_NTZ_CTB_TRAN"].astype("string").str.strip().str.upper().eq("C")
        & radar["CD_EST_TRAN_INST"].map(
            lambda valor: _inteiro(valor, "CD_EST_TRAN_INST")
        ).eq(0)
    ]

    radar_por_id = {
        str(_inteiro(linha["NR_TRAN_INST_PCT"], "NR_TRAN_INST_PCT")): linha
        for linha in creditos_radar.to_dict("records")
    }
    estudo_por_id = {
        str(_inteiro(linha["NR_TRAN_CREDITO"], "NR_TRAN_CREDITO")): linha
        for linha in estudo.to_dict("records")
    }
    if set(radar_por_id) != set(estudo_por_id):
        raise ErroContratoDashboard(
            "Creditos efetivados divergem entre df_radar e df_estudo_entradas."
        )

    agregado_radar: dict[tuple[Any, ...], dict[str, Any]] = {}
    for id_credito, linha_estudo in estudo_por_id.items():
        linha_radar = radar_por_id[id_credito]
        fl_saneado = _texto(linha_estudo["FL_SANEADO"]).upper()
        if fl_saneado not in {"S", "N"}:
            raise ErroContratoDashboard("FL_SANEADO deve usar somente S ou N.")
        flag_esperada = "S" if fl_saneado == "S" else "N"

        campos_iguais = (
            _inteiro(linha_radar["CD_CLI"], "CD_CLI")
            == _inteiro(linha_estudo["CD_CLI"], "CD_CLI")
            and _inteiro(linha_radar["NR_PERIODO"], "NR_PERIODO")
            == _inteiro(linha_estudo["NR_PERIODO"], "NR_PERIODO")
            and _texto(linha_radar["REF_PERIODO"])
            == _texto(linha_estudo["REF_PERIODO"])
            and _inteiro(linha_radar["NR_MCA_PCT_OPB"], "NR_MCA_PCT_OPB")
            == _inteiro(linha_estudo["NR_MCA_PCT_OPB"], "NR_MCA_PCT_OPB")
            and _data_iso(linha_radar["DT_TRAN"], "DT_TRAN")
            == _data_iso(linha_estudo["DT_TRAN"], "DT_TRAN")
            and _texto(linha_radar["CD_TIP_MOE_CRR"]).upper()
            == _texto(linha_estudo["CD_TIP_MOE_CRR"]).upper()
            and _decimal_exato(linha_radar["VL_TRAN"], "VL_TRAN")
            == _decimal_exato(linha_estudo["VL_TRAN"], "VL_TRAN")
            and _texto(linha_radar["FL_MOVIMENTACAO_PROPRIA"]).upper()
            == flag_esperada
        )
        if not campos_iguais:
            raise ErroContratoDashboard(
                f"Credito {id_credito} diverge entre df_radar e df_estudo_entradas."
            )

        chave = _chave_resumo_normalizada(linha_radar)
        valores = agregado_radar.setdefault(
            chave,
            {
                "QT_ENTRADAS": 0,
                "ENTRADAS_TOTAIS_IDENTIFICADAS": Decimal("0"),
                "QT_MOVIMENTACOES_PROPRIAS": 0,
                "VALOR_TRANSACAO_PROPRIA": Decimal("0"),
                "ENTRADAS_TOTAIS_CORRIGIDAS": Decimal("0"),
            },
        )
        valor = _decimal_exato(linha_radar["VL_TRAN"], "VL_TRAN")
        valores["QT_ENTRADAS"] += 1
        valores["ENTRADAS_TOTAIS_IDENTIFICADAS"] += valor
        if flag_esperada == "S":
            valores["QT_MOVIMENTACOES_PROPRIAS"] += 1
            valores["VALOR_TRANSACAO_PROPRIA"] += valor
        else:
            valores["ENTRADAS_TOTAIS_CORRIGIDAS"] += valor

    resumo_por_chave = {
        _chave_resumo_normalizada(linha): linha
        for linha in resumo.to_dict("records")
    }
    if len(resumo_por_chave) != len(resumo) or set(agregado_radar) != set(resumo_por_chave):
        raise ErroContratoDashboard(
            "Radar, estudo e resumo divergem no grao periodo e moeda."
        )
    for chave, esperado in agregado_radar.items():
        observado = resumo_por_chave[chave]
        for campo, valor_esperado in esperado.items():
            valor_observado = (
                _inteiro(observado[campo], campo)
                if campo.startswith("QT_")
                else _decimal_exato(observado[campo], campo)
            )
            if valor_observado != valor_esperado:
                raise ErroContratoDashboard(
                    f"Radar, estudo e resumo divergem no campo {campo}."
                )

    def totais_cliente_moeda(
        agregados: dict[tuple[Any, ...], dict[str, Any]],
    ) -> dict[tuple[Any, str], dict[str, Any]]:
        totais: dict[tuple[Any, str], dict[str, Any]] = {}
        for chave, valores in agregados.items():
            chave_total = (chave[0], chave[3])
            acumulado = totais.setdefault(
                chave_total,
                {campo: Decimal("0") for campo in valores},
            )
            for campo, valor in valores.items():
                acumulado[campo] += Decimal(valor)
        return totais

    agregado_resumo = {
        chave: {
            campo: (
                _inteiro(linha[campo], campo)
                if campo.startswith("QT_")
                else _decimal_exato(linha[campo], campo)
            )
            for campo in agregado_radar[chave]
        }
        for chave, linha in resumo_por_chave.items()
    }
    if totais_cliente_moeda(agregado_radar) != totais_cliente_moeda(agregado_resumo):
        raise ErroContratoDashboard(
            "Radar, estudo e resumo divergem nos totais do cliente por moeda."
        )


def montar_payload_dashboard(
    df_radar: pd.DataFrame,
    df_estudo_entradas: pd.DataFrame,
    df_resumo_entradas: pd.DataFrame,
    df_periodos_utilizados: pd.DataFrame,
    df_resumo_execucao: pd.DataFrame,
) -> dict[str, Any]:
    """Valida os contratos locais e monta um payload sem recalcular classificacoes."""
    radar = _exigir_dataframe("df_radar", df_radar, COLUNAS_RADAR)
    estudo = _exigir_dataframe(
        "df_estudo_entradas", df_estudo_entradas, COLUNAS_ESTUDO_ENTRADAS
    )
    resumo = _exigir_dataframe(
        "df_resumo_entradas", df_resumo_entradas, COLUNAS_RESUMO_ENTRADAS
    )
    periodos = _exigir_dataframe(
        "df_periodos_utilizados",
        df_periodos_utilizados,
        {
            "CD_CLI",
            "NR_PERIODO",
            "REF_PERIODO",
            "DT_INICIO_PERIODO",
            "DT_FIM_PERIODO",
        },
    )
    execucao = _exigir_dataframe(
        "df_resumo_execucao",
        df_resumo_execucao,
        {
            "CD_CLI",
            "ORIGEM_CD_CLI",
            "PERIODOS_SOLICITADOS",
            "DT_VISUALIZACAO",
            "STATUS_VALIDACAO",
        },
    )

    if radar["NR_TRAN_INST_PCT"].isna().any() or radar["NR_TRAN_INST_PCT"].duplicated().any():
        raise ErroContratoDashboard(
            "NR_TRAN_INST_PCT deve ser unico e preenchido em df_radar."
        )
    if estudo["NR_TRAN_CREDITO"].isna().any() or estudo["NR_TRAN_CREDITO"].duplicated().any():
        raise ErroContratoDashboard(
            "NR_TRAN_CREDITO deve ser unico e preenchido no estudo de entradas."
        )
    if len(execucao) != 1:
        raise ErroContratoDashboard("df_resumo_execucao deve possuir uma linha.")

    _validar_resumo_entradas(estudo, resumo)
    _validar_creditos_radar(radar, estudo, resumo)

    valores_por_moeda: dict[str, list[Decimal]] = {}
    for linha in radar.to_dict("records"):
        moeda = _texto(linha["CD_TIP_MOE_CRR"]).upper()
        if not moeda:
            raise ErroContratoDashboard("Moeda ausente em df_radar.")
        valores_por_moeda.setdefault(moeda, []).append(
            _decimal_exato(linha["VL_TRAN"], "VL_TRAN")
        )

    moedas = sorted(valores_por_moeda)
    escalas = {
        moeda: max(2, *(_escala_decimal(valor) for valor in valores))
        for moeda, valores in valores_por_moeda.items()
    }

    transacoes: list[dict[str, Any]] = []
    transacoes_por_id: dict[str, dict[str, Any]] = {}
    for linha in radar.sort_values(
        ["NR_PERIODO", "DT_TRAN", "NR_TRAN_INST_PCT"], kind="mergesort"
    ).to_dict("records"):
        moeda = _texto(linha["CD_TIP_MOE_CRR"]).upper()
        valor = _decimal_exato(linha["VL_TRAN"], "VL_TRAN")
        id_transacao = str(_inteiro(linha["NR_TRAN_INST_PCT"], "NR_TRAN_INST_PCT"))
        registro = {
            "id_transacao": id_transacao,
            "cd_cli": str(_inteiro(linha["CD_CLI"], "CD_CLI")),
            "nr_periodo": _inteiro(linha["NR_PERIODO"], "NR_PERIODO"),
            "ref_periodo": _texto(linha["REF_PERIODO"]),
            "fonte": str(_inteiro(linha["NR_MCA_PCT_OPB"], "NR_MCA_PCT_OPB")),
            "data": _data_iso(linha["DT_TRAN"], "DT_TRAN"),
            "natureza": _texto(linha["CD_NTZ_CTB_TRAN"]).upper(),
            "estado": _inteiro(linha["CD_EST_TRAN_INST"], "CD_EST_TRAN_INST"),
            "estado_descricao": _texto(linha["TX_EST_TRAN_INST"]),
            "grupo_codigo": str(_inteiro(linha["CD_GR_CTGR_TRAN"], "CD_GR_CTGR_TRAN")),
            "grupo_descricao": _texto(linha["TX_DCR_GR_CTGR"]),
            "categoria_codigo": str(_inteiro(linha["CD_CTGR_TRAN"], "CD_CTGR_TRAN")),
            "categoria_descricao": _texto(linha["TX_DCR_CTGR_TRAN"]),
            "moeda": moeda,
            "valor_unidades": _unidades(valor, escalas[moeda], "VL_TRAN"),
            "descricao": _texto(linha["TX_DCR_TRAN"]),
            "radar_codigo": _inteiro(
                linha["CD_CLASSIFICACAO_RADAR"], "CD_CLASSIFICACAO_RADAR"
            ),
            "radar_descricao": _texto(linha["TX_DCR_CLASSIFICACAO_RADAR"]),
            "fl_agro": _texto(linha["FL_AGRO"]).upper(),
            "fl_movimentacao_propria": _texto(
                linha["FL_MOVIMENTACAO_PROPRIA"]
            ).upper(),
        }
        if registro["natureza"] not in {"C", "D"}:
            raise ErroContratoDashboard("Natureza invalida em df_radar.")
        if registro["fl_movimentacao_propria"] not in {"S", "N"}:
            raise ErroContratoDashboard("Flag de movimentacao propria invalida.")
        transacoes.append(registro)
        transacoes_por_id[id_transacao] = registro

    pares: list[dict[str, Any]] = []
    saneados = estudo[
        estudo["FL_SANEADO"].astype("string").str.strip().str.upper().eq("S")
    ]
    if saneados["NR_TRAN_DEBITO_SELECIONADO"].duplicated().any():
        raise ErroContratoDashboard("Um debito foi selecionado mais de uma vez.")
    for linha in saneados.to_dict("records"):
        credito = str(_inteiro(linha["NR_TRAN_CREDITO"], "NR_TRAN_CREDITO"))
        debito = str(
            _inteiro(
                linha["NR_TRAN_DEBITO_SELECIONADO"],
                "NR_TRAN_DEBITO_SELECIONADO",
            )
        )
        if credito not in transacoes_por_id or debito not in transacoes_por_id:
            raise ErroContratoDashboard(
                "Credito ou debito saneado nao foi encontrado em df_radar."
            )
        registro_credito = transacoes_por_id[credito]
        registro_debito = transacoes_por_id[debito]
        if registro_credito["natureza"] != "C" or registro_debito["natureza"] != "D":
            raise ErroContratoDashboard("Par saneado possui naturezas invalidas.")
        if registro_credito["estado"] != 0 or registro_debito["estado"] != 0:
            raise ErroContratoDashboard("Par saneado deve possuir estado 0 nos dois lados.")
        if registro_credito["cd_cli"] != registro_debito["cd_cli"]:
            raise ErroContratoDashboard("Par saneado deve pertencer ao mesmo cliente.")
        if registro_credito["moeda"] != registro_debito["moeda"]:
            raise ErroContratoDashboard("Par saneado deve possuir a mesma moeda.")
        if registro_credito["valor_unidades"] != registro_debito["valor_unidades"]:
            raise ErroContratoDashboard("Par saneado deve possuir o mesmo valor exato.")
        if registro_credito["fonte"] == registro_debito["fonte"]:
            raise ErroContratoDashboard("Par saneado deve utilizar fontes diferentes.")
        if (
            registro_credito["fl_movimentacao_propria"] != "S"
            or registro_debito["fl_movimentacao_propria"] != "S"
        ):
            raise ErroContratoDashboard(
                "Credito e debito saneados devem estar marcados como movimentacao propria."
            )

        diferenca_dias = _inteiro(linha["DIFERENCA_DIAS"], "DIFERENCA_DIAS")
        diferenca_observada = abs(
            (
                pd.Timestamp(registro_credito["data"])
                - pd.Timestamp(registro_debito["data"])
            ).days
        )
        if diferenca_dias not in {0, 1, 2, 3} or diferenca_dias != diferenca_observada:
            raise ErroContratoDashboard(
                "DIFERENCA_DIAS nao corresponde as datas do par saneado."
            )
        evidencia_esperada = "MUITO_FORTE" if diferenca_dias == 0 else "FORTE"
        motivo_esperado = (
            "MATCH_MESMO_DIA" if diferenca_dias == 0 else f"MATCH_{diferenca_dias}_DIA"
            + ("S" if diferenca_dias > 1 else "")
        )
        nivel_evidencia = _texto(linha["NIVEL_EVIDENCIA"])
        motivo = _texto(linha["MOTIVO_CLASSIFICACAO"])
        if nivel_evidencia != evidencia_esperada or motivo != motivo_esperado:
            raise ErroContratoDashboard(
                "Evidencia ou motivo nao corresponde a diferenca de dias do par."
            )
        qt_candidatos = _inteiro(linha["QT_CANDIDATOS"], "QT_CANDIDATOS")
        if qt_candidatos < 1:
            raise ErroContratoDashboard(
                "Credito saneado deve registrar ao menos um candidato disponivel."
            )
        pares.append(
            {
                "credito_id": credito,
                "debito_id": debito,
                "nivel_evidencia": nivel_evidencia,
                "qt_candidatos": qt_candidatos,
                "diferenca_dias": diferenca_dias,
                "motivo": motivo,
            }
        )

    ids_creditos_saneados = {item["credito_id"] for item in pares}
    ids_debitos_selecionados = {item["debito_id"] for item in pares}
    ids_marcados_radar = {
        item["id_transacao"]
        for item in transacoes
        if item["fl_movimentacao_propria"] == "S"
    }
    if ids_marcados_radar != ids_creditos_saneados | ids_debitos_selecionados:
        raise ErroContratoDashboard(
            "Flags de movimentacao propria divergem dos pares selecionados."
        )

    resumo_payload: list[dict[str, Any]] = []
    for linha in resumo.sort_values(
        ["NR_PERIODO", "CD_TIP_MOE_CRR"], kind="mergesort"
    ).to_dict("records"):
        moeda = _texto(linha["CD_TIP_MOE_CRR"]).upper()
        if moeda not in escalas:
            raise ErroContratoDashboard(
                "Resumo de entradas possui moeda sem transacao observada."
            )
        escala = escalas[moeda]
        resumo_payload.append(
            {
                "cd_cli": str(_inteiro(linha["CD_CLI"], "CD_CLI")),
                "nr_periodo": _inteiro(linha["NR_PERIODO"], "NR_PERIODO"),
                "ref_periodo": _texto(linha["REF_PERIODO"]),
                "moeda": moeda,
                "qt_entradas": _inteiro(linha["QT_ENTRADAS"], "QT_ENTRADAS"),
                "entradas_identificadas_unidades": _unidades(
                    _decimal_exato(
                        linha["ENTRADAS_TOTAIS_IDENTIFICADAS"],
                        "ENTRADAS_TOTAIS_IDENTIFICADAS",
                    ),
                    escala,
                    "ENTRADAS_TOTAIS_IDENTIFICADAS",
                ),
                "qt_movimentacoes_proprias": _inteiro(
                    linha["QT_MOVIMENTACOES_PROPRIAS"],
                    "QT_MOVIMENTACOES_PROPRIAS",
                ),
                "movimentacao_propria_unidades": _unidades(
                    _decimal_exato(
                        linha["VALOR_TRANSACAO_PROPRIA"],
                        "VALOR_TRANSACAO_PROPRIA",
                    ),
                    escala,
                    "VALOR_TRANSACAO_PROPRIA",
                ),
                "entradas_corrigidas_unidades": _unidades(
                    _decimal_exato(
                        linha["ENTRADAS_TOTAIS_CORRIGIDAS"],
                        "ENTRADAS_TOTAIS_CORRIGIDAS",
                    ),
                    escala,
                    "ENTRADAS_TOTAIS_CORRIGIDAS",
                ),
            }
        )

    controles: list[dict[str, Any]] = []
    combinacoes: set[tuple[int | None, str | None, str]] = set()
    for item in transacoes:
        combinacoes.update(
            {
                (item["nr_periodo"], item["fonte"], item["moeda"]),
                (item["nr_periodo"], None, item["moeda"]),
                (None, item["fonte"], item["moeda"]),
                (None, None, item["moeda"]),
            }
        )
    for periodo, fonte, moeda in sorted(
        combinacoes,
        key=lambda item: (
            item[2],
            -1 if item[0] is None else item[0],
            "" if item[1] is None else item[1],
        ),
    ):
        recorte = [
            item
            for item in transacoes
            if item["moeda"] == moeda
            and (periodo is None or item["nr_periodo"] == periodo)
            and (fonte is None or item["fonte"] == fonte)
        ]
        creditos = [item for item in recorte if item["natureza"] == "C" and item["estado"] == 0]
        proprios_credito = [
            item for item in creditos if item["fl_movimentacao_propria"] == "S"
        ]
        corrigidos = [
            item for item in creditos if item["fl_movimentacao_propria"] == "N"
        ]
        saidas = [
            item
            for item in recorte
            if item["natureza"] == "D"
            and item["estado"] == 0
            and item["fl_movimentacao_propria"] == "N"
        ]
        soma = lambda itens: sum((int(item["valor_unidades"]) for item in itens), 0)
        identificadas = soma(creditos)
        propria = soma(proprios_credito)
        corrigida = soma(corrigidos)
        if identificadas != propria + corrigida:
            raise ErroContratoDashboard(
                "Reconciliacao por filtros falhou para entradas."
            )
        controles.append(
            {
                "nr_periodo": periodo,
                "fonte": fonte,
                "moeda": moeda,
                "qt_identificadas": len(creditos),
                "entradas_identificadas_unidades": str(identificadas),
                "qt_proprias": len(proprios_credito),
                "movimentacao_propria_unidades": str(propria),
                "qt_corrigidas": len(corrigidos),
                "entradas_corrigidas_unidades": str(corrigida),
                "qt_saidas": len(saidas),
                "saidas_analisadas_unidades": str(soma(saidas)),
            }
        )

    periodos_payload = [
        {
            "nr_periodo": _inteiro(linha["NR_PERIODO"], "NR_PERIODO"),
            "ref_periodo": _texto(linha["REF_PERIODO"]),
            "inicio": _data_iso(linha["DT_INICIO_PERIODO"], "DT_INICIO_PERIODO"),
            "fim": _data_iso(linha["DT_FIM_PERIODO"], "DT_FIM_PERIODO"),
        }
        for linha in periodos.sort_values("NR_PERIODO", kind="mergesort").to_dict("records")
    ]
    linha_execucao = execucao.iloc[0]
    fontes = sorted({item["fonte"] for item in transacoes}, key=lambda x: int(x))
    moeda_inicial = "BRL" if "BRL" in moedas else (moedas[0] if moedas else None)

    return {
        "versao": "1.0",
        "contexto": {
            "cd_cli": str(_inteiro(linha_execucao["CD_CLI"], "CD_CLI")),
            "origem_cd_cli": _texto(linha_execucao["ORIGEM_CD_CLI"]),
            "periodos_solicitados": _inteiro(
                linha_execucao["PERIODOS_SOLICITADOS"],
                "PERIODOS_SOLICITADOS",
            ),
            "data_visualizacao": _data_iso(
                linha_execucao["DT_VISUALIZACAO"], "DT_VISUALIZACAO"
            ),
            "status": _texto(linha_execucao["STATUS_VALIDACAO"]),
            "sem_movimentacoes": not bool(transacoes),
        },
        "periodos": periodos_payload,
        "fontes": fontes,
        "moedas": [
            {"codigo": moeda, "escala": escalas[moeda]} for moeda in moedas
        ],
        "filtros_iniciais": {
            "periodo": None,
            "fonte": None,
            "moeda": moeda_inicial,
            "populacao": "ENTRADAS",
            "visao": "RADAR",
        },
        "transacoes": transacoes,
        "pares_movimentacao_propria": pares,
        "resumo_entradas": resumo_payload,
        "controles": controles,
    }


def fluxo_dashboard(
    df_radar: pd.DataFrame,
    df_estudo_entradas: pd.DataFrame,
    df_resumo_entradas: pd.DataFrame,
    df_periodos_utilizados: pd.DataFrame,
    df_resumo_execucao: pd.DataFrame,
    exibir: bool = True,
) -> dict[str, Any]:
    """Monta e, opcionalmente, exibe o dashboard no Jupyter."""
    payload = montar_payload_dashboard(
        df_radar,
        df_estudo_entradas,
        df_resumo_entradas,
        df_periodos_utilizados,
        df_resumo_execucao,
    )
    html = render_dashboard(payload)
    if exibir:
        display(HTML(html))
    return {"payload": payload, "html": html}


__all__ = [
    "ErroContratoDashboard",
    "montar_payload_dashboard",
    "fluxo_dashboard",
]
