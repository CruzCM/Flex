# Tabela de Saída do ETL — Versão Final

> nomes a serem escolhidos 
MOM_FNC_CLI (Momento Financeiro Cliente)
ACMP_ANA_FNC_CLI (Acompanhamento Analítico Financeiro Cliente)
ACMP_FNC_ANA_CLI (Acompanhamento Financeiro Analítico Cliente)
IN_ANA_EDU_FNC_CLI(indicadores Analíticos de Educação Financeira do Cliente)
ANA_IND_EDU_FNC_CLI (Análise de Indicadores de Educação Financeira do Cliente)
ANA_EDU_FIN_CLI (Análise de Educação Financeira do Cliente)

## Identificação

| Nome antigo | Nome lógico novo | Nome físico novo | CLASSIFICAÇÃO (NÃO CATEGORIA) | Valor Referência | Observação |
|---|---|---|---|---|---|
|  | Data Execução | DT_EXEA |  |  |  |
|  | Data Mês Referência | DT_MES_REF |  |  |  |
| CD_CLI | Código Cliente | CD_CLI |  |  |  |
|  | Código Perfil Renda | CD_PRFL_REN |  |  |  |
|  | Texto Perfil Renda | TX_PRFL_REN |  |  |  |
| IDADE(...) | Idade Cliente | NR_IDD_CLI |  |  |  |
| QTD_TOTAL_TRANSACAO | Quantidade Transação Total | QT_TRANS_TOTAL |  | CONTAGEM |  |
| QTD_TOTAL_CREDITO | Quantidade Crédito Total | QT_CRED_TOTAL |  | CONTAGEM |  |
| QTD_TOTAL_DEBITO | Quantidade Débito Total | QT_DEB_TOTAL |  | CONTAGEM |  |
| CD_PERFIL | Código Perfil Financeiro | CD_PRFL_FIN |  | TABELA DB2D1D. DVS_GRDR_FNCO_PF |  |
| TX_PERFIL | Texto Perfil Financeiro | TX_PRFL_FIN |  | ENDIVIDADO/EQUILIBRADO/INVESTIDOR |  |
| CD_SUB_PERFIL | Código Subperfil Financeiro | CD_SPRFL_FIN |  | TABELA DB2D1D. DVS_GRDR_FNCO_PF |  |
| TX_SUB_PERFIL | Texto Subperfil Financeiro | TX_SPRFL_FIN |  | ACOBRATA,IMINENTE,INADIMPLENTE, |  |
| TX_PERFIL_FINAL | Texto Perfil Financeiro Final | TX_PRFL_FIN_FIM |  | TX_PERFIL + TX_SUB_PERFIL |  |

## Blocos de Crédito

| Nome antigo | Nome lógico novo | Nome físico novo | CLASSIFICAÇÃO (NÃO CATEGORIA) | Valor Referência | Observação |
|---|---|---|---|---|---|
| C1 | Valor Crédito Receita Benefício | VL_CRED_REC_BEN | Receita / rendimento / benefício |  |  |
| C2 | Valor Crédito Restituição Ajuste | VL_CRED_REST_AJST | Restituição / estorno / ajuste |  |  |
| C3 | Valor Crédito Resgate Investimento | VL_CRED_RESG_INV | Resgate de investimento |  |  |
| C4 | Valor Crédito Transferência Indefinida | VL_CRED_TRANSF_IND | Transferência / entrada indefinida |  |  |
| C5 | Valor Crédito Liberado | VL_CRED_LIB | Crédito tomado / liberação de crédito |  |  |
| Entrada_Total | Valor Entrada Total | VL_ENT_TOTAL |  | VL_ENT_TOTAL = VL_CRED_REC_BEN + VL_CRED_REST_AJST + VL_CRED_RESG_INV + VL_CRED_TRANSF_IND + VL_CRED_LIB |  |

## Blocos de Débito

