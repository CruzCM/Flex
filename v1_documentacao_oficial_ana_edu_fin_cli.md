# Documentação Oficial — ANA_EDU_FIN_CLI

```python
%%spark

sandbox = "t2i2016"
database = f"sbx_{sandbox}"
nome_tabela = "ana_edu_fin_cli"
tabela_spark = f"{database}.{nome_tabela}"

atualizar_metadado = True

ddl_tabela_spark = f"""
CREATE TABLE {tabela_spark} (

    -- Bloco 1: Dados do cliente
    CD_CLI                     INT             COMMENT 'Código do cliente',
    TS_ATL_TRAN                TIMESTAMP       COMMENT 'Maior timestamp de atualização das transações do cliente no recorte operacional de 90 dias',
    DD_INC_MM_CLC_BLC          SMALLINT        COMMENT 'Dia inicial do cálculo do balanço: 1 a 31; 996 = múltiplas contas elegíveis; 997 = sem conta BB corrente identificável; 999 = conta sem data cadastrada',
    VL_REN_PRES                DECIMAL(18,2)   COMMENT 'Valor da renda presumida do cliente; nulo até a definição da fonte e da regra de preenchimento',
    CD_MAC_PRFL_CLI            BIGINT          COMMENT 'Código do macroperfil financeiro',
    NM_MAC_PRFL_CLI            STRING          COMMENT 'Texto do macroperfil financeiro; CODIGO NAO MAPEADO quando o código estiver fora do domínio conhecido',
    CD_MIC_PRFL_CLI            BIGINT          COMMENT 'Código do microperfil financeiro',
    NM_MIC_PRFL_CLI            STRING          COMMENT 'Texto do microperfil financeiro; CODIGO NAO MAPEADO quando o código estiver fora do domínio conhecido',
    NM_PRFL_FIN                STRING          COMMENT 'Texto unificado do perfil financeiro; nulo sem código e CODIGO NAO MAPEADO para código fora do domínio conhecido',

    -- Bloco 2: Período da análise
    DT_REF_INI                 DATE            COMMENT 'Menor data inicial entre os ciclos financeiros fechados selecionados',
    DT_REF_FIM                 DATE            COMMENT 'Maior data final entre os ciclos financeiros fechados selecionados',
    DT_MES_EXEA                DATE            COMMENT 'Mês de execução do ETL, representado pelo primeiro dia do mês',
    DT_EXEA                    DATE            COMMENT 'Data de execução do ETL',

    -- Bloco 3: Resumo técnico das transações
    QT_TRANS_TOTAL             BIGINT          COMMENT 'Quantidade total de transações',
    QT_TRANS_ENT               BIGINT          COMMENT 'Quantidade de transações de entrada',
    QT_TRANS_SAI               BIGINT          COMMENT 'Quantidade de transações de saída',
    VL_TRANS_ENT               DECIMAL(25,2)   COMMENT 'Valor total de entradas',
    VL_TRANS_SAI               DECIMAL(25,2)   COMMENT 'Valor total de saídas',

    -- Bloco 4: Valores de entrada
    VL_ENT_REN                 DECIMAL(18,2)   COMMENT 'Valores recebidos que representam renda, remuneração ou benefícios',
    VL_ENT_EST                 DECIMAL(18,2)   COMMENT 'Valores devolvidos ou recebidos de volta por correções, cancelamentos ou ajustes',
    VL_ENT_RESG                DECIMAL(18,2)   COMMENT 'Valores recuperados de investimentos ou aplicações financeiras',
    VL_ENT_OUT                 DECIMAL(18,2)   COMMENT 'Valores recebidos cuja origem não foi identificada ou não se enquadram nas demais classificações',
    VL_ENT_CRED                DECIMAL(18,2)   COMMENT 'Valores obtidos por empréstimos, financiamentos ou outras operações de crédito',
    VL_ENT_TOTAL               DECIMAL(18,2)   COMMENT 'Valor total de entrada',

    -- Bloco 5: Valores de saída
    VL_SAI_IND                 DECIMAL(18,2)   COMMENT 'Saídas cujo destino não foi identificado ou não se enquadram nas demais classificações',
    VL_SAI_ESS                 DECIMAL(18,2)   COMMENT 'Gastos necessários para a manutenção da vida e do dia a dia',
    VL_SAI_FLEX                DECIMAL(18,2)   COMMENT 'Gastos relacionados a escolhas pessoais, lazer e estilo de vida',
    VL_SAI_FUT                 DECIMAL(18,2)   COMMENT 'Valores destinados à formação de patrimônio, reserva ou objetivos futuros',
    VL_SAI_OBR                 DECIMAL(18,2)   COMMENT 'Valores destinados ao pagamento de dívidas, parcelas e compromissos financeiros',
    VL_SAI_TOTAL               DECIMAL(18,2)   COMMENT 'Valor total de saída',

    -- Bloco 6: Indicadores de orçamento
    VL_RES_ORC                 DECIMAL(18,2)   COMMENT 'Valor do resultado do orçamento: entradas menos saídas',
    PC_SAI_ENT                 DECIMAL(9,6)    COMMENT 'Percentual do valor total de saídas sobre o valor total de entradas: VL_SAI_TOTAL / VL_ENT_TOTAL',
    CD_RES_ORC                 INT             COMMENT 'Código do resultado do orçamento: 0 = Neutro; 1 = Superavitário; 2 = Deficitário',
    TX_RES_ORC                 STRING          COMMENT 'Texto do resultado do orçamento',
    CD_FAIXA_ORC               INT             COMMENT 'Código da faixa do resultado orçamentário: 0 = Neutro; 1 = Deficitário Moderado; 2 = Deficitário Acentuado; 3 = Superavitário Moderado; 4 = Superavitário Acentuado',
    TX_STS_RES                 STRING          COMMENT 'Status da intensidade do resultado: Acentuado ou Moderado; nulo quando o resultado for Neutro',
    TX_STS_FINAL               STRING          COMMENT 'Texto final composto pelo resultado e seu status',

    -- Bloco 7: Indicadores de saída sobre entrada
    PC_SAI_IND                 DECIMAL(9,6)    COMMENT 'Percentual do valor de saída indeterminada sobre o valor total de entradas: VL_SAI_IND / VL_ENT_TOTAL',
    PC_SAI_ESS                 DECIMAL(9,6)    COMMENT 'Percentual do valor de saída essencial sobre o valor total de entradas: VL_SAI_ESS / VL_ENT_TOTAL',
    PC_SAI_FLEX                DECIMAL(9,6)    COMMENT 'Percentual do valor de saída flexível sobre o valor total de entradas: VL_SAI_FLEX / VL_ENT_TOTAL',
    PC_SAI_FUT                 DECIMAL(9,6)    COMMENT 'Percentual do valor de saída para o futuro sobre o valor total de entradas: VL_SAI_FUT / VL_ENT_TOTAL',
    PC_SAI_OBR                 DECIMAL(9,6)    COMMENT 'Percentual do valor de saída para obrigações sobre o valor total de entradas: VL_SAI_OBR / VL_ENT_TOTAL',

    -- Bloco 8: Parâmetros de referência
    PC_REF_IND                 DECIMAL(9,6)    COMMENT 'Percentual de referência para saída indeterminada',
    PC_REF_ESS                 DECIMAL(9,6)    COMMENT 'Percentual de referência para saída essencial',
    PC_REF_FLEX                DECIMAL(9,6)    COMMENT 'Percentual de referência para saída flexível',
    PC_REF_FUT                 DECIMAL(9,6)    COMMENT 'Percentual de referência para saída destinada ao futuro',
    PC_REF_OBR                 DECIMAL(9,6)    COMMENT 'Percentual de referência para saída de obrigações',

    -- Bloco 9: Pontuação por concentração
    NR_PONT_CONC_IND           INT             COMMENT 'Pontuação de concentração da saída indeterminada',
    NR_PONT_CONC_ESS           INT             COMMENT 'Pontuação de concentração essencial',
    NR_PONT_CONC_FLEX          INT             COMMENT 'Pontuação de concentração flexível',
    NR_PONT_CONC_FUT           INT             COMMENT 'Pontuação de concentração da saída destinada ao futuro',
    NR_PONT_CONC_OBR           INT             COMMENT 'Pontuação de concentração da saída de obrigações',

    -- Bloco 10: Pontuação orçamentária
    NR_PONT_ORC_IND            INT             COMMENT 'Pontuação orçamentária da classificação indeterminada',
    NR_PONT_ORC_ESS            INT             COMMENT 'Pontuação de orçamento essencial',
    NR_PONT_ORC_FLEX           INT             COMMENT 'Pontuação de orçamento flexível',
    NR_PONT_ORC_FUT            INT             COMMENT 'Pontuação orçamentária da classificação futuro',
    NR_PONT_ORC_OBR            INT             COMMENT 'Pontuação orçamentária da classificação obrigações',

    -- Bloco 11: Pontuação por perfil
    NR_PONT_PRFL_IND           INT             COMMENT 'Pontuação por perfil da classificação indeterminada',
    NR_PONT_PRFL_ESS           INT             COMMENT 'Pontuação de perfil essencial',
    NR_PONT_PRFL_FLEX          INT             COMMENT 'Pontuação de perfil flexível',
    NR_PONT_PRFL_FUT           INT             COMMENT 'Pontuação por perfil da classificação futuro',
    NR_PONT_PRFL_OBR           INT             COMMENT 'Pontuação por perfil da classificação obrigações',

    -- Bloco 12: Pontuação consolidada e classificação vencedora
    NR_PONT_IND_FIM            INT             COMMENT 'Pontuação final da classificação indeterminada',
    NR_PONT_ESS_FIM            INT             COMMENT 'Pontuação final da classificação essenciais',
    NR_PONT_FLEX_FIM           INT             COMMENT 'Pontuação final da classificação flexíveis',
    NR_PONT_FUT_FIM            INT             COMMENT 'Pontuação final da classificação futuro',
    NR_PONT_OBR_FIM            INT             COMMENT 'Pontuação final da classificação obrigações',
    CD_TEMA_VENCEDOR           INT             COMMENT 'Código do conceito vencedor: 1 = Categorização dos Gastos; 2 = Gestão de Orçamento; 3 = Consumo Planejado; 4 = Formação de Reserva; 5 = Uso Consciente do Crédito; 9 = Empate; nulo sem pontuação completa',
    TX_TEMA_VENCEDOR           STRING          COMMENT 'Texto do conceito vencedor; nulo quando as cinco pontuações finais não estiverem preenchidas',

    -- Bloco 13: Contexto e elegibilidade
    FL_TEM_MOV_AGRO            STRING          COMMENT 'Indica se o cliente teve movimentação de crédito ou débito em categoria marcada como agro: S ou N',
    FL_PARTICIPA_RADAR         STRING          COMMENT 'Campo reservado para regra futura de participação; nulo nesta versão'
)
COMMENT 'Análise de Educação Financeira do Cliente'
STORED AS PARQUET
TBLPROPERTIES (
    'parquet.compress' = 'SNAPPY'
)
"""

query_drop_tabela = f"DROP TABLE IF EXISTS {tabela_spark}"

if atualizar_metadado:
    spark.sql(query_drop_tabela)
    spark.sql(ddl_tabela_spark)
```

