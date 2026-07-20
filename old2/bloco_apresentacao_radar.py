%%spark

# ============================================================
# TABELAS E GRÁFICOS PARA A APRESENTAÇÃO
# PARTICIPAÇÃO NO RADAR
# ============================================================

from pyspark.sql import functions as F
from pyspark.sql import Window
from pyspark.storagelevel import StorageLevel

import io
import base64
import pandas as pd
import matplotlib.pyplot as plt

from tabulate import tabulate


# ============================================================
# 00 CONFIGURAÇÕES
# ============================================================

TABELA = "sbx_t2i2016.v1_ana_edu_fin_cli"

LIMPAR_GRAFICOS_ANTES = True
LINHAS_TABELA = 100

# Limites definidos no estudo inicial e usados na apresentação.
CONFIG_TRANSACOES = {
    "QT_TRANS_TOTAL": {
        "TITULO": "Quantidade Total de Transações",
        "Q3": 69,
        "SUPERIORES": [120, 159, 266],
        "OUTLIER": 156,
    },
    "QT_TRANS_ENT": {
        "TITULO": "Quantidade de Transações de Entrada",
        "Q3": 16,
        "SUPERIORES": [28, 41, 87],
        "OUTLIER": 37,
    },
    "QT_TRANS_SAI": {
        "TITULO": "Quantidade de Transações de Saída",
        "Q3": 53,
        "SUPERIORES": [93, 123, 200],
        "OUTLIER": 122,
    },
}

plt.rcParams.update({
    "figure.figsize": (12, 6),
    "axes.titlesize": 14,
    "axes.labelsize": 11,
    "xtick.labelsize": 10,
    "ytick.labelsize": 10,
})


# ============================================================
# 01 REPOSITÓRIO DE GRÁFICOS
# ============================================================

class Graficos:

    def __init__(self):
        self.itens = {}

    def publicar(
        self,
        nome,
        formato="png",
        dpi=150,
        bbox_inches="tight",
        fechar=True,
    ):
        buffer = io.BytesIO()

        plt.savefig(
            buffer,
            format=formato,
            dpi=dpi,
            bbox_inches=bbox_inches,
        )

        if fechar:
            plt.close()

        buffer.seek(0)

        self.itens[nome] = (
            base64.b64encode(
                buffer.read()
            ).decode()
        )

        print(f"✅ {nome}")

    def limpar(self):
        quantidade = len(self.itens)
        self.itens.clear()
        print(f"🗑️ {quantidade} gráfico(s) removido(s)")


if "graficos" not in globals():
    graficos = Graficos()
    print("🚀 Repositório de gráficos criado")


def publicar_grafico(nome, **kwargs):
    graficos.publicar(nome, **kwargs)


def listar_graficos_spark():
    nomes = sorted(graficos.itens.keys())

    print("\n" + "=" * 100)
    print("GRÁFICOS")
    print("=" * 100)

    if not nomes:
        print("⚠️ Nenhum gráfico encontrado")
        return

    for i, nome in enumerate(nomes, start=1):
        print(f"{i:02d} -> {nome}")

    print("\n" + "=" * 100)
    print("COPIE PARA O NOTEBOOK LOCAL")
    print("=" * 100)
    print(f"exibir_grafico_spark({nomes!r})")


if LIMPAR_GRAFICOS_ANTES:
    graficos.limpar()


# ============================================================
# 02 FUNÇÕES PADRÃO
# ============================================================

def formatar_inteiro(valor):
    if valor is None:
        return "0"

    return f"{int(round(float(valor))):,}".replace(",", ".")


def formatar_decimal(valor, casas=2):
    if valor is None:
        return "0,00"

    texto = f"{float(valor):,.{casas}f}"

    return (
        texto
        .replace(",", "X")
        .replace(".", ",")
        .replace("X", ".")
    )


def formatar_percentual(valor, casas=2):
    return f"{float(valor or 0):.{casas}f}%".replace(".", ",")


def mostrar_tabela(titulo, sdf, linhas=LINHAS_TABELA):
    print("\n")
    print("=" * 120)
    print(titulo)
    print("=" * 120)

    pdf = sdf.limit(linhas).toPandas()

    print(
        tabulate(
            pdf,
            headers="keys",
            tablefmt="psql",
            showindex=False,
        )
    )

    print(f"\nTotal de linhas exibidas: {formatar_inteiro(len(pdf))}")

    return pdf


def registrar_tabela(nome, sdf, linhas=LINHAS_TABELA):
    tabelas_apresentacao[nome] = sdf
    sdf.createOrReplaceTempView(f"VW_{nome}")
    return mostrar_tabela(nome, sdf, linhas)


def perfil_valido(coluna):
    return (
        F.upper(
            F.trim(
                F.coalesce(
                    F.col(coluna),
                    F.lit("A CLASSIFICAR"),
                )
            )
        )
        != F.lit("A CLASSIFICAR")
    )


