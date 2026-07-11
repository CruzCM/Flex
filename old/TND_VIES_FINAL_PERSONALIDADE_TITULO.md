# TND (VIES) — VERSÃO FINAL COM PERSONALIDADE DE TÍTULO

**Tabela:** `TND_CGTV_TCN`

## O que muda pontualmente

Esta versão mantém a função original das TNDs e acrescenta uma camada explícita de personalidade para títulos.

Mudanças objetivas:

1. A TND continua definindo a rota cognitiva da mensagem.
2. A TND passa também a definir a forma esperada do título.
3. O título deixa de apenas resumir o valor e passa a carregar a assinatura cognitiva da TND.
4. Curiosidade passa a preferir título em forma de pergunta curta e respondível.
5. Contraste passa a preferir título com diferença perceptível entre duas condições.
6. Transformação passa a preferir título com passagem, avanço ou mudança possível.
7. Especificidade passa a preferir título com elemento concreto.
8. Simplicidade passa a preferir título direto, essencial e sem ornamento.
9. A validação externa passa a avaliar também se o título tem personalidade.
10. Não há mudança obrigatória no schema da tabela. A assinatura de título deve ser registrada dentro de `TX_DCR_DETD_TND`.

## Decisão de arquitetura

A TND não deve aparecer apenas no corpo da mensagem.

A TND deve influenciar:

- a abertura do texto;
- a ordem dos argumentos;
- a relação de valor em destaque;
- o encerramento;
- a forma do título.

O título é o ponto de maior visibilidade da assinatura cognitiva.

Por isso, quando a TND tiver uma forma clara de título, essa forma deve ser preservada sempre que não ferir fidelidade, clareza ou limite de caracteres.

## Integração com o agente de Headline

A mudança principal no agente de Headline é trocar a regra fraca:

```text
Usar o ângulo cognitivo principal como possível fonte de gancho.
```

por uma regra forte:

```text
Usar o ângulo cognitivo principal como regra de forma do gancho,
sempre que isso não ferir fidelidade, clareza ou limite de caracteres.
```

### Patch recomendado para o prompt de Headline

Adicionar a seção abaixo em `system_6_0`, dentro de `# CONSTRUÇÃO`.

```text
# ASSINATURA COGNITIVA DO TÍTULO

A headline deve preservar a personalidade cognitiva predominante do resumo institucional.

Use a rota de leitura do texto como regra de forma do gancho, não apenas como tema.

Quando a assinatura cognitiva for reconhecível:

- Curiosidade: prefira uma pergunta curta, direta e respondível pela tagline ou pelo resumo.
- Contraste: destaque a diferença entre duas condições, sem exagerar oposição.
- Transformação: mostre uma passagem, avanço ou mudança possível.
- Especificidade: abra pelo elemento mais concreto da solução, necessidade ou benefício.
- Simplicidade: use uma afirmação direta, essencial e de baixo esforço.
- Afinidade: abra por uma situação reconhecível do público.
- Pertencimento: destaque a condição compartilhada do grupo contextual.
- Previsibilidade: mostre relação clara entre ação e efeito.
- Consistência: destaque alinhamento entre objetivo e escolha.
- Congruência Final: formule uma ideia que pareça completa e coerente.

Não neutralize uma pergunta, contraste, progressão ou elemento concreto quando isso for parte da assinatura da mensagem.

Se o resumo institucional trouxer uma pergunta como estrutura central, a headline deve preferencialmente manter forma interrogativa.

Se a forma cognitiva entrar em conflito com clareza, fidelidade ou limite de caracteres, preserve clareza e fidelidade, mas mantenha o máximo possível da assinatura.

Não transforme uma headline cognitivamente marcada em uma frase institucional genérica.
```

## Definição

Nesta arquitetura, TND significa **Tendência Cognitiva de Enquadramento**.

“Viés” é o nome funcional da camada.

Cada TND define uma rota cognitiva própria para apresentar a mesma proposta de valor de forma diferente.

A TND não cria uma nova oferta, não altera fatos, não aumenta promessas e não define a voz institucional.

Ela altera a forma de leitura da mensagem por meio de:

- ponto de entrada;
- foco principal;
- ordem dos argumentos;
- ritmo;
- estrutura sintática;
- relação de valor destacada;
- forma de encerramento;
- personalidade do título.

## Papel no fluxo

