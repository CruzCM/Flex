# Radar Financeiro — Fala Negocial

## Bloco 1 — Abertura e Enquadramento

“Boa tarde, pessoal.

O objetivo de hoje é mostrar, de forma simples, **como o Radar escolhe os clientes e como chega ao tema financeiro mais adequado para cada um deles**.

Os cinco públicos que o Radar trabalha já foram apresentados anteriormente. Hoje, o que queremos validar são as **regras que levam cada cliente até um desses públicos**.

Tecnicamente, o Radar funciona como uma esteira de dados com regras previamente definidas, sem decisão subjetiva durante o processamento (`ETL determinístico de público-alvo`).

Vamos percorrer essa jornada na mesma ordem em que o cliente é analisado: primeiro verificamos quem pode participar, depois entendemos sua renda e seu comportamento financeiro, organizamos suas movimentações e, por fim, aplicamos as regras que definem o tema mais adequado.

Em cada etapa, eu vou trazer exemplos práticos para ficar claro **quem entra, quem sai e por quê**.”

---

# Bloco 2 — Quem pode entrar no Radar?

“O primeiro passo é definir quem está apto a participar.

Temos algumas regras de entrada bastante objetivas.

A primeira é a **moeda**.

Se o cliente tiver qualquer movimentação em moeda estrangeira, ele não participa do Radar.

Não descartamos apenas aquela compra em dólar ou euro. Nesse caso, o cliente inteiro fica fora da análise.

Tecnicamente, o cliente só permanece se todas as movimentações consideradas estiverem em Real (`CD_TIP_MOE_CRR = 'BRL'`; `FL_SOMENTE_BRL = 'S'`).

A razão é simples: o Radar foi desenhado para analisar uma vida financeira movimentada integralmente em reais.

A segunda regra é relacionada ao **público agro**.

Se identificarmos movimentações características da atividade rural, esse cliente também fica fora.

Tecnicamente, a presença de qualquer movimentação classificada como Agro sinaliza a exclusão (`FL_TEM_MOV_AGRO = 'S'`).

Isso acontece porque o fluxo financeiro de um produtor rural é muito diferente do fluxo de uma pessoa que recebe e gasta mensalmente.

O produtor pode ter meses de grandes despesas com insumos e depois receber a receita apenas na época da safra. Avaliar esse comportamento com uma lógica mensal poderia gerar orientações erradas.

Por isso, entendemos que o público agro precisa de uma abordagem própria.

Também consideramos apenas movimentações válidas e de pessoa física (`CD_EST_TRAN_INST = 0`; `CD_TIP_PSS = 1`).

E temos uma regra de bom senso fundamental: **o cliente precisa ter utilizado o aplicativo no período definido para entrada no Radar**.

Por que essa regra existe?

Porque a orientação do Radar é entregue dentro do próprio aplicativo. Então não faz sentido gastar processamento gerando um diagnóstico para alguém que não utiliza o canal onde esse conteúdo será apresentado.

Mas aqui existe um ponto importante, que costuma gerar dúvida:

**nós não olhamos apenas para a data em que o cliente fez uma compra ou passou o cartão.**

A data da movimentação é uma informação (`DT_TRAN`), mas, para essa regra de entrada, utilizamos a data de inclusão da transação no ambiente do Gestor Financeiro Pessoal (`TS_INCL_TRAN`).

Na lógica do Radar, essa informação funciona como evidência de atualização associada ao uso do aplicativo.

Na prática, isso permite separar duas coisas diferentes: o cliente pode continuar movimentando a conta normalmente e, mesmo assim, não estar utilizando o aplicativo.”

### Exemplo 1 — Compra em moeda estrangeira

“Imaginem um cliente que fez 25 movimentações normais em reais, somando R$ 4.200, mas também realizou uma compra de apenas 12 dólares.

Mesmo sendo uma compra pequena, a regra atual é objetiva:

