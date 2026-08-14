# A trajetoria dos dados na ANA_EDU_FIN_CLI

## Objetivo

Este documento explica como cada cliente e cada transacao percorrem o ETL ate formar uma linha da tabela `ANA_EDU_FIN_CLI`. A sequencia acompanha a dependencia entre os dados: primeiro o cliente entra no publico, depois recebe uma janela financeira, suas transacoes sao classificadas e agregadas e, por fim, sao calculados indicadores, pontuacoes, vencedor e flags.

A tabela final possui uma linha por cliente do publico-alvo e 71 atributos. A carga e integral, com `overwrite`.

As referencias seguem o formato `tabela`.`atributo`. Views e atributos intermediarios aparecem somente quando ajudam a explicar a origem de um atributo persistido.

## Visao geral da jornada

O fluxo utiliza tres fontes principais:

| Fonte | Participacao na historia do dado |
|---|---|
| `DB2GFP.TRAN_RLZD_INST_PCT` | Forma o publico-alvo, identifica as contas e fornece as transacoes da janela financeira. |
| `DB2GFP.CT_GRDR_FNCO` | Fornece o dia inicial do ciclo financeiro da conta. |
| `sbx_t2i2016.DVS_GRDR_FNCO_PF` | Fornece o macroperfil e o microperfil financeiro mais recentes. |

O parametro `PERIODOS`, informado na execucao com valor de 1 a 6, define quantos ciclos financeiros fechados serao analisados. Ele orienta o calculo da janela, mas nao e persistido em `ANA_EDU_FIN_CLI`.

## 1. O cliente entra no publico-alvo

### `ANA_EDU_FIN_CLI`.`CD_CLI`

`ANA_EDU_FIN_CLI`.`CD_CLI` identifica o cliente e define a granularidade da tabela final. Sua origem e `DB2GFP.TRAN_RLZD_INST_PCT`.`CD_CLI`.

Um cliente entra no publico quando possui ao menos uma transacao com `DB2GFP.TRAN_RLZD_INST_PCT`.`CD_EST_TRAN_INST` igual a `0` e `DB2GFP.TRAN_RLZD_INST_PCT`.`TS_ATL_TRAN` dentro das 90 datas de calendario consideradas pela execucao: a data atual e as 89 datas anteriores. A partir desse ponto, o cliente permanece no fluxo mesmo que nao possua transacoes dentro dos ciclos financeiros fechados que serao analisados.

### `ANA_EDU_FIN_CLI`.`TS_ATL_TRAN`

No DB2, o recorte e agrupado por cliente e conta e produz o maior `DB2GFP.TRAN_RLZD_INST_PCT`.`TS_ATL_TRAN` de cada grupo. No Spark, `ANA_EDU_FIN_CLI`.`TS_ATL_TRAN` recebe o maior valor entre os grupos do cliente. O resultado e o maior timestamp individual encontrado no recorte operacional de 90 dias, sempre considerando apenas `DB2GFP.TRAN_RLZD_INST_PCT`.`CD_EST_TRAN_INST = 0`.

Esse timestamp representa a atualizacao transacional mais recente do cliente no recorte. Ele nao representa a ultima entrada do cliente em um sistema. Sua funcao no ETL e localizar o ciclo financeiro que ainda esta aberto.

### `ANA_EDU_FIN_CLI`.`VL_REN_PRES`

`ANA_EDU_FIN_CLI`.`VL_REN_PRES` reserva o valor da renda presumida como dado pessoal do cliente. Nesta versao, `query_renda_presumida` parte do publico-alvo e atribui `NULL` a todos os clientes. A origem e a regra de escolha serao definidas futuramente.

O campo nao representa `DB2GFP.REN_INFD_CLI`.`VL_REN_INFD`, pois essa origem descreve renda informada pelo cliente. Enquanto permanecer nulo, `ANA_EDU_FIN_CLI`.`VL_REN_PRES` nao participa de percentuais, orcamento, pontuacoes ou da escolha do conceito vencedor.

## 2. A conta determina o dia do ciclo

### Caminho entre cliente, conta e ciclo

O recorte inicial ja traz de `DB2GFP.TRAN_RLZD_INST_PCT` os atributos necessarios para identificar a conta de cada cliente. Uma conta e elegivel quando atende simultaneamente a:

- `DB2GFP.TRAN_RLZD_INST_PCT`.`NR_MCA_PCT_OPB = 999999999`;
- `DB2GFP.TRAN_RLZD_INST_PCT`.`CD_PRD = 6`;
- `DB2GFP.TRAN_RLZD_INST_PCT`.`NR_AG_TITR` preenchido;
- `DB2GFP.TRAN_RLZD_INST_PCT`.`CD_CT_TITR` preenchido.

A agencia e a conta seguem para `DB2GFP.CT_GRDR_FNCO` por duas ligacoes:

- `DB2GFP.TRAN_RLZD_INST_PCT`.`NR_AG_TITR` com `DB2GFP.CT_GRDR_FNCO`.`CD_UOR_CC`;
- `DB2GFP.TRAN_RLZD_INST_PCT`.`CD_CT_TITR` com `DB2GFP.CT_GRDR_FNCO`.`NR_CC`.

No Spark, agencia e conta sao normalizadas e as repeticoes da mesma combinacao fisica sao eliminadas. Assim, varias transacoes da mesma conta continuam representando apenas uma conta elegivel.

### `ANA_EDU_FIN_CLI`.`DD_INC_MM_CLC_BLC`

Quando o caminho encontra uma unica conta elegivel e seu cadastro financeiro, `ANA_EDU_FIN_CLI`.`DD_INC_MM_CLC_BLC` recebe `DB2GFP.CT_GRDR_FNCO`.`DD_INC_MM_CLC_BLC`, com valor de 1 a 31. Esse dia define quando cada ciclo financeiro do cliente comeca.

Quando o dia nao pode ser determinado, o mesmo atributo guarda um diagnostico:

| Valor de `ANA_EDU_FIN_CLI`.`DD_INC_MM_CLC_BLC` | Situacao encontrada |
|---:|---|
| `996` | Mais de uma combinacao distinta de agencia e conta atende aos criterios de elegibilidade. |
| `997` | Nenhuma conta BB corrente elegivel possui agencia e conta identificaveis no recorte. |
| `999` | Existe exatamente uma conta elegivel, mas o dia nao foi localizado em `DB2GFP.CT_GRDR_FNCO`. |

Esses codigos sao persistidos para preservar o diagnostico. Para que o calculo da janela continue, a view intermediaria usa `vw_janela_financeira`.`DD_INC_MM_CLC_BLC_CALCULO = 1` sempre que o valor persistido nao estiver entre 1 e 31. Esse fallback altera apenas o calculo; nao substitui o diagnostico gravado na tabela final.

## 3. O ciclo se transforma em janela financeira

O ETL usa `ANA_EDU_FIN_CLI`.`TS_ATL_TRAN`, o dia de calculo do ciclo e `PERIODOS` para separar o ciclo aberto dos ciclos fechados. Se o dia configurado nao existir em determinado mes, como 31 em fevereiro, o inicio daquele ciclo e ajustado para o ultimo dia disponivel no mes.

### `ANA_EDU_FIN_CLI`.`DT_REF_INI`

`ANA_EDU_FIN_CLI`.`DT_REF_INI` e o inicio do ciclo fechado mais antigo selecionado. O ETL primeiro encontra o inicio do ciclo aberto que contem `ANA_EDU_FIN_CLI`.`TS_ATL_TRAN` e volta a quantidade de meses informada em `PERIODOS`. O dia do ciclo e novamente ajustado ao ultimo dia do mes quando necessario.

Esse atributo se torna o limite inferior individual para a leitura das transacoes do cliente.

### `ANA_EDU_FIN_CLI`.`DT_REF_FIM`

`ANA_EDU_FIN_CLI`.`DT_REF_FIM` e o dia imediatamente anterior ao inicio do ciclo aberto. Ele representa o ultimo dia do ciclo fechado mais recente e se torna o limite superior individual da analise transacional.

### Exemplo de dois periodos

Considere um cliente ficticio com:

- `ANA_EDU_FIN_CLI`.`DD_INC_MM_CLC_BLC = 10`;
- `ANA_EDU_FIN_CLI`.`TS_ATL_TRAN = 2026-08-13 15:00:00`;
- `PERIODOS = 2`.

O ciclo aberto comeca em 10/08/2026 e termina em 09/09/2026, portanto fica fora da analise. Os dois ciclos fechados cobrem 10/06/2026 a 09/08/2026. O resultado e:

- `ANA_EDU_FIN_CLI`.`DT_REF_INI = 2026-06-10`;
- `ANA_EDU_FIN_CLI`.`DT_REF_FIM = 2026-08-09`.

### `ANA_EDU_FIN_CLI`.`DT_MES_EXEA`

`ANA_EDU_FIN_CLI`.`DT_MES_EXEA` registra o mes de execucao do ETL como uma data no primeiro dia do mes. Se a execucao ocorrer em 13/08/2026, o atributo recebe `2026-08-01`.

### `ANA_EDU_FIN_CLI`.`DT_EXEA`

`ANA_EDU_FIN_CLI`.`DT_EXEA` registra a data em que o ETL foi executado. Ela e derivada automaticamente da data atual e nao depende da janela individual do cliente.

## 4. As transacoes atravessam a janela individual

### A leitura necessaria

Depois de conhecer todas as janelas individuais, o ETL encontra a menor `vw_janela_financeira`.`DT_REF_INI` e a maior `vw_janela_financeira`.`DT_REF_FIM`. Esses limites globais reduzem a leitura inicial no DB2. A consulta retorna somente:

- `DB2GFP.TRAN_RLZD_INST_PCT`.`NR_TRAN_INST_PCT`, identificador da transacao;
- `DB2GFP.TRAN_RLZD_INST_PCT`.`CD_CLI`, cliente da transacao;
- `DB2GFP.TRAN_RLZD_INST_PCT`.`DT_TRAN`, data usada no recorte financeiro;
- `DB2GFP.TRAN_RLZD_INST_PCT`.`VL_TRAN`, valor usado nas somas;
- `DB2GFP.TRAN_RLZD_INST_PCT`.`CD_NTZ_CTB_TRAN`, natureza contabil da transacao;
- `DB2GFP.TRAN_RLZD_INST_PCT`.`CD_CTGR_TRAN_OGNL`, categoria original usada na classificacao.

A leitura mantem apenas `DB2GFP.TRAN_RLZD_INST_PCT`.`CD_EST_TRAN_INST = 0` e clientes pertencentes ao mesmo publico efetivo dos 90 dias. No Spark, cada transacao ainda precisa respeitar a janela do proprio cliente: `DB2GFP.TRAN_RLZD_INST_PCT`.`DT_TRAN` deve estar entre `vw_janela_financeira`.`DT_REF_INI` e `vw_janela_financeira`.`DT_REF_FIM`.

### O dicionario transforma categoria em significado

O dicionario incorporado ao notebook relaciona a categoria e a natureza da transacao. O encontro exige simultaneamente:

- `DB2GFP.TRAN_RLZD_INST_PCT`.`CD_CTGR_TRAN_OGNL` igual a `vw_mapa_classificacao_categoria`.`CD_CATEGORIA`;
- `DB2GFP.TRAN_RLZD_INST_PCT`.`CD_NTZ_CTB_TRAN` igual a `vw_mapa_classificacao_categoria`.`TIPO`.

Quando ha correspondencia, a transacao recebe `vw_base_transacoes`.`CD_CLASSIFICACAO_CATEGORIA`, `vw_base_transacoes`.`NM_CLASSIFICACAO_CATEGORIA` e `vw_base_transacoes`.`FL_AGRO_CATEGORIA`.