1. A Apresentação define a proposta de valor.
2. O Copywriter desenvolve essa proposta conforme o Cenário.
3. O resultado forma `{PH_BASE_SEM_VIES}`.
4. Cada TND usa o mesmo `{PH_BASE_SEM_VIES}` de forma independente.
5. A TND gera uma nova rota de relevância.
6. A Voz BB transforma cada resultado em comunicação institucional, sem apagar sua assinatura estrutural.
7. A Tagline destila o valor principal.
8. A Headline sintetiza esse valor com a personalidade cognitiva da TND.
9. A CTA transforma a mensagem em ação proporcional.

A TND possui liberdade de forma.

A TND deve preservar fidelidade de significado.

## Regra central

A TND não precisa preservar:

- a primeira frase;
- a abertura;
- a ordem dos argumentos;
- o foco principal;
- o ritmo;
- o encerramento;
- a estrutura sintática do texto-base.

A TND deve preservar:

- público;
- necessidade prática;
- estado desejado;
- solução;
- ganho funcional;
- efeito emocional;
- fatos;
- condições;
- limites;
- nível de certeza;
- nível de promessa;
- ações já existentes, quando houver.

A TND reorganiza a exposição da verdade.

A TND não cria uma nova verdade.

## Regras gerais

- Cada mensagem deve aplicar apenas uma TND.
- Todas as TNDs devem partir do mesmo `{PH_BASE_SEM_VIES}`.
- Nenhuma mensagem gerada pode servir como fonte para outra.
- A TND pode reconstruir o texto inteiro.
- A TND não pode inventar fatos, números, valores, prazos, condições, elegibilidade, provas, autoridade, riscos, consequências, urgência, escassez, comunidade ou garantias.
- A TND não pode transformar apoio, possibilidade, contribuição ou favorecimento em certeza.
- A TND não pode criar CTA, botão, link, comando ou instrução operacional.
- Caso exista uma ação no texto-base, ela pode ser preservada, mas não fortalecida ou substituída.
- A TND não pode misturar duas rotas cognitivas.
- `TX_RCPO_PDRO_TND` serve apenas para classificação, seleção e recomendação. Não representa palavras obrigatórias da mensagem.
- A personalidade de título deve ser aplicada somente quando a Headline for gerada.
- A personalidade de título não autoriza inventar fatos, intensificar promessa ou criar CTA.

## Schema

| Campo | Descrição |
|---|---|
| `NM_TND_PDRO` | Nome da Tendência Cognitiva de Enquadramento |
| `TX_FUC_OPRL_TND` | Intenção e função estratégica da tendência |
| `TX_DCR_DETD_TND` | Regras de abertura, desenvolvimento, encerramento, limites e assinatura de título |
| `TX_RCPO_PDRO_TND` | Palavras-chave para classificação e recomendação |

## Matriz de singularidade

| Tendência | Pergunta mental | Tipo de abertura | Relação em destaque | Encerramento | Assinatura de título |
|---|---|---|---|---|---|
| Afinidade | “Isso reconhece minha situação?” | Condição individual reconhecível | Contexto pessoal e adequação | Pertinência para aquela situação | Situação reconhecível do público |
| Congruência Final | “Essa ideia fecha com lógica?” | Valor central | Causa e efeito | Retomada da ideia inicial | Ideia fechada e coerente |
| Consistência | “Isso combina com o que quero alcançar?” | Estado desejado | Objetivo e escolha coerente | Continuidade de direção | Alinhamento entre objetivo e escolha |
| Contraste | “Qual diferença isso faz?” | Duas condições distintas | Situação atual e alternativa possível | Diferença prática | Diferença entre duas condições |
| Curiosidade | “O que isso esclarece?” | Pergunta respondível | Lacuna e explicação | Compreensão resolvida | Pergunta curta e respondível |
| Especificidade | “O que exatamente está sendo oferecido?” | Elemento mais concreto | Precisão da oferta ou ganho | Ganho objetivo | Elemento concreto da solução ou benefício |
| Pertencimento | “Isso é para pessoas na minha situação?” | Perfil coletivo | Condição compartilhada | Pertinência ao grupo contextual | Condição compartilhada do grupo |
| Previsibilidade | “Como isso se conecta?” | Relação causal | Encadeamento entre necessidade e solução | Clareza de contribuição | Relação clara entre ação e efeito |
| Simplicidade | “Qual é o essencial?” | Tese direta | Valor central | Síntese objetiva | Tese curta, direta e essencial |
| Transformação | “Que avanço isso pode favorecer?” | Condição atual ou direção desejada | Transição possível | Direção de mudança | Passagem, avanço ou mudança possível |