**esse cliente não participa do Radar**, porque possui movimentação em moeda estrangeira.

Tecnicamente, essa movimentação faz a regra de moeda falhar (`CD_TIP_MOE_CRR = 'USD'`; `FL_SOMENTE_BRL = 'N'`).”

### Exemplo 2 — Movimentação Agro

“Agora imaginem um cliente que normalmente compra supermercado e combustível, mas também realizou uma compra de R$ 800 em insumos agrícolas.

Essa movimentação caracteriza atividade agro.

Nesse caso, o cliente também deixa o Radar, porque seu comportamento financeiro precisa ser analisado com uma lógica específica para a atividade rural.

Tecnicamente, a categorização Agro aciona a sinalização de exclusão (`FL_TEM_MOV_AGRO = 'S'`).”

### Exemplo 3 — O cliente movimenta a conta, mas não abre o app

“Imaginem este caso:

Hoje é **15 de setembro** e estamos rodando o Radar.

O cliente passou o cartão na padaria no dia **20 de agosto**. Portanto, sabemos que ele continuou movimentando normalmente a conta (`DT_TRAN = 20/08`).

Porém, a última atualização associada ao uso do aplicativo ocorreu no dia **10 de maio** (`TS_INCL_TRAN = 10/05`).

Se olhássemos apenas para a data da compra (`DT_TRAN`), esse cliente pareceria ativo e entraria no Radar.

Mas a nossa regra de entrada utiliza a informação associada ao uso do aplicativo (`TS_INCL_TRAN`) dentro da janela definida.

Como isso não aconteceu, ele não entra no processamento.

A lógica é simples:

**geramos conteúdo para quem efetivamente utiliza o canal onde esse conteúdo será entregue.**”

### O que precisamos validar aqui?

“Então, neste primeiro ponto, precisamos confirmar duas decisões:

A exclusão completa de clientes com moeda estrangeira ou movimentações agro continua sendo a regra (`FL_SOMENTE_BRL = 'N'` ou `FL_TEM_MOV_AGRO = 'S'`)?

E o uso recente do aplicativo continua sendo nossa porta de entrada para o Radar (`TS_INCL_TRAN`)?”

---

# Bloco 3 — Identificação, conta e renda

“Depois que o cliente passa pela primeira etapa, precisamos garantir que conseguimos identificar corretamente sua **conta, seu CPF e sua renda**.

O Radar precisa dessas informações porque elas permitem construir corretamente o período financeiro que será analisado e localizar a renda utilizada como referência.

Para a conta, a regra atual exige que exista **uma única conta válida** para o cliente.

Tecnicamente, buscamos uma conta corrente elegível do Banco do Brasil (`NR_MCA_PCT_OPB = 999999999`; `CD_PRD = 6`) com agência e conta válidas (`NR_AG_TITR`; `CD_CT_TITR`).

Isso evita que o sistema escolha arbitrariamente entre duas contas diferentes e utilize um ciclo financeiro que talvez não represente corretamente aquele cliente.

Também precisamos de um **CPF válido e único** (`NR_CPF_CNPJ_TITR`), porque é por meio dele que localizamos a renda presumida.

A conta é utilizada para localizar o ciclo financeiro (`DB2GFP.CT_GRDR_FNCO`; `CD_UOR_CC`; `NR_CC`).

O CPF é utilizado para localizar a renda (`DB2DFE.REN_AVLD_PF`; `NR_CPF_BASE_SRF`).

E aqui existe uma regra importante:

**a renda presumida é obrigatória.**

Se não conseguimos localizar essa renda, o cliente não continua no Radar (`VL_REN_PRES`).

Isso acontece porque a renda é nossa referência para avaliar se determinado nível de gasto é baixo, adequado ou elevado.”

### Exemplo — Cliente sem renda

“Imaginem um cliente que utiliza o aplicativo, tem conta válida e CPF identificado, mas não possui renda disponível na nossa base.