def grafico_rosca(
    pdf,
    coluna_rotulo,
    coluna_valor,
    titulo,
    nome,
):
    figura, eixo = plt.subplots(figsize=(8, 8))

    eixo.pie(
        pdf[coluna_valor],
        labels=pdf[coluna_rotulo],
        autopct="%1.1f%%",
        startangle=90,
        wedgeprops={"width": 0.45},
    )

    eixo.set_title(titulo)
    figura.tight_layout()
    publicar_grafico(nome)


def grafico_barra_horizontal(
    pdf,
    coluna_rotulo,
    coluna_valor,
    coluna_percentual,
    titulo,
    nome,
    eixo_x="Quantidade de clientes",
):
    dados = (
        pdf
        .copy()
        .sort_values(coluna_valor, ascending=True)
    )

    figura, eixo = plt.subplots(figsize=(12, 6))

    barras = eixo.barh(
        dados[coluna_rotulo],
        dados[coluna_valor],
    )

    eixo.set_title(titulo)
    eixo.set_xlabel(eixo_x)

    maior = float(dados[coluna_valor].max()) if len(dados) else 0

    for indice, barra in enumerate(barras):
        quantidade = float(dados.iloc[indice][coluna_valor])
        percentual = float(dados.iloc[indice][coluna_percentual])

        eixo.text(
            quantidade + maior * 0.01,
            barra.get_y() + barra.get_height() / 2,
            f"{formatar_inteiro(quantidade)} ({formatar_percentual(percentual)})",
            va="center",
            fontsize=9,
        )

    if maior > 0:
        eixo.set_xlim(0, maior * 1.30)

    figura.tight_layout()
    publicar_grafico(nome)


def grafico_perfil_100(pdf):
    dados = pdf.copy()

    pivot = (
        dados
        .pivot(
            index="DIMENSAO",
            columns="STATUS",
            values="PC_CLIENTES",
        )
        .fillna(0)
    )

    ordem = [
        "NM_PRFL",
        "NM_MAC_PRFL_CLI",
        "PERFIL COMPLETO",
    ]

    pivot = pivot.reindex([x for x in ordem if x in pivot.index])

    figura, eixo = plt.subplots(figsize=(12, 6))

    pivot.plot(
        kind="barh",
        stacked=True,
        ax=eixo,
    )

    eixo.set_title("Perfil Apto à Regra x A Classificar")
    eixo.set_xlabel("Percentual de clientes")
    eixo.set_ylabel("")
    eixo.set_xlim(0, 100)

    for container in eixo.containers:
        rotulos = [
            f"{barra.get_width():.1f}%"
            if barra.get_width() >= 3
            else ""
            for barra in container
        ]

        eixo.bar_label(
            container,
            labels=rotulos,
            label_type="center",
            fontsize=9,
        )

    eixo.legend(title="Status", bbox_to_anchor=(1.02, 1), loc="upper left")
    figura.tight_layout()
    publicar_grafico("01_PERFIL_CLIENTE_GLOBAL")


def grafico_funil(pdf):
    dados = (
        pdf
        .sort_values("ORDEM", ascending=False)
        .copy()
    )

    figura, eixo = plt.subplots(figsize=(14, 8))

    barras = eixo.barh(
        dados["ETAPA"],
        dados["QT_CLIENTES"],
    )

    eixo.set_title("Funil de Elegibilidade para o Radar")
    eixo.set_xlabel("Quantidade de clientes")

    maior = float(dados["QT_CLIENTES"].max())

    for indice, barra in enumerate(barras):
        quantidade = float(dados.iloc[indice]["QT_CLIENTES"])
        percentual = float(dados.iloc[indice]["PC_BASE"])
        perda = float(dados.iloc[indice]["PERDA_ETAPA"])

        eixo.text(
            quantidade + maior * 0.01,
            barra.get_y() + barra.get_height() / 2,
            f"{formatar_inteiro(quantidade)} ({formatar_percentual(percentual)})",
            va="center",
            fontsize=9,
        )

        if perda > 0:
            eixo.text(
                quantidade * 0.55,
                barra.get_y() + barra.get_height() / 2,
                f"-{formatar_inteiro(perda)}",
                ha="center",
                va="center",
                fontsize=8,
            )

    eixo.set_xlim(0, maior * 1.25)
    figura.tight_layout()
    publicar_grafico("06_FUNIL_ELEGIBILIDADE_RADAR")


def grafico_curiosidade_transacoes(pdf, variavel, titulo, nome):
    dados = (
        pdf[pdf["VARIAVEL"] == variavel]
        .copy()
        .sort_values("ORDEM", ascending=False)
    )

    figura, eixo = plt.subplots(figsize=(12, 7))

    barras = eixo.barh(
        dados["FAIXA"],
        dados["QT_CLIENTES"],
    )

    eixo.set_title(titulo)
    eixo.set_xlabel("Quantidade de clientes")

    maior = float(dados["QT_CLIENTES"].max())

    for indice, barra in enumerate(barras):
        quantidade = float(dados.iloc[indice]["QT_CLIENTES"])
        percentual = float(dados.iloc[indice]["PC_BASE"])

        eixo.text(
            quantidade + maior * 0.01,
            barra.get_y() + barra.get_height() / 2,
            f"{formatar_inteiro(quantidade)} ({formatar_percentual(percentual)})",
            va="center",
            fontsize=9,
        )

    eixo.set_xlim(0, maior * 1.30)
    figura.tight_layout()
    publicar_grafico(nome)


