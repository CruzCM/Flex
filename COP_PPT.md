# PAPEL

Atue como especialista em apresentações executivas para comitês de negócio e validação de regras.

Crie uma apresentação executiva, clara e didática sobre o **Radar Financeiro**.

A apresentação deve permitir que pessoas sem conhecimento técnico entendam:

* como o cliente entra no Radar;
* quais situações excluem o cliente;
* como o período financeiro é definido;
* como as movimentações são tratadas;
* como os gastos são organizados;
* como o Radar chega aos cinco públicos;
* quais decisões precisam ser homologadas pela mesa.

---

# OBJETIVO DA APRESENTAÇÃO

O objetivo não é ensinar programação, banco de dados ou SQL.

O objetivo é **validar regras de negócio**.

Ao final da apresentação, a mesa deve conseguir responder:

**“Esta é realmente a regra que queremos aplicar ao cliente?”**

---

# PÚBLICO

Considere uma audiência formada principalmente por:

* executivos;
* gestores;
* responsáveis pelo produto;
* áreas negociais;
* participantes sem conhecimento técnico aprofundado.

Pode haver profissionais técnicos na reunião, portanto a apresentação deve preservar a rastreabilidade das regras implementadas.

---

# REGRA DE LINGUAGEM

Use linguagem:

* simples;
* executiva;
* direta;
* didática;
* orientada ao efeito da regra sobre o cliente.

Evite transformar a apresentação em documentação de TI.

Explique primeiro **o significado negocial**.

Imediatamente depois, quando existir uma implementação técnica correspondente, mantenha a referência técnica **entre parênteses e em estilo de código**.

Exemplo correto:

> O cliente precisa ter utilizado recentemente o aplicativo (`TS_INCL_TRAN`).

Outro exemplo:

> Se houver qualquer movimentação em moeda estrangeira, o cliente fica fora do Radar (`FL_SOMENTE_BRL = 'N'`).

Não retirar essas referências técnicas.

Não transformar os códigos técnicos no assunto principal do slide.

---

# PRINCÍPIO NARRATIVO

Conte a história seguindo a jornada real do cliente.

A sequência deve ser:

1. Quem pode entrar no Radar?
2. Como identificamos conta, CPF e renda?
3. Qual período financeiro analisamos?
4. Qual é a renda e o perfil financeiro?
5. Como eliminamos transferências entre contas próprias?
6. Como organizamos os gastos?
7. Como escolhemos o tema financeiro?
8. Quais são os cinco públicos?
9. Quais visões alternativas são produzidas?
10. Quais decisões precisam ser homologadas?

Não reorganize essa sequência.

---

# REGRA PARA EXEMPLOS

Sempre que uma regra puder parecer abstrata, utilize exemplos numéricos simples.

Prefira exemplos de situações cotidianas:

* padaria;
* supermercado;
* cartão;
* Pix;
* conta em outro banco;
* salário;
* lazer;
* empréstimos;
* poupança.

Os exemplos devem facilitar a compreensão da regra, não introduzir novas regras.

Não invente regras, percentuais, campos, códigos ou critérios que não estejam fornecidos no conteúdo-base.

---

# REGRA PARA DATAS

Quando a compreensão depender de uma janela temporal, utilize datas concretas.

Exemplo:

> Estamos em 15 de setembro.
> O cliente fez uma compra em 20 de agosto (`DT_TRAN`), mas sua última atualização associada ao aplicativo ocorreu em 10 de maio (`TS_INCL_TRAN`).

Para explicar ciclos financeiros, mostre visualmente:

**Ciclo aberto**
20/08 → 15/09

versus

**Último ciclo fechado**
20/07 → 19/08

A apresentação deve deixar evidente por que o Radar prefere um período completo.

---

# ARQUITETURA DOS SLIDES

Crie aproximadamente **12 a 15 slides**, priorizando clareza em vez de quantidade.

## Slide 1 — Capa

Título:

**Radar Financeiro**

Subtítulo:

**Como transformamos movimentações financeiras em uma orientação adequada para cada cliente**

Visual limpo e executivo.

---

## Slide 2 — O que vamos validar

Mostrar a jornada completa do Radar em uma linha visual:

**Entrada → Identificação → Ciclo → Contexto financeiro → Movimentações → Orçamento → Pontuação → Público**

Mensagem principal:

> Hoje não estamos validando tecnologia. Estamos validando as regras que determinam quem entra, quem sai e qual orientação chega ao cliente.

---

## Slides seguintes

Transforme cada etapa da jornada em um ou mais slides conforme necessário.

Para cada etapa, seguir preferencialmente esta composição:

### 1. Pergunta negocial

Exemplo:

**Quem pode entrar no Radar?**

### 2. Regra em linguagem simples

