# Modelagem Final Revisada — ANA_EDU_FIN_CLI

```python
%%spark

sandbox = "t2i2016"
database = f"sbx_{sandbox}"
table_name = "ana_edu_fin_cli"
tabela_spark = f"{database}.{table_name}"

atualizar_metadado = True

ddl_tabela_spark = f"""
CREATE TABLE {tabela_spark} (

    -- Identificação
    CD_CLI                     INT             COMMENT 'Código do cliente',

    -- Quantidades de transações
    QT_TRANS_TOTAL             BIGINT          COMMENT 'Quantidade total de transações',

    QT_TRANS_ENT               BIGINT          COMMENT 'Quantidade de transações de entrada',
    QTD_TRANS_ENT_CC           BIGINT          COMMENT 'Quantidade de transações de entrada em conta corrente',
    QTD_TRANS_ENT_CD           BIGINT          COMMENT 'Quantidade de transações de entrada em cartão',

    QT_TRANS_SAI               BIGINT          COMMENT 'Quantidade de transações de saída',
    QTD_TRANS_SAI_CC           BIGINT          COMMENT 'Quantidade de transações de saída em conta corrente',
    QTD_TRANS_SAI_CD           BIGINT          COMMENT 'Quantidade de transações de saída em cartão',

    -- Valores de transações
    VL_TRANS_ENT               DECIMAL(25,2)   COMMENT 'Valor total de entradas',
    VL_TRANS_ENT_CC            DECIMAL(25,2)   COMMENT 'Valor de entradas em conta corrente',
    VL_TRANS_ENT_CD            DECIMAL(25,2)   COMMENT 'Valor de entradas em cartão',

    VL_TRANS_SAI               DECIMAL(25,2)   COMMENT 'Valor total de saídas',
    VL_TRANS_SAI_CC            DECIMAL(25,2)   COMMENT 'Valor de saídas em conta corrente',
    VL_TRANS_SAI_CD            DECIMAL(25,2)   COMMENT 'Valor de saídas em cartão',

    -- Perfil de renda
    CD_PRFL                    INT             COMMENT 'Código do perfil de renda',
    NM_PRFL                    STRING          COMMENT 'Texto do perfil de renda',

    -- Perfil financeiro
    CD_MAC_PRFL_CLI            BIGINT          COMMENT 'Código do macroperfil financeiro',
    NM_MAC_PRFL_CLI            STRING          COMMENT 'Texto do macroperfil financeiro',

    CD_MIC_PRFL_CLI            BIGINT          COMMENT 'Código do microperfil financeiro',
    NM_MIC_PRFL_CLI            STRING          COMMENT 'Texto do microperfil financeiro',

    -- Perfil financeiro unificado
    CD_PRFL_FIN                BIGINT          COMMENT 'Código derivado do perfil financeiro: macro x 10 + micro',
    NM_PRFL_FIN                STRING          COMMENT 'Texto unificado do perfil financeiro',

    -- Blocos de entrada
    VL_ENT_REC                 DECIMAL(18,2)   COMMENT 'Valor de entrada por receita, rendimento ou benefício',
    VL_ENT_REEMB               DECIMAL(18,2)   COMMENT 'Valor de entrada por restituição, estorno ou ajuste',
    VL_ENT_RESG                DECIMAL(18,2)   COMMENT 'Valor de entrada por resgate de investimento',
    VL_ENT_IND                 DECIMAL(18,2)   COMMENT 'Valor de entrada por transferência ou entrada indefinida',
    VL_ENT_EMPR                DECIMAL(18,2)   COMMENT 'Valor de entrada por empréstimo ou crédito liberado',
    VL_ENT_TOTAL               DECIMAL(18,2)   COMMENT 'Valor total de entrada',

    -- Blocos de saída
    VL_SAI_GEN                 DECIMAL(18,2)   COMMENT 'Valor de saída genérica ou não classificada',
    VL_SAI_ESS                 DECIMAL(18,2)   COMMENT 'Valor de saída essencial',
    VL_SAI_FLEX                DECIMAL(18,2)   COMMENT 'Valor de saída flexível',
    VL_SAI_RES                 DECIMAL(18,2)   COMMENT 'Valor de saída para reserva ou futuro',
    VL_SAI_DIV                 DECIMAL(18,2)   COMMENT 'Valor de saída para dívidas, crédito ou custo financeiro',
    VL_SAI_TOTAL               DECIMAL(18,2)   COMMENT 'Valor total de saída',

    -- Resultado do orçamento
    VL_RES_ORC                 DECIMAL(18,2)   COMMENT 'Valor do resultado do orçamento: entradas menos saídas',
    CD_RES_ORC                 INT             COMMENT 'Código do resultado do orçamento: 0 = Neutro; 1 = Superavitário; 2 = Deficitário',
    TX_RES_ORC                 STRING          COMMENT 'Texto do resultado do orçamento',
    PC_SAI_ENT                 DECIMAL(9,6)    COMMENT 'Percentual de saída sobre entrada',
    TX_STS_RES                 STRING          COMMENT 'Status da intensidade do resultado: Forte ou Fraco',
    TX_STS_FINAL               STRING          COMMENT 'Texto final composto pelo resultado e seu status',

    -- Percentuais de referência
    PC_REF_GEN                 DECIMAL(9,6)    COMMENT 'Percentual de referência para saída genérica',
    PC_REF_ESS                 DECIMAL(9,6)    COMMENT 'Percentual de referência para saída essencial',
    PC_REF_FLEX                DECIMAL(9,6)    COMMENT 'Percentual de referência para saída flexível',
    PC_REF_RES                 DECIMAL(9,6)    COMMENT 'Percentual de referência para reserva',
    PC_REF_CRED                DECIMAL(9,6)    COMMENT 'Percentual de referência para crédito',

    -- Pontuação por concentração
    NR_PONT_CONC_GEN           INT             COMMENT 'Pontuação de concentração genérica',
    NR_PONT_CONC_ESS           INT             COMMENT 'Pontuação de concentração essencial',
    NR_PONT_CONC_FLEX          INT             COMMENT 'Pontuação de concentração flexível',
    NR_PONT_CONC_RES           INT             COMMENT 'Pontuação de concentração reserva',
    NR_PONT_CONC_CRED          INT             COMMENT 'Pontuação de concentração crédito',

    -- Pontuação do orçamento
    NR_PONT_ORC_GEN            INT             COMMENT 'Pontuação de orçamento genérica',
    NR_PONT_ORC_ESS            INT             COMMENT 'Pontuação de orçamento essencial',
    NR_PONT_ORC_FLEX           INT             COMMENT 'Pontuação de orçamento flexível',
    NR_PONT_ORC_RES            INT             COMMENT 'Pontuação de orçamento reserva',
    NR_PONT_ORC_CRED           INT             COMMENT 'Pontuação de orçamento crédito',

    -- Pontuação do perfil
    NR_PONT_PRFL_GEN           INT             COMMENT 'Pontuação de perfil genérica',
    NR_PONT_PRFL_ESS           INT             COMMENT 'Pontuação de perfil essencial',
    NR_PONT_PRFL_FLEX          INT             COMMENT 'Pontuação de perfil flexível',
    NR_PONT_PRFL_RES           INT             COMMENT 'Pontuação de perfil reserva',
    NR_PONT_PRFL_CRED          INT             COMMENT 'Pontuação de perfil crédito',

    -- Pontuação final por tema
    NR_PONT_CATEG              INT             COMMENT 'Pontuação final de categorização de gastos',
    NR_PONT_ORC                INT             COMMENT 'Pontuação final de gestão de orçamento',
    NR_PONT_CONS               INT             COMMENT 'Pontuação final de consumo planejado',
    NR_PONT_RES                INT             COMMENT 'Pontuação final de formação de reserva',
    NR_PONT_CRED               INT             COMMENT 'Pontuação final de uso consciente do crédito',

    -- Marcação de contexto e participação no radar
    FL_TEM_MOV_AGRO            STRING          COMMENT 'Indica se o cliente teve movimentação de crédito ou débito em categoria marcada como agro: S ou N',
    FL_PARTICIPA_RADAR         STRING          COMMENT 'Indica se o cliente atende às regras mínimas para participar do radar: S ou N',

    -- Datas de execução e referência

    DT_EXEA                    DATE            COMMENT 'Data de execução do ETL',

    DT_MES_EXEA                DATE            COMMENT 'Mês de execução do ETL, representado pelo primeiro dia do mês',

    DT_REF_INI                 DATE            COMMENT 'Data inicial do período de referência analisado',

    DT_REF_FIM                 DATE            COMMENT 'Data final do período de referência analisado'
)
COMMENT 'Análise de Educação Financeira do Cliente'
STORED AS PARQUET
TBLPROPERTIES (
    'parquet.compress' = 'SNAPPY'
)
"""

if atualizar_metadado:
    spark.sql(f"DROP TABLE IF EXISTS {tabela_spark}")
    spark.sql(ddl_tabela_spark)
```

