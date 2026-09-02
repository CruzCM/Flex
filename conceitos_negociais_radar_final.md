# Radar Financeiro — Moeda, Valores, Orçamento, Prioridades e Cenários

## 1. Propósito e fronteiras

Este documento conclui a definição semântica do Radar Financeiro. Ele explica, em linguagem de negócio:

- cobertura monetária e contexto Agro;
- volumetria e valores financeiros;
- orçamento da visão principal;
- percentuais e parâmetros de referência;
- três dimensões de prioridade;
- prioridade final, completude, empate e vencedor;
- cenários financeiros;
- estados especiais que precisam ser explicados;
- hierarquia recomendada para a narrativa do produto.

As fórmulas e os estados descritos são os efetivamente reconhecidos pelo contrato. Quando o efeito de um parâmetro é conhecido, mas sua justificativa de origem não está documentada, o efeito é explicado e a origem permanece explicitamente não definida.

## 2. Situação da exigência de bancos diferentes

### 2.1 Classificação correta da decisão

A exigência de que uma transferência própria possua dois códigos de banco conhecidos e diferentes não está presente no contrato funcional consolidado nem nas chaves de reconciliação executadas pelo motor.

A condição foi explicitada e aprovada durante a entrevista semântica do negócio. Portanto, com as evidências disponíveis, sua classificação correta é:

> **Nova decisão negocial aprovada, com implementação pendente.**

Não existe evidência documental suficiente para afirmar que essa condição sempre fez parte da regra e foi acidentalmente omitida. Por isso, ela não deve ser registrada retroativamente como bug contra uma regra preexistente.

A autorização negocial disponível é a decisão expressa de que:

- as contas observadas pertencem ao cliente;
- uma transferência própria precisa ocorrer entre bancos diferentes;
- entrada e saída no mesmo banco não formam transferência própria;
- banco nulo não comprova bancos diferentes;
- a condição deve valer para pares exatos e de borda.

A partir dessa aprovação, o processamento existente deixa de estar aderente ao estado negocial desejado. A forma precisa de registrar a situação é:

```text
Tipo: decisão negocial nova
Status: aprovada
Implementação: pendente
Criticidade: alta
Comportamento atual: ainda não aderente à decisão aprovada
```

Se surgir uma fonte negocial anterior e formal que demonstre que bancos diferentes já eram obrigatórios, a classificação poderá ser revisada para bug ou não aderência histórica. Sem essa evidência, essa afirmação não é autorizada.

## 3. K — Cobertura monetária

### 3.1 `FL_SOMENTE_BRL`

**Nome humano recomendado:** Somente BRL entre as moedas identificadas.

Esse rótulo é mais preciso do que “Somente movimentações em reais”, porque moedas nulas não contam na distinção de moedas.

`FL_SOMENTE_BRL = 'S'` significa que:

- existe pelo menos uma movimentação efetiva;
- entre as moedas não nulas observadas, existe exatamente uma moeda distinta;
- essa moeda é BRL.

Movimentações com moeda nula podem coexistir com BRL e a flag ainda ser `S`. Portanto, `S` não comprova que todas as linhas possuem moeda preenchida; comprova que nenhuma outra moeda identificada além de BRL foi encontrada.

`FL_SOMENTE_BRL = 'N'` significa que existe movimentação efetiva, mas o conjunto não atende à condição anterior. Isso inclui:

- BRL acompanhado de outra moeda identificada;
- somente moedas diferentes de BRL;
- somente moedas nulas.

`N` não é erro. É um contexto de cobertura e, quando há outra moeda, uma limitação de abrangência das métricas financeiras, que são calculadas somente em BRL.

Quando existem 100 movimentos em BRL e um em USD:

- o diagnóstico sobre os 100 movimentos em BRL continua válido;
- o diagnóstico não cobre 100% dos fatos financeiros observados;
- o movimento em USD continua sendo um fato real do cliente;
- o movimento em USD não entra nas somas porque não há conversão cambial.

A movimentação não BRL deve permanecer disponível no detalhe transacional, identificada como “fora das métricas em BRL”. É recomendável mostrar a lista das moedas observadas, além da flag, para que a pessoa saiba qual parte do universo ficou fora. Essa lista é explicativa e não integra os 80 atributos do resultado.

Quando só existem movimentações não BRL, a explicação humana é:

> Foram observadas movimentações financeiras, mas nenhuma em BRL. Como o Radar não realiza conversão cambial, as métricas financeiras e a priorização baseadas em reais não puderam ser calculadas.

Quando não existe nenhuma movimentação efetiva, `FL_SOMENTE_BRL` é nula. Nulo significa ausência de universo para avaliar a cobertura monetária, e não presença de moeda estrangeira.

## 4. K2 — Contexto Agro

### 4.1 `IN_AGRO`

Uma categoria é Agro quando o mapa de classificação atribui `IN_AGRO = 'S'`. O indicador pertence à categoria da movimentação, não ao cliente como um todo.

No conjunto reconhecido, a marca identifica receitas e despesas relacionadas a atividade rural ou agropecuária, como:

- Receitas Agro;
- Criações;
- Cultivos;
- Insumos;
- Apoio Produtivo.

O indicador não comprova que o cliente pertence a um segmento comercial Agro, possui relacionamento especializado ou exerce formalmente atividade rural. Ele informa somente que existe uma movimentação cuja categoria foi marcada como Agro.

`IN_AGRO` não altera diretamente orçamento, percentuais ou pontuações. Ele forma contexto e permite derivar a flag de presença Agro. A entrada de uma receita Agro na base `ENTRADAS_REALIZADAS` decorre da regra desse cenário, que soma créditos classificados em BRL sem aplicar flags de participação; não decorre da flag Agro em si.

### 4.2 `FL_TEM_MOV_AGRO`

**Nome humano recomendado:** Possui movimentação Agro em BRL.

`FL_TEM_MOV_AGRO = 'S'` significa que existe pelo menos uma movimentação efetiva em BRL cuja categoria está marcada como Agro.

`FL_TEM_MOV_AGRO = 'N'` significa que existem movimentações efetivas em BRL, mas nenhuma delas está marcada como Agro.

`FL_TEM_MOV_AGRO = NULL` significa que não existe movimentação efetiva em BRL sobre a qual a presença Agro possa ser avaliada.

A flag:

- não muda diretamente o diagnóstico;
- não adiciona nem remove pontuação;
- informa a existência de um contexto financeiro específico;
- ajuda a explicar por que determinadas categorias podem ter tratamento distinto de participação.

Ela é calculada sobre BRL porque descreve o mesmo universo monetário usado pelas métricas financeiras. Se existir Agro somente em moeda não BRL, a leitura correta é:

