%%spark

# ============================================================
# ESTUDO EXPLORATÓRIO INICIAL
# PARTICIPAÇÃO NO RADAR
#
# OBJETIVO
# ------------------------------------------------------------
# Produzir uma visão global dos clientes que:
#   1. participam do Radar;
#   2. não participam do Radar;
#   3. possuem ou não perfil apto;
#   4. atendem ou não aos requisitos transacionais;
#   5. possuem ou não movimentação Agro.
#
# O bloco também:
#   - recalcula a regra oficial de participação;
#   - valida o resultado contra FL_PARTICIPA_RADAR;
#   - constrói um funil acumulado;
#   - apresenta motivos sobrepostos, exclusivos e combinados;
#   - compara o comportamento transacional dos grupos;
#   - calcula distribuições, percentis e outliers;
#   - gera tabelas e gráficos prontos para apresentação.
# ============================================================

from pathlib import Path

from pyspark.sql import functions as F
from pyspark.sql import Window
from pyspark.storagelevel import StorageLevel

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from tabulate import tabulate


# ============================================================
# 00 CONFIGURAÇÕES
# ============================================================

TABELA = "sbx_t2i2016.v1_ana_edu_fin_cli"

LINHAS_TABELA = 100
TOP_COMBINACOES = 15

SALVAR_GRAFICOS = False
PASTA_GRAFICOS = Path("graficos_estudo_radar")

if SALVAR_GRAFICOS:
    PASTA_GRAFICOS.mkdir(
        parents=True,
        exist_ok=True
    )

plt.rcParams.update({
    "figure.figsize": (12, 6),
    "axes.titlesize": 14,
    "axes.labelsize": 11,
    "xtick.labelsize": 10,
    "ytick.labelsize": 10
})


# ============================================================
# 01 FUNÇÕES PADRÃO
# ============================================================

def formatar_inteiro(valor):
    """
    Formata números inteiros no padrão brasileiro.
    """

    if valor is None:
        return "0"

    return (
        f"{int(round(valor)):,}"
        .replace(",", ".")
    )


def formatar_decimal(
    valor,
    casas=2
):
    """
    Formata números decimais no padrão brasileiro.
    """

    if valor is None:
        return "0,00"

    texto = f"{float(valor):,.{casas}f}"

    return (
        texto
        .replace(",", "X")
        .replace(".", ",")
        .replace("X", ".")
    )


def formatar_percentual(
    valor,
    casas=2
):
    """
    Formata percentuais.
    """

    return (
        f"{float(valor or 0):.{casas}f}%"
        .replace(".", ",")
    )


def mostrar_tabela(
    titulo,
    sdf,
    linhas=LINHAS_TABELA
):
    """
    Exibe um Spark DataFrame agregado no padrão tabular do estudo.
    """

    print("\n")
    print("=" * 120)
    print(titulo)
    print("=" * 120)

    pdf = (
        sdf
        .limit(linhas)
        .toPandas()
    )

    print(
        tabulate(
            pdf,
            headers="keys",
            tablefmt="psql",
            showindex=False
        )
    )

    print(
        f"\nTotal de linhas exibidas: "
        f"{formatar_inteiro(len(pdf))}"
    )

    return pdf


def insight(
    titulo,
    texto
):
    """
    Exibe uma conclusão textual imediatamente após a análise.
    """

    print("\n")
    print("=" * 120)
    print(f"INSIGHT | {titulo}")
    print("=" * 120)
    print(texto.strip())


def publicar_grafico(
    nome
):
    """
    Publica o gráfico no notebook e, opcionalmente, salva em PNG.
    """

    figura = plt.gcf()

    figura.tight_layout()

    if SALVAR_GRAFICOS:

        caminho = (
            PASTA_GRAFICOS
            /
            f"{nome}.png"
        )

        figura.savefig(
            caminho,
            dpi=180,
            bbox_inches="tight"
        )

        print(
            f"Gráfico salvo em: {caminho}"
        )

    plt.show()
    plt.close(figura)


def adicionar_rotulos_barras(
    eixo,
    percentual=False,
    casas=1
):
    """
    Adiciona rótulos às barras verticais ou horizontais.
    """

    for container in eixo.containers:

        rotulos = []

        for barra in container:

            valor = (
                barra.get_width()
                if barra.get_width() != 0
                else barra.get_height()
            )

            if percentual:
                rotulo = f"{valor:.{casas}f}%"
            else:
                rotulo = formatar_inteiro(valor)

            rotulos.append(rotulo)

        try:
            eixo.bar_label(
                container,
                labels=rotulos,
                padding=3,
                fontsize=9
            )
        except Exception:
            pass


def grafico_barra_horizontal(
    pdf,
    coluna_rotulo,
    coluna_valor,
    titulo,
    nome,
    coluna_percentual=None,
    inverter=True
):
    """
    Gráfico de barras horizontais.
    """

    dados = (
        pdf
        .copy()
        .sort_values(
            coluna_valor,
            ascending=False
        )
    )

    figura, eixo = plt.subplots(
        figsize=(12, 6)
    )

    barras = eixo.barh(
        dados[coluna_rotulo],
        dados[coluna_valor]
    )

    eixo.set_title(titulo)
    eixo.set_xlabel("Quantidade de clientes")

    maior_valor = (
        float(dados[coluna_valor].max())
        if len(dados) > 0
        else 0
    )

    for indice, barra in enumerate(barras):

        valor = float(
            dados.iloc[indice][coluna_valor]
        )

        if coluna_percentual:

            percentual = float(
                dados.iloc[indice][coluna_percentual]
            )

            rotulo = (
                f"{formatar_inteiro(valor)} "
                f"({formatar_percentual(percentual)})"
            )

        else:

            rotulo = formatar_inteiro(valor)

        eixo.text(
            valor + maior_valor * 0.01,
            barra.get_y() + barra.get_height() / 2,
            rotulo,
            va="center",
            fontsize=9
        )

    if maior_valor > 0:
        eixo.set_xlim(
            0,
            maior_valor * 1.28
        )

    if inverter:
        eixo.invert_yaxis()

    publicar_grafico(nome)


def grafico_rosca(
    pdf,
    coluna_rotulo,
    coluna_valor,
    titulo,
    nome
):
    """
    Gráfico de rosca.
    """

    figura, eixo = plt.subplots(
        figsize=(8, 8)
    )

    eixo.pie(
        pdf[coluna_valor],
        labels=pdf[coluna_rotulo],
        autopct="%1.1f%%",
        startangle=90,
        wedgeprops={
            "width": 0.45
        }
    )

    eixo.set_title(titulo)

    publicar_grafico(nome)


def grafico_funil(
    pdf,
    titulo,
    nome
):
    """
    Funil acumulado das regras de participação.
    """

    dados = (
        pdf
        .sort_values(
            "ORDEM",
            ascending=False
        )
        .copy()
    )

    figura, eixo = plt.subplots(
        figsize=(13, 7)
    )

    barras = eixo.barh(
        dados["ETAPA"],
        dados["QT_CLIENTES"]
    )

    eixo.set_title(titulo)
    eixo.set_xlabel("Quantidade de clientes")

    maior_valor = float(
        dados["QT_CLIENTES"].max()
    )

    for indice, barra in enumerate(barras):

        quantidade = float(
            dados.iloc[indice]["QT_CLIENTES"]
        )

        percentual = float(
            dados.iloc[indice]["PC_BASE"]
        )

        perda = float(
            dados.iloc[indice]["PERDA_ETAPA"]
        )

        rotulo = (
            f"{formatar_inteiro(quantidade)} "
            f"({formatar_percentual(percentual)})"
        )

        eixo.text(
            quantidade + maior_valor * 0.01,
            barra.get_y() + barra.get_height() / 2,
            rotulo,
            va="center",
            fontsize=9
        )

        if perda > 0:

            eixo.text(
                quantidade * 0.50,
                barra.get_y() + barra.get_height() / 2,
                f"-{formatar_inteiro(perda)}",
                ha="center",
                va="center",
                fontsize=8
            )

    publicar_grafico(nome)


def grafico_barras_agrupadas(
    pdf,
    coluna_indice,
    coluna_grupo,
    coluna_valor,
    titulo,
    nome,
    eixo_y="Quantidade"
):
    """
    Gráfico de barras agrupadas a partir de uma tabela longa.
    """

    pivot = (
        pdf
        .pivot(
            index=coluna_indice,
            columns=coluna_grupo,
            values=coluna_valor
        )
        .fillna(0)
    )

    eixo = pivot.plot(
        kind="bar",
        figsize=(12, 6)
    )

    eixo.set_title(titulo)
    eixo.set_xlabel("")
    eixo.set_ylabel(eixo_y)

    plt.xticks(
        rotation=0
    )

    for container in eixo.containers:

        rotulos = [
            formatar_decimal(
                barra.get_height(),
                1
            )
            for barra in container
        ]

        eixo.bar_label(
            container,
            labels=rotulos,
            padding=3,
            fontsize=8
        )

    publicar_grafico(nome)