A consulta de renda não encontra registro para esse CPF (`DB2DFE.REN_AVLD_PF`).

Mesmo com todas as outras informações corretas, ele fica fora do Radar.

Sem uma referência de renda (`VL_REN_PRES`), não conseguimos avaliar de forma segura quanto os gastos representam da capacidade financeira daquele cliente.”

### Exemplo — Cliente com duas contas

“Agora imaginem um cliente com duas contas igualmente válidas.

Hoje, o Radar não escolhe uma delas no palpite.

Tecnicamente, a regra exige exatamente uma conta elegível (`FL_CONTA_ELEGIVEL_UNICA = 'S'`).

Quando existem duas contas candidatas, essa condição deixa de ser atendida (`FL_CONTA_ELEGIVEL_UNICA = 'N'`; `DD_INC_MM_CLC_BLC = 996`).

Sem uma regra que determine qual conta deve prevalecer, o processamento é interrompido para aquele cliente.”

### O que precisamos validar?

“Aqui temos duas decisões.

Continuamos excluindo os casos em que não conseguimos identificar CPF e renda de forma segura (`NR_CPF_CNPJ_TITR`; `VL_REN_PRES`)?

E, quando o cliente possui mais de uma conta válida, continuamos sem processá-lo ou queremos definir uma regra para escolher uma dessas contas (`FL_CONTA_ELEGIVEL_UNICA`)?”

---

# Bloco 4 — Qual período financeiro vamos analisar?

“Depois de identificar a conta correta, precisamos definir **qual período representa o mês financeiro daquele cliente**.

Nem todo cliente necessariamente tem seu ciclo começando no dia primeiro.

Por isso, quando temos a informação do ciclo financeiro, utilizamos o dia específico daquele cliente (`DB2GFP.CT_GRDR_FNCO`; `DD_INC_MM_CLC_BLC`).

Se houver mais de uma informação histórica de ciclo, utilizamos a mais recente (`TS_ULT_EXEA_PSQ`).

Mas aqui existe uma diferença importante em relação às regras anteriores.

**A falta dessa informação não exclui o cliente.**

Se não encontramos o dia do ciclo, utilizamos o dia primeiro como referência e seguimos normalmente (`DD_INC_MM_CLC_BLC_FALLBACK = 1`).

Ou seja, essa é uma regra de inclusão, não de exclusão.

Outra decisão importante é que o Radar trabalha somente com **períodos financeiros completamente encerrados** (`DT_REF_INI`; `DT_REF_FIM`).

E um exemplo deixa essa regra mais fácil de visualizar.”

### Exemplo — Por que usamos somente ciclos fechados?

“Imaginem que hoje seja **15 de setembro** e que o ciclo financeiro desse cliente comece todo dia **20** (`DD_INC_MM_CLC_BLC = 20`).

O ciclo atual começou em **20 de agosto** e ainda está acontecendo.

Se utilizássemos esse período até 15 de setembro, analisaríamos um ciclo incompleto.

Parte das despesas que normalmente aconteceriam até o fechamento ainda nem ocorreu.

Isso poderia fazer o cliente parecer gastar menos do que realmente gasta e distorcer o diagnóstico.

Por isso, o Radar dá um passo para trás e utiliza o último ciclo totalmente encerrado:

**de 20 de julho a 19 de agosto** (`DT_REF_INI = 20/07`; `DT_REF_FIM = 19/08`).

Assim, comparamos períodos completos e evitamos tomar decisões com base em um mês ainda em andamento.”

### Exemplo — Cliente sem dia de ciclo

“E existe ainda a nossa regra inclusiva.

Se esse cliente não tiver um dia de ciclo cadastrado (`DD_INC_MM_CLC_BLC` ausente), ele **não é excluído**.

Adotamos o dia primeiro como referência (`DD_INC_MM_CLC_BLC_FALLBACK = 1`).