> Há movimentação Agro fora do universo em BRL, mas não há movimentação Agro nas métricas financeiras calculadas em reais.

Nesse estado, a flag permanece nula se não existir nenhuma linha BRL. A movimentação Agro não BRL deve continuar visível no detalhe de cobertura monetária.

## 5. L — Volumetria financeira

### 5.1 `QT_TRANS_TOTAL`

**Nome humano:** Quantidade de movimentações financeiras efetivas em BRL.

Esse nome preserva as três condições que já ocorreram antes da contagem:

- a movimentação pertence à janela oficial;
- sobreviveu à reconciliação;
- possui moeda BRL.

“Quantidade de transações” é um rótulo incompleto quando aparece sozinho, pois pode sugerir linhas brutas, externas ou não reconciliadas.

`QT_TRANS_TOTAL` inclui todas as movimentações efetivas em BRL, mesmo quando:

- não encontram casamento no mapa;
- não participam da composição temática;
- não participam do orçamento.

Por isso, a volumetria responde quantos fatos efetivos em BRL existem, e não quantos fatos contribuíram para as somas.

Quando não existe movimentação efetiva em BRL, `QT_TRANS_TOTAL = 0`.

### 5.2 `QT_TRANS_ENT`

**Nome humano recomendado:** Créditos efetivos em BRL.

O campo conta movimentações efetivas em BRL cuja natureza contábil é C. Ele não conta rendas e não garante participação no orçamento.

“Créditos” é mais preciso do que “Rendas”. “Entradas” pode ser usado em textos introdutórios desde que acompanhado da ressalva de que nem todo crédito é renda ou entrada orçamentária.

Quando o universo BRL está vazio, o campo é nulo. Na invariante de quantidade, esse nulo é tratado como zero apenas para conferir a soma dos parciais.

### 5.3 `QT_TRANS_SAI`

**Nome humano recomendado:** Débitos efetivos em BRL.

O campo conta movimentações efetivas em BRL cuja natureza contábil é D. “Débitos” preserva a natureza contábil; “Movimentações de saída” é uma tradução aceitável para público não técnico.

Um débito com `VL_TRAN` negativo continua sendo contado como débito. A quantidade segue a natureza D, não o sinal. No detalhe, natureza e valor assinado precisam aparecer juntos para não sugerir que o Radar corrigiu o lançamento.

Quando o universo BRL está vazio, o campo é nulo, com a mesma normalização restrita usada para a invariante de volumetria.

## 6. L2 — Totais transacionais e orçamentários

### 6.1 `VL_TRANS_ENT` e `VL_ENT_TOTAL`

`VL_TRANS_ENT` é uma cópia contratual de `VL_ENT_TOTAL`. Ambos representam exatamente:

> Total dos créditos efetivos em BRL que participam do orçamento.

Não existe diferença de fórmula nem diferença empresarial entre os dois campos. `VL_TRANS_ENT` é um alias redundante mantido no contrato de 80 atributos.

No HTML executivo, deve aparecer somente um valor, com o nome “Entradas orçamentárias realizadas”. Os dois campos podem permanecer disponíveis na visão técnica dos 80 atributos para preservar o contrato.

### 6.2 `VL_TRANS_SAI` e `VL_SAI_TOTAL`

`VL_TRANS_SAI` é uma cópia contratual de `VL_SAI_TOTAL`. Ambos representam:

> Total dos débitos efetivos em BRL que participam do orçamento.

Também não existe diferença humana entre eles. O HTML executivo deve mostrar um único valor, preferencialmente “Saídas orçamentárias realizadas”, mantendo a duplicidade apenas no contrato técnico.

## 7. L3 — Entradas temáticas

### 7.1 `VL_ENT_REN`

**Nome humano recomendado:** Renda classificada observada.

O campo representa o valor dos créditos efetivos em BRL classificados como Renda e autorizados a participar da composição temática.

A distinção definitiva é:

```text
Renda presumida
→ capacidade financeira estimada para o período

Renda classificada observada
→ créditos reais do período que o mapa reconheceu como classe Renda
```

“Renda observada” é aceitável, mas “Renda classificada observada” é mais preciso porque deixa claro que o resultado depende do mapa.

### 7.2 `VL_ENT_EST`

**Nome humano recomendado:** Restituições e estornos observados.

O campo reúne créditos efetivos em BRL classificados como Estorno e participantes da composição temática. No mapa reconhecido, essa classe é materializada pela categoria Restituição de IR.

O texto não deve generalizar como se qualquer reversão ou devolução fosse automaticamente reconhecida. A classificação depende das categorias existentes.

A apresentação deve dizer:

> Créditos classificados como restituição ou estorno; não representam renda recorrente.

### 7.3 `VL_ENT_RESG`

**Nome humano:** Resgates de investimentos.

O campo representa valores que voltaram à conta a partir de investimentos que já pertenciam ao cliente.

O resgate participa da composição temática das entradas porque explica a origem patrimonial do crédito. Ele não participa do orçamento porque não representa recurso novo: apenas converte um ativo investido em saldo disponível.

A explicação recomendada é:

> Movimentação patrimonial; não representa renda nova.

### 7.4 `VL_ENT_OUT`

`VL_ENT_OUT` é atualmente um campo reservado. As linhas estáticas de Outras Entradas possuem natureza nula e não casam com créditos C. Movimentações sem classificação recebem flags `N` e também não alimentam esse valor.

Enquanto essa situação permanecer:

- o campo fica em zero;
- não deve disputar espaço no resumo executivo;
- pode aparecer na visão técnica;
- a apresentação das entradas pode mostrar apenas classes com conteúdo, em vez de forçar cinco linhas vazias.

### 7.5 `VL_ENT_CRED`

`VL_ENT_CRED` também é um campo reservado. Nenhuma categoria está associada à Classe Radar Crédito.

Não existe conceito futuro documentado que autorize definir essa classe como empréstimo, financiamento ou “outros créditos”. A denominação correta é “Classe reservada, sem categoria associada”.

Enquanto não houver conteúdo reconhecido, o campo deve permanecer restrito à visão técnica.

### 7.6 `VL_ENT_TOTAL`

**Nome humano recomendado:** Entradas orçamentárias realizadas.

Definição completa:

> Soma literal dos créditos efetivos em BRL cujas categorias participam do orçamento.

`VL_ENT_TOTAL` não representa todos os créditos observados. Créditos sem participação orçamentária ficam fora, inclusive resgates de investimentos.

A diferença para `ENTRADAS_REALIZADAS` é:

```text
VL_ENT_TOTAL
→ créditos efetivos em BRL com participação orçamentária = S

ENTRADAS_REALIZADAS
→ todos os créditos efetivos em BRL que encontraram classificação válida,
  sem aplicar participação temática ou orçamentária
```