## Regras de título por TND

### Afinidade

O título deve parecer reconhecer uma situação concreta da pessoa.

Prefira:

- condição vivida;
- momento reconhecível;
- necessidade próxima;
- linguagem simples e humana.

Evite:

- título institucional genérico;
- generalizações amplas;
- intimidade excessiva;
- afirmar que a instituição entende exatamente a pessoa.

Exemplos de forma:

```text
Gastos que se repetem
Quando o mês aperta
Seu dinheiro em foco
```

### Congruência Final

O título deve transmitir completude lógica.

Prefira:

- frase que pareça fechar uma ideia;
- relação clara entre valor e sentido;
- formulação equilibrada e conclusiva.

Evite:

- pergunta aberta;
- gancho de suspense;
- título que introduza assunto novo.

Exemplos de forma:

```text
Uma escolha que faz sentido
Tudo no mesmo caminho
Seu plano com mais lógica
```

### Consistência

O título deve mostrar alinhamento entre o que a pessoa busca e a escolha apresentada.

Prefira:

- continuidade;
- coerência;
- direção;
- escolha compatível com o objetivo.

Evite:

- antes e depois dramático;
- identidade pessoal inventada;
- promessa de transformação garantida.

Exemplos de forma:

```text
Escolhas no seu ritmo
Seu objetivo em foco
Um passo coerente
```

### Contraste

O título deve colocar duas condições em diferença perceptível.

Prefira:

- pares simples;
- diferença prática;
- comparação curta;
- contraste sem exagero.

Evite:

- medo;
- oposição forçada;
- antes e depois garantido;
- “errado versus certo”.

Exemplos de forma:

```text
Menos dúvida, mais clareza
Do impulso ao plano
Mais controle, menos surpresa
```

### Curiosidade

O título deve preferencialmente ser uma pergunta.

A pergunta deve ser curta, direta e respondível pela tagline ou pelo resumo institucional.

Prefira:

- pergunta sobre o valor central;
- pergunta sobre a necessidade;
- pergunta sobre o elemento concreto;
- pergunta que abra uma lacuna legítima.

Evite:

- suspense artificial;
- segredo;
- clickbait;
- pergunta que a mensagem não consegue responder;
- pergunta que gere medo ou julgamento.

Exemplos de forma:

```text
Para onde vai seu dinheiro?
Quanto já está comprometido?
Essa compra cabe no mês?
```

### Especificidade

O título deve abrir pelo elemento mais concreto disponível.

Prefira:

- nome da solução;
- benefício real;
- objeto prático;
- dado qualitativo sustentado pelo texto;
- elemento visível ou acionável.

Evite:

- abstrações;
- adjetivos vagos;
- números, prazos ou condições não presentes;
- promessa maior do que a fonte sustenta.

Exemplos de forma:

```text
Gastos por categoria
Parcelas e vencimentos
Meta de reserva
```

### Pertencimento

O título deve destacar uma condição compartilhada por pessoas no mesmo contexto.

Prefira:

- grupo contextual;
- situação comum;
- vínculo pela condição, não por prova social;
- pertinência do tema para aquele grupo.

Evite:

- comunidade inventada;
- “todo mundo”;
- “pessoas como você” quando soar invasivo;
- aprovação social inexistente.

Exemplos de forma:

```text
Para quem planeja o mês
Para quem usa crédito
Para quem quer reservar
```

### Previsibilidade

O título deve mostrar conexão clara entre ação e efeito.

Prefira:

- relação causal simples;
- ideia de sequência;
- clareza antes da decisão;
- consequência prática sustentada.

Evite:

- passo a passo inventado;
- prazo inexistente;
- processo que o texto não sustenta;
- garantia de resultado.

Exemplos de forma:

```text
Entenda antes de decidir
Planeje antes de comprar
Veja o impacto do crédito
```

### Simplicidade

O título deve dizer o essencial com baixa carga cognitiva.

Prefira:

- frase curta;
- uma única ideia;
- vocabulário direto;
- substantivos concretos;
- ausência de ornamento.

