# Catálogo Técnico-Funcional de Apresentações, Cenários e Tendências Cognitivas

> Documentação dos elementos que orientam a geração de insights no Genera.
>
> Foco do documento: **Apresentações**, **Cenários** e **Tendências Cognitivas**.
>
> Produto, Público, Voz BB, Mensagem, Título, CTA, Curadoria e Aprovação aparecem apenas para contextualizar a esteira de geração.

---

## Índice

1. [Fluxograma da geração](#fluxograma-da-geração)
2. [Produto e Público como insumos](#produto-e-público-como-insumos)
3. [Camada 1 — Apresentações](#camada-1--apresentações)
4. [Camada 2 — Cenários](#camada-2--cenários)
5. [Camada 3 — Tendências Cognitivas](#camada-3--tendências-cognitivas)
6. [Síntese das camadas](#síntese-das-camadas)
7. [Regras de governança](#regras-de-governança)
8. [Glossário essencial](#glossário-essencial)

---

# Fluxograma da geração

## Leitura principal

A geração de insights não começa em uma tela em branco.

Ela parte de dados de negócio já cadastrados, organiza esses dados em uma proposta de valor, aplica uma lógica narrativa e, depois, cria 10 alternativas a partir de tendências cognitivas diferentes.

O ponto mais importante é:

> **As 10 mensagens podem mudar de forma, mas precisam preservar o mesmo significado.**

---

## Fluxograma técnico-funcional

```mermaid
flowchart TD

    %% =========================
    %% INSUMOS
    %% =========================
    subgraph S0["0. Insumos de negócio"]
        P["Produto cadastrado<br/>Descrição<br/>Benefício racional<br/>Benefício emocional"]
        U["Público cadastrado<br/>Descrição<br/>Necessidade racional<br/>Necessidade emocional"]
    end

    %% =========================
    %% BRIEFING
    %% =========================
    subgraph S1["1. Briefing da recomendação"]
        B["Briefing<br/>Produto + Público<br/>Apresentação + Cenário<br/>Limites + Vigência"]
    end

    %% =========================
    %% APLICAÇÃO
    %% =========================
    subgraph S2["2. Montagem pela aplicação"]
        APSC["Tipo de apresentação<br/>APSC_TCN"]
        AP["Apresentação preenchida<br/>com placeholders oficiais"]
    end

    %% =========================
    %% BASE NEUTRA
    %% =========================
    subgraph S3["3. Base neutra"]
        REV["Etapa 1<br/>Revisão da apresentação"]
        CNR["Tipo de cenário<br/>CNR_TCN"]
        BASE["Etapa 2<br/>Base sem viés"]
        CKP["Checkpoint-base<br/>referência comum"]
    end

    %% =========================
    %% LOOP TENDENCIAS
    %% =========================
    subgraph S4["4. Loop por tendência cognitiva"]
        LOOP{"Executar para cada<br/>TND_CGTV_TCN"}
        TND["Tendência cognitiva<br/>Contraste, Curiosidade,<br/>Especificidade..."]
        BIAS["Etapa 3<br/>Base com viés"]
        BB["Etapa 4<br/>Voz BB"]
        MSG["Etapa 5<br/>Mensagem"]
        TIT["Etapa 6<br/>Título"]
        CTA["Etapa 7<br/>CTA"]
        ALT["Alternativa gerada<br/>Tendência + Título + Mensagem + CTA"]
    end

    %% =========================
    %% SAIDA
    %% =========================
    subgraph S5["5. Saída operacional"]
        LISTA["Lista com 10 alternativas"]
        CUR["Curadoria humana<br/>seleciona 1 mensagem"]
        APR{"Decisão"}
        OK["Aprovar<br/>promove versão válida"]
        NOK["Reprovar<br/>mantém versão ativa"]
        BANCO["Banco de Insights<br/>status + versão + histórico"]
    end

    P --> B
    U --> B

    B --> APSC
    APSC --> AP

    AP --> REV
    REV --> BASE
    CNR --> BASE
    BASE --> CKP

    CKP --> LOOP
    LOOP --> TND
    TND --> BIAS
    BIAS --> BB
    BB --> MSG
    MSG --> TIT
    TIT --> CTA
    CTA --> ALT

    ALT --> LISTA
    LISTA --> CUR
    CUR --> APR
    APR --> OK
    APR --> NOK
    OK --> BANCO
    NOK --> BANCO
```

---

## Versão textual do fluxo

```text
Produto + Público
        |
        v
Briefing da recomendação
        |
        v
Tipo de apresentação
        |
        v
Apresentação preenchida pela aplicação
        |
        v
Revisão da apresentação
        |
        v
Tipo de cenário narrativo
        |
        v
Base sem viés
        |
        v
Checkpoint-base
        |
        v
Loop por tendência cognitiva
        |
        v
Base com viés
        |
        v
Voz BB
        |
        v
Mensagem
        |
        v
Título
        |
        v
CTA
        |
        v
10 alternativas geradas
        |
        v
Curadoria
        |
        v
Aprovação ou reprovação
        |
        v
Banco de Insights atualizado
```

---

## O que cada camada decide

| Camada | Decide | Não decide |
|---|---|---|
| Produto | O que será comunicado | Forma da mensagem |
| Público | Para quem será comunicado | Rota narrativa |
| Apresentação | Como organizar a proposta de valor inicial | Viés cognitivo |
| Cenário | Como desenvolver a narrativa | Título e CTA finais |
| Tendência Cognitiva | Qual rota de leitura será aplicada | Novo benefício ou nova promessa |
| Voz BB | Como institucionalizar a linguagem | Alteração de significado |
| Mensagem, Título e CTA | Como materializar o insight | Nova regra de negócio |
| Curadoria | Qual alternativa seguirá no fluxo | Geração automática sem decisão humana |
| Aprovação | Se a versão proposta vira válida | Ativação sem governança |

---

## Fala sugerida

> “Este fluxograma mostra a geração de ponta a ponta.
>
> O processo começa com Produto e Público, que são os insumos de negócio. Eles informam o que será comunicado e para quem.
>
> A partir disso, a aplicação monta o briefing e preenche o tipo de apresentação escolhido. A apresentação é a primeira organização da proposta de valor.
>
> Depois, a IA revisa essa apresentação e usa o cenário narrativo para criar uma base sem viés. Essa base vira um checkpoint, ou seja, uma referência comum para todas as próximas variações.
>
> Em seguida começa o loop por tendência cognitiva. Para cada tendência, o sistema cria uma base com viés, ajusta a linguagem em Voz BB e gera mensagem, título e CTA.
>
> No final, o Genera entrega 10 alternativas. Elas partem do mesmo briefing, mas cada uma apresenta o valor por uma rota cognitiva diferente.
>
> A partir daí, o usuário faz a curadoria, escolhe uma alternativa e segue para aprovação ou reprovação.
>
> A lógica central é: Produto e Público definem o conteúdo; Apresentação organiza; Cenário narra; Tendência Cognitiva enquadra; e a governança controla o que entra em operação.”

---

# Produto e Público como insumos

Produto e Público são a base de negócio da geração.

Eles não são tipos de geração. Eles apenas fornecem o conteúdo que será organizado pelas Apresentações, desenvolvido pelos Cenários e enquadrado pelas Tendências Cognitivas.

---

## Produto

O Produto representa a solução, serviço, funcionalidade ou orientação que poderá ser recomendada.

| Elemento | Papel |
|---|---|
| Descrição | Explica o que é a solução |
| Benefício racional | Explica o que ela permite fazer |
| Benefício emocional | Explica o efeito emocional associado |

Placeholders usados:

```text
{PH_SGT_DCR}
{PH_SGT_RCNL}
{PH_SGT_EMOC}
```

---

## Público

O Público representa o grupo ou situação de usuário para quem a recomendação será direcionada.

| Elemento | Papel |
|---|---|
| Descrição | Explica quem é ou em qual situação está |
| Necessidade racional | Explica o que precisa resolver |
| Necessidade emocional | Explica o estado emocional buscado |

Placeholders usados:

```text
{PH_PBCO_DCR}
{PH_PBCO_RCNL}
{PH_PBCO_EMOC}
```

---

## Síntese

```text
Produto + Público = contexto de negócio

Apresentação = primeira organização desse contexto em proposta de valor
```

---

# Camada 1 — Apresentações

## O que são Apresentações

As Apresentações são modelos estruturados que organizam Produto e Público em uma primeira proposta de valor.

Elas determinam por qual ponto a comunicação começa:

- pelo encaixe entre público e produto;
- pela necessidade do público;
- pelo mecanismo da solução;
- pelo resultado prático;
- pelo estado emocional buscado;
- pelo progresso desejado.

---

## Por que as Apresentações existem

As Apresentações existem para evitar que a geração comece de forma aberta demais.

Elas oferecem uma frase-mãe estruturada, preenchida pela aplicação com os dados de Produto e Público, antes da criação narrativa da IA.

A Apresentação não é a mensagem final.

Ela é a primeira organização estratégica da proposta de valor.

---

## O que a Apresentação controla

| Elemento | Como a Apresentação controla |
|---|---|
| Ordem das ideias | Define se a mensagem começa pelo público, necessidade, solução, resultado ou emoção |
| Proposta de valor | Conecta público, produto, necessidade e benefício |
| Fidelidade de significado | Usa apenas dados estruturados já cadastrados |
| Base para a IA | Entrega um texto inicial para revisão e copywriting |

---

## O que a Apresentação não faz

- Não cria benefício novo.
- Não define a tendência cognitiva.
- Não define o CTA.
- Não substitui a Voz BB.
- Não decide a headline final.
- Não altera os dados de Produto ou Público.
- Não deve introduzir promessa que não exista nos insumos.

---

## Placeholders oficiais usados nas Apresentações

```text
{PH_SGT_DCR}
{PH_SGT_RCNL}
{PH_SGT_EMOC}
{PH_PBCO_DCR}
{PH_PBCO_RCNL}
{PH_PBCO_EMOC}
```

---

## Tipos oficiais de Apresentação

| ID | Tipo de apresentação | Função oficial |
|---:|---|---|
| 3049 | Encaixe de Valor | Juntar publico, necessidade, solucao e beneficio. |
| 3050 | Necessidade Prioritaria | Abrir pela necessidade racional do publico. |
| 3051 | Mecanismo de Valor | Abrir pelo mecanismo ou solucao. |
| 3052 | Resultado Pratico | Abrir pelo resultado funcional. |
| 3053 | Seguranca Emocional | Abrir pelo estado emocional buscado. |
| 3054 | Progresso Aspiracional | Abrir pela direcao de progresso. |

---

## 3049 — Encaixe de Valor

### Identificação

| Campo | Valor |
|---|---|
| Tabela | `APSC_TCN` |
| ID | `3049` |
| Nome | Encaixe de Valor |
| Função oficial | Juntar publico, necessidade, solucao e beneficio. |

### Texto oficial

```text
Para {PH_PBCO_DCR}, quando precisam {PH_PBCO_RCNL} e buscam {PH_PBCO_EMOC}, {PH_SGT_DCR} oferece {PH_SGT_RCNL}, favorecendo {PH_SGT_EMOC}.
```

### O que é

É a apresentação mais equilibrada. Ela conecta público, necessidade racional, necessidade emocional, produto, benefício racional e benefício emocional em uma única estrutura.

### Por que existe

Existe para criar uma visão completa da proposta de valor sem privilegiar apenas um elemento.

### O que faz na geração

- Mostra para quem a recomendação é feita.
- Explica a necessidade do público.
- Apresenta a solução.
- Conecta o benefício funcional ao efeito emocional.

### Quando usar

Use quando a recomendação precisa mostrar o encaixe completo entre público e produto, sem enfatizar apenas necessidade, mecanismo ou emoção.

### O que não faz

- Não intensifica a emoção.
- Não transforma o benefício em promessa garantida.
- Não cria urgência.
- Não altera os dados estruturados.

---

## 3050 — Necessidade Prioritaria

### Identificação

| Campo | Valor |
|---|---|
| Tabela | `APSC_TCN` |
| ID | `3050` |
| Nome | Necessidade Prioritaria |
| Função oficial | Abrir pela necessidade racional do publico. |

### Texto oficial

```text
Quando precisam {PH_PBCO_RCNL}, {PH_PBCO_DCR} encontram em {PH_SGT_DCR} uma alternativa que oferece {PH_SGT_RCNL}, gera {PH_SGT_EMOC} e apoia {PH_PBCO_EMOC}.
```

### O que é

É a apresentação que começa pela necessidade racional do público.

### Por que existe

Existe para colocar o problema prático ou a necessidade funcional como ponto de partida da comunicação.

### O que faz na geração

- Abre pelo que o público precisa resolver.
- Em seguida apresenta o produto como alternativa.
- Conecta o benefício racional ao efeito emocional.

### Quando usar

Use quando a recomendação deve partir de uma necessidade clara do usuário, como organizar, comparar, simular, planejar, consultar ou acompanhar.

### O que não faz

- Não dramatiza o problema.
- Não transforma necessidade em dor intensa.
- Não cria tom de urgência.
- Não promete solução automática.

---

## 3051 — Mecanismo de Valor

### Identificação

| Campo | Valor |
|---|---|
| Tabela | `APSC_TCN` |
| ID | `3051` |
| Nome | Mecanismo de Valor |
| Função oficial | Abrir pelo mecanismo ou solucao. |

### Texto oficial

```text
Com {PH_SGT_DCR}, {PH_PBCO_DCR} acessam {PH_SGT_RCNL} para {PH_PBCO_RCNL}, gerando {PH_SGT_EMOC} e apoiando {PH_PBCO_EMOC}.
```

### O que é

É a apresentação que começa pelo produto, serviço, funcionalidade ou mecanismo que permite entregar valor.

### Por que existe

Existe para destacar como a solução funciona antes de explicar o resultado para o público.

### O que faz na geração

- Coloca o produto em primeiro plano.
- Explica o benefício racional oferecido.
- Conecta o mecanismo à necessidade do público.
- Mantém o efeito emocional como consequência.

### Quando usar

Use quando a força da recomendação está no mecanismo, como app, cofrinho, parcelas, portabilidade, categorização, visualização ou simulação.

### O que não faz

- Não deve virar explicação técnica excessiva.
- Não transforma mecanismo em garantia.
- Não cria detalhe funcional inexistente.
- Não substitui o cenário FAB, embora combine bem com ele.

---

## 3052 — Resultado Pratico

### Identificação

| Campo | Valor |
|---|---|
| Tabela | `APSC_TCN` |
| ID | `3052` |
| Nome | Resultado Pratico |
| Função oficial | Abrir pelo resultado funcional. |

### Texto oficial

```text
{PH_SGT_RCNL} ajuda {PH_PBCO_DCR} a {PH_PBCO_RCNL}. Com {PH_SGT_DCR}, isso pode gerar {PH_SGT_EMOC} e apoiar {PH_PBCO_EMOC}.
```

### O que é

É a apresentação que começa pelo resultado funcional do produto.

### Por que existe

Existe para comunicar rapidamente o que a solução ajuda o público a fazer.

### O que faz na geração

- Abre pelo benefício racional.
- Relaciona o benefício ao público.
- Apresenta o produto como meio para esse resultado.
- Usa linguagem mais direta e prática.

### Quando usar

Use quando a mensagem precisa ser objetiva e orientada ao ganho prático.

### O que não faz

- Não deve prometer resultado garantido.
- Não deve usar linguagem absoluta.
- Não deve transformar ajuda em certeza.
- Não deve criar comparação com outras soluções.

---

## 3053 — Seguranca Emocional

### Identificação

| Campo | Valor |
|---|---|
| Tabela | `APSC_TCN` |
| ID | `3053` |
| Nome | Seguranca Emocional |
| Função oficial | Abrir pelo estado emocional buscado. |

### Texto oficial

```text
Para buscar {PH_PBCO_EMOC} quando precisam {PH_PBCO_RCNL}, {PH_PBCO_DCR} contam com {PH_SGT_DCR}, que oferece {PH_SGT_RCNL} e favorece {PH_SGT_EMOC}.
```

### O que é

É a apresentação que começa pelo estado emocional buscado pelo público.

### Por que existe

Existe para dar mais peso ao motivo emocional da recomendação, sem abandonar a necessidade racional.

### O que faz na geração

- Abre pelo estado emocional desejado.
- Relaciona esse estado à necessidade racional.
- Apresenta o produto como apoio.
- Mantém o benefício racional como sustentação.

### Quando usar

Use quando segurança, tranquilidade, confiança, clareza, motivação ou autonomia forem centrais na recomendação.

### O que não faz

- Não exagera emoção.
- Não cria medo.
- Não promete alívio garantido.
- Não substitui prova funcional por sentimento.

---

## 3054 — Progresso Aspiracional

### Identificação

| Campo | Valor |
|---|---|
| Tabela | `APSC_TCN` |
| ID | `3054` |
| Nome | Progresso Aspiracional |
| Função oficial | Abrir pela direcao de progresso. |

### Texto oficial

```text
No caminho para {PH_PBCO_EMOC}, {PH_PBCO_DCR} podem {PH_PBCO_RCNL} com o apoio de {PH_SGT_DCR}, que oferece {PH_SGT_RCNL} e gera {PH_SGT_EMOC}.
```

### O que é

É a apresentação que organiza a proposta como avanço ou caminho possível.

### Por que existe

Existe para posicionar a recomendação como apoio a uma evolução do usuário, sem prometer transformação garantida.

### O que faz na geração

- Abre pela direção de progresso.
- Mostra o público em movimento.
- Apresenta o produto como apoio.
- Conecta o avanço à necessidade racional e ao benefício emocional.

### Quando usar

Use quando a comunicação deve mostrar planejamento, avanço, organização, construção de reserva, conquista ou melhoria gradual.

### O que não faz

- Não garante mudança.
- Não promete transformação completa.
- Não cria antes e depois exagerado.
- Não substitui a Tendência Transformação.

---

# Camada 2 — Cenários

## O que são Cenários

Os Cenários definem a lógica narrativa da mensagem.

Se a Apresentação organiza a proposta de valor, o Cenário define como essa proposta será desenvolvida pela IA.

---

## Por que os Cenários existem

Os Cenários existem para controlar a forma narrativa da mensagem.

Eles ajudam a definir se o texto será:

- direto;
- estruturado em atenção, interesse, desejo e fechamento;
- organizado como antes, depois e ponte;
- construído a partir de característica, vantagem e benefício.

---

## Relação entre Apresentação e Cenário

```text
Apresentação = estrutura da proposta de valor

Cenário = estrutura narrativa da mensagem
```

A Apresentação responde o que precisa ser comunicado.

O Cenário responde como esse conteúdo será desenvolvido.

---

## O que o Cenário controla

| Elemento | Como o Cenário controla |
|---|---|
| Desenvolvimento narrativo | Define a progressão da mensagem |
| Ênfase argumentativa | Define se o foco está em valor, atenção, mudança possível ou mecanismo |
| Organização da copy | Orienta a forma de transformar a apresentação em base sem viés |
| Limites de persuasão | Impede exageros, medo, garantia ou CTA fora da etapa |

---

## O que o Cenário não faz

- Não define a tendência cognitiva.
- Não cria uma nova oferta.
- Não altera Produto ou Público.
- Não cria CTA operacional quando o cenário não permite.
- Não substitui a etapa de Voz BB.
- Não decide sozinho título, mensagem e CTA finais.

---

## Tipos oficiais de Cenário

| ID | Cenário | Função oficial | Descrição oficial |
|---:|---|---|---|
| 1017 | Copywriting Direto | Apresentar o valor central com clareza. | Valor central, relevancia, beneficio concreto e mensagem curta. |
| 1018 | AIDA | Guiar por atencao, interesse, desejo e fechamento natural. | Estrutura AIDA sem CTA operacional. |
| 1019 | BAB | Apresentar antes, depois possivel e ponte. | Estrutura BAB sem medo nem transformacao garantida. |
| 1020 | FAB | Conectar caracteristica, vantagem e beneficio. | Estrutura FAB para mecanismos como parcelas, cofrinho, cashback ou app. |

---

## 1017 — Copywriting Direto

### Identificação

| Campo | Valor |
|---|---|
| Tabela | `CNR_TCN` |
| ID | `1017` |
| Nome | Copywriting Direto |
| Função oficial | Apresentar o valor central com clareza. |
| Descrição oficial | Valor central, relevancia, beneficio concreto e mensagem curta. |

### O que é

É o cenário mais objetivo. Ele apresenta o valor central da recomendação com clareza e economia de linguagem.

### Por que existe

Existe para gerar uma base direta, adequada a comunicações curtas e interfaces com pouco espaço.

### O que faz na geração

- Preserva a ideia principal.
- Evita rodeios narrativos.
- Prioriza benefício concreto.
- Facilita a geração de mensagens curtas.

### Quando usar

Use quando o objetivo for clareza, objetividade e baixo esforço de leitura.

### O que não faz

- Não usa estrutura dramática.
- Não cria suspense.
- Não desenvolve uma narrativa longa.
- Não força gatilhos emocionais.

---

## 1018 — AIDA

### Identificação

| Campo | Valor |
|---|---|
| Tabela | `CNR_TCN` |
| ID | `1018` |
| Nome | AIDA |
| Função oficial | Guiar por atencao, interesse, desejo e fechamento natural. |
| Descrição oficial | Estrutura AIDA sem CTA operacional. |

### O que é

É o cenário que organiza a mensagem pela lógica Atenção, Interesse, Desejo e fechamento natural.

### Por que existe

Existe para dar uma progressão persuasiva ao texto sem antecipar o CTA operacional.

### O que faz na geração

- Cria uma abertura de atenção.
- Desenvolve interesse pelo valor.
- Mostra desejo ou relevância.
- Fecha de forma natural, sem comandar uma ação final.

### Quando usar

Use quando a comunicação precisa conduzir o usuário por uma progressão mais persuasiva, mas ainda controlada.

### O que não faz

- Não cria CTA operacional nesta etapa.
- Não usa urgência artificial.
- Não promete resultado garantido.
- Não deve parecer anúncio agressivo.

---

## 1019 — BAB

### Identificação

| Campo | Valor |
|---|---|
| Tabela | `CNR_TCN` |
| ID | `1019` |
| Nome | BAB |
| Função oficial | Apresentar antes, depois possivel e ponte. |
| Descrição oficial | Estrutura BAB sem medo nem transformacao garantida. |

### O que é

É o cenário que organiza a mensagem em Antes, Depois possível e Ponte.

### Por que existe

Existe para mostrar uma evolução possível entre uma situação atual e uma condição melhor organizada, usando o produto como ponte.

### O que faz na geração

- Mostra a situação inicial.
- Apresenta uma condição possível de melhoria.
- Posiciona a solução como ponte.
- Mantém cuidado para não prometer transformação garantida.

### Quando usar

Use quando a recomendação envolve organização, planejamento, comparação, clareza ou mudança gradual.

### O que não faz

- Não usa medo.
- Não cria cenário negativo exagerado.
- Não garante transformação.
- Não promete antes e depois absoluto.

---

## 1020 — FAB

### Identificação

| Campo | Valor |
|---|---|
| Tabela | `CNR_TCN` |
| ID | `1020` |
| Nome | FAB |
| Função oficial | Conectar caracteristica, vantagem e beneficio. |
| Descrição oficial | Estrutura FAB para mecanismos como parcelas, cofrinho, cashback ou app. |

### O que é

É o cenário que conecta Característica, Vantagem e Benefício.

### Por que existe

Existe para explicar valor a partir de um mecanismo concreto da solução.

### O que faz na geração

- Identifica a característica ou mecanismo.
- Mostra a vantagem prática.
- Conecta essa vantagem ao benefício do usuário.
- Funciona bem quando há recurso ou funcionalidade clara.

### Quando usar

Use quando a recomendação depende de um mecanismo visível, como app, parcelas, cofrinho, cashback, categorização, simulação ou visualização.

### O que não faz

- Não deve virar ficha técnica.
- Não cria característica inexistente.
- Não promete vantagem não cadastrada.
- Não transforma mecanismo em garantia.

---

# Camada 3 — Tendências Cognitivas

## O que são Tendências Cognitivas

As Tendências Cognitivas são rotas de enquadramento da mensagem.

Elas permitem gerar 10 alternativas diferentes para o mesmo briefing, sem alterar a proposta de valor original.

Também podem ser chamadas, em linguagem funcional, de vieses de comunicação ou vieses cognitivos de enquadramento.

---

## Por que as Tendências Cognitivas existem

Elas existem para variar a forma de apresentação do mesmo valor.

A diferença entre as mensagens não deve ser apenas troca de palavras.

A diferença deve estar na arquitetura de leitura:

- abertura;
- foco;
- ordem dos argumentos;
- ritmo;
- estrutura sintática;
- relação de valor destacada;
- encerramento;
- forma do título.

---

## Princípio central

**Liberdade de forma. Fidelidade de significado.**

A Tendência Cognitiva pode mudar como a mensagem é construída, mas não pode mudar o que a recomendação significa.

---

## O que a Tendência Cognitiva controla

| Elemento | Como a tendência controla |
|---|---|
| Abertura | Define o ponto de entrada cognitivo da mensagem |
| Foco | Escolhe qual relação de valor será mais perceptível |
| Ordem dos argumentos | Reorganiza a sequência de ideias |
| Ritmo | Define se o texto será mais direto, comparativo, reconhecível ou explicativo |
| Título | Influencia a forma do gancho |
| Mensagem | Orienta o enquadramento do valor central |
| CTA | Pode influenciar a coerência da ação, sem criar promessa nova |

---

## O que a Tendência Cognitiva não faz

- Não cria novo produto.
- Não cria novo público.
- Não inventa benefício.
- Não altera dados estruturados.
- Não aumenta promessa.
- Não muda condições comerciais.
- Não mistura múltiplas tendências no mesmo item.
- Não substitui a Voz BB.
- Não autoriza exagero emocional.

---

## Tendências oficiais

| ID | Tendência / Viés | Função oficial | Descrição oficial |
|---:|---|---|---|
| 1 | Contraste | Tornar o valor perceptivel pela diferenca entre duas condicoes. | Comparar condicao atual e alternativa possivel sem medo ou garantia. |
| 2 | Curiosidade | Abrir lacuna de compreensao que a mensagem consegue resolver. | Usar pergunta precisa, curta e respondivel, sem clickbait. |
| 3 | Especificidade | Aumentar clareza pela concretude do que ja existe. | Destacar elemento concreto disponivel no texto-base. |
| 4 | Pertencimento | Ativar identidade contextual compartilhada. | Mostrar relevancia para pessoas na mesma condicao, sem prova social. |
| 5 | Previsibilidade | Reduzir incerteza interpretativa com logica clara. | Conectar situacao, solucao, ganho funcional e efeito emocional. |
| 6 | Simplicidade | Reduzir esforco mental e apresentar o essencial. | Usar frase direta, uma ideia por frase e ate tres ideias principais. |
| 7 | Transformacao | Tornar o avanco possivel mais perceptivel. | Organizar a mensagem como percurso sem garantir resultado. |
| 8 | Consistencia | Alinhar solucao ao objetivo declarado pela pessoa. | Mostrar escolha coerente com o objetivo, sem atribuir valores pessoais. |
| 9 | Afinidade | Criar reconhecimento situacional imediato. | Abrir por condicao reconhecivel do publico, sem intimidade excessiva. |
| 10 | Congruencia Final | Criar sensacao de completude logica. | Abrir por valor central e encerrar retomando a mesma ideia. |

---

## Assinatura de título por tendência

| Tendência | Personalidade esperada do título |
|---|---|
| Afinidade | Título com situação reconhecível |
| Congruência Final | Ideia fechada e coerente |
| Consistência | Alinhamento entre objetivo e escolha |
| Contraste | Diferença entre duas condições |
| Curiosidade | Pergunta curta e respondível |
| Especificidade | Elemento concreto |
| Pertencimento | Condição compartilhada do grupo |
| Previsibilidade | Relação clara entre ação e efeito |
| Simplicidade | Tese curta, direta e essencial |
| Transformação | Passagem, avanço ou mudança possível |

---

## 1 — Contraste

### Identificação

| Campo | Valor |
|---|---|
| Tabela | `TND_CGTV_TCN` |
| ID | `1` |
| Nome | Contraste |
| Função oficial | Tornar o valor perceptivel pela diferenca entre duas condicoes. |
| Descrição oficial | Comparar condicao atual e alternativa possivel sem medo ou garantia. |

### O que é

É a tendência que torna o valor mais claro ao comparar duas condições: uma situação atual e uma alternativa possível.

### Por que existe

Existe porque a diferença entre dois estados pode tornar o benefício mais perceptível.

### O que faz na geração

- Usa comparação controlada.
- Mostra diferença entre situação atual e alternativa.
- Evita medo, drama ou promessa garantida.
- Ajuda o usuário a perceber o valor pela mudança de condição.

### Quando usar

Use quando houver uma diferença clara entre uma situação desorganizada e uma alternativa mais organizada, entre pouca clareza e mais clareza, ou entre decidir sem apoio e decidir com apoio.

### O que não faz

- Não cria ameaça.
- Não usa medo.
- Não promete resultado certo.
- Não exagera a diferença.

---

## 2 — Curiosidade

### Identificação

| Campo | Valor |
|---|---|
| Tabela | `TND_CGTV_TCN` |
| ID | `2` |
| Nome | Curiosidade |
| Função oficial | Abrir lacuna de compreensao que a mensagem consegue resolver. |
| Descrição oficial | Usar pergunta precisa, curta e respondivel, sem clickbait. |

### O que é

É a tendência que abre uma lacuna de compreensão simples, relevante e respondível.

### Por que existe

Existe para criar interesse sem exagero e sem clickbait.

### O que faz na geração

- Formula uma pergunta ou tensão curta.
- Mantém a resposta dentro do conteúdo da mensagem.
- Cria curiosidade funcional.
- Evita mistério artificial.

### Quando usar

Use quando a recomendação puder ser apresentada por uma dúvida concreta do usuário.

### O que não faz

- Não usa clickbait.
- Não cria pergunta que a mensagem não responde.
- Não exagera suspense.
- Não introduz informação fora do briefing.

---

## 3 — Especificidade

### Identificação

| Campo | Valor |
|---|---|
| Tabela | `TND_CGTV_TCN` |
| ID | `3` |
| Nome | Especificidade |
| Função oficial | Aumentar clareza pela concretude do que ja existe. |
| Descrição oficial | Destacar elemento concreto disponivel no texto-base. |

### O que é

É a tendência que aumenta a clareza destacando um elemento concreto já disponível no texto-base.

### Por que existe

Existe porque detalhes concretos tornam a mensagem mais clara e confiável.

### O que faz na geração

- Prioriza um elemento específico.
- Usa concretude em vez de generalidade.
- Facilita a compreensão imediata.
- Mantém fidelidade ao que já existe na base.

### Quando usar

Use quando houver elemento concreto relevante, como app, cofrinho, parcelas, simulação, categorias, vigência, pagamento ou visualização.

### O que não faz

- Não inventa números.
- Não cria taxas, prazos ou condições.
- Não acrescenta detalhe não confirmado.
- Não transforma especificidade em promessa comercial.

---

## 4 — Pertencimento

### Identificação

| Campo | Valor |
|---|---|
| Tabela | `TND_CGTV_TCN` |
| ID | `4` |
| Nome | Pertencimento |
| Função oficial | Ativar identidade contextual compartilhada. |
| Descrição oficial | Mostrar relevancia para pessoas na mesma condicao, sem prova social. |

### O que é

É a tendência que mostra que a recomendação se aplica a uma condição compartilhada por um grupo de pessoas.

### Por que existe

Existe para tornar a mensagem reconhecível dentro de uma situação comum do público.

### O que faz na geração

- Abre por uma condição compartilhada.
- Mostra relevância contextual.
- Ajuda o usuário a se reconhecer na situação.
- Evita prova social artificial.

### Quando usar

Use quando a recomendação é direcionada a pessoas em uma situação comum, como quem quer organizar gastos, comparar crédito, planejar compra ou guardar dinheiro.

### O que não faz

- Não usa “todo mundo”.
- Não afirma que outras pessoas já fizeram algo.
- Não cria prova social.
- Não força identidade pessoal.

---

## 5 — Previsibilidade

### Identificação

| Campo | Valor |
|---|---|
| Tabela | `TND_CGTV_TCN` |
| ID | `5` |
| Nome | Previsibilidade |
| Função oficial | Reduzir incerteza interpretativa com logica clara. |
| Descrição oficial | Conectar situacao, solucao, ganho funcional e efeito emocional. |

### O que é

É a tendência que organiza a mensagem por encadeamento lógico.

### Por que existe

Existe para reduzir incerteza e facilitar a compreensão da relação entre situação, solução e benefício.

### O que faz na geração

- Conecta situação, solução, ganho funcional e efeito emocional.
- Usa progressão clara.
- Evita saltos narrativos.
- Ajuda o usuário a entender por que a recomendação faz sentido.

### Quando usar

Use quando a recomendação precisa ser explicada de forma lógica e sequencial.

### O que não faz

- Não inventa etapas.
- Não cria processo não existente.
- Não usa promessa de previsibilidade financeira.
- Não transforma relação lógica em garantia.

---

## 6 — Simplicidade

### Identificação

| Campo | Valor |
|---|---|
| Tabela | `TND_CGTV_TCN` |
| ID | `6` |
| Nome | Simplicidade |
| Função oficial | Reduzir esforco mental e apresentar o essencial. |
| Descrição oficial | Usar frase direta, uma ideia por frase e ate tres ideias principais. |

### O que é

É a tendência que reduz esforço mental e apresenta apenas o essencial.

### Por que existe

Existe para tornar a comunicação mais direta, clara e leve.

### O que faz na geração

- Usa frases curtas.
- Trabalha uma ideia por frase.
- Limita a densidade de informação.
- Evita sobrecarga.

### Quando usar

Use quando a interface tiver pouco espaço ou quando a recomendação precisa ser entendida rapidamente.

### O que não faz

- Não empobrece o conteúdo.
- Não vira slogan vazio.
- Não remove informação necessária.
- Não usa simplificação que altere significado.

---

## 7 — Transformacao

### Identificação

| Campo | Valor |
|---|---|
| Tabela | `TND_CGTV_TCN` |
| ID | `7` |
| Nome | Transformacao |
| Função oficial | Tornar o avanco possivel mais perceptivel. |
| Descrição oficial | Organizar a mensagem como percurso sem garantir resultado. |

### O que é

É a tendência que organiza a mensagem como percurso, avanço ou mudança possível.

### Por que existe

Existe para mostrar que a recomendação pode apoiar uma evolução do usuário, sem prometer transformação garantida.

### O que faz na geração

- Mostra passagem de uma condição para outra.
- Organiza a mensagem como caminho.
- Valoriza avanço possível.
- Mantém cautela com promessas.

### Quando usar

Use quando o produto ou orientação ajuda o usuário a planejar, organizar, começar, avançar ou construir algo no tempo.

### O que não faz

- Não garante resultado.
- Não promete transformação completa.
- Não cria antes e depois absoluto.
- Não usa linguagem milagrosa.

---

## 8 — Consistencia

### Identificação

| Campo | Valor |
|---|---|
| Tabela | `TND_CGTV_TCN` |
| ID | `8` |
| Nome | Consistencia |
| Função oficial | Alinhar solucao ao objetivo declarado pela pessoa. |
| Descrição oficial | Mostrar escolha coerente com o objetivo, sem atribuir valores pessoais. |

### O que é

É a tendência que mostra coerência entre o objetivo do usuário e a solução apresentada.

### Por que existe

Existe para reforçar que a recomendação faz sentido dentro do que o usuário busca resolver.

### O que faz na geração

- Alinha solução e objetivo.
- Mostra coerência de escolha.
- Valoriza o encaixe racional.
- Evita julgamento ou atribuição de valores pessoais.

### Quando usar

Use quando o público tem um objetivo claro, como planejar compra, organizar orçamento, revisar crédito ou guardar dinheiro.

### O que não faz

- Não atribui intenção pessoal não confirmada.
- Não moraliza a decisão.
- Não cria julgamento.
- Não afirma que o usuário “valoriza” algo se isso não estiver no briefing.

---

## 9 — Afinidade

### Identificação

| Campo | Valor |
|---|---|
| Tabela | `TND_CGTV_TCN` |
| ID | `9` |
| Nome | Afinidade |
| Função oficial | Criar reconhecimento situacional imediato. |
| Descrição oficial | Abrir por condicao reconhecivel do publico, sem intimidade excessiva. |

### O que é

É a tendência que cria reconhecimento imediato pela situação vivida pelo público.

### Por que existe

Existe para fazer a mensagem parecer próxima do contexto do usuário, sem usar intimidade artificial.

### O que faz na geração

- Abre por uma situação reconhecível.
- Usa linguagem contextual.
- Facilita identificação.
- Mantém tom respeitoso.

### Quando usar

Use quando a situação do público é muito concreta, como usar limite especial, ter contas em mais de um banco, querer trocar celular ou começar uma reserva.

### O que não faz

- Não usa gíria.
- Não cria intimidade excessiva.
- Não fala como se conhecesse a vida pessoal do usuário.
- Não usa tom invasivo.

---

## 10 — Congruencia Final

### Identificação

| Campo | Valor |
|---|---|
| Tabela | `TND_CGTV_TCN` |
| ID | `10` |
| Nome | Congruencia Final |
| Função oficial | Criar sensacao de completude logica. |
| Descrição oficial | Abrir por valor central e encerrar retomando a mesma ideia. |

### O que é

É a tendência que cria uma mensagem circular e coerente, retomando no fim a ideia central apresentada no começo.

### Por que existe

Existe para dar sensação de fechamento, completude e coerência.

### O que faz na geração

- Abre pelo valor central.
- Desenvolve a justificativa.
- Encerra retomando a mesma ideia.
- Evita dispersão.

### Quando usar

Use quando a mensagem precisa parecer especialmente coesa, fechada e institucional.

### O que não faz

- Não introduz assunto novo no final.
- Não muda o foco da mensagem.
- Não usa fechamento desconectado.
- Não cria nova promessa no encerramento.

---

# Síntese das camadas

| Camada | Pergunta que responde | Resultado |
|---|---|---|
| Produto | O que será comunicado? | Solução e benefícios |
| Público | Para quem será comunicado? | Situação e necessidades |
| Apresentação | Como organizar a proposta inicial? | Apresentação preenchida |
| Cenário | Como desenvolver a narrativa? | Base sem viés |
| Tendência Cognitiva | Por qual rota o valor será percebido? | Base com viés |
| Voz BB | Como institucionalizar o texto? | Base BB |
| Mensagem | Como explicar o valor? | Texto principal |
| Título | Como criar o gancho? | Headline |
| CTA | Qual ação sugerir? | Chamada para ação |

---

# Regras de governança

## Regra central

**Liberdade de forma. Fidelidade de significado.**

A IA pode variar forma, ordem, ritmo e enquadramento.

A IA não pode alterar significado, criar promessa nova ou inventar benefício.

---

## Regras obrigatórias

- Usar apenas informações presentes nos dados de origem.
- Não inventar números, taxas, prazos, percentuais, condições ou garantias.
- Não intensificar emoção indevidamente.
- Não misturar tendências cognitivas.
- Não criar CTA antes da etapa própria.
- Respeitar limites de caracteres.
- Preservar Voz BB sem alterar o conteúdo de negócio.
- Manter rastreabilidade entre briefing, geração, tendência, iteração e versão.

---

## Promessas sensíveis

Usar apenas quando houver fonte ou condição explícita:

- melhores condições;
- vantagens e benefícios;
- sem juros;
- sem entrada;
- sem IOF;
- cashback;
- prazo para começar a pagar;
- menos etapas;
- condições especiais;
- crédito rápido e fácil;
- pré-aprovado;
- parcelas que cabem no orçamento.

Quando necessário, condicionar:

- quando disponível;
- conforme oferta;
- conforme as condições disponíveis para o cliente;
- sujeito à análise;
- quando a cota for contemplada;
- quando o serviço estiver disponível.

---

# Glossário essencial

| Termo | Significado |
|---|---|
| Produto | Solução, serviço, funcionalidade ou orientação recomendável |
| Público | Grupo ou situação de usuário para quem a recomendação será direcionada |
| Apresentação | Modelo que organiza Produto e Público em proposta de valor |
| Cenário | Lógica narrativa usada para desenvolver a proposta |
| Tendência Cognitiva | Rota de comunicação aplicada para gerar variações |
| Viés | Nome funcional da camada de tendência cognitiva |
| Genera | Motor de geração automática dos insights |
| Base sem viés | Texto neutro produzido antes da aplicação da tendência |
| Checkpoint-base | Referência fixa usada para gerar variações por tendência |
| Base com viés | Texto reorganizado por uma tendência cognitiva |
| Voz BB | Ajuste institucional da mensagem |
| Mensagem | Texto principal do insight |
| Título | Headline do insight |
| CTA | Chamada para ação |
| Curadoria | Escolha humana entre as alternativas geradas |
| Versão proposta | Versão criada por geração ou edição e ainda pendente de aprovação |
| Versão válida | Versão aprovada e considerada ativa no fluxo |

---

# Resumo executivo

Este catálogo documenta as três camadas principais que controlam a geração de insights no Genera: Apresentações, Cenários e Tendências Cognitivas.

Produto e Público formam a base de negócio. A Apresentação organiza essa base em uma primeira proposta de valor. O Cenário define a lógica narrativa. A Tendência Cognitiva cria 10 rotas diferentes de comunicação sobre o mesmo conteúdo.

Essa arquitetura permite gerar alternativas variadas sem perder controle sobre o significado.

O resultado é uma geração com liberdade de forma, mas com fidelidade ao conteúdo cadastrado, às regras de negócio e à governança do ciclo de vida da recomendação.