## Identificação da tabela

| Item | Definição |
|---|---|
| Nome lógico | Análise de Educação Financeira do Cliente |
| Nome físico | `ANA_EDU_FIN_CLI` |
| Nome no Hive | `ana_edu_fin_cli` |
| Granularidade | Uma linha por `CD_CLI` na janela mensal processada. |
| Finalidade | Organizar indicadores do período para apoiar a educação financeira do cliente. |
| Carga | Integral, com `overwrite`. |
| Estrutura final | 67 colunas. |

## Mudanças consolidadas nesta revisão

- A base final usa uma linha por cliente na janela mensal processada, sem campos de data persistidos nesta versão.
- O resumo técnico mantém a leitura de entrada e saída pela natureza `C` e `D`.
- Os blocos classificados usam `CD_CLASSIFICACAO_CATEGORIA`, com códigos `0` a `4` para entradas e `5` a `9` para saídas.
- O perfil financeiro substitui a nomenclatura lógica anterior; o nome físico da origem `DVS_GRDR_FNCO_PF` permanece inalterado.
- O resultado do orçamento, os percentuais de referência e as pontuações são calculados a partir da sumarizada.
- Percentuais internos de concentração são usados somente no cálculo da pontuação e não são persistidos como colunas finais.
- Todas as divisões usam `NULLIF` e `COALESCE`; sem denominador válido, o resultado é `0`.
- A marcação agro é definida no mapa de categorias. Cliente com movimentação agro não participa do radar.
- As regras de negócio e os limiares de pontuação foram preservados.