Quando nao ha correspondencia, o caminho feliz e preservado por fallbacks:

| Natureza | Classificacao aplicada | Marca agro |
|---|---|---|
| `C` | Codigo `0`, Outras Entradas | `N` |
| `D` | Codigo `5`, Indeterminado | `N` |
| Outra natureza | Codigo e texto `NULL` | `N` |

Exemplo: uma transacao de debito com categoria original nao encontrada no mapa recebe `vw_base_transacoes`.`CD_CLASSIFICACAO_CATEGORIA = 5`, `vw_base_transacoes`.`NM_CLASSIFICACAO_CATEGORIA = 'Indeterminado'` e `vw_base_transacoes`.`FL_AGRO_CATEGORIA = 'N'`.

## 5. O movimento vira resumo tecnico

Os cinco atributos deste bloco observam a natureza contabil, sem depender do nome da classificacao financeira.

### `ANA_EDU_FIN_CLI`.`QT_TRANS_TOTAL`

Conta todas as transacoes do cliente que passaram pelo filtro da janela individual. Quando nenhuma transacao e encontrada, recebe `0`.

### `ANA_EDU_FIN_CLI`.`QT_TRANS_ENT` e `ANA_EDU_FIN_CLI`.`QT_TRANS_SAI`

`ANA_EDU_FIN_CLI`.`QT_TRANS_ENT` conta as transacoes em que `DB2GFP.TRAN_RLZD_INST_PCT`.`CD_NTZ_CTB_TRAN = 'C'`. `ANA_EDU_FIN_CLI`.`QT_TRANS_SAI` faz a mesma contagem para natureza `D`. Ambos recebem `0` sem movimento.

### `ANA_EDU_FIN_CLI`.`VL_TRANS_ENT` e `ANA_EDU_FIN_CLI`.`VL_TRANS_SAI`

`ANA_EDU_FIN_CLI`.`VL_TRANS_ENT` soma `DB2GFP.TRAN_RLZD_INST_PCT`.`VL_TRAN` das naturezas `C`. `ANA_EDU_FIN_CLI`.`VL_TRANS_SAI` soma o mesmo atributo para as naturezas `D`. Valores nulos de transacao contribuem com zero, e os dois totais recebem `0` quando o cliente nao possui movimento na janela.

Esses valores formam o resumo tecnico por natureza. Os proximos blocos reorganizam os mesmos movimentos pelo significado atribuido pelo dicionario.

## 6. As entradas ganham classificacao

Cada valor de entrada soma `DB2GFP.TRAN_RLZD_INST_PCT`.`VL_TRAN` quando `vw_base_transacoes`.`CD_CLASSIFICACAO_CATEGORIA` possui o codigo correspondente.

| Atributo final | Codigo | Significado do valor acumulado |
|---|---:|---|
| `ANA_EDU_FIN_CLI`.`VL_ENT_OUT` | `0` | Recebimentos sem origem identificada ou fora das demais classificacoes. Inclui o fallback de transacoes de natureza `C`. |
| `ANA_EDU_FIN_CLI`.`VL_ENT_REN` | `1` | Renda, remuneracao ou beneficios. |
| `ANA_EDU_FIN_CLI`.`VL_ENT_EST` | `2` | Devolucoes por correcoes, cancelamentos ou ajustes. |
| `ANA_EDU_FIN_CLI`.`VL_ENT_RESG` | `3` | Recursos recuperados de investimentos ou aplicacoes. |
| `ANA_EDU_FIN_CLI`.`VL_ENT_CRED` | `4` | Recursos obtidos por emprestimos, financiamentos ou outras operacoes de credito. |

Todos esses atributos recebem `0` quando nao ha valor classificado para a categoria.

### `ANA_EDU_FIN_CLI`.`VL_ENT_TOTAL`

`ANA_EDU_FIN_CLI`.`VL_ENT_TOTAL` fecha o bloco somando:

```text
VL_ENT_REN + VL_ENT_EST + VL_ENT_RESG + VL_ENT_OUT + VL_ENT_CRED
```

Esse total e o denominador unico dos percentuais de saida e participa do resultado orcamentario.

## 7. As saidas ganham classificacao

Cada valor de saida soma `DB2GFP.TRAN_RLZD_INST_PCT`.`VL_TRAN` quando `vw_base_transacoes`.`CD_CLASSIFICACAO_CATEGORIA` possui o codigo correspondente.

| Atributo final | Codigo | Significado do valor acumulado |
|---|---:|---|
| `ANA_EDU_FIN_CLI`.`VL_SAI_IND` | `5` | Saidas sem destino identificado ou fora das demais classificacoes. Inclui o fallback de transacoes de natureza `D`. |
| `ANA_EDU_FIN_CLI`.`VL_SAI_ESS` | `6` | Gastos necessarios para a manutencao da vida e do dia a dia. |
| `ANA_EDU_FIN_CLI`.`VL_SAI_FLEX` | `7` | Escolhas pessoais, lazer e estilo de vida. |
| `ANA_EDU_FIN_CLI`.`VL_SAI_FUT` | `8` | Formacao de patrimonio, reserva ou objetivos futuros. |
| `ANA_EDU_FIN_CLI`.`VL_SAI_OBR` | `9` | Dividas, parcelas e compromissos financeiros. |

Todos esses atributos recebem `0` quando nao ha valor classificado para a categoria.

### `ANA_EDU_FIN_CLI`.`VL_SAI_TOTAL`

`ANA_EDU_FIN_CLI`.`VL_SAI_TOTAL` fecha o bloco somando:

```text
VL_SAI_IND + VL_SAI_ESS + VL_SAI_FLEX + VL_SAI_FUT + VL_SAI_OBR
```

Esse total participa do percentual geral de saidas e do resultado orcamentario.

## 8. Os valores formam os indicadores de orcamento

### `ANA_EDU_FIN_CLI`.`VL_RES_ORC`