Nesse mesmo exemplo, estando em 15 de setembro, analisaríamos o último mês completamente encerrado:

**de 1º de agosto a 31 de agosto** (`DT_REF_INI = 01/08`; `DT_REF_FIM = 31/08`).

O cliente permanece no Radar e o cálculo segue normalmente.”

### O que precisamos validar?

“O uso do dia primeiro quando não encontramos o ciclo está aprovado (`DD_INC_MM_CLC_BLC_FALLBACK = 1`)?

E mantemos a decisão de trabalhar somente com períodos financeiros completamente encerrados (`DT_REF_INI`; `DT_REF_FIM`)?”

---

# Bloco 5 — Renda e perfil financeiro

“Com o período definido, precisamos de duas informações importantes para entender o cliente: **a renda e o perfil financeiro**.

A renda, como vimos, é obrigatória.

Ela é localizada pelo CPF na base corporativa de renda (`DB2DFE.REN_AVLD_PF`; `NR_CPF_BASE_SRF`) e utilizamos o registro mais recente disponível (`DT_INCL_REN_AVLD`; `VL_REN`).

Quando analisamos mais de um ciclo financeiro, ajustamos essa renda para o mesmo período.

Por exemplo: se estamos olhando dois meses, trabalhamos com a renda correspondente aos dois meses (`VL_REN_PRES = VL_REN × quantidade de ciclos`).

Além disso, utilizamos o **perfil financeiro histórico do cliente**.

Esse perfil é localizado na base corporativa de perfil (`DB2D1D.DVS_GRDR_FNCO_PF`) e utilizamos o registro vigente mais recente (`DT_REF <= DT_EXEA`).

Hoje trabalhamos com três grandes perfis:

**Endividado** (`CD_MAC_PRFL_CLI = 1`);

**Equilibrista** (`CD_MAC_PRFL_CLI = 2`);

**Investidor** (`CD_MAC_PRFL_CLI = 3`).

Esse perfil nos ajuda a complementar aquilo que estamos observando nas movimentações recentes.

E, pela regra atual, o perfil também é obrigatório.

Se não conseguimos identificar um desses três perfis, o cliente não continua no Radar (`CD_MAC_PRFL_CLI` nulo ou diferente de `1`, `2` ou `3`).

A razão é que esse histórico faz parte da pontuação que determina qual orientação será entregue.”

### Exemplo — Cliente sem perfil financeiro

“Imaginem um cliente com conta válida, renda de R$ 7 mil e movimentação normal.

Porém, não conseguimos identificar seu perfil financeiro histórico.

Tecnicamente, a consulta à base de perfil não encontra um macroperfil válido (`DB2D1D.DVS_GRDR_FNCO_PF`; `CD_MAC_PRFL_CLI`).

Mesmo tendo renda e movimentação, ele fica fora do Radar porque faltaria uma das informações utilizadas para determinar o tema mais adequado.”

### O que precisamos validar?

“Precisamos confirmar três pontos:

O perfil financeiro continua sendo obrigatório (`CD_MAC_PRFL_CLI = 1, 2 ou 3`)?

Continuamos utilizando a renda mais recente disponível (`DT_INCL_REN_AVLD`)?

E, quando analisamos mais de um ciclo, continuamos ajustando a renda proporcionalmente à quantidade de ciclos (`VL_REN_PRES`)?”

---

# Bloco 6 — Evitando contar transferências como gasto

“Agora entramos nas movimentações financeiras propriamente ditas.

Aqui existe um cuidado muito importante.

O Radar precisa diferenciar **um gasto real de uma simples transferência de dinheiro entre contas do próprio cliente**.

Para essa etapa, buscamos movimentações em uma janela ampliada de cinco dias antes e cinco dias depois do período oficial (`DT_TRAN BETWEEN DT_REF_INI - 5 dias AND DT_REF_FIM + 5 dias`).