Evite:

- pergunta quando não for necessária;
- metáfora;
- slogan vazio;
- múltiplas ideias.

Exemplos de forma:

```text
Gastos em ordem
Mês mais planejado
Crédito com clareza
```

### Transformação

O título deve mostrar uma passagem, avanço ou mudança possível.

Prefira:

- percurso entre condição atual e direção desejada;
- movimento gradual;
- avanço prático;
- transição sem garantia absoluta.

Evite:

- jornada fictícia;
- antes e depois garantido;
- resultado automático;
- promessa de mudança total.

Exemplos de forma:

```text
Do gasto à escolha
Do plano à reserva
Mais clareza para avançar
```

## Regras de rejeição

Uma mensagem deve ser rejeitada e regenerada quando:

- iniciar pelo mesmo tipo de abertura de outra TND;
- reproduzir a mesma sequência argumentativa;
- parecer uma paráfrase superficial;
- trocar apenas palavras sem mudar a arquitetura de leitura;
- introduzir informações ausentes no texto-base;
- transformar possibilidade em garantia;
- misturar assinaturas de duas TNDs;
- perder a assinatura estrutural da TND selecionada;
- criar linguagem incompatível com posterior aplicação da Voz BB.

Uma headline deve ser rejeitada e regenerada quando:

- ficar correta, mas genérica;
- não refletir a assinatura cognitiva da TND;
- transformar pergunta em afirmação quando a Curiosidade organizar a mensagem;
- eliminar contraste quando o Contraste organizar a mensagem;
- eliminar progressão quando a Transformação organizar a mensagem;
- eliminar elemento concreto quando a Especificidade organizar a mensagem;
- usar fórmula institucional vaga;
- criar CTA, comando ou promessa não sustentada;
- repetir literalmente a tagline;
- perder clareza para tentar parecer criativa.

## Modelos de tendência

# 1. Afinidade

## `NM_TND_PDRO`

Afinidade

## `TX_FUC_OPRL_TND`

**Intenção:** criar reconhecimento situacional imediato.

**Função:** fazer a pessoa perceber que a mensagem parte de uma condição que ela reconhece como própria.

## `TX_DCR_DETD_TND`

Abra pela condição, necessidade ou dificuldade que o público já vive no texto-base.

Apresente essa condição de forma próxima e concreta, sem inventar hábitos, rotinas, comportamentos, histórias ou exemplos externos.

Desenvolva a mensagem mostrando por que a solução é compatível com aquele contexto específico.

Conecte o ganho funcional ao efeito emocional permitido.

Finalize reforçando que a proposta faz sentido para aquela situação vivida.

Use reconhecimento e proximidade, sem imitar gírias, exagerar intimidade ou afirmar que a instituição entende exatamente a experiência da pessoa.

Assinatura para título: use uma situação reconhecível do público como forma principal do gancho. O título deve soar pertinente para aquele contexto, sem ser genérico ou invasivo.

Não transforme Afinidade em Pertencimento. Afinidade fala com a pessoa em sua situação; Pertencimento fala de pessoas em uma condição compartilhada.

## `TX_RCPO_PDRO_TND`

reconhecimento, contexto vivido, proximidade, empatia, relevância pessoal, identificação, título situacional, gancho reconhecível

---

# 2. Congruência Final

## `NM_TND_PDRO`

Congruência Final

## `TX_FUC_OPRL_TND`

**Intenção:** criar sensação de completude lógica.

**Função:** abrir pelo valor central, explicar como ele se sustenta e encerrar retomando esse mesmo valor.

## `TX_DCR_DETD_TND`

Abra pelo benefício, resultado ou estado desejado mais relevante presente no texto-base.

Desenvolva somente as relações necessárias para sustentar essa ideia: necessidade, solução e ganho funcional.

Organize a mensagem por causa e efeito.

No encerramento, retome semanticamente a ideia da abertura com outra formulação.

A última unidade do texto deve confirmar a tese inicial, sem introduzir assunto novo, urgência, prova inexistente ou CTA.

Assinatura para título: use uma formulação curta que pareça completa, coerente e conclusiva. O título deve sugerir que a ideia principal se fecha com lógica.

Não transforme Congruência Final em Consistência. Congruência Final organiza o texto como composição circular; Consistência organiza o texto como alinhamento entre objetivo e escolha.