## Identificação da tabela

| Item | Definição |
|---|---|
| Nome lógico | Análise de Educação Financeira do Cliente |
| Nome físico | `ANA_EDU_FIN_CLI` |
| Nome no Hive | `ana_edu_fin_cli` |
| Granularidade | Uma linha por `CD_CLI` do público-alvo, com janela financeira individual. |
| Finalidade | Organizar indicadores do período para apoiar a educação financeira do cliente. |
| Carga | Integral, com `overwrite`. |
| Estrutura final | 71 colunas. |

## Premissas consolidadas

- O usuário informa somente `PERIODOS`, inteiro entre `1` e `6`, que representa a quantidade de ciclos financeiros fechados analisados.
- O público-alvo contém clientes com transações efetivadas, `CD_EST_TRAN_INST = 0`, atualizadas nas 90 datas de calendário encerradas na data de execução.
- A base final usa uma linha por cliente do público-alvo, mesmo quando não houver transação nos ciclos fechados selecionados.
- `TS_ATL_TRAN` representa o maior timestamp de atualização de uma transação efetivada encontrado no recorte operacional de 90 dias; não representa acesso ao sistema.
- `DD_INC_MM_CLC_BLC` é obtido pela conta corrente BB identificada nas transações efetivadas do recorte e usa os códigos técnicos `996`, `997` e `999` quando o dia não puder ser determinado.
- `VL_REN_PRES` permanece nulo para todos os clientes até que a fonte e a regra da renda presumida sejam definidas; o campo não participa dos cálculos nesta versão.
- Os códigos `996`, `997` e `999` permanecem persistidos, mas o cálculo interno da janela usa o dia `1` como fallback.
- O ciclo que contém `TS_ATL_TRAN` é considerado aberto e não participa da análise; somente os ciclos fechados imediatamente anteriores são selecionados.
- O resumo técnico mantém a leitura de entrada e saída pela natureza `C` e `D`.
- Os blocos classificados usam `CD_CLASSIFICACAO_CATEGORIA`, com códigos `0` a `4` para entradas e `5` a `9` para saídas.
- O perfil financeiro é obtido da origem `DVS_GRDR_FNCO_PF` e padronizado nos campos de macroperfil, microperfil e perfil financeiro unificado.
- O resultado do orçamento, os percentuais de referência e as pontuações são calculados a partir da sumarizada.
- A faixa do resultado orçamentário é persistida em `CD_FAIXA_ORC`, com enumeração de `0` a `4`, para centralizar a ligação entre o resultado e as regras de pontuação.
- Os percentuais de saída por categoria são persistidos em `PC_SAI_IND`, `PC_SAI_ESS`, `PC_SAI_FLEX`, `PC_SAI_FUT` e `PC_SAI_OBR`, todos calculados sobre `VL_ENT_TOTAL`.
- Todas as divisões usam `NULLIF` e `COALESCE`; sem denominador válido, o resultado é `0`.
- A marcação agro é definida no mapa de categorias.
- `FL_PARTICIPA_RADAR` permanece `NULL` para todos os clientes nesta versão.
- As regras de negócio e os limiares de pontuação são aplicados de forma padronizada.

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
| `PRES` | Presumida |