| Nome antigo | Nome lógico novo | Nome físico novo | CLASSIFICAÇÃO (NÃO CATEGORIA) | Valor Referência | Observação |
|---|---|---|---|---|---|
| D1 | Valor Débito Genérico | VL_DEB_GEN | Genérico / não classificado |  |  |
| D2 | Valor Débito Essencial | VL_DEB_ESS | Essenciais |  |  |
| D3 | Valor Débito Flexível | VL_DEB_FLEX | Flexíveis |  |  |
| D4 | Valor Débito Futuro | VL_DEB_FUT | Reserva / Futuro |  |  |
| D5 | Valor Débito Crédito | VL_DEB_CRED | Dívidas / crédito / custo financeiro |  |  |
| Saida_Total | Valor Saída Total | VL_SAI_TOTAL |  | VL_SAI_TOTAL = VL_DEB_GEN + VL_DEB_ESS + VL_DEB_FLEX + VL_DEB_FUT + VL_DEB_CRED |  |

## Resultado do Orçamento

| Nome antigo | Nome lógico novo | Nome físico novo | CLASSIFICAÇÃO (NÃO CATEGORIA) | Valor Referência | Observação |
|---|---|---|---|---|---|
| Valor_Resultado_Orçamento | Valor Resultado Orçamento | VL_RES_ORC |  | VL_RES_ORC = VL_ENT_TOTAL - VL_SAI_TOTAL |  |
| Codigo_Resultado_Orçamento | Código Resultado Orçamento | CD_RES_ORC |  | 0,1,2 |  |
| Texto_Resultado_Orçamento | Texto Resultado Orçamento | TX_RES_ORC |  | NEUTRO, SUPERAVITÁRIO, DEFICITÁRIO |  |
| %_Resultado (verificar nome) | Percentual Saída Entrada | PC_SAI_ENT |  | VL_SAI_TOTAL / VL_ENT_TOTAL |  |
| tx_status_resultado | Texto Status Resultado | TX_STS_RES |  | faixa2(forte),faixa1(fraco) |  |
| tx_status_final | Texto Status Final | TX_STS_FINAL |  | Texto_Resultado_Orçamento + tx_status_resultado (neutro + forte) |  |

## Percentuais dos Créditos

| Nome antigo | Nome lógico novo | Nome físico novo | CLASSIFICAÇÃO (NÃO CATEGORIA) | Valor Referência | Observação |
|---|---|---|---|---|---|
| PERCENTUAL_C1 | Percentual Crédito Receita Benefício Entrada | PC_CRED_REC_BEN_ENT | (%) Receita / rendimento / benefício | VL_CRED_REC_BEN / VL_ENT_TOTAL |  |
| PERCENTUAL_C2 | Percentual Crédito Restituição Ajuste Entrada | PC_CRED_REST_AJST_ENT | (%) Restituição / estorno / ajuste | VL_CRED_REST_AJST / VL_ENT_TOTAL |  |
| PERCENTUAL_C3 | Percentual Crédito Resgate Investimento Entrada | PC_CRED_RESG_INV_ENT | (%) Resgate de investimento | VL_CRED_RESG_INV / VL_ENT_TOTAL |  |
| PERCENTUAL_C4 | Percentual Crédito Transferência Indefinida Entrada | PC_CRED_TRANSF_IND_ENT | (%) Transferência / entrada indefinida | VL_CRED_TRANSF_IND / VL_ENT_TOTAL |  |
| PERCENTUAL_C5 | Percentual Crédito Liberação Entrada | PC_CRED_LIB_ENT | (%) Crédito tomado / liberação de crédito | VL_CRED_LIB / VL_ENT_TOTAL |  |

## Percentuais dos Débitos

| Nome antigo | Nome lógico novo | Nome físico novo | CLASSIFICAÇÃO (NÃO CATEGORIA) | Valor Referência | Observação |
|---|---|---|---|---|---|
| PERCENTUAL_D1 | Percentual Débito Genérico Saída | PC_DEB_GEN_SAI | (%) Genérico / não classificado | VL_DEB_GEN / VL_SAI_TOTAL |  |
| PERCENTUAL_D2 | Percentual Débito Essencial Saída | PC_DEB_ESS_SAI | (%) Essenciais | VL_DEB_ESS / VL_SAI_TOTAL |  |
| PERCENTUAL_D3 | Percentual Débito Flexível Saída | PC_DEB_FLEX_SAI | (%) Flexíveis | VL_DEB_FLEX / VL_SAI_TOTAL |  |
| PERCENTUAL_D4 | Percentual Débito Futuro Saída | PC_DEB_FUT_SAI | (%) Reserva / Futuro | VL_DEB_FUT / VL_SAI_TOTAL |  |
| PERCENTUAL_D5 | Percentual Débito Crédito Saída | PC_DEB_CRED_SAI | (%) Dívidas / crédito / custo financeiro | VL_DEB_CRED / VL_SAI_TOTAL |  |