Assim, `ENTRADAS_REALIZADAS` pode ser maior por incluir resgates, receitas Agro e outros créditos classificados fora do orçamento.

## 8. L4 — Saídas temáticas

### 8.1 `VL_SAI_IND`

**Nome humano recomendado:** Saídas de finalidade indeterminada.

O campo representa saídas reconhecidas pelo mapa, mas sem informação suficiente para serem atribuídas a Essenciais, Não Essenciais, Futuro ou Obrigações.

Essas saídas formam o tema Categorização dos Gastos porque uma concentração elevada nessa classe reduz a capacidade de compreender para onde os recursos foram direcionados. A orientação associada procura aumentar a clareza e a qualidade da categorização do gasto.

Indeterminado não significa ausência de classificação. A movimentação encontrou o mapa e recebeu intencionalmente a classe Indeterminado.

### 8.2 `VL_SAI_ESS`

**Nome humano recomendado:** Gastos essenciais.

Definição:

> Valores destinados às necessidades correntes de vida e manutenção da pessoa ou da família.

“Necessidades correntes” é a explicação conceitual; “Gastos essenciais” é o rótulo mais direto para apresentação.

### 8.3 `VL_SAI_NAO_ESS`

**Nome humano recomendado:** Consumo planejável — Não Essenciais.

A classe Não Essenciais descreve a natureza atribuída às movimentações. O tema Consumo Planejado descreve o objetivo de orientação: ajudar a planejar a parcela mais discricionária do consumo.

Portanto:

```text
Classe: Não Essenciais
Tema de orientação: Consumo Planejado
```

“Não Essencial” não é julgamento moral nem afirma que a compra não tinha importância para o cliente.

### 8.4 `VL_SAI_FUT`

**Nome humano recomendado:** Recursos destinados ao futuro financeiro.

Definição:

> Recursos direcionados à proteção e à construção da capacidade financeira futura.

O conjunto reconhecido inclui aplicação financeira e contribuição previdenciária classificada como GPS. Ele não autoriza afirmar que toda categoria genérica de previdência pertence à classe Futuro.

Uma aplicação participa da destinação temática porque demonstra formação de patrimônio ou reserva. Ela não participa do orçamento porque o recurso continua pertencendo ao cliente sob outra forma.

Essa distinção deve ser explícita:

> Destinação temática não é sinônimo de consumo orçamentário.

### 8.5 `VL_SAI_OBR`

**Nome humano recomendado:** Obrigações financeiras e patrimoniais.

Definição:

> Valores destinados a compromissos financeiros, patrimoniais ou de crédito já assumidos.

A classe Obrigações contém compromissos que não são necessariamente operações de crédito. O tema Uso Consciente do Crédito é o nome educacional ao qual essa classe foi associada pelo modelo.

A ponte conceitual é o comprometimento financeiro: dívidas, prestações, encargos e compromissos patrimoniais reduzem a flexibilidade disponível e são tratados na orientação ligada ao uso consciente do crédito. Entretanto, não deve ser afirmado que toda obrigação observada surgiu de crédito. A justificativa detalhada do nome do tema não está documentada além dessa associação vigente.

### 8.6 `VL_SAI_TOTAL`

**Nome humano recomendado:** Saídas orçamentárias realizadas.

Definição completa:

> Soma literal dos débitos efetivos em BRL cujas categorias participam do orçamento.

`VL_SAI_TOTAL` pode ser diferente da soma dos cinco valores temáticos. A composição temática e o orçamento usam flags independentes. A aplicação financeira, por exemplo, pertence ao tema Futuro, mas fica fora das saídas orçamentárias.

Essa é uma explicação central para o HTML:

```text
Distribuição temática ≠ leitura orçamentária
```

O detalhe deve permitir identificar categorias que participam do tema e ficam fora do orçamento. Sem essa visibilidade, a pessoa pode interpretar a diferença como erro de soma.

## 9. M — Orçamento na visão `RENDA_PRESUMIDA`

### 9.1 Base da visão principal

Na visão principal, a entrada usada pelo orçamento é a renda presumida ajustada à quantidade de ciclos. As saídas continuam sendo as saídas orçamentárias realizadas.

```text
Base de entrada = renda presumida do período
Saídas = saídas orçamentárias realizadas
```

### 9.2 `VL_RES_ORC`

**Nome humano recomendado:** Resultado orçamentário estimado.

Na visão principal:

```text
Resultado orçamentário estimado
= renda presumida do período
− saídas orçamentárias realizadas
```

Valor positivo significa que as saídas orçamentárias ficaram abaixo da capacidade financeira presumida. Valor negativo significa que as saídas superaram essa capacidade. Zero significa igualdade literal entre as duas grandezas.

Esse campo:

- não é saldo bancário;
- não é patrimônio;
- não prova dinheiro disponível em conta;
- é uma diferença analítica entre uma capacidade estimada e saídas observadas.

“Capacidade remanescente” pode ser usado como explicação complementar, mas “Resultado orçamentário estimado” é mais neutro e evita parecer saldo disponível.

### 9.3 `PC_SAI_ENT`

**Nome humano recomendado:** Relação das saídas com a renda presumida.

Quando os valores possuem sinais usuais, a expressão “Comprometimento da renda presumida” também é compreensível. O rótulo neutro é preferível porque o contrato preserva sinais negativos.

Na visão principal, o campo responde:

> Que proporção da renda presumida do período corresponde às saídas orçamentárias realizadas?

Exemplos:

```text
Renda presumida: R$ 10.000
Saídas:          R$  8.000
Relação:         80%
```

```text
Renda presumida: R$ 10.000
Saídas:          R$ 13.000
Relação:         130%
```

No segundo exemplo, é correto dizer que as saídas equivalem a 130% da renda presumida e, matematicamente, superam essa base em 30%. Não se deve concluir automaticamente que a pessoa “gastou 30% mais do que ganha”, porque a renda é estimada e as saídas seguem categorias e sinais específicos.

Razões negativas são preservadas literalmente. O HTML deve sinalizar “valor influenciado pelos sinais originais das movimentações” e evitar uma narrativa positiva ou negativa automática. Não existe correção especial de sinal no contrato.

## 10. M2 — Faixas orçamentárias

As faixas descrevem a relação entre saídas e base. Elas não certificam saúde financeira nem produzem, isoladamente, um julgamento sobre o cliente.

| Faixa | Relação saídas/base | Leitura humana |
|---|---:|---|
| Neutro | 95% a 105%, inclusive | Saídas próximas da base dentro da tolerância contratual. |
| Deficitário Moderado | acima de 105% até 125% | Saídas moderadamente superiores à base. |
| Deficitário Acentuado | acima de 125% | Saídas acentuadamente superiores à base. |
| Superavitário Moderado | de 75%, inclusive, até menos de 95% | Saídas moderadamente inferiores à base. |
| Superavitário Acentuado | abaixo de 75% | Saídas acentuadamente inferiores à base. |