> Sequência fixa das classificações consolidadas: **1. Indeterminado; 2. Essenciais; 3. Flexíveis; 4. Futuro; 5. Obrigações.**

## Bloco 1: Dados do cliente

| Nome lógico | Nome físico | Classificação | Valor de referência | Observação |
|---|---|---|---|---|
| Código Cliente | CD_CLI |  |  | Uma linha por cliente do público-alvo. |
| Timestamp da Última Atualização de Transação | TS_ATL_TRAN |  | `MAX(TRAN_RLZD_INST_PCT.TS_ATL_TRAN)` | Maior atualização de transação efetivada no recorte de hoje e das 89 datas anteriores; não representa acesso do cliente ao sistema. |
| Dia Inicial do Cálculo do Balanço | DD_INC_MM_CLC_BLC |  | `CT_GRDR_FNCO.DD_INC_MM_CLC_BLC` | Dia de `1` a `31`; `996` = múltiplas contas elegíveis; `997` = sem conta BB corrente identificável; `999` = conta sem data cadastrada. |
| Valor da Renda Presumida | VL_REN_PRES |  | `NULL` | Dado pessoal reservado para integração futura; ainda sem fonte e regra de seleção definidas. |
| Código Macro Perfil Cliente | CD_MAC_PRFL_CLI |  | `sbx_t2i2016.DVS_GRDR_FNCO_PF` | Registro mais recente por cliente. |
| Nome Macro Perfil Cliente | NM_MAC_PRFL_CLI |  | Endividado / Equilibrista / Investidor | Código nulo produz nome nulo; código fora do domínio recebe `CODIGO NAO MAPEADO`. |
| Código Micro Perfil Cliente | CD_MIC_PRFL_CLI |  | `sbx_t2i2016.DVS_GRDR_FNCO_PF` | Registro mais recente por cliente. |
| Nome Micro Perfil Cliente | NM_MIC_PRFL_CLI |  | Inadimplente / Acrobata / Iminente / Consciente / Equilibrista / Acelerado / Precavido / Despreocupado | Código nulo produz nome nulo; código fora do domínio recebe `CODIGO NAO MAPEADO`. |
| Nome Perfil Financeiro | NM_PRFL_FIN |  | `NM_MAC_PRFL_CLI + ' ' + NM_MIC_PRFL_CLI` | Nulo quando algum código estiver ausente; recebe `CODIGO NAO MAPEADO` quando algum código estiver fora do domínio. |