Consideramos movimentações ativas (`CD_EST_TRAN_INST = 0`), distinguimos créditos e débitos (`CD_NTZ_CTB_TRAN = 'C'` ou `'D'`) e, para os débitos, exigimos a indicação de consumo (`IN_VSLO_CSM = 'S'`).

Imaginem que eu transfira R$ 2 mil da minha conta no Banco do Brasil para minha conta em outro banco.

Eu não fiquei R$ 2 mil mais pobre e também não ganhei R$ 2 mil.

Eu apenas movi o dinheiro de lugar.

Se contássemos isso como renda e despesa, estaríamos distorcendo completamente a vida financeira do cliente.

Por isso, o Radar procura movimentações equivalentes — mesmo cliente, mesmo valor, mesma moeda, datas compatíveis, naturezas opostas e instituições diferentes (`CD_CLI`; `VL_TRAN`; `CD_TIP_MOE_CRR`; `DT_TRAN`; `CD_NTZ_CTB_TRAN`).

Quando as duas movimentações acontecem na mesma data e atendem às condições, tratamos como **par exato**.

Quando uma delas está dentro da janela e a correspondente aparece até cinco dias fora dela, tratamos como **par de borda**.

Depois dessa limpeza, ficam somente as movimentações que realmente devem participar da análise.”

### Exemplo — Transferência entre contas próprias

“Um cliente transfere R$ 1.500 do Banco do Brasil para sua própria conta no Nubank.

Temos uma saída de R$ 1.500 em um banco (`CD_NTZ_CTB_TRAN = 'D'`; `VL_TRAN = 1500`) e uma entrada do mesmo valor no outro (`CD_NTZ_CTB_TRAN = 'C'`; `VL_TRAN = 1500`).

O Radar identifica que essas duas movimentações representam apenas uma transferência entre contas e retira ambas do cálculo.

Assim, o orçamento do cliente não fica artificialmente inflado.”

### O que precisamos validar?

“A margem de até cinco dias é suficiente para acomodar diferenças causadas por fins de semana e feriados (`±5 dias`)?

E a regra utilizada para identificar quais débitos representam efetivamente consumo continua adequada (`IN_VSLO_CSM = 'S'`)?”

---

# Bloco 7 — Organizando os gastos

“Depois de eliminar essas distorções, organizamos as movimentações do cliente.

Cada movimentação é comparada com nosso mapa de categorias (`CD_CTGR_TRAN_OGNL`; `CD_NTZ_CTB_TRAN`).

Esse mapa também define se a movimentação participa dos cálculos (`IN_PARTICIPA_CALCULO = 'S'`) e se participa do orçamento (`IN_PARTICIPA_ORCAMENTO = 'S'`).

De forma simplificada, queremos entender quanto do dinheiro está indo para grupos como:

**despesas essenciais**, como mercado, água, luz e farmácia (`VL_SAI_ESS`);

**despesas não essenciais**, como lazer, restaurantes, streaming e vestuário (`VL_SAI_NAO_ESS`);

**formação de futuro**, como poupança e investimentos (`VL_SAI_FUT`);

**obrigações financeiras**, como parcelas, empréstimos e faturas (`VL_SAI_OBR`);

e despesas que ainda **não conseguimos classificar** (`VL_SAI_IND`).

Também calculamos o total de entradas (`VL_ENT_TOTAL`) e o total de saídas (`VL_SAI_TOTAL`).

Com isso, calculamos o resultado do orçamento (`VL_RES_ORC = VL_ENT_TOTAL - VL_SAI_TOTAL`) e quanto as saídas representam das entradas (`PC_SAI_ENT = VL_SAI_TOTAL / VL_ENT_TOTAL`).

A partir disso, classificamos a situação financeira do período em cinco faixas (`CD_FAIXA_ORC`):

**Equilibrado**: saídas entre 95% e 105% das entradas (`CD_FAIXA_ORC = 0`);