def grafico_barras_empilhadas(
    pdf,
    coluna_indice,
    coluna_grupo,
    coluna_valor,
    titulo,
    nome,
    percentual=False
):
    """
    Gráfico de barras empilhadas.
    """

    pivot = (
        pdf
        .pivot(
            index=coluna_indice,
            columns=coluna_grupo,
            values=coluna_valor
        )
        .fillna(0)
    )

    if percentual:

        denominador = (
            pivot
            .sum(axis=1)
            .replace(0, np.nan)
        )

        pivot = (
            pivot
            .div(
                denominador,
                axis=0
            )
            .fillna(0)
            *
            100
        )

    eixo = pivot.plot(
        kind="bar",
        stacked=True,
        figsize=(12, 6)
    )

    eixo.set_title(titulo)
    eixo.set_xlabel("")
    eixo.set_ylabel(
        "Percentual"
        if percentual
        else "Quantidade de clientes"
    )

    plt.xticks(
        rotation=0
    )

    if percentual:

        for container in eixo.containers:

            rotulos = [
                (
                    f"{barra.get_height():.1f}%"
                    if barra.get_height() >= 3
                    else ""
                )
                for barra in container
            ]

            eixo.bar_label(
                container,
                labels=rotulos,
                label_type="center",
                fontsize=8
            )

    publicar_grafico(nome)


def criar_tabela_frequencia(
    sdf,
    coluna,
    total,
    nome_coluna="CATEGORIA"
):
    """
    Cria tabela de quantidade e percentual para uma variável.
    """

    return (

        sdf

        .groupBy(
            coluna
        )

        .agg(
            F.count("*")
            .alias("QT_CLIENTES")
        )

        .withColumn(
            "PC_CLIENTES",
            F.round(
                F.col("QT_CLIENTES")
                /
                F.lit(total)
                *
                100,
                2
            )
        )

        .withColumnRenamed(
            coluna,
            nome_coluna
        )

        .orderBy(
            F.desc("QT_CLIENTES")
        )

    )


# ============================================================
# 02 CARGA E VALIDAÇÃO DAS COLUNAS
# ============================================================

colunas_necessarias = [

    "CD_CLI",

    "QT_TRANS_TOTAL",
    "QT_TRANS_ENT",
    "QT_TRANS_SAI",

    "VL_TRANS_ENT",
    "VL_TRANS_SAI",

    "NM_PRFL",
    "NM_MAC_PRFL_CLI",
    "NM_MIC_PRFL_CLI",
    "NM_PRFL_FIN",

    "FL_TEM_MOV_AGRO",
    "FL_PARTICIPA_RADAR",

    "DT_EXEA",
    "DT_MES_EXEA",
    "DT_REF_INI",
    "DT_REF_FIM"

]

df_origem = spark.table(
    TABELA
)

colunas_ausentes = sorted(
    set(colunas_necessarias)
    -
    set(df_origem.columns)
)

if colunas_ausentes:

    raise ValueError(
        "As seguintes colunas obrigatórias não foram encontradas: "
        +
        ", ".join(colunas_ausentes)
    )

df_base = (

    df_origem

    .select(
        *colunas_necessarias
    )

)


# ============================================================
# 03 REGRA OFICIAL DO RADAR
# ============================================================

def texto_valido_perfil(
    coluna
):
    """
    A regra oficial aceita qualquer conteúdo diferente de
    A CLASSIFICAR. Portanto, SEM PERFIL permanece aceito,
    reproduzindo exatamente o processamento oficial.
    """

    return (
        F.upper(
            F.trim(
                F.coalesce(
                    F.col(coluna),
                    F.lit("A CLASSIFICAR")
                )
            )
        )
        !=
        F.lit("A CLASSIFICAR")
    )


regra_qt_total = (
    F.coalesce(
        F.col("QT_TRANS_TOTAL"),
        F.lit(0)
    )
    >
    0
)

regra_qt_entrada = (
    F.coalesce(
        F.col("QT_TRANS_ENT"),
        F.lit(0)
    )
    >
    0
)

regra_qt_saida = (
    F.coalesce(
        F.col("QT_TRANS_SAI"),
        F.lit(0)
    )
    >
    0
)

regra_vl_entrada = (
    F.coalesce(
        F.col("VL_TRANS_ENT"),
        F.lit(0)
    )
    >
    0
)

regra_vl_saida = (
    F.coalesce(
        F.col("VL_TRANS_SAI"),
        F.lit(0)
    )
    >
    0
)

regra_nm_prfl = texto_valido_perfil(
    "NM_PRFL"
)

regra_nm_macro = texto_valido_perfil(
    "NM_MAC_PRFL_CLI"
)

regra_nm_micro = texto_valido_perfil(
    "NM_MIC_PRFL_CLI"
)

regra_nm_fin = texto_valido_perfil(
    "NM_PRFL_FIN"
)

regra_perfil_apto = (
    regra_nm_prfl
    &
    regra_nm_macro
    &
    regra_nm_micro
    &
    regra_nm_fin
)

regra_sem_agro = (
    F.upper(
        F.trim(
            F.coalesce(
                F.col("FL_TEM_MOV_AGRO"),
                F.lit("N")
            )
        )
    )
    ==
    F.lit("N")
)

regra_transacional = (
    regra_qt_total
    &
    regra_qt_entrada
    &
    regra_qt_saida
    &
    regra_vl_entrada
    &
    regra_vl_saida
)

regra_radar = (
    regra_transacional
    &
    regra_perfil_apto
    &
    regra_sem_agro
)


# ============================================================
# 04 ENRIQUECIMENTO DA BASE
# ============================================================

df_estudo = (

    df_base

    .withColumn(
        "IN_QT_TOTAL_POSITIVA",
        F.when(
            regra_qt_total,
            1
        ).otherwise(0)
    )

    .withColumn(
        "IN_QT_ENTRADA_POSITIVA",
        F.when(
            regra_qt_entrada,
            1
        ).otherwise(0)
    )

    .withColumn(
        "IN_QT_SAIDA_POSITIVA",
        F.when(
            regra_qt_saida,
            1
        ).otherwise(0)
    )

    .withColumn(
        "IN_VL_ENTRADA_POSITIVO",
        F.when(
            regra_vl_entrada,
            1
        ).otherwise(0)
    )

    .withColumn(
        "IN_VL_SAIDA_POSITIVO",
        F.when(
            regra_vl_saida,
            1
        ).otherwise(0)
    )

    .withColumn(
        "IN_PERFIL_APTO",
        F.when(
            regra_perfil_apto,
            1
        ).otherwise(0)
    )

    .withColumn(
        "IN_SEM_MOV_AGRO",
        F.when(
            regra_sem_agro,
            1
        ).otherwise(0)
    )

    .withColumn(
        "IN_TRANSACAO_APTA",
        F.when(
            regra_transacional,
            1
        ).otherwise(0)
    )

    .withColumn(
        "ST_PERFIL_RADAR",
        F.when(
            regra_perfil_apto,
            F.lit("COM PERFIL APTO")
        ).otherwise(
            F.lit("SEM PERFIL APTO")
        )
    )

    .withColumn(
        "ST_MOVIMENTACAO_AGRO",
        F.when(
            regra_sem_agro,
            F.lit("SEM MOVIMENTAÇÃO AGRO")
        ).otherwise(
            F.lit("COM MOVIMENTAÇÃO AGRO")
        )
    )

    .withColumn(
        "FL_RADAR_RECALCULADO",
        F.when(
            regra_radar,
            F.lit("S")
        ).otherwise(
            F.lit("N")
        )
    )

    .withColumn(
        "QT_MOTIVOS_NAO_PARTICIPACAO",

        F.when(
            ~regra_qt_total,
            1
        ).otherwise(0)

        +

        F.when(
            ~regra_qt_entrada,
            1
        ).otherwise(0)

        +

        F.when(
            ~regra_qt_saida,
            1
        ).otherwise(0)

        +

        F.when(
            ~regra_vl_entrada,
            1
        ).otherwise(0)

        +

        F.when(
            ~regra_vl_saida,
            1
        ).otherwise(0)

        +

        F.when(
            ~regra_perfil_apto,
            1
        ).otherwise(0)

        +

        F.when(
            ~regra_sem_agro,
            1
        ).otherwise(0)
    )

    .withColumn(
        "DS_MOTIVO_PRINCIPAL",

        F.when(
            ~regra_qt_total,
            F.lit("01. SEM TRANSAÇÃO TOTAL")
        )

        .when(
            ~regra_qt_entrada,
            F.lit("02. SEM ENTRADA")
        )

        .when(
            ~regra_qt_saida,
            F.lit("03. SEM SAÍDA")
        )

        .when(
            ~regra_vl_entrada,
            F.lit("04. VALOR DE ENTRADA ZERO")
        )

        .when(
            ~regra_vl_saida,
            F.lit("05. VALOR DE SAÍDA ZERO")
        )

        .when(
            ~regra_perfil_apto,
            F.lit("06. SEM PERFIL APTO")
        )

        .when(
            ~regra_sem_agro,
            F.lit("07. MOVIMENTAÇÃO AGRO")
        )

        .otherwise(
            F.lit("08. PARTICIPA DO RADAR")
        )
    )

    .withColumn(
        "DS_COMBINACAO_MOTIVOS",

        F.when(
            regra_radar,
            F.lit("SEM MOTIVO")
        )

        .otherwise(

            F.concat_ws(

                " + ",

                F.when(
                    ~regra_qt_total,
                    F.lit("SEM TRANSAÇÃO TOTAL")
                ),

                F.when(
                    ~regra_qt_entrada,
                    F.lit("SEM ENTRADA")
                ),

                F.when(
                    ~regra_qt_saida,
                    F.lit("SEM SAÍDA")
                ),

                F.when(
                    ~regra_vl_entrada,
                    F.lit("VALOR DE ENTRADA ZERO")
                ),

                F.when(
                    ~regra_vl_saida,
                    F.lit("VALOR DE SAÍDA ZERO")
                ),

                F.when(
                    ~regra_perfil_apto,
                    F.lit("SEM PERFIL APTO")
                ),

                F.when(
                    ~regra_sem_agro,
                    F.lit("MOVIMENTAÇÃO AGRO")
                )

            )

        )
    )

    .persist(
        StorageLevel.MEMORY_AND_DISK
    )

)