Quando o cliente possui transacoes na janela, `ANA_EDU_FIN_CLI`.`VL_RES_ORC` e calculado por:

```text
VL_ENT_TOTAL - VL_SAI_TOTAL
```

Um resultado positivo indica sobra de recursos; um resultado negativo indica que as saidas superaram as entradas. Sem transacoes, o atributo recebe `NULL`.

### `ANA_EDU_FIN_CLI`.`PC_SAI_ENT`

`ANA_EDU_FIN_CLI`.`PC_SAI_ENT` mede o peso de todas as saidas sobre todas as entradas:

```text
VL_SAI_TOTAL / VL_ENT_TOTAL
```

A divisao usa protecao contra denominador zero. Quando `ANA_EDU_FIN_CLI`.`VL_ENT_TOTAL` e zero, `ANA_EDU_FIN_CLI`.`PC_SAI_ENT` recebe `0`. O atributo tambem recebe `0` para clientes sem transacoes.

### `ANA_EDU_FIN_CLI`.`CD_FAIXA_ORC`

Quando existem transacoes, `ANA_EDU_FIN_CLI`.`PC_SAI_ENT` e transformado em uma faixa unica que alimenta os demais atributos orcamentarios:

| Codigo | Intervalo de `ANA_EDU_FIN_CLI`.`PC_SAI_ENT` | Leitura |
|---:|---|---|
| `0` | De `0.950000` a `1.050000`, inclusive | Neutro |
| `1` | Maior que `1.050000` e menor ou igual a `1.250000` | Deficitario Moderado |
| `2` | Maior que `1.250000` | Deficitario Acentuado |
| `3` | Maior ou igual a `0.750000` e menor que `0.950000` | Superavitario Moderado |
| `4` | Menor que `0.750000` | Superavitario Acentuado |

Sem transacoes, `ANA_EDU_FIN_CLI`.`CD_FAIXA_ORC` recebe `NULL`. Se houver transacoes, mas `ANA_EDU_FIN_CLI`.`VL_ENT_TOTAL` for zero, o percentual protegido sera zero e a faixa resultante sera `4`.

### `ANA_EDU_FIN_CLI`.`CD_RES_ORC` e `ANA_EDU_FIN_CLI`.`TX_RES_ORC`

Esses atributos resumem a faixa em tres resultados:

| `ANA_EDU_FIN_CLI`.`CD_RES_ORC` | `ANA_EDU_FIN_CLI`.`TX_RES_ORC` | Faixas de origem |
|---:|---|---|
| `0` | Neutro | `0` |
| `1` | Superavitario | `3` ou `4` |
| `2` | Deficitario | `1` ou `2` |

Os dois recebem `NULL` sem transacoes.

### `ANA_EDU_FIN_CLI`.`TX_STS_RES`

`ANA_EDU_FIN_CLI`.`TX_STS_RES` informa a intensidade do resultado. As faixas `2` e `4` recebem `Acentuado`; as faixas `1` e `3` recebem `Moderado`. A faixa neutra nao possui intensidade, por isso recebe `NULL`. O atributo tambem recebe `NULL` sem transacoes.

### `ANA_EDU_FIN_CLI`.`TX_STS_FINAL`

`ANA_EDU_FIN_CLI`.`TX_STS_FINAL` entrega a leitura completa do orcamento:

- faixa `0`: `Neutro`;
- faixa `1`: `Deficitario Moderado`;
- faixa `2`: `Deficitario Acentuado`;
- faixa `3`: `Superavitario Moderado`;
- faixa `4`: `Superavitario Acentuado`.

Sem transacoes, recebe `NULL`.

## 9. Cada saida e comparada com a entrada

Os cinco percentuais usam exclusivamente `ANA_EDU_FIN_CLI`.`VL_ENT_TOTAL` como denominador. Quando esse valor e zero, todos recebem `0`.

| Atributo final | Calculo |
|---|---|
| `ANA_EDU_FIN_CLI`.`PC_SAI_IND` | `ANA_EDU_FIN_CLI`.`VL_SAI_IND` / `ANA_EDU_FIN_CLI`.`VL_ENT_TOTAL` |
| `ANA_EDU_FIN_CLI`.`PC_SAI_ESS` | `ANA_EDU_FIN_CLI`.`VL_SAI_ESS` / `ANA_EDU_FIN_CLI`.`VL_ENT_TOTAL` |
| `ANA_EDU_FIN_CLI`.`PC_SAI_FLEX` | `ANA_EDU_FIN_CLI`.`VL_SAI_FLEX` / `ANA_EDU_FIN_CLI`.`VL_ENT_TOTAL` |
| `ANA_EDU_FIN_CLI`.`PC_SAI_FUT` | `ANA_EDU_FIN_CLI`.`VL_SAI_FUT` / `ANA_EDU_FIN_CLI`.`VL_ENT_TOTAL` |
| `ANA_EDU_FIN_CLI`.`PC_SAI_OBR` | `ANA_EDU_FIN_CLI`.`VL_SAI_OBR` / `ANA_EDU_FIN_CLI`.`VL_ENT_TOTAL` |

Como os cinco numeradores formam `ANA_EDU_FIN_CLI`.`VL_SAI_TOTAL`, a soma desses percentuais corresponde conceitualmente a `ANA_EDU_FIN_CLI`.`PC_SAI_ENT`. Os campos sao persistidos com seis casas decimais, portanto uma diferenca residual de arredondamento pode aparecer na soma materializada.

## 10. Os percentuais recebem referencias

As referencias sao parametros fixos adicionados a todas as linhas. Elas nao sao calculadas a partir do comportamento individual do cliente.

