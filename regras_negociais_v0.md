# Radar Financeiro — Regras Negociais Consolidadas

## 1. Objetivo e contrato geral

O Radar Financeiro produz um diagnóstico financeiro individual a partir das movimentações recentes de um cliente pessoa física. O diagnóstico combina elegibilidade, conta corrente, ciclo financeiro, renda presumida, perfil financeiro e movimentações realizadas para:

- formar uma janela financeira de um a seis ciclos fechados;
- eliminar movimentações que se anulam por reconciliação;
- classificar entradas e saídas em temas financeiros;
- calcular orçamento, concentração de gastos e aderência ao perfil;
- identificar o tema de maior prioridade para o cliente;
- simular o diagnóstico com renda presumida ou entradas efetivamente realizadas.

O resultado oficial é publicado em `vw_radar_financeiro_cliente_mvp`.

### 1.1 Grão e cardinalidade

O grão do resultado é:

> uma linha por cliente selecionado e execução.

O contrato exige:

- exatamente uma linha;
- exatamente 80 atributos, na ordem definida na seção 14;
- `CD_CLI` igual ao cliente selecionado;
- preenchimento dos 12 atributos obrigatórios indicados no dicionário final.

O processamento é individual. Não existe resultado agregado de vários clientes na mesma linha.

### 1.2 Conceitos fundamentais

| Conceito | Definição |
|---|---|
| Cliente selecionado | Cliente identificado por `CD_CLI`, diretamente informado, localizado por CPF ou selecionado aleatoriamente entre os elegíveis. |
| Formação do público | Verificação de que o cliente possui transação realizada de pessoa física na janela de um mês-calendário anterior à execução. |
| Conta elegível | Único par de agência e conta associado ao cliente que atende aos códigos de pacote e produto definidos neste contrato. |
| Ciclo financeiro | Período delimitado pelo dia de fechamento da conta. |
| Janela financeira | Intervalo inclusivo entre `DT_REF_INI` e `DT_REF_FIM`, cobrindo de um a seis ciclos fechados. |
| Contexto de reconciliação | Cinco dias corridos antes e cinco dias corridos depois da janela financeira. |
| Movimento oficial bruto | Transação localizada dentro da janela financeira antes da reconciliação. |
| Movimento efetivo | Movimento oficial que não foi consumido por par exato nem por par de borda. |
| Classe Radar | Classificação temática de uma movimentação segundo categoria e natureza contábil. |
| Base financeira | Valor usado como denominador dos percentuais e como entrada total para o orçamento de um cenário. |
| Pontuação completa | Estado em que os cinco temas possuem pontuação final não nula. |
| Tema vencedor | Tema com a maior pontuação final; havendo mais de um máximo, o resultado é empate. |

### 1.3 Fluxo negocial

```text
Entradas e data de execução
  → seleção e elegibilidade do cliente
  → CPF e conta elegível
  → normalização da conta
  → ciclo e janela financeira
  → renda e perfil
  → movimentações no contexto de ±5 dias
  → reconciliação exata
  → reconciliação de borda
  → universo efetivo
  → classificação e filtro BRL
  → agregações e orçamento
  → percentuais e pontuações
  → vencedor
  → resultado oficial e cenários
```

## 2. Entradas, domínios e datas

### 2.1 Entradas

| Entrada | Domínio | Regra |
|---|---|---|
| `CD_CLI` | Inteiro representável em INT32 | Identificador principal do cliente. Tem prioridade sobre `CPF`. |
| `CPF` | Valor usado na seleção auxiliar | Usado somente quando `CD_CLI` é nulo. |
| `periodo` | Inteiro de 1 a 6 | Quantidade de ciclos financeiros fechados. |
| `HOJE` | Data ISO nos primeiros 10 caracteres | Origina `DATA_EXECUCAO`. |

Valores iniciais usuais:

| Entrada | Valor inicial |
|---|---|
| `CD_CLI` | `NULL` |
| `CPF` | `NULL` |
| `periodo` | `1` |

### 2.2 Prioridade para seleção do cliente

A seleção obedece estritamente à seguinte prioridade:

1. se `CD_CLI` estiver preenchido, o valor é usado e `CPF` é ignorado;
2. se `CD_CLI` for nulo e `CPF` estiver preenchido, localiza-se o `CD_CLI` da transação mais recente desse CPF;
3. se ambos forem nulos, seleciona-se aleatoriamente um `CD_CLI` elegível.

#### Seleção por CPF

A seleção por CPF lê `DB2GFP.TRAN_RLZD_INST_PCT` e exige:

- `NR_CPF_CNPJ_TITR = CPF`;
- `CD_EST_TRAN_INST = 0`;
- `CD_TIP_PSS = 1`;
- `DATA_INICIAL_PUBLICO <= TS_INCL_TRAN < DATA_FINAL_EXCLUSIVA_PUBLICO`.

Os resultados são ordenados por `TS_INCL_TRAN DESC` e somente a primeira linha é usada. Se nenhuma linha for encontrada, não há cliente para continuar o processamento.

O valor auxiliar `CPF` não passa por validação explícita de tipo, tamanho ou representação antes da consulta. Sua aceitação efetiva depende da fonte consultada.

#### Seleção aleatória

A seleção aleatória usa a mesma fonte, janela, estado e tipo de pessoa. Também exige `CD_CLI IS NOT NULL`, considera os clientes distintos e escolhe uma linha em ordem aleatória.

### 2.3 Validação de `CD_CLI`

Após a seleção, `CD_CLI`:

- não pode ser nulo;
- não pode ser booleano;
- deve possuir representação textual inteira exata conforme `[+-]?[0-9]+`;
- é convertido para inteiro;
- deve estar entre `-2147483648` e `2147483647`, inclusive.

Qualquer violação bloqueia o processamento antes das consultas do cliente.

### 2.4 Validação de `periodo`

`periodo`:

- deve ser do tipo inteiro;
- não aceita booleanos;
- deve estar no intervalo fechado `1..6`.

Assim, valores como `0`, `7`, `1.0`, `"1"` e `NULL` são inválidos.

### 2.5 Data de execução

`DATA_EXECUCAO` é a data ISO formada pelos primeiros 10 caracteres de `HOJE`:

```text
DATA_EXECUCAO = DATE(HOJE[1:10])
```

Uma data ausente ou inválida impede a formação das demais referências temporais.

### 2.6 Janela de formação do público

`DATA_INICIAL_PUBLICO` corresponde ao mesmo dia do mês-calendário anterior a `DATA_EXECUCAO`. Se o mês anterior não possuir esse dia, usa-se seu último dia.

```text
DATA_FINAL_EXCLUSIVA_PUBLICO = DATA_EXECUCAO
DATA_INICIAL_PUBLICO = DATA_EXECUCAO recuada em um mês-calendário
```

O intervalo é fechado no início e aberto no fim:

```text
DATA_INICIAL_PUBLICO <= TS_INCL_TRAN < DATA_FINAL_EXCLUSIVA_PUBLICO
```

`DT_MES_EXEA` é sempre o primeiro dia do mês de `DATA_EXECUCAO`.

## 3. Fontes e contratos de dados

### 3.1 Fontes físicas

| Fonte | Tecnologia lógica | Grão utilizado | Finalidade |
|---|---|---|---|
| `DB2GFP.TRAN_RLZD_INST_PCT` | DB2 | Uma linha por transação institucional | Seleção do cliente, formação do público, CPF, conta e movimentações. |
| `DB2GFP.CT_GRDR_FNCO` | DB2 | Registros de ciclo por agência e conta | Obter dia e referência do fechamento financeiro. |
| `DB2DFE.REN_AVLD_PF` | Hive/Spark SQL | Registros de renda avaliada por CPF | Obter renda presumida mais recente. |
| `DB2D1D.DVS_GRDR_FNCO_PF` | DB2 | Registros de perfil por cliente e data | Obter macroperfil e microperfil mais recentes. |

### 3.2 Consulta de formação do cliente

#### Atributos projetados

| Ordem | Atributo | Uso negocial |
|---:|---|---|
| 1 | `CD_CLI` | Identificação e agrupamento do cliente. |
| 2 | `TS_INCL_TRAN` | Elegibilidade temporal e timestamp de referência. |
| 3 | `NR_CPF_CNPJ_TITR` | Verificação de CPF único. |
| 4 | `NR_AG_TITR` | Agência da conta candidata. |
| 5 | `CD_CT_TITR` | Conta candidata. |
| 6 | `NR_MCA_PCT_OPB` | Critério do pacote operacional elegível. |
| 7 | `CD_PRD` | Critério do produto elegível. |

#### Atributos usados apenas em filtros

- `CD_EST_TRAN_INST`;
- `CD_TIP_PSS`.

#### Filtros

```text
CD_CLI = cliente selecionado
CD_EST_TRAN_INST = 0
CD_TIP_PSS = 1
DATA_INICIAL_PUBLICO <= TS_INCL_TRAN < DATA_FINAL_EXCLUSIVA_PUBLICO
```

Zero linhas significa cliente inelegível e bloqueia a execução.

### 3.3 Consulta de ciclo

| Ordem | Atributo | Tipo funcional | Uso |
|---:|---|---|---|
| 1 | `CD_UOR_CC` | `INT` | Agência normalizada. |
| 2 | `NR_CC` | `DECIMAL(11,0)` | Conta normalizada. |
| 3 | `DD_INC_MM_CLC_BLC` | `SMALLINT` | Dia de início do ciclo. |
| 4 | `TS_ULT_EXEA_PSQ` | `TIMESTAMP` | Referência para escolher o registro mais recente. |

Filtros:

```text
CD_UOR_CC = CD_UOR_CC_NORM
NR_CC = NR_CC_NORM
```

Sem conta normalizada, a fonte não é consultada e o conjunto de ciclo é considerado vazio.

### 3.4 Consulta de renda

| Ordem | Atributo físico | Atributo funcional | Tipo funcional |
|---:|---|---|---|
| 1 | `NR_CPF_BASE_SRF` | `NR_CPF` | `DECIMAL(11,0)` |
| 2 | `DT_INCL_REN_AVLD` | `DT_INCL_REN_AVLD` | `DATE` |
| 3 | `VL_REN` | `VL_REN` | `DECIMAL(17,2)` |

Filtro:

```text
NR_CPF_BASE_SRF = CD_CPF
```

A consulta ocorre somente quando `FL_CPF_UNICO = 'S'` e `CD_CPF` não é nulo. Não há corte da data de renda por `DATA_EXECUCAO`; portanto, a maior data disponível é elegível mesmo que seja posterior à execução.

### 3.5 Consulta de perfil