### Regra do dia inicial do cálculo do balanço

1. Selecionar em `DB2GFP.TRAN_RLZD_INST_PCT` as transações efetivadas das 90 datas de calendário do recorte operacional.
2. Agrupar no DB2 por cliente e identificação de conta, calculando o maior `TS_ATL_TRAN` de cada grupo.
3. No Spark, calcular o maior `TS_ATL_TRAN` entre os grupos de cada cliente para formar o público-alvo.
4. Considerar elegíveis somente as contas com `NR_MCA_PCT_OPB = 999999999`, `CD_PRD = 6`, `NR_AG_TITR` preenchido e `CD_CT_TITR` preenchido.
5. Normalizar e eliminar repetições pela combinação física de `NR_AG_TITR` e `CD_CT_TITR`.
6. Relacionar `NR_AG_TITR` e `CD_CT_TITR` com `DB2GFP.CT_GRDR_FNCO.CD_UOR_CC` e `NR_CC`.
7. Persistir `CT_GRDR_FNCO.DD_INC_MM_CLC_BLC` ou o código técnico correspondente.

A contagem de múltiplas contas considera combinações distintas de agência e conta, de modo que várias transações da mesma conta representam uma única ocorrência. A precedência dos códigos é:

| Código | Condição |
|---:|---|
| `997` | Nenhuma conta BB corrente elegível com agência e conta identificáveis no recorte operacional. |
| `996` | Mais de uma combinação distinta de agência e conta atende aos critérios de elegibilidade. |
| `999` | Exatamente uma ocorrência elegível, mas sem `DD_INC_MM_CLC_BLC` localizado em `CT_GRDR_FNCO`. |