**Déficit moderado**: saídas entre 105% e 125% (`CD_FAIXA_ORC = 1`);

**Déficit acentuado**: saídas acima de 125% (`CD_FAIXA_ORC = 2`);

**Superávit moderado**: saídas entre 75% e 95% (`CD_FAIXA_ORC = 3`);

**Superávit acentuado**: saídas abaixo de 75% (`CD_FAIXA_ORC = 4`).

Em termos simples, queremos saber se o cliente **gastou aproximadamente o que recebeu, gastou mais ou conseguiu gastar menos e gerar sobra**.”

### O que precisamos validar?

“As faixas utilizadas para determinar equilíbrio, déficit e superávit continuam adequadas (`75%`, `95%`, `105%` e `125%`)?

E movimentações que não conseguimos mapear devem continuar visíveis para acompanhamento, mas sem interferir no cálculo (`IN_PARTICIPA_CALCULO = 'N'`; `IN_PARTICIPA_ORCAMENTO = 'N'`)?”

---

# Bloco 8 — Como o Radar escolhe o tema do cliente?

“Agora chegamos ao coração do Radar.

Depois de organizar todas essas informações, precisamos responder:

**qual é o principal tema financeiro sobre o qual faz sentido conversar com esse cliente agora?**

O Radar considera três tipos de informação.

Primeiro, observa **onde o cliente está concentrando seus gastos** (`NR_PONT_CONC_*`).

Por exemplo, quanto da renda está comprometido com despesas essenciais (`PC_SAI_ESS`), gastos não essenciais (`PC_SAI_NAO_ESS`), obrigações e crédito (`PC_SAI_OBR`) ou formação de reserva (`PC_SAI_FUT`).

Segundo, considera **a situação geral do orçamento** (`NR_PONT_ORC_*`; `CD_FAIXA_ORC`).

O cliente está no vermelho?

Está equilibrado?

Ou possui uma boa sobra financeira?

Terceiro, utilizamos o **perfil financeiro histórico** que vimos anteriormente (`NR_PONT_PRFL_*`; `CD_MAC_PRFL_CLI`).

Essas três informações são combinadas e cada tema recebe uma pontuação.

Ao final, identificamos a maior pontuação (`NR_PONT_MAX`) e o tema correspondente (`CD_TEMA_VENCEDOR`).”

## Público 1 — Categorização dos Gastos

“Existe uma exceção importante.

Se mais de **75% das despesas do cliente não puderem ser classificadas**, não faz sentido dizer para ele que precisa investir mais, gastar menos com lazer ou reorganizar suas dívidas.

Tecnicamente, quando as despesas indeterminadas ultrapassam 75% (`PC_SAI_IND > 0.75`), a pontuação de exceção recebe o valor máximo (`NR_PONT_CONC_IND = 99`).

Primeiro precisamos ajudá-lo a entender **para onde o dinheiro está indo**.

Por isso, nesse caso, Categorização dos Gastos vira automaticamente a prioridade (`CD_TEMA_VENCEDOR = 1`).”

### Exemplo

“Um cliente gastou R$ 4 mil e R$ 3.200 desse valor não pôde ser classificado (`VL_SAI_IND = R$ 3.200`).

Isso significa que **80% dos gastos** estão sem identificação adequada (`PC_SAI_IND = 80%`).

Como ultrapassou os 75%, a regra especial é acionada (`NR_PONT_CONC_IND = 99`).

Nesse caso, a prioridade é Categorização dos Gastos (`CD_TEMA_VENCEDOR = 1`).”

---

## Público 2 — Gestão de Orçamento

“Esse tema aparece quando os sinais mostram dificuldade para equilibrar receitas e despesas, principalmente quando existe peso elevado de gastos essenciais.

