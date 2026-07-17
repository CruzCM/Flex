%%spark

from pyspark.sql import functions as F

# Camada de explicabilidade da persona financeira.
# A tabela de origem deve conter as pontuacoes ja calculadas pelo fluxo original.
# Por padrao, a leitura textual da V1 usa a tabela historica v1_ana_edu_fin_cli.
tabela_origem = globals().get("tabela_spark", "sbx_t2i2016.v1_ana_edu_fin_cli")
df = spark.table(tabela_origem)

# ============================================================
# 1. PERCENTUAIS DERIVADOS DE SAIDA
# ============================================================
sem_saida_total = F.coalesce(F.col("VL_SAI_TOTAL"), F.lit(0)) == 0
den_saida = F.when(sem_saida_total, F.lit(None)).otherwise(F.col("VL_SAI_TOTAL"))

def pc_saida(coluna_valor):
    return F.when(
        sem_saida_total,
        F.lit(0.0)
    ).otherwise(
        F.round(F.coalesce(F.col(coluna_valor), F.lit(0.0)) / den_saida * 100, 2)
    )

df = (
    df
    .withColumn("PC_SAI_GEN",  pc_saida("VL_SAI_GEN"))
    .withColumn("PC_SAI_ESS",  pc_saida("VL_SAI_ESS"))
    .withColumn("PC_SAI_FLEX", pc_saida("VL_SAI_FLEX"))
    .withColumn("PC_SAI_RES",  pc_saida("VL_SAI_RES"))
    .withColumn("PC_SAI_CRED", pc_saida("VL_SAI_DIV"))
)

# ============================================================
# 2. TEXTOS DAS REGRAS DE CONCENTRACAO
# ============================================================
sem_saida_txt = "sem saida total no periodo; pontuacao de concentracao igual a 0"

df = (
    df
    .withColumn(
        "TX_REGRA_CONC_GEN",
        F.when(sem_saida_total, sem_saida_txt)
         .when(F.col("NR_PONT_CONC_GEN") == 0, "ficou menor ou igual a referencia de 75,00%")
         .when(F.col("NR_PONT_CONC_GEN") == 99, "ficou acima da referencia de 75,00%")
         .otherwise("regra de categorizacao nao identificada")
    )
    .withColumn(
        "TX_REGRA_CONC_ESS",
        F.when(sem_saida_total, sem_saida_txt)
         .when(F.col("NR_PONT_CONC_ESS") == 0, "ficou abaixo de 50,00%")
         .when(F.col("NR_PONT_CONC_ESS") == 1, "ficou maior ou igual a 50,00% e menor que 75,00%")
         .when(F.col("NR_PONT_CONC_ESS") == 2, "ficou maior ou igual a 75,00%")
         .otherwise("regra de essenciais nao identificada")
    )
    .withColumn(
        "TX_REGRA_CONC_FLEX",
        F.when(sem_saida_total, sem_saida_txt)
         .when(F.col("NR_PONT_CONC_FLEX") == 0, "ficou abaixo de 30,00%")
         .when(F.col("NR_PONT_CONC_FLEX") == 1, "ficou maior ou igual a 30,00% e menor que 45,00%")
         .when(F.col("NR_PONT_CONC_FLEX") == 2, "ficou maior ou igual a 45,00%")
         .otherwise("regra de flexiveis nao identificada")
    )
    .withColumn(
        "TX_REGRA_CONC_RES",
        F.when(sem_saida_total, sem_saida_txt)
         .when(F.col("NR_PONT_CONC_RES") == 0, "ficou maior ou igual a 30,00%")
         .when(F.col("NR_PONT_CONC_RES") == 1, "ficou maior ou igual a 20,00% e menor que 30,00%")
         .when(F.col("NR_PONT_CONC_RES") == 2, "ficou abaixo de 20,00%")
         .otherwise("regra de reserva nao identificada")
    )
    .withColumn(
        "TX_REGRA_CONC_CRED",
        F.when(sem_saida_total, sem_saida_txt)
         .when(F.col("NR_PONT_CONC_CRED") == 0, "ficou abaixo de 30,00%")
         .when(F.col("NR_PONT_CONC_CRED") == 1, "ficou maior ou igual a 30,00% e menor que 45,00%")
         .when(F.col("NR_PONT_CONC_CRED") == 2, "ficou maior ou igual a 45,00%")
         .otherwise("regra de credito nao identificada")
    )
)

# ============================================================
# 3. TEXTOS DO RESULTADO ORCAMENTARIO
# ============================================================
sem_entrada_total = F.coalesce(F.col("VL_ENT_TOTAL"), F.lit(0)) == 0
tem_saida_total = F.coalesce(F.col("VL_SAI_TOTAL"), F.lit(0)) > 0

pc_sai_ent_pct = F.coalesce(F.col("PC_SAI_ENT"), F.lit(0.0)) * 100

