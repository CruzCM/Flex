# TND (VIES) — VERSÃO FINAL

**Tabela:** `TND_CGTV_TCN`

## Definição

Nesta arquitetura, TND significa **Tendência Cognitiva de Enquadramento**.

“Viés” é o nome funcional da camada. Cada TND define uma rota cognitiva própria para apresentar a mesma proposta de valor de forma diferente.

A TND não cria uma nova oferta, não altera fatos, não aumenta promessas e não define a voz institucional.

Ela altera a forma de leitura da mensagem por meio de:

- ponto de entrada;
- foco principal;
- ordem dos argumentos;
- ritmo;
- estrutura sintática;
- relação de valor destacada;
- forma de encerramento.

---

## Papel no fluxo

1. A Apresentação define a proposta de valor.
2. O Copywriter desenvolve essa proposta conforme o Cenário.
3. O resultado forma `{PH_BASE_SEM_VIES}`.
4. Cada TND usa o mesmo `{PH_BASE_SEM_VIES}` de forma independente.
5. A TND gera uma nova rota de relevância.
6. A Voz BB transforma cada resultado em comunicação institucional, sem apagar sua assinatura estrutural.

A TND possui liberdade de forma.

A TND deve preservar fidelidade de significado.

---

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

---

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

---

## Schema

| Campo | Descrição |
|---|---|
| `NM_TND_PDRO` | Nome da Tendência Cognitiva de Enquadramento |
| `TX_FUC_OPRL_TND` | Intenção e função estratégica da tendência |
| `TX_DCR_DETD_TND` | Regras de abertura, desenvolvimento, encerramento e limites |
| `TX_RCPO_PDRO_TND` | Palavras-chave para classificação e recomendação |

---

## Matriz de singularidade

| Tendência | Pergunta mental | Tipo de abertura | Relação em destaque | Encerramento |
|---|---|---|---|---|
| Afinidade | “Isso reconhece minha situação?” | Condição individual reconhecível | Contexto pessoal e adequação | Pertinência para aquela situação |
| Congruência Final | “Essa ideia fecha com lógica?” | Valor central | Causa e efeito | Retomada da ideia inicial |
| Consistência | “Isso combina com o que quero alcançar?” | Estado desejado | Objetivo e escolha coerente | Continuidade de direção |
| Contraste | “Qual diferença isso faz?” | Duas condições distintas | Situação atual e alternativa possível | Diferença prática |
| Curiosidade | “O que isso esclarece?” | Pergunta respondível | Lacuna e explicação | Compreensão resolvida |
| Especificidade | “O que exatamente está sendo oferecido?” | Elemento mais concreto | Precisão da oferta ou ganho | Ganho objetivo |
| Pertencimento | “Isso é para pessoas na minha situação?” | Perfil coletivo | Condição compartilhada | Pertinência ao grupo contextual |
| Previsibilidade | “Como isso se conecta?” | Relação causal | Encadeamento entre necessidade e solução | Clareza de contribuição |
| Simplicidade | “Qual é o essencial?” | Tese direta | Valor central | Síntese objetiva |
| Transformação | “Que avanço isso pode favorecer?” | Condição atual ou direção desejada | Transição possível | Direção de mudança |

---

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

---

# MODELOS DE TENDÊNCIA

## 1. Afinidade

### `NM_TND_PDRO`

Afinidade

### `TX_FUC_OPRL_TND`

**Intenção:** criar reconhecimento situacional imediato.

**Função:** fazer a pessoa perceber que a mensagem parte de uma condição que ela reconhece como própria.

### `TX_DCR_DETD_TND`

Abra pela condição, necessidade ou dificuldade que o público já vive no texto-base.

Apresente essa condição de forma próxima e concreta, sem inventar hábitos, rotinas, comportamentos, histórias ou exemplos externos.

Desenvolva a mensagem mostrando por que a solução é compatível com aquele contexto específico.

Conecte o ganho funcional ao efeito emocional permitido.

Finalize reforçando que a proposta faz sentido para aquela situação vivida.

Use reconhecimento e proximidade, sem imitar gírias, exagerar intimidade ou afirmar que a instituição entende exatamente a experiência da pessoa.

Não transforme Afinidade em Pertencimento. Afinidade fala com a pessoa em sua situação; Pertencimento fala de pessoas em uma condição compartilhada.

### `TX_RCPO_PDRO_TND`

reconhecimento, contexto vivido, proximidade, empatia, relevância pessoal, identificação

---

## 2. Congruência Final

### `NM_TND_PDRO`

Congruência Final

### `TX_FUC_OPRL_TND`

**Intenção:** criar sensação de completude lógica.

**Função:** abrir pelo valor central, explicar como ele se sustenta e encerrar retomando esse mesmo valor.