## Percentuais de Referência

| Nome antigo | Nome lógico novo | Nome físico novo | CLASSIFICAÇÃO (NÃO CATEGORIA) | Valor Referência | Observação |
|---|---|---|---|---|---|
| PRP_D1 | Percentual Referência Genérico | PC_REF_GEN | (75%) Genérico / não classificado | 75% fixo |  |
| PRP_D2 | Percentual Referência Essencial | PC_REF_ESS | (50%) Essenciais | 50% fixo |  |
| PRP_D3 | Percentual Referência Flexível | PC_REF_FLEX | (30%) Flexíveis | 30% fixo |  |
| PRP_D4 | Percentual Referência Futuro | PC_REF_FUT | (20%) Reserva / Futuro | 20% fixo |  |
| PRP_D5 | Percentual Referência Crédito | PC_REF_CRED | (30%) Dívidas / crédito / custo financeiro | 30% fixo |  |

## Pontuação por Concentração

| Nome antigo | Nome lógico novo | Nome físico novo | CLASSIFICAÇÃO (NÃO CATEGORIA) | Valor Referência | Observação |
|---|---|---|---|---|---|
| PONTACAO_TOTAL_TEMA 1 | Pontuação Concentração Genérica | NR_PONT_CONC_GEN |  | se PC_DEB_GEN_SAI > 75% = 0 + 99 |  |
| PONTACAO_TOTAL_TEMA 2 | Pontuação Concentração Essencial | NR_PONT_CONC_ESS |  | + 0 – PC_DEB_ESS_SAI < 50%<br>+ 1 – PC_DEB_ESS_SAI < 75%<br>+ 2 – PC_DEB_ESS_SAI > 75% |  |
| PONTACAO_TOTAL_TEMA 3 | Pontuação Concentração Flexível | NR_PONT_CONC_FLEX |  |  |  |
| PONTACAO_TOTAL_TEMA 4 | Pontuação Concentração Futuro | NR_PONT_CONC_FUT |  |  |  |
| PONTACAO_TOTAL_TEMA 5 | Pontuação Concentração Crédito | NR_PONT_CONC_CRED |  |  |  |

## Pontuação do Orçamento

| Nome antigo | Nome lógico novo | Nome físico novo | CLASSIFICAÇÃO (NÃO CATEGORIA) | Valor Referência | Observação |
|---|---|---|---|---|---|
| PONTUAÇÃO_TOTAL_ORÇAMENTO_TEMA 1 | Pontuação Orçamento Genérica | NR_PONT_ORC_GEN |  | • Deficitário forte: +2.<br>• Deficitário fraco: +1.<br>• Neutro forte ou neutro fraco: +1.<br>• Superavitário fraco ou forte: +0. |  |
| PONTUAÇÃO_TOTAL_ORÇAMENTO_TEMA 2 | Pontuação Orçamento Essencial | NR_PONT_ORC_ESS |  |  |  |
| PONTUAÇÃO_TOTAL_ORÇAMENTO_TEMA 3 | Pontuação Orçamento Flexível | NR_PONT_ORC_FLEX |  |  |  |
| PONTUAÇÃO_TOTAL_ORÇAMENTO_TEMA 4 | Pontuação Orçamento Futuro | NR_PONT_ORC_FUT |  |  |  |
| PONTUAÇÃO_TOTAL_ORÇAMENTO_TEMA 5 | Pontuação Orçamento Crédito | NR_PONT_ORC_CRED |  |  |  |

## Pontuação do Perfil