| Atributo final | Valor | Comparacao que alimenta |
|---|---:|---|
| `ANA_EDU_FIN_CLI`.`PC_REF_IND` | `0.750000` | Concentracao de saidas indeterminadas. |
| `ANA_EDU_FIN_CLI`.`PC_REF_ESS` | `0.500000` | Concentracao de gastos essenciais. |
| `ANA_EDU_FIN_CLI`.`PC_REF_FLEX` | `0.300000` | Concentracao de gastos flexiveis. |
| `ANA_EDU_FIN_CLI`.`PC_REF_FUT` | `0.200000` | Participacao de recursos destinados ao futuro. |
| `ANA_EDU_FIN_CLI`.`PC_REF_OBR` | `0.300000` | Concentracao de obrigacoes. |

Mesmo um cliente sem transacoes recebe os cinco valores de referencia. O que fica suspenso nesse caso e a pontuacao.

## 11. O perfil financeiro entra como uma segunda historia

O perfil nao depende das transacoes da janela. Para cada cliente, o ETL procura registros em `sbx_t2i2016.DVS_GRDR_FNCO_PF` e seleciona apenas o mais recente por `sbx_t2i2016.DVS_GRDR_FNCO_PF`.`DT_REF`. Em caso de empate, os codigos de macroperfil e microperfil em ordem decrescente completam a ordenacao.

Se o cliente nao tiver perfil na fonte, os cinco atributos deste bloco recebem `NULL`.

### `ANA_EDU_FIN_CLI`.`CD_MAC_PRFL_CLI` e `ANA_EDU_FIN_CLI`.`NM_MAC_PRFL_CLI`

`ANA_EDU_FIN_CLI`.`CD_MAC_PRFL_CLI` preserva `sbx_t2i2016.DVS_GRDR_FNCO_PF`.`CD_MAC_PRFL_CLI`. `ANA_EDU_FIN_CLI`.`NM_MAC_PRFL_CLI` traduz o codigo:

| Codigo | Nome |
|---:|---|
| `1` | Endividado |
| `2` | Equilibrista |
| `3` | Investidor |

Codigo nulo produz nome nulo. Codigo preenchido e fora do dominio conhecido e preservado em `ANA_EDU_FIN_CLI`.`CD_MAC_PRFL_CLI`, enquanto `ANA_EDU_FIN_CLI`.`NM_MAC_PRFL_CLI` recebe `CODIGO NAO MAPEADO`.

### `ANA_EDU_FIN_CLI`.`CD_MIC_PRFL_CLI` e `ANA_EDU_FIN_CLI`.`NM_MIC_PRFL_CLI`

`ANA_EDU_FIN_CLI`.`CD_MIC_PRFL_CLI` preserva `sbx_t2i2016.DVS_GRDR_FNCO_PF`.`CD_MIC_PRFL_CLI`. `ANA_EDU_FIN_CLI`.`NM_MIC_PRFL_CLI` traduz o codigo:

| Codigo | Nome |
|---:|---|
| `1` | Inadimplente |
| `2` | Acrobata |
| `3` | Iminente |
| `4` | Consciente |
| `5` | Equilibrista |
| `6` | Acelerado |
| `7` | Precavido |
| `8` | Despreocupado |

Codigo nulo produz nome nulo. Codigo preenchido e fora do dominio conhecido e preservado em `ANA_EDU_FIN_CLI`.`CD_MIC_PRFL_CLI`, enquanto `ANA_EDU_FIN_CLI`.`NM_MIC_PRFL_CLI` recebe `CODIGO NAO MAPEADO`.

### `ANA_EDU_FIN_CLI`.`NM_PRFL_FIN`

Em geral, `ANA_EDU_FIN_CLI`.`NM_PRFL_FIN` concatena `ANA_EDU_FIN_CLI`.`NM_MAC_PRFL_CLI` e `ANA_EDU_FIN_CLI`.`NM_MIC_PRFL_CLI`. A combinacao de macroperfil Equilibrista com microperfil Equilibrista e simplificada para `Equilibrista`.

Se algum nome for nulo, o resultado e `NULL`. Se algum nome receber `CODIGO NAO MAPEADO`, o resultado tambem sera `CODIGO NAO MAPEADO`. Esse atributo alimenta as pontuacoes por perfil.

## 12. A concentracao gera a primeira pontuacao

As pontuacoes de concentracao comparam cada `ANA_EDU_FIN_CLI`.`PC_SAI_*` com seu `ANA_EDU_FIN_CLI`.`PC_REF_*`. Sem transacoes, todas recebem `NULL`. Quando existem transacoes, mas `ANA_EDU_FIN_CLI`.`VL_ENT_TOTAL` e zero, todas recebem `0` antes da aplicacao das faixas.

| Atributo final | Regra com base valida |
|---|---|
| `ANA_EDU_FIN_CLI`.`NR_PONT_CONC_IND` | `99` quando `ANA_EDU_FIN_CLI`.`PC_SAI_IND` supera `ANA_EDU_FIN_CLI`.`PC_REF_IND`; caso contrario, `0`. |
| `ANA_EDU_FIN_CLI`.`NR_PONT_CONC_ESS` | `0` abaixo da referencia; `1` da referencia ate antes de 1,5 vez a referencia; `2` a partir de 1,5 vez. |
| `ANA_EDU_FIN_CLI`.`NR_PONT_CONC_FLEX` | `0` abaixo da referencia; `1` da referencia ate antes de 1,5 vez a referencia; `2` a partir de 1,5 vez. |
| `ANA_EDU_FIN_CLI`.`NR_PONT_CONC_FUT` | `2` abaixo da referencia; `1` da referencia ate antes de 1,5 vez a referencia; `0` a partir de 1,5 vez. |
| `ANA_EDU_FIN_CLI`.`NR_PONT_CONC_OBR` | `0` abaixo da referencia; `1` da referencia ate antes de 1,5 vez a referencia; `2` a partir de 1,5 vez. |

A inversao em `ANA_EDU_FIN_CLI`.`NR_PONT_CONC_FUT` e intencional: uma participacao maior de recursos destinados ao futuro reduz essa pontuacao.

## 13. O orcamento gera a segunda pontuacao