| Ordem | Atributo | Uso |
|---:|---|---|
| 1 | `CD_CLI` | Chave do cliente. |
| 2 | `DT_REF` | Corte temporal e seleção do registro mais recente. |
| 3 | `CD_MAC_PRFL_CLI` | Código do macroperfil usado na pontuação. |
| 4 | `NM_MAC_PRFL_CLI` | Nome informativo do macroperfil. |
| 5 | `CD_MIC_PRFL_CLI` | Código informativo do microperfil. |
| 6 | `NM_MIC_PRFL_CLI` | Nome informativo do microperfil. |

Filtros:

```text
CD_CLI = cliente selecionado
DT_REF <= DATA_EXECUCAO
```

### 3.6 Consulta de movimentações

#### Projeção física

| Ordem | Atributo | Participa do motor |
|---:|---|---|
| 1 | `NR_TRAN_INST_PCT` | Sim; identifica linhas durante a reconciliação. |
| 2 | `CD_CLI` | Sim. |
| 3 | `DT_TRAN` | Sim. |
| 4 | `CD_NTZ_CTB_TRAN` | Sim. |
| 5 | `CD_CTGR_TRAN_OGNL` | Sim. |
| 6 | `CD_TIP_MOE_CRR` | Sim. |
| 7 | `VL_TRAN` | Sim. |
| 8 | `TX_DCR_TRAN_OGNL` | Não; atributo explicativo. |
| 9 | `NR_MCA_PCT_OPB` | Não; atributo explicativo. |

`CD_EST_TRAN_INST` e `IN_VSLO_CSM` são lidos apenas para aplicar filtros.

#### Filtros na origem

```text
CD_CLI = cliente selecionado
CD_EST_TRAN_INST = 0
DT_REF_INI - 5 dias <= DT_TRAN <= DT_REF_FIM + 5 dias
CD_NTZ_CTB_TRAN = 'C'
OU
(CD_NTZ_CTB_TRAN = 'D' E IN_VSLO_CSM = 'S')
```

O filtro `IN_VSLO_CSM = 'S'` é exclusivo dos débitos. Não são aplicados na origem filtros de pessoa física, pacote, produto, categoria, moeda ou valor.

#### Schema funcional rígido

O motor consome exatamente:

| Ordem | Atributo | Tipo |
|---:|---|---|
| 1 | `NR_TRAN_INST_PCT` | `BIGINT` |
| 2 | `CD_CLI` | `INT` |
| 3 | `DT_TRAN` | `DATE` |
| 4 | `CD_NTZ_CTB_TRAN` | `STRING` |
| 5 | `CD_CTGR_TRAN_OGNL` | `INT` |
| 6 | `CD_TIP_MOE_CRR` | `STRING` |
| 7 | `VL_TRAN` | `DECIMAL(15,2)` |

Nomes, ordem e tipos — incluindo precisão e escala decimal — compõem a assinatura funcional. Nulabilidade e metadados de transporte não alteram essa assinatura. Divergência estrutural bloqueia o processamento.

Sem janela financeira, a fonte de movimentações não é consultada e o conjunto funcional é vazio.

## 4. Formação e elegibilidade do cliente

### 4.1 Referência do cliente

Para o cliente elegível:

```text
TS_INCL_TRAN_REF = MAX(TS_INCL_TRAN)
```

Esse timestamp ancora a determinação do ciclo financeiro.

### 4.2 Unicidade do CPF

```text
FL_CPF_UNICO = 'S' se COUNT(DISTINCT NR_CPF_CNPJ_TITR) = 1
FL_CPF_UNICO = 'N' caso contrário
```

`COUNT(DISTINCT)` ignora valores nulos. Portanto:

- um único CPF não nulo, ainda que acompanhado de valores nulos, resulta em `S`;
- nenhum CPF não nulo resulta em `N`;
- dois ou mais CPFs não nulos distintos resultam em `N`.

Quando único:

```text
CD_CPF = CAST(MAX(NR_CPF_CNPJ_TITR) AS DECIMAL(14,0))
```

Quando não único, `CD_CPF = NULL`.

### 4.3 Conta elegível

Uma linha fornece conta candidata quando:

```text
NR_MCA_PCT_OPB = 999999999
CD_PRD = 6
NR_AG_TITR IS NOT NULL
CD_CT_TITR IS NOT NULL
TRIM(CAST(CD_CT_TITR AS STRING)) != ''
```

As contas são agrupadas pelos valores físicos de `NR_AG_TITR` e `CD_CT_TITR` antes da normalização.

```text
FL_CONTA_ELEGIVEL_UNICA = 'S' se existir exatamente um par distinto
FL_CONTA_ELEGIVEL_UNICA = 'N' caso contrário
```

Agência e conta somente são propagadas quando a flag é `S`. Representações físicas diferentes que futuramente resultariam na mesma conta normalizada continuam contando como pares distintos nesta etapa.

### 4.4 Normalização de agência e conta

O schema lógico da conta normalizada é:

| Ordem | Atributo | Tipo |
|---:|---|---|
| 1 | `FL_CONTA_ELEGIVEL_UNICA` | `STRING` |
| 2 | `NR_AG_TITR` | Tipo recebido da fonte |
| 3 | `CD_CT_TITR` | Tipo recebido da fonte |
| 4 | `CD_UOR_CC_NORM` | `INT` |
| 5 | `NR_CC_NORM` | `DECIMAL(11,0)` |

Passos:

1. converter agência e conta para texto;
2. remover espaços nas extremidades com `TRIM`;
3. exigir apenas dígitos, conforme `^[0-9]+$`;
4. exigir `FL_CONTA_ELEGIVEL_UNICA = 'S'`;
5. converter a agência para inteiro e exigir o intervalo INT32;
6. remover zeros à esquerda da conta;
7. exigir no máximo 11 dígitos significativos;
8. quando a conta contiver somente zeros, normalizá-la para `0`.

As duas saídas normalizadas ficam nulas quando qualquer condição falha. Exemplos:

| Agência física | Conta física | Flag única | Resultado |
|---|---|---|---|
| `" 3242 "` | `"0000047949   "` | `S` | agência `3242`; conta `47949` |
| `"7"` | `"00000000000"` | `S` | agência `7`; conta `0` |
| `"32A2"` | `"47949"` | `S` | ambas nulas |
| `"2147483648"` | `"47949"` | `S` | ambas nulas |
| `"3242"` | `"123456789012"` | `S` | ambas nulas |
| `"3242"` | `"47949"` | `N` | ambas nulas |

## 5. Ciclo e janela financeira

### 5.1 Seleção do ciclo

Com conta normalizada, os registros são particionados por `(CD_UOR_CC, NR_CC)` e ordenados por `TS_ULT_EXEA_PSQ DESC`. A primeira linha fornece:

- `TS_DD_INC_MM_CLC_BLC_REF = TS_ULT_EXEA_PSQ`;
- `DD_INC_MM_CLC_BLC = CAST(DD_INC_MM_CLC_BLC AS SMALLINT)`.

Não existe segundo critério de desempate. Duas linhas com o mesmo maior timestamp deixam a escolha entre elas sem ordenação adicional.

### 5.2 Fallback do dia

| Situação | `DD_INC_MM_CLC_BLC_FALLBACK` |
|---|---:|
| Conta normalizada indisponível | `NULL` |
| Conta disponível, mas sem registro ou sem dia em ciclo | `1` |
| Registro de ciclo com dia | Valor de `DD_INC_MM_CLC_BLC` |

Um dia resolvido fora do intervalo `1..31` bloqueia o processamento.

### 5.3 Início do ciclo aberto

O cálculo usa `TS_INCL_TRAN_REF` e o dia de fallback:

1. forma-se um candidato no mês do timestamp de referência;
2. quando o mês não possui o dia contratual, usa-se seu último dia;
3. se `TS_INCL_TRAN_REF` for maior ou igual ao candidato, o candidato é o início do ciclo aberto;
4. caso contrário, o início aberto é o dia contratual no mês anterior, novamente limitado ao último dia disponível.

A comparação considera o timestamp completo contra a meia-noite do dia candidato.

### 5.4 Janela de ciclos fechados

```text
DT_REF_FIM = início do ciclo aberto - 1 dia
DT_REF_INI = início do ciclo aberto recuado em periodo meses
```

O recuo de `DT_REF_INI` sempre parte do dia contratual original, não do dia eventualmente truncado em um mês curto. No mês de destino, o dia é novamente limitado ao último dia disponível.

Exemplo:

| Dia do ciclo | Referência | Período | `DT_REF_INI` | `DT_REF_FIM` |
|---:|---|---:|---|---|
| 10 | 13/08/2026 | 2 | 10/06/2026 | 09/08/2026 |

A janela é inclusiva nas duas extremidades:

```text
DT_REF_INI <= DT_TRAN <= DT_REF_FIM
```

Sem dia de fallback, `DT_REF_INI` e `DT_REF_FIM` são simultaneamente nulos. A existência de somente uma das duas datas é inconsistente e bloqueia.

## 6. Renda e perfil financeiro

### 6.1 Seleção da renda

A renda somente é procurada quando o CPF é único e não nulo. Os registros são particionados por CPF e ordenados por `DT_INCL_REN_AVLD DESC`.

A primeira linha fornece:

```text
DT_REN_PRES_REF = CAST(DT_INCL_REN_AVLD AS DATE)
VL_REN_PRES = CAST(VL_REN * periodo AS DECIMAL(17,2))
```

Não existe desempate adicional para mais de uma linha na mesma maior data. Também não há corte da data de renda pela data de execução.

Na ausência de renda elegível:

- `DT_REN_PRES_REF = NULL`;
- `VL_REN_PRES = NULL`.

Renda física nula também produz renda presumida nula. O ajuste por período representa a mesma renda mensal multiplicada pela quantidade de ciclos; não é uma soma de registros mensais distintos.

### 6.2 Seleção do perfil

Somente registros com `DT_REF <= DATA_EXECUCAO` são elegíveis. Seleciona-se a maior `DT_REF` e todos os registros existentes nessa data.

| Cardinalidade na maior data | Tratamento |
|---:|---|
| 0 | Criar uma linha com os cinco atributos de perfil nulos. |
| 1 | Aceitar o perfil. |
| 2 ou mais | Bloquear por ambiguidade. |

Os atributos resultantes são:

- `DT_REF_PRFL`;
- `CD_MAC_PRFL_CLI`;
- `NM_MAC_PRFL_CLI`;
- `CD_MIC_PRFL_CLI`;
- `NM_MIC_PRFL_CLI`.

Somente `CD_MAC_PRFL_CLI` participa das pontuações. Nomes e microperfil são informativos. Um macroperfil fora de `(1,2,3)` permanece no resultado, mas torna nulas as pontuações de perfil dos quatro temas que dependem dele.

