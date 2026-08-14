# Documentação do ETL — ANA_EDU_FIN_CLI V1

## Objetivo

Este documento descreve o fluxo técnico do notebook `v1_todos_ana_edu_fin_cli.ipynb`. O notebook forma o público-alvo, calcula a janela financeira individual, processa as transações dos ciclos fechados e carrega a tabela `ANA_EDU_FIN_CLI` com 71 colunas.

A definição oficial dos atributos, tipos, enums e regras de negócio permanece em [`v1_documentacao_oficial_ana_edu_fin_cli.md`](v1_documentacao_oficial_ana_edu_fin_cli.md).

## Entrada

O usuário informa somente:

```python
PERIODOS = 2
```

`PERIODOS` aceita números inteiros de `1` a `6` e representa a quantidade de ciclos financeiros fechados analisados. A data de execução é recebida automaticamente pela variável de ambiente `HOJE`.

## Fontes

| Origem | Uso |
|---|---|
| `DB2GFP.TRAN_RLZD_INST_PCT` | Público-alvo, identificação da conta e transações da janela financeira. |
| `DB2GFP.CT_GRDR_FNCO` | Dia inicial do cálculo do balanço. |
| `sbx_t2i2016.DVS_GRDR_FNCO_PF` | Macroperfil, microperfil e perfil financeiro. |
| `CATEGORIAS` | Dicionário incorporado de classificação das transações. |

## Fluxo

O processamento é incremental. Cada etapa possui uma responsabilidade, uma consulta nomeada quando aplicável e uma view para a etapa seguinte.

| Etapa | Responsabilidade | Consulta principal | Saída |
|---:|---|---|---|
| 1 | Criar as conexões Spark e DB2. | — | `spark`, `cliente_db2` |
| 2 | Definir `PERIODOS`, tabela e data de execução. | — | Configuração do processamento |
| 3 | Extrair o público e as contas observadas nos últimos 90 dias. | `query_publico_contas` | `vw_publico_contas` |
| 4 | Calcular `MAX(TS_ATL_TRAN)` por cliente e o dia do ciclo ou diagnóstico. | `query_publico_alvo`, `query_dia_ciclo` | `vw_publico_alvo`, `vw_dia_ciclo` |
| 5 | Calcular `DT_REF_INI` e `DT_REF_FIM` por cliente. | `query_janela_financeira` | `vw_janela_financeira` |
| 6 | Obter os limites globais para reduzir a extração DB2. | — | `dt_ref_ini_global`, `dt_ref_fim_global` |
| 7 | Buscar transações e aplicar a janela individual. | `query_transacoes_janela`, `query_transacoes_cliente` | `df_base_transacoes` |
| 8 | Classificar transações com o dicionário incorporado. | — | `vw_base_transacoes` |
| 9 | Obter o perfil financeiro mais recente. | `query_perfil_financeiro` | `vw_perfil_financeiro` |
| 10 | Reservar a renda presumida como dado pessoal nulo. | `query_renda_presumida` | `vw_renda_presumida` |
| 11 | Agregar quantidades, valores e movimentação agro. | `query_agregacoes` | `vw_agregacoes` |
| 12 | Preservar todos os clientes do público por `LEFT JOIN`. | `query_base_cliente` | `vw_base_cliente` |
| 13 | Calcular totais, percentuais e referências. | `query_percentuais` | `vw_percentuais` |
| 14 | Calcular resultado e faixa orçamentária. | `query_orcamento` | `vw_orcamento` |
| 15 | Calcular pontuação por concentração. | `query_pontuacao_concentracao` | `vw_pontuacao_concentracao` |
| 16 | Calcular pontuação orçamentária. | `query_pontuacao_orcamento` | `vw_pontuacao_orcamento` |
| 17 | Calcular pontuação por perfil. | `query_pontuacao_perfil` | `vw_pontuacao_perfil` |
| 18 | Consolidar as cinco pontuações finais. | `query_pontuacao_final` | `vw_pontuacao_final` |
| 19 | Identificar vencedor único ou empate. | `query_vencedor` | `vw_vencedor` |
| 20 | Organizar as 71 colunas na ordem física oficial. | `query_tabela_final` | `df_ana_edu_fin_cli` |
| 21 | Recriar a tabela quando solicitado. | `query_drop_tabela`, `ddl_tabela_spark` | Tabela Hive |
| 22 | Executar a carga integral. | — | `ANA_EDU_FIN_CLI` |

