# APRESENTAÇÃO

## Objetivo

A apresentação transforma seis dados fixos de público e produto em uma proposição de valor com direção estratégica própria.

Ela define:

* Qual ideia abre a comunicação;
* Qual relação de valor recebe prioridade;
* Qual percurso mental o copywriter deve preservar;
* Como o mesmo conjunto de dados pode gerar entradas realmente diferentes.

A apresentação não cria fatos, provas, promessas, urgência ou benefícios novos.

---

## Placeholders obrigatórios

Todos os modelos devem usar exatamente estes seis placeholders:

```text
{PH_PBCO_DCR}
{PH_PBCO_RCNL}
{PH_PBCO_EMOC}
{PH_SGT_DCR}
{PH_SGT_RCNL}
{PH_SGT_EMOC}
```

---

## Contrato semântico dos placeholders

| Placeholder      | Significado                                       | Forma recomendada                                               |
| ---------------- | ------------------------------------------------- | --------------------------------------------------------------- |
| `{PH_PBCO_DCR}`  | Perfil situacional do público                     | “pessoas que usam limite especial”                              |
| `{PH_PBCO_RCNL}` | Necessidade prática, ação ou problema a resolver  | “organizar pagamentos sem depender do limite especial”          |
| `{PH_PBCO_EMOC}` | Estado emocional desejado                         | “mais controle sobre o orçamento”                               |
| `{PH_SGT_DCR}`   | Produto, serviço, orientação ou solução oferecida | “uma linha de crédito para substituir o uso do limite especial” |
| `{PH_SGT_RCNL}`  | Ganho funcional além da descrição da oferta       | “mais previsibilidade para planejar pagamentos”                 |
| `{PH_SGT_EMOC}`  | Efeito emocional favorecido pela solução          | “mais tranquilidade nas decisões”                               |

### Regra de não sobreposição

Cada placeholder precisa acrescentar uma informação nova.

```text
{PH_PBCO_DCR}
Identifica a condição que caracteriza o público.

{PH_PBCO_RCNL}
Mostra o que essa condição faz a pessoa precisar resolver.

{PH_SGT_DCR}
Identifica qual oferta é apresentada.

{PH_SGT_RCNL}
Explica qual resultado prático a oferta favorece.

{PH_PBCO_EMOC}
Mostra como a pessoa quer se sentir.

{PH_SGT_EMOC}
Indica qual efeito emocional a oferta pode gerar.
```

---

## Schema da apresentação

| Campo               | Descrição                                        |
| ------------------- | ------------------------------------------------ |
| `NM_APSC_PDRO`      | Nome da apresentação                             |
| `TX_FUC_OPRL_APSC`  | Intenção e função estratégica                    |
| `TX_DCR_DETD_APSC`  | Estrutura com os seis placeholders               |
| `TX_RCPO_PDRO_APSC` | Palavras-chave para classificação e recomendação |

---

# Modelos de apresentação

## 1. Encaixe de Valor

### `NM_APSC_PDRO`

Encaixe de Valor

### `TX_FUC_OPRL_APSC`

**Intenção:** mostrar por que a solução faz sentido para esse público.

**Função:** apresentar o público, contextualizar sua necessidade prática e seu estado desejado, introduzir a solução e concluir com os benefícios racional e emocional.

### `TX_DCR_DETD_APSC`

```text
Para {PH_PBCO_DCR}, quando precisam {PH_PBCO_RCNL} e buscam {PH_PBCO_EMOC}, {PH_SGT_DCR} oferece {PH_SGT_RCNL}, favorecendo {PH_SGT_EMOC}.
```

### `TX_RCPO_PDRO_APSC`

```text
encaixe, proposta de valor, adequação, correspondência, contexto, clareza
```

### Usar quando

A comunicação precisa apresentar a relação completa entre público, necessidade e solução.

---

## 2. Necessidade Prioritária

### `NM_APSC_PDRO`

Necessidade Prioritária

### `TX_FUC_OPRL_APSC`

**Intenção:** fazer a necessidade prática ocupar o centro da comunicação.

**Função:** abrir pela necessidade do público, contextualizar quem vive essa situação, apresentar a solução e demonstrar seus ganhos práticos e emocionais.

### `TX_DCR_DETD_APSC`