| Nome antigo | Nome lógico novo | Nome físico novo | CLASSIFICAÇÃO (NÃO CATEGORIA) | Valor Referência | Observação |
|---|---|---|---|---|---|
| PONTUAÇÃO_TOTAL_PERFIL_TEMA 1 | Pontuação Perfil Genérica | NR_PONT_PRFL_GEN |  | • Endividado Acrobata: +2.<br>• Endividado Inadimplente: +1.<br>• Equilibrista: +1.<br>• Investidor Precavido, Protegido, Despreocupado ou Acelerado: +1. |  |
| PONTUAÇÃO_TOTAL_PERFIL_TEMA 2 | Pontuação Perfil Essencial | NR_PONT_PRFL_ESS |  |  |  |
| PONTUAÇÃO_TOTAL_PERFIL_TEMA 3 | Pontuação Perfil Flexível | NR_PONT_PRFL_FLEX |  |  |  |
| PONTUAÇÃO_TOTAL_PERFIL_TEMA 4 | Pontuação Perfil Futuro | NR_PONT_PRFL_FUT |  |  |  |
| PONTUAÇÃO_TOTAL_PERFIL_TEMA 5 | Pontuação Perfil Crédito | NR_PONT_PRFL_CRED |  |  |  |

## Pontuação Final por Tema

| Nome antigo | Nome lógico novo | Nome físico novo | CLASSIFICAÇÃO (NÃO CATEGORIA) | Valor Referência | Observação |
|---|---|---|---|---|---|
| PONTUAÇÃO_TEMA_1 | Pontuação Categorização | NR_PONT_CATEG | CATEGORIZAÇÃO DE GASTO<br>(começa 0 pontos) | se PC_DEB_GEN_SAI > 75% = 0 + 99 |  |
| PONTUAÇÃO_TEMA_2 | Pontuação Orçamento | NR_PONT_ORC | GESTÃO DE ORÇAMENTO<br>(começa 0 pontos) | + 0 – PC_DEB_ESS_SAI < 50%<br>+ 1 – PC_DEB_ESS_SAI < 75%<br>+ 2 – PC_DEB_ESS_SAI > 75%<br>------<br>• Deficitário forte: +2.<br>• Deficitário fraco: +1.<br>• Neutro forte ou neutro fraco: +1.<br>• Superavitário fraco ou forte: +0.<br>------<br>• Endividado Acrobata: +2.<br>• Endividado Inadimplente: +1.<br>• Equilibrista: +1.<br>• Investidor Precavido, Protegido, Despreocupado ou Acelerado: +1. |  |
| PONTUAÇÃO_TEMA_3 | Pontuação Consumo | NR_PONT_CONS | CONSUMO PLANEJADO<br>(começa 0 pontos) | + 0 – PC_DEB_FLEX_SAI < 30%<br>+ 1 – PC_DEB_FLEX_SAI < 45%<br>+ 2 – PC_DEB_FLEX_SAI > 45%<br>------<br>• Deficitário forte: +2.<br>• Deficitário fraco: +1.<br>• Neutro negativo ou neutro positivo: +1.<br>• Superavitário fraco ou forte: +0.<br>------<br>• Endividado Consciente: +2.<br>• Endividado Iminente: +1. |  |
| PONTUAÇÃO_TEMA_4 | Pontuação Reserva | NR_PONT_RES | Formação de Reserva<br>(começa 0 pontos) | + 0 – PC_DEB_FUT_SAI >30%<br>+ 1 – PC_DEB_FUT_SAI < 20%<br>+ 2 – PC_DEB_FUT_SAI = 0%<br>------<br>• Deficitário forte ou fraco: +0.<br>• Neutro negativo ou neutro positivo: +1.<br>• Superavitário fraco: +1.<br>• Superavitário forte: +2.<br>------<br>• Endividado Consciente: +1.<br>• Equilibrista: +2.<br>• Investidor Precavido, Protegido, Despreocupado ou Acelerado: +2. |  |
| PONTUAÇÃO_TEMA_5 | Pontuação Crédito | NR_PONT_CRED | USO CONSCIENTE DO CREDITO<br>(começa 0 pontos) | + 0 – PC_DEB_CRED_SAI >30%<br>+ 1 – PC_DEB_CRED_SAI < 20%<br>+ 2 – PC_DEB_CRED_SAI = 0%<br>------<br>• Deficitário forte: +2.<br>• Deficitário fraco: +1.<br>• Neutro negativo ou neutro positivo: +1.<br>• Superavitário fraco ou forte: +0.<br>------<br>• Endividado Acrobata: +1.<br>• Endividado Iminente: +2.<br>• Endividado Inadimplente: +2. |  |