df = df.withColumn(
    "TX_REGRA_RESULTADO",
    F.when(sem_entrada_total & ~tem_saida_total, "sem entradas e sem saidas no periodo")
     .when(sem_entrada_total & tem_saida_total, "sem entrada registrada e com saida no periodo")
     .when(F.col("PC_SAI_ENT") < 0.75,  "comprometimento abaixo de 75,00%")
     .when(F.col("PC_SAI_ENT") < 0.95,  "comprometimento de 75,00% a 95,00%")
     .when(F.col("PC_SAI_ENT") < 1.00,  "comprometimento de 95,00% a 100,00%")
     .when(F.col("PC_SAI_ENT") <= 1.05, "comprometimento de 100,00% a 105,00%")
     .when(F.col("PC_SAI_ENT") <= 1.25, "comprometimento de 105,00% a 125,00%")
     .otherwise("comprometimento acima de 125,00%")
)

df = (
    df
    .withColumn(
        "TX_LEITURA_MOVIMENTACAO",
        F.when(
            sem_entrada_total & ~tem_saida_total,
            "nao houve movimentacao financeira suficiente para avaliar entradas e saidas"
        ).when(
            sem_entrada_total & tem_saida_total,
            "houve saidas sem entrada registrada, indicando pressao financeira no periodo"
        ).when(
            F.col("CD_RES_ORC") == 1,
            "o periodo fechou com sobra financeira, criando espaco para organizacao ou reserva"
        ).when(
            (F.col("CD_RES_ORC") == 0) & (F.col("VL_RES_ORC") > 0),
            "o periodo ficou proximo do equilibrio, com pequena sobra financeira"
        ).when(
            (F.col("CD_RES_ORC") == 0) & (F.col("VL_RES_ORC") < 0),
            "o periodo ficou proximo do equilibrio, com saidas um pouco acima das entradas"
        ).when(
            F.col("CD_RES_ORC") == 0,
            "o periodo ficou equilibrado entre entradas e saidas"
        ).when(
            F.col("CD_RES_ORC") == 2,
            "o periodo fechou com deficit, indicando necessidade de atencao ao orcamento"
        ).otherwise("resultado financeiro do periodo nao classificado")
    )
    .withColumn(
        "TX_LEITURA_CONC_GEN",
        F.when(sem_saida_total, "sem saidas no periodo para avaliar a qualidade da categorizacao")
         .when(F.col("NR_PONT_CONC_GEN") == 0, "alta categorizacao do gasto. A parcela de saidas genericas ficou dentro do limite aceito, deixando a leitura do periodo mais confiavel")
         .when(F.col("NR_PONT_CONC_GEN") == 99, "baixa categorizacao do gasto. Uma parcela elevada das saidas ficou generica ou nao classificada, reduzindo a qualidade da leitura")
         .otherwise("qualidade de categorizacao nao classificada")
    )
    .withColumn(
        "TX_LEITURA_CONC_ESS",
        F.when(sem_saida_total, "sem saidas no periodo para avaliar despesas essenciais")
         .when(F.col("NR_PONT_CONC_ESS") == 0, "baixa concentracao de despesas essenciais. Os gastos essenciais nao aparecem como principal pressao do periodo")
         .when(F.col("NR_PONT_CONC_ESS") == 1, "concentracao moderada de despesas essenciais. Ha sinal de acompanhamento, mas ainda nao e a faixa mais critica")
         .when(F.col("NR_PONT_CONC_ESS") == 2, "alta concentracao de despesas essenciais. Uma parte relevante das saidas esta comprometida com gastos basicos")
         .otherwise("concentracao de despesas essenciais nao classificada")
    )
    .withColumn(
        "TX_LEITURA_CONC_FLEX",
        F.when(sem_saida_total, "sem saidas no periodo para avaliar consumo planejado")
         .when(F.col("NR_PONT_CONC_FLEX") == 0, "baixa concentracao de despesas flexiveis. O consumo variavel nao aparece como principal ponto de atencao")
         .when(F.col("NR_PONT_CONC_FLEX") == 1, "concentracao moderada de despesas flexiveis. O consumo variavel merece acompanhamento")
         .when(F.col("NR_PONT_CONC_FLEX") == 2, "alta concentracao de despesas flexiveis. O consumo variavel pode estar pressionando o planejamento financeiro")
         .otherwise("concentracao de despesas flexiveis nao classificada")
    )
    .withColumn(
        "TX_LEITURA_CONC_RES",
        F.when(sem_saida_total, "sem saidas no periodo para avaliar formacao de reserva")
         .when(F.col("NR_PONT_CONC_RES") == 0, "boa formacao de reserva. A parcela direcionada para reserva ou futuro ficou em patamar saudavel")
         .when(F.col("NR_PONT_CONC_RES") == 1, "formacao de reserva intermediaria. Existe algum direcionamento para reserva, mas ainda ha oportunidade de fortalecer protecao financeira")
         .when(F.col("NR_PONT_CONC_RES") == 2, "baixa formacao de reserva. Pouca saida foi direcionada para reserva ou futuro, sinalizando oportunidade de protecao financeira")
         .otherwise("formacao de reserva nao classificada")
    )
    .withColumn(
        "TX_LEITURA_CONC_CRED",
        F.when(sem_saida_total, "sem saidas no periodo para avaliar uso de credito")
         .when(F.col("NR_PONT_CONC_CRED") == 0, "baixa utilizacao de credito. As saidas ligadas a dividas, credito ou custo financeiro ficaram abaixo da referencia de atencao")
         .when(F.col("NR_PONT_CONC_CRED") == 1, "uso moderado de credito. Ha presenca relevante de saidas ligadas a credito, ainda na primeira faixa de atencao")
         .when(F.col("NR_PONT_CONC_CRED") == 2, "alta utilizacao de credito. O credito ou custo financeiro aparece como pressao importante no periodo")
         .otherwise("utilizacao de credito nao classificada")
    )
)