def grafico_outliers_x_radar(pdf):
    dados = pdf[pdf["FL_PARTICIPA_RADAR"] == "S"].copy()

    pivot = (
        dados
        .pivot(
            index="VARIAVEL",
            columns="STATUS_OUTLIER",
            values="PC_DENTRO_GRUPO",
        )
        .fillna(0)
    )

    ordem = [
        "QT_TRANS_TOTAL",
        "QT_TRANS_ENT",
        "QT_TRANS_SAI",
    ]

    pivot = pivot.reindex([x for x in ordem if x in pivot.index])

    figura, eixo = plt.subplots(figsize=(12, 6))

    pivot.plot(
        kind="bar",
        ax=eixo,
    )

    eixo.set_title("Participação no Radar: Outliers x Não Outliers")
    eixo.set_xlabel("")
    eixo.set_ylabel("Percentual que participa do Radar")
    eixo.set_ylim(0, 100)
    plt.xticks(rotation=0)

    for container in eixo.containers:
        rotulos = [f"{barra.get_height():.1f}%" for barra in container]
        eixo.bar_label(container, labels=rotulos, padding=3, fontsize=8)

    eixo.legend(title="Grupo")
    figura.tight_layout()
    publicar_grafico("12_OUTLIERS_X_RADAR")


# ============================================================
# 03 CARGA DA ÚLTIMA EXECUÇÃO
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
    "DT_REF_INI",
    "DT_REF_FIM",
]

origem = spark.table(TABELA)

colunas_ausentes = sorted(set(colunas_necessarias) - set(origem.columns))

if colunas_ausentes:
    raise ValueError(
        "Colunas obrigatórias ausentes: "
        + ", ".join(colunas_ausentes)
    )

DT_EXEA_REFERENCIA = origem.agg(F.max("DT_EXEA").alias("DT_EXEA")).first()["DT_EXEA"]

base = (
    origem
    .filter(F.col("DT_EXEA") == F.lit(DT_EXEA_REFERENCIA))
    .select(*colunas_necessarias)
)


# ============================================================
# 04 REGRAS DO RADAR
# ============================================================

regra_qt_total = F.coalesce(F.col("QT_TRANS_TOTAL"), F.lit(0)) > 0
regra_qt_entrada = F.coalesce(F.col("QT_TRANS_ENT"), F.lit(0)) > 0
regra_qt_saida = F.coalesce(F.col("QT_TRANS_SAI"), F.lit(0)) > 0
regra_vl_entrada = F.coalesce(F.col("VL_TRANS_ENT"), F.lit(0)) > 0
regra_vl_saida = F.coalesce(F.col("VL_TRANS_SAI"), F.lit(0)) > 0

regra_nm_prfl = perfil_valido("NM_PRFL")
regra_nm_macro = perfil_valido("NM_MAC_PRFL_CLI")
regra_nm_micro = perfil_valido("NM_MIC_PRFL_CLI")
regra_nm_fin = perfil_valido("NM_PRFL_FIN")

regra_perfil_apto = (
    regra_nm_prfl
    & regra_nm_macro
    & regra_nm_micro
    & regra_nm_fin
)

regra_sem_agro = (
    F.upper(
        F.trim(
            F.coalesce(
                F.col("FL_TEM_MOV_AGRO"),
                F.lit("N"),
            )
        )
    )
    == F.lit("N")
)

regra_transacional = (
    regra_qt_total
    & regra_qt_entrada
    & regra_qt_saida
    & regra_vl_entrada
    & regra_vl_saida
)

regra_radar = regra_transacional & regra_perfil_apto & regra_sem_agro


df = (
    base
    .withColumn(
        "ST_PERFIL_APTO",
        F.when(regra_perfil_apto, "PERFIL APTO À REGRA")
        .otherwise("A CLASSIFICAR"),
    )
    .withColumn(
        "ST_AGRO",
        F.when(regra_sem_agro, "SEM MOVIMENTAÇÃO AGRO")
        .otherwise("COM MOVIMENTAÇÃO AGRO"),
    )
    .withColumn(
        "FL_RADAR_RECALCULADO",
        F.when(regra_radar, "S").otherwise("N"),
    )
    .withColumn(
        "DS_MOTIVO_PRINCIPAL",
        F.when(~regra_qt_total, "01. SEM TRANSAÇÃO TOTAL")
        .when(~regra_qt_entrada, "02. SEM ENTRADA")
        .when(~regra_qt_saida, "03. SEM SAÍDA")
        .when(~regra_vl_entrada, "04. VALOR DE ENTRADA ZERO")
        .when(~regra_vl_saida, "05. VALOR DE SAÍDA ZERO")
        .when(~regra_perfil_apto, "06. SEM PERFIL APTO")
        .when(~regra_sem_agro, "07. MOVIMENTAÇÃO AGRO")
        .otherwise("08. PARTICIPA DO RADAR"),
    )
    .persist(StorageLevel.MEMORY_AND_DISK)
)