Os códigos de diagnóstico são preservados em `DD_INC_MM_CLC_BLC`. Para calcular os ciclos, qualquer valor fora do intervalo de `1` a `31` usa internamente `DD_INC_MM_CLC_BLC_CALCULO = 1`.

### Regra dos períodos financeiros

- `PERIODOS` aceita valores inteiros de `1` a `6` e não é persistido na tabela final.
- O início de cada ciclo usa `DD_INC_MM_CLC_BLC_CALCULO`. Quando esse dia não existir no mês, usa-se o último dia disponível.
- O ciclo que contém a data de `TS_ATL_TRAN` é o ciclo aberto e fica fora da análise.
- `DT_REF_FIM` é o dia anterior ao início do ciclo aberto.
- `DT_REF_INI` é o início ajustado do ciclo localizado `PERIODOS` meses antes do ciclo aberto.
- As transações analisadas possuem `CD_EST_TRAN_INST = 0` e respeitam a janela individual de cada cliente: `DT_TRAN BETWEEN DT_REF_INI AND DT_REF_FIM`.

Exemplo: com dia do ciclo `10`, `TS_ATL_TRAN = 2026-08-13` e `PERIODOS = 2`, o ciclo aberto começa em `2026-08-10`. A janela fechada consolidada vai de `2026-06-10` a `2026-08-09`.

## Bloco 2: Período da análise

| Nome lógico | Nome físico | Classificação | Valor de referência | Observação |
|---|---|---|---|---|
| Data Inicial de Referência | DT_REF_INI |  | Ciclo fechado mais antigo selecionado | Menor data inicial da janela individual. |
| Data Final de Referência | DT_REF_FIM |  | Dia anterior ao ciclo aberto | Maior data final da janela individual. |
| Mês de Execução | DT_MES_EXEA |  |  | Primeiro dia do mês de execução do ETL. |
| Data de Execução | DT_EXEA |  |  | Data de execução do ETL. |

## Bloco 3: Resumo técnico das transações

| Nome lógico | Nome físico | Classificação | Valor de referência | Observação |
|---|---|---|---|---|
| Código Cliente | CD_CLI |  |  | Uma linha por cliente do público-alvo. |
| Quantidade Transação Total | QT_TRANS_TOTAL |  | Contagem | Todas as transações da janela financeira individual; recebe `0` sem movimento. |
| Quantidade Transação Entrada | QT_TRANS_ENT |  | Contagem | Natureza `C`. |
| Quantidade Transação Saída | QT_TRANS_SAI |  | Contagem | Natureza `D`. |
| Valor Entrada Total Técnico | VL_TRANS_ENT |  | Soma de `VL_TRAN` com natureza `C` | Resumo técnico por natureza. |
| Valor Saída Total Técnico | VL_TRANS_SAI |  | Soma de `VL_TRAN` com natureza `D` | Resumo técnico por natureza. |

## Bloco 4: Valores de entrada

| Nome lógico | Nome físico | Classificação | Valor de referência | Observação |
|---|---|---|---|---|
| Valor Entrada Outras Entradas | VL_ENT_OUT | Outras Entradas | Código 0 | Valores recebidos cuja origem não foi identificada ou não se enquadram nas demais classificações. |
| Valor Entrada Renda | VL_ENT_REN | Renda | Código 1 | Valores recebidos que representam renda, remuneração ou benefícios. |
| Valor Entrada Estorno | VL_ENT_EST | Estorno | Código 2 | Valores devolvidos ou recebidos de volta por correções, cancelamentos ou ajustes. |
| Valor Entrada Resgate | VL_ENT_RESG | Resgate | Código 3 | Valores recuperados de investimentos ou aplicações financeiras. |
| Valor Entrada Crédito | VL_ENT_CRED | Crédito | Código 4 | Valores obtidos por empréstimos, financiamentos ou outras operações de crédito. |
| Valor Entrada Total | VL_ENT_TOTAL |  | `VL_ENT_OUT + VL_ENT_REN + VL_ENT_EST + VL_ENT_RESG + VL_ENT_CRED` |  |

## Bloco 5: Valores de saída

| Nome lógico | Nome físico | Classificação | Valor de referência | Observação |
|---|---|---|---|---|
| Valor Saída Indeterminado | VL_SAI_IND | Indeterminado | Código 5 | Saídas cujo destino não foi identificado ou não se enquadram nas demais classificações. |
| Valor Saída Essenciais | VL_SAI_ESS | Essenciais | Código 6 | Gastos necessários para a manutenção da vida e do dia a dia. |
| Valor Saída Flexíveis | VL_SAI_FLEX | Flexíveis | Código 7 | Gastos relacionados a escolhas pessoais, lazer e estilo de vida. |
| Valor Saída Futuro | VL_SAI_FUT | Futuro | Código 8 | Valores destinados à formação de patrimônio, reserva ou objetivos futuros. |
| Valor Saída Obrigações | VL_SAI_OBR | Obrigações | Código 9 | Valores destinados ao pagamento de dívidas, parcelas e compromissos financeiros. |
| Valor Saída Total | VL_SAI_TOTAL |  | `VL_SAI_IND + VL_SAI_ESS + VL_SAI_FLEX + VL_SAI_FUT + VL_SAI_OBR` |  |