## Padrão mínimo de siglas

| Sigla | Uso |
|---|---|
| `CD` | Código |
| `FL` | Flag |
| `NM` | Nome |
| `NR` | Número / pontuação |
| `PC` | Percentual |
| `QT` | Quantidade |
| `QTD` | Quantidade detalhada |
| `TX` | Texto ou status |
| `VL` | Valor monetário |
| `ENT` | Entrada |
| `SAI` | Saída |
| `PRFL` | Perfil |

> Sequência temática fixa: **1. Genérica / Categorização; 2. Essencial / Orçamento; 3. Flexível / Consumo; 4. Reserva / Formação de Reserva; 5. Crédito / Uso Consciente do Crédito.**

## Identificação e resumo técnico das transações

| Nome antigo | Nome lógico novo | Nome físico novo | CLASSIFICAÇÃO (NÃO CATEGORIA) | Valor Referência | Observação |
|---|---|---|---|---|---|
| CD_CLI | Código Cliente | CD_CLI |  |  | Uma linha por cliente na janela mensal. |
| QTD_TOTAL_TRANSACAO | Quantidade Transação Total | QT_TRANS_TOTAL |  | Contagem | Todas as transações do período. |
| QTD_TOTAL_CREDITO | Quantidade Transação Entrada | QT_TRANS_ENT |  | Contagem | Natureza `C`. |
|  | Quantidade Entrada em Conta Corrente | QTD_TRANS_ENT_CC |  | Contagem | Natureza `C` e `CD_PRD = 6`. |
|  | Quantidade Entrada em Cartão | QTD_TRANS_ENT_CD |  | Contagem | Natureza `C` e `CD_PRD = 9`. |
| QTD_TOTAL_DEBITO | Quantidade Transação Saída | QT_TRANS_SAI |  | Contagem | Natureza `D`. |
|  | Quantidade Saída em Conta Corrente | QTD_TRANS_SAI_CC |  | Contagem | Natureza `D` e `CD_PRD = 6`. |
|  | Quantidade Saída em Cartão | QTD_TRANS_SAI_CD |  | Contagem | Natureza `D` e `CD_PRD = 9`. |
|  | Valor Entrada Total Técnico | VL_TRANS_ENT |  | Soma de `VL_TRAN` com natureza `C` | Resumo técnico por natureza. |
|  | Valor Entrada em Conta Corrente | VL_TRANS_ENT_CC |  | Soma de `VL_TRAN` com natureza `C` e `CD_PRD = 6` |  |
|  | Valor Entrada em Cartão | VL_TRANS_ENT_CD |  | Soma de `VL_TRAN` com natureza `C` e `CD_PRD = 9` |  |
|  | Valor Saída Total Técnico | VL_TRANS_SAI |  | Soma de `VL_TRAN` com natureza `D` | Resumo técnico por natureza. |
|  | Valor Saída em Conta Corrente | VL_TRANS_SAI_CC |  | Soma de `VL_TRAN` com natureza `D` e `CD_PRD = 6` |  |
|  | Valor Saída em Cartão | VL_TRANS_SAI_CD |  | Soma de `VL_TRAN` com natureza `D` e `CD_PRD = 9` |  |

