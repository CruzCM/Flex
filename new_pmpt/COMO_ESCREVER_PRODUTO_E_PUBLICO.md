# COMO ESCREVER PRODUTO E PÚBLICO

## Guia oficial da arquitetura de geração de mensagens

**Status:** versão 1.0 — contrato semântico congelado  
**Escopo:** cadastro de produtos e públicos que alimenta Apresentação, Copywriter, TND, Voz BB, tagline, headline e CTA.

---

## 1. Objetivo deste documento

Este guia define como escrever os cadastros de **produto** e **público** que servem de fonte para toda a arquitetura de geração de mensagens.

O cadastro não é uma descrição neutra de banco de dados. Ele é a base factual e persuasiva da comunicação. Quando um campo é vago, repetitivo ou tecnicamente confuso, toda a cadeia tende a produzir texto genérico, fraco ou incoerente.

A meta é produzir registros que sejam, ao mesmo tempo:

- verdadeiros e sustentáveis;
- claros para uma pessoa leiga;
- específicos o suficiente para gerar mensagem relevante;
- flexíveis o suficiente para alimentar diferentes Apresentações e Tendências Cognitivas;
- consistentes com o nível de promessa real da solução.

### Princípio central

> Apelo não vem de adjetivo.  
> Apelo vem de situação concreta + tarefa prática + benefício real + estado desejado.

---

## 2. A unidade de comunicação

A unidade mínima da arquitetura é:

```text
PRODUTO + PÚBLICO
```

O produto explica **qual solução existe e qual resultado concreto ela entrega**.

O público explica **em qual situação aquela solução pode ser relevante, qual tarefa prática precisa ser realizada e como a pessoa quer se sentir**.

```text
PÚBLICO
situação vivida
↓
necessidade prática
↓
estado emocional desejado

PRODUTO
solução e mecanismo
↓
benefício racional concreto
↓
efeito emocional plausível
```

A mensagem final nasce da relação entre esses dois blocos.

---

## 3. O que produto e público são — e o que não são

### Produto

Produto é a solução oferecida: serviço, ferramenta, modalidade, orientação ou prática educativa.

Ele deve responder:

```text
O que é?
Como funciona, de forma simples?
Qual resultado concreto a pessoa pode acessar, realizar ou receber?
Que efeito emocional esse resultado pode favorecer?
```

Produto **não é** apenas o nome comercial, uma lista de funcionalidades ou um slogan.

### Público

Público é a situação em que a solução pode fazer sentido.

Ele deve responder:

```text
O que essa pessoa vive?
O que ela precisa fazer ou resolver na prática?
Como ela deseja se sentir diante dessa situação?
```

Público **não é** um diagnóstico, julgamento, rótulo interno, score, percentual ou interpretação técnica do comportamento da pessoa.

---

## 4. Regra máxima: escrever para leigos

Todo campo deve ser compreendido por alguém que não conhece produtos financeiros, conceitos de crédito ou termos técnicos.

### Tradução obrigatória

| Evitar | Preferir |
|---|---|
| análise de crédito alinhada ao histórico compartilhado | possibilidade de aumentar o limite de crédito, se a análise aprovar |
| jornada de iniciação de pagamento | fazer um pagamento com dinheiro de outro banco sem abrir outro aplicativo |
| contrato parcelado com prazo definido | dividir o valor usado em parcelas e saber quando termina de pagar |
| carta de crédito após contemplação | usar um valor de crédito quando a cota for liberada |
| visão consolidada de compromissos financeiros | ver quanto do mês já está comprometido com parcelas e juros |

### Pergunta de validação

> Uma pessoa leiga entenderia o que isso significa sem precisar pesquisar uma palavra?

Se a resposta for não, reescreva.

---

## 5. Contrato semântico dos seis campos

Os campos abaixo alimentam diretamente os placeholders da Apresentação.

