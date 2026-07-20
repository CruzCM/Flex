# Alteração das Regras de Pontuação

## 1. Objetivo da alteração

As regras de pontuação devem ser ajustadas para manter as movimentações do período como principal fundamento da recomendação e utilizar o perfil financeiro apenas como um reforço de personalização.

A nova estrutura continuará utilizando três componentes:

1. Pontuação por Concentração;
2. Pontuação por Orçamento;
3. Pontuação por Perfil.

A lógica geral será:

> **A concentração identifica o sinal do período, o orçamento reforça o contexto financeiro e o perfil ajuda a diferenciar clientes com movimentações semelhantes.**

O perfil poderá alterar o resultado quando os temas estiverem empatados ou com pontuações próximas, mas não deverá superar sozinho um sinal mais forte das movimentações.

Nesta etapa, não deverá ser implementada nenhuma regra de desempate. Caso dois ou mais temas terminem com a mesma pontuação, o empate deverá ser mantido para avaliação posterior da área de negócio.

---

# 2. Pontuação por Concentração

## Regra mantida sem alteração

A Pontuação por Concentração não será alterada.

Os percentuais continuarão sendo calculados sobre a composição das saídas:

| Indicador | Cálculo mantido |
|---|---|
| Percentual de Saída Genérica | Valor de Saída Genérica dividido pelo Valor de Saída Total |
| Percentual de Saída Essencial | Valor de Saída Essencial dividido pelo Valor de Saída Total |
| Percentual de Saída Flexível | Valor de Saída Flexível dividido pelo Valor de Saída Total |
| Percentual de Saída para Reserva | Valor de Saída para Reserva dividido pelo Valor de Saída Total |
| Percentual de Saída com Crédito | Valor de Saída com Dívidas ou Crédito dividido pelo Valor de Saída Total |

Quando o Valor de Saída Total for igual a zero, todos os percentuais e todas as pontuações por concentração continuarão sendo iguais a zero.

As referências, faixas e pontuações atuais serão mantidas.

---

## 2.1. Categorização dos Gastos

Campo:

`NR_PONT_CONC_GEN`

| Percentual de saída genérica | Pontuação |
|---|---:|
| Menor ou igual a 75% | 0 |
| Maior que 75% | 99 |

A regra permanece sem alteração.

A pontuação `99` continuará representando prioridade para o tema Categorização dos Gastos.

---

## 2.2. Gestão do Orçamento

Campo:

`NR_PONT_CONC_ESS`

| Percentual de saída essencial | Pontuação |
|---|---:|
| Menor que 50% | 0 |
| Maior ou igual a 50% e menor que 75% | 1 |
| Maior ou igual a 75% | 2 |

A regra permanece sem alteração.

---

## 2.3. Consumo Planejado

Campo:

`NR_PONT_CONC_FLEX`

| Percentual de saída flexível | Pontuação |
|---|---:|
| Menor que 30% | 0 |
| Maior ou igual a 30% e menor que 45% | 1 |
| Maior ou igual a 45% | 2 |

A regra permanece sem alteração.

---

## 2.4. Formação de Reserva

Campo:

`NR_PONT_CONC_RES`

| Percentual de saída para reserva | Pontuação |
|---|---:|
| Maior ou igual a 30% | 0 |
| Maior ou igual a 20% e menor que 30% | 1 |
| Menor que 20% | 2 |

A regra permanece sem alteração.

A lógica continuará sendo inversa: quanto menor a participação das saídas destinadas à reserva ou ao futuro, maior será a pontuação.

---

## 2.5. Uso Consciente do Crédito

Campo:

`NR_PONT_CONC_CRED`

| Percentual de saída com crédito | Pontuação |
|---|---:|
| Menor que 30% | 0 |
| Maior ou igual a 30% e menor que 45% | 1 |
| Maior ou igual a 45% | 2 |

A regra permanece sem alteração.

---

# 3. Classificação do Orçamento

## Regra mantida sem alteração

A classificação do resultado do orçamento continuará sendo calculada pela relação entre o Valor de Saída Total e o Valor de Entrada Total.

| Relação entre saídas e entradas | Classificação |
|---|---|
| Menor que 0,95 | Superavitário |
| Maior ou igual a 0,95 e menor ou igual a 1,05 | Neutro |
| Maior que 1,05 | Deficitário |

Os limites utilizados para classificar o orçamento como Superavitário, Neutro ou Deficitário não serão alterados.