## Público-Alvo

O público contém clientes com `TS_ATL_TRAN` entre o início da data de execução menos 89 dias e o início do dia seguinte. Somente transações efetivadas, com `CD_EST_TRAN_INST = 0`, participam.

Para reduzir o volume transferido, `query_publico_contas` calcula no DB2 o maior timestamp de cada combinação de cliente e conta. No Spark, `query_publico_alvo` calcula novamente o máximo entre os grupos e produz uma linha por `CD_CLI`. A propriedade `MAX(MAX(grupo)) = MAX(cliente)` preserva exatamente o maior `TS_ATL_TRAN` do cliente dentro do recorte de 90 dias, sem leitura histórica adicional.

O processo é interrompido quando o público-alvo está vazio para evitar a sobrescrita da tabela sem registros.

## Leituras DB2

As consultas enviadas pelo Spark JDBC não usam `WITH`. O DB2 restringe público, período e estado, reduz o recorte inicial por cliente e conta e relaciona a conta ao dia do ciclo. Os diagnósticos e cálculos analíticos são feitos posteriormente no Spark.

- As tabelas são referenciadas com schema completo.
- As datas são validadas em formato ISO e representadas como `DATE('YYYY-MM-DD')`.
- A extração inicial é filtrada diretamente pelo recorte operacional; as transações da janela são limitadas ao mesmo público por `EXISTS`.
- Cada consulta retorna somente as colunas necessárias para a etapa.
- O JDBC usa provisoriamente apenas `fetchsize=10_000`, sem `partitionColumn`, bounds ou `numPartitions`.
- A coluna e os limites de particionamento serão definidos somente após diagnóstico de distribuição e capacidade do DB2.
- As duas extrações de `TRAN_RLZD_INST_PCT` são materializadas e registram quantidade de linhas e duração.
- Falhas preservam a exceção JDBC original, incluindo os detalhes disponibilizados pelo driver.

## Dia do Ciclo

`query_publico_contas` obtém a identificação da conta diretamente de `TRAN_RLZD_INST_PCT`. Uma conta é elegível quando `NR_MCA_PCT_OPB = 999999999`, `CD_PRD = 6`, `NR_AG_TITR` está preenchido e `CD_CT_TITR` está preenchido. A agência e a conta são relacionadas a `CT_GRDR_FNCO.CD_UOR_CC` e `CT_GRDR_FNCO.NR_CC` para obter `DD_INC_MM_CLC_BLC`.

No Spark, `query_dia_ciclo` normaliza agência e conta e elimina repetições da mesma combinação física antes de contar as contas do cliente. Várias transações da mesma conta representam uma única conta elegível.

| Valor | Significado |
|---:|---|
| `1` a `31` | Dia cadastrado para início do ciclo. |
| `996` | Mais de uma combinação distinta de agência e conta é elegível. |
| `997` | Nenhuma conta corrente BB elegível possui agência e conta identificáveis no recorte. |
| `999` | Exatamente uma conta elegível não possui dia localizado em `CT_GRDR_FNCO`. |

Os diagnósticos são preservados na tabela final. Para o cálculo interno da janela, valores fora de `1` a `31` usam dia `1`.

## Janela Financeira

O ciclo que contém `TS_ATL_TRAN` é considerado aberto e não entra na análise. A rotina seleciona os `PERIODOS` ciclos fechados imediatamente anteriores.

- `DT_REF_FIM`: dia anterior ao início do ciclo aberto.
- `DT_REF_INI`: início do ciclo localizado `PERIODOS` meses antes do ciclo aberto.
- Quando o dia do ciclo não existe em um mês, usa-se o último dia disponível.

Exemplo para dia `10`, `TS_ATL_TRAN = 2026-08-13` e `PERIODOS = 2`:

| Ciclo | Intervalo |
|---|---|
| Aberto, excluído | `2026-08-10` a `2026-09-09` |
| Fechado 1 | `2026-07-10` a `2026-08-09` |
| Fechado 2 | `2026-06-10` a `2026-07-09` |
| Janela persistida | `DT_REF_INI = 2026-06-10`, `DT_REF_FIM = 2026-08-09` |

## Transações e Classificação

A leitura transacional ocorre em duas etapas. No DB2, `query_transacoes_janela` usa o menor `DT_REF_INI` e o maior `DT_REF_FIM` do público como limites globais, restringe os registros aos clientes do público efetivo por `EXISTS` e aplica `CD_EST_TRAN_INST = 0`. Assim, lançamentos futuros (`1`) e exclusões lógicas (`9`) não são transferidos ao Spark.