# ============================================================
# 05 VISÃO GERAL E MATERIALIZAÇÃO
# ============================================================

resumo_base = (

    df_estudo

    .agg(

        F.count("*")
        .alias("QT_REGISTROS"),

        F.countDistinct(
            "CD_CLI"
        )
        .alias("QT_CLIENTES_DISTINTOS"),

        F.min(
            "DT_REF_INI"
        )
        .alias("DT_REF_INI"),

        F.max(
            "DT_REF_FIM"
        )
        .alias("DT_REF_FIM"),

        F.min(
            "DT_EXEA"
        )
        .alias("DT_EXEA_MIN"),

        F.max(
            "DT_EXEA"
        )
        .alias("DT_EXEA_MAX"),

        F.sum(
            F.when(
                F.col("FL_PARTICIPA_RADAR")
                !=
                F.col("FL_RADAR_RECALCULADO"),
                1
            ).otherwise(0)
        )
        .alias("QT_DIVERGENCIA_RADAR"),

        F.sum(
            F.when(
                F.upper(
                    F.trim(
                        F.coalesce(
                            F.col("NM_PRFL"),
                            F.lit("")
                        )
                    )
                )
                ==
                F.lit("SEM PERFIL"),
                1
            ).otherwise(0)
        )
        .alias("QT_NM_PRFL_SEM_PERFIL")

    )

    .first()

)

QT_TOTAL = int(
    resumo_base["QT_REGISTROS"]
)

QT_CLIENTES_DISTINTOS = int(
    resumo_base["QT_CLIENTES_DISTINTOS"]
)

QT_DIVERGENCIA_RADAR = int(
    resumo_base["QT_DIVERGENCIA_RADAR"] or 0
)

if QT_TOTAL != QT_CLIENTES_DISTINTOS:

    raise ValueError(
        "A base possui mais de uma linha por CD_CLI. "
        f"Registros={QT_TOTAL}; "
        f"clientes distintos={QT_CLIENTES_DISTINTOS}."
    )

print("\n")
print("=" * 120)
print("BASE ANALISADA")
print("=" * 120)
print(f"Tabela: {TABELA}")
print(f"Clientes: {formatar_inteiro(QT_TOTAL)}")
print(
    "Período de referência: "
    f"{resumo_base['DT_REF_INI']} "
    f"a "
    f"{resumo_base['DT_REF_FIM']}"
)
print(
    "Execução: "
    f"{resumo_base['DT_EXEA_MIN']}"
)
print(
    "Divergências entre regra recalculada e campo gravado: "
    f"{formatar_inteiro(QT_DIVERGENCIA_RADAR)}"
)


# ============================================================
# 06 TABELA 00 | RESUMO DA BASE
# ============================================================

tb_00_resumo_base = (

    df_estudo

    .agg(

        F.count("*")
        .alias("QT_CLIENTES"),

        F.countDistinct(
            "CD_CLI"
        )
        .alias("QT_CLIENTES_DISTINTOS"),

        F.min(
            "DT_REF_INI"
        )
        .alias("DT_REF_INI"),

        F.max(
            "DT_REF_FIM"
        )
        .alias("DT_REF_FIM"),

        F.min(
            "DT_EXEA"
        )
        .alias("DT_EXEA"),

        F.sum(
            F.when(
                F.col("FL_PARTICIPA_RADAR")
                ==
                "S",
                1
            ).otherwise(0)
        )
        .alias("QT_PARTICIPA"),

        F.sum(
            F.when(
                F.col("FL_PARTICIPA_RADAR")
                ==
                "N",
                1
            ).otherwise(0)
        )
        .alias("QT_NAO_PARTICIPA"),

        F.sum(
            "IN_PERFIL_APTO"
        )
        .alias("QT_PERFIL_APTO"),

        F.sum(
            F.when(
                F.col("IN_PERFIL_APTO")
                ==
                0,
                1
            ).otherwise(0)
        )
        .alias("QT_SEM_PERFIL_APTO"),

        F.sum(
            F.when(
                F.col("FL_TEM_MOV_AGRO")
                ==
                "S",
                1
            ).otherwise(0)
        )
        .alias("QT_COM_MOV_AGRO"),

        F.sum(
            F.when(
                F.col("QT_TRANS_ENT")
                ==
                0,
                1
            ).otherwise(0)
        )
        .alias("QT_ENTRADA_ZERO"),

        F.sum(
            F.when(
                F.col("QT_TRANS_SAI")
                ==
                0,
                1
            ).otherwise(0)
        )
        .alias("QT_SAIDA_ZERO")

    )

)

pdf_00 = mostrar_tabela(
    "00_RESUMO_BASE",
    tb_00_resumo_base
)

linha_00 = pdf_00.iloc[0]

insight(
    "VISÃO GLOBAL",
    f"""
Base analisada: {formatar_inteiro(linha_00['QT_CLIENTES'])} clientes.

Participam do Radar:
{formatar_inteiro(linha_00['QT_PARTICIPA'])}
({formatar_percentual(linha_00['QT_PARTICIPA'] / QT_TOTAL * 100)})

Não participam do Radar:
{formatar_inteiro(linha_00['QT_NAO_PARTICIPA'])}
({formatar_percentual(linha_00['QT_NAO_PARTICIPA'] / QT_TOTAL * 100)})

Clientes com perfil apto:
{formatar_inteiro(linha_00['QT_PERFIL_APTO'])}
({formatar_percentual(linha_00['QT_PERFIL_APTO'] / QT_TOTAL * 100)})

Clientes sem perfil apto:
{formatar_inteiro(linha_00['QT_SEM_PERFIL_APTO'])}
({formatar_percentual(linha_00['QT_SEM_PERFIL_APTO'] / QT_TOTAL * 100)})
"""
)


# ============================================================
# 07 TABELA 01 | PARTICIPAÇÃO NO RADAR
# ============================================================

tb_01_participacao_radar = (

    criar_tabela_frequencia(
        df_estudo,
        "FL_PARTICIPA_RADAR",
        QT_TOTAL,
        "FL_PARTICIPA_RADAR"
    )

    .withColumn(
        "RESULTADO",
        F.when(
            F.col("FL_PARTICIPA_RADAR")
            ==
            "S",
            F.lit("PARTICIPA")
        ).otherwise(
            F.lit("NÃO PARTICIPA")
        )
    )

    .select(
        "RESULTADO",
        "FL_PARTICIPA_RADAR",
        "QT_CLIENTES",
        "PC_CLIENTES"
    )

    .orderBy(
        F.desc("QT_CLIENTES")
    )

)