### `TX_DCR_DETD_TND`

Abra pelo benefício, resultado ou estado desejado mais relevante presente no texto-base.

Desenvolva somente as relações necessárias para sustentar essa ideia: necessidade, solução e ganho funcional.

Organize a mensagem por causa e efeito.

No encerramento, retome semanticamente a ideia da abertura com outra formulação.

A última unidade do texto deve confirmar a tese inicial, sem introduzir assunto novo, urgência, prova inexistente ou CTA.

Não transforme Congruência Final em Consistência. Congruência Final organiza o texto como composição circular; Consistência organiza o texto como alinhamento entre objetivo e escolha.

### `TX_RCPO_PDRO_TND`

coerência, completude, fechamento, retomada, causalidade, consistência de valor

---

## 3. Consistência

### `NM_TND_PDRO`

Consistência

### `TX_FUC_OPRL_TND`

**Intenção:** alinhar a solução ao objetivo já declarado pela pessoa.

**Função:** mostrar que a proposta é coerente com o estado que o público deseja alcançar.

### `TX_DCR_DETD_TND`

Abra pelo estado desejado, objetivo ou direção explicitamente presente no texto-base.

Apresente a necessidade prática como algo que dificulta essa direção.

Mostre a solução como uma escolha coerente com o objetivo já declarado.

Explique o ganho funcional como apoio para esse avanço.

Finalize reforçando a continuidade entre o que a pessoa busca e o que a solução favorece.

Não atribua valores pessoais, decisões anteriores, hábitos, compromissos passados ou características de identidade que não estejam no texto-base.

Não transforme Consistência em Transformação. Consistência enfatiza alinhamento de escolha; Transformação enfatiza deslocamento entre condições.

### `TX_RCPO_PDRO_TND`

alinhamento, objetivo, coerência de escolha, continuidade, direção, decisão consistente

---

## 4. Contraste

### `NM_TND_PDRO`

Contraste

### `TX_FUC_OPRL_TND`

**Intenção:** tornar o valor perceptível pela diferença entre duas condições.

**Função:** colocar a situação atual e a alternativa possível em comparação clara.

### `TX_DCR_DETD_TND`

Abra apresentando duas condições distintas já sustentadas pelo texto-base.

A comparação pode ocorrer entre necessidade atual e estado desejado, ou entre dificuldade atual e ganho funcional oferecido.

Mantenha as duas condições separadas e fáceis de perceber.

Apresente a solução como ponte prática entre elas.

Finalize destacando a diferença concreta que a solução pode favorecer.

Não agrave a dificuldade, não crie perdas, não invente riscos e não trate o estado desejado como resultado garantido.

Não transforme Contraste em Transformação. Contraste coloca condições lado a lado; Transformação mostra um percurso progressivo entre elas.

### `TX_RCPO_PDRO_TND`

comparação, diferença, condição atual, alternativa, ponte, mudança concreta

---

## 5. Curiosidade

### `NM_TND_PDRO`

Curiosidade

### `TX_FUC_OPRL_TND`

**Intenção:** abrir uma lacuna de compreensão que a própria mensagem consegue resolver.

**Função:** usar uma pergunta precisa para chamar atenção e esclarecer a relação de valor logo em seguida.

### `TX_DCR_DETD_TND`

Abra com uma pergunta direta baseada em uma relação já presente no texto-base.

A pergunta deve ser respondida integralmente pela própria mensagem.

Responda à pergunta logo em seguida, explicando a relação entre necessidade, solução e benefício.

Use frases curtas e progressão objetiva.

Finalize consolidando a compreensão obtida.

Não esconda informação relevante, não crie suspense artificial, não use clickbait, não sugira segredo e não insira CTA.

Curiosidade deve gerar esclarecimento, não manipulação.

### `TX_RCPO_PDRO_TND`

pergunta, lacuna respondida, descoberta, atenção, esclarecimento, compreensão

---

## 6. Especificidade

### `NM_TND_PDRO`

Especificidade

### `TX_FUC_OPRL_TND`

**Intenção:** aumentar clareza e credibilidade pela concretude do que já existe.

**Função:** substituir abstração por elementos precisos disponíveis no texto-base.

### `TX_DCR_DETD_TND`

Abra pelo elemento mais concreto disponível no texto-base: a solução nomeada, a condição específica do público ou o ganho funcional claramente descrito.

Priorize substantivos, verbos e relações objetivas.

Explique como esse elemento concreto se conecta à necessidade e ao efeito emocional.

Evite adjetivos vagos, formulações genéricas e abstrações desnecessárias quando o texto-base já oferecer uma descrição precisa.

Não invente números, medidas, prazos, critérios, limites, provas ou requisitos.