“Neutro” significa proximidade entre saídas e base, não equilíbrio integral da vida financeira.

“Superavitário” não é necessariamente bom. Pode representar disponibilidade, ausência de fatos observados, categorias fora do orçamento ou particularidades dos sinais. “Deficitário” não é necessariamente ruim: a base é estimada e pode não representar todos os recursos do período.

As faixas descrevem o estado orçamentário. A prioridade de orientação surge depois, quando o estado é combinado com concentração e perfil.

Os cortes de 75%, 95%, 105% e 125% são parâmetros metodológicos contratuais. Os materiais disponíveis não comprovam se foram definidos por especialistas, análise empírica, benchmark ou outra origem. Essa origem não deve ser inventada.

No resumo, devem aparecer a relação encontrada e o texto da faixa. Os limites podem ficar em ajuda contextual ou detalhe metodológico; não precisam ocupar o primeiro nível de leitura.

## 11. M3 — Campos do orçamento

| Campo | Significado | Apresentação recomendada |
|---|---|---|
| `CD_RES_ORC` | Código do estado macro: 0 Neutro, 1 Superavitário, 2 Deficitário. | Somente técnico. |
| `TX_RES_ORC` | Nome do estado macro: Neutro, Superavitário ou Deficitário. | Pode apoiar filtros e resumos. |
| `CD_FAIXA_ORC` | Código da faixa detalhada de direção e intensidade, de 0 a 4. | Somente técnico. |
| `TX_STS_RES` | Qualificador Moderado ou Acentuado; nulo no estado Neutro. | Complementar. |
| `TX_STS_FINAL` | Texto completo da faixa orçamentária. | Campo preferido no dashboard. |

Se apenas um atributo textual puder aparecer como resumo, deve ser `TX_STS_FINAL`, acompanhado de `PC_SAI_ENT` para mostrar a grandeza que originou o enquadramento.

## 12. N — Percentuais dos cinco temas

Na visão principal, cada percentual compara o valor temático com a renda presumida ajustada ao período.

### 12.1 `PC_SAI_IND`

**Nome humano:** Percentual da renda presumida associado a saídas de finalidade indeterminada.

Ele mede quanto da capacidade estimada está concentrado em saídas reconhecidas, mas sem destinação temática específica. Quanto maior, menor a clareza sobre o uso financeiro dos recursos.

### 12.2 `PC_SAI_ESS`

**Nome humano:** Percentual da renda presumida destinado a gastos essenciais.

Ele revela quanto da capacidade estimada foi direcionado às necessidades correntes reconhecidas pelo mapa.

### 12.3 `PC_SAI_NAO_ESS`

**Nome humano:** Percentual da renda presumida destinado ao consumo planejável.

Ele revela quanto da capacidade estimada foi direcionado à classe Não Essenciais.

### 12.4 `PC_SAI_FUT`

**Nome humano:** Percentual da renda presumida direcionado ao futuro financeiro.

Ele mede a destinação temática para formação ou proteção da capacidade futura. Aplicações continuam compondo esse percentual mesmo quando não participam do orçamento, porque o percentual usa a composição temática.

### 12.5 `PC_SAI_OBR`

**Nome humano:** Percentual da renda presumida destinado a obrigações.

“Destinado a obrigações” é preferível a “renda comprometida”, pois “comprometimento” pode ser confundido com a relação orçamentária total.

### 12.6 Interpretação geral

Percentual acima de 100% significa somente que o valor temático literal excedeu a base financeira usada naquela visão. Não autoriza concluir automaticamente que a pessoa gastou mais do que ganha.

A interpretação precisa considerar:

- renda presumida é uma estimativa;
- valores preservam sinais originais;
- aplicações podem participar de tema sem participar do orçamento;
- categorias não classificadas ou excluídas podem ficar fora das somas.

Quando a renda presumida é nula:

> Renda presumida não disponível; percentual temático não calculado.

Quando a renda presumida existe, mas é zero ou negativa:

> Renda presumida não positiva; não existe base válida para calcular o percentual temático.

Nulo não deve ser exibido como 0%.

## 13. O — Parâmetros de referência dos temas

### 13.1 Significado

`PC_REF_*` é um parâmetro fixo usado pelo modelo para formar os gatilhos da pontuação de concentração.

**Nome humano recomendado:** Parâmetro de referência do modelo.

Os valores são:

| Tema | Campo | Parâmetro |
|---|---|---:|
| Categorização dos Gastos | `PC_REF_IND` | 75% |
| Gestão de Orçamento | `PC_REF_ESS` | 50% |
| Consumo Planejado | `PC_REF_NAO_ESS` | 30% |
| Formação de Reserva | `PC_REF_FUT` | 20% |
| Uso Consciente do Crédito | `PC_REF_OBR` | 30% |

Esses valores:

- não são metas comprovadas de saúde financeira;
- não são recomendações individualizadas;
- não são benchmarks comprovados;
- não devem ser apresentados como limite universal adequado a toda pessoa;
- são constantes metodológicas que acionam faixas do modelo.

A origem conceitual dos valores não está documentada. Não é possível afirmar se vieram de especialistas, dados empíricos ou outra metodologia.

No produto, devem ser mostrados como parâmetros usados pelo modelo, nunca como recomendação direta ao cliente.

### 13.2 Direção da referência

Acima da referência não é sempre pior.

- Em Essenciais, Não Essenciais e Obrigações, percentuais maiores elevam a contribuição de prioridade.
- Em Futuro, percentuais menores elevam a contribuição de prioridade.
- Em Indeterminado, mais de 75% aciona uma regra excepcional de dominância.

No tema Futuro, 20% é o limite entre a maior prioridade de concentração e a faixa intermediária. O valor de 30% é outro corte da matriz: a partir dele, a contribuição de concentração cai para zero. Portanto, 20% não descreve sozinho toda a faixa considerada suficiente pelo modelo.

O modelo interpreta maior destinação ao Futuro como menor necessidade de orientação nesse tema. Essa é a razão funcional da lógica invertida. A escolha específica de 20% e 30% não possui justificativa de origem documentada.

No tema Indeterminado, 75% é um gatilho excepcional. O efeito comprovado é tornar Categorização dos Gastos dominante quando a proporção supera esse limite e a pontuação está completa. A razão metodológica para escolher exatamente 75% não está documentada.

## 14. P — Prioridade de concentração

### 14.1 Conceito geral

Concentração é a parcela da base financeira direcionada a uma classe temática de saída.

A pontuação de concentração não mede distância matemática contínua da referência. Ela enquadra o percentual observado em faixas discretas.