## Perfil de renda e perfil financeiro

| Nome antigo | Nome lógico novo | Nome físico novo | CLASSIFICAÇÃO (NÃO CATEGORIA) | Valor Referência | Observação |
|---|---|---|---|---|---|
|  | Código Perfil de Renda | CD_PRFL | Exploratório / agrupamento | `DB2SMI.CLI_SGM` | Perfil mais recente com `CD_CRIT_SGM_CLI = 2`. |
|  | Nome Perfil de Renda | NM_PRFL | Exploratório / agrupamento | SEM PERFIL / PF A / PF B / PF C / PF D / PF E | Valor não reconhecido recebe `A CLASSIFICAR`. |
| CD_PERFIL | Código Macro Perfil Cliente | CD_MAC_PRFL_CLI |  | `sbx_t2i2016.DVS_GRDR_FNCO_PF` | Registro mais recente por cliente. |
| NM_PERFIL | Nome Macro Perfil Cliente | NM_MAC_PRFL_CLI |  | Endividado / Equilibrista / Investidor | Valor não reconhecido recebe `A CLASSIFICAR`. |
| CD_SUB_PERFIL | Código Micro Perfil Cliente | CD_MIC_PRFL_CLI |  | `sbx_t2i2016.DVS_GRDR_FNCO_PF` | Registro mais recente por cliente. |
| NM_SUB_PERFIL | Nome Micro Perfil Cliente | NM_MIC_PRFL_CLI |  | Inadimplente / Acrobata / Iminente / Consciente / Equilibrista / Acelerado / Precavido / Despreocupado | Valor não reconhecido recebe `A CLASSIFICAR`. |
|  | Código Perfil Financeiro | CD_PRFL_FIN |  | `CD_MAC_PRFL_CLI * 10 + CD_MIC_PRFL_CLI` | Campo derivado; nulo quando algum perfil estiver `A CLASSIFICAR`. |
| TX_PERFIL_FINAL | Nome Perfil Financeiro | NM_PRFL_FIN |  | `NM_MAC_PRFL_CLI + ' ' + NM_MIC_PRFL_CLI` | Campo derivado; recebe `A CLASSIFICAR` quando necessário. |