tx_orc_itens = F.concat_ws(
    ", ",
    F.when(F.col("NR_PONT_ORC_ESS") > 0, F.concat_ws("", F.lit("Gestao do Orcamento +"), F.col("NR_PONT_ORC_ESS").cast("string"))),
    F.when(F.col("NR_PONT_ORC_FLEX") > 0, F.concat_ws("", F.lit("Consumo Planejado +"), F.col("NR_PONT_ORC_FLEX").cast("string"))),
    F.when(F.col("NR_PONT_ORC_RES") > 0, F.concat_ws("", F.lit("Formacao de Reserva +"), F.col("NR_PONT_ORC_RES").cast("string"))),
    F.when(F.col("NR_PONT_ORC_CRED") > 0, F.concat_ws("", F.lit("Uso Consciente do Credito +"), F.col("NR_PONT_ORC_CRED").cast("string")))
)

df = df.withColumn(
    "TX_LEITURA_ORCAMENTO",
    F.when(
        F.coalesce(F.col("NR_PONT_ORC_ESS"), F.lit(0))
        + F.coalesce(F.col("NR_PONT_ORC_FLEX"), F.lit(0))
        + F.coalesce(F.col("NR_PONT_ORC_RES"), F.lit(0))
        + F.coalesce(F.col("NR_PONT_ORC_CRED"), F.lit(0)) == 0,
        "o resultado do orcamento nao adicionou reforco de tema"
    ).when(
        F.col("CD_RES_ORC") == 2,
        F.concat_ws("", F.lit("o mes teve deficit financeiro; pela regra original, esse sinal reforca "), tx_orc_itens)
    ).when(
        F.col("CD_RES_ORC") == 1,
        F.concat_ws("", F.lit("o mes teve sobra financeira; pela regra original, esse sinal reforca "), tx_orc_itens)
    ).when(
        F.col("CD_RES_ORC") == 0,
        F.concat_ws("", F.lit("o mes ficou proximo do equilibrio entre entradas e saidas; pela regra original, esse sinal leve reforca "), tx_orc_itens)
    ).otherwise(F.concat_ws("", F.lit("orcamento aplicado em "), tx_orc_itens))
)

# ============================================================
# 4. TEXTO DA REGRA DE PERFIL
# ============================================================
tx_perfil_itens = F.concat_ws(
    ", ",
    F.when(F.col("NR_PONT_PRFL_ESS") > 0, F.concat_ws("", F.lit("Gestao do Orcamento +"), F.col("NR_PONT_PRFL_ESS").cast("string"))),
    F.when(F.col("NR_PONT_PRFL_FLEX") > 0, F.concat_ws("", F.lit("Consumo Planejado +"), F.col("NR_PONT_PRFL_FLEX").cast("string"))),
    F.when(F.col("NR_PONT_PRFL_RES") > 0, F.concat_ws("", F.lit("Formacao de Reserva +"), F.col("NR_PONT_PRFL_RES").cast("string"))),
    F.when(F.col("NR_PONT_PRFL_CRED") > 0, F.concat_ws("", F.lit("Uso Consciente do Credito +"), F.col("NR_PONT_PRFL_CRED").cast("string")))
)

df = df.withColumn(
    "TX_LEITURA_PERFIL",
    F.when(
        F.coalesce(F.col("NR_PONT_PRFL_ESS"), F.lit(0))
        + F.coalesce(F.col("NR_PONT_PRFL_FLEX"), F.lit(0))
        + F.coalesce(F.col("NR_PONT_PRFL_RES"), F.lit(0))
        + F.coalesce(F.col("NR_PONT_PRFL_CRED"), F.lit(0)) == 0,
        "o perfil financeiro nao adicionou reforco de tema"
    ).otherwise(
        F.concat_ws("", F.lit("o perfil financeiro "), F.coalesce(F.col("NM_PRFL_FIN"), F.lit("nao informado")), F.lit(" direciona reforco para "), tx_perfil_itens)
    )
)