## `TX_RCPO_PDRO_TND`

coerência, completude, fechamento, retomada, causalidade, consistência de valor, título conclusivo, gancho coerente

---

# 3. Consistência

## `NM_TND_PDRO`

Consistência

## `TX_FUC_OPRL_TND`

**Intenção:** alinhar a solução ao objetivo já declarado pela pessoa.

**Função:** mostrar que a proposta é coerente com o estado que o público deseja alcançar.

## `TX_DCR_DETD_TND`

Abra pelo estado desejado, objetivo ou direção explicitamente presente no texto-base.

Apresente a necessidade prática como algo que dificulta essa direção.

Mostre a solução como uma escolha coerente com o objetivo já declarado.

Explique o ganho funcional como apoio para esse avanço.

Finalize reforçando a continuidade entre o que a pessoa busca e o que a solução favorece.

Assinatura para título: destaque o alinhamento entre objetivo e escolha. O título deve comunicar continuidade, coerência ou direção, sem atribuir valores pessoais não sustentados.

Não atribua valores pessoais, decisões anteriores, hábitos, compromissos passados ou características de identidade que não estejam no texto-base.

Não transforme Consistência em Transformação. Consistência enfatiza alinhamento de escolha; Transformação enfatiza deslocamento entre condições.

## `TX_RCPO_PDRO_TND`

alinhamento, objetivo, coerência de escolha, continuidade, direção, decisão consistente, título alinhado, gancho de coerência

---

# 4. Contraste

## `NM_TND_PDRO`

Contraste

## `TX_FUC_OPRL_TND`

**Intenção:** tornar o valor perceptível pela diferença entre duas condições.

**Função:** colocar a situação atual e a alternativa possível em comparação clara.

## `TX_DCR_DETD_TND`

Abra apresentando duas condições distintas já sustentadas pelo texto-base.

A comparação pode ocorrer entre necessidade atual e estado desejado, ou entre dificuldade atual e ganho funcional oferecido.

Mantenha as duas condições separadas e fáceis de perceber.

Apresente a solução como ponte prática entre elas.

Finalize destacando a diferença concreta que a solução pode favorecer.

Assinatura para título: use uma diferença perceptível entre duas condições. O título pode usar estruturas de contraste, como “menos/mais”, “do/para” ou pares equivalentes, somente quando sustentadas pelo texto-base.

Não agrave a dificuldade, não crie perdas, não invente riscos e não trate o estado desejado como resultado garantido.

Não transforme Contraste em Transformação. Contraste coloca condições lado a lado; Transformação mostra um percurso progressivo entre elas.

## `TX_RCPO_PDRO_TND`

comparação, diferença, condição atual, alternativa, ponte, mudança concreta, título contrastivo, gancho de contraste

---

# 5. Curiosidade

## `NM_TND_PDRO`

Curiosidade

## `TX_FUC_OPRL_TND`

**Intenção:** abrir uma lacuna de compreensão que a própria mensagem consegue resolver.

**Função:** usar uma pergunta precisa para chamar atenção e esclarecer a relação de valor logo em seguida.

## `TX_DCR_DETD_TND`

Abra com uma pergunta direta baseada em uma relação já presente no texto-base.

A pergunta deve ser respondida integralmente pela própria mensagem.

Responda à pergunta logo em seguida, explicando a relação entre necessidade, solução e benefício.

Use frases curtas e progressão objetiva.

Finalize consolidando a compreensão obtida.

Assinatura para título: prefira uma pergunta curta, direta e respondível. O título deve abrir uma lacuna legítima e ser respondido pela tagline ou pelo resumo institucional. Se a pergunta não couber por limite, preserve ao máximo a sensação de pergunta ou descoberta sem usar clickbait.

Não esconda informação relevante, não crie suspense artificial, não use clickbait, não sugira segredo e não insira CTA.

Curiosidade deve gerar esclarecimento, não manipulação.

## `TX_RCPO_PDRO_TND`

pergunta, lacuna respondida, descoberta, atenção, esclarecimento, compreensão, título interrogativo, gancho de pergunta

---

# 6. Especificidade

## `NM_TND_PDRO`

Especificidade

## `TX_FUC_OPRL_TND`

**Intenção:** aumentar clareza e credibilidade pela concretude do que já existe.

**Função:** substituir abstração por elementos precisos disponíveis no texto-base.