## 7. Movimentações e reconciliação

### 7.1 Marcação temporal

Cada movimentação consultada recebe:

```text
IN_JANELA = 'S' se DT_REF_INI <= DT_TRAN <= DT_REF_FIM
IN_JANELA = 'N' caso contrário
```

O universo oficial bruto contém somente linhas `IN_JANELA = 'S'` antes de qualquer anulação.

### 7.2 Reconciliação por pares exatos

Uma linha pode participar de par exato quando:

- `NR_TRAN_INST_PCT` não é nulo;
- `CD_NTZ_CTB_TRAN` pertence a `('C','D')`;
- `DT_TRAN` não é nula;
- `VL_TRAN` não é nulo;
- `CD_TIP_MOE_CRR` não é nula.

As linhas são agrupadas por:

```text
CD_CLI
DT_TRAN
VL_TRAN
CD_TIP_MOE_CRR
IN_JANELA
```

Categoria não faz parte da chave. Crédito e débito de categorias diferentes podem se anular quando os demais componentes coincidirem.

Para cada grupo:

```text
QT_PARES_EXATOS = MIN(quantidade de créditos, quantidade de débitos)
```

Em cada natureza, os IDs são ordenados de forma crescente. Os primeiros `QT_PARES_EXATOS` IDs de crédito e débito são consumidos.

Como `IN_JANELA` pertence à chave:

- linhas oficiais formam pares exatos somente com linhas oficiais;
- linhas de contexto formam pares exatos somente com linhas de contexto;
- uma linha oficial não forma par exato com linha externa.

Os consumos são rotulados como `EXATO_OFICIAL` ou `EXATO_CONTEXTO`.

### 7.3 Universo residual

Todos os IDs consumidos por pares exatos são retirados do contexto. Somente as linhas restantes podem participar da reconciliação de borda.

### 7.4 Reconciliação de borda

Um par de borda exige:

- mesmo cliente;
- mesmo valor;
- mesma moeda;
- naturezas opostas;
- uma linha dentro e outra fora da janela;
- diferença absoluta entre as datas de 1 a 5 dias, inclusive.

Categoria não participa da chave. Diferença de zero dia não é borda; diferenças de seis dias ou mais são rejeitadas.

Para cada combinação de cliente, valor, moeda e natureza:

1. as listas interna e externa são ordenadas por `(DT_TRAN, NR_TRAN_INST_PCT)`;
2. avaliam-se as possibilidades de pular uma linha interna, pular uma linha externa ou formar um par elegível;
3. escolhe-se a solução com a seguinte prioridade:
   1. maior quantidade total de pares;
   2. menor soma das diferenças absolutas em dias;
   3. menor assinatura lexicográfica dos pares de IDs.

A linha interna recebe `BORDA_OFICIAL` e a contraparte externa recebe `BORDA_CONTEXTO`.

### 7.5 Remoções oficiais e universo efetivo

Somente IDs com `EXATO_OFICIAL` ou `BORDA_OFICIAL` são removidos do universo oficial bruto.

O universo efetivo preserva:

| Atributo |
|---|
| `CD_CLI` |
| `DT_TRAN` |
| `CD_NTZ_CTB_TRAN` |
| `CD_CTGR_TRAN_OGNL` |
| `CD_TIP_MOE_CRR` |
| `VL_TRAN` |

O identificador da transação já cumpriu sua função na reconciliação e não avança para as fórmulas financeiras.

### 7.6 Invariantes da reconciliação

O processamento bloqueia quando qualquer uma destas condições falha:

```text
COUNT(ids consumidos) = COUNT(DISTINCT ids consumidos)
COUNT(ids oficiais removidos) = COUNT(DISTINCT ids oficiais removidos)
QT_REMOVIDAS_OFICIAIS = 2 * QT_PARES_EXATOS_OFICIAIS + QT_PARES_BORDA
QT_EFETIVO = QT_OFICIAL_BRUTO - QT_REMOVIDAS_OFICIAIS
```

## 8. Mapa de categorias e classificação

### 8.1 Schema do mapa

O mapa possui exatamente 70 linhas e 12 atributos:

| Ordem | Atributo | Tipo | Nulável | Significado |
|---:|---|---|---|---|
| 1 | `TIPO` | `STRING` | Sim | Natureza contábil: crédito (`C`), débito (`D`) ou nula. |
| 2 | `CD_GRUPO` | `INT` | Não | Código do grupo negocial. |
| 3 | `TX_GRUPO` | `STRING` | Não | Nome do grupo. |
| 4 | `CD_CATEGORIA` | `INT` | Não | Código da categoria física. |
| 5 | `TX_CATEGORIA` | `STRING` | Não | Nome da categoria. |
| 6 | `CD_IR` | `INT` | Não | Código de tratamento no imposto de renda. |
| 7 | `TX_IR` | `STRING` | Não | Descrição do tratamento no imposto de renda. |
| 8 | `CD_CLASS_RADAR` | `INT` | Não | Código da classe temática Radar. |
| 9 | `TX_CLASS_RADAR` | `STRING` | Não | Nome da classe temática Radar. |
| 10 | `IN_AGRO` | `STRING` | Não | Indica classificação Agro. |
| 11 | `IN_PARTICIPA_CALCULO` | `STRING` | Não | Indica participação nas somas temáticas. |
| 12 | `IN_PARTICIPA_ORCAMENTO` | `STRING` | Não | Indica participação nos totais orçamentários. |

A chave de casamento é composta:

```text
movimento.CD_CTGR_TRAN_OGNL = mapa.CD_CATEGORIA
E movimento.CD_NTZ_CTB_TRAN = mapa.TIPO
```

O contrato exige 70 linhas e 70 chaves distintas. Como igualdade SQL com `NULL` não é verdadeira, as linhas de categorias 0 e 83, cujo `TIPO` é nulo, não casam com movimentos de natureza `C` ou `D`.

### 8.2 Domínio de grupos

| `CD_GRUPO` | `TX_GRUPO` |
|---:|---|
| 0 | Sem categoria |
| 1 | Receitas |
| 2 | Casa |
| 3 | Educação |
| 4 | Lazer |
| 5 | Saúde |
| 6 | Alimentação |
| 7 | Transporte |
| 8 | Despesas Pessoais |
| 9 | Comunicação |
| 10 | Tarifas e impostos |
| 11 | Outros |
| 12 | Fatura |
| 13 | Investimentos |
| 14 | Agro |

### 8.3 Domínio de imposto de renda

| `CD_IR` | `TX_IR` |
|---:|---|
| 0 | Não pertence |
| 1 | Pagamentos efetuados |
| 2 | Bens e direitos |
| 3 | Dívidas e ônus reais |
| 4 | Doações efetuadas |

`CD_IR` e `TX_IR` descrevem a categoria, mas não entram nas fórmulas de orçamento ou pontuação.

### 8.4 Domínio de classes Radar

| `CD_CLASS_RADAR` | `TX_CLASS_RADAR` | Natureza esperada no cálculo |
|---:|---|---|
| 0 | Outras Entradas | Crédito |
| 1 | Renda | Crédito |
| 2 | Estorno | Crédito |
| 3 | Resgate | Crédito |
| 4 | Crédito | Crédito |
| 5 | Indeterminado | Débito |
| 6 | Essenciais | Débito |
| 7 | Não Essenciais | Débito |
| 8 | Futuro | Débito |
| 9 | Obrigações | Débito |

O motor possui campo para classe 4, mas nenhuma das 70 linhas atuais está associada a essa classe.

### 8.5 Mapa integral