Explique o efeito para o cliente.

### 3. Referência técnica discreta

Entre parênteses e em `código`.

### 4. Exemplo prático

Use números ou datas quando ajudarem.

### 5. Decisão da mesa

Encerrar o bloco com:

**O que precisamos validar?**

---

# CINCO PÚBLICOS

Apresente claramente os cinco públicos:

1. **Categorização dos Gastos** (`CD_TEMA_VENCEDOR = 1`)
2. **Gestão de Orçamento** (`CD_TEMA_VENCEDOR = 2`)
3. **Consumo Planejado** (`CD_TEMA_VENCEDOR = 3`)
4. **Formação de Reserva** (`CD_TEMA_VENCEDOR = 4`)
5. **Uso Consciente do Crédito** (`CD_TEMA_VENCEDOR = 5`)

Apresente também o caso de empate (`CD_TEMA_VENCEDOR = 9`).

Não apresentar os cinco públicos apenas como uma lista.

Criar uma representação visual que permita entender **qual comportamento leva a cada orientação**.

---

# DESTAQUES OBRIGATÓRIOS

Dê destaque visual especial para estas regras:

### Exclusões rígidas

* moeda estrangeira (`FL_SOMENTE_BRL = 'N'`);
* movimentação Agro (`FL_TEM_MOV_AGRO = 'S'`);
* ausência de renda presumida (`VL_REN_PRES`);
* ausência de perfil financeiro válido (`CD_MAC_PRFL_CLI`).

### Regra inclusiva

A ausência de ciclo financeiro **não exclui o cliente**.

Usar dia primeiro como fallback (`DD_INC_MM_CLC_BLC_FALLBACK = 1`).

### Transferências próprias

Mostrar que mover dinheiro entre duas contas do mesmo cliente **não representa renda nem gasto**.

### Regra dos 75%

Se mais de 75% das despesas estiverem sem classificação (`PC_SAI_IND > 0.75`), priorizar Categorização dos Gastos (`NR_PONT_CONC_IND = 99`).

### Empate

O Radar não escolhe arbitrariamente.

Quando mais de um tema possui a maior pontuação (`QT_TEMAS_PONT_MAX > 1`), registrar empate (`CD_TEMA_VENCEDOR = 9`).

---

# DIREÇÃO VISUAL

Criar uma apresentação executiva e moderna.

Priorizar:

* diagramas de fluxo;
* jornadas;
* comparações lado a lado;
* cards;
* timelines;
* indicadores simples;
* gráficos conceituais;
* exemplos visuais.

Evitar:

* slides com grandes blocos de texto;
* excesso de bullet points;
* aparência de documentação técnica;
* tabelas muito densas;
* código ocupando área de destaque;
* imagens decorativas sem relação com a mensagem.

Cada slide deve transmitir **uma ideia principal**.

---

# HIERARQUIA VISUAL

Em cada slide:

**Título:** pergunta ou conclusão negocial.

**Mensagem principal:** uma frase curta que a audiência deve guardar.

**Conteúdo visual:** regra, fluxo, comparação ou exemplo.

**Referência técnica:** discreta, entre parênteses e em `código`.

---

# NOTAS DO APRESENTADOR

Crie notas do apresentador para todos os slides.

As notas devem utilizar como base a fala negocial fornecida.

Não colocar toda a fala dentro do slide.

O slide deve ser visual e sintético.

A explicação completa deve ficar nas **notas do apresentador**.

Nas notas:

* preservar exemplos;
* preservar números;
* preservar datas;
* preservar justificativas negociais;
* preservar referências técnicas em `código`;
* preservar as perguntas de homologação.

---

# SLIDE FINAL — DECISÕES DA MESA

Criar um slide final chamado:

**Decisões para Homologação**

Organizar os 13 pontos de decisão de maneira visual e executiva.

Para cada decisão, permitir os três possíveis status:

**APROVADO | ALTERAR | INVESTIGAR**

Não criar decisões adicionais.

---

# REGRAS DE FIDELIDADE

Obrigatório:

* não inventar regras;
* não alterar percentuais;
* não alterar valores dos exemplos;
* não alterar códigos técnicos;
* não substituir nomes de campos técnicos;
* não criar conclusões não presentes no conteúdo fornecido;
* não eliminar referências técnicas;
* não transformar hipótese em regra;
* não alterar a sequência lógica da jornada.

Se alguma informação não estiver disponível, não completar por suposição.

---

# RESULTADO ESPERADO

A apresentação deve passar a sensação de que:

> “O Radar possui regras claras, explicáveis e auditáveis, e agora o negócio precisa homologar se essas são as regras que queremos aplicar ao cliente.”

O tom deve ser de **validação e tomada de decisão**, e não de defesa técnica da solução.