| Cadastro | Placeholder | Pergunta que responde | Forma recomendada |
|---|---|---|---|
| `TX_DCR_DETD_PBCO` | `{PH_PBCO_DCR}` | Quem vive esse contexto? | `Pessoas que + situação concreta` |
| `TX_NCDD_RCNL_PBCO` | `{PH_PBCO_RCNL}` | O que essa pessoa precisa fazer? | `Verbo no infinitivo + objeto + contexto` |
| `TX_NCDD_EMOC_PBCO` | `{PH_PBCO_EMOC}` | Como ela quer se sentir? | `Mais + estado emocional específico` |
| `TX_DCR_DETD_SGT` | `{PH_SGT_DCR}` | O que é a solução? | `Uma solução, serviço, orientação ou ferramenta + mecanismo simples` |
| `TX_BNF_RCNL_SGT` | `{PH_SGT_RCNL}` | O que ela entrega de concreto? | `Resultado funcional específico, em frase nominal` |
| `TX_BNF_EMOC_SGT` | `{PH_SGT_EMOC}` | O que esse resultado pode favorecer? | `Mais + efeito emocional plausível` |

### Regra de não sobreposição

Cada campo deve acrescentar uma informação que os outros não trazem.

```text
Público descrição
= a condição em que a pessoa está

Necessidade racional
= a tarefa prática que ela precisa realizar

Necessidade emocional
= o estado que ela busca nessa situação

Produto descrição
= a solução e seu mecanismo

Benefício racional
= o resultado concreto da solução

Benefício emocional
= o efeito humano possível desse resultado
```

---

## 6. Como escrever o produto

### 6.1. Nome do produto

O nome identifica a solução e deve ser mantido conforme o catálogo aprovado.

Exemplos:

```text
OPEN FINANCE BB
COFRINHO BB
CATEGORIZAÇÃO DOS GASTOS
GESTÃO DO ORÇAMENTO
```

O nome serve para classificação. A descrição e os benefícios precisam explicar o produto para quem não o conhece.

### 6.2. Descrição do produto

A descrição apresenta o que a solução faz, usando palavras simples.

**Boa estrutura:**

```text
Uma [solução] para [ação principal] por meio de [mecanismo simples].
```

**Exemplos bons:**

```text
Um serviço que permite ao BB considerar informações financeiras que você tem em outros bancos ao avaliar crédito.

Uma opção para dividir em parcelas o valor usado no Limite Especial da conta.

Uma orientação de Educação Financeira para organizar os gastos do mês em grupos, como alimentação, transporte, contas e lazer.
```

**Evitar:**

```text
Solução inovadora para potencializar sua vida financeira.

Produto de educação para promover bem-estar financeiro.

Ferramenta completa e inteligente para decisões mais conscientes.
```

Essas frases não explicam mecanismo, ação ou resultado real.

### 6.3. Benefício racional do produto

Este é o campo mais importante do cadastro.

O benefício racional deve nomear **uma entrega concreta**, não uma abstração. Ele precisa dizer o que a pessoa pode receber, fazer, usar, ver, comparar, organizar ou acompanhar.

#### Formato preferencial

Use uma frase nominal concreta, porque ela encaixa melhor em todas as Apresentações.

```text
A possibilidade de aumentar o limite de crédito, se a análise aprovar

Parcelas e prazo definidos para pagar o valor usado

Cashback ou desconto na compra de celulares participantes, conforme a oferta

Uma visão dos gastos que se repetem e dos que ocupam mais espaço no mês

Uma meta de reserva com um valor definido para começar a guardar
```

#### Não usar como benefício principal

```text
Mais clareza
Mais organização
Mais previsibilidade
Mais facilidade
Mais controle
Mais confiança
```

Essas expressões podem aparecer como efeito emocional ou como consequência na copy, mas não substituem a entrega real do produto.

#### Critério de qualidade

> O benefício racional precisa ser algo que uma pessoa consiga apontar, receber, visualizar, escolher, comparar, contratar, usar ou realizar.

### 6.4. Benefício emocional do produto

O benefício emocional mostra o efeito humano plausível do benefício racional.

Ele não pode prometer transformação garantida.

**Boa estrutura:**

```text
Mais + efeito emocional + situação relacionada
```

**Exemplos:**