| `TIPO` | `CD_GRUPO` | `TX_GRUPO` | `CD_CATEGORIA` | `TX_CATEGORIA` | `CD_IR` | `TX_IR` | `CD_CLASS_RADAR` | `TX_CLASS_RADAR` | `IN_AGRO` | `IN_PARTICIPA_CALCULO` | `IN_PARTICIPA_ORCAMENTO` |
|---|---:|---|---:|---|---:|---|---:|---|---|---|---|
| `NULL` | 0 | Sem categoria | 0 | Sem categoria | 0 | Não pertence | 0 | Outras Entradas | N | S | S |
| C | 1 | Receitas | 1 | Salário | 0 | Não pertence | 1 | Renda | N | S | S |
| C | 1 | Receitas | 2 | Vale Alimentação | 0 | Não pertence | 1 | Renda | N | S | S |
| C | 1 | Receitas | 3 | Restituição de IR | 0 | Não pertence | 2 | Estorno | N | S | S |
| C | 1 | Receitas | 4 | Bonificação | 0 | Não pertence | 1 | Renda | N | S | S |
| C | 1 | Receitas | 5 | Outros Rendimentos | 0 | Não pertence | 1 | Renda | N | S | S |
| D | 2 | Casa | 6 | Água | 0 | Não pertence | 6 | Essenciais | N | S | S |
| D | 2 | Casa | 7 | Eletricidade e Gás | 0 | Não pertence | 6 | Essenciais | N | S | S |
| D | 2 | Casa | 9 | Compra de Imóvel | 2 | Bens e direitos | 9 | Obrigações | N | S | S |
| D | 2 | Casa | 10 | Aluguel e Condomínio | 0 | Não pertence | 6 | Essenciais | N | S | S |
| D | 2 | Casa | 11 | Móveis e Utensílios | 0 | Não pertence | 7 | Não Essenciais | N | S | S |
| D | 2 | Casa | 12 | Serviços e Manutenção | 0 | Não pertence | 6 | Essenciais | N | S | S |
| D | 2 | Casa | 13 | Empregados | 0 | Não pertence | 7 | Não Essenciais | N | S | S |
| D | 2 | Casa | 14 | Animais e Pets | 0 | Não pertence | 7 | Não Essenciais | N | S | S |
| D | 3 | Educação | 15 | Educação Superior | 1 | Pagamentos efetuados | 7 | Não Essenciais | N | S | S |
| D | 3 | Educação | 16 | Colégio | 1 | Pagamentos efetuados | 6 | Essenciais | N | S | S |
| D | 3 | Educação | 17 | Idiomas | 0 | Não pertence | 7 | Não Essenciais | N | S | S |
| D | 3 | Educação | 18 | Publicações e Papelaria | 0 | Não pertence | 7 | Não Essenciais | N | S | S |
| D | 3 | Educação | 20 | Outros Gastos, Educação | 0 | Não pertence | 7 | Não Essenciais | N | S | S |
| D | 4 | Lazer | 21 | Viagens e Lazer | 0 | Não pertence | 7 | Não Essenciais | N | S | S |
| D | 4 | Lazer | 22 | Esportes e Academia | 0 | Não pertence | 7 | Não Essenciais | N | S | S |
| D | 4 | Lazer | 25 | Cultura e Entretenimento | 0 | Não pertence | 7 | Não Essenciais | N | S | S |
| D | 5 | Saúde | 27 | Plano de Saúde | 1 | Pagamentos efetuados | 6 | Essenciais | N | S | S |
| D | 5 | Saúde | 28 | Serviços de Saúde | 1 | Pagamentos efetuados | 6 | Essenciais | N | S | S |
| D | 5 | Saúde | 29 | Dentista | 1 | Pagamentos efetuados | 6 | Essenciais | N | S | S |
| D | 5 | Saúde | 30 | Farmácias e Drogarias | 0 | Não pertence | 6 | Essenciais | N | S | S |
| D | 6 | Alimentação | 32 | Feira e Supermercado | 0 | Não pertence | 6 | Essenciais | N | S | S |
| D | 6 | Alimentação | 35 | Bar, Rest. e Padaria | 0 | Não pertence | 7 | Não Essenciais | N | S | S |
| D | 7 | Transporte | 36 | Compra de Veículo | 2 | Bens e direitos | 9 | Obrigações | N | S | S |
| D | 7 | Transporte | 37 | Combustível | 0 | Não pertence | 6 | Essenciais | N | S | S |
| D | 7 | Transporte | 38 | Estacionamento e Pedágio | 0 | Não pertence | 7 | Não Essenciais | N | S | S |
| D | 7 | Transporte | 39 | Seguro de Veículo | 0 | Não pertence | 7 | Não Essenciais | N | S | S |
| D | 7 | Transporte | 40 | Serviços e Manutenção | 0 | Não pertence | 7 | Não Essenciais | N | S | S |
| D | 7 | Transporte | 41 | Transporte Urbano e Apps | 0 | Não pertence | 6 | Essenciais | N | S | S |
| D | 8 | Despesas Pessoais | 42 | Vestuário e Acessórios | 0 | Não pertence | 7 | Não Essenciais | N | S | S |
| D | 8 | Despesas Pessoais | 43 | Cuidado Pessoal e Beleza | 0 | Não pertence | 7 | Não Essenciais | N | S | S |
| D | 8 | Despesas Pessoais | 44 | Compras Diversas | 0 | Não pertence | 5 | Indeterminado | N | S | S |
| D | 8 | Despesas Pessoais | 45 | Pensão Alimentícia | 1 | Pagamentos efetuados | 6 | Essenciais | N | S | S |
| D | 8 | Despesas Pessoais | 46 | Seguros e Previdência | 0 | Não pertence | 5 | Indeterminado | N | S | S |
| D | 8 | Despesas Pessoais | 47 | Doação | 4 | Doações efetuadas | 7 | Não Essenciais | N | S | S |
| D | 8 | Despesas Pessoais | 48 | Gasto com Familiares | 0 | Não pertence | 7 | Não Essenciais | N | S | S |
| D | 8 | Despesas Pessoais | 49 | Presentes | 0 | Não pertence | 7 | Não Essenciais | N | S | S |
| D | 9 | Comunicação | 51 | Telefonia e Internet | 0 | Não pertence | 6 | Essenciais | N | S | S |
| D | 9 | Comunicação | 53 | Assinatura TV e Streaming | 0 | Não pertence | 7 | Não Essenciais | N | S | S |
| D | 10 | Tarifas e impostos | 54 | IPTU | 0 | Não pertence | 6 | Essenciais | N | S | S |
| D | 10 | Tarifas e impostos | 55 | IPVA e Gastos Detran | 0 | Não pertence | 6 | Essenciais | N | S | S |
| D | 10 | Tarifas e impostos | 56 | Imposto de Renda | 0 | Não pertence | 6 | Essenciais | N | S | S |
| D | 10 | Tarifas e impostos | 57 | ISS(Imposto sobre Serviços) | 0 | Não pertence | 6 | Essenciais | N | S | S |
| D | 10 | Tarifas e impostos | 58 | GPS(Guia de Previdência Social) | 0 | Não pertence | 8 | Futuro | N | S | S |
| D | 10 | Tarifas e impostos | 59 | Serviços Financeiros | 0 | Não pertence | 9 | Obrigações | N | S | S |
| D | 8 | Despesas Pessoais | 60 | Serviços Diversos | 0 | Não pertence | 7 | Não Essenciais | N | S | S |
| D | 4 | Lazer | 61 | Jogos e Loterias | 0 | Não pertence | 7 | Não Essenciais | N | S | S |
| `NULL` | 0 | Sem categoria | 83 | Sem Categoria | 0 | Não pertence | 0 | Outras Entradas | N | S | S |
| D | 12 | Fatura | 111 | Cartão de Crédito | 0 | Não pertence | 9 | Obrigações | N | N | N |
| D | 11 | Outros | 279 | Gastos Diversos | 0 | Não pertence | 5 | Indeterminado | N | S | S |
| C | 14 | Agro | 300 | Receitas Agro | 0 | Não pertence | 1 | Renda | S | N | N |
| D | 14 | Agro | 310 | Criações | 0 | Não pertence | 5 | Indeterminado | S | N | N |
| D | 14 | Agro | 330 | Cultivos | 0 | Não pertence | 5 | Indeterminado | S | N | N |
| D | 14 | Agro | 350 | Insumos | 0 | Não pertence | 5 | Indeterminado | S | N | N |
| D | 14 | Agro | 370 | Apoio Produtivo | 0 | Não pertence | 5 | Indeterminado | S | N | N |
| D | 10 | Tarifas e impostos | 3787 | IOF | 0 | Não pertence | 9 | Obrigações | N | S | S |
| D | 10 | Tarifas e impostos | 3788 | Encargos e Tarifas | 0 | Não pertence | 9 | Obrigações | N | S | S |
| D | 2 | Casa | 3790 | Seguro Residencial | 0 | Não pertence | 7 | Não Essenciais | N | S | S |
| D | 8 | Despesas Pessoais | 4417 | Empréstimos e Prestações | 3 | Dívidas e ônus reais | 9 | Obrigações | N | S | S |
| D | 11 | Outros | 39434 | Cheque | 0 | Não pertence | 5 | Indeterminado | N | S | S |
| D | 11 | Outros | 39435 | Saque | 0 | Não pertence | 5 | Indeterminado | N | S | S |
| D | 11 | Outros | 39436 | Transferência | 0 | Não pertence | 5 | Indeterminado | N | S | S |
| D | 11 | Outros | 39437 | Boletos Diversos | 0 | Não pertence | 5 | Indeterminado | N | S | S |
| D | 13 | Investimentos | 448977 | Aplicação | 0 | Não pertence | 8 | Futuro | N | S | N |
| C | 13 | Investimentos | 448978 | Resgate de Investimentos | 0 | Não pertence | 3 | Resgate | N | S | N |

### 8.6 Ausência de classificação

O casamento usa `LEFT JOIN`. Uma movimentação sem chave no mapa permanece no universo e recebe:

| Atributo | Fallback |
|---|---|
| `TX_CATEGORIA` | `Sem Categoria` |
| `CD_CLASS_RADAR` | `0` |
| `TX_CLASS_RADAR` | `Outras Entradas` |
| `IN_AGRO` | `N` |
| `IN_PARTICIPA_CALCULO` | `N` |
| `IN_PARTICIPA_ORCAMENTO` | `N` |
| `CD_GRUPO`, `TX_GRUPO`, `CD_IR`, `TX_IR` | `NULL` |

A linha sem classificação:

- continua contando na volumetria BRL;
- não entra em soma temática;
- não entra em total orçamentário;
- quando é débito, conserva natureza de saída mesmo recebendo o texto de fallback `Outras Entradas`.

### 8.7 Tratamentos especiais

| Categoria | Natureza | Tratamento |
|---:|---|---|
| 111 — Cartão de Crédito | D | Classe Obrigações, porém fora do cálculo temático e do orçamento. |
| 300 — Receitas Agro | C | Marca Agro, porém fora do cálculo temático e do orçamento. |
| 310, 330, 350 e 370 — Agro | D | Marcam Agro, porém fora do cálculo temático e do orçamento. |
| 448977 — Aplicação | D | Entra em Futuro, mas não no orçamento. |
| 448978 — Resgate | C | Entra em Resgate, mas não no orçamento. |

## 9. Motor financeiro

### 9.1 Universo em BRL

Depois da classificação, somente `CD_TIP_MOE_CRR = 'BRL'` alimenta quantidades, valores, orçamento, percentuais e pontuações.

As flags de participação não são requisito para entrar no universo BRL. Elas controlam apenas as somas posteriores.

### 9.2 Flag de moeda

`FL_SOMENTE_BRL` é calculada sobre todas as movimentações efetivas, antes do filtro BRL:

| Situação | Resultado |
|---|---|
| Nenhuma movimentação efetiva | `NULL` |
| Exatamente uma moeda não nula distinta e seu máximo é `BRL` | `S` |
| Qualquer outra situação | `N` |

`COUNT(DISTINCT)` e `MAX` ignoram moedas nulas. Consequentemente:

- BRL acompanhada apenas de moedas nulas ainda resulta em `S`;
- somente moedas nulas resulta em `N`, desde que existam linhas;
- BRL acompanhada de outra moeda não nula resulta em `N`.

### 9.3 Flag Agro

`FL_TEM_MOV_AGRO` é calculada somente no universo BRL:

| Situação | Resultado |
|---|---|
| Nenhuma movimentação BRL | `NULL` |
| Pelo menos uma linha BRL com `IN_AGRO = 'S'` | `S` |
| Existem linhas BRL, mas nenhuma Agro | `N` |

A flag independe de participação temática ou orçamentária.

### 9.4 Volumetria

```text
QT_TRANS_TOTAL = COUNT(todas as linhas BRL efetivas)
QT_TRANS_ENT = SUM(1 para natureza C; 0 caso contrário)
QT_TRANS_SAI = SUM(1 para natureza D; 0 caso contrário)
```

Com universo BRL vazio:

- `QT_TRANS_TOTAL = 0`;
- `QT_TRANS_ENT = NULL`;
- `QT_TRANS_SAI = NULL`.

Na invariante de volumetria, apenas esses dois parciais nulos são tratados como zero:

```text
QT_TRANS_TOTAL = COALESCE(QT_TRANS_ENT, 0) + COALESCE(QT_TRANS_SAI, 0)
```

### 9.5 Regra monetária

`VL_TRAN` é usado com seu sinal original. Não se aplica valor absoluto, inversão de sinal nem correção de valores negativos.

Cada soma temática ou orçamentária:

- soma somente as linhas que atendem a seus filtros;
- usa `0.00` quando não há valor elegível;
- retorna `DECIMAL(25,2)`.

### 9.6 Entradas temáticas