## Bloco 6: Indicadores de orçamento

| Nome lógico | Nome físico | Classificação | Valor de referência | Observação |
|---|---|---|---|---|
| Valor Resultado Orçamento | VL_RES_ORC |  | `VL_ENT_TOTAL - VL_SAI_TOTAL` | Recebe `NULL` quando não houver transações na janela. |
| Código Resultado Orçamento | CD_RES_ORC |  | 0 / 1 / 2 | 0 = Neutro; 1 = Superavitário; 2 = Deficitário. |
| Texto Resultado Orçamento | TX_RES_ORC |  | Neutro / Superavitário / Deficitário | Faixa neutra entre `0,95` e `1,05`. |
| Percentual Saída Entrada | PC_SAI_ENT |  | `VL_SAI_TOTAL / VL_ENT_TOTAL` | Sem `VL_ENT_TOTAL` válido, recebe `0`; a classificação orçamentária permanece `NULL` sem transações. |
| Código Faixa Resultado Orçamento | CD_FAIXA_ORC |  | 0 / 1 / 2 / 3 / 4 | 0 = Neutro; 1 = Deficitário Moderado; 2 = Deficitário Acentuado; 3 = Superavitário Moderado; 4 = Superavitário Acentuado. |
| Texto Status Resultado | TX_STS_RES |  | Acentuado / Moderado / `NULL` | Calculado a partir das faixas do resultado; para `TX_RES_ORC = 'Neutro'`, não possui status de intensidade e recebe `NULL`. |
| Texto Status Final | TX_STS_FINAL |  | `TX_RES_ORC + TX_STS_RES` ou `Neutro` | Para resultado neutro, recebe somente `Neutro`; nos demais casos, combina o resultado com `Acentuado` ou `Moderado`. |

## Bloco 7: Indicadores de saída sobre entrada

| Nome lógico | Nome físico | Classificação | Valor de referência | Observação |
|---|---|---|---|---|
| Percentual Saída Indeterminada sobre Entrada | PC_SAI_IND | Indeterminado | `VL_SAI_IND / VL_ENT_TOTAL` | Sem `VL_ENT_TOTAL` válido, recebe `0`. |
| Percentual Saída Essencial sobre Entrada | PC_SAI_ESS | Essenciais | `VL_SAI_ESS / VL_ENT_TOTAL` | Sem `VL_ENT_TOTAL` válido, recebe `0`. |
| Percentual Saída Flexível sobre Entrada | PC_SAI_FLEX | Flexíveis | `VL_SAI_FLEX / VL_ENT_TOTAL` | Sem `VL_ENT_TOTAL` válido, recebe `0`. |
| Percentual Saída Futuro sobre Entrada | PC_SAI_FUT | Futuro | `VL_SAI_FUT / VL_ENT_TOTAL` | Sem `VL_ENT_TOTAL` válido, recebe `0`. |
| Percentual Saída Obrigações sobre Entrada | PC_SAI_OBR | Obrigações | `VL_SAI_OBR / VL_ENT_TOTAL` | Sem `VL_ENT_TOTAL` válido, recebe `0`. |

## Bloco 8: Parâmetros de referência

| Nome lógico | Nome físico | Classificação | Valor de referência | Observação |
|---|---|---|---|---|
| Percentual Referência Indeterminado | PC_REF_IND | Indeterminado | 75% fixo (`0.750000`) | Limite de referência da classificação. |
| Percentual Referência Essencial | PC_REF_ESS | Essenciais | 50% fixo (`0.500000`) | Limite de referência da classificação. |
| Percentual Referência Flexível | PC_REF_FLEX | Flexíveis | 30% fixo (`0.300000`) | Limite de referência da classificação. |
| Percentual Referência Futuro | PC_REF_FUT | Futuro | 20% fixo (`0.200000`) | Limite de referência da classificação. |
| Percentual Referência Obrigações | PC_REF_OBR | Obrigações | 30% fixo (`0.300000`) | Limite de referência da classificação. |

## Bloco 9: Pontuação por concentração

Quando `QT_TRANS_TOTAL = 0`, todas as pontuações dos blocos 9, 10, 11 e 12 recebem `NULL`. As regras abaixo são aplicadas somente quando houver transações na janela financeira.