## `TX_DCR_DETD_TND`

Abra pelo elemento mais concreto disponível no texto-base: a solução nomeada, a condição específica do público ou o ganho funcional claramente descrito.

Priorize substantivos, verbos e relações objetivas.

Explique como esse elemento concreto se conecta à necessidade e ao efeito emocional.

Evite adjetivos vagos, formulações genéricas e abstrações desnecessárias quando o texto-base já oferecer uma descrição precisa.

Assinatura para título: use o elemento mais concreto disponível como gancho. Pode ser a solução, o objeto da necessidade, o benefício real ou o resultado funcional, desde que esteja presente no texto-base.

Não invente números, medidas, prazos, critérios, limites, provas ou requisitos.

Finalize retomando o ganho prático de modo objetivo.

Não transforme Especificidade em Previsibilidade. Especificidade responde “o que exatamente”; Previsibilidade responde “como isso se conecta”.

## `TX_RCPO_PDRO_TND`

concretude, precisão, detalhe disponível, clareza, delimitação, objetividade, título concreto, gancho específico

---

# 7. Pertencimento

## `NM_TND_PDRO`

Pertencimento

## `TX_FUC_OPRL_TND`

**Intenção:** ativar identidade contextual compartilhada.

**Função:** mostrar que a proposta é relevante para pessoas em uma condição comum.

## `TX_DCR_DETD_TND`

Abra pelo perfil coletivo do público, usando a condição compartilhada já presente no texto-base.

Apresente a necessidade como algo relevante para pessoas que vivem esse contexto.

Mostre a solução como adequada àquela condição coletiva.

Conecte o ganho funcional ao benefício emocional.

Finalize reforçando a pertinência da proposta para esse grupo contextual.

Assinatura para título: destaque a condição compartilhada do grupo contextual. O título deve sinalizar pertinência para pessoas naquela situação, sem criar comunidade, maioria ou validação social.

Não crie comunidade, maioria, aprovação social, depoimentos, validação externa ou pertencimento formal.

A identidade deve vir da condição comum, não de prova social inexistente.

Não transforme Pertencimento em Afinidade. Pertencimento fala de um grupo contextual; Afinidade fala diretamente da situação reconhecível da pessoa.

## `TX_RCPO_PDRO_TND`

identidade contextual, condição compartilhada, público coletivo, vínculo, pertinência, reconhecimento de grupo, título coletivo, gancho de pertencimento

---

# 8. Previsibilidade

## `NM_TND_PDRO`

Previsibilidade

## `TX_FUC_OPRL_TND`

**Intenção:** reduzir incerteza interpretativa por meio de uma lógica clara.

**Função:** explicar de forma direta como necessidade, solução, ganho funcional e efeito emocional se conectam.

## `TX_DCR_DETD_TND`

Abra estabelecendo uma relação causal clara presente no texto-base.

Organize a mensagem em sequência lógica: situação, solução, ganho funcional e efeito emocional.

Use conectores que deixem explícita a relação entre ideias, como “quando”, “com isso”, “por isso”, “assim” e equivalentes naturais.

Priorize clareza de encadeamento, não detalhamento operacional.

Assinatura para título: mostre uma relação clara entre ação e efeito, ou entre compreensão e decisão. O título deve reduzir incerteza interpretativa, sem inventar processo, prazo ou etapa.

Não invente etapas, prazos, fluxos, critérios, condições de aprovação ou garantias de previsibilidade.

Finalize reafirmando como a solução contribui para tornar a situação mais clara, organizada ou controlável.

## `TX_RCPO_PDRO_TND`

causalidade, sequência lógica, transparência, clareza, controle, previsibilidade, título causal, gancho previsível

---

# 9. Simplicidade

## `NM_TND_PDRO`

Simplicidade

## `TX_FUC_OPRL_TND`

**Intenção:** reduzir esforço mental e tornar o valor imediatamente compreensível.

**Função:** apresentar o essencial com máxima clareza e mínima carga cognitiva.

## `TX_DCR_DETD_TND`

Abra pela tese central do texto-base em uma frase direta.

Apresente apenas a razão prática principal e o efeito mais relevante da proposta.

Use uma ideia por frase, períodos curtos e construções simples.

Evite explicações paralelas, perguntas, contrastes extensos, termos técnicos dispensáveis, adjetivação vazia e digressões.