Tecnicamente, o tema de Gestão de Orçamento recebe pontuação pela concentração de essenciais, pela situação orçamentária e pelo perfil (`NR_PONT_CONC_ESS`; `NR_PONT_ORC_ESS`; `NR_PONT_PRFL_ESS`).”

### Exemplo

“Um cliente com renda de R$ 4 mil gastou R$ 4.600 e comprometeu 65% da renda com despesas essenciais (`PC_SAI_ESS = 65%`).

A combinação desses fatores leva o Radar para **Gestão de Orçamento** (`CD_TEMA_VENCEDOR = 2`).”

---

## Público 3 — Consumo Planejado

“Aqui o foco está principalmente nos gastos mais flexíveis, aqueles sobre os quais normalmente existe maior possibilidade de escolha.

Tecnicamente, avaliamos principalmente a concentração de gastos não essenciais (`PC_SAI_NAO_ESS`) combinada com orçamento e perfil.”

### Exemplo

“Um cliente com renda de R$ 6 mil possui suas despesas básicas relativamente controladas, mas utiliza mais de 43% da renda em lazer, restaurantes, delivery, streaming e outras despesas não essenciais (`PC_SAI_NAO_ESS ≈ 43,3%`).

Nesse caso, o Radar entende que o tema mais adequado é **Consumo Planejado** (`CD_TEMA_VENCEDOR = 3`).”

---

## Público 4 — Formação de Reserva

“Esse público representa clientes que apresentam capacidade financeira para guardar mais dinheiro, mas ainda transformam pouco dessa capacidade em reserva ou investimento.

Aqui a lógica da concentração é invertida: quanto menor a parcela direcionada ao futuro, maior a necessidade de orientação (`PC_SAI_FUT`).”

### Exemplo

“Um cliente com renda de R$ 8 mil gastou apenas R$ 5.200.

Isso significa que as saídas representam 65% das entradas, caracterizando uma sobra expressiva (`CD_FAIXA_ORC = 4`).

Mesmo assim, ele guardou apenas R$ 600 (`PC_SAI_FUT = 7,5%`).

Nesse caso, o Radar identifica uma oportunidade de trabalhar **Formação de Reserva** (`CD_TEMA_VENCEDOR = 4`).”

---

## Público 5 — Uso Consciente do Crédito

“Aqui observamos principalmente o peso das dívidas, parcelas, empréstimos e faturas na renda do cliente (`PC_SAI_OBR`).”

### Exemplo

“Um cliente com renda de R$ 5 mil possui R$ 2.300 comprometidos com cartão e empréstimos.

Isso representa **46% da renda** (`PC_SAI_OBR = 46%`).

Somado ao restante da situação financeira e ao seu histórico, o Radar pode indicar **Uso Consciente do Crédito** como prioridade (`CD_TEMA_VENCEDOR = 5`).”

---

## E se houver empate?

“Pode acontecer de dois temas terminarem com exatamente a mesma pontuação.

Quando isso ocorre, o Radar **não escolhe arbitrariamente**.

Ele identifica que mais de um tema atingiu a pontuação máxima (`QT_TEMAS_PONT_MAX > 1`) e registra o empate (`CD_TEMA_VENCEDOR = 9`).

A partir daí, precisamos definir qual regra negocial queremos utilizar para decidir o tema que será levado ao cliente.”

### O que precisamos validar?

“Neste bloco, temos três decisões principais.

A prioridade automática para Categorização quando mais de 75% dos gastos estiverem sem classificação continua adequada (`PC_SAI_IND > 0.75`; `NR_PONT_CONC_IND = 99`)?

Os pesos utilizados para combinar comportamento atual, orçamento e perfil histórico estão coerentes (`NR_PONT_CONC_*`; `NR_PONT_ORC_*`; `NR_PONT_PRFL_*`)?

E qual deve ser nossa regra quando dois ou mais temas terminarem empatados (`CD_TEMA_VENCEDOR = 9`)?”

---

# Bloco 9 — Três maneiras de olhar o mesmo cliente