Uma entrada temática exige natureza `C` e `IN_PARTICIPA_CALCULO = 'S'`:

| Campo | Classe |
|---|---:|
| `VL_ENT_OUT` | 0 — Outras Entradas |
| `VL_ENT_REN` | 1 — Renda |
| `VL_ENT_EST` | 2 — Estorno |
| `VL_ENT_RESG` | 3 — Resgate |
| `VL_ENT_CRED` | 4 — Crédito |

Com o mapa atual, nenhuma linha casa com a classe 4. As linhas estáticas de classe 0 têm natureza nula e também não casam com créditos `C`. Assim, `VL_ENT_CRED` e `VL_ENT_OUT` permanecem em zero enquanto o mapa mantiver essa configuração.

### 9.7 Saídas temáticas

Uma saída temática exige natureza `D` e `IN_PARTICIPA_CALCULO = 'S'`:

| Campo | Classe |
|---|---:|
| `VL_SAI_IND` | 5 — Indeterminado |
| `VL_SAI_ESS` | 6 — Essenciais |
| `VL_SAI_NAO_ESS` | 7 — Não Essenciais |
| `VL_SAI_FUT` | 8 — Futuro |
| `VL_SAI_OBR` | 9 — Obrigações |

### 9.8 Totais orçamentários

```text
VL_ENT_TOTAL =
  SUM(VL_TRAN onde natureza = C e IN_PARTICIPA_ORCAMENTO = S)

VL_SAI_TOTAL =
  SUM(VL_TRAN onde natureza = D e IN_PARTICIPA_ORCAMENTO = S)

VL_TRANS_ENT = VL_ENT_TOTAL
VL_TRANS_SAI = VL_SAI_TOTAL
```

Participação temática e participação orçamentária são independentes. Uma categoria pode participar de uma, de ambas ou de nenhuma.

### 9.9 Resultado e razão orçamentária

```text
VL_RES_ORC = CAST(VL_ENT_TOTAL - VL_SAI_TOTAL AS DECIMAL(25,2))
```

```text
PC_SAI_ENT = NULL se QT_TRANS_TOTAL = 0 ou VL_ENT_TOTAL = 0
PC_SAI_ENT = ROUND(VL_SAI_TOTAL / VL_ENT_TOTAL, 6) caso contrário
```

`PC_SAI_ENT` é `DECIMAL(9,6)`. Valores negativos não recebem tratamento especial. Quando a divisão produz razão inferior a `0.75`, inclusive por sinais negativos, a regra de faixas aplica o enquadramento superavitário acentuado.

### 9.10 Faixas orçamentárias

| `CD_FAIXA_ORC` | Intervalo de `PC_SAI_ENT` | `CD_RES_ORC` | `TX_RES_ORC` | `TX_STS_RES` | `TX_STS_FINAL` |
|---:|---|---:|---|---|---|
| `NULL` | Razão nula | `NULL` | `NULL` | `NULL` | `NULL` |
| 0 | `0.950000 <= PC <= 1.050000` | 0 | Neutro | `NULL` | Neutro |
| 1 | `1.050000 < PC <= 1.250000` | 2 | Deficitário | Moderado | Deficitário Moderado |
| 2 | `PC > 1.250000` | 2 | Deficitário | Acentuado | Deficitário Acentuado |
| 3 | `0.750000 <= PC < 0.950000` | 1 | Superavitário | Moderado | Superavitário Moderado |
| 4 | `PC < 0.750000` | 1 | Superavitário | Acentuado | Superavitário Acentuado |

## 10. Percentuais e pontuações

### 10.1 Temas pontuados

| Sufixo | Base temática | Tema final |
|---|---|---|
| `IND` | Saídas de classe Indeterminado | Categorização dos Gastos |
| `ESS` | Saídas Essenciais | Gestão de Orçamento |
| `NAO_ESS` | Saídas Não Essenciais | Consumo Planejado |
| `FUT` | Saídas de Futuro | Formação de Reserva |
| `OBR` | Saídas de Obrigações | Uso Consciente do Crédito |

### 10.2 Percentuais observados

Para cada tema:

```text
PC_SAI_TEMA = NULL
  se BASE_FINANCEIRA IS NULL ou BASE_FINANCEIRA <= 0

PC_SAI_TEMA = ROUND(VL_SAI_TEMA / BASE_FINANCEIRA, 6)
  caso contrário
```

| Campo | Numerador |
|---|---|
| `PC_SAI_IND` | `VL_SAI_IND` |
| `PC_SAI_ESS` | `VL_SAI_ESS` |
| `PC_SAI_NAO_ESS` | `VL_SAI_NAO_ESS` |
| `PC_SAI_FUT` | `VL_SAI_FUT` |
| `PC_SAI_OBR` | `VL_SAI_OBR` |

No resultado oficial, `BASE_FINANCEIRA = VL_REN_PRES`. Todos os percentuais são `DECIMAL(9,6)`.

### 10.3 Percentuais fixos de referência

| Campo | Valor |
|---|---:|
| `PC_REF_IND` | `0.750000` |
| `PC_REF_ESS` | `0.500000` |
| `PC_REF_NAO_ESS` | `0.300000` |
| `PC_REF_FUT` | `0.200000` |
| `PC_REF_OBR` | `0.300000` |

Essas referências são constantes e não dependem do cliente, período, perfil ou cenário.

### 10.4 Nulabilidade comum da concentração

Cada pontuação de concentração segue primeiro esta precedência:

| Condição | Resultado |
|---|---:|
| `QT_TRANS_TOTAL IS NULL` | `NULL` |
| `QT_TRANS_TOTAL = 0` | `NULL` |
| `BASE_FINANCEIRA IS NULL` | `NULL` |
| `BASE_FINANCEIRA <= 0` | `0` |
| Base positiva | Aplicar matriz do tema. |

Assim, base zero ou negativa torna os percentuais observados nulos, mas torna as pontuações de concentração iguais a zero quando existem transações.

### 10.5 Pontuação de concentração

#### Indeterminado

| Condição | `NR_PONT_CONC_IND` |
|---|---:|
| `PC_SAI_IND > 0.750000` | 99 |
| `PC_SAI_IND <= 0.750000` | 0 |

O limite de `0.750000` pertence à faixa de zero ponto.

#### Essenciais

| Condição | `NR_PONT_CONC_ESS` |
|---|---:|
| `PC_SAI_ESS < 0.500000` | 0 |
| `0.500000 <= PC_SAI_ESS < 0.750000` | 1 |
| `PC_SAI_ESS >= 0.750000` | 2 |

#### Não Essenciais

| Condição | `NR_PONT_CONC_NAO_ESS` |
|---|---:|
| `PC_SAI_NAO_ESS < 0.300000` | 0 |
| `0.300000 <= PC_SAI_NAO_ESS < 0.450000` | 1 |
| `PC_SAI_NAO_ESS >= 0.450000` | 2 |

#### Futuro

| Condição | `NR_PONT_CONC_FUT` |
|---|---:|
| `PC_SAI_FUT >= 0.300000` | 0 |
| `0.200000 <= PC_SAI_FUT < 0.300000` | 1 |
| `PC_SAI_FUT < 0.200000` | 2 |

Quanto menor a participação destinada ao Futuro, maior a prioridade atribuída a esse tema.

#### Obrigações

| Condição | `NR_PONT_CONC_OBR` |
|---|---:|
| `PC_SAI_OBR < 0.300000` | 0 |
| `0.300000 <= PC_SAI_OBR < 0.450000` | 1 |
| `PC_SAI_OBR >= 0.450000` | 2 |

### 10.6 Pontuação orçamentária

`NR_PONT_ORC_IND` é:

- `NULL` quando `QT_TRANS_TOTAL` é nulo ou zero;
- `0` caso contrário.

Para os demais temas, quantidade nula ou zero, ou faixa orçamentária nula, produz `NULL`.

| `CD_FAIXA_ORC` | `NR_PONT_ORC_ESS` | `NR_PONT_ORC_NAO_ESS` | `NR_PONT_ORC_FUT` | `NR_PONT_ORC_OBR` |
|---:|---:|---:|---:|---:|
| 0 | 1 | 1 | 1 | 1 |
| 1 | 1 | 1 | 0 | 1 |
| 2 | 2 | 2 | 0 | 2 |
| 3 | 0 | 0 | 1 | 0 |
| 4 | 0 | 0 | 2 | 0 |

### 10.7 Pontuação de perfil

Domínio negocial do macroperfil:

| `CD_MAC_PRFL_CLI` | Perfil |
|---:|---|
| 1 | Endividado |
| 2 | Equilibrista |
| 3 | Investidor |

`NR_PONT_PRFL_IND` é:

- `NULL` quando `QT_TRANS_TOTAL` é nulo ou zero;
- `0` caso contrário, independentemente do perfil.

Para os demais temas:

- quantidade nula ou zero produz `NULL`;
- macroperfil nulo ou fora de `(1,2,3)` produz `NULL`;
- macroperfil válido aplica a matriz.

| Macroperfil | `NR_PONT_PRFL_ESS` | `NR_PONT_PRFL_NAO_ESS` | `NR_PONT_PRFL_FUT` | `NR_PONT_PRFL_OBR` |
|---:|---:|---:|---:|---:|
| 1 — Endividado | 0 | 1 | 0 | 2 |
| 2 — Equilibrista | 1 | 0 | 1 | 0 |
| 3 — Investidor | 1 | 0 | 2 | 0 |

### 10.8 Pontuações finais

O tema de Categorização dos Gastos possui regra especial:

```text
NR_PONT_IND_FIM = NR_PONT_CONC_IND
```

`NR_PONT_ORC_IND` e `NR_PONT_PRFL_IND` existem no contrato, mas não são somados à pontuação final de IND.

Para os demais temas:

```text
NR_PONT_TEMA_FIM =
  NR_PONT_CONC_TEMA
  + NR_PONT_ORC_TEMA
  + NR_PONT_PRFL_TEMA
```

Se qualquer parcela for nula, a pontuação final correspondente é nula.

### 10.9 Completude

`FL_PONTUACAO_COMPLETA = 'S'` somente quando as cinco pontuações finais são não nulas. Em qualquer outro estado, recebe `N`.

Uma base financeira menor ou igual a zero não impede, por si só, a completude: havendo transações, orçamento classificável e macroperfil válido, as concentrações serão zero e as demais parcelas poderão completar as pontuações.

### 10.10 Máximo, empate e vencedor

Com pontuação incompleta:

| Atributo | Valor |
|---|---|
| `NR_PONT_MAX` | `NULL` |
| `QT_TEMAS_PONT_MAX` | `NULL` |
| `CD_TEMA_VENCEDOR` | `NULL` |
| `TX_TEMA_VENCEDOR` | `NULL` |