# ============================================================
# 5. RESULTADO DOS TEMAS SEM DESEMPATE
# ============================================================
pontuacoes_finais = [
    "NR_PONT_CATEG",
    "NR_PONT_ORC",
    "NR_PONT_CONS",
    "NR_PONT_RES",
    "NR_PONT_CRED",
]

df = df.withColumn(
    "NR_MAIOR_PONTUACAO",
    F.greatest(*[F.coalesce(F.col(c), F.lit(0)) for c in pontuacoes_finais])
)

df = df.withColumn(
    "ARR_TEMAS_MAIOR_PONTUACAO",
    F.expr("""
        CASE
            WHEN NR_MAIOR_PONTUACAO > 0 THEN filter(array(
                CASE WHEN NR_PONT_CATEG = NR_MAIOR_PONTUACAO THEN 'Categorizacao de gastos' END,
                CASE WHEN NR_PONT_ORC   = NR_MAIOR_PONTUACAO THEN 'Gestao do orcamento' END,
                CASE WHEN NR_PONT_CONS  = NR_MAIOR_PONTUACAO THEN 'Consumo planejado' END,
                CASE WHEN NR_PONT_RES   = NR_MAIOR_PONTUACAO THEN 'Formacao de reserva' END,
                CASE WHEN NR_PONT_CRED  = NR_MAIOR_PONTUACAO THEN 'Uso consciente do credito' END
            ), x -> x is not null)
            ELSE cast(array() as array<string>)
        END
    """)
)

df = df.withColumn("QT_TEMAS_MAIOR_PONTUACAO", F.size("ARR_TEMAS_MAIOR_PONTUACAO"))
df = df.withColumn("TX_TEMAS_MAIOR_PONTUACAO", F.concat_ws(", ", "ARR_TEMAS_MAIOR_PONTUACAO"))

df = df.withColumn(
    "TX_RESULTADO_ASPECTO_DESTAQUE",
    F.when(
        F.col("NR_MAIOR_PONTUACAO") == 0,
        "nenhum tema apresentou pontuacao final maior que zero no periodo"
    ).when(
        F.col("QT_TEMAS_MAIOR_PONTUACAO") > 1,
        F.concat_ws(
            "",
            F.lit("empate entre "),
            F.col("TX_TEMAS_MAIOR_PONTUACAO"),
            F.lit(", com pontuacao final "),
            F.col("NR_MAIOR_PONTUACAO").cast("string"),
            F.lit(" ponto(s)")
        )
    ).otherwise(
        F.concat_ws(
            "",
            F.lit("maior pontuacao em "),
            F.element_at("ARR_TEMAS_MAIOR_PONTUACAO", 1),
            F.lit(", com pontuacao final "),
            F.col("NR_MAIOR_PONTUACAO").cast("string"),
            F.lit(" ponto(s)")
        )
    )
)

def leitura_tema(col_final):
    final = F.coalesce(F.col(col_final), F.lit(0))
    maior = F.coalesce(F.col("NR_MAIOR_PONTUACAO"), F.lit(0))
    return F.when(
        maior == 0,
        "nao apareceu como prioridade no periodo"
    ).when(
        (final == maior) & (F.col("QT_TEMAS_MAIOR_PONTUACAO") > 1),
        "empatou como prioridade do periodo pela regra original"
    ).when(
        final == maior,
        "foi o tema de maior prioridade do periodo pela regra original"
    ).when(
        final > 0,
        "apareceu como sinal secundario no periodo"
    ).otherwise("nao recebeu sinal suficiente para virar prioridade")

df = (
    df
    .withColumn("TX_LEITURA_TEMA_CATEG", leitura_tema("NR_PONT_CATEG"))
    .withColumn("TX_LEITURA_TEMA_ORC", leitura_tema("NR_PONT_ORC"))
    .withColumn("TX_LEITURA_TEMA_CONS", leitura_tema("NR_PONT_CONS"))
    .withColumn("TX_LEITURA_TEMA_RES", leitura_tema("NR_PONT_RES"))
    .withColumn("TX_LEITURA_TEMA_CRED", leitura_tema("NR_PONT_CRED"))
    .withColumn(
        "TX_LEITURA_ASPECTO_DESTAQUE",
        F.when(
            F.col("NR_MAIOR_PONTUACAO") == 0,
            "nenhum tema se destacou como prioridade no periodo"
        ).when(
            F.col("QT_TEMAS_MAIOR_PONTUACAO") > 1,
            F.concat_ws("", F.lit("a regra original nao deixa uma prioridade unica; houve empate entre "), F.col("TX_TEMAS_MAIOR_PONTUACAO"))
        ).otherwise(
            F.concat_ws("", F.lit("o tema com maior prioridade pratica foi "), F.element_at("ARR_TEMAS_MAIOR_PONTUACAO", 1))
        )
    )
)