As classificações Forte e Fraco também poderão continuar sendo calculadas e armazenadas para acompanhamento, análise ou histórico.

A alteração será somente na pontuação: Forte e Fraco deixarão de acrescentar pontuações diferentes.

---

# 4. Nova Pontuação por Orçamento

A Pontuação por Orçamento será simplificada.

Ela poderá assumir somente os valores `0` ou `1`.

O resultado do orçamento deverá funcionar como reforço da leitura das movimentações, sem receber pesos diferentes para Forte ou Fraco.

---

## 4.1. Categorização dos Gastos

Campo:

`NR_PONT_ORC_GEN`

| Resultado do orçamento | Pontuação |
|---|---:|
| Superavitário | 0 |
| Neutro | 0 |
| Deficitário | 0 |

A Categorização dos Gastos continuará sem receber Pontuação por Orçamento.

---

## 4.2. Gestão do Orçamento

Campo:

`NR_PONT_ORC_ESS`

| Resultado do orçamento | Pontuação |
|---|---:|
| Superavitário | 0 |
| Neutro | 0 |
| Deficitário | 1 |

O orçamento deficitário acrescentará `1` ponto ao tema Gestão do Orçamento.

---

## 4.3. Consumo Planejado

Campo:

`NR_PONT_ORC_FLEX`

| Resultado do orçamento | Pontuação |
|---|---:|
| Superavitário | 0 |
| Neutro | 0 |
| Deficitário | 1 |

O orçamento deficitário acrescentará `1` ponto ao tema Consumo Planejado.

---

## 4.4. Formação de Reserva

Campo:

`NR_PONT_ORC_RES`

| Resultado do orçamento | Pontuação |
|---|---:|
| Superavitário | 1 |
| Neutro | 0 |
| Deficitário | 0 |

O orçamento superavitário acrescentará `1` ponto ao tema Formação de Reserva.

O orçamento deficitário não acrescentará ponto ao tema, pois um resultado negativo não representa espaço financeiro para reforçar a formação de reserva naquele período.

---

## 4.5. Uso Consciente do Crédito

Campo:

`NR_PONT_ORC_CRED`

| Resultado do orçamento | Pontuação |
|---|---:|
| Superavitário | 0 |
| Neutro | 0 |
| Deficitário | 1 |

O orçamento deficitário acrescentará `1` ponto ao tema Uso Consciente do Crédito.

---

## 4.6. Resumo da Pontuação por Orçamento

| Resultado do orçamento | Gestão do Orçamento | Consumo Planejado | Formação de Reserva | Uso Consciente do Crédito |
|---|---:|---:|---:|---:|
| Deficitário | 1 | 1 | 0 | 1 |
| Neutro | 0 | 0 | 0 | 0 |
| Superavitário | 0 | 0 | 1 | 0 |

A Pontuação por Orçamento terá peso máximo de `1` ponto em qualquer tema.

---

# 5. Nova Pontuação por Perfil

A Pontuação por Perfil será totalmente revisada.

O perfil financeiro deverá funcionar como reforço de personalização e poderá acrescentar, no máximo, `1` ponto.

Nenhum perfil deverá receber `2` pontos.

Cada perfil completo poderá reforçar, no máximo, um tema. Não deverá existir pontuação principal e secundária para o mesmo perfil.

Essa regra busca impedir que um único perfil aumente vários temas simultaneamente e também evita que o perfil tenha mais peso do que as movimentações do período.

A pontuação deverá utilizar preferencialmente o perfil financeiro completo, considerando macroperfil e subperfil.

Quando o macroperfil estiver disponível, mas o subperfil não estiver disponível ou não estiver reconhecido, deverá ser utilizada a regra de fallback por macroperfil.

---

## 5.1. Pontuação por Perfil Completo

| Perfil financeiro completo | Gestão do Orçamento | Consumo Planejado | Formação de Reserva | Uso Consciente do Crédito |
|---|---:|---:|---:|---:|
| Endividado Consciente | 0 | 1 | 0 | 0 |
| Endividado Acrobata | 1 | 0 | 0 | 0 |
| Endividado Iminente | 0 | 0 | 0 | 1 |
| Endividado Inadimplente | 0 | 0 | 0 | 1 |
| Equilibrista | 0 | 0 | 1 | 0 |
| Equilibrista Equilibrista | 0 | 0 | 1 | 0 |
| Investidor Precavido | 0 | 0 | 0 | 0 |
| Investidor Protegido | 0 | 0 | 0 | 0 |
| Investidor Despreocupado | 0 | 0 | 0 | 0 |
| Investidor Acelerado | 0 | 0 | 0 | 0 |
| A Classificar | 0 | 0 | 0 | 0 |
| Sem perfil disponível | 0 | 0 | 0 | 0 |