# ============================================================
# 05 CONTROLES GERAIS
# ============================================================

controle = (
    df
    .agg(
        F.count("*").alias("QT_TOTAL"),
        F.countDistinct("CD_CLI").alias("QT_CLIENTES_DISTINTOS"),
        F.min("DT_REF_INI").alias("DT_REF_INI"),
        F.max("DT_REF_FIM").alias("DT_REF_FIM"),
        F.sum(
            F.when(
                F.col("FL_PARTICIPA_RADAR") != F.col("FL_RADAR_RECALCULADO"),
                1,
            ).otherwise(0)
        ).alias("QT_DIVERGENCIAS"),
        F.sum(
            F.when(
                F.upper(F.trim(F.coalesce(F.col("NM_PRFL"), F.lit(""))))
                == "SEM PERFIL",
                1,
            ).otherwise(0)
        ).alias("QT_SEM_PERFIL_ACEITO"),
    )
    .first()
)

QT_TOTAL = int(controle["QT_TOTAL"])
QT_CLIENTES_DISTINTOS = int(controle["QT_CLIENTES_DISTINTOS"])
QT_DIVERGENCIAS = int(controle["QT_DIVERGENCIAS"] or 0)
QT_SEM_PERFIL_ACEITO = int(controle["QT_SEM_PERFIL_ACEITO"] or 0)

if QT_TOTAL != QT_CLIENTES_DISTINTOS:
    raise ValueError(
        "A execução selecionada possui mais de uma linha por cliente. "
        f"Registros={QT_TOTAL}; clientes={QT_CLIENTES_DISTINTOS}."
    )

print("\n" + "=" * 120)
print("BASE DA APRESENTAÇÃO")
print("=" * 120)
print(f"Tabela...............: {TABELA}")
print(f"Execução.............: {DT_EXEA_REFERENCIA}")
print(f"Período..............: {controle['DT_REF_INI']} a {controle['DT_REF_FIM']}")
print(f"Clientes.............: {formatar_inteiro(QT_TOTAL)}")
print(f"Divergências Radar...: {formatar_inteiro(QT_DIVERGENCIAS)}")


tabelas_apresentacao = {}


# ============================================================
# 06 TABELA 00 | RESUMO DA BASE
# ============================================================

resumo_linha = (
    df
    .agg(
        F.count("*").alias("QT_CLIENTES"),
        F.min("DT_REF_INI").alias("DT_REF_INI"),
        F.max("DT_REF_FIM").alias("DT_REF_FIM"),
        F.sum(F.when(regra_perfil_apto, 1).otherwise(0)).alias("QT_PERFIL_APTO"),
        F.sum(F.when(~regra_perfil_apto, 1).otherwise(0)).alias("QT_SEM_PERFIL_APTO"),
        F.sum(F.when(~regra_sem_agro, 1).otherwise(0)).alias("QT_COM_AGRO"),
        F.sum(F.when(F.col("FL_PARTICIPA_RADAR") == "S", 1).otherwise(0)).alias("QT_PARTICIPA"),
        F.sum(F.when(F.col("FL_PARTICIPA_RADAR") == "N", 1).otherwise(0)).alias("QT_NAO_PARTICIPA"),
    )
)

pdf_00 = registrar_tabela(
    "00_RESUMO_BASE",
    resumo_linha,
)


# ============================================================
# 07 TABELA 01 | PERFIL GLOBAL
# ============================================================

perfil_controle = (
    df
    .agg(
        F.sum(F.when(regra_nm_prfl, 1).otherwise(0)).alias("NM_PRFL_APTO"),
        F.sum(F.when(~regra_nm_prfl, 1).otherwise(0)).alias("NM_PRFL_CLASSIFICAR"),
        F.sum(F.when(regra_nm_macro, 1).otherwise(0)).alias("NM_MACRO_APTO"),
        F.sum(F.when(~regra_nm_macro, 1).otherwise(0)).alias("NM_MACRO_CLASSIFICAR"),
        F.sum(F.when(regra_perfil_apto, 1).otherwise(0)).alias("PERFIL_COMPLETO_APTO"),
        F.sum(F.when(~regra_perfil_apto, 1).otherwise(0)).alias("PERFIL_COMPLETO_CLASSIFICAR"),
    )
    .first()
)

linhas_perfil = [
    (1, "NM_PRFL", "PERFIL APTO À REGRA", int(perfil_controle["NM_PRFL_APTO"] or 0)),
    (1, "NM_PRFL", "A CLASSIFICAR", int(perfil_controle["NM_PRFL_CLASSIFICAR"] or 0)),
    (2, "NM_MAC_PRFL_CLI", "PERFIL APTO À REGRA", int(perfil_controle["NM_MACRO_APTO"] or 0)),
    (2, "NM_MAC_PRFL_CLI", "A CLASSIFICAR", int(perfil_controle["NM_MACRO_CLASSIFICAR"] or 0)),
    (3, "PERFIL COMPLETO", "PERFIL APTO À REGRA", int(perfil_controle["PERFIL_COMPLETO_APTO"] or 0)),
    (3, "PERFIL COMPLETO", "A CLASSIFICAR", int(perfil_controle["PERFIL_COMPLETO_CLASSIFICAR"] or 0)),
]