Com pontuação completa:

```text
NR_PONT_MAX = maior das cinco pontuações finais
QT_TEMAS_PONT_MAX = quantidade de temas iguais ao máximo
```

Máximo igual a zero é válido.

| `CD_TEMA_VENCEDOR` | `TX_TEMA_VENCEDOR` | Condição |
|---:|---|---|
| 1 | Categorização dos Gastos | IND é o único máximo. |
| 2 | Gestão de Orçamento | ESS é o único máximo. |
| 3 | Consumo Planejado | NÃO ESS. é o único máximo. |
| 4 | Formação de Reserva | FUTURO é o único máximo. |
| 5 | Uso Consciente do Crédito | OBRIGAÇÕES é o único máximo. |
| 9 | Empate | Dois ou mais temas compartilham o máximo. |

## 11. Cenários financeiros

### 11.1 Cenários disponíveis

Existem exatamente dois códigos:

| `CD_CENARIO` | Base |
|---|---|
| `RENDA_PRESUMIDA` | Renda presumida ajustada ao período. |
| `ENTRADAS_REALIZADAS` | Soma de créditos efetivos, classificados e em BRL. |

`BASE_FINANCEIRA` é `DECIMAL(25,2)`.

### 11.2 Base de renda presumida

```text
BASE_FINANCEIRA = CAST(VL_REN_PRES AS DECIMAL(25,2))
```

Se `DT_REF_INI` ou `DT_REF_FIM` for nula, a base do cenário também é nula, ainda que exista renda disponível.

### 11.3 Base de entradas realizadas

Uma linha participa quando:

- pertence ao universo efetivo, portanto não foi reconciliada;
- possui natureza `C`;
- possui moeda `BRL`;
- casa por `INNER JOIN` com categoria e natureza no mapa.

Não são aplicados `IN_PARTICIPA_CALCULO` nem `IN_PARTICIPA_ORCAMENTO`. Por isso:

- resgate de investimentos participa;
- receita Agro participa;
- crédito classificado fora do tema ou do orçamento pode participar;
- crédito sem classificação é excluído;
- moeda diferente de BRL é excluída;
- débitos são excluídos.

```text
ENTRADAS_REALIZADAS = CAST(SUM(VL_TRAN) AS DECIMAL(25,2))
```

| Situação | Base |
|---|---|
| Janela indisponível | `NULL` |
| Janela válida, sem crédito elegível | `0.00` |
| Janela válida, com créditos elegíveis | Soma direta de `VL_TRAN`. |

Valores negativos continuam com o sinal original na soma.

### 11.4 Aplicação da base

Para cada cenário, a mesma `BASE_FINANCEIRA` substitui simultaneamente:

```text
VL_ENT_TOTAL na entrada da etapa de orçamento
VL_REN_PRES na entrada da etapa de percentuais
```

Em seguida são recalculadas, na mesma ordem:

1. classificação orçamentária;
2. percentuais;
3. pontuações;
4. vencedor.

Não existe fórmula específica por cenário nessas quatro etapas.

### 11.5 Campos recalculados

O snapshot de cenário conserva o contrato de 80 atributos. São substituídos somente 31 campos.

Orçamento:

- `VL_RES_ORC`;
- `PC_SAI_ENT`;
- `CD_RES_ORC`;
- `TX_RES_ORC`;
- `CD_FAIXA_ORC`;
- `TX_STS_RES`;
- `TX_STS_FINAL`.

Percentuais, concentração, orçamento dependente e fechamento:

- `PC_SAI_IND`, `PC_SAI_ESS`, `PC_SAI_NAO_ESS`, `PC_SAI_FUT` e `PC_SAI_OBR`;
- `NR_PONT_CONC_IND`, `NR_PONT_CONC_ESS`, `NR_PONT_CONC_NAO_ESS`, `NR_PONT_CONC_FUT` e `NR_PONT_CONC_OBR`;
- `NR_PONT_ORC_ESS`, `NR_PONT_ORC_NAO_ESS`, `NR_PONT_ORC_FUT` e `NR_PONT_ORC_OBR`;
- `NR_PONT_IND_FIM`, `NR_PONT_ESS_FIM`, `NR_PONT_NAO_ESS_FIM`, `NR_PONT_FUT_FIM` e `NR_PONT_OBR_FIM`;
- `FL_PONTUACAO_COMPLETA`;
- `NR_PONT_MAX`;
- `QT_TEMAS_PONT_MAX`;
- `CD_TEMA_VENCEDOR`;
- `TX_TEMA_VENCEDOR`.

### 11.6 Campos invariantes

Os outros 49 campos permanecem iguais ao resultado oficial, incluindo:

- identificação, datas, CPF, conta, ciclo, renda e perfil;
- janela, flags e quantidades;
- `VL_TRANS_ENT` e `VL_ENT_TOTAL`;
- todos os valores temáticos e de saída;
- referências fixas;
- `NR_PONT_ORC_IND`;
- todas as pontuações de perfil.

A base alternativa é insumo do recálculo, mas não substitui `VL_TRANS_ENT` nem `VL_ENT_TOTAL` dentro do snapshot final. Portanto, o campo `VL_RES_ORC` de um cenário pode ter sido calculado com uma base diferente do valor preservado em `VL_ENT_TOTAL`.

O cenário `RENDA_PRESUMIDA` também pode divergir do resultado oficial: no resultado oficial, o orçamento usa entradas orçamentárias realizadas; no cenário, o orçamento usa a renda presumida como entrada total.

## 12. Estados negociais, nulabilidade e bloqueios

### 12.1 Significado de zero, nulo, ausência e bloqueio

| Estado | Significado |
|---|---|
| `0` ou `0.00` | Resultado calculável cujo valor efetivo é zero. |
| `NULL` | Atributo não calculável, não aplicável ou indisponível, sem necessariamente impedir a linha final. |
| Ausência de registro | A fonte não retornou linha; pode ser convertida em campos nulos, fallback ou bloqueio, conforme a etapa. |
| Bloqueio | O contrato não permite produzir um resultado confiável para a condição encontrada. |

Não se deve substituir `NULL` por zero fora dos casos explicitamente definidos.

### 12.2 Matriz de estados

| Situação | Efeito |
|---|---|
| `CD_CLI` ausente ou inválido | Bloqueio. |
| `periodo` fora de `1..6` ou com tipo inválido | Bloqueio. |
| Cliente sem linha na formação do público | Bloqueio. |
| Nenhum CPF não nulo ou mais de um CPF distinto | `FL_CPF_UNICO = 'N'`; `CD_CPF` e renda ficam nulos. |
| Nenhuma ou várias contas elegíveis | `FL_CONTA_ELEGIVEL_UNICA = 'N'`; conta normalizada e janela ficam nulas. |
| Conta única com texto inválido ou fora dos limites | Campos normalizados e janela ficam nulos. |
| Conta normalizada sem registro de ciclo | Dia fallback `1`; janela continua calculável. |
| Dia de ciclo fora de `1..31` | Bloqueio. |
| Somente uma data da janela preenchida | Bloqueio. |
| Renda ausente | Renda e percentuais nulos; concentração e fechamento incompletos. |
| Mais de um perfil na maior data | Bloqueio. |
| Perfil ausente | Atributos de perfil nulos; pontuações de perfil e fechamento incompletos. |
| Macroperfil fora de `1..3` | Perfil permanece no resultado; pontuações de perfil dependentes ficam nulas. |
| Janela indisponível | Movimentações não são consultadas; cenários recebem base nula. |
| Janela válida sem movimentações BRL | `QT_TRANS_TOTAL = 0`; parciais de quantidade nulos; valores monetários zero; pontuação incompleta. |
| Movimento efetivo sem classificação | Conta na volumetria BRL, mas fica fora das somas temáticas e orçamentárias. |
| Movimento em moeda não BRL | Afeta `FL_SOMENTE_BRL`, mas não alimenta as métricas financeiras. |
| Nenhum BRL | `FL_TEM_MOV_AGRO = NULL`. |
| Base financeira nula | Percentuais e concentrações nulos; pontuação incompleta. |
| Base financeira zero ou negativa com transações | Percentuais nulos; concentrações iguais a zero. |
| `VL_ENT_TOTAL = 0` | `PC_SAI_ENT` e faixa orçamentária nulos. |
| Mais de um tema no máximo | Vencedor código 9 e texto `Empate`. |

### 12.3 Condições bloqueantes consolidadas

O processamento deve ser interrompido quando ocorrer:

- cliente ausente, booleano, não inteiro ou fora de INT32;
- período inválido;
- cliente fora da formação do público;
- dia de ciclo resolvido fora de `1..31`;
- preenchimento unilateral das datas da janela;
- mais de um perfil na maior data elegível;
- mapa com quantidade diferente de 70 ou chave duplicada;
- schema funcional de movimentações com nome, ordem ou tipo divergente;
- ID consumido mais de uma vez na reconciliação;
- cardinalidade de remoções ou universo efetivo inconsistente;
- volumetria total diferente da soma normalizada de entradas e saídas;
- resultado final com cardinalidade diferente de uma linha;
- resultado com cliente divergente;
- quantidade final diferente de 80 atributos;
- qualquer atributo obrigatório nulo.

## 13. Invariantes negociais

As seguintes igualdades e domínios devem ser verdadeiros:

```text
1 <= periodo <= 6
1 <= DD_INC_MM_CLC_BLC_FALLBACK <= 31, quando não nulo
DT_REF_INI <= DT_REF_FIM, quando a janela existe

QT_TRANS_TOTAL =
  COALESCE(QT_TRANS_ENT, 0) + COALESCE(QT_TRANS_SAI, 0)

VL_TRANS_ENT = VL_ENT_TOTAL
VL_TRANS_SAI = VL_SAI_TOTAL

No resultado oficial:
VL_RES_ORC = VL_ENT_TOTAL - VL_SAI_TOTAL

Nos snapshots de cenário:
VL_RES_ORC = BASE_FINANCEIRA - VL_SAI_TOTAL

NR_PONT_IND_FIM = NR_PONT_CONC_IND

FL_PONTUACAO_COMPLETA = 'S'
  se e somente se as cinco pontuações finais forem não nulas

CD_TEMA_VENCEDOR = 9
  se e somente se a pontuação estiver completa
  e QT_TEMAS_PONT_MAX > 1
```

Além disso:

- o mapa possui 70 linhas e chaves únicas;
- nenhuma transação é consumida em mais de um par;
- cada snapshot de cenário possui o mesmo schema e ordem dos 80 atributos oficiais;
- todas as saídas e fatos transacionais permanecem iguais entre os dois cenários;
- somente os 31 campos declarados podem variar em função da base financeira.

## 14. Contrato final de 80 atributos