A extração retorna somente `NR_TRAN_INST_PCT`, `CD_CLI`, `DT_TRAN`, `VL_TRAN`, `CD_NTZ_CTB_TRAN` e `CD_CTGR_TRAN_OGNL`. No Spark, `query_transacoes_cliente` relaciona cada registro a `vw_janela_financeira` por `CD_CLI` e mantém somente `DT_TRAN BETWEEN DT_REF_INI AND DT_REF_FIM` daquele cliente. Os limites globais reduzem a leitura DB2; a janela individual determina efetivamente quais transações entram nos cálculos.

### Aplicação do dicionário

O dicionário `CATEGORIAS` permanece incorporado ao notebook. Somente entradas com `TIPO` igual a `C` ou `D` formam `vw_mapa_classificacao_categoria`. O mapa é distribuído por broadcast e relacionado à transação pela combinação:

```text
CD_CTGR_TRAN_OGNL = CD_CATEGORIA
CD_NTZ_CTB_TRAN   = TIPO
```

Essa combinação impede que o mesmo código de categoria seja aplicado a uma natureza incompatível. A classificação produz `CD_CLASSIFICACAO_CATEGORIA`, `NM_CLASSIFICACAO_CATEGORIA` e a marca técnica `FL_AGRO_CATEGORIA`.

| Natureza | Códigos resultantes | Fallback sem correspondência |
|---|---|---|
| Entrada `C` | `0` Outras Entradas; `1` Renda; `2` Estorno; `3` Resgate; `4` Crédito | `0` e `Outras Entradas` |
| Saída `D` | `5` Indeterminado; `6` Essenciais; `7` Flexíveis; `8` Futuro; `9` Obrigações | `5` e `Indeterminado` |
| Outra natureza | Sem classificação consolidada | Código e texto `NULL` |

Quando não existe marca agro no mapa, `FL_AGRO_CATEGORIA` recebe `N`. Na agregação por cliente, `FL_TEM_MOV_AGRO` recebe `S` se houver pelo menos uma transação de natureza `C` ou `D` marcada como agro; nos demais casos recebe `N`.

As quantidades são contadas por cliente. Os valores técnicos usam a natureza contábil, enquanto os blocos de entrada e saída usam `CD_CLASSIFICACAO_CATEGORIA`. Em todas as somas, `VL_TRAN` nulo é tratado como `0`.

## Perfil Financeiro

O registro mais recente de `sbx_t2i2016.DVS_GRDR_FNCO_PF` preserva os códigos de macroperfil e microperfil. Código nulo produz nome nulo; código preenchido e fora do domínio conhecido permanece no respectivo `CD_*`, enquanto o nome recebe `CODIGO NAO MAPEADO`.

`NM_PRFL_FIN` fica nulo quando algum código estiver ausente, recebe `CODIGO NAO MAPEADO` quando algum código estiver fora do domínio e combina os dois nomes quando ambos forem conhecidos. As pontuações de perfil consideram apenas nomes finais conhecidos.

## Renda Presumida

`query_renda_presumida` parte de `vw_publico_alvo` e produz uma linha por `CD_CLI`, com `VL_REN_PRES` convertido para `DECIMAL(18,2)` e preenchido com `NULL`. `query_base_cliente` associa `vw_renda_presumida` por `LEFT JOIN`.

Essa etapa funciona como contrato para a futura integração. A origem e a regra de escolha ainda não foram definidas, e `VL_REN_PRES` não participa de percentuais, orçamento, pontuações ou vencedor. `DB2GFP.REN_INFD_CLI` não é usada automaticamente porque descreve renda informada pelo cliente, um conceito diferente.

## Clientes Sem Transações

O conjunto final parte de `vw_janela_financeira` e associa `vw_agregacoes` por `LEFT JOIN`. Por isso, todo cliente do público permanece no resultado mesmo quando não possui transação efetivada em seus ciclos fechados. A ausência de movimento não elimina a janela individual nem os dados disponíveis de perfil.