tb_01 = (
    spark
    .createDataFrame(
        linhas_perfil,
        ["ORDEM", "DIMENSAO", "STATUS", "QT_CLIENTES"],
    )
    .withColumn(
        "PC_CLIENTES",
        F.round(F.col("QT_CLIENTES") / F.lit(QT_TOTAL) * 100, 2),
    )
    .orderBy("ORDEM", "STATUS")
)

pdf_01 = registrar_tabela("01_PERFIL_CLIENTE_GLOBAL", tb_01)
grafico_perfil_100(pdf_01)

print(
    "\nOBSERVAÇÃO | NM_PRFL = SEM PERFIL é aceito pela regra oficial: "
    f"{formatar_inteiro(QT_SEM_PERFIL_ACEITO)} cliente(s)."
)


# ============================================================
# 08 TABELA 02 | MOVIMENTAÇÃO AGRO
# ============================================================

tb_02 = (
    df
    .groupBy("ST_AGRO")
    .agg(F.count("*").alias("QT_CLIENTES"))
    .withColumn(
        "PC_CLIENTES",
        F.round(F.col("QT_CLIENTES") / F.lit(QT_TOTAL) * 100, 2),
    )
    .orderBy(F.desc("QT_CLIENTES"))
)

pdf_02 = registrar_tabela("02_MOVIMENTACAO_AGRO", tb_02)

grafico_rosca(
    pdf_02,
    "ST_AGRO",
    "QT_CLIENTES",
    "Movimentação Agro",
    "02_MOVIMENTACAO_AGRO",
)


# ============================================================
# 09 TABELA 03 | ENTRADAS X SAÍDAS
# ============================================================

linha_transacoes = (
    df
    .agg(
        F.sum("QT_TRANS_ENT").alias("QT_ENTRADAS"),
        F.sum("QT_TRANS_SAI").alias("QT_SAIDAS"),
    )
    .first()
)

qt_entradas = int(linha_transacoes["QT_ENTRADAS"] or 0)
qt_saidas = int(linha_transacoes["QT_SAIDAS"] or 0)
qt_movimentos = qt_entradas + qt_saidas

linhas_transacoes = [
    (
        "ENTRADAS",
        qt_entradas,
        float(qt_entradas / qt_movimentos * 100 if qt_movimentos else 0),
        float(qt_entradas / QT_TOTAL if QT_TOTAL else 0),
    ),
    (
        "SAÍDAS",
        qt_saidas,
        float(qt_saidas / qt_movimentos * 100 if qt_movimentos else 0),
        float(qt_saidas / QT_TOTAL if QT_TOTAL else 0),
    ),
]

tb_03 = spark.createDataFrame(
    linhas_transacoes,
    ["TIPO_TRANSACAO", "QT_TRANSACOES", "PC_TRANSACOES", "MEDIA_POR_CLIENTE"],
)

pdf_03 = registrar_tabela("03_ENTRADAS_X_SAIDAS", tb_03)

grafico_barra_horizontal(
    pdf_03,
    "TIPO_TRANSACAO",
    "QT_TRANSACOES",
    "PC_TRANSACOES",
    "Quantidade de Transações: Entradas x Saídas",
    "03_ENTRADAS_X_SAIDAS",
    "Quantidade de transações",
)


# ============================================================
# 10 TABELA 04 | ENTRADA E SAÍDA ZERO
# ============================================================

linha_zero = (
    df
    .agg(
        F.sum(F.when(F.col("QT_TRANS_ENT") == 0, 1).otherwise(0)).alias("ENTRADA_ZERO"),
        F.sum(F.when(F.col("QT_TRANS_SAI") == 0, 1).otherwise(0)).alias("SAIDA_ZERO"),
        F.sum(
            F.when(
                (F.col("QT_TRANS_ENT") == 0) & (F.col("QT_TRANS_SAI") == 0),
                1,
            ).otherwise(0)
        ).alias("ENTRADA_E_SAIDA_ZERO"),
    )
    .first()
)

linhas_zero = [
    (1, "QT_TRANS_ENT = 0", int(linha_zero["ENTRADA_ZERO"] or 0)),
    (2, "QT_TRANS_SAI = 0", int(linha_zero["SAIDA_ZERO"] or 0)),
    (3, "ENTRADA E SAÍDA = 0", int(linha_zero["ENTRADA_E_SAIDA_ZERO"] or 0)),
]

tb_04 = (
    spark
    .createDataFrame(linhas_zero, ["ORDEM", "CONDICAO", "QT_CLIENTES"])
    .withColumn(
        "PC_CLIENTES",
        F.round(F.col("QT_CLIENTES") / F.lit(QT_TOTAL) * 100, 2),
    )
    .orderBy("ORDEM")
)

pdf_04 = registrar_tabela("04_ENTRADA_SAIDA_ZERO", tb_04)