# ============================================================
# 6. EXPLICACAO DAS FORMULAS FINAIS
# ============================================================
def texto_final_tema(col_conc, col_orc, col_prfl, col_final):
    return F.concat_ws(
        "",
        F.lit("concentracao "),
        F.coalesce(F.col(col_conc), F.lit(0)).cast("string"),
        F.lit(" + orcamento "),
        F.coalesce(F.col(col_orc), F.lit(0)).cast("string"),
        F.lit(" + perfil "),
        F.coalesce(F.col(col_prfl), F.lit(0)).cast("string"),
        F.lit(" = "),
        F.coalesce(F.col(col_final), F.lit(0)).cast("string")
    )

df = (
    df
    .withColumn("TX_FORMULA_FINAL_ORC", texto_final_tema("NR_PONT_CONC_ESS", "NR_PONT_ORC_ESS", "NR_PONT_PRFL_ESS", "NR_PONT_ORC"))
    .withColumn("TX_FORMULA_FINAL_CONS", texto_final_tema("NR_PONT_CONC_FLEX", "NR_PONT_ORC_FLEX", "NR_PONT_PRFL_FLEX", "NR_PONT_CONS"))
    .withColumn("TX_FORMULA_FINAL_RES", texto_final_tema("NR_PONT_CONC_RES", "NR_PONT_ORC_RES", "NR_PONT_PRFL_RES", "NR_PONT_RES"))
    .withColumn("TX_FORMULA_FINAL_CRED", texto_final_tema("NR_PONT_CONC_CRED", "NR_PONT_ORC_CRED", "NR_PONT_PRFL_CRED", "NR_PONT_CRED"))
)

# ============================================================
# 7. CLASSIFICACAO CONSOLIDADA
# ============================================================
df = df.withColumn(
    "NR_PONT_PERSONA",
    F.coalesce(F.col("NR_PONT_CONC_ESS"), F.lit(0))
    + F.coalesce(F.col("NR_PONT_CONC_FLEX"), F.lit(0))
    + F.coalesce(F.col("NR_PONT_CONC_RES"), F.lit(0))
    + F.coalesce(F.col("NR_PONT_CONC_CRED"), F.lit(0))
)

df = df.withColumn(
    "TX_FAIXA_CLASSIFICACAO_GERAL",
    F.when(F.col("NR_PONT_PERSONA").between(0, 2), "de 0 a 2 pontos")
     .when(F.col("NR_PONT_PERSONA").between(3, 4), "de 3 a 4 pontos")
     .when(F.col("NR_PONT_PERSONA").between(5, 6), "de 5 a 6 pontos")
     .when(F.col("NR_PONT_PERSONA").between(7, 8), "de 7 a 8 pontos")
     .otherwise("fora das faixas previstas")
)

df = df.withColumn(
    "TX_CLASSIFICACAO_GERAL",
    F.when(F.col("NR_PONT_PERSONA").between(0, 2), "Base Financeira Consolidada")
     .when(F.col("NR_PONT_PERSONA").between(3, 4), "Base Financeira Equilibrada")
     .when(F.col("NR_PONT_PERSONA").between(5, 6), "Oportunidade de Evolucao Financeira")
     .when(F.col("NR_PONT_PERSONA").between(7, 8), "Prioridade para Organizacao Financeira")
     .otherwise("Classificacao nao definida")
)