pdf_01 = mostrar_tabela(
    "01_PARTICIPACAO_RADAR",
    tb_01_participacao_radar
)

grafico_rosca(
    pdf_01,
    "RESULTADO",
    "QT_CLIENTES",
    "Participação no Radar",
    "01_PARTICIPACAO_RADAR"
)


# ============================================================
# 08 TABELA 02 | PERFIL APTO X SEM PERFIL APTO
# ============================================================

tb_02_status_perfil = criar_tabela_frequencia(
    df_estudo,
    "ST_PERFIL_RADAR",
    QT_TOTAL,
    "STATUS_PERFIL"
)

pdf_02 = mostrar_tabela(
    "02_STATUS_PERFIL_RADAR",
    tb_02_status_perfil
)

grafico_rosca(
    pdf_02,
    "STATUS_PERFIL",
    "QT_CLIENTES",
    "Clientes com Perfil Apto para o Radar",
    "02_STATUS_PERFIL_RADAR"
)


# ============================================================
# 09 TABELA 03 | CAMPOS DE PERFIL NÃO APTOS
# ============================================================

linha_perfil = (

    df_estudo

    .agg(

        F.sum(
            F.when(
                ~regra_nm_prfl,
                1
            ).otherwise(0)
        )
        .alias("NM_PRFL"),

        F.sum(
            F.when(
                ~regra_nm_macro,
                1
            ).otherwise(0)
        )
        .alias("NM_MAC_PRFL_CLI"),

        F.sum(
            F.when(
                ~regra_nm_micro,
                1
            ).otherwise(0)
        )
        .alias("NM_MIC_PRFL_CLI"),

        F.sum(
            F.when(
                ~regra_nm_fin,
                1
            ).otherwise(0)
        )
        .alias("NM_PRFL_FIN"),

        F.sum(
            F.when(
                F.upper(
                    F.trim(
                        F.coalesce(
                            F.col("NM_PRFL"),
                            F.lit("")
                        )
                    )
                )
                ==
                "SEM PERFIL",
                1
            ).otherwise(0)
        )
        .alias("NM_PRFL_SEM_PERFIL")

    )

    .first()

)

linhas_perfil = [

    (
        1,
        "NM_PRFL = A CLASSIFICAR ou nulo",
        int(linha_perfil["NM_PRFL"] or 0)
    ),

    (
        2,
        "NM_MAC_PRFL_CLI = A CLASSIFICAR ou nulo",
        int(linha_perfil["NM_MAC_PRFL_CLI"] or 0)
    ),

    (
        3,
        "NM_MIC_PRFL_CLI = A CLASSIFICAR ou nulo",
        int(linha_perfil["NM_MIC_PRFL_CLI"] or 0)
    ),

    (
        4,
        "NM_PRFL_FIN = A CLASSIFICAR ou nulo",
        int(linha_perfil["NM_PRFL_FIN"] or 0)
    ),

    (
        5,
        "NM_PRFL = SEM PERFIL (aceito pela regra oficial)",
        int(linha_perfil["NM_PRFL_SEM_PERFIL"] or 0)
    )

]

tb_03_campos_perfil = (

    spark

    .createDataFrame(
        linhas_perfil,
        [
            "ORDEM",
            "CRITERIO",
            "QT_CLIENTES"
        ]
    )

    .withColumn(
        "PC_BASE",
        F.round(
            F.col("QT_CLIENTES")
            /
            F.lit(QT_TOTAL)
            *
            100,
            2
        )
    )

    .orderBy(
        "ORDEM"
    )

)

pdf_03 = mostrar_tabela(
    "03_CAMPOS_PERFIL_NAO_APTOS",
    tb_03_campos_perfil
)

insight(
    "REGRA DE PERFIL",
    """
O status COM PERFIL APTO exige que os quatro campos de perfil
sejam diferentes de A CLASSIFICAR.

As quantidades por campo são sobrepostas:
um mesmo cliente pode falhar em mais de um campo.

O valor SEM PERFIL em NM_PRFL é aceito pela regra oficial,
pois a exclusão considera somente A CLASSIFICAR.
"""
)


# ============================================================
# 10 TABELA 04 | MOVIMENTAÇÃO AGRO
# ============================================================

tb_04_movimentacao_agro = criar_tabela_frequencia(
    df_estudo,
    "ST_MOVIMENTACAO_AGRO",
    QT_TOTAL,
    "STATUS_AGRO"
)

pdf_04 = mostrar_tabela(
    "04_MOVIMENTACAO_AGRO",
    tb_04_movimentacao_agro
)

grafico_rosca(
    pdf_04,
    "STATUS_AGRO",
    "QT_CLIENTES",
    "Movimentação Agro",
    "04_MOVIMENTACAO_AGRO"
)


# ============================================================
# 11 TABELA 05 | VALIDAÇÃO DA REGRA OFICIAL
# ============================================================

tb_05_validacao_radar = (

    df_estudo

    .groupBy(
        "FL_PARTICIPA_RADAR",
        "FL_RADAR_RECALCULADO"
    )

    .agg(
        F.count("*")
        .alias("QT_CLIENTES")
    )

    .withColumn(
        "PC_BASE",
        F.round(
            F.col("QT_CLIENTES")
            /
            F.lit(QT_TOTAL)
            *
            100,
            4
        )
    )

    .orderBy(
        "FL_PARTICIPA_RADAR",
        "FL_RADAR_RECALCULADO"
    )

)

pdf_05 = mostrar_tabela(
    "05_VALIDACAO_REGRA_RADAR",
    tb_05_validacao_radar
)

insight(
    "VALIDAÇÃO DA REGRA",
    f"""
Divergências entre FL_PARTICIPA_RADAR e a regra recalculada:
{formatar_inteiro(QT_DIVERGENCIA_RADAR)}

{
    "A regra foi reproduzida integralmente."
    if QT_DIVERGENCIA_RADAR == 0
    else
    "Existem divergências que precisam ser investigadas antes da apresentação."
}
"""
)


# ============================================================
# 12 TABELA 06 | FUNIL ACUMULADO DE ELEGIBILIDADE
# ============================================================

condicoes_funil = [

    (
        1,
        "Base analisada",
        F.lit(True)
    ),

    (
        2,
        "Quantidade total positiva",
        regra_qt_total
    ),

    (
        3,
        "Com quantidade de entrada",
        regra_qt_total
        &
        regra_qt_entrada
    ),

    (
        4,
        "Com quantidade de saída",
        regra_qt_total
        &
        regra_qt_entrada
        &
        regra_qt_saida
    ),

    (
        5,
        "Com valor de entrada positivo",
        regra_qt_total
        &
        regra_qt_entrada
        &
        regra_qt_saida
        &
        regra_vl_entrada
    ),

    (
        6,
        "Com valor de saída positivo",
        regra_transacional
    ),

    (
        7,
        "Com perfil apto",
        regra_transacional
        &
        regra_perfil_apto
    ),

    (
        8,
        "Participa do Radar (sem Agro)",
        regra_radar
    )

]

agregacoes_funil = [

    F.sum(
        F.when(
            condicao,
            1
        ).otherwise(0)
    )
    .alias(
        f"ETAPA_{ordem}"
    )

    for ordem, _, condicao
    in condicoes_funil

]

linha_funil = (

    df_estudo

    .agg(
        *agregacoes_funil
    )

    .first()

)

linhas_funil = []

quantidade_anterior = None

for ordem, etapa, _ in condicoes_funil:

    quantidade = int(
        linha_funil[
            f"ETAPA_{ordem}"
        ]
        or
        0
    )

    perda = (
        0
        if quantidade_anterior is None
        else quantidade_anterior - quantidade
    )

    percentual_base = (
        quantidade
        /
        QT_TOTAL
        *
        100
        if QT_TOTAL > 0
        else 0
    )

    percentual_etapa_anterior = (
        100.0
        if quantidade_anterior is None
        else
        (
            quantidade
            /
            quantidade_anterior
            *
            100
            if quantidade_anterior > 0
            else 0
        )
    )

    linhas_funil.append(
        (
            ordem,
            etapa,
            quantidade,
            float(percentual_base),
            int(perda),
            float(percentual_etapa_anterior)
        )
    )

    quantidade_anterior = quantidade

tb_06_funil = (

    spark

    .createDataFrame(
        linhas_funil,
        [
            "ORDEM",
            "ETAPA",
            "QT_CLIENTES",
            "PC_BASE",
            "PERDA_ETAPA",
            "PC_RETENCAO_ETAPA"
        ]
    )

    .orderBy(
        "ORDEM"
    )

)