Organize a mensagem em até três ideias principais: valor, razão prática e efeito percebido.

Finalize retomando o valor central de forma objetiva.

Assinatura para título: use uma frase curta, direta e essencial. O título deve reduzir esforço mental e evitar ornamento, metáfora ou múltiplas ideias.

Não transforme Simplicidade em slogan, promessa ampla ou redução que elimine uma relação material do texto-base.

## `TX_RCPO_PDRO_TND`

fluência, essencial, clareza imediata, linguagem simples, baixo esforço, objetividade, título direto, gancho simples

---

# 10. Transformação

## `NM_TND_PDRO`

Transformação

## `TX_FUC_OPRL_TND`

**Intenção:** tornar o avanço possível mais perceptível.

**Função:** organizar a mensagem como um percurso entre uma condição atual e uma direção desejada.

## `TX_DCR_DETD_TND`

Abra pela necessidade prática atual ou pelo estado desejado que dá sentido à mudança.

Apresente a solução como meio de transição, não como garantia de resultado.

Explique o ganho funcional como elemento que favorece movimento, organização, clareza, controle ou avanço.

Conclua mostrando o efeito emocional como direção possível e coerente com a mudança apresentada.

A mensagem deve transmitir percurso e progresso, não comparação estática.

Assinatura para título: mostre uma passagem, avanço ou mudança possível. O título pode usar estruturas de transição, como “do/para”, quando a relação estiver sustentada pelo texto-base.

Não crie jornada fictícia, personagem, antes e depois garantido, prova inexistente ou resultado automático.

Não transforme Transformação em Contraste. Transformação organiza a leitura como passagem; Contraste organiza a leitura como comparação.

## `TX_RCPO_PDRO_TND`

progresso, transição, avanço possível, mudança gradual, trajetória, direção desejada, título de passagem, gancho de transformação

## Validação externa do loop

Cada execução deve ser avaliada fora do agente gerador.

Uma variação só é aprovada quando apresentar diferença em pelo menos três dimensões:

1. Tipo de abertura.
2. Pergunta mental predominante.
3. Ordem dos argumentos.
4. Relação de valor destacada.
5. Ritmo de leitura.
6. Estrutura sintática predominante.
7. Forma de encerramento.

A comparação não deve ser apenas lexical.

É esperado que as mensagens compartilhem termos de público, solução e benefício, porque usam o mesmo texto-base.

O que deve mudar é a arquitetura de persuasão.

## Validação externa do título

Cada headline deve ser avaliada junto com a TND que originou a mensagem.

Uma headline só é aprovada quando responder “sim” a estas perguntas:

1. O título preserva fidelidade ao resumo institucional?
2. O título respeita o limite de caracteres?
3. O título não cria fato, promessa, urgência, condição ou CTA?
4. O título tem uma única ideia central?
5. O título carrega a assinatura cognitiva da TND?
6. O título é diferente de uma frase institucional genérica?
7. O título não repete literalmente a tagline?
8. O título funciona mesmo quando lido isoladamente?

Critérios específicos:

- Curiosidade: o título é preferencialmente uma pergunta curta e respondível.
- Contraste: o título mostra diferença perceptível entre duas condições.
- Transformação: o título sugere avanço ou passagem possível.
- Especificidade: o título traz elemento concreto.
- Simplicidade: o título é direto e essencial.
- Afinidade: o título reconhece uma situação.
- Pertencimento: o título mostra uma condição compartilhada.
- Previsibilidade: o título deixa clara uma relação.
- Consistência: o título mostra alinhamento.
- Congruência Final: o título parece fechado e coerente.

## Execução futura

Para gerar as mensagens:

1. Fixar um único `{PH_BASE_SEM_VIES}`.
2. Executar uma TND por vez.
3. Usar `TX_FUC_OPRL_TND` como direção estratégica.
4. Usar `TX_DCR_DETD_TND` como regra de construção.
5. Gerar cada mensagem de forma independente.
6. Validar fidelidade ao texto-base.
7. Validar diferença estrutural entre as mensagens.
8. Enviar cada resultado individualmente para a Voz BB.
9. Gerar tagline a partir da versão BB.
10. Gerar headline preservando a assinatura cognitiva da TND.
11. Validar personalidade do título.
12. Regenerar somente a tendência ou o título que não apresentar assinatura própria.