# ============================================================
# 8. CARACTERISTICAS DO PERIODO
# ============================================================
df = (
    df
    .withColumn(
        "TX_CLASSIFICACAO_GEN",
        F.when(sem_saida_total, "sem saidas no periodo para classificar categorizacao")
         .when(F.col("NR_PONT_CONC_GEN") == 0, "alta categorizacao dos gastos")
         .when(F.col("NR_PONT_CONC_GEN") == 99, "baixa categorizacao dos gastos")
         .otherwise("categorizacao intermediaria dos gastos")
    )
    .withColumn(
        "TX_CLASSIFICACAO_ESS",
        F.when(sem_saida_total, "sem saidas no periodo para classificar despesas essenciais")
         .when(F.col("NR_PONT_CONC_ESS") == 0, "baixa concentracao de despesas essenciais")
         .when(F.col("NR_PONT_CONC_ESS") == 1, "media concentracao de despesas essenciais")
         .when(F.col("NR_PONT_CONC_ESS") == 2, "alta concentracao de despesas essenciais")
         .otherwise("concentracao de despesas essenciais nao classificada")
    )
    .withColumn(
        "TX_CLASSIFICACAO_FLEX",
        F.when(sem_saida_total, "sem saidas no periodo para classificar despesas flexiveis")
         .when(F.col("NR_PONT_CONC_FLEX") == 0, "baixa concentracao de despesas flexiveis")
         .when(F.col("NR_PONT_CONC_FLEX") == 1, "media concentracao de despesas flexiveis")
         .when(F.col("NR_PONT_CONC_FLEX") == 2, "alta concentracao de despesas flexiveis")
         .otherwise("concentracao de despesas flexiveis nao classificada")
    )
    .withColumn(
        "TX_CLASSIFICACAO_RES",
        F.when(sem_saida_total, "sem saidas no periodo para classificar formacao de reserva")
         .when(F.col("NR_PONT_CONC_RES") == 0, "alta formacao de reserva financeira")
         .when(F.col("NR_PONT_CONC_RES") == 1, "media formacao de reserva financeira")
         .when(F.col("NR_PONT_CONC_RES") == 2, "baixa formacao de reserva financeira")
         .otherwise("formacao de reserva nao classificada")
    )
    .withColumn(
        "TX_CLASSIFICACAO_CRED",
        F.when(sem_saida_total, "sem saidas no periodo para classificar uso de credito")
         .when(F.col("NR_PONT_CONC_CRED") == 0, "baixa utilizacao de credito")
         .when(F.col("NR_PONT_CONC_CRED") == 1, "media utilizacao de credito")
         .when(F.col("NR_PONT_CONC_CRED") == 2, "alta utilizacao de credito")
         .otherwise("utilizacao de credito nao classificada")
    )
)

# ============================================================
# 9. HELPERS DE FORMATACAO
# ============================================================
ASCII_FROM = "\u00e1\u00e0\u00e2\u00e3\u00e4\u00e9\u00e8\u00ea\u00eb\u00ed\u00ec\u00ee\u00ef\u00f3\u00f2\u00f4\u00f5\u00f6\u00fa\u00f9\u00fb\u00fc\u00e7\u00c1\u00c0\u00c2\u00c3\u00c4\u00c9\u00c8\u00ca\u00cb\u00cd\u00cc\u00ce\u00cf\u00d3\u00d2\u00d4\u00d5\u00d6\u00da\u00d9\u00db\u00dc\u00c7"
ASCII_TO = "aaaaaeeeeiiiiooooouuuucAAAAAEEEEIIIIOOOOOUUUUC"

def ascii_text(col):
    return F.translate(
        F.coalesce(col.cast("string"), F.lit("nao informado")),
        ASCII_FROM,
        ASCII_TO
    )

def brl(c):
    return F.translate(
        F.format_number(F.coalesce(F.col(c).cast("double"), F.lit(0.0)), 2),
        ",.",
        ".,"
    )

def pct(c):
    return F.translate(
        F.format_number(F.coalesce(F.col(c).cast("double"), F.lit(0.0)), 2),
        ",.",
        ".,"
    )

def pref(c):
    return F.translate(
        F.format_number(F.coalesce(F.col(c).cast("double"), F.lit(0.0)) * 100, 2),
        ",.",
        ".,"
    )

def s(c):
    return ascii_text(F.col(c))

def n(c):
    return F.coalesce(F.col(c).cast("string"), F.lit("0"))

pc_sai_ent_fmt = F.when(
    sem_entrada_total & tem_saida_total,
    F.lit("sem denominador valido")
).otherwise(
    F.concat_ws(
        "",
        F.translate(F.format_number(pc_sai_ent_pct.cast("double"), 2), ",.", ".,"),
        F.lit("%")
    )
)