grafico_barra_horizontal(
    pdf_04,
    "CONDICAO",
    "QT_CLIENTES",
    "PC_CLIENTES",
    "Clientes sem Entrada ou sem Saída",
    "04_ENTRADA_SAIDA_ZERO",
)


# ============================================================
# 11 TABELAS 05 E 06 | ANÁLISE DE SAÍDA ZERO
# ============================================================

df_saida_zero = df.filter(F.col("QT_TRANS_SAI") == 0)

linha_saida_zero = (
    df_saida_zero
    .agg(
        F.count("*").alias("QT_CLIENTES_SAIDA_ZERO"),
        F.sum(F.when(F.col("QT_TRANS_ENT") > 0, 1).otherwise(0)).alias("QT_COM_ENTRADA"),
        F.sum(F.when(F.col("QT_TRANS_ENT") == 0, 1).otherwise(0)).alias("QT_SEM_ENTRADA"),
        F.sum("QT_TRANS_ENT").alias("QT_TOTAL_ENTRADAS"),
        F.avg("QT_TRANS_ENT").alias("MEDIA_ENTRADAS"),
        F.percentile_approx("QT_TRANS_ENT", [0.50, 0.75, 0.95], 10000).alias("PERCENTIS"),
    )
    .first()
)

percentis_saida_zero = linha_saida_zero["PERCENTIS"] or [0, 0, 0]

linhas_saida_zero_resumo = [
    (
        int(linha_saida_zero["QT_CLIENTES_SAIDA_ZERO"] or 0),
        int(linha_saida_zero["QT_COM_ENTRADA"] or 0),
        int(linha_saida_zero["QT_SEM_ENTRADA"] or 0),
        int(linha_saida_zero["QT_TOTAL_ENTRADAS"] or 0),
        float(linha_saida_zero["MEDIA_ENTRADAS"] or 0),
        int(percentis_saida_zero[0] or 0),
        int(percentis_saida_zero[1] or 0),
        int(percentis_saida_zero[2] or 0),
    )
]

tb_05 = spark.createDataFrame(
    linhas_saida_zero_resumo,
    [
        "QT_CLIENTES_SAIDA_ZERO",
        "QT_COM_ENTRADA",
        "QT_SEM_ENTRADA",
        "QT_TOTAL_ENTRADAS",
        "MEDIA_ENTRADAS",
        "MEDIANA_ENTRADAS",
        "P75_ENTRADAS",
        "P95_ENTRADAS",
    ],
)

pdf_05 = registrar_tabela("05_SAIDA_ZERO_RESUMO", tb_05)

ordem_faixas = F.when(F.col("QT_TRANS_ENT") == 0, 1) \
    .when(F.col("QT_TRANS_ENT") <= 5, 2) \
    .when(F.col("QT_TRANS_ENT") <= 10, 3) \
    .when(F.col("QT_TRANS_ENT") <= 20, 4) \
    .otherwise(5)

nome_faixas = F.when(F.col("QT_TRANS_ENT") == 0, "0") \
    .when(F.col("QT_TRANS_ENT") <= 5, "1 a 5") \
    .when(F.col("QT_TRANS_ENT") <= 10, "6 a 10") \
    .when(F.col("QT_TRANS_ENT") <= 20, "11 a 20") \
    .otherwise("Mais de 20")

tb_06 = (
    df_saida_zero
    .withColumn("ORDEM", ordem_faixas)
    .withColumn("FAIXA_ENTRADAS", nome_faixas)
    .groupBy("ORDEM", "FAIXA_ENTRADAS")
    .agg(F.count("*").alias("QT_CLIENTES"))
    .withColumn(
        "PC_CLIENTES",
        F.round(
            F.col("QT_CLIENTES")
            / F.lit(int(linha_saida_zero["QT_CLIENTES_SAIDA_ZERO"] or 0))
            * 100,
            2,
        ),
    )
    .orderBy("ORDEM")
)

pdf_06 = registrar_tabela("06_SAIDA_ZERO_FAIXAS_ENTRADA", tb_06)

grafico_barra_horizontal(
    pdf_06,
    "FAIXA_ENTRADAS",
    "QT_CLIENTES",
    "PC_CLIENTES",
    "Entradas dos Clientes com Saída Igual a Zero",
    "05_SAIDA_ZERO_FAIXAS_ENTRADA",
)


# ============================================================
# 12 TABELA 07 | FUNIL DE ELEGIBILIDADE
# ============================================================

condicoes_funil = [
    (1, "Base analisada", F.lit(True)),
    (2, "Quantidade total positiva", regra_qt_total),
    (3, "Com quantidade de entrada", regra_qt_total & regra_qt_entrada),
    (4, "Com quantidade de saída", regra_qt_total & regra_qt_entrada & regra_qt_saida),
    (
        5,
        "Com valor de entrada positivo",
        regra_qt_total & regra_qt_entrada & regra_qt_saida & regra_vl_entrada,
    ),
    (6, "Com valor de saída positivo", regra_transacional),
    (7, "Com perfil apto", regra_transacional & regra_perfil_apto),
    (8, "Participa do Radar — sem Agro", regra_radar),
]