---

## 5.2. Justificativa das relações entre Perfil e Tema

### Endividado Consciente

O perfil Endividado Consciente acrescentará `1` ponto ao tema Consumo Planejado.

Esse perfil possui dívidas pequenas ou controladas e não apresenta, pelo perfil isoladamente, a mesma relação de urgência com o crédito observada nos perfis Iminente ou Inadimplente.

O reforço em Consumo Planejado possui caráter preventivo e somente terá efeito na pontuação final quando já existir sinal de gastos flexíveis nas movimentações.

### Endividado Acrobata

O perfil Endividado Acrobata acrescentará `1` ponto ao tema Gestão do Orçamento.

Esse perfil apresenta comprometimento financeiro moderado. O tema Gestão do Orçamento permite uma orientação mais ampla sobre organização das despesas, acompanhamento e definição de prioridades.

### Endividado Iminente

O perfil Endividado Iminente acrescentará `1` ponto ao tema Uso Consciente do Crédito.

Esse perfil possui relação mais direta com alto comprometimento financeiro e risco de atraso.

### Endividado Inadimplente

O perfil Endividado Inadimplente acrescentará `1` ponto ao tema Uso Consciente do Crédito.

Esse perfil possui relação direta com operações em atraso e compromissos de crédito.

### Equilibrista

O perfil Equilibrista acrescentará `1` ponto ao tema Formação de Reserva.

Esse perfil possui relação direta com ausência ou insuficiência de reserva financeira para lidar com imprevistos.

### Investidores

Os perfis Investidor Precavido, Protegido, Despreocupado e Acelerado não acrescentarão pontos.

A existência de investimentos não deverá gerar automaticamente reforço para Formação de Reserva.

A baixa formação de reserva no período já é observada pela Pontuação por Concentração de Reserva. Por isso, não é necessário acrescentar um novo ponto apenas pelo cliente ser Investidor.

Além disso, os subperfis Investidores apresentam situações diferentes relacionadas a volume, liquidez, risco e composição dos investimentos, não sendo adequado direcioná-los automaticamente para um único tema do modelo atual.

---

## 5.3. Regra de Fallback por Macroperfil

A regra de perfil completo deverá ter prioridade.

O fallback será utilizado somente quando o macroperfil estiver disponível, mas o subperfil estiver ausente, inválido ou não reconhecido.

| Macroperfil disponível sem subperfil válido | Gestão do Orçamento | Consumo Planejado | Formação de Reserva | Uso Consciente do Crédito |
|---|---:|---:|---:|---:|
| Endividado | 0 | 0 | 0 | 1 |
| Equilibrista | 0 | 0 | 1 | 0 |
| Investidor | 0 | 0 | 0 | 0 |
| A Classificar | 0 | 0 | 0 | 0 |

No fallback, o macroperfil Endividado reforçará Uso Consciente do Crédito por ser a relação temática mais direta e institucionalmente reconhecida.

O macroperfil Equilibrista reforçará Formação de Reserva.

O macroperfil Investidor não acrescentará pontos, porque o macroperfil isolado não permite identificar a situação específica da reserva, da liquidez e do risco.

---

## 5.4. Regras por Campo

### Pontuação de Perfil Genérica

Campo:

`NR_PONT_PRFL_GEN`

A pontuação continuará sendo sempre igual a zero.

### Pontuação de Perfil Essencial

Campo:

`NR_PONT_PRFL_ESS`

Receberá `1` ponto somente para:

- Endividado Acrobata.

Nos demais casos, receberá zero.

### Pontuação de Perfil Flexível

Campo:

`NR_PONT_PRFL_FLEX`

Receberá `1` ponto somente para:

- Endividado Consciente.

Nos demais casos, receberá zero.

### Pontuação de Perfil de Reserva

Campo:

`NR_PONT_PRFL_RES`

Receberá `1` ponto somente para:

- Equilibrista;
- Equilibrista Equilibrista;
- macroperfil Equilibrista sem subperfil válido.

Nos demais casos, receberá zero.

### Pontuação de Perfil de Crédito

Campo:

`NR_PONT_PRFL_CRED`

Receberá `1` ponto somente para:

- Endividado Iminente;
- Endividado Inadimplente;
- macroperfil Endividado sem subperfil válido.

Nos demais casos, receberá zero.

---

# 6. Aplicação do Perfil na Pontuação Final

A Pontuação por Perfil não deverá criar sozinha um tema relevante.

O ponto de perfil somente deverá participar da Pontuação Final quando a Pontuação por Concentração do mesmo tema for maior que zero.

Quando a Pontuação por Concentração do tema for igual a zero, a Pontuação Final do tema também deverá ser igual a zero.

Essa regra será aplicada mesmo que o orçamento ou o perfil tenham recebido pontuação naquele tema.

| Pontuação por Concentração | Tratamento da Pontuação Final |
|---|---|
| Igual a 0 | Pontuação Final do tema será 0 |
| Maior que 0 | Somar Concentração, Orçamento e Perfil |

Essa regra garante que o perfil apenas fortaleça um sinal identificado nas movimentações.

---

# 7. Pontuação Final por Tema

## 7.1. Categorização dos Gastos

Campo final:

`NR_PONT_CATEG`

A regra permanece sem alteração.

A Pontuação Final será igual à Pontuação por Concentração Genérica:

**Pontuação Final de Categorização = Pontuação por Concentração Genérica**

| Pontuação por Concentração Genérica | Pontuação Final |
|---|---:|
| 0 | 0 |
| 99 | 99 |

A Categorização dos Gastos não receberá Pontuação por Orçamento nem Pontuação por Perfil.

---

## 7.2. Gestão do Orçamento

Campo final:

`NR_PONT_ORC`

Quando `NR_PONT_CONC_ESS` for igual a zero:

**Pontuação Final de Gestão do Orçamento = 0**

Quando `NR_PONT_CONC_ESS` for maior que zero:

**Pontuação Final de Gestão do Orçamento = Pontuação por Concentração Essencial + Pontuação por Orçamento Essencial + Pontuação por Perfil Essencial**

| Componente | Faixa |
|---|---:|
| Pontuação por Concentração Essencial | 0 a 2 |
| Pontuação por Orçamento Essencial | 0 ou 1 |
| Pontuação por Perfil Essencial | 0 ou 1 |
| Pontuação Final possível | 0 a 4 |

---

## 7.3. Consumo Planejado

Campo final:

`NR_PONT_CONS`

Quando `NR_PONT_CONC_FLEX` for igual a zero:

**Pontuação Final de Consumo Planejado = 0**

Quando `NR_PONT_CONC_FLEX` for maior que zero:

**Pontuação Final de Consumo Planejado = Pontuação por Concentração Flexível + Pontuação por Orçamento Flexível + Pontuação por Perfil Flexível**

| Componente | Faixa |
|---|---:|
| Pontuação por Concentração Flexível | 0 a 2 |
| Pontuação por Orçamento Flexível | 0 ou 1 |
| Pontuação por Perfil Flexível | 0 ou 1 |
| Pontuação Final possível | 0 a 4 |

---

## 7.4. Formação de Reserva

Campo final:

`NR_PONT_RES`

Quando `NR_PONT_CONC_RES` for igual a zero:

**Pontuação Final de Formação de Reserva = 0**

Quando `NR_PONT_CONC_RES` for maior que zero:

**Pontuação Final de Formação de Reserva = Pontuação por Concentração de Reserva + Pontuação por Orçamento de Reserva + Pontuação por Perfil de Reserva**

| Componente | Faixa |
|---|---:|
| Pontuação por Concentração de Reserva | 0 a 2 |
| Pontuação por Orçamento de Reserva | 0 ou 1 |
| Pontuação por Perfil de Reserva | 0 ou 1 |
| Pontuação Final possível | 0 a 4 |

---

## 7.5. Uso Consciente do Crédito

Campo final:

`NR_PONT_CRED`

Quando `NR_PONT_CONC_CRED` for igual a zero:

**Pontuação Final de Uso Consciente do Crédito = 0**

Quando `NR_PONT_CONC_CRED` for maior que zero:

**Pontuação Final de Uso Consciente do Crédito = Pontuação por Concentração de Crédito + Pontuação por Orçamento de Crédito + Pontuação por Perfil de Crédito**

| Componente | Faixa |
|---|---:|
| Pontuação por Concentração de Crédito | 0 a 2 |
| Pontuação por Orçamento de Crédito | 0 ou 1 |
| Pontuação por Perfil de Crédito | 0 ou 1 |
| Pontuação Final possível | 0 a 4 |