| Grupo de atributos | Comportamento quando `QT_TRANS_TOTAL = 0` |
|---|---|
| Identificação e janela | `CD_CLI`, `TS_ATL_TRAN`, `DD_INC_MM_CLC_BLC`, `DT_REF_INI` e `DT_REF_FIM` permanecem preenchidos conforme as etapas anteriores. |
| Perfil financeiro | Permanece preenchido quando encontrado na origem; caso contrário, conserva seus valores nulos ou não mapeados definidos na etapa de perfil. |
| Quantidades técnicas | `QT_TRANS_TOTAL`, `QT_TRANS_ENT` e `QT_TRANS_SAI` recebem `0`. |
| Valores técnicos e classificados | Todos os campos `VL_TRANS_*`, `VL_ENT_*` e `VL_SAI_*` recebem `0`. |
| Percentuais calculados | `PC_SAI_ENT` e os cinco `PC_SAI_*` recebem `0`, pois `VL_ENT_TOTAL = 0`. |
| Referências | Os cinco parâmetros fixos `PC_REF_*` continuam preenchidos. |
| Orçamento | `VL_RES_ORC`, `CD_RES_ORC`, `TX_RES_ORC`, `CD_FAIXA_ORC`, `TX_STS_RES` e `TX_STS_FINAL` recebem `NULL`. |
| Pontuações | Todos os campos de concentração, orçamento, perfil e pontuação final recebem `NULL`. |
| Vencedor | `CD_TEMA_VENCEDOR` e `TX_TEMA_VENCEDOR` recebem `NULL`. |
| Contexto agro | `FL_TEM_MOV_AGRO` recebe `N`, indicando que nenhuma movimentação agro foi identificada na janela. |
| Participação | `FL_PARTICIPA_RADAR` permanece `NULL`. |

Assim, zero representa ausência de quantidade ou valor, enquanto `NULL` representa indicador analítico não calculado por falta de base transacional.

## Vencedor e Participação

O vencedor é calculado somente quando `NR_PONT_IND_FIM`, `NR_PONT_ESS_FIM`, `NR_PONT_FLEX_FIM`, `NR_PONT_FUT_FIM` e `NR_PONT_OBR_FIM` estão preenchidos. Se qualquer uma das cinco pontuações for `NULL`, o máximo não é calculado e os dois campos de vencedor recebem `NULL`.

Com as cinco pontuações completas, a rotina encontra o maior valor e conta quantas classificações possuem exatamente esse máximo. Empates em valores inferiores ao máximo não interferem. Quando duas ou mais classificações compartilham o máximo, o resultado é `9 = Empate`; isso inclui empate entre dois, três, quatro ou cinco conceitos e também o caso em que as cinco pontuações são `0`.

| Código | Texto | Pontuação associada |
|---:|---|---|
| `1` | Categorização dos Gastos | `NR_PONT_IND_FIM` |
| `2` | Gestão de Orçamento | `NR_PONT_ESS_FIM` |
| `3` | Consumo Planejado | `NR_PONT_FLEX_FIM` |
| `4` | Formação de Reserva | `NR_PONT_FUT_FIM` |
| `5` | Uso Consciente do Crédito | `NR_PONT_OBR_FIM` |
| `9` | Empate | Duas ou mais pontuações iguais ao máximo |
| `NULL` | `NULL` | Pelo menos uma pontuação final ausente |

Exemplos:

| `IND` | `ESS` | `FLEX` | `FUT` | `OBR` | Resultado |
|---:|---:|---:|---:|---:|---|
| `2` | `6` | `3` | `4` | `1` | `2 = Gestão de Orçamento` |
| `2` | `6` | `6` | `4` | `1` | `9 = Empate` |
| `0` | `0` | `0` | `0` | `0` | `9 = Empate` |
| `2` | `NULL` | `3` | `4` | `1` | `NULL` |

O código `0` não é produzido. `FL_PARTICIPA_RADAR` permanece `NULL` para todos os clientes, independentemente do vencedor, do empate, do perfil, da movimentação agro ou dos diagnósticos do ciclo. A regra de participação será definida futuramente.

## Carga

A tabela é armazenada em Parquet com compressão Snappy. Quando `atualizar_metadado = True`, o notebook remove e recria a tabela antes da carga. A publicação é integral, usando `overwrite` e `insertInto`.

## Validações Atuais

Esta versão mantém somente:

- validação de `PERIODOS` entre `1` e `6`;
- validação da data automática de execução no formato ISO;
- proteção contra público-alvo vazio.

Demais inconsistências são deixadas aparecer naturalmente durante o processamento. Validações completas de qualidade e diagnóstico ficam para uma etapa futura.