```text
Mais tranquilidade para saber como o saldo será pago.

Mais satisfação por encontrar uma boa condição de compra.

Mais motivação para continuar juntando dinheiro para as próprias metas.
```

**Evitar:**

```text
Fim da preocupação financeira.

Segurança total para o futuro.

Liberdade financeira garantida.
```

---

## 7. Como escrever o público

### 7.1. Nome do público

O nome organiza o catálogo.

Em produtos bancários, o nome pode representar a situação principal:

```text
Uso recorrente do Limite Especial
Histórico financeiro em outras instituições
Metas financeiras junto aos gastos do dia a dia
```

Em Educação Financeira, produto e público podem ter o mesmo nome do tema, quando essa for a decisão de catálogo:

```text
Categorização dos Gastos
Gestão do Orçamento
Uso Consciente do Crédito
Consumo Planejado
Formação de Reserva
```

Quando os nomes forem iguais, os conteúdos continuam tendo funções diferentes: o produto explica a orientação; o público explica o contexto.

### 7.2. Descrição do público

A descrição deve mostrar uma situação reconhecível, sem afirmar que o sistema sabe tudo sobre a vida da pessoa.

**Boa estrutura:**

```text
Pessoas que + situação possível, observável e não julgadora.
```

**Exemplos bons:**

```text
Pessoas que recorrem ao Limite Especial para cobrir despesas do mês.

Pessoas que querem entender melhor gastos que se repetem no mês.

Pessoas que querem acompanhar como entradas, saídas e compromissos se distribuem no mês.
```

### Linguagem de Educação Financeira

Quando a recomendação nasce de sinais de movimentação, ela deve ser cuidadosa e não conclusiva.

**Usar:**

```text
Pessoas que querem entender melhor...
Pessoas que querem acompanhar...
Pessoas que desejam planejar...
Pessoas que buscam organizar...
```

**Evitar:**

```text
Identificamos gastos excessivos.
Você está com dificuldade no orçamento.
Seu consumo está alto.
Você não sabe se organizar.
```

O objetivo é orientar sem invadir, incentivar sem julgar e convidar para uma prática concreta.

### 7.3. Necessidade racional do público

A necessidade racional é um único trabalho prático. Ela deve ter verbo no infinitivo e ser possível de iniciar com uma ação concreta.

**Boa estrutura:**

```text
Verbo + objeto + contexto ou limitação.
```

**Exemplos bons:**

```text
Organizar o pagamento do saldo usado sem depender do Limite Especial.

Categorizar as despesas do período para identificar para onde o dinheiro está indo.

Planejar uma compra considerando prioridade e impacto no orçamento.

Começar a reservar dinheiro para objetivos e imprevistos.
```

**Evitar:**

```text
Ter parcelas fixas e juros menores.
Ter mais tranquilidade.
Economizar mais.
Melhorar a vida financeira.
```

Essas frases descrevem benefício, emoção ou objetivo amplo, não uma tarefa concreta.

### 7.4. Necessidade emocional do público

A necessidade emocional é o estado que a pessoa quer alcançar enquanto lida com a necessidade racional.

Ela deve ter apenas um eixo predominante.

**Exemplos bons:**

```text
Mais controle sobre o próprio dinheiro.
Mais previsibilidade para conduzir o mês financeiro.
Mais autonomia nas escolhas de consumo.
Mais segurança para olhar para o futuro.
```

**Evitar acumular estados:**

```text
Mais organização, previsibilidade, estabilidade e tranquilidade.
Mais autonomia, sem culpa e sem privação.
```

Escolha o estado principal. Os demais podem aparecer posteriormente na copy, quando sustentados pelo texto-base.

---

## 8. Produto bancário e Educação Financeira

### Produtos bancários

O produto é a solução bancária real.

```text
Open Finance BB
Consórcio Imobiliário BB
Parcelamento do Limite Especial da Conta BB
ITP BB
Cofrinho BB
```

O benefício racional deve ser uma entrega concreta do produto: aumento possível de limite, carta de crédito, parcelas definidas, cashback ou desconto, pagamento sem alternar de aplicativo, acompanhamento de meta etc.