| Nome lógico | Nome físico | Classificação | Valor de referência | Observação |
|---|---|---|---|---|
| Pontuação Concentração Indeterminada | NR_PONT_CONC_IND | Indeterminado | +0 — `PC_SAI_IND <= PC_REF_IND`<br>+99 — `PC_SAI_IND > PC_REF_IND` | Recebe `NULL` quando não houver transações na janela. |
| Pontuação Concentração Essencial | NR_PONT_CONC_ESS | Essencial / Orçamento | +0 — `PC_SAI_ESS < PC_REF_ESS`<br>+1 — `PC_SAI_ESS >= PC_REF_ESS` e `PC_SAI_ESS < (PC_REF_ESS * 1.5)`<br>+2 — `PC_SAI_ESS >= (PC_REF_ESS * 1.5)` | Recebe `NULL` quando não houver transações na janela. |
| Pontuação Concentração Flexível | NR_PONT_CONC_FLEX | Flexível / Consumo | +0 — `PC_SAI_FLEX < PC_REF_FLEX`<br>+1 — `PC_SAI_FLEX >= PC_REF_FLEX` e `PC_SAI_FLEX < (PC_REF_FLEX * 1.5)`<br>+2 — `PC_SAI_FLEX >= (PC_REF_FLEX * 1.5)` | Recebe `NULL` quando não houver transações na janela. |
| Pontuação Concentração Futuro | NR_PONT_CONC_FUT | Futuro | +0 — `PC_SAI_FUT >= (PC_REF_FUT * 1.5)`<br>+1 — `PC_SAI_FUT >= PC_REF_FUT` e `PC_SAI_FUT < (PC_REF_FUT * 1.5)`<br>+2 — `PC_SAI_FUT < PC_REF_FUT` | Recebe `NULL` quando não houver transações na janela. |
| Pontuação Concentração Obrigações | NR_PONT_CONC_OBR | Obrigações | +0 — `PC_SAI_OBR < PC_REF_OBR`<br>+1 — `PC_SAI_OBR >= PC_REF_OBR` e `PC_SAI_OBR < (PC_REF_OBR * 1.5)`<br>+2 — `PC_SAI_OBR >= (PC_REF_OBR * 1.5)` | Recebe `NULL` quando não houver transações na janela. |

## Bloco 10: Pontuação orçamentária

| Nome lógico | Nome físico | Classificação | Valor de referência | Observação |
|---|---|---|---|---|
| Pontuação Orçamentária Indeterminada | NR_PONT_ORC_IND | Indeterminado | Não se aplica: +0 | A classificação não utiliza resultado orçamentário. |
| Pontuação Orçamentária Essenciais | NR_PONT_ORC_ESS | Essenciais | Deficitário acentuado: +2<br>Deficitário moderado: +1<br>Neutro: +1<br>Superavitário moderado ou acentuado: +0 | Avaliar por `TX_RES_ORC` e `TX_STS_RES`. |
| Pontuação Orçamentária Flexíveis | NR_PONT_ORC_FLEX | Flexíveis | Deficitário acentuado: +2<br>Deficitário moderado: +1<br>Neutro: +1<br>Superavitário moderado ou acentuado: +0 | Avaliar por `TX_RES_ORC` e `TX_STS_RES`. |
| Pontuação Orçamentária Futuro | NR_PONT_ORC_FUT | Futuro | Deficitário acentuado ou moderado: +0<br>Neutro: +1<br>Superavitário moderado: +1<br>Superavitário acentuado: +2 | Avaliar por `TX_RES_ORC` e `TX_STS_RES`. |
| Pontuação Orçamentária Obrigações | NR_PONT_ORC_OBR | Obrigações | Deficitário acentuado: +2<br>Deficitário moderado: +1<br>Neutro: +1<br>Superavitário moderado ou acentuado: +0 | Avaliar por `TX_RES_ORC` e `TX_STS_RES`. |

## Bloco 11: Pontuação por perfil

Para Essenciais, Flexíveis, Futuro e Obrigações, `NM_PRFL_FIN` nulo ou igual a `CODIGO NAO MAPEADO` produz pontuação nula. Nas regras abaixo, "demais perfis" significa somente os demais perfis reconhecidos.