### 14.1 Regras do contrato

A ordem dos atributos é parte do contrato. “Obrigatório” indica que o valor da linha final é validado como não nulo. Um campo não marcado como obrigatório pode ser naturalmente não nulo por sua fórmula, mas não pertence ao conjunto de 12 valores submetidos ao gate final.

### 14.2 Cliente, CPF e conta — atributos 1 a 7

| # | Atributo | Tipo | Obrigatório | Origem, significado e dependências | Regra de nulidade |
|---:|---|---|---|---|---|
| 1 | `CD_CLI` | `INT` | Sim | Cliente selecionado e validado; chave do resultado. | Não pode ser nulo. |
| 2 | `DT_EXEA` | `DATE` | Sim | Data de execução derivada de `HOJE`. | Não pode ser nula. |
| 3 | `DT_MES_EXEA` | `DATE` | Sim | Primeiro dia do mês de `DT_EXEA`. | Não pode ser nula. |
| 4 | `TS_INCL_TRAN_REF` | `TIMESTAMP` | Sim | Maior `TS_INCL_TRAN` do cliente na formação do público; ancora o ciclo. | Não pode ser nulo após elegibilidade. |
| 5 | `FL_CPF_UNICO` | `STRING` | Sim | `S` quando existe exatamente um CPF não nulo distinto; `N` nos demais casos. | Não pode ser nula. |
| 6 | `CD_CPF` | `DECIMAL(14,0)` | Não | CPF propagado quando `FL_CPF_UNICO = 'S'`. | Nulo quando o CPF não é único ou não existe CPF não nulo. |
| 7 | `FL_CONTA_ELEGIVEL_UNICA` | `STRING` | Sim | `S` quando existe exatamente um par físico de agência e conta elegível; `N` nos demais casos. | Não pode ser nula. |

### 14.3 Ciclo — atributos 8 a 10

| # | Atributo | Tipo | Obrigatório | Origem, significado e dependências | Regra de nulidade |
|---:|---|---|---|---|---|
| 8 | `TS_DD_INC_MM_CLC_BLC_REF` | `TIMESTAMP` | Não | `TS_ULT_EXEA_PSQ` da linha de ciclo escolhida para a conta normalizada. | Nulo sem linha de ciclo ou sem conta normalizada. |
| 9 | `DD_INC_MM_CLC_BLC` | `SMALLINT` | Não | Dia físico do ciclo na linha escolhida. | Nulo sem linha, sem dia ou sem conta normalizada. |
| 10 | `DD_INC_MM_CLC_BLC_FALLBACK` | `SMALLINT` | Não | Dia efetivamente usado: dia físico ou `1` quando existe conta normalizada sem dia. | Nulo quando a conta normalizada está indisponível. |

### 14.4 Renda — atributos 11 e 12

| # | Atributo | Tipo | Obrigatório | Origem, significado e dependências | Regra de nulidade |
|---:|---|---|---|---|---|
| 11 | `DT_REN_PRES_REF` | `DATE` | Não | Maior `DT_INCL_REN_AVLD` encontrada para o CPF único. | Nula sem CPF único ou sem registro de renda. |
| 12 | `VL_REN_PRES` | `DECIMAL(17,2)` | Não | `VL_REN * periodo` na linha de renda escolhida. | Nulo sem renda, com renda física nula ou sem CPF único. |

### 14.5 Perfil — atributos 13 a 17

| # | Atributo | Tipo | Obrigatório | Origem, significado e dependências | Regra de nulidade |
|---:|---|---|---|---|---|
| 13 | `DT_REF_PRFL` | `DATE` | Não | Maior data de perfil menor ou igual à execução. | Nula quando não existe perfil elegível. |
| 14 | `CD_MAC_PRFL_CLI` | `INT` | Não | Código do macroperfil da linha escolhida; dirige a matriz de perfil. | Nulo quando não existe perfil; códigos fora de `1..3` são preservados. |
| 15 | `NM_MAC_PRFL_CLI` | `STRING` | Não | Nome do macroperfil da mesma linha. | Nulo quando não existe perfil ou quando a fonte o entrega nulo. |
| 16 | `CD_MIC_PRFL_CLI` | `INT` | Não | Código informativo do microperfil. | Nulo quando não existe perfil ou quando a fonte o entrega nulo. |
| 17 | `NM_MIC_PRFL_CLI` | `STRING` | Não | Nome informativo do microperfil. | Nulo quando não existe perfil ou quando a fonte o entrega nulo. |

### 14.6 Janela, moeda e Agro — atributos 18 a 21

| # | Atributo | Tipo | Obrigatório | Origem, significado e dependências | Regra de nulidade |
|---:|---|---|---|---|---|
| 18 | `DT_REF_INI` | `DATE` | Não | Início inclusivo da quantidade solicitada de ciclos fechados. | Nula sem dia de fallback. |
| 19 | `DT_REF_FIM` | `DATE` | Não | Dia imediatamente anterior ao início do ciclo aberto. | Nula sem dia de fallback; deve existir junto com `DT_REF_INI`. |
| 20 | `FL_SOMENTE_BRL` | `STRING` | Não | `S` quando a única moeda não nula distinta das linhas efetivas é BRL; `N` nos demais universos não vazios. | Nula quando não existe movimentação efetiva. |
| 21 | `FL_TEM_MOV_AGRO` | `STRING` | Não | `S` quando existe linha BRL Agro; `N` quando há BRL sem Agro. | Nula quando não existe linha BRL. |

### 14.7 Quantidades e totais diretos — atributos 22 a 26

| # | Atributo | Tipo | Obrigatório | Origem, significado e dependências | Regra de nulidade |
|---:|---|---|---|---|---|
| 22 | `QT_TRANS_TOTAL` | `BIGINT` | Não | Contagem de todas as movimentações efetivas em BRL. | A fórmula retorna `0` no universo vazio. |
| 23 | `QT_TRANS_ENT` | `BIGINT` | Não | Soma de linhas BRL de natureza `C`. | Nula somente quando o universo BRL está vazio. |
| 24 | `QT_TRANS_SAI` | `BIGINT` | Não | Soma de linhas BRL de natureza `D`. | Nula somente quando o universo BRL está vazio. |
| 25 | `VL_TRANS_ENT` | `DECIMAL(25,2)` | Não | Cópia de `VL_ENT_TOTAL`; total de créditos orçamentários. | A fórmula retorna `0.00` sem entrada elegível. |
| 26 | `VL_TRANS_SAI` | `DECIMAL(25,2)` | Não | Cópia de `VL_SAI_TOTAL`; total de débitos orçamentários. | A fórmula retorna `0.00` sem saída elegível. |

### 14.8 Entradas temáticas — atributos 27 a 32

| # | Atributo | Tipo | Obrigatório | Origem, significado e dependências | Regra de nulidade |
|---:|---|---|---|---|---|
| 27 | `VL_ENT_REN` | `DECIMAL(25,2)` | Não | Soma BRL de créditos da classe 1 com participação em cálculo. | `0.00` sem linha elegível. |
| 28 | `VL_ENT_EST` | `DECIMAL(25,2)` | Não | Soma BRL de créditos da classe 2 com participação em cálculo. | `0.00` sem linha elegível. |
| 29 | `VL_ENT_RESG` | `DECIMAL(25,2)` | Não | Soma BRL de créditos da classe 3 com participação em cálculo. | `0.00` sem linha elegível. |
| 30 | `VL_ENT_OUT` | `DECIMAL(25,2)` | Não | Soma BRL de créditos da classe 0 com participação em cálculo. | `0.00` sem linha elegível. |
| 31 | `VL_ENT_CRED` | `DECIMAL(25,2)` | Não | Soma BRL de créditos da classe 4 com participação em cálculo. | `0.00` sem linha elegível. |
| 32 | `VL_ENT_TOTAL` | `DECIMAL(25,2)` | Não | Soma BRL de créditos com `IN_PARTICIPA_ORCAMENTO = 'S'`. | `0.00` sem linha elegível. |

### 14.9 Saídas temáticas — atributos 33 a 38

| # | Atributo | Tipo | Obrigatório | Origem, significado e dependências | Regra de nulidade |
|---:|---|---|---|---|---|
| 33 | `VL_SAI_IND` | `DECIMAL(25,2)` | Não | Soma BRL de débitos da classe 5 com participação em cálculo. | `0.00` sem linha elegível. |
| 34 | `VL_SAI_ESS` | `DECIMAL(25,2)` | Não | Soma BRL de débitos da classe 6 com participação em cálculo. | `0.00` sem linha elegível. |
| 35 | `VL_SAI_NAO_ESS` | `DECIMAL(25,2)` | Não | Soma BRL de débitos da classe 7 com participação em cálculo. | `0.00` sem linha elegível. |
| 36 | `VL_SAI_FUT` | `DECIMAL(25,2)` | Não | Soma BRL de débitos da classe 8 com participação em cálculo. | `0.00` sem linha elegível. |
| 37 | `VL_SAI_OBR` | `DECIMAL(25,2)` | Não | Soma BRL de débitos da classe 9 com participação em cálculo. | `0.00` sem linha elegível. |
| 38 | `VL_SAI_TOTAL` | `DECIMAL(25,2)` | Não | Soma BRL de débitos com `IN_PARTICIPA_ORCAMENTO = 'S'`. | `0.00` sem linha elegível. |

### 14.10 Orçamento — atributos 39 a 45

| # | Atributo | Tipo | Obrigatório | Origem, significado e dependências | Regra de nulidade |
|---:|---|---|---|---|---|
| 39 | `VL_RES_ORC` | `DECIMAL(25,2)` | Não | No oficial, `VL_ENT_TOTAL - VL_SAI_TOTAL`; no cenário, `BASE_FINANCEIRA - VL_SAI_TOTAL`. | No oficial, não nulo pelas somas normalizadas; no cenário, pode ser nulo com base nula. |
| 40 | `PC_SAI_ENT` | `DECIMAL(9,6)` | Não | Razão arredondada `VL_SAI_TOTAL / VL_ENT_TOTAL` no oficial ou `VL_SAI_TOTAL / BASE_FINANCEIRA` no cenário. | Nula sem transação BRL ou quando a entrada usada no cálculo é zero; no cenário, base nula também produz nulo. |
| 41 | `CD_RES_ORC` | `INT` | Não | Código 0 neutro, 1 superavitário ou 2 deficitário, derivado da faixa. | Nulo quando `PC_SAI_ENT` é nulo. |
| 42 | `TX_RES_ORC` | `STRING` | Não | `Neutro`, `Superavitário` ou `Deficitário`. | Nulo quando `PC_SAI_ENT` é nulo. |
| 43 | `CD_FAIXA_ORC` | `INT` | Não | Faixa 0 a 4 segundo os limites da seção 9.10. | Nulo quando `PC_SAI_ENT` é nulo. |
| 44 | `TX_STS_RES` | `STRING` | Não | Intensidade `Moderado` ou `Acentuado`. | Nulo para razão nula e para faixa Neutra. |
| 45 | `TX_STS_FINAL` | `STRING` | Não | Texto completo da faixa orçamentária. | Nulo quando `PC_SAI_ENT` é nulo. |