pdf_06 = mostrar_tabela(
    "06_FUNIL_ELEGIBILIDADE_RADAR",
    tb_06_funil
)

grafico_funil(
    pdf_06,
    "Funil de Elegibilidade para o Radar",
    "06_FUNIL_ELEGIBILIDADE_RADAR"
)


# ============================================================
# 13 TABELA 07 | MOTIVOS SOBREPOSTOS
# ============================================================

QT_NAO_PARTICIPA = int(

    df_estudo

    .filter(
        F.col("FL_RADAR_RECALCULADO")
        ==
        "N"
    )

    .count()

)

motivos_sobrepostos = [

    (
        1,
        "SEM TRANSAÇÃO TOTAL",
        ~regra_qt_total
    ),

    (
        2,
        "SEM ENTRADA",
        ~regra_qt_entrada
    ),

    (
        3,
        "SEM SAÍDA",
        ~regra_qt_saida
    ),

    (
        4,
        "VALOR DE ENTRADA ZERO",
        ~regra_vl_entrada
    ),

    (
        5,
        "VALOR DE SAÍDA ZERO",
        ~regra_vl_saida
    ),

    (
        6,
        "SEM PERFIL APTO",
        ~regra_perfil_apto
    ),

    (
        7,
        "MOVIMENTAÇÃO AGRO",
        ~regra_sem_agro
    )

]

linha_motivos = (

    df_estudo

    .filter(
        F.col("FL_RADAR_RECALCULADO")
        ==
        "N"
    )

    .agg(

        *[

            F.sum(
                F.when(
                    condicao,
                    1
                ).otherwise(0)
            )
            .alias(
                f"MOTIVO_{ordem}"
            )

            for ordem, _, condicao
            in motivos_sobrepostos

        ]

    )

    .first()

)

linhas_motivos = []

for ordem, motivo, _ in motivos_sobrepostos:

    quantidade = int(
        linha_motivos[
            f"MOTIVO_{ordem}"
        ]
        or
        0
    )

    linhas_motivos.append(
        (
            ordem,
            motivo,
            quantidade,
            float(
                quantidade
                /
                QT_TOTAL
                *
                100
            ),
            float(
                quantidade
                /
                QT_NAO_PARTICIPA
                *
                100
                if QT_NAO_PARTICIPA > 0
                else 0
            )
        )
    )

tb_07_motivos_sobrepostos = (

    spark

    .createDataFrame(
        linhas_motivos,
        [
            "ORDEM",
            "MOTIVO",
            "QT_CLIENTES",
            "PC_BASE",
            "PC_NAO_PARTICIPANTES"
        ]
    )

    .orderBy(
        F.desc("QT_CLIENTES")
    )

)

pdf_07 = mostrar_tabela(
    "07_MOTIVOS_SOBREPOSTOS_NAO_PARTICIPACAO",
    tb_07_motivos_sobrepostos
)

grafico_barra_horizontal(
    pdf_07,
    "MOTIVO",
    "QT_CLIENTES",
    "Motivos de Não Participação — Visão Sobreposta",
    "07_MOTIVOS_SOBREPOSTOS",
    "PC_NAO_PARTICIPANTES"
)

insight(
    "MOTIVOS SOBREPOSTOS",
    """
Nesta visão, um mesmo cliente pode aparecer em mais de um motivo.
Ela mede a abrangência de cada problema, mas as quantidades
não devem ser somadas.
"""
)


# ============================================================
# 14 TABELA 08 | MOTIVO PRINCIPAL SEM DUPLA CONTAGEM
# ============================================================

tb_08_motivo_principal = (

    df_estudo

    .groupBy(
        "DS_MOTIVO_PRINCIPAL"
    )

    .agg(
        F.count("*")
        .alias("QT_CLIENTES")
    )

    .withColumn(
        "PC_BASE",
        F.round(
            F.col("QT_CLIENTES")
            /
            F.lit(QT_TOTAL)
            *
            100,
            2
        )
    )

    .orderBy(
        "DS_MOTIVO_PRINCIPAL"
    )

)

pdf_08 = mostrar_tabela(
    "08_MOTIVO_PRINCIPAL_SEM_DUPLA_CONTAGEM",
    tb_08_motivo_principal
)

pdf_08_nao_participa = (

    pdf_08[
        ~pdf_08[
            "DS_MOTIVO_PRINCIPAL"
        ]
        .str.contains(
            "PARTICIPA DO RADAR",
            na=False
        )
    ]

    .copy()

)

grafico_barra_horizontal(
    pdf_08_nao_participa,
    "DS_MOTIVO_PRINCIPAL",
    "QT_CLIENTES",
    "Motivo Principal de Não Participação",
    "08_MOTIVO_PRINCIPAL",
    "PC_BASE"
)


# ============================================================
# 15 TABELA 09 | COMBINAÇÕES DE MOTIVOS
# ============================================================

tb_09_combinacoes_motivos = (

    df_estudo

    .filter(
        F.col("FL_RADAR_RECALCULADO")
        ==
        "N"
    )

    .groupBy(
        "DS_COMBINACAO_MOTIVOS"
    )

    .agg(
        F.count("*")
        .alias("QT_CLIENTES")
    )

    .withColumn(
        "PC_NAO_PARTICIPANTES",
        F.round(
            F.col("QT_CLIENTES")
            /
            F.lit(QT_NAO_PARTICIPA)
            *
            100,
            2
        )
    )

    .orderBy(
        F.desc("QT_CLIENTES")
    )

)

pdf_09 = mostrar_tabela(
    "09_COMBINACOES_MOTIVOS_NAO_PARTICIPACAO",
    tb_09_combinacoes_motivos,
    TOP_COMBINACOES
)

grafico_barra_horizontal(
    pdf_09.head(10),
    "DS_COMBINACAO_MOTIVOS",
    "QT_CLIENTES",
    "Principais Combinações de Motivos",
    "09_COMBINACOES_MOTIVOS",
    "PC_NAO_PARTICIPANTES"
)


# ============================================================
# 16 TABELA 10 | QUANTIDADE DE MOTIVOS POR CLIENTE
# ============================================================

tb_10_quantidade_motivos = (

    df_estudo

    .groupBy(
        "QT_MOTIVOS_NAO_PARTICIPACAO"
    )

    .agg(
        F.count("*")
        .alias("QT_CLIENTES")
    )

    .withColumn(
        "PC_BASE",
        F.round(
            F.col("QT_CLIENTES")
            /
            F.lit(QT_TOTAL)
            *
            100,
            2
        )
    )

    .orderBy(
        "QT_MOTIVOS_NAO_PARTICIPACAO"
    )

)

pdf_10 = mostrar_tabela(
    "10_QUANTIDADE_MOTIVOS_POR_CLIENTE",
    tb_10_quantidade_motivos
)


# ============================================================
# 17 TABELA 11 | PERFIL APTO X RADAR
# ============================================================

janela_perfil = Window.partitionBy(
    "ST_PERFIL_RADAR"
)

tb_11_perfil_x_radar = (

    df_estudo

    .groupBy(
        "ST_PERFIL_RADAR",
        "FL_PARTICIPA_RADAR"
    )

    .agg(
        F.count("*")
        .alias("QT_CLIENTES")
    )

    .withColumn(
        "QT_TOTAL_STATUS_PERFIL",
        F.sum(
            "QT_CLIENTES"
        )
        .over(
            janela_perfil
        )
    )

    .withColumn(
        "PC_DENTRO_STATUS_PERFIL",
        F.round(
            F.col("QT_CLIENTES")
            /
            F.col("QT_TOTAL_STATUS_PERFIL")
            *
            100,
            2
        )
    )

    .orderBy(
        "ST_PERFIL_RADAR",
        "FL_PARTICIPA_RADAR"
    )

)

pdf_11 = mostrar_tabela(
    "11_PERFIL_APTO_X_RADAR",
    tb_11_perfil_x_radar
)

grafico_barras_empilhadas(
    pdf_11,
    "ST_PERFIL_RADAR",
    "FL_PARTICIPA_RADAR",
    "QT_CLIENTES",
    "Participação no Radar por Status de Perfil",
    "11_PERFIL_APTO_X_RADAR",
    percentual=True
)


# ============================================================
# 18 TABELA 12 | AGRO X RADAR
# ============================================================

janela_agro = Window.partitionBy(
    "ST_MOVIMENTACAO_AGRO"
)