## Blocos de Entrada

| Nome antigo | Nome lógico novo | Nome físico novo | CLASSIFICAÇÃO (NÃO CATEGORIA) | Valor Referência | Observação |
|---|---|---|---|---|---|
| C1 | Valor Entrada Receita | VL_ENT_REC | Receita / rendimento / benefício | Código 1 |  |
| C2 | Valor Entrada Reembolso | VL_ENT_REEMB | Restituição / estorno / ajuste | Código 2 |  |
| C3 | Valor Entrada Resgate | VL_ENT_RESG | Resgate de investimento | Código 3 |  |
| C4 | Valor Entrada Indefinida | VL_ENT_IND | Transferência / entrada indefinida | Código 0 |  |
| C5 | Valor Entrada Empréstimo | VL_ENT_EMPR | Crédito tomado / liberação de crédito | Código 4 | Dinheiro recebido que cria obrigação futura. |
| Entrada_Total | Valor Entrada Total | VL_ENT_TOTAL |  | `VL_ENT_REC + VL_ENT_REEMB + VL_ENT_RESG + VL_ENT_IND + VL_ENT_EMPR` |  |

## Blocos de Saída

| Nome antigo | Nome lógico novo | Nome físico novo | CLASSIFICAÇÃO (NÃO CATEGORIA) | Valor Referência | Observação |
|---|---|---|---|---|---|
| D1 | Valor Saída Genérica | VL_SAI_GEN | Genérico / não classificado | Código 5 |  |
| D2 | Valor Saída Essencial | VL_SAI_ESS | Essenciais | Código 6 |  |
| D3 | Valor Saída Flexível | VL_SAI_FLEX | Flexíveis | Código 7 |  |
| D4 | Valor Saída Reserva | VL_SAI_RES | Reserva / futuro | Código 8 |  |
| D5 | Valor Saída Dívidas | VL_SAI_DIV | Dívidas / crédito / custo financeiro | Código 9 |  |
| Saida_Total | Valor Saída Total | VL_SAI_TOTAL |  | `VL_SAI_GEN + VL_SAI_ESS + VL_SAI_FLEX + VL_SAI_RES + VL_SAI_DIV` |  |

## Resultado do Orçamento

| Nome antigo | Nome lógico novo | Nome físico novo | CLASSIFICAÇÃO (NÃO CATEGORIA) | Valor Referência | Observação |
|---|---|---|---|---|---|
| Valor_Resultado_Orçamento | Valor Resultado Orçamento | VL_RES_ORC |  | `VL_ENT_TOTAL - VL_SAI_TOTAL` |  |
| Codigo_Resultado_Orçamento | Código Resultado Orçamento | CD_RES_ORC |  | 0 / 1 / 2 | 0 = Neutro; 1 = Superavitário; 2 = Deficitário. |
| Texto_Resultado_Orçamento | Texto Resultado Orçamento | TX_RES_ORC |  | Neutro / Superavitário / Deficitário | Faixa neutra entre `0,95` e `1,05`. |
| %_Resultado | Percentual Saída Entrada | PC_SAI_ENT |  | `VL_SAI_TOTAL / VL_ENT_TOTAL` | Sem denominador válido, recebe `0`. |
| tx_status_resultado | Texto Status Resultado | TX_STS_RES |  | Forte / Fraco | Calculado a partir das faixas do resultado. |
| tx_status_final | Texto Status Final | TX_STS_FINAL |  | `TX_RES_ORC + TX_STS_RES` | Exemplo: `Neutro Forte`. |

## Percentuais de Referência