As pontuacoes orcamentarias usam `ANA_EDU_FIN_CLI`.`CD_FAIXA_ORC`. Sem transacoes ou sem faixa calculada, as pontuacoes aplicaveis recebem `NULL`.

### `ANA_EDU_FIN_CLI`.`NR_PONT_ORC_IND`

A classificacao Indeterminado nao utiliza o resultado orcamentario. Com transacoes, `ANA_EDU_FIN_CLI`.`NR_PONT_ORC_IND` recebe `0`; sem transacoes, recebe `NULL`.

### `ANA_EDU_FIN_CLI`.`NR_PONT_ORC_ESS`, `ANA_EDU_FIN_CLI`.`NR_PONT_ORC_FLEX` e `ANA_EDU_FIN_CLI`.`NR_PONT_ORC_OBR`

Esses tres atributos seguem a mesma regra:

| `ANA_EDU_FIN_CLI`.`CD_FAIXA_ORC` | Pontuacao |
|---:|---:|
| `2`, Deficitario Acentuado | `2` |
| `0` ou `1`, Neutro ou Deficitario Moderado | `1` |
| `3` ou `4`, Superavitario | `0` |

### `ANA_EDU_FIN_CLI`.`NR_PONT_ORC_FUT`

`ANA_EDU_FIN_CLI`.`NR_PONT_ORC_FUT` valoriza o superavit mais acentuado:

| `ANA_EDU_FIN_CLI`.`CD_FAIXA_ORC` | Pontuacao |
|---:|---:|
| `4`, Superavitario Acentuado | `2` |
| `0` ou `3`, Neutro ou Superavitario Moderado | `1` |
| `1` ou `2`, Deficitario | `0` |

## 14. O perfil gera a terceira pontuacao

Sem transacoes, todas as pontuacoes por perfil recebem `NULL`. Para Essenciais, Flexiveis, Futuro e Obrigacoes, um `ANA_EDU_FIN_CLI`.`NM_PRFL_FIN` nulo ou igual a `CODIGO NAO MAPEADO` tambem produz `NULL`.

### `ANA_EDU_FIN_CLI`.`NR_PONT_PRFL_IND`

Indeterminado nao utiliza perfil financeiro. Com transacoes, `ANA_EDU_FIN_CLI`.`NR_PONT_PRFL_IND` recebe `0`, mesmo que o perfil esteja ausente; sem transacoes, recebe `NULL`.

### `ANA_EDU_FIN_CLI`.`NR_PONT_PRFL_ESS`

| `ANA_EDU_FIN_CLI`.`NM_PRFL_FIN` | Pontuacao |
|---|---:|
| Endividado Acrobata | `2` |
| Endividado Inadimplente | `1` |
| Equilibrista | `1` |
| Investidor Precavido, Investidor Despreocupado ou Investidor Acelerado | `1` |
| Demais perfis reconhecidos | `0` |

### `ANA_EDU_FIN_CLI`.`NR_PONT_PRFL_FLEX`

| `ANA_EDU_FIN_CLI`.`NM_PRFL_FIN` | Pontuacao |
|---|---:|
| Endividado Consciente | `2` |
| Endividado Iminente | `1` |
| Demais perfis reconhecidos | `0` |

### `ANA_EDU_FIN_CLI`.`NR_PONT_PRFL_FUT`

| `ANA_EDU_FIN_CLI`.`NM_PRFL_FIN` | Pontuacao |
|---|---:|
| Endividado Consciente | `1` |
| Equilibrista | `2` |
| Investidor Precavido, Investidor Despreocupado ou Investidor Acelerado | `2` |
| Demais perfis reconhecidos | `0` |

### `ANA_EDU_FIN_CLI`.`NR_PONT_PRFL_OBR`

| `ANA_EDU_FIN_CLI`.`NM_PRFL_FIN` | Pontuacao |
|---|---:|
| Endividado Acrobata | `1` |
| Endividado Iminente ou Endividado Inadimplente | `2` |
| Demais perfis reconhecidos | `0` |

## 15. As tres leituras formam a pontuacao final

### `ANA_EDU_FIN_CLI`.`NR_PONT_IND_FIM`

`ANA_EDU_FIN_CLI`.`NR_PONT_IND_FIM` recebe diretamente `ANA_EDU_FIN_CLI`.`NR_PONT_CONC_IND`. As pontuacoes orcamentaria e de perfil de Indeterminado nao entram nessa consolidacao.

### `ANA_EDU_FIN_CLI`.`NR_PONT_ESS_FIM`

Soma `ANA_EDU_FIN_CLI`.`NR_PONT_CONC_ESS`, `ANA_EDU_FIN_CLI`.`NR_PONT_ORC_ESS` e `ANA_EDU_FIN_CLI`.`NR_PONT_PRFL_ESS`.

### `ANA_EDU_FIN_CLI`.`NR_PONT_FLEX_FIM`

Soma `ANA_EDU_FIN_CLI`.`NR_PONT_CONC_FLEX`, `ANA_EDU_FIN_CLI`.`NR_PONT_ORC_FLEX` e `ANA_EDU_FIN_CLI`.`NR_PONT_PRFL_FLEX`.

### `ANA_EDU_FIN_CLI`.`NR_PONT_FUT_FIM`

Soma `ANA_EDU_FIN_CLI`.`NR_PONT_CONC_FUT`, `ANA_EDU_FIN_CLI`.`NR_PONT_ORC_FUT` e `ANA_EDU_FIN_CLI`.`NR_PONT_PRFL_FUT`.

### `ANA_EDU_FIN_CLI`.`NR_PONT_OBR_FIM`

Soma `ANA_EDU_FIN_CLI`.`NR_PONT_CONC_OBR`, `ANA_EDU_FIN_CLI`.`NR_PONT_ORC_OBR` e `ANA_EDU_FIN_CLI`.`NR_PONT_PRFL_OBR`.

Nas quatro somas, a ausencia de qualquer componente produz uma pontuacao final `NULL`. Sem transacoes, as cinco pontuacoes finais ficam `NULL`.