tb_12_agro_x_radar = (

    df_estudo

    .groupBy(
        "ST_MOVIMENTACAO_AGRO",
        "FL_PARTICIPA_RADAR"
    )

    .agg(
        F.count("*")
        .alias("QT_CLIENTES")
    )

    .withColumn(
        "QT_TOTAL_STATUS_AGRO",
        F.sum(
            "QT_CLIENTES"
        )
        .over(
            janela_agro
        )
    )

    .withColumn(
        "PC_DENTRO_STATUS_AGRO",
        F.round(
            F.col("QT_CLIENTES")
            /
            F.col("QT_TOTAL_STATUS_AGRO")
            *
            100,
            2
        )
    )

    .orderBy(
        "ST_MOVIMENTACAO_AGRO",
        "FL_PARTICIPA_RADAR"
    )

)

pdf_12 = mostrar_tabela(
    "12_AGRO_X_RADAR",
    tb_12_agro_x_radar
)


# ============================================================
# 19 TABELA 13 | ENTRADAS X SAÍDAS
# ============================================================

linha_volume = (

    df_estudo

    .agg(

        F.sum(
            "QT_TRANS_ENT"
        )
        .alias("QT_TRANS_ENT"),

        F.sum(
            "QT_TRANS_SAI"
        )
        .alias("QT_TRANS_SAI"),

        F.sum(
            F.col("VL_TRANS_ENT")
            .cast("double")
        )
        .alias("VL_TRANS_ENT"),

        F.sum(
            F.col("VL_TRANS_SAI")
            .cast("double")
        )
        .alias("VL_TRANS_SAI")

    )

    .first()

)

qt_entrada_total = int(
    linha_volume["QT_TRANS_ENT"] or 0
)

qt_saida_total = int(
    linha_volume["QT_TRANS_SAI"] or 0
)

qt_movimentos_total = (
    qt_entrada_total
    +
    qt_saida_total
)

linhas_volume = [

    (
        "ENTRADAS",
        qt_entrada_total,
        float(
            qt_entrada_total
            /
            qt_movimentos_total
            *
            100
            if qt_movimentos_total > 0
            else 0
        ),
        float(
            linha_volume["VL_TRANS_ENT"]
            or
            0
        )
    ),

    (
        "SAÍDAS",
        qt_saida_total,
        float(
            qt_saida_total
            /
            qt_movimentos_total
            *
            100
            if qt_movimentos_total > 0
            else 0
        ),
        float(
            linha_volume["VL_TRANS_SAI"]
            or
            0
        )
    )

]

tb_13_entradas_saidas = (

    spark

    .createDataFrame(
        linhas_volume,
        [
            "TIPO_TRANSACAO",
            "QT_TRANSACOES",
            "PC_TRANSACOES",
            "VL_TRANSACOES"
        ]
    )

    .orderBy(
        F.desc("QT_TRANSACOES")
    )

)

pdf_13 = mostrar_tabela(
    "13_ENTRADAS_X_SAIDAS",
    tb_13_entradas_saidas
)

grafico_barra_horizontal(
    pdf_13,
    "TIPO_TRANSACAO",
    "QT_TRANSACOES",
    "Quantidade de Transações: Entradas x Saídas",
    "13_ENTRADAS_X_SAIDAS",
    "PC_TRANSACOES"
)

insight(
    "ENTRADAS X SAÍDAS",
    f"""
Quantidade total de entradas:
{formatar_inteiro(qt_entrada_total)}
({formatar_percentual(qt_entrada_total / qt_movimentos_total * 100)})

Quantidade total de saídas:
{formatar_inteiro(qt_saida_total)}
({formatar_percentual(qt_saida_total / qt_movimentos_total * 100)})
"""
)


# ============================================================
# 20 TABELA 14 | CLIENTES COM ENTRADA OU SAÍDA ZERO
# ============================================================

linha_zero = (

    df_estudo

    .agg(

        F.sum(
            F.when(
                F.col("QT_TRANS_ENT")
                ==
                0,
                1
            ).otherwise(0)
        )
        .alias("ENTRADA_ZERO"),

        F.sum(
            F.when(
                F.col("QT_TRANS_SAI")
                ==
                0,
                1
            ).otherwise(0)
        )
        .alias("SAIDA_ZERO"),

        F.sum(
            F.when(
                (
                    F.col("QT_TRANS_ENT")
                    ==
                    0
                )
                &
                (
                    F.col("QT_TRANS_SAI")
                    ==
                    0
                ),
                1
            ).otherwise(0)
        )
        .alias("ENTRADA_E_SAIDA_ZERO")

    )

    .first()

)

linhas_zero = [

    (
        "ENTRADA ZERO",
        int(
            linha_zero["ENTRADA_ZERO"]
            or
            0
        )
    ),

    (
        "SAÍDA ZERO",
        int(
            linha_zero["SAIDA_ZERO"]
            or
            0
        )
    ),

    (
        "ENTRADA E SAÍDA ZERO",
        int(
            linha_zero["ENTRADA_E_SAIDA_ZERO"]
            or
            0
        )
    )

]

tb_14_movimentacao_zero = (

    spark

    .createDataFrame(
        linhas_zero,
        [
            "SITUACAO",
            "QT_CLIENTES"
        ]
    )

    .withColumn(
        "PC_BASE",
        F.round(
            F.col("QT_CLIENTES")
            /
            F.lit(QT_TOTAL)
            *
            100,
            2
        )
    )

    .orderBy(
        F.desc("QT_CLIENTES")
    )

)

pdf_14 = mostrar_tabela(
    "14_CLIENTES_COM_MOVIMENTACAO_ZERO",
    tb_14_movimentacao_zero
)

grafico_barra_horizontal(
    pdf_14,
    "SITUACAO",
    "QT_CLIENTES",
    "Clientes com Entrada ou Saída Zero",
    "14_CLIENTES_MOVIMENTACAO_ZERO",
    "PC_BASE"
)


# ============================================================
# 21 TABELA 15 | ANÁLISE COMPLEMENTAR DE SAÍDA ZERO
# ============================================================

tb_15_saida_zero = (

    df_estudo

    .filter(
        F.col("QT_TRANS_SAI")
        ==
        0
    )

    .agg(

        F.count("*")
        .alias("QT_CLIENTES"),

        F.sum(
            "QT_TRANS_ENT"
        )
        .alias("QT_TRANS_ENT_TOTAL"),

        F.round(
            F.avg(
                "QT_TRANS_ENT"
            ),
            2
        )
        .alias("MEDIA_QT_TRANS_ENT"),

        F.expr(
            "percentile_approx(QT_TRANS_ENT, 0.50, 10000)"
        )
        .alias("MEDIANA_QT_TRANS_ENT"),

        F.expr(
            "percentile_approx(QT_TRANS_ENT, 0.75, 10000)"
        )
        .alias("P75_QT_TRANS_ENT"),

        F.expr(
            "percentile_approx(QT_TRANS_ENT, 0.95, 10000)"
        )
        .alias("P95_QT_TRANS_ENT"),

        F.sum(
            F.when(
                F.col("QT_TRANS_ENT")
                ==
                0,
                1
            ).otherwise(0)
        )
        .alias("QT_TAMBEM_SEM_ENTRADA"),

        F.round(
            F.sum(
                F.col("VL_TRANS_ENT")
                .cast("double")
            ),
            2
        )
        .alias("VL_TRANS_ENT_TOTAL"),

        F.sum(
            F.when(
                F.col("FL_PARTICIPA_RADAR")
                ==
                "S",
                1
            ).otherwise(0)
        )
        .alias("QT_PARTICIPA_RADAR")

    )

    .withColumn(
        "PC_TAMBEM_SEM_ENTRADA",
        F.round(
            F.col("QT_TAMBEM_SEM_ENTRADA")
            /
            F.col("QT_CLIENTES")
            *
            100,
            2
        )
    )

)

pdf_15 = mostrar_tabela(
    "15_ANALISE_CLIENTES_COM_SAIDA_ZERO",
    tb_15_saida_zero
)

linha_15 = pdf_15.iloc[0]

insight(
    "CLIENTES COM SAÍDA ZERO",
    f"""
Clientes sem saída:
{formatar_inteiro(linha_15['QT_CLIENTES'])}

Transações de entrada realizadas por esses clientes:
{formatar_inteiro(linha_15['QT_TRANS_ENT_TOTAL'])}

Média de entradas por cliente:
{formatar_decimal(linha_15['MEDIA_QT_TRANS_ENT'])}

Mediana:
{formatar_inteiro(linha_15['MEDIANA_QT_TRANS_ENT'])}

Também não possuem entradas:
{formatar_inteiro(linha_15['QT_TAMBEM_SEM_ENTRADA'])}
({formatar_percentual(linha_15['PC_TAMBEM_SEM_ENTRADA'])})

Participantes do Radar dentro desse grupo:
{formatar_inteiro(linha_15['QT_PARTICIPA_RADAR'])}
"""
)