| Nome antigo | Nome lógico novo | Nome físico novo | CLASSIFICAÇÃO (NÃO CATEGORIA) | Valor Referência | Observação |
|---|---|---|---|---|---|
| PRP_D1 | Percentual Referência Genérica | PC_REF_GEN | Genérico / não classificado | 75% fixo (`0.750000`) | Referência do Tema 1. |
| PRP_D2 | Percentual Referência Essencial | PC_REF_ESS | Essenciais | 50% fixo (`0.500000`) | Referência inicial do Tema 2. |
| PRP_D3 | Percentual Referência Flexível | PC_REF_FLEX | Flexíveis | 30% fixo (`0.300000`) | Referência inicial do Tema 3. |
| PRP_D4 | Percentual Referência Reserva | PC_REF_RES | Reserva / futuro | 20% fixo (`0.200000`) | Referência inicial do Tema 4. |
| PRP_D5 | Percentual Referência Crédito | PC_REF_CRED | Dívidas / crédito / custo financeiro | 30% fixo (`0.300000`) | Referência inicial do Tema 5. |

## Pontuação por Concentração

| Nome antigo | Nome lógico novo | Nome físico novo | CLASSIFICAÇÃO (NÃO CATEGORIA) | Valor Referência | Observação |
|---|---|---|---|---|---|
| PONTACAO_TOTAL_TEMA 1 | Pontuação Concentração Genérica | NR_PONT_CONC_GEN | Genérica / Categorização | +0 — `PC_SAI_GEN <= PC_REF_GEN`<br>+99 — `PC_SAI_GEN > PC_REF_GEN` | Quando `VL_SAI_TOTAL = 0`, recebe +0. |
| PONTACAO_TOTAL_TEMA 2 | Pontuação Concentração Essencial | NR_PONT_CONC_ESS | Essencial / Orçamento | +0 — `PC_SAI_ESS < PC_REF_ESS`<br>+1 — `PC_SAI_ESS >= PC_REF_ESS` e `PC_SAI_ESS < (PC_REF_ESS * 1.5)`<br>+2 — `PC_SAI_ESS >= (PC_REF_ESS * 1.5)` | Quando `VL_SAI_TOTAL = 0`, recebe +0. |
| PONTACAO_TOTAL_TEMA 3 | Pontuação Concentração Flexível | NR_PONT_CONC_FLEX | Flexível / Consumo | +0 — `PC_SAI_FLEX < PC_REF_FLEX`<br>+1 — `PC_SAI_FLEX >= PC_REF_FLEX` e `PC_SAI_FLEX < (PC_REF_FLEX * 1.5)`<br>+2 — `PC_SAI_FLEX >= (PC_REF_FLEX * 1.5)` | Quando `VL_SAI_TOTAL = 0`, recebe +0. |
| PONTACAO_TOTAL_TEMA 4 | Pontuação Concentração Reserva | NR_PONT_CONC_RES | Reserva / Formação de Reserva | +0 — `PC_SAI_RES >= (PC_REF_RES * 1.5)`<br>+1 — `PC_SAI_RES >= PC_REF_RES` e `PC_SAI_RES < (PC_REF_RES * 1.5)`<br>+2 — `PC_SAI_RES < PC_REF_RES` | Quando `VL_SAI_TOTAL = 0`, recebe +0. |
| PONTACAO_TOTAL_TEMA 5 | Pontuação Concentração Crédito | NR_PONT_CONC_CRED | Crédito / Uso Consciente do Crédito | +0 — `PC_SAI_DIV < PC_REF_CRED`<br>+1 — `PC_SAI_DIV >= PC_REF_CRED` e `PC_SAI_DIV < (PC_REF_CRED * 1.5)`<br>+2 — `PC_SAI_DIV >= (PC_REF_CRED * 1.5)` | Quando `VL_SAI_TOTAL = 0`, recebe +0. |

## Pontuação do Orçamento