### Educação Financeira

**Educação Financeira é a oferta de orientação.**

Os temas são cadastrados como produtos temáticos:

```text
Categorização dos Gastos
Gestão do Orçamento
Uso Consciente do Crédito
Consumo Planejado
Formação de Reserva
```

A descrição deve começar por uma orientação educativa e indicar a prática:

```text
Uma orientação de Educação Financeira para...
```

**Minhas Finanças não é o produto.**

Minhas Finanças é o ambiente em que a pessoa já recebe a recomendação e realiza a atividade. Por isso, o nome do ambiente não deve substituir o produto na descrição.

```text
Não:
Uma orientação no Minhas Finanças para organizar gastos.

Sim:
Uma orientação de Educação Financeira para organizar os gastos do mês em grupos.
```

---

## 9. Método passo a passo para criar um cadastro

### Passo 1 — Definir a unidade de comunicação

Pergunte:

```text
Qual produto ou orientação será apresentada?
Para qual contexto de público?
Qual prática ou resultado a mensagem deve tornar relevante?
```

A resposta precisa caber em um único par Produto + Público.

### Passo 2 — Separar fato de interpretação

Antes de escrever, organize a informação em seis perguntas:

```text
O que a solução é?
Como ela funciona para uma pessoa leiga?
Qual entrega concreta ela oferece?
Qual efeito emocional essa entrega pode favorecer?
Que situação o público vive ou pode reconhecer?
Qual tarefa prática ele precisa realizar?
```

Não leve para o cadastro informações internas como score, classificação, hipótese comportamental ou leitura técnica não comunicável.

### Passo 3 — Escrever a descrição do produto

Escreva primeiro a solução em linguagem simples. Não use benefício, emoção ou slogan como substituto da descrição.

### Passo 4 — Escolher um benefício racional real

Escolha a entrega mais concreta e mais relevante para a comunicação.

Não tente colocar todos os benefícios existentes no mesmo campo.

```text
Um produto pode ter muitos benefícios.
O cadastro deve eleger um benefício racional principal.
```

### Passo 5 — Derivar o benefício emocional

Pergunte:

```text
Quando a pessoa acessa esse benefício concreto, qual estado emocional isso pode favorecer?
```

Mantenha uma relação proporcional. O efeito não pode prometer mais do que o produto sustenta.

### Passo 6 — Escrever o contexto do público

Descreva uma situação possível e reconhecível. Evite julgamento, diagnóstico e tom invasivo.

### Passo 7 — Definir a necessidade racional

Transforme a necessidade em uma prática clara, com verbo no infinitivo.

A necessidade racional deve permitir que a CTA seja inferida mais tarde, mas não deve conter CTA de interface.

### Passo 8 — Definir a necessidade emocional

Escolha um único estado emocional que a pessoa busca alcançar nessa situação.

### Passo 9 — Conferir as separações

Verifique:

```text
O produto descrição explica o mecanismo?
O benefício racional nomeia uma entrega concreta?
O benefício emocional é um efeito plausível?
O público descrição mostra contexto sem julgamento?
A necessidade racional é uma tarefa única?
A necessidade emocional é um estado desejado único?
```

### Passo 10 — Testar na Apresentação

A ficha só está pronta quando seus seis campos funcionam dentro das estruturas de Apresentação.

---

## 10. Como o cadastro encaixa na Apresentação

A Apresentação transforma os seis campos em uma proposição de valor. Ela não inventa fatos, provas, promessas ou benefícios novos.

### Teste principal: Encaixe de Valor

```text
Para [PÚBLICO_DESCRIÇÃO], quando precisam [NECESSIDADE_RACIONAL]
e buscam [NECESSIDADE_EMOCIONAL], [PRODUTO_DESCRIÇÃO] oferece
[BENEFÍCIO_RACIONAL], favorecendo [BENEFÍCIO_EMOCIONAL].
```

Esse teste revela se os campos estão separados e se combinam de forma natural.

### Outros testes de encaixe