### 14.11 Percentuais observados — atributos 46 a 50

| # | Atributo | Tipo | Obrigatório | Origem, significado e dependências | Regra de nulidade |
|---:|---|---|---|---|---|
| 46 | `PC_SAI_IND` | `DECIMAL(9,6)` | Não | `ROUND(VL_SAI_IND / BASE_FINANCEIRA, 6)`. | Nulo com base nula, zero ou negativa. |
| 47 | `PC_SAI_ESS` | `DECIMAL(9,6)` | Não | `ROUND(VL_SAI_ESS / BASE_FINANCEIRA, 6)`. | Nulo com base nula, zero ou negativa. |
| 48 | `PC_SAI_NAO_ESS` | `DECIMAL(9,6)` | Não | `ROUND(VL_SAI_NAO_ESS / BASE_FINANCEIRA, 6)`. | Nulo com base nula, zero ou negativa. |
| 49 | `PC_SAI_FUT` | `DECIMAL(9,6)` | Não | `ROUND(VL_SAI_FUT / BASE_FINANCEIRA, 6)`. | Nulo com base nula, zero ou negativa. |
| 50 | `PC_SAI_OBR` | `DECIMAL(9,6)` | Não | `ROUND(VL_SAI_OBR / BASE_FINANCEIRA, 6)`. | Nulo com base nula, zero ou negativa. |

### 14.12 Percentuais de referência — atributos 51 a 55

| # | Atributo | Tipo | Obrigatório | Origem, significado e dependências | Regra de nulidade |
|---:|---|---|---|---|---|
| 51 | `PC_REF_IND` | `DECIMAL(9,6)` | Sim | Constante `0.750000`. | Não pode ser nulo. |
| 52 | `PC_REF_ESS` | `DECIMAL(9,6)` | Sim | Constante `0.500000`. | Não pode ser nulo. |
| 53 | `PC_REF_NAO_ESS` | `DECIMAL(9,6)` | Sim | Constante `0.300000`. | Não pode ser nulo. |
| 54 | `PC_REF_FUT` | `DECIMAL(9,6)` | Sim | Constante `0.200000`. | Não pode ser nulo. |
| 55 | `PC_REF_OBR` | `DECIMAL(9,6)` | Sim | Constante `0.300000`. | Não pode ser nulo. |

### 14.13 Pontuação de concentração — atributos 56 a 60

| # | Atributo | Tipo | Obrigatório | Origem, significado e dependências | Regra de nulidade |
|---:|---|---|---|---|---|
| 56 | `NR_PONT_CONC_IND` | `INT` | Não | Matriz IND; 99 acima de 75%, zero nos demais casos calculáveis. | Nulo sem transações ou com base nula; zero com base não positiva. |
| 57 | `NR_PONT_CONC_ESS` | `INT` | Não | Matriz ESS de 0 a 2 pontos. | Nulo sem transações ou com base nula; zero com base não positiva. |
| 58 | `NR_PONT_CONC_NAO_ESS` | `INT` | Não | Matriz Não Essenciais de 0 a 2 pontos. | Nulo sem transações ou com base nula; zero com base não positiva. |
| 59 | `NR_PONT_CONC_FUT` | `INT` | Não | Matriz Futuro de 0 a 2 pontos, com maior prioridade para menor percentual. | Nulo sem transações ou com base nula; zero com base não positiva. |
| 60 | `NR_PONT_CONC_OBR` | `INT` | Não | Matriz Obrigações de 0 a 2 pontos. | Nulo sem transações ou com base nula; zero com base não positiva. |

### 14.14 Pontuação orçamentária — atributos 61 a 65

| # | Atributo | Tipo | Obrigatório | Origem, significado e dependências | Regra de nulidade |
|---:|---|---|---|---|---|
| 61 | `NR_PONT_ORC_IND` | `INT` | Não | Sempre zero quando existem transações; não participa de `NR_PONT_IND_FIM`. | Nulo quando `QT_TRANS_TOTAL` é nulo ou zero. |
| 62 | `NR_PONT_ORC_ESS` | `INT` | Não | Matriz orçamentária ESS por `CD_FAIXA_ORC`. | Nulo sem transações ou sem faixa. |
| 63 | `NR_PONT_ORC_NAO_ESS` | `INT` | Não | Matriz orçamentária Não Essenciais por `CD_FAIXA_ORC`. | Nulo sem transações ou sem faixa. |
| 64 | `NR_PONT_ORC_FUT` | `INT` | Não | Matriz orçamentária Futuro por `CD_FAIXA_ORC`. | Nulo sem transações ou sem faixa. |
| 65 | `NR_PONT_ORC_OBR` | `INT` | Não | Matriz orçamentária Obrigações por `CD_FAIXA_ORC`. | Nulo sem transações ou sem faixa. |

### 14.15 Pontuação de perfil — atributos 66 a 70

| # | Atributo | Tipo | Obrigatório | Origem, significado e dependências | Regra de nulidade |
|---:|---|---|---|---|---|
| 66 | `NR_PONT_PRFL_IND` | `INT` | Não | Sempre zero quando existem transações; não participa de `NR_PONT_IND_FIM`. | Nulo quando `QT_TRANS_TOTAL` é nulo ou zero. |
| 67 | `NR_PONT_PRFL_ESS` | `INT` | Não | Matriz de macroperfil para ESS. | Nulo sem transações ou com macroperfil nulo/fora do domínio. |
| 68 | `NR_PONT_PRFL_NAO_ESS` | `INT` | Não | Matriz de macroperfil para Não Essenciais. | Nulo sem transações ou com macroperfil nulo/fora do domínio. |
| 69 | `NR_PONT_PRFL_FUT` | `INT` | Não | Matriz de macroperfil para Futuro. | Nulo sem transações ou com macroperfil nulo/fora do domínio. |
| 70 | `NR_PONT_PRFL_OBR` | `INT` | Não | Matriz de macroperfil para Obrigações. | Nulo sem transações ou com macroperfil nulo/fora do domínio. |

### 14.16 Pontuações finais — atributos 71 a 75

| # | Atributo | Tipo | Obrigatório | Origem, significado e dependências | Regra de nulidade |
|---:|---|---|---|---|---|
| 71 | `NR_PONT_IND_FIM` | `INT` | Não | Igual a `NR_PONT_CONC_IND`. | Nulo quando a concentração IND é nula. |
| 72 | `NR_PONT_ESS_FIM` | `INT` | Não | Concentração + orçamento + perfil de ESS. | Nulo se qualquer parcela é nula. |
| 73 | `NR_PONT_NAO_ESS_FIM` | `INT` | Não | Concentração + orçamento + perfil de Não Essenciais. | Nulo se qualquer parcela é nula. |
| 74 | `NR_PONT_FUT_FIM` | `INT` | Não | Concentração + orçamento + perfil de Futuro. | Nulo se qualquer parcela é nula. |
| 75 | `NR_PONT_OBR_FIM` | `INT` | Não | Concentração + orçamento + perfil de Obrigações. | Nulo se qualquer parcela é nula. |

### 14.17 Fechamento — atributos 76 a 80

| # | Atributo | Tipo | Obrigatório | Origem, significado e dependências | Regra de nulidade |
|---:|---|---|---|---|---|
| 76 | `FL_PONTUACAO_COMPLETA` | `STRING` | Sim | `S` se as cinco finais são não nulas; `N` caso contrário. | Não pode ser nula. |
| 77 | `NR_PONT_MAX` | `INT` | Não | Maior valor entre as cinco pontuações finais. | Nulo quando `FL_PONTUACAO_COMPLETA = 'N'`. |
| 78 | `QT_TEMAS_PONT_MAX` | `INT` | Não | Quantidade de temas cuja pontuação final é igual ao máximo. | Nulo quando a pontuação está incompleta. |
| 79 | `CD_TEMA_VENCEDOR` | `INT` | Não | Código 1 a 5 para máximo único; código 9 para empate. | Nulo quando a pontuação está incompleta. |
| 80 | `TX_TEMA_VENCEDOR` | `STRING` | Não | Nome do tema único ou `Empate`. | Nulo quando a pontuação está incompleta. |

### 14.18 Atributos obrigatórios

Os 12 valores obrigatoriamente não nulos são:

1. `CD_CLI`;
2. `DT_EXEA`;
3. `DT_MES_EXEA`;
4. `TS_INCL_TRAN_REF`;
5. `FL_CPF_UNICO`;
6. `FL_CONTA_ELEGIVEL_UNICA`;
7. `PC_REF_IND`;
8. `PC_REF_ESS`;
9. `PC_REF_NAO_ESS`;
10. `PC_REF_FUT`;
11. `PC_REF_OBR`;
12. `FL_PONTUACAO_COMPLETA`.

## 15. Resumo executivo do contrato

| Assunto | Regra consolidada |
|---|---|
| Cliente | `CD_CLI` informado, localizado por CPF ou escolhido aleatoriamente entre os elegíveis. |
| Formação | Transação realizada de pessoa física no mês-calendário anterior à execução. |
| Período | De um a seis ciclos financeiros fechados. |
| Conta | Exatamente uma conta candidata e normalizável para agência INT32 e conta DECIMAL(11,0). |
| Renda | Registro de maior data para CPF único, multiplicado por `periodo`. |
| Perfil | Única linha na maior data menor ou igual à execução. |
| Movimentos | Créditos e débitos visíveis realizados, na janela ampliada em cinco dias. |
| Reconciliação | Pares exatos primeiro; pares de borda no resíduo; nenhum ID pode ser reutilizado. |
| Moeda | Somente BRL alimenta o motor financeiro. |
| Classificação | Chave categoria + natureza; linha não classificada permanece, mas fica fora das somas. |
| Orçamento | Entradas e saídas marcadas para orçamento, sem alteração do sinal de `VL_TRAN`. |
| Base oficial | Renda presumida nos percentuais; entradas orçamentárias realizadas no orçamento. |
| Cenários | Renda presumida ou créditos efetivos classificados em BRL como base única do recálculo. |
| Pontuação | Concentração + orçamento + perfil, exceto IND, que usa somente concentração. |
| Fechamento | Máximo único gera tema; máximos múltiplos geram empate; parcela nula gera incompletude. |
| Resultado | Uma linha, 80 atributos, 12 valores obrigatórios. |