| Nome antigo | Nome lógico novo | Nome físico novo | CLASSIFICAÇÃO (NÃO CATEGORIA) | Valor Referência | Observação |
|---|---|---|---|---|---|
| PONTUAÇÃO_TOTAL_ORÇAMENTO_TEMA 1 | Pontuação Orçamento Genérica | NR_PONT_ORC_GEN | Genérica / Categorização | Não se aplica: +0 | Tema 1 não utiliza resultado orçamentário. |
| PONTUAÇÃO_TOTAL_ORÇAMENTO_TEMA 2 | Pontuação Orçamento Essencial | NR_PONT_ORC_ESS | Essencial / Orçamento | Deficitário forte: +2<br>Deficitário fraco: +1<br>Neutro forte ou fraco: +1<br>Superavitário fraco ou forte: +0 | Avaliar por `TX_RES_ORC` e `TX_STS_RES`. |
| PONTUAÇÃO_TOTAL_ORÇAMENTO_TEMA 3 | Pontuação Orçamento Flexível | NR_PONT_ORC_FLEX | Flexível / Consumo | Deficitário forte: +2<br>Deficitário fraco: +1<br>Neutro forte ou fraco: +1<br>Superavitário fraco ou forte: +0 | Avaliar por `TX_RES_ORC` e `TX_STS_RES`. |
| PONTUAÇÃO_TOTAL_ORÇAMENTO_TEMA 4 | Pontuação Orçamento Reserva | NR_PONT_ORC_RES | Reserva / Formação de Reserva | Deficitário forte ou fraco: +0<br>Neutro forte ou fraco: +1<br>Superavitário fraco: +1<br>Superavitário forte: +2 | Avaliar por `TX_RES_ORC` e `TX_STS_RES`. |
| PONTUAÇÃO_TOTAL_ORÇAMENTO_TEMA 5 | Pontuação Orçamento Crédito | NR_PONT_ORC_CRED | Crédito / Uso Consciente do Crédito | Deficitário forte: +2<br>Deficitário fraco: +1<br>Neutro forte ou fraco: +1<br>Superavitário fraco ou forte: +0 | Avaliar por `TX_RES_ORC` e `TX_STS_RES`. |

## Pontuação do Perfil

| Nome antigo | Nome lógico novo | Nome físico novo | CLASSIFICAÇÃO (NÃO CATEGORIA) | Valor Referência | Observação |
|---|---|---|---|---|---|
| PONTUAÇÃO_TOTAL_PERFIL_TEMA 1 | Pontuação Perfil Genérica | NR_PONT_PRFL_GEN | Genérica / Categorização | Não se aplica: +0 | Tema 1 não utiliza perfil financeiro. |
| PONTUAÇÃO_TOTAL_PERFIL_TEMA 2 | Pontuação Perfil Essencial | NR_PONT_PRFL_ESS | Essencial / Orçamento | Endividado Acrobata: +2<br>Endividado Inadimplente: +1<br>Equilibrista ou Equilibrista Equilibrista: +1<br>Investidor Precavido, Despreocupado ou Acelerado: +1<br>Demais perfis: +0 | Avaliar por `NM_PRFL_FIN`. |
| PONTUAÇÃO_TOTAL_PERFIL_TEMA 3 | Pontuação Perfil Flexível | NR_PONT_PRFL_FLEX | Flexível / Consumo | Endividado Consciente: +2<br>Endividado Iminente: +1<br>Demais perfis: +0 | Avaliar por `NM_PRFL_FIN`. |
| PONTUAÇÃO_TOTAL_PERFIL_TEMA 4 | Pontuação Perfil Reserva | NR_PONT_PRFL_RES | Reserva / Formação de Reserva | Endividado Consciente: +1<br>Equilibrista ou Equilibrista Equilibrista: +2<br>Investidor Precavido, Despreocupado ou Acelerado: +2<br>Demais perfis: +0 | Avaliar por `NM_PRFL_FIN`. |
| PONTUAÇÃO_TOTAL_PERFIL_TEMA 5 | Pontuação Perfil Crédito | NR_PONT_PRFL_CRED | Crédito / Uso Consciente do Crédito | Endividado Acrobata: +1<br>Endividado Iminente: +2<br>Endividado Inadimplente: +2<br>Demais perfis: +0 | Avaliar por `NM_PRFL_FIN`. |