Uma pontuação maior significa maior contribuição desse componente para a prioridade de orientação. Não significa cliente melhor, pior, aprovado ou reprovado.

### 14.2 `NR_PONT_CONC_IND`

| Condição | Pontos | Leitura |
|---|---:|---|
| Até 75%, inclusive | 0 | O gatilho excepcional não foi acionado. |
| Acima de 75% | 99 | Categorização dos Gastos recebe dominância, se o fechamento estiver completo. |

O valor 99 não é uma medida linear de criticidade. Ele é um mecanismo de precedência: os demais temas alcançam no máximo seis pontos finais, enquanto 99 garante que IND seja o único máximo quando todas as prioridades puderem ser calculadas.

O efeito negocial é priorizar a compreensão e a categorização das saídas antes de orientar outros temas quando mais de 75% da base está em Indeterminado. A justificativa de origem para usar 99, em vez de dois pontos, não está documentada além desse efeito de dominância.

### 14.3 `NR_PONT_CONC_ESS`

| Percentual | Pontos | Leitura |
|---|---:|---|
| Abaixo de 50% | 0 | Faixa inferior de prioridade por concentração. |
| De 50%, inclusive, a menos de 75% | 1 | Faixa intermediária. |
| A partir de 75% | 2 | Faixa superior de prioridade por concentração. |

Os pontos 0, 1 e 2 representam níveis ordinais de contribuição. A razão metodológica dos cortes não está documentada.

### 14.4 `NR_PONT_CONC_NAO_ESS`

| Percentual | Pontos | Leitura |
|---|---:|---|
| Abaixo de 30% | 0 | Faixa inferior de prioridade. |
| De 30%, inclusive, a menos de 45% | 1 | Faixa intermediária. |
| A partir de 45% | 2 | Faixa superior de prioridade. |

A pontuação indica a intensidade de prioridade atribuída à concentração em consumo planejável. Não constitui julgamento sobre compras individuais.

### 14.5 `NR_PONT_CONC_FUT`

| Percentual | Pontos | Leitura |
|---|---:|---|
| A partir de 30% | 0 | Maior destinação ao Futuro reduz a prioridade de orientação. |
| De 20%, inclusive, a menos de 30% | 1 | Zona intermediária. |
| Abaixo de 20% | 2 | Baixa destinação temática ao Futuro eleva a prioridade. |

A lógica é invertida porque o modelo trata formação e proteção futura como destinação desejável: quanto menor a parcela identificada, maior a necessidade de orientação nesse tema.

### 14.6 `NR_PONT_CONC_OBR`

| Percentual | Pontos | Leitura |
|---|---:|---|
| Abaixo de 30% | 0 | Faixa inferior de prioridade. |
| De 30%, inclusive, a menos de 45% | 1 | Faixa intermediária. |
| A partir de 45% | 2 | Faixa superior de prioridade por concentração em obrigações. |

Obrigações e Não Essenciais usam os mesmos cortes de 30% e 45%. A equivalência está comprovada na matriz; o motivo metodológico para compartilhar esses limites não está documentado.

### 14.7 Base financeira não positiva

Quando existem transações e a base financeira é zero ou negativa, os percentuais ficam nulos, mas a concentração recebe zero no comportamento contratual aplicável.

Esse zero é uma convenção técnica do modelo. Ele não significa “tema sem prioridade por concentração” como conclusão empresarial, porque o percentual não pôde ser calculado.

O HTML deve priorizar a mensagem:

> Concentração não interpretável porque a base financeira não é positiva.

Se o valor técnico zero for exibido, deve vir acompanhado dessa ressalva. Não deve ser apresentado como evidência de situação adequada.

## 15. Q — Prioridade orçamentária por tema

### 15.1 Conceito geral

A dimensão orçamentária mede como a relação global entre saídas e base ajusta a prioridade de cada tema.

O mesmo valor temático pode demandar orientação diferente conforme o orçamento esteja deficitário, neutro ou superavitário. Essa dimensão acrescenta o contexto de pressão ou disponibilidade financeira à prioridade temática.

### 15.2 `NR_PONT_ORC_IND`

Quando há movimentações, `NR_PONT_ORC_IND = 0`. Sem movimentações, é nulo.

O campo existe para preservar a estrutura simétrica de cinco temas, mas não participa da pontuação final de Categorização dos Gastos. Deve ficar fora da narrativa executiva e disponível apenas no detalhamento técnico da composição.

### 15.3 Essenciais, Não Essenciais e Obrigações

Os três temas compartilham a mesma matriz:

| Estado orçamentário | Pontos | Efeito no modelo |
|---|---:|---|
| Deficitário Acentuado | 2 | Maior contribuição de prioridade. |
| Neutro | 1 | Contribuição intermediária. |
| Deficitário Moderado | 1 | Contribuição intermediária. |
| Superavitário Moderado | 0 | Sem acréscimo orçamentário. |
| Superavitário Acentuado | 0 | Sem acréscimo orçamentário. |

O efeito funcional é aumentar a prioridade desses temas quando existe maior pressão das saídas sobre a base. A escolha de aplicar a mesma matriz aos três temas é contratual; sua justificativa metodológica detalhada não está documentada.

### 15.4 Formação de Reserva

Futuro usa direção diferente:

| Estado orçamentário | Pontos | Leitura autorizada |
|---|---:|---|
| Superavitário Acentuado | 2 | Maior oportunidade de orientar recursos disponíveis ao Futuro. |
| Neutro | 1 | Oportunidade intermediária. |
| Superavitário Moderado | 1 | Oportunidade intermediária. |
| Deficitário Moderado | 0 | Sem acréscimo orçamentário para Futuro. |
| Deficitário Acentuado | 0 | Sem acréscimo orçamentário para Futuro. |

A leitura coerente é que maior disponibilidade relativa cria maior oportunidade de formação de reserva, enquanto um orçamento deficitário não adiciona prioridade orçamentária a esse tema. Essa interpretação descreve o efeito da matriz; a origem metodológica dos pesos não está documentada.

## 16. R — Prioridade de perfil por tema

### 16.1 Conceito geral

A dimensão de perfil ajusta a prioridade temática conforme o macroperfil comportamental recebido de outra área.

Pontuação maior significa que o tema recebe maior relevância dentro daquele contexto de perfil. Não significa que o perfil avalia a qualidade financeira do cliente nem que o Radar recalculou sua classificação.

### 16.2 Categorização dos Gastos

`NR_PONT_PRFL_IND = 0` quando existem movimentações. O tema Indeterminado é avaliado independentemente do macroperfil, porque sua prioridade final depende exclusivamente da concentração de saídas indeterminadas.

Esse campo é estrutural e não entra na pontuação final de IND.