# ============================================================
# 22 TABELA 16 | COMPARATIVO TRANSACIONAL POR RADAR
# ============================================================

tb_16_transacoes_por_radar = (

    df_estudo

    .groupBy(
        "FL_PARTICIPA_RADAR"
    )

    .agg(

        F.count("*")
        .alias("QT_CLIENTES"),

        F.round(
            F.avg(
                "QT_TRANS_TOTAL"
            ),
            2
        )
        .alias("MEDIA_QT_TRANS_TOTAL"),

        F.expr(
            "percentile_approx(QT_TRANS_TOTAL, 0.50, 10000)"
        )
        .alias("MEDIANA_QT_TRANS_TOTAL"),

        F.expr(
            "percentile_approx(QT_TRANS_TOTAL, 0.75, 10000)"
        )
        .alias("P75_QT_TRANS_TOTAL"),

        F.expr(
            "percentile_approx(QT_TRANS_TOTAL, 0.95, 10000)"
        )
        .alias("P95_QT_TRANS_TOTAL"),

        F.round(
            F.avg(
                "QT_TRANS_ENT"
            ),
            2
        )
        .alias("MEDIA_QT_TRANS_ENT"),

        F.expr(
            "percentile_approx(QT_TRANS_ENT, 0.50, 10000)"
        )
        .alias("MEDIANA_QT_TRANS_ENT"),

        F.round(
            F.avg(
                "QT_TRANS_SAI"
            ),
            2
        )
        .alias("MEDIA_QT_TRANS_SAI"),

        F.expr(
            "percentile_approx(QT_TRANS_SAI, 0.50, 10000)"
        )
        .alias("MEDIANA_QT_TRANS_SAI"),

        F.round(
            F.avg(
                F.col("VL_TRANS_ENT")
                .cast("double")
            ),
            2
        )
        .alias("MEDIA_VL_TRANS_ENT"),

        F.round(
            F.avg(
                F.col("VL_TRANS_SAI")
                .cast("double")
            ),
            2
        )
        .alias("MEDIA_VL_TRANS_SAI")

    )

    .withColumn(
        "PC_CLIENTES",
        F.round(
            F.col("QT_CLIENTES")
            /
            F.lit(QT_TOTAL)
            *
            100,
            2
        )
    )

    .orderBy(
        "FL_PARTICIPA_RADAR"
    )

)

pdf_16 = mostrar_tabela(
    "16_COMPARATIVO_TRANSACIONAL_POR_RADAR",
    tb_16_transacoes_por_radar
)

pdf_16_grafico = (

    pdf_16[[
        "FL_PARTICIPA_RADAR",
        "MEDIANA_QT_TRANS_TOTAL",
        "MEDIANA_QT_TRANS_ENT",
        "MEDIANA_QT_TRANS_SAI"
    ]]

    .melt(
        id_vars=[
            "FL_PARTICIPA_RADAR"
        ],
        var_name="INDICADOR",
        value_name="VALOR"
    )

)

pdf_16_grafico["INDICADOR"] = (

    pdf_16_grafico[
        "INDICADOR"
    ]

    .replace({

        "MEDIANA_QT_TRANS_TOTAL":
        "Total",

        "MEDIANA_QT_TRANS_ENT":
        "Entrada",

        "MEDIANA_QT_TRANS_SAI":
        "Saída"

    })

)

grafico_barras_agrupadas(
    pdf_16_grafico,
    "INDICADOR",
    "FL_PARTICIPA_RADAR",
    "VALOR",
    "Mediana de Transações por Participação no Radar",
    "16_MEDIANA_TRANSACOES_POR_RADAR",
    "Mediana de transações"
)


# ============================================================
# 23 TABELA 17 | DISTRIBUIÇÃO DAS TRANSAÇÕES
# ============================================================

variaveis_transacao = [

    "QT_TRANS_TOTAL",
    "QT_TRANS_ENT",
    "QT_TRANS_SAI"

]

probabilidades = [

    0.25,
    0.50,
    0.75,
    0.90,
    0.95,
    0.99

]

quantis = df_estudo.approxQuantile(
    variaveis_transacao,
    probabilidades,
    0.001
)

agregacoes_estatisticas = []

for variavel in variaveis_transacao:

    agregacoes_estatisticas.extend([

        F.min(
            variavel
        )
        .alias(
            f"{variavel}_MIN"
        ),

        F.round(
            F.avg(
                variavel
            ),
            4
        )
        .alias(
            f"{variavel}_MEDIA"
        ),

        F.round(
            F.stddev(
                variavel
            ),
            4
        )
        .alias(
            f"{variavel}_DESVIO"
        ),

        F.max(
            variavel
        )
        .alias(
            f"{variavel}_MAX"
        )

    ])

linha_estatisticas = (

    df_estudo

    .agg(
        *agregacoes_estatisticas
    )

    .first()

)

linhas_distribuicao = []

limites_outlier = {}

for indice, variavel in enumerate(
    variaveis_transacao
):

    q1, mediana, q3, p90, p95, p99 = quantis[
        indice
    ]

    iqr = (
        q3
        -
        q1
    )

    limite_outlier = (
        q3
        +
        1.5
        *
        iqr
    )

    limites_outlier[
        variavel
    ] = limite_outlier

    linhas_distribuicao.append(
        (
            variavel,
            float(
                linha_estatisticas[
                    f"{variavel}_MIN"
                ]
                or
                0
            ),
            float(
                linha_estatisticas[
                    f"{variavel}_MEDIA"
                ]
                or
                0
            ),
            float(
                linha_estatisticas[
                    f"{variavel}_DESVIO"
                ]
                or
                0
            ),
            float(q1),
            float(mediana),
            float(q3),
            float(p90),
            float(p95),
            float(p99),
            float(limite_outlier),
            float(
                linha_estatisticas[
                    f"{variavel}_MAX"
                ]
                or
                0
            )
        )
    )

tb_17_distribuicao_transacoes = (

    spark

    .createDataFrame(
        linhas_distribuicao,
        [
            "VARIAVEL",
            "MIN",
            "MEDIA",
            "DESVIO_PADRAO",
            "P25",
            "P50",
            "P75",
            "P90",
            "P95",
            "P99",
            "LIMITE_OUTLIER_IQR",
            "MAX"
        ]
    )

    .orderBy(
        "VARIAVEL"
    )

)

pdf_17 = mostrar_tabela(
    "17_DISTRIBUICAO_TRANSACOES",
    tb_17_distribuicao_transacoes
)


# ============================================================
# 24 TABELA 18 | OUTLIERS
# ============================================================

agregacoes_outliers = [

    F.sum(
        F.when(
            F.col(variavel)
            >
            F.lit(
                limites_outlier[
                    variavel
                ]
            ),
            1
        ).otherwise(0)
    )
    .alias(
        variavel
    )

    for variavel
    in variaveis_transacao

]

linha_outliers = (

    df_estudo

    .agg(
        *agregacoes_outliers
    )

    .first()

)

linhas_outliers = []

for variavel in variaveis_transacao:

    quantidade = int(
        linha_outliers[
            variavel
        ]
        or
        0
    )

    linhas_outliers.append(
        (
            variavel,
            float(
                limites_outlier[
                    variavel
                ]
            ),
            quantidade,
            float(
                quantidade
                /
                QT_TOTAL
                *
                100
            )
        )
    )

tb_18_outliers = (

    spark

    .createDataFrame(
        linhas_outliers,
        [
            "VARIAVEL",
            "LIMITE_OUTLIER",
            "QT_CLIENTES_OUTLIERS",
            "PC_BASE"
        ]
    )

    .orderBy(
        F.desc("QT_CLIENTES_OUTLIERS")
    )

)

pdf_18 = mostrar_tabela(
    "18_OUTLIERS_TRANSACOES",
    tb_18_outliers
)

grafico_barra_horizontal(
    pdf_18,
    "VARIAVEL",
    "QT_CLIENTES_OUTLIERS",
    "Clientes Outliers por Quantidade de Transações",
    "18_OUTLIERS_TRANSACOES",
    "PC_BASE"
)


# ============================================================
# 25 TABELA 19 | OUTLIERS X RADAR
# ============================================================

agregacoes_outliers_radar = [

    F.sum(
        F.when(
            F.col(variavel)
            >
            F.lit(
                limites_outlier[
                    variavel
                ]
            ),
            1
        ).otherwise(0)
    )
    .alias(
        f"OUT_{variavel}"
    )

    for variavel
    in variaveis_transacao

]