```text
Quando precisam {PH_PBCO_RCNL}, {PH_PBCO_DCR} encontram em {PH_SGT_DCR} uma alternativa que oferece {PH_SGT_RCNL}, gera {PH_SGT_EMOC} e apoia {PH_PBCO_EMOC}.
```

### `TX_RCPO_PDRO_APSC`

```text
necessidade, problema, dificuldade, desafio, resposta, resolução
```

### Usar quando

A dor, tarefa ou obstáculo precisa abrir a leitura antes da solução.

---

## 3. Mecanismo de Valor

### `NM_APSC_PDRO`

Mecanismo de Valor

### `TX_FUC_OPRL_APSC`

**Intenção:** explicar o que a solução oferece e por que isso importa.

**Função:** apresentar primeiro a oferta e seu benefício racional, relacionar a entrega à necessidade do público e fechar com os ganhos emocionais.

### `TX_DCR_DETD_APSC`

```text
Com {PH_SGT_DCR}, {PH_PBCO_DCR} acessam {PH_SGT_RCNL} para {PH_PBCO_RCNL}, gerando {PH_SGT_EMOC} e apoiando {PH_PBCO_EMOC}.
```

### `TX_RCPO_PDRO_APSC`

```text
mecanismo, funcionalidade, capacidade, entrega, utilidade, funcionamento
```

### Usar quando

O benefício racional é concreto e a pessoa precisa entender como a solução gera valor.

---

## 4. Resultado Prático

### `NM_APSC_PDRO`

Resultado Prático

### `TX_FUC_OPRL_APSC`

**Intenção:** tornar a mudança operacional o protagonista da mensagem.

**Função:** abrir pelo ganho prático, explicar para quem ele importa e em qual necessidade atua, apresentar a solução e concluir com os benefícios emocionais.

### `TX_DCR_DETD_APSC`

```text
{PH_SGT_RCNL} ajuda {PH_PBCO_DCR} a {PH_PBCO_RCNL}. Com {PH_SGT_DCR}, isso pode gerar {PH_SGT_EMOC} e apoiar {PH_PBCO_EMOC}.
```

### `TX_RCPO_PDRO_APSC`

```text
resultado, eficiência, rotina, praticidade, impacto funcional, clareza
```

### Usar quando

O ganho prático é mais relevante que a descrição da oferta.

---

## 5. Segurança Emocional

### `NM_APSC_PDRO`

Segurança Emocional

### `TX_FUC_OPRL_APSC`

**Intenção:** reduzir incerteza e reforçar cuidado, clareza ou controle.

**Função:** abrir pelo estado emocional que o público busca, contextualizar a necessidade prática, apresentar a solução e mostrar como ela favorece um ganho racional e emocional.

### `TX_DCR_DETD_APSC`

```text
Para buscar {PH_PBCO_EMOC} quando precisam {PH_PBCO_RCNL}, {PH_PBCO_DCR} contam com {PH_SGT_DCR}, que oferece {PH_SGT_RCNL} e favorece {PH_SGT_EMOC}.
```

### `TX_RCPO_PDRO_APSC`

```text
segurança, controle, clareza, tranquilidade, confiança, alívio
```

### Usar quando

`{PH_PBCO_EMOC}` estiver ligado a segurança, controle, clareza, confiança ou tranquilidade.

### Não usar quando

O estado desejado for conquista, reconhecimento, avanço ou autonomia.

---

## 6. Progresso Aspiracional

### `NM_APSC_PDRO`

Progresso Aspiracional

### `TX_FUC_OPRL_APSC`

**Intenção:** conectar a solução ao futuro desejado e ao avanço da pessoa.

**Função:** abrir pelo estado desejado, contextualizar quem é o público e qual necessidade precisa ser enfrentada, apresentar a solução e reforçar seus ganhos racionais e emocionais.

### `TX_DCR_DETD_APSC`

```text
No caminho para {PH_PBCO_EMOC}, {PH_PBCO_DCR} podem {PH_PBCO_RCNL} com o apoio de {PH_SGT_DCR}, que oferece {PH_SGT_RCNL} e gera {PH_SGT_EMOC}.
```

### `TX_RCPO_PDRO_APSC`

```text
progresso, autonomia, evolução, futuro, conquista, protagonismo
```

### Usar quando

`{PH_PBCO_EMOC}` estiver ligado a avanço, autonomia, realização, conquista ou protagonismo.

### Não usar quando

O foco for risco, proteção, contenção de danos ou alívio de preocupação.