# ============================================================
# 10. TX_PERSONA_UNICA
# ============================================================
df = df.withColumn(
    "TX_PERSONA_UNICA",
    F.concat_ws(
        "",
        F.lit("LEITURA UNICA POR CLIENTE\n\n"),
        F.lit("Cliente "), s("CD_CLI"), F.lit(" - macroperfil "), s("NM_MAC_PRFL_CLI"),
        F.lit(", perfil de renda "), s("NM_PRFL"), F.lit(" e perfil financeiro "),
        s("NM_PRFL_FIN"), F.lit(".\n"),
        F.lit("Periodo: "), s("DT_REF_INI"), F.lit(" a "), s("DT_REF_FIM"), F.lit(".\n\n"),

        F.lit("MOVIMENTACAO\n"),
        F.lit("- Leitura: "), s("TX_LEITURA_MOVIMENTACAO"), F.lit(".\n"),
        F.lit("- Motivo: entradas de R$ "), brl("VL_ENT_TOTAL"), F.lit(", saidas de R$ "), brl("VL_SAI_TOTAL"),
        F.lit(", resultado de R$ "), brl("VL_RES_ORC"), F.lit(" e comprometimento de "), pc_sai_ent_fmt,
        F.lit(" ("), s("TX_REGRA_RESULTADO"), F.lit("; "), s("TX_STS_FINAL"), F.lit(").\n\n"),

        F.lit("CONCENTRACAO DOS GASTOS\n"),
        F.lit("- Categorizacao: "), s("TX_LEITURA_CONC_GEN"), F.lit(".\n"),
        F.lit("  Motivo: R$ "), brl("VL_SAI_GEN"), F.lit(" de R$ "), brl("VL_SAI_TOTAL"),
        F.lit(" ficaram em saidas genericas, equivalente a "), pct("PC_SAI_GEN"), F.lit("%; referencia "), pref("PC_REF_GEN"),
        F.lit("%; regra: "), s("TX_REGRA_CONC_GEN"), F.lit("; pontuacao "), n("NR_PONT_CONC_GEN"), F.lit(".\n"),
        F.lit("- Essenciais: "), s("TX_LEITURA_CONC_ESS"), F.lit(".\n"),
        F.lit("  Motivo: R$ "), brl("VL_SAI_ESS"), F.lit(" de R$ "), brl("VL_SAI_TOTAL"),
        F.lit(" foram despesas essenciais, equivalente a "), pct("PC_SAI_ESS"), F.lit("%; referencia "), pref("PC_REF_ESS"),
        F.lit("%; regra: "), s("TX_REGRA_CONC_ESS"), F.lit("; pontuacao "), n("NR_PONT_CONC_ESS"), F.lit(".\n"),
        F.lit("- Flexiveis: "), s("TX_LEITURA_CONC_FLEX"), F.lit(".\n"),
        F.lit("  Motivo: R$ "), brl("VL_SAI_FLEX"), F.lit(" de R$ "), brl("VL_SAI_TOTAL"),
        F.lit(" foram despesas flexiveis, equivalente a "), pct("PC_SAI_FLEX"), F.lit("%; referencia "), pref("PC_REF_FLEX"),
        F.lit("%; regra: "), s("TX_REGRA_CONC_FLEX"), F.lit("; pontuacao "), n("NR_PONT_CONC_FLEX"), F.lit(".\n"),
        F.lit("- Reserva: "), s("TX_LEITURA_CONC_RES"), F.lit(".\n"),
        F.lit("  Motivo: R$ "), brl("VL_SAI_RES"), F.lit(" de R$ "), brl("VL_SAI_TOTAL"),
        F.lit(" foram direcionados para reserva ou futuro, equivalente a "), pct("PC_SAI_RES"), F.lit("%; referencia "), pref("PC_REF_RES"),
        F.lit("%; regra: "), s("TX_REGRA_CONC_RES"), F.lit("; pontuacao "), n("NR_PONT_CONC_RES"), F.lit(".\n"),
        F.lit("- Credito: "), s("TX_LEITURA_CONC_CRED"), F.lit(".\n"),
        F.lit("  Motivo: R$ "), brl("VL_SAI_DIV"), F.lit(" de R$ "), brl("VL_SAI_TOTAL"),
        F.lit(" foram saidas ligadas a dividas, credito ou custo financeiro, equivalente a "), pct("PC_SAI_CRED"), F.lit("%; referencia "), pref("PC_REF_CRED"),
        F.lit("%; regra: "), s("TX_REGRA_CONC_CRED"), F.lit("; pontuacao "), n("NR_PONT_CONC_CRED"), F.lit(".\n\n"),

        F.lit("PONTUACAO PELO ORCAMENTO\n"),
        F.lit("- Leitura: "), s("TX_LEITURA_ORCAMENTO"), F.lit(".\n"),
        F.lit("- Motivo: resultado "), s("TX_STS_FINAL"), F.lit(", comprometimento de "), pc_sai_ent_fmt,
        F.lit("; pontos por tema: Categorizacao "), n("NR_PONT_ORC_GEN"),
        F.lit(", Gestao do Orcamento "), n("NR_PONT_ORC_ESS"),
        F.lit(", Consumo Planejado "), n("NR_PONT_ORC_FLEX"),
        F.lit(", Formacao de Reserva "), n("NR_PONT_ORC_RES"),
        F.lit(", Uso Consciente do Credito "), n("NR_PONT_ORC_CRED"), F.lit(".\n\n"),

        F.lit("PONTUACAO PELO PERFIL\n"),
        F.lit("- Leitura: "), s("TX_LEITURA_PERFIL"), F.lit(".\n"),
        F.lit("- Motivo: perfil base "), s("NM_PRFL_FIN"), F.lit("; pontos por tema: Categorizacao "), n("NR_PONT_PRFL_GEN"),
        F.lit(", Gestao do Orcamento "), n("NR_PONT_PRFL_ESS"),
        F.lit(", Consumo Planejado "), n("NR_PONT_PRFL_FLEX"),
        F.lit(", Formacao de Reserva "), n("NR_PONT_PRFL_RES"),
        F.lit(", Uso Consciente do Credito "), n("NR_PONT_PRFL_CRED"), F.lit(".\n\n"),

        F.lit("RESULTADO POR TEMA\n"),
        F.lit("Criterio: soma direta de concentracao + orcamento + perfil.\n"),
        F.lit("- Categorizacao de gastos: "), s("TX_LEITURA_TEMA_CATEG"), F.lit(".\n"),
        F.lit("  Motivo: pontuacao final "), n("NR_PONT_CATEG"), F.lit("; igual a pontuacao de concentracao generica.\n"),
        F.lit("- Gestao do orcamento: "), s("TX_LEITURA_TEMA_ORC"), F.lit(".\n"),
        F.lit("  Motivo: pontuacao final "), n("NR_PONT_ORC"), F.lit("; "), s("TX_FORMULA_FINAL_ORC"), F.lit(".\n"),
        F.lit("- Consumo planejado: "), s("TX_LEITURA_TEMA_CONS"), F.lit(".\n"),
        F.lit("  Motivo: pontuacao final "), n("NR_PONT_CONS"), F.lit("; "), s("TX_FORMULA_FINAL_CONS"), F.lit(".\n"),
        F.lit("- Formacao de reserva: "), s("TX_LEITURA_TEMA_RES"), F.lit(".\n"),
        F.lit("  Motivo: pontuacao final "), n("NR_PONT_RES"), F.lit("; "), s("TX_FORMULA_FINAL_RES"), F.lit(".\n"),
        F.lit("- Uso consciente do credito: "), s("TX_LEITURA_TEMA_CRED"), F.lit(".\n"),
        F.lit("  Motivo: pontuacao final "), n("NR_PONT_CRED"), F.lit("; "), s("TX_FORMULA_FINAL_CRED"), F.lit(".\n\n"),

        F.lit("ASPECTO FINANCEIRO DE MAIOR PONTUACAO\n"),
        F.lit("- Leitura: "), s("TX_LEITURA_ASPECTO_DESTAQUE"), F.lit(".\n"),
        F.lit("- Motivo: "), s("TX_RESULTADO_ASPECTO_DESTAQUE"), F.lit(".\n\n"),

        F.lit("CLASSIFICACAO CONSOLIDADA DA CONCENTRACAO\n"),
        F.lit("- Leitura: "), s("TX_CLASSIFICACAO_GERAL"), F.lit(". Esta classificacao resume a intensidade dos sinais de concentracao, sem somar orcamento ou perfil.\n"),
        F.lit("- Motivo: "), n("NR_PONT_CONC_ESS"), F.lit(" + "), n("NR_PONT_CONC_FLEX"),
        F.lit(" + "), n("NR_PONT_CONC_RES"), F.lit(" + "), n("NR_PONT_CONC_CRED"),
        F.lit(" = "), n("NR_PONT_PERSONA"), F.lit("; faixa "), s("TX_FAIXA_CLASSIFICACAO_GERAL"), F.lit(".\n\n"),

        F.lit("SINTESE FINAL\n"),
        F.lit("- Leitura: "), s("TX_LEITURA_ASPECTO_DESTAQUE"), F.lit(". Como apoio, o periodo mostra "),
        s("TX_CLASSIFICACAO_ESS"), F.lit(", "), s("TX_CLASSIFICACAO_FLEX"), F.lit(", "),
        s("TX_CLASSIFICACAO_RES"), F.lit(" e "), s("TX_CLASSIFICACAO_CRED"), F.lit(".\n"),
        F.lit("- Motivo: maior pontuacao final "), n("NR_MAIOR_PONTUACAO"), F.lit("; temas no topo: "),
        s("TX_TEMAS_MAIOR_PONTUACAO"), F.lit("; classificacao da concentracao: "),
        s("TX_CLASSIFICACAO_GERAL"), F.lit(".")
    )
)

%%spark

from pyspark.sql import functions as F
from pyspark.sql.window import Window

amostra = (
    df
    .where(
        (F.col("FL_PARTICIPA_RADAR") == "S") &
        (F.col("TX_PERSONA_UNICA").isNotNull())
    )
    .withColumn(
        "rn",
        F.row_number().over(
            Window.partitionBy("NM_MAC_PRFL_CLI")
                  .orderBy(F.rand())
        )
    )
    .where(F.col("rn") == 1)
    .select(
        "NM_MAC_PRFL_CLI",
        "CD_CLI",
        "TX_PERSONA_UNICA"
    )
    .orderBy("NM_MAC_PRFL_CLI")
    .collect()
)

for registro in amostra:
    print("\n" + "=" * 110)
    print(f"MACROPERFIL: {registro['NM_MAC_PRFL_CLI']}")
    print(f"CLIENTE: {registro['CD_CLI']}")
    print("=" * 110)

    texto = (
        registro["TX_PERSONA_UNICA"]
        .replace("&lt;br&gt;&lt;br&gt;", "\n\n")
        .replace("&lt;br&gt;", "\n")
    )

    print(texto)