## Pontuação Final por Tema

| Nome antigo | Nome lógico novo | Nome físico novo | CLASSIFICAÇÃO (NÃO CATEGORIA) | Valor Referência | Observação |
|---|---|---|---|---|---|
| PONTUAÇÃO_TEMA_1 | Pontuação Categorização | NR_PONT_CATEG | Categorização de Gastos | `NR_PONT_CATEG = NR_PONT_CONC_GEN` | Tema 1 — Genérica. |
| PONTUAÇÃO_TEMA_2 | Pontuação Orçamento | NR_PONT_ORC | Gestão de Orçamento | `NR_PONT_ORC = NR_PONT_CONC_ESS + NR_PONT_ORC_ESS + NR_PONT_PRFL_ESS` | Tema 2 — Essencial. |
| PONTUAÇÃO_TEMA_3 | Pontuação Consumo | NR_PONT_CONS | Consumo Planejado | `NR_PONT_CONS = NR_PONT_CONC_FLEX + NR_PONT_ORC_FLEX + NR_PONT_PRFL_FLEX` | Tema 3 — Flexível. |
| PONTUAÇÃO_TEMA_4 | Pontuação Reserva | NR_PONT_RES | Formação de Reserva | `NR_PONT_RES = NR_PONT_CONC_RES + NR_PONT_ORC_RES + NR_PONT_PRFL_RES` | Tema 4 — Reserva. |
| PONTUAÇÃO_TEMA_5 | Pontuação Crédito | NR_PONT_CRED | Uso Consciente do Crédito | `NR_PONT_CRED = NR_PONT_CONC_CRED + NR_PONT_ORC_CRED + NR_PONT_PRFL_CRED` | Tema 5 — Crédito. |

Cada tema recebe apenas a soma dos componentes definidos para ele. A escolha de um único tema prioritário e as regras de desempate ficam para a próxima etapa.

## Marcação de contexto e participação no radar

| Nome antigo | Nome lógico novo | Nome físico novo | CLASSIFICAÇÃO (NÃO CATEGORIA) | Valor Referência | Observação |
|---|---|---|---|---|---|
|  | Marca Agro da Categoria | FL_AGRO_CATEGORIA | Marca técnica transacional | S / N | Campo mantido apenas no mapa de categorias e na camada transacional; não é persistido na tabela final. |
|  | Cliente com Movimentação Agro | FL_TEM_MOV_AGRO | Contexto agro | S / N | Recebe `S` quando houver movimentação de natureza `C` ou `D` em categoria marcada como agro. |
|  | Participação no Radar | FL_PARTICIPA_RADAR | Elegibilidade técnica | S / N | Recebe `S` somente quando houver movimentação mínima, perfis válidos e `FL_TEM_MOV_AGRO = 'N'`. |

### Regras de participação no radar

| Condição | Regra |
|---|---|
| Quantidades mínimas | `QT_TRANS_TOTAL > 0`, `QT_TRANS_ENT > 0` e `QT_TRANS_SAI > 0`. |
| Valores mínimos | `VL_TRANS_ENT > 0` e `VL_TRANS_SAI > 0`. |
| Perfil de renda | `NM_PRFL` diferente de `A CLASSIFICAR`. |
| Macroperfil financeiro | `NM_MAC_PRFL_CLI` diferente de `A CLASSIFICAR`. |
| Microperfil financeiro | `NM_MIC_PRFL_CLI` diferente de `A CLASSIFICAR`. |
| Perfil financeiro unificado | `NM_PRFL_FIN` diferente de `A CLASSIFICAR`. |
| Contexto agro | `FL_TEM_MOV_AGRO = 'N'`. Cliente com movimentação agro não participa do radar. |