```text
Quando precisam [NECESSIDADE_RACIONAL], [PÚBLICO_DESCRIÇÃO]
encontram em [PRODUTO_DESCRIÇÃO] uma alternativa que oferece
[BENEFÍCIO_RACIONAL], gera [BENEFÍCIO_EMOCIONAL] e apoia
[NECESSIDADE_EMOCIONAL].
```

```text
Com [PRODUTO_DESCRIÇÃO], [PÚBLICO_DESCRIÇÃO] acessam
[BENEFÍCIO_RACIONAL] para [NECESSIDADE_RACIONAL], gerando
[BENEFÍCIO_EMOCIONAL] e apoiando [NECESSIDADE_EMOCIONAL].
```

```text
[BENEFÍCIO_RACIONAL] ajuda [PÚBLICO_DESCRIÇÃO] a
[NECESSIDADE_RACIONAL]. Com [PRODUTO_DESCRIÇÃO], isso pode gerar
[BENEFÍCIO_EMOCIONAL] e apoiar [NECESSIDADE_EMOCIONAL].
```

### Regra gramatical decisiva

O benefício racional deve preferencialmente ser uma frase nominal concreta, porque ele precisa funcionar em construções como:

```text
oferece [benefício]
acessam [benefício]
[benefício] ajuda pessoas a...
```

Por isso, prefira:

```text
Uma visão dos gastos que se repetem no mês.
Parcelas e prazo definidos para pagar o valor usado.
A possibilidade de aumentar o limite de crédito, se a análise aprovar.
```

Em vez de:

```text
Identificar gastos.
Organizar pagamentos.
Mais clareza.
```

### Escolha da Apresentação

| Apresentação | Use quando a prioridade é |
|---|---|
| Encaixe de Valor | mostrar a relação completa entre público, necessidade e solução |
| Necessidade Prioritária | abrir pela tarefa ou problema prático |
| Mecanismo de Valor | abrir pela solução e explicar como ela ajuda |
| Resultado Prático | abrir pelo benefício racional concreto |
| Segurança Emocional | reforçar controle, clareza, confiança, tranquilidade ou segurança |
| Progresso Aspiracional | reforçar autonomia, avanço, realização, conquista ou protagonismo |

Segurança Emocional e Progresso Aspiracional não devem ser selecionadas apenas por variedade. Elas dependem do estado emocional predominante no cadastro.

---

## 11. Como o cadastro percorre a arquitetura

```text
Produto + Público
↓
Apresentação
↓
Revisor
↓
Cenário + Copywriter
↓
TND
↓
Voz BB
↓
Tagline
↓
Headline
↓
CTA
```

### Papel de cada camada

| Camada | O que faz com o cadastro |
|---|---|
| Apresentação | organiza público, necessidade, solução e benefícios em uma proposição de valor |
| Revisor | corrige forma sem alterar sentido ou promessa |
| Cenário + Copywriter | desenvolve a proposta conforme uma estrutura persuasiva |
| TND | muda a rota de leitura sem mudar os fatos ou o nível de promessa |
| Voz BB | torna a mensagem institucional, clara, humana e proporcional |
| Tagline | destila um único eixo de valor |
| Headline | cria um gancho imediato alinhado à tagline |
| CTA | escolhe o próximo passo mais específico e proporcional |

### O que o cadastro não deve fazer

O cadastro não deve tentar escrever a campanha inteira, escolher uma TND, simular uma tagline ou incluir CTA de botão.

Ele deve fornecer uma base forte para que os agentes façam isso depois.

---

## 12. Relação com a CTA

A CTA é gerada no fim da arquitetura. Ela não deve ser escrita dentro dos seis campos.

Ainda assim, a necessidade racional precisa ser concreta o suficiente para orientar a ação futura.

| Tema de Educação Financeira | CTA principal de referência |
|---|---|
| Categorização dos Gastos | Organizar meus gastos |
| Gestão do Orçamento | Planejar meu mês |
| Uso Consciente do Crédito | Revisar meu crédito |
| Consumo Planejado | Planejar uma compra |
| Formação de Reserva | Começar minha reserva |