## 16. A maior pontuacao define o conceito vencedor

O vencedor so e calculado quando as cinco pontuacoes finais estao preenchidas. Primeiro o ETL encontra o maior valor. Depois conta quantas classificacoes atingiram exatamente esse valor.

### `ANA_EDU_FIN_CLI`.`CD_TEMA_VENCEDOR` e `ANA_EDU_FIN_CLI`.`TX_TEMA_VENCEDOR`

| Pontuacao que atingiu sozinha o maior valor | Codigo | Texto persistido |
|---|---:|---|
| `ANA_EDU_FIN_CLI`.`NR_PONT_IND_FIM` | `1` | Categorizacao dos Gastos |
| `ANA_EDU_FIN_CLI`.`NR_PONT_ESS_FIM` | `2` | Gestao de Orcamento |
| `ANA_EDU_FIN_CLI`.`NR_PONT_FLEX_FIM` | `3` | Consumo Planejado |
| `ANA_EDU_FIN_CLI`.`NR_PONT_FUT_FIM` | `4` | Formacao de Reserva |
| `ANA_EDU_FIN_CLI`.`NR_PONT_OBR_FIM` | `5` | Uso Consciente do Credito |

Se duas ou mais pontuacoes compartilham o maior valor, `ANA_EDU_FIN_CLI`.`CD_TEMA_VENCEDOR` recebe `9` e `ANA_EDU_FIN_CLI`.`TX_TEMA_VENCEDOR` recebe `Empate`. Isso inclui o caso em que as cinco pontuacoes finais sao iguais a zero. O codigo `0` nao e produzido.

Exemplo: pontuacoes finais `2, 4, 4, 1, 3` possuem maximo `4` em duas classificacoes. O resultado e codigo `9` e texto `Empate`.

Se alguma pontuacao final estiver `NULL`, os dois atributos de vencedor tambem recebem `NULL`.

## 17. As flags encerram a linha

### `ANA_EDU_FIN_CLI`.`FL_TEM_MOV_AGRO`

O mapa incorporado marca cada categoria com `vw_mapa_classificacao_categoria`.`IN_AGRO`. `ANA_EDU_FIN_CLI`.`FL_TEM_MOV_AGRO` recebe `S` quando ao menos uma transacao de natureza `C` ou `D` possui `vw_base_transacoes`.`FL_AGRO_CATEGORIA = 'S'`.

Sem categoria agro, sem correspondencia no mapa ou sem transacoes na janela, recebe `N`. Portanto, `N` significa que o fluxo nao encontrou movimentacao agro classificada na janela analisada; nao e um valor nulo ou pendente.

### `ANA_EDU_FIN_CLI`.`FL_PARTICIPA_RADAR`

`ANA_EDU_FIN_CLI`.`FL_PARTICIPA_RADAR` esta reservado para uma regra futura. Nesta versao, recebe `NULL` para todos os clientes, independentemente de perfil, pontuacao, vencedor, movimento agro ou diagnostico do ciclo.

## 18. O caminho do cliente sem transacoes fechadas

Um cliente pode entrar no publico por possuir atualizacao transacional no recorte de 90 dias e, ainda assim, nao ter movimento entre sua `ANA_EDU_FIN_CLI`.`DT_REF_INI` e sua `ANA_EDU_FIN_CLI`.`DT_REF_FIM`. A tabela parte da janela financeira e associa as agregacoes por `LEFT JOIN`, preservando esse cliente.

Nesse caminho:

- `ANA_EDU_FIN_CLI`.`CD_CLI`, `ANA_EDU_FIN_CLI`.`TS_ATL_TRAN`, `ANA_EDU_FIN_CLI`.`DD_INC_MM_CLC_BLC`, `ANA_EDU_FIN_CLI`.`DT_REF_INI` e `ANA_EDU_FIN_CLI`.`DT_REF_FIM` permanecem preenchidos;
- os cinco atributos de perfil podem estar preenchidos ou nulos, pois dependem de uma fonte independente;
- quantidades, valores de entrada, valores de saida e percentuais recebem `0`;
- os cinco `ANA_EDU_FIN_CLI`.`PC_REF_*` permanecem preenchidos com os parametros fixos;
- resultado orcamentario, faixa, textos de resultado, pontuacoes e vencedor recebem `NULL`;
- `ANA_EDU_FIN_CLI`.`FL_TEM_MOV_AGRO` recebe `N`;
- `ANA_EDU_FIN_CLI`.`FL_PARTICIPA_RADAR` recebe `NULL`.

Assim, ausencia de movimento nos ciclos fechados nao elimina o cliente nem inventa uma avaliacao financeira sem base transacional.

## 19. Indice das 71 colunas finais

O indice abaixo apresenta a ordem fisica usada na criacao e na carga de `ANA_EDU_FIN_CLI`.

### Bloco 1: Dados do cliente, 9 colunas

1. `ANA_EDU_FIN_CLI`.`CD_CLI`
2. `ANA_EDU_FIN_CLI`.`TS_ATL_TRAN`
3. `ANA_EDU_FIN_CLI`.`DD_INC_MM_CLC_BLC`
4. `ANA_EDU_FIN_CLI`.`VL_REN_PRES`
5. `ANA_EDU_FIN_CLI`.`CD_MAC_PRFL_CLI`
6. `ANA_EDU_FIN_CLI`.`NM_MAC_PRFL_CLI`
7. `ANA_EDU_FIN_CLI`.`CD_MIC_PRFL_CLI`
8. `ANA_EDU_FIN_CLI`.`NM_MIC_PRFL_CLI`
9. `ANA_EDU_FIN_CLI`.`NM_PRFL_FIN`

### Bloco 2: Periodo da analise, 4 colunas

1. `ANA_EDU_FIN_CLI`.`DT_REF_INI`
2. `ANA_EDU_FIN_CLI`.`DT_REF_FIM`
3. `ANA_EDU_FIN_CLI`.`DT_MES_EXEA`
4. `ANA_EDU_FIN_CLI`.`DT_EXEA`