### 16.3 Efeito comprovado da matriz

| Macroperfil | Essenciais | Não Essenciais | Futuro | Obrigações |
|---|---:|---:|---:|---:|
| Endividado | 0 | 1 | 0 | 2 |
| Equilibrista | 1 | 0 | 1 | 0 |
| Investidor | 1 | 0 | 2 | 0 |

Leitura dos efeitos:

- Endividado acrescenta maior peso a Obrigações, peso intermediário a Não Essenciais e nenhum peso a Essenciais ou Futuro.
- Equilibrista acrescenta peso intermediário a Essenciais e Futuro e nenhum peso a Não Essenciais ou Obrigações.
- Investidor acrescenta maior peso a Futuro, peso intermediário a Essenciais e nenhum peso a Não Essenciais ou Obrigações.

Os critérios que definem os três macroperfis e a justificativa empresarial específica de cada peso não foram fornecidos pela área produtora. Portanto, não é autorizado explicar causalmente por que Endividado recebe dois em Obrigações ou Investidor recebe dois em Futuro. O Radar consome a matriz como regra de ajuste de prioridade.

## 17. S — Prioridades finais

### 17.1 Categorização dos Gastos

`NR_PONT_IND_FIM` usa somente a concentração:

```text
Prioridade final de Categorização dos Gastos
= prioridade de concentração de Indeterminado
```

Orçamento e perfil não influenciam esse tema porque o fenômeno avaliado é a proporção de saídas sem destinação temática específica. Pressão orçamentária ou macroperfil não tornam uma movimentação mais ou menos categorizável.

### 17.2 Demais temas

Para Gestão de Orçamento, Consumo Planejado, Formação de Reserva e Uso Consciente do Crédito:

```text
Prioridade final
= concentração
+ orçamento
+ perfil
```

Se qualquer componente estiver nulo, a prioridade final do tema também fica nula.

### 17.3 Significado do número final

Pontuação final maior significa maior prioridade de orientação dentro do modelo. Dependendo do tema, essa prioridade pode representar:

- maior necessidade de atenção;
- maior pressão financeira;
- maior oportunidade de orientação.

“Prioridade” é o termo preferido para o negócio. “Score” ou “pontuação” pode permanecer no detalhe técnico.

Os números podem ser mostrados, mas nunca isoladamente. A composição em concentração, orçamento e perfil é mais importante para explicar por que o tema atingiu aquela posição.

Um tema com quatro pontos não é “duas vezes pior” que um tema com dois. Os valores são ordinais para priorização e resultam da soma de pesos discretos; não formam uma escala quantitativa linear de gravidade, risco ou saúde.

O valor 99 de IND é ainda mais excepcional: representa dominância metodológica, não uma grandeza comparável a quatro ou seis pontos.

## 18. T — Completude, máximo, empate e prioridade principal

### 18.1 `FL_PONTUACAO_COMPLETA`

`FL_PONTUACAO_COMPLETA = 'S'` significa:

> Todas as cinco prioridades temáticas puderam ser calculadas.

`FL_PONTUACAO_COMPLETA = 'N'` significa:

> Os fatos financeiros podem existir, mas a priorização completa dos cinco temas não pôde ser concluída.

Podem produzir incompletude:

- ausência de movimentações efetivas em BRL;
- base financeira nula;
- base zero quando impede a classificação orçamentária;
- ausência de renda na visão principal;
- ausência de perfil ou macroperfil fora do domínio;
- orçamento sem faixa calculável;
- janela indisponível.

O HTML deve informar qual componente ficou indisponível por tema. Exemplo:

> Formação de Reserva sem prioridade final: componente de perfil indisponível.

### 18.2 `NR_PONT_MAX`

É o maior valor entre as cinco prioridades finais quando a pontuação está completa. Seu papel é técnico na identificação do primeiro nível de prioridade.

Para o negócio, é mais útil mostrar o tema ou os temas que atingiram esse valor. O número máximo pode aparecer como explicação secundária.

### 18.3 `QT_TEMAS_PONT_MAX`

É a quantidade de temas que compartilham a prioridade máxima.

- quando vale 1, a existência de prioridade única pode ficar implícita;
- quando vale de 2 a 5, a quantidade deve ser mostrada junto com os nomes empatados.

### 18.4 `CD_TEMA_VENCEDOR` e `TX_TEMA_VENCEDOR`

`CD_TEMA_VENCEDOR` é um código técnico: 1 a 5 para prioridade única e 9 para empate. Deve permanecer na visão técnica.

`TX_TEMA_VENCEDOR` representa a primeira prioridade de orientação quando existe um único máximo.

O título recomendado no HTML é:

> Prioridade de orientação

“Tema vencedor” pode ser mantido apenas como nome contratual ou termo de apoio para equipes que já o conhecem. Ele não deve sugerir competição, mérito ou melhor desempenho.

### 18.5 Empate

Quando dois ou mais temas compartilham o máximo, o Radar deliberadamente não desempata.

O negócio deve ver todos os temas empatados. Eles podem ser derivados das cinco prioridades finais, embora o campo textual final traga apenas “Empate”. Não existe ordem recomendada entre eles e a apresentação não deve inventar uma prioridade.

### 18.6 Máximo igual a zero

Se as cinco prioridades forem zero:

- a pontuação está completa;
- o máximo é zero;
- cinco temas estão empatados;
- não existe destaque isolado.

A explicação correta é:

> Nenhum tema se destacou como primeira prioridade pelas regras atuais.

Isso não significa ausência de necessidade financeira, saúde perfeita ou aprovação do cliente.

## 19. U — Cenários financeiros

### 19.1 Visão principal

`RENDA_PRESUMIDA` é definitivamente a visão principal do produto. O dashboard deve abrir nessa visão e manter seu nome visível durante toda a análise.

O termo genérico “Base financeira” pode aparecer como conceito técnico, mas a interface deve sempre mostrar o nome concreto:

```text
Base usada nesta visão: Renda presumida — R$ X
```

ou:

```text
Base usada nesta visão: Entradas realizadas — R$ X
```

### 19.2 Pergunta de negócio de `ENTRADAS_REALIZADAS`

O cenário responde:

> Como mudaria a prioridade de orientação se os créditos efetivamente observados fossem usados como capacidade financeira de comparação, em vez da renda presumida?

É uma análise de sensibilidade à escolha da base e uma comparação entre capacidade estimada e fluxo creditado observado.

Ela pode ajudar a investigar divergências entre a estimativa de renda e a dinâmica da conta, mas não autoriza concluir que os créditos representam renda real ou que a renda presumida está errada.

### 19.3 Composição das entradas realizadas

A base inclui movimentações que:

- permaneceram efetivas após reconciliação;
- possuem natureza C;
- estão em BRL;
- encontraram casamento válido no mapa.