Essas CTAs representam a prática que a orientação busca iniciar. Elas podem ser mantidas em uma tabela de ação separada, sem contaminar os campos de produto e público.

---

## 13. Exemplos completos

### Exemplo A — Produto bancário: Open Finance BB

```text
PRODUTO_DESCRIÇÃO
Um serviço que permite ao BB considerar informações financeiras que você tem em outros bancos ao avaliar crédito.

BENEFÍCIO_RACIONAL
A possibilidade de aumentar o limite de crédito, se a análise aprovar.

BENEFÍCIO_EMOCIONAL
Mais confiança para buscar crédito usando um histórico financeiro mais completo.

PÚBLICO_DESCRIÇÃO
Pessoas que mantêm parte do histórico financeiro em outras instituições.

NECESSIDADE_RACIONAL
Usar o histórico financeiro de outros bancos para apoiar a busca por crédito.

NECESSIDADE_EMOCIONAL
Mais segurança para avaliar opções de crédito.
```

### Exemplo B — Produto educativo: Categorização dos Gastos

```text
PRODUTO_DESCRIÇÃO
Uma orientação de Educação Financeira para organizar os gastos do mês em grupos, como alimentação, transporte, contas e lazer.

BENEFÍCIO_RACIONAL
Uma visão dos gastos que se repetem e dos que ocupam mais espaço no mês.

BENEFÍCIO_EMOCIONAL
Mais segurança para decidir o que manter ou ajustar no mês.

PÚBLICO_DESCRIÇÃO
Pessoas que querem entender melhor gastos que se repetem no mês.

NECESSIDADE_RACIONAL
Categorizar as despesas do período para identificar para onde o dinheiro está indo.

NECESSIDADE_EMOCIONAL
Mais controle sobre o próprio dinheiro.
```

### Teste do Exemplo B na Apresentação

```text
Para pessoas que querem entender melhor gastos que se repetem no mês,
quando precisam categorizar as despesas do período para identificar para onde
o dinheiro está indo e buscam mais controle sobre o próprio dinheiro, uma
orientação de Educação Financeira para organizar os gastos do mês em grupos,
como alimentação, transporte, contas e lazer, oferece uma visão dos gastos que
se repetem e dos que ocupam mais espaço no mês, favorecendo mais segurança
para decidir o que manter ou ajustar no mês.
```

O texto-base pode ser longo. Isso é esperado. A Apresentação prova a integridade da cadeia; Copywriter, TND e Voz BB serão responsáveis por torná-la mais natural e persuasiva depois.

---

## 14. Checklist final de aprovação

A ficha só pode seguir para a arquitetura quando todas as respostas forem positivas.

### Produto

- [ ] A descrição explica o que é em linguagem leiga?
- [ ] O mecanismo está claro sem termos técnicos desnecessários?
- [ ] O benefício racional é uma entrega concreta e única?
- [ ] O benefício racional evita abstrações como “mais clareza” ou “mais facilidade”?
- [ ] O benefício emocional é plausível e não garantido?

### Público

- [ ] A descrição mostra uma situação reconhecível?
- [ ] A linguagem evita diagnóstico, julgamento e invasão?
- [ ] A necessidade racional é uma tarefa prática única?
- [ ] A necessidade emocional tem apenas um eixo predominante?

### Integração

- [ ] Cada campo acrescenta informação nova?
- [ ] A relação Produto + Público está clara?
- [ ] O cadastro encaixa gramaticalmente nas Apresentações?
- [ ] O benefício racional funciona como objeto de “oferece” e “acessam”?
- [ ] A necessidade racional permite inferir uma CTA futura sem conter CTA?
- [ ] O texto preserva o nível real de promessa da solução?

---

## 15. Regra final

> O cadastro não deve tentar parecer publicitário.  
> Ele deve ser específico, compreensível e útil.

Quando a base é forte, a arquitetura consegue criar diferentes mensagens sem inventar fatos, sem repetir os mesmos argumentos e sem transformar a comunicação em linguagem genérica.