tb_19_outliers_x_radar_larga = (

    df_estudo

    .groupBy(
        "FL_PARTICIPA_RADAR"
    )

    .agg(
        F.count("*")
        .alias("QT_CLIENTES_GRUPO"),
        *agregacoes_outliers_radar
    )

    .orderBy(
        "FL_PARTICIPA_RADAR"
    )

)

pdf_19_larga = mostrar_tabela(
    "19_OUTLIERS_X_RADAR",
    tb_19_outliers_x_radar_larga
)

linhas_19 = []

for _, linha in pdf_19_larga.iterrows():

    flag = linha[
        "FL_PARTICIPA_RADAR"
    ]

    total_grupo = int(
        linha[
            "QT_CLIENTES_GRUPO"
        ]
    )

    for variavel in variaveis_transacao:

        quantidade = int(
            linha[
                f"OUT_{variavel}"
            ]
        )

        linhas_19.append(
            (
                flag,
                variavel,
                quantidade,
                float(
                    quantidade
                    /
                    total_grupo
                    *
                    100
                    if total_grupo > 0
                    else 0
                )
            )
        )

pdf_19 = pd.DataFrame(
    linhas_19,
    columns=[
        "FL_PARTICIPA_RADAR",
        "VARIAVEL",
        "QT_CLIENTES_OUTLIERS",
        "PC_GRUPO"
    ]
)

grafico_barras_agrupadas(
    pdf_19,
    "VARIAVEL",
    "FL_PARTICIPA_RADAR",
    "PC_GRUPO",
    "Percentual de Outliers por Participação no Radar",
    "19_OUTLIERS_X_RADAR",
    "Percentual dentro do grupo"
)


# ============================================================
# 26 TABELA 20 | MATRIZ FINAL DE ELEGIBILIDADE
# ============================================================

tb_20_matriz_elegibilidade = (

    df_estudo

    .groupBy(
        "IN_TRANSACAO_APTA",
        "IN_PERFIL_APTO",
        "IN_SEM_MOV_AGRO",
        "FL_PARTICIPA_RADAR"
    )

    .agg(
        F.count("*")
        .alias("QT_CLIENTES")
    )

    .withColumn(
        "PC_BASE",
        F.round(
            F.col("QT_CLIENTES")
            /
            F.lit(QT_TOTAL)
            *
            100,
            2
        )
    )

    .withColumn(
        "STATUS_TRANSACAO",
        F.when(
            F.col("IN_TRANSACAO_APTA")
            ==
            1,
            F.lit("TRANSAÇÃO APTA")
        ).otherwise(
            F.lit("TRANSAÇÃO NÃO APTA")
        )
    )

    .withColumn(
        "STATUS_PERFIL",
        F.when(
            F.col("IN_PERFIL_APTO")
            ==
            1,
            F.lit("PERFIL APTO")
        ).otherwise(
            F.lit("PERFIL NÃO APTO")
        )
    )

    .withColumn(
        "STATUS_AGRO",
        F.when(
            F.col("IN_SEM_MOV_AGRO")
            ==
            1,
            F.lit("SEM AGRO")
        ).otherwise(
            F.lit("COM AGRO")
        )
    )

    .select(
        "STATUS_TRANSACAO",
        "STATUS_PERFIL",
        "STATUS_AGRO",
        "FL_PARTICIPA_RADAR",
        "QT_CLIENTES",
        "PC_BASE"
    )

    .orderBy(
        F.desc("QT_CLIENTES")
    )

)

pdf_20 = mostrar_tabela(
    "20_MATRIZ_FINAL_ELEGIBILIDADE",
    tb_20_matriz_elegibilidade
)


# ============================================================
# 27 CONSOLIDAÇÃO DOS RESULTADOS
# ============================================================

resultados_estudo_radar = {

    "00_RESUMO_BASE":
    tb_00_resumo_base,

    "01_PARTICIPACAO_RADAR":
    tb_01_participacao_radar,

    "02_STATUS_PERFIL_RADAR":
    tb_02_status_perfil,

    "03_CAMPOS_PERFIL_NAO_APTOS":
    tb_03_campos_perfil,

    "04_MOVIMENTACAO_AGRO":
    tb_04_movimentacao_agro,

    "05_VALIDACAO_REGRA_RADAR":
    tb_05_validacao_radar,

    "06_FUNIL_ELEGIBILIDADE_RADAR":
    tb_06_funil,

    "07_MOTIVOS_SOBREPOSTOS":
    tb_07_motivos_sobrepostos,

    "08_MOTIVO_PRINCIPAL":
    tb_08_motivo_principal,

    "09_COMBINACOES_MOTIVOS":
    tb_09_combinacoes_motivos,

    "10_QUANTIDADE_MOTIVOS":
    tb_10_quantidade_motivos,

    "11_PERFIL_APTO_X_RADAR":
    tb_11_perfil_x_radar,

    "12_AGRO_X_RADAR":
    tb_12_agro_x_radar,

    "13_ENTRADAS_X_SAIDAS":
    tb_13_entradas_saidas,

    "14_MOVIMENTACAO_ZERO":
    tb_14_movimentacao_zero,

    "15_SAIDA_ZERO":
    tb_15_saida_zero,

    "16_TRANSACOES_POR_RADAR":
    tb_16_transacoes_por_radar,

    "17_DISTRIBUICAO_TRANSACOES":
    tb_17_distribuicao_transacoes,

    "18_OUTLIERS":
    tb_18_outliers,

    "19_OUTLIERS_X_RADAR":
    tb_19_outliers_x_radar_larga,

    "20_MATRIZ_ELEGIBILIDADE":
    tb_20_matriz_elegibilidade

}

for nome_resultado, tabela_resultado in (
    resultados_estudo_radar.items()
):

    tabela_resultado.createOrReplaceTempView(
        f"VW_{nome_resultado}"
    )


# ============================================================
# 28 RESUMO EXECUTIVO AUTOMÁTICO
# ============================================================

linha_radar_s = (

    pdf_01[
        pdf_01[
            "FL_PARTICIPA_RADAR"
        ]
        ==
        "S"
    ]

)

linha_radar_n = (

    pdf_01[
        pdf_01[
            "FL_PARTICIPA_RADAR"
        ]
        ==
        "N"
    ]

)

qt_radar_s = (
    int(
        linha_radar_s.iloc[0][
            "QT_CLIENTES"
        ]
    )
    if len(linha_radar_s) > 0
    else 0
)

qt_radar_n = (
    int(
        linha_radar_n.iloc[0][
            "QT_CLIENTES"
        ]
    )
    if len(linha_radar_n) > 0
    else 0
)

principal_motivo = (

    pdf_08_nao_participa

    .sort_values(
        "QT_CLIENTES",
        ascending=False
    )

    .iloc[0]

    if len(
        pdf_08_nao_participa
    )
    >
    0

    else None

)

texto_principal_motivo = (

    principal_motivo[
        "DS_MOTIVO_PRINCIPAL"
    ]

    if principal_motivo is not None

    else "NÃO IDENTIFICADO"

)

qt_principal_motivo = (

    int(
        principal_motivo[
            "QT_CLIENTES"
        ]
    )

    if principal_motivo is not None

    else 0

)

insight(
    "RESUMO EXECUTIVO",
    f"""
1. A base possui {formatar_inteiro(QT_TOTAL)} clientes.

2. Participam do Radar:
   {formatar_inteiro(qt_radar_s)}
   ({formatar_percentual(qt_radar_s / QT_TOTAL * 100)}).

3. Não participam do Radar:
   {formatar_inteiro(qt_radar_n)}
   ({formatar_percentual(qt_radar_n / QT_TOTAL * 100)}).

4. O principal motivo exclusivo de não participação é:
   {texto_principal_motivo}

   Clientes nesse motivo:
   {formatar_inteiro(qt_principal_motivo)}
   ({formatar_percentual(qt_principal_motivo / QT_TOTAL * 100)} da base).

5. A validação encontrou:
   {formatar_inteiro(QT_DIVERGENCIA_RADAR)}
   divergências entre a regra recalculada e FL_PARTICIPA_RADAR.

6. As tabelas finais estão disponíveis no dicionário:
   resultados_estudo_radar

7. As mesmas tabelas foram publicadas como views temporárias
   com o prefixo VW_.
"""
)

print("\n")
print("=" * 120)
print("FIM DO ESTUDO EXPLORATÓRIO INICIAL DO RADAR")
print("=" * 120)
print(
    "DataFrame enriquecido disponível em: df_estudo"
)
print(
    "Tabelas consolidadas disponíveis em: resultados_estudo_radar"
)