Ela não aplica participação temática nem participação orçamentária. Por isso inclui:

- resgate, porque é um crédito classificado observado;
- receita Agro, porque é um crédito classificado em BRL;
- crédito classificado mesmo quando não participa do orçamento.

Resgate e Agro entram não porque sejam renda, mas porque o cenário procura todos os créditos financeiros reconhecidos pelo mapa.

A definição correta é:

> Entradas realizadas são todos os créditos efetivos, classificados e em BRL, independentemente das flags de participação.

Crédito sem classificação, débito e moeda não BRL ficam fora.

### 19.4 Diferença entre as bases

Se a renda presumida é R$ 10 mil e as entradas realizadas são R$ 30 mil, a conclusão autorizada é:

> A capacidade estimada e o fluxo creditado observado produziram bases diferentes para a análise.

Renda Presumida e Entradas Realizadas são duas lentes sobre os mesmos fatos financeiros efetivos, e não duas medições equivalentes de renda.

Pode-se dizer que houve divergência entre a estimativa e os créditos observados. Não se deve afirmar que o cliente ganha R$ 30 mil, que sua renda está subestimada ou que possui R$ 30 mil de capacidade recorrente, porque a base pode conter resgates, receitas específicas, restituições e outros créditos.

O HTML deve decompor as entradas realizadas por classe e categoria. Essa explicação é essencial quando a base fica muito acima da renda presumida.

### 19.5 Comparação dos diagnósticos

Os campos mais úteis para comparação executiva são:

- valor da base;
- resultado orçamentário estimado;
- relação saídas/base;
- status orçamentário;
- cinco percentuais temáticos;
- cinco prioridades finais;
- completude;
- prioridade única ou empate.

Os 31 campos recalculados devem permanecer acessíveis no detalhe técnico, mas não precisam aparecer todos no resumo.

Quando a prioridade muda entre cenários, significa que o diagnóstico é sensível à base financeira escolhida. Essa sensibilidade é valiosa para atendimento porque indica que a orientação depende materialmente de usar capacidade estimada ou fluxo creditado. Ela deve gerar investigação, não escolha oportunista do resultado preferido.

## 20. V — Resultado oficial híbrido

O resultado oficial de 80 atributos combina:

- percentuais temáticos baseados em renda presumida;
- orçamento baseado em entradas orçamentárias realizadas.

Não existe uso empresarial independente documentado que exija essa combinação como narrativa principal. Seu propósito comprovado é preservar o contrato físico, a rastreabilidade e a compatibilidade dos 80 atributos.

Como o produto principal usa `RENDA_PRESUMIDA` de forma consistente no orçamento e nos percentuais, o híbrido não deve ser apresentado ao usuário comum. Misturar bases sem explicação cria uma leitura incoerente.

O resultado híbrido deve permanecer acessível na visão técnica dos 80 atributos. Qualquer uso negocial específico futuro precisa ser declarado antes de promovê-lo à narrativa executiva.

## 21. W — Estados especiais para apresentação

### 21.1 Renda presumida ausente

> Renda presumida não disponível. Os fatos financeiros foram apurados quando possível, mas a priorização dependente dessa base não pôde ser concluída.

### 21.2 Renda presumida igual a zero

Zero é diferente de ausência:

> Renda presumida informada com valor zero. Existe um registro de renda, mas não há base positiva para calcular percentuais e orçamento da visão principal.

O HTML não deve usar “renda não encontrada” nesse estado.

### 21.3 Perfil ausente

> Perfil financeiro não disponível. As movimentações continuam válidas, mas as prioridades que dependem do macroperfil ficam incompletas.

### 21.4 Conta elegível não única

> Não foi possível determinar uma única conta corrente BB elegível para localizar o ciclo financeiro.

O texto não deve afirmar se nenhuma conta foi encontrada ou se várias contas foram encontradas, pois a flag não diferencia as causas.

### 21.5 CPF não único

> Não foi possível determinar um único CPF não nulo para o cliente.

O texto não deve escolher entre ausência e multiplicidade.

### 21.6 Janela financeira indisponível

> Não foi possível formar a janela financeira do cliente. As movimentações do período e os diagnósticos dependentes da janela não foram apurados.

### 21.7 Janela válida sem movimentações observadas

> Nenhuma movimentação financeira válida foi observada no período analisado.

Esse texto deve ser usado somente quando realmente não houve movimento. “Nenhuma movimentação efetiva em BRL” é mais amplo e pode esconder moedas estrangeiras ou neutralizações.

### 21.8 Somente moedas não BRL

> Foram observadas movimentações, mas nenhuma em BRL. Sem conversão cambial, o Radar preserva os fatos no detalhe e não calcula as métricas financeiras em reais.

### 21.9 Todos os movimentos oficiais neutralizados

> Havia movimentações no ciclo, mas todas foram interpretadas como contrapartes de transferências próprias e neutralizadas. Nenhum fato financeiro efetivo permaneceu para o diagnóstico.

Enquanto a decisão de bancos diferentes não estiver implementada, essa explicação deve carregar o alerta de que o pareamento ainda pode incluir linhas do mesmo banco.

### 21.10 Fatos efetivos sem classificação

> Foram encontrados fatos financeiros efetivos em BRL, mas o mapa não reconheceu suas combinações de categoria e natureza. Eles permanecem na volumetria e ficam fora das somas temáticas e orçamentárias.

As somas correspondentes recebem zero. Como essas linhas continuam contando em `QT_TRANS_TOTAL`, o contrato pode permitir que as etapas posteriores produzam prioridades a partir dos valores temáticos zerados, da situação orçamentária e do perfil disponível. O HTML deve revelar que não houve classificação reconhecida e não apresentar essa prioridade como se estivesse sustentada por uma distribuição temática observada.

### 21.11 Perfil ambíguo

A ambiguidade na data mais recente é bloqueante. Uma execução bloqueada não deve gerar o dashboard oficial, pois não existe resultado final confiável.

É recomendável uma página ou mensagem separada de falha operacional:

> A análise foi interrompida porque mais de um perfil financeiro foi encontrado na referência mais recente.

Essa página de estado não é um dashboard parcial e não deve apresentar prioridade, orçamento ou vencedor.

## 22. X — As cinco perguntas que orientam os números

### 22.1 `VL_REN_PRES`

> Qual é a capacidade financeira estimada para o período analisado?

### 22.2 `VL_SAI_TEMA`

> Quanto dos fatos financeiros efetivos foi direcionado a esta dimensão temática?

### 22.3 `PC_SAI_TEMA`

> Que parcela da base financeira ativa foi direcionada a esta dimensão temática?

### 22.4 `NR_PONT_TEMA_FIM`