---

# 8. Empates entre Temas

Nesta alteração, não deverá ser implementada nenhuma regra de desempate.

Caso dois ou mais temas apresentem a mesma Pontuação Final, todos deverão permanecer com a pontuação calculada.

O processamento não deverá:

- escolher automaticamente um dos temas empatados;
- aplicar uma ordem fixa de prioridade;
- utilizar o perfil novamente para desempatar;
- utilizar a maior concentração como desempate;
- selecionar o primeiro tema pela ordem dos campos;
- substituir uma pontuação empatada por outra.

Os campos de Pontuação Final deverão ser entregues com seus valores originais para que a área de negócio avalie posteriormente como os empates serão tratados.

---

# 9. Pontuações Máximas

| Tema | Concentração | Orçamento | Perfil | Pontuação máxima |
|---|---:|---:|---:|---:|
| Categorização dos Gastos | 0 ou 99 | 0 | 0 | 99 |
| Gestão do Orçamento | 0 a 2 | 0 ou 1 | 0 ou 1 | 4 |
| Consumo Planejado | 0 a 2 | 0 ou 1 | 0 ou 1 | 4 |
| Formação de Reserva | 0 a 2 | 0 ou 1 | 0 ou 1 | 4 |
| Uso Consciente do Crédito | 0 a 2 | 0 ou 1 | 0 ou 1 | 4 |

Os quatro temas principais passarão a ter a mesma pontuação máxima.

---

# 10. Resumo das Regras Mantidas

As seguintes regras não serão alteradas:

1. O cálculo dos percentuais de concentração.
2. O uso do Valor de Saída Total como denominador das concentrações.
3. As referências de concentração.
4. As faixas de Pontuação por Concentração.
5. A Pontuação por Concentração entre `0`, `1` e `2`.
6. A Pontuação de Categorização entre `0` e `99`.
7. O tratamento de Valor de Saída Total igual a zero.
8. Os limites de classificação do orçamento como Superavitário, Neutro ou Deficitário.
9. O cálculo dos campos Forte e Fraco para fins analíticos, caso seja necessário mantê-los.
10. Os nomes dos campos atuais de pontuação.

---

# 11. Resumo das Regras Alteradas

As seguintes regras deverão ser alteradas:

1. Forte e Fraco deixarão de influenciar a Pontuação por Orçamento.
2. A Pontuação por Orçamento passará a variar somente entre `0` e `1`.
3. O orçamento neutro deixará de acrescentar pontos.
4. O orçamento deficitário acrescentará `1` ponto a Gestão do Orçamento, Consumo Planejado e Uso Consciente do Crédito.
5. O orçamento superavitário acrescentará `1` ponto a Formação de Reserva.
6. A Pontuação por Perfil passará a ter valor máximo igual a `1`.
7. Nenhum perfil receberá `2` pontos.
8. Cada perfil completo reforçará, no máximo, um tema.
9. O perfil completo será utilizado antes do macroperfil.
10. O macroperfil será utilizado como fallback quando não existir subperfil válido.
11. Os perfis Investidores não acrescentarão pontos.
12. O perfil somente participará da Pontuação Final quando o tema apresentar Pontuação por Concentração maior que zero.
13. Quando a Pontuação por Concentração for igual a zero, a Pontuação Final do tema será igual a zero.
14. Os quatro temas principais terão pontuação máxima igual a `4`.
15. Os empates serão mantidos e não deverão ser resolvidos nesta etapa.

---

# 12. Regra Final Consolidada

A Pontuação Final seguirá a seguinte lógica:

- A Pontuação por Concentração continuará sendo o principal componente.
- A Pontuação por Orçamento acrescentará, no máximo, `1` ponto.
- A Pontuação por Perfil acrescentará, no máximo, `1` ponto.
- O perfil poderá diferenciar clientes com movimentações semelhantes.
- O perfil não poderá criar sozinho um tema sem sinal de concentração.
- Nenhum perfil poderá reforçar mais de um tema.
- Os Investidores não receberão reforço automático em Formação de Reserva.
- A classificação Forte ou Fraco não participará mais da pontuação.
- O orçamento neutro não acrescentará pontos.
- Quando houver empate, o empate deverá ser preservado.

O princípio final será:

> **A movimentação define os temas relevantes, o orçamento reforça o contexto e o perfil diferencia clientes com sinais semelhantes, sem substituir a evidência do período.**