Finalize retomando o ganho prático de modo objetivo.

Não transforme Especificidade em Previsibilidade. Especificidade responde “o que exatamente”; Previsibilidade responde “como isso se conecta”.

### `TX_RCPO_PDRO_TND`

concretude, precisão, detalhe disponível, clareza, delimitação, objetividade

---

## 7. Pertencimento

### `NM_TND_PDRO`

Pertencimento

### `TX_FUC_OPRL_TND`

**Intenção:** ativar identidade contextual compartilhada.

**Função:** mostrar que a proposta é relevante para pessoas em uma condição comum.

### `TX_DCR_DETD_TND`

Abra pelo perfil coletivo do público, usando a condição compartilhada já presente no texto-base.

Apresente a necessidade como algo relevante para pessoas que vivem esse contexto.

Mostre a solução como adequada àquela condição coletiva.

Conecte o ganho funcional ao benefício emocional.

Finalize reforçando a pertinência da proposta para esse grupo contextual.

Não crie comunidade, maioria, aprovação social, depoimentos, validação externa ou pertencimento formal.

A identidade deve vir da condição comum, não de prova social inexistente.

Não transforme Pertencimento em Afinidade. Pertencimento fala de um grupo contextual; Afinidade fala diretamente da situação reconhecível da pessoa.

### `TX_RCPO_PDRO_TND`

identidade contextual, condição compartilhada, público coletivo, vínculo, pertinência, reconhecimento de grupo

---

## 8. Previsibilidade

### `NM_TND_PDRO`

Previsibilidade

### `TX_FUC_OPRL_TND`

**Intenção:** reduzir incerteza interpretativa por meio de uma lógica clara.

**Função:** explicar de forma direta como necessidade, solução, ganho funcional e efeito emocional se conectam.

### `TX_DCR_DETD_TND`

Abra estabelecendo uma relação causal clara presente no texto-base.

Organize a mensagem em sequência lógica: situação, solução, ganho funcional e efeito emocional.

Use conectores que deixem explícita a relação entre ideias, como “quando”, “com isso”, “por isso”, “assim” e equivalentes naturais.

Priorize clareza de encadeamento, não detalhamento operacional.

Não invente etapas, prazos, fluxos, critérios, condições de aprovação ou garantias de previsibilidade.

Finalize reafirmando como a solução contribui para tornar a situação mais clara, organizada ou controlável.

### `TX_RCPO_PDRO_TND`

causalidade, sequência lógica, transparência, clareza, controle, previsibilidade

---

## 9. Simplicidade

### `NM_TND_PDRO`

Simplicidade

### `TX_FUC_OPRL_TND`

**Intenção:** reduzir esforço mental e tornar o valor imediatamente compreensível.

**Função:** apresentar o essencial com máxima clareza e mínima carga cognitiva.

### `TX_DCR_DETD_TND`

Abra pela tese central do texto-base em uma frase direta.

Apresente apenas a razão prática principal e o efeito mais relevante da proposta.

Use uma ideia por frase, períodos curtos e construções simples.

Evite explicações paralelas, perguntas, contrastes extensos, termos técnicos dispensáveis, adjetivação vazia e digressões.

Organize a mensagem em até três ideias principais: valor, razão prática e efeito percebido.

Finalize retomando o valor central de forma objetiva.

Não transforme Simplicidade em slogan, promessa ampla ou redução que elimine uma relação material do texto-base.

### `TX_RCPO_PDRO_TND`

fluência, essencial, clareza imediata, linguagem simples, baixo esforço, objetividade

---

## 10. Transformação

### `NM_TND_PDRO`

Transformação

### `TX_FUC_OPRL_TND`

**Intenção:** tornar o avanço possível mais perceptível.

**Função:** organizar a mensagem como um percurso entre uma condição atual e uma direção desejada.

### `TX_DCR_DETD_TND`

Abra pela necessidade prática atual ou pelo estado desejado que dá sentido à mudança.

Apresente a solução como meio de transição, não como garantia de resultado.

Explique o ganho funcional como elemento que favorece movimento, organização, clareza, controle ou avanço.

Conclua mostrando o efeito emocional como direção possível e coerente com a mudança apresentada.

A mensagem deve transmitir percurso e progresso, não comparação estática.

Não crie jornada fictícia, personagem, antes e depois garantido, prova inexistente ou resultado automático.

Não transforme Transformação em Contraste. Transformação organiza a leitura como passagem; Contraste organiza a leitura como comparação.

### `TX_RCPO_PDRO_TND`

progresso, transição, avanço possível, mudança gradual, trajetória, direção desejada

---

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

---

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
9. Regenerar somente a tendência que não apresentar assinatura própria.