> Qual é a prioridade de orientação deste tema considerando os componentes aplicáveis de concentração, orçamento e perfil?

Para Categorização dos Gastos, o único componente aplicável é concentração.

### 22.5 `TX_TEMA_VENCEDOR`

> Qual tema deve receber primeiro a orientação, quando existe prioridade completa e um único máximo?

Quando existe empate ou incompletude, essa pergunta não possui uma resposta única.

## 23. Y — Hierarquia final da narrativa

### 23.1 Primeiros dez segundos

A primeira visão deve responder, nesta ordem:

1. quem e qual período estão sendo analisados;
2. qual cenário está ativo;
3. qual é a base financeira e seu valor;
4. quais são as saídas orçamentárias e sua relação com a base;
5. qual é o status orçamentário;
6. se existe prioridade única, empate ou diagnóstico incompleto.

A prioridade pode estar visível, mas deve permanecer acompanhada da base e do contexto que a produziu. Ela não deve aparecer como uma nota solta.

### 23.2 Compreensão em até dois minutos

A pessoa precisa entender:

1. evidência de utilização recente;
2. conta elegível, ciclo e janela;
3. renda presumida e sua referência;
4. cobertura monetária e contexto Agro;
5. quantidade de movimentos oficiais, neutralizados e efetivos;
6. composição das entradas e saídas;
7. diferença entre tema e orçamento;
8. percentuais sobre a base ativa;
9. composição das prioridades por concentração, orçamento e perfil;
10. prioridade única, empate ou causa da incompletude;
11. diferença ao alternar para Entradas Realizadas.

### 23.3 Conteúdo de “ver detalhes”

Devem ficar sob expansão:

- movimentações individuais;
- descrição original, banco, moeda e valor assinado;
- categorias, grupos e tratamento de participação;
- movimentos não BRL;
- categorias fora do tema ou do orçamento;
- pares exatos e de borda;
- movimentos externos usados como evidência;
- microperfil;
- limites das faixas;
- decomposição completa das entradas realizadas;
- composição numérica das prioridades.

### 23.4 Conteúdo exclusivamente técnico

Não deve disputar atenção com o diagnóstico:

- identificadores internos de transação;
- códigos quando já existe nome humano;
- schema e tipos físicos;
- aliases redundantes dos 80 atributos;
- posições de rankeamento e assinaturas de desempate;
- contagens auxiliares de pareamento;
- nomes de views, consultas ou fontes físicas;
- campos de auditoria e validações de contrato.

### 23.5 Posição da reconciliação

A reconciliação deve aparecer em dois níveis:

- um funil resumido depois do resumo financeiro e antes da explicação detalhada da composição e das prioridades;
- pares e contrapartes somente no detalhe.

O resumo precisa mostrar:

```text
movimentos oficiais
→ linhas neutralizadas
→ movimentos efetivos
```

Assim, a pessoa entende a formação dos fatos efetivos antes de interpretar valores temáticos e prioridades, sem fazer a mecânica de pares dominar os primeiros segundos.

### 23.6 Permanência da base ativa

Renda presumida deve permanecer visível durante toda a seção de diagnóstico quando essa visão estiver ativa. Ao alternar o cenário, o nome e o valor da nova base devem continuar visíveis.

O nome do cenário é obrigatório em todas as áreas com números recalculados. Isso impede que percentuais, orçamento e prioridade de uma base sejam confundidos com a outra.

## 24. Z — Narrativa operacional definitiva

A narrativa proposta representa o Radar com três ajustes de precisão:

- o Radar não estima sozinho a renda; ele consome uma estimativa e a ajusta ao período;
- a neutralização entre bancos diferentes é a decisão negocial desejada, mas ainda está pendente de implementação;
- prioridade única só existe quando a pontuação está completa e não há empate.

A narrativa definitiva é:

1. Identificamos a pessoa e o período financeiro analisado.
2. Usamos a renda presumida recebida, ajustada à quantidade de ciclos, como capacidade financeira estimada da visão principal.
3. Observamos as movimentações reais associadas ao cliente.
4. Neutralizamos pares interpretados como transferências entre contas próprias para não confundir movimentação patrimonial com renda ou consumo; a regra desejada exige bancos conhecidos e diferentes e permanece pendente de implementação.
5. Classificamos os fatos que permaneceram segundo sua finalidade financeira.
6. Medimos quanto da base financeira ativa foi direcionado a cada dimensão temática.
7. Consideramos a situação orçamentária e o perfil financeiro recebido nos temas em que esses componentes se aplicam.
8. Identificamos a primeira prioridade de orientação quando as cinco prioridades estão completas e existe um único máximo; caso contrário, informamos empate ou incompletude.
9. Comparamos a leitura principal com a lente secundária de créditos efetivamente realizados.

Essa sequência preserva a pergunta central do produto:

> Como a pessoa distribui sua renda presumida e o que essa distribuição revela sobre sua saúde financeira e sua prioridade de orientação?

“Saúde financeira”, nesse contexto, não é uma nota geral nem uma aprovação. É a leitura combinada da distribuição temática, da relação entre saídas e base, do contexto comportamental recebido e da prioridade educacional resultante.

## 25. Limites definitivos de interpretação

O conteúdo deste documento não autoriza afirmar que:

- bancos diferentes já fazem parte do pareamento executado;
- a ausência dessa condição é comprovadamente um bug histórico;
- toda movimentação efetiva está em BRL;
- flag de moeda `N` invalida os fatos BRL;
- presença Agro transforma o cliente em cliente Agro;
- `QT_TRANS_ENT` conta rendas;
- `VL_TRANS_ENT` e `VL_ENT_TOTAL` possuem conceitos diferentes;
- todas as entradas observadas participam do orçamento;
- resgate representa renda nova;
- aplicação representa consumo ou perda patrimonial;
- a soma temática precisa ser igual ao total orçamentário;
- resultado orçamentário é saldo bancário ou patrimônio;
- Superavitário significa automaticamente bom;
- Deficitário significa automaticamente ruim;
- parâmetros de referência são metas universais de saúde;
- a origem dos limiares e pesos é conhecida;
- pontuação maior significa cliente pior;
- quatro pontos representam o dobro da gravidade de dois;
- zero técnico com base não positiva significa situação adequada;
- perfil explica causalmente o comportamento observado;
- empate possui ordem oculta entre os temas;
- máximo zero significa ausência de necessidade de orientação;
- Entradas Realizadas representa renda real;
- diferença entre bases comprova erro na renda presumida;
- resultado híbrido deve orientar a experiência principal;
- execução bloqueada possui dashboard oficial válido.

Essas fronteiras mantêm separadas quatro coisas que não podem ser confundidas: fato observado, cálculo contratual, interpretação autorizada e decisão negocial ainda pendente de implementação.