| Nome lógico | Nome físico | Classificação | Valor de referência | Observação |
|---|---|---|---|---|
| Pontuação por Perfil Indeterminado | NR_PONT_PRFL_IND | Indeterminado | Não se aplica: +0 | A classificação não utiliza perfil financeiro. |
| Pontuação por Perfil Essenciais | NR_PONT_PRFL_ESS | Essenciais | Endividado Acrobata: +2<br>Endividado Inadimplente: +1<br>Equilibrista ou Equilibrista Equilibrista: +1<br>Investidor Precavido, Despreocupado ou Acelerado: +1<br>Demais perfis: +0 | Avaliar por `NM_PRFL_FIN`. |
| Pontuação por Perfil Flexíveis | NR_PONT_PRFL_FLEX | Flexíveis | Endividado Consciente: +2<br>Endividado Iminente: +1<br>Demais perfis: +0 | Avaliar por `NM_PRFL_FIN`. |
| Pontuação por Perfil Futuro | NR_PONT_PRFL_FUT | Futuro | Endividado Consciente: +1<br>Equilibrista ou Equilibrista Equilibrista: +2<br>Investidor Precavido, Despreocupado ou Acelerado: +2<br>Demais perfis: +0 | Avaliar por `NM_PRFL_FIN`. |
| Pontuação por Perfil Obrigações | NR_PONT_PRFL_OBR | Obrigações | Endividado Acrobata: +1<br>Endividado Iminente: +2<br>Endividado Inadimplente: +2<br>Demais perfis: +0 | Avaliar por `NM_PRFL_FIN`. |

## Bloco 12: Pontuação consolidada e classificação vencedora

| Nome lógico | Nome físico | Classificação | Valor de referência | Observação |
|---|---|---|---|---|
| Pontuação Final Indeterminado | NR_PONT_IND_FIM | Indeterminado | `NR_PONT_IND_FIM = NR_PONT_CONC_IND` |  |
| Pontuação Final Essenciais | NR_PONT_ESS_FIM | Essenciais | `NR_PONT_ESS_FIM = NR_PONT_CONC_ESS + NR_PONT_ORC_ESS + NR_PONT_PRFL_ESS` |  |
| Pontuação Final Flexíveis | NR_PONT_FLEX_FIM | Flexíveis | `NR_PONT_FLEX_FIM = NR_PONT_CONC_FLEX + NR_PONT_ORC_FLEX + NR_PONT_PRFL_FLEX` |  |
| Pontuação Final Futuro | NR_PONT_FUT_FIM | Futuro | `NR_PONT_FUT_FIM = NR_PONT_CONC_FUT + NR_PONT_ORC_FUT + NR_PONT_PRFL_FUT` |  |
| Pontuação Final Obrigações | NR_PONT_OBR_FIM | Obrigações | `NR_PONT_OBR_FIM = NR_PONT_CONC_OBR + NR_PONT_ORC_OBR + NR_PONT_PRFL_OBR` |  |
| Código do Conceito Vencedor | CD_TEMA_VENCEDOR |  | 1 / 2 / 3 / 4 / 5 / 9 / `NULL` | Calculado somente quando as cinco pontuações finais estiverem preenchidas; `9` representa empate. |
| Texto do Conceito Vencedor | TX_TEMA_VENCEDOR |  | Categorização dos Gastos / Gestão de Orçamento / Consumo Planejado / Formação de Reserva / Uso Consciente do Crédito / Empate / `NULL` | Recebe `NULL` quando alguma pontuação final estiver ausente. |

`CD_TEMA_VENCEDOR` e `TX_TEMA_VENCEDOR` identificam o conceito educacional vencedor a partir das cinco pontuações consolidadas. Em empate, recebem `9` e `Empate`. Sem pontuação completa, ambos recebem `NULL`. O código `0` não é produzido nesta versão.

| Pontuação consolidada | Conceito vencedor |
|---|---|
| `NR_PONT_IND_FIM` | Categorização dos Gastos |
| `NR_PONT_ESS_FIM` | Gestão de Orçamento |
| `NR_PONT_FLEX_FIM` | Consumo Planejado |
| `NR_PONT_FUT_FIM` | Formação de Reserva |
| `NR_PONT_OBR_FIM` | Uso Consciente do Crédito |

## Bloco 13: Contexto e elegibilidade

| Nome lógico | Nome físico | Classificação | Valor de referência | Observação |
|---|---|---|---|---|
| Marca Agro da Categoria | FL_AGRO_CATEGORIA | Marca técnica transacional | S / N | Campo mantido apenas no mapa de categorias e na camada transacional; não é persistido na tabela final. |
| Cliente com Movimentação Agro | FL_TEM_MOV_AGRO | Contexto agro | S / N | Recebe `S` quando houver movimentação de natureza `C` ou `D` em categoria marcada como agro. |
| Participação no Radar | FL_PARTICIPA_RADAR | Regra futura | `NULL` | A lógica de participação está suspensa nesta versão. |

### Participação no radar

Não há regra de elegibilidade nesta etapa. `FL_PARTICIPA_RADAR` recebe `NULL` para todos os clientes, independentemente de movimentação, perfil, contexto agro ou diagnóstico do dia do ciclo.