linha_funil = (
    df
    .agg(
        *[
            F.sum(F.when(condicao, 1).otherwise(0)).alias(f"ETAPA_{ordem}")
            for ordem, _, condicao in condicoes_funil
        ]
    )
    .first()
)

linhas_funil = []
quantidade_anterior = None

for ordem, etapa, _ in condicoes_funil:
    quantidade = int(linha_funil[f"ETAPA_{ordem}"] or 0)
    perda = 0 if quantidade_anterior is None else quantidade_anterior - quantidade

    linhas_funil.append(
        (
            ordem,
            etapa,
            quantidade,
            float(quantidade / QT_TOTAL * 100 if QT_TOTAL else 0),
            int(perda),
            float(
                quantidade / quantidade_anterior * 100
                if quantidade_anterior
                else 100
            ),
        )
    )

    quantidade_anterior = quantidade

tb_07 = (
    spark
    .createDataFrame(
        linhas_funil,
        [
            "ORDEM",
            "ETAPA",
            "QT_CLIENTES",
            "PC_BASE",
            "PERDA_ETAPA",
            "PC_RETENCAO_ETAPA",
        ],
    )
    .orderBy("ORDEM")
)

pdf_07 = registrar_tabela("07_FUNIL_ELEGIBILIDADE_RADAR", tb_07)
grafico_funil(pdf_07)


# ============================================================
# 13 TABELA 08 | MOTIVO PRINCIPAL
# ============================================================

QT_NAO_PARTICIPA = df.filter(F.col("FL_RADAR_RECALCULADO") == "N").count()

tb_08 = (
    df
    .filter(F.col("FL_RADAR_RECALCULADO") == "N")
    .groupBy("DS_MOTIVO_PRINCIPAL")
    .agg(F.count("*").alias("QT_CLIENTES"))
    .withColumn(
        "PC_NAO_PARTICIPANTES",
        F.round(F.col("QT_CLIENTES") / F.lit(QT_NAO_PARTICIPA) * 100, 2),
    )
    .withColumn(
        "PC_BASE",
        F.round(F.col("QT_CLIENTES") / F.lit(QT_TOTAL) * 100, 2),
    )
    .orderBy(F.desc("QT_CLIENTES"))
)

pdf_08 = registrar_tabela("08_MOTIVO_PRINCIPAL_NAO_PARTICIPACAO", tb_08)

grafico_barra_horizontal(
    pdf_08,
    "DS_MOTIVO_PRINCIPAL",
    "QT_CLIENTES",
    "PC_NAO_PARTICIPANTES",
    "Motivo Principal de Não Participação",
    "07_MOTIVO_PRINCIPAL_NAO_PARTICIPACAO",
)


# ============================================================
# 14 TABELA 09 | RESULTADO FINAL DO RADAR
# ============================================================

tb_09 = (
    df
    .withColumn(
        "RESULTADO_RADAR",
        F.when(F.col("FL_PARTICIPA_RADAR") == "S", "PARTICIPA")
        .otherwise("NÃO PARTICIPA"),
    )
    .groupBy("RESULTADO_RADAR")
    .agg(F.count("*").alias("QT_CLIENTES"))
    .withColumn(
        "PC_CLIENTES",
        F.round(F.col("QT_CLIENTES") / F.lit(QT_TOTAL) * 100, 2),
    )
    .orderBy(F.desc("QT_CLIENTES"))
)

pdf_09 = registrar_tabela("09_RESULTADO_FINAL_RADAR", tb_09)

grafico_rosca(
    pdf_09,
    "RESULTADO_RADAR",
    "QT_CLIENTES",
    "Resultado Final de Participação no Radar",
    "08_RESULTADO_FINAL_RADAR",
)


# ============================================================
# 15 TABELA 10 | CURIOSIDADES TRANSACIONAIS
# ============================================================

linhas_curiosidades = []

for variavel, config in CONFIG_TRANSACOES.items():
    q3 = int(config["Q3"])
    superior_1, superior_2, superior_3 = [int(x) for x in config["SUPERIORES"]]
    limite_outlier = int(config["OUTLIER"])

    linha = (
        df
        .agg(
            F.sum(F.when(F.col(variavel) <= q3, 1).otherwise(0)).alias("ATE_Q3"),
            F.sum(F.when(F.col(variavel) > q3, 1).otherwise(0)).alias("ACIMA_Q3"),
            F.sum(F.when(F.col(variavel) > superior_1, 1).otherwise(0)).alias("SUPERIOR_1"),
            F.sum(F.when(F.col(variavel) > superior_2, 1).otherwise(0)).alias("SUPERIOR_2"),
            F.sum(F.when(F.col(variavel) > superior_3, 1).otherwise(0)).alias("SUPERIOR_3"),
            F.sum(F.when(F.col(variavel) > limite_outlier, 1).otherwise(0)).alias("OUTLIER"),
        )
        .first()
    )

    faixas = [
        (1, "DISTRIBUIÇÃO", f"Até {q3}", int(linha["ATE_Q3"] or 0)),
        (2, "DISTRIBUIÇÃO", f"Mais de {q3}", int(linha["ACIMA_Q3"] or 0)),
        (3, "FAIXA SUPERIOR", f"Mais de {superior_1}", int(linha["SUPERIOR_1"] or 0)),
        (4, "FAIXA SUPERIOR", f"Mais de {superior_2}", int(linha["SUPERIOR_2"] or 0)),
        (5, "FAIXA SUPERIOR", f"Mais de {superior_3}", int(linha["SUPERIOR_3"] or 0)),
        (6, "OUTLIER", f"Outlier: acima de {limite_outlier}", int(linha["OUTLIER"] or 0)),
    ]

    for ordem, tipo_faixa, faixa, quantidade in faixas:
        linhas_curiosidades.append(
            (
                variavel,
                config["TITULO"],
                ordem,
                tipo_faixa,
                faixa,
                quantidade,
                float(quantidade / QT_TOTAL * 100 if QT_TOTAL else 0),
            )
        )