“Além do resultado principal, o Radar também entrega duas visões alternativas do mesmo cliente.

Esses resultados são gravados na base final do Radar (`ANA_RADAR_FIN_CLI`).

A ideia é permitir que o negócio compare diferentes formas de interpretar sua situação financeira.

Na **visão oficial**, combinamos aquilo que efetivamente entrou na conta com a renda presumida, cada informação sendo utilizada na parte do cálculo para a qual foi definida.

Na segunda visão, utilizamos a **renda presumida como principal referência** (`_RENDA_PRESUMIDA`).

É uma forma de olhar para a **capacidade financeira estimada** do cliente.

Na terceira, utilizamos apenas as **entradas que efetivamente identificamos nas movimentações** (`_ENTRADAS_REALIZADAS`).

É uma visão mais próxima do **caixa realizado**.

Assim, conseguimos comparar as três leituras sem precisar reconstruir todo o processamento.”

---

# Bloco 10 — Encerramento e decisões da mesa

“Para encerrar, o mais importante é entender que o Radar segue um conjunto claro de regras.

Nós conseguimos explicar por que um cliente entrou ou não entrou na análise e também quais informações fizeram determinado tema ser escolhido.

Hoje precisamos sair daqui com a validação das principais decisões de negócio.

São elas:

1. Cliente com qualquer movimentação em moeda estrangeira fica fora do Radar (`FL_SOMENTE_BRL = 'N'`).

2. Cliente com movimentação Agro fica fora e deve ser tratado em uma solução específica (`FL_TEM_MOV_AGRO = 'S'`).

3. O uso recente do aplicativo continua sendo a porta de entrada para o público (`TS_INCL_TRAN`).

4. Precisamos identificar de forma segura uma conta e um CPF para seguir com a análise (`NR_AG_TITR`; `CD_CT_TITR`; `NR_CPF_CNPJ_TITR`).

5. Quando não encontramos o ciclo financeiro, utilizamos o dia primeiro e mantemos o cliente (`DD_INC_MM_CLC_BLC_FALLBACK = 1`).

6. Trabalhamos somente com períodos financeiros já encerrados (`DT_REF_INI`; `DT_REF_FIM`).

7. A renda presumida continua sendo obrigatória (`VL_REN_PRES`; `DB2DFE.REN_AVLD_PF`).

8. O perfil financeiro também continua sendo obrigatório (`CD_MAC_PRFL_CLI = 1, 2 ou 3`; `DB2D1D.DVS_GRDR_FNCO_PF`).

9. Transferências entre contas próprias devem ser retiradas do cálculo, considerando a margem de até cinco dias (`±5 dias`; `DT_TRAN`; `VL_TRAN`; `CD_NTZ_CTB_TRAN`).

10. Mantemos as faixas atuais para identificar equilíbrio, déficit e superávit (`CD_FAIXA_ORC`; `75%`, `95%`, `105%` e `125%`).

11. Quando mais de 75% dos gastos estiverem sem classificação, Categorização dos Gastos se torna prioridade (`PC_SAI_IND > 0.75`; `NR_PONT_CONC_IND = 99`).

12. Mantemos os pesos atualmente utilizados para os três perfis financeiros (`CD_MAC_PRFL_CLI`; `NR_PONT_PRFL_*`).

13. Precisamos definir qual tratamento será utilizado quando houver empate entre dois ou mais temas (`QT_TEMAS_PONT_MAX > 1`; `CD_TEMA_VENCEDOR = 9`).

Para cada um desses pontos, a decisão da mesa pode ser:

**Aprovado, Alterar ou Investigar.**

Com essas definições homologadas, conseguimos fechar as regras negociais do Radar e garantir que aquilo que será implementado tecnicamente representa exatamente o que o negócio espera entregar ao cliente.

Muito obrigado.

Agora podemos passar ponto a ponto pelas decisões.”