### Bloco 3: Resumo tecnico, 5 colunas

1. `ANA_EDU_FIN_CLI`.`QT_TRANS_TOTAL`
2. `ANA_EDU_FIN_CLI`.`QT_TRANS_ENT`
3. `ANA_EDU_FIN_CLI`.`QT_TRANS_SAI`
4. `ANA_EDU_FIN_CLI`.`VL_TRANS_ENT`
5. `ANA_EDU_FIN_CLI`.`VL_TRANS_SAI`

### Bloco 4: Valores de entrada, 6 colunas

1. `ANA_EDU_FIN_CLI`.`VL_ENT_REN`
2. `ANA_EDU_FIN_CLI`.`VL_ENT_EST`
3. `ANA_EDU_FIN_CLI`.`VL_ENT_RESG`
4. `ANA_EDU_FIN_CLI`.`VL_ENT_OUT`
5. `ANA_EDU_FIN_CLI`.`VL_ENT_CRED`
6. `ANA_EDU_FIN_CLI`.`VL_ENT_TOTAL`

### Bloco 5: Valores de saida, 6 colunas

1. `ANA_EDU_FIN_CLI`.`VL_SAI_IND`
2. `ANA_EDU_FIN_CLI`.`VL_SAI_ESS`
3. `ANA_EDU_FIN_CLI`.`VL_SAI_FLEX`
4. `ANA_EDU_FIN_CLI`.`VL_SAI_FUT`
5. `ANA_EDU_FIN_CLI`.`VL_SAI_OBR`
6. `ANA_EDU_FIN_CLI`.`VL_SAI_TOTAL`

### Bloco 6: Indicadores de orcamento, 7 colunas

1. `ANA_EDU_FIN_CLI`.`VL_RES_ORC`
2. `ANA_EDU_FIN_CLI`.`PC_SAI_ENT`
3. `ANA_EDU_FIN_CLI`.`CD_RES_ORC`
4. `ANA_EDU_FIN_CLI`.`TX_RES_ORC`
5. `ANA_EDU_FIN_CLI`.`CD_FAIXA_ORC`
6. `ANA_EDU_FIN_CLI`.`TX_STS_RES`
7. `ANA_EDU_FIN_CLI`.`TX_STS_FINAL`

### Bloco 7: Saidas sobre entrada, 5 colunas

1. `ANA_EDU_FIN_CLI`.`PC_SAI_IND`
2. `ANA_EDU_FIN_CLI`.`PC_SAI_ESS`
3. `ANA_EDU_FIN_CLI`.`PC_SAI_FLEX`
4. `ANA_EDU_FIN_CLI`.`PC_SAI_FUT`
5. `ANA_EDU_FIN_CLI`.`PC_SAI_OBR`

### Bloco 8: Parametros de referencia, 5 colunas

1. `ANA_EDU_FIN_CLI`.`PC_REF_IND`
2. `ANA_EDU_FIN_CLI`.`PC_REF_ESS`
3. `ANA_EDU_FIN_CLI`.`PC_REF_FLEX`
4. `ANA_EDU_FIN_CLI`.`PC_REF_FUT`
5. `ANA_EDU_FIN_CLI`.`PC_REF_OBR`

### Bloco 9: Pontuacao por concentracao, 5 colunas

1. `ANA_EDU_FIN_CLI`.`NR_PONT_CONC_IND`
2. `ANA_EDU_FIN_CLI`.`NR_PONT_CONC_ESS`
3. `ANA_EDU_FIN_CLI`.`NR_PONT_CONC_FLEX`
4. `ANA_EDU_FIN_CLI`.`NR_PONT_CONC_FUT`
5. `ANA_EDU_FIN_CLI`.`NR_PONT_CONC_OBR`

### Bloco 10: Pontuacao orcamentaria, 5 colunas

1. `ANA_EDU_FIN_CLI`.`NR_PONT_ORC_IND`
2. `ANA_EDU_FIN_CLI`.`NR_PONT_ORC_ESS`
3. `ANA_EDU_FIN_CLI`.`NR_PONT_ORC_FLEX`
4. `ANA_EDU_FIN_CLI`.`NR_PONT_ORC_FUT`
5. `ANA_EDU_FIN_CLI`.`NR_PONT_ORC_OBR`

### Bloco 11: Pontuacao por perfil, 5 colunas

1. `ANA_EDU_FIN_CLI`.`NR_PONT_PRFL_IND`
2. `ANA_EDU_FIN_CLI`.`NR_PONT_PRFL_ESS`
3. `ANA_EDU_FIN_CLI`.`NR_PONT_PRFL_FLEX`
4. `ANA_EDU_FIN_CLI`.`NR_PONT_PRFL_FUT`
5. `ANA_EDU_FIN_CLI`.`NR_PONT_PRFL_OBR`

### Bloco 12: Pontuacao final e vencedor, 7 colunas

1. `ANA_EDU_FIN_CLI`.`NR_PONT_IND_FIM`
2. `ANA_EDU_FIN_CLI`.`NR_PONT_ESS_FIM`
3. `ANA_EDU_FIN_CLI`.`NR_PONT_FLEX_FIM`
4. `ANA_EDU_FIN_CLI`.`NR_PONT_FUT_FIM`
5. `ANA_EDU_FIN_CLI`.`NR_PONT_OBR_FIM`
6. `ANA_EDU_FIN_CLI`.`CD_TEMA_VENCEDOR`
7. `ANA_EDU_FIN_CLI`.`TX_TEMA_VENCEDOR`

### Bloco 13: Contexto e elegibilidade, 2 colunas

1. `ANA_EDU_FIN_CLI`.`FL_TEM_MOV_AGRO`
2. `ANA_EDU_FIN_CLI`.`FL_PARTICIPA_RADAR`

**Total: 71 colunas.**