tb_10 = (
    spark
    .createDataFrame(
        linhas_curiosidades,
        [
            "VARIAVEL",
            "TITULO",
            "ORDEM",
            "TIPO_FAIXA",
            "FAIXA",
            "QT_CLIENTES",
            "PC_BASE",
        ],
    )
    .orderBy("VARIAVEL", "ORDEM")
)

pdf_10 = registrar_tabela("10_CURIOSIDADES_TRANSACOES", tb_10, linhas=100)

grafico_curiosidade_transacoes(
    pdf_10,
    "QT_TRANS_TOTAL",
    "Curiosidades — Quantidade Total de Transações",
    "09_CURIOSIDADE_QT_TRANS_TOTAL",
)

grafico_curiosidade_transacoes(
    pdf_10,
    "QT_TRANS_ENT",
    "Curiosidades — Transações de Entrada",
    "10_CURIOSIDADE_QT_TRANS_ENT",
)

grafico_curiosidade_transacoes(
    pdf_10,
    "QT_TRANS_SAI",
    "Curiosidades — Transações de Saída",
    "11_CURIOSIDADE_QT_TRANS_SAI",
)


# ============================================================
# 16 TABELA 11 | OUTLIERS X RADAR
# ============================================================

outliers_union = None

for variavel, config in CONFIG_TRANSACOES.items():
    limite = int(config["OUTLIER"])

    parcial = (
        df
        .withColumn(
            "STATUS_OUTLIER",
            F.when(F.col(variavel) > limite, "OUTLIER")
            .otherwise("NÃO OUTLIER"),
        )
        .groupBy("STATUS_OUTLIER", "FL_PARTICIPA_RADAR")
        .agg(F.count("*").alias("QT_CLIENTES"))
        .withColumn("VARIAVEL", F.lit(variavel))
        .withColumn("LIMITE_OUTLIER", F.lit(limite))
        .select(
            "VARIAVEL",
            "LIMITE_OUTLIER",
            "STATUS_OUTLIER",
            "FL_PARTICIPA_RADAR",
            "QT_CLIENTES",
        )
    )

    outliers_union = parcial if outliers_union is None else outliers_union.unionByName(parcial)

janela_outlier = Window.partitionBy("VARIAVEL", "STATUS_OUTLIER")

tb_11 = (
    outliers_union
    .withColumn(
        "PC_DENTRO_GRUPO",
        F.round(
            F.col("QT_CLIENTES")
            / F.sum("QT_CLIENTES").over(janela_outlier)
            * 100,
            2,
        ),
    )
    .orderBy("VARIAVEL", "STATUS_OUTLIER", "FL_PARTICIPA_RADAR")
)

pdf_11 = registrar_tabela("11_OUTLIERS_X_RADAR", tb_11, linhas=100)
grafico_outliers_x_radar(pdf_11)


# ============================================================
# 17 VALIDAÇÃO DA REGRA
# ============================================================

if QT_DIVERGENCIAS > 0:
    tb_validacao = (
        df
        .groupBy("FL_PARTICIPA_RADAR", "FL_RADAR_RECALCULADO")
        .agg(F.count("*").alias("QT_CLIENTES"))
        .orderBy("FL_PARTICIPA_RADAR", "FL_RADAR_RECALCULADO")
    )

    registrar_tabela("99_VALIDACAO_REGRA_RADAR", tb_validacao)

    print(
        "\n⚠️ ATENÇÃO: existem divergências entre a flag gravada "
        "e a regra recalculada."
    )
else:
    print("\n✅ Regra do Radar reproduzida sem divergências.")


# ============================================================
# 18 RESULTADO FINAL
# ============================================================

print("\n" + "=" * 120)
print("RESULTADO FINAL")
print("=" * 120)
print(f"Tabelas geradas.: {len(tabelas_apresentacao)}")
print(f"Gráficos gerados: {len(graficos.itens)}")
print("\nViews temporárias disponíveis:")

for nome in tabelas_apresentacao:
    print(f"- VW_{nome}")

print("\nLIMITAÇÃO")
print(
    "A tabela atual não possui o nome individual das transações. "
    "Por isso, o Top 5 de transações de entrada e saída não é gerado neste bloco."
)

listar_graficos_spark()
