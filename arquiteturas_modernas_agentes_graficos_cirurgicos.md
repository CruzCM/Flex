# Arquiteturas Modernas de Agentes

**Duração aproximada: 8 a 10 minutos**

---

# Slide 1 — Agentes modernos e o template

## Diagrama

```mermaid
flowchart LR
    U[Usuário] --> API[API]
    API --> A[LLM / Agente]
    A --> R[Resposta]

    classDef flow fill:#5858F8,color:#FFFFFF,stroke:#8B8DFF,stroke-width:2px;
    classDef neutral fill:#F7F8FF,color:#252F91,stroke:#A8ACD8,stroke-width:2px;

    class A flow;
    class U,API,R neutral;
```

### Pessoa 1 — Conceito

Quando a gente fala em agente de IA, é comum pensar em um chatbot.

Eu faço uma pergunta, o modelo processa e devolve uma resposta.

Mas um agente moderno pode ir além disso.

Ele pode entender o que precisa fazer, buscar informações, usar ferramentas, acessar outros sistemas e decidir qual caminho seguir antes de responder.

A ideia aqui não é aprofundar cada tecnologia.

É apresentar as principais peças que formam esse tipo de aplicação e mostrar como elas aparecem no nosso ambiente.

### Pessoa 2 — Na nossa esteira

E aqui a gente não começa do zero.

A esteira já provisiona um microserviço com uma estrutura pronta para receber essa lógica.

Nesse template já temos componentes como FastAPI, LangGraph, integração com o modelo, RAG, ferramentas e validadores.

Ou seja, boa parte da estrutura base da aplicação já vem preparada pela esteira.

A partir daí, o nosso trabalho fica mais concentrado nas regras de negócio e no comportamento do agente.

---

# Slide 2 — Frameworks para construção de aplicações

## Diagrama

```mermaid
flowchart LR
    U[Usuário] --> API[API]
    API --> LG[LangGraph]
    LG --> A[LLM / Agente]

    A -->|Responder| R[Resposta]
    A -.->|Próxima etapa| LG

    classDef flow fill:#5858F8,color:#FFFFFF,stroke:#8B8DFF,stroke-width:2px;
    classDef neutral fill:#F7F8FF,color:#252F91,stroke:#A8ACD8,stroke-width:2px;

    class LG flow;
    class U,API,A,R neutral;
```

### Pessoa 1 — Conceito

Até aqui parece simples: entra uma pergunta e sai uma resposta.

Mas o agente pode precisar responder diretamente, buscar uma informação ou chamar uma ferramenta antes de responder.

Quando esses diferentes caminhos começam a aparecer, precisamos estruturar esse fluxo.

É aí que entram frameworks como **LangChain** e **LangGraph**.

De forma simples, o LangChain oferece componentes para trabalhar com modelos, mensagens e ferramentas.

Já o LangGraph permite organizar as etapas e os diferentes caminhos que a execução do agente pode seguir.

### Pessoa 2 — Na nossa esteira

No nosso código, isso aparece no `graph.py`.

É ali que a gente define esse fluxo usando LangGraph.

Quando uma requisição entra, o modelo pode responder diretamente ou identificar que precisa executar alguma etapa antes.

Se precisar buscar uma informação ou usar uma ferramenta, o fluxo segue para essa etapa e depois continua até chegar à resposta.

Então, quando falamos que o agente decide o próximo passo, essa decisão faz parte do fluxo definido no próprio grafo.

E um desses caminhos pode ser buscar uma informação que o modelo não tem disponível.

É aí que entra o **RAG**.

---

# Slide 3 — RAG

## Diagrama

```mermaid
flowchart LR
    U[Usuário] --> API[API]
    API --> LG[LangGraph]
    LG --> A[LLM / Agente]
    A --> R[Resposta]

    A -->|Buscar contexto| RAG[RAG]
    RAG --> G["Genera BB<br/>Índice"]
    G -->|Chunks| A

    classDef flow fill:#5858F8,color:#FFFFFF,stroke:#8B8DFF,stroke-width:2px;
    classDef rag fill:#31D49D,color:#12372D,stroke:#65E0B7,stroke-width:2px;
    classDef neutral fill:#F7F8FF,color:#252F91,stroke:#A8ACD8,stroke-width:2px;

    class LG,A flow;
    class RAG,G rag;
    class U,API,R neutral;
```

### Pessoa 1 — Conceito

O modelo de IA não conhece automaticamente os documentos, normas e informações internas da empresa.

O **RAG**, ou Retrieval-Augmented Generation, ajuda justamente nesse ponto.

Antes de responder, a aplicação busca informações relacionadas à pergunta em uma base de conhecimento.

Os trechos mais relevantes são entregues ao modelo como contexto.

Assim, o modelo consegue construir a resposta usando também informações que estão fora do seu conhecimento original.

### Pessoa 2 — Na nossa esteira

No nosso ambiente, isso acontece através do **Genera BB**.

Os documentos já foram indexados previamente.

Quando o agente precisa buscar uma informação, ele consulta esse índice.

Ele envia a pergunta para o Genera BB, e o Genera BB devolve os trechos mais relevantes encontrados.

Esses trechos são os chamados **chunks**.

A partir daí, o agente usa esses chunks como contexto para construir a resposta.

Até aqui, estamos falando de buscar conhecimento.

Mas o agente também pode precisar consultar uma API, acessar outro sistema ou executar alguma ação.

E é aí que entram as **Tools**.

---

# Slide 4 — Tools e MCP

## Diagrama

```mermaid
flowchart LR
    U[Usuário] --> API[API]
    API --> LG[LangGraph]
    LG --> A[LLM / Agente]
    A --> R[Resposta]

    A --> RG["RAG / Genera BB"]
    RG -.->|Chunks| A

    A -->|Usar ferramenta| T[Tool]
    T --> MCP[MCP]
    MCP --> EXT["API / Serviço"]
    EXT -.->|Resultado| A

    classDef flow fill:#5858F8,color:#FFFFFF,stroke:#8B8DFF,stroke-width:2px;
    classDef rag fill:#31D49D,color:#12372D,stroke:#65E0B7,stroke-width:2px;
    classDef tools fill:#FF9A3D,color:#392000,stroke:#FFBA78,stroke-width:2px;
    classDef neutral fill:#F7F8FF,color:#252F91,stroke:#A8ACD8,stroke-width:2px;

    class LG,A flow;
    class RG rag;
    class T,MCP,EXT tools;
    class U,API,R neutral;
```

### Pessoa 1 — Conceito

Uma **Tool** é uma capacidade que disponibilizamos para o agente.

Pode ser consultar uma API, buscar uma cotação, acessar uma base ou executar alguma função.

O modelo identifica que precisa daquela capacidade e solicita o uso da ferramenta.

A aplicação executa a chamada, recebe o resultado e devolve esse resultado para o agente continuar.

Isso permite que o agente faça mais do que gerar texto.

Quando começamos a ter várias ferramentas e integrações diferentes, entra também o **MCP, Model Context Protocol**.

O MCP define um padrão para disponibilizar ferramentas e outros recursos para aplicações de IA.

### Pessoa 2 — Na nossa esteira

Na nossa estrutura, as ferramentas também fazem parte do fluxo do agente.

Quando o modelo identifica que precisa usar uma Tool, o LangGraph direciona a execução para a etapa responsável por essa chamada.

A ferramenta é executada, o resultado volta para o fluxo e o agente continua o processamento.

Com MCP, essas ferramentas podem ser disponibilizadas seguindo um padrão comum.

O agente pode se conectar a servidores MCP, identificar as ferramentas disponíveis e utilizá-las durante a execução.

Então, até aqui, temos um agente que consegue seguir um fluxo, buscar conhecimento e utilizar ferramentas.

Mas, conforme a solução cresce, concentrar muitas responsabilidades em um único agente pode aumentar bastante a complexidade.

É aí que entram os **sistemas multiagentes**.

---

# Slide 5 — Sistemas Multiagentes

## Diagrama

```mermaid
flowchart LR
    U[Usuário] --> API[API]
    API --> LG[LangGraph]
    LG --> S[Supervisor / Roteador]

    S --> A1["Agente<br/>Investimentos"]
    S --> A2["Agente<br/>Câmbio"]
    S --> A3["Agente<br/>Normas"]

    A1 --> R[Resposta]
    A2 --> R
    A3 --> R

    classDef flow fill:#5858F8,color:#FFFFFF,stroke:#8B8DFF,stroke-width:2px;
    classDef multi fill:#9B6CFF,color:#FFFFFF,stroke:#B99AFF,stroke-width:2px;
    classDef neutral fill:#F7F8FF,color:#252F91,stroke:#A8ACD8,stroke-width:2px;

    class LG flow;
    class S,A1,A2,A3 multi;
    class U,API,R neutral;
```

### Pessoa 1 — Conceito

Em vez de ter um único agente responsável por vários tipos de problema, podemos separar essas responsabilidades.

Essa é a ideia de um sistema multiagente.

Podemos ter, por exemplo, um agente especializado em investimentos, outro em câmbio e outro em normas.

Cada agente fica responsável por um domínio ou conjunto específico de tarefas.

### Pessoa 2 — Na arquitetura

E aqui estamos falando de uma escolha arquitetural.

Não significa que toda solução precise ter vários agentes.

Uma possibilidade é ter um agente supervisor.

Ele recebe a solicitação e distribui o trabalho para agentes especializados.

Outra possibilidade é ter um roteador, que identifica o tipo de solicitação e encaminha diretamente para o agente responsável.

Também podemos ter situações em que um agente produz uma resposta e outro faz uma validação antes que ela siga adiante.

A ideia principal é separar responsabilidades quando a complexidade da aplicação cresce.

---

# Slide 6 — Juntando tudo

## Diagrama

```mermaid
flowchart LR
    U[Usuário] --> API[API]
    API --> LG[LangGraph]
    LG --> S[Supervisor / Roteador]
    S --> A[Agentes especializados]
    A --> R[Resposta]

    A --> RAG[RAG]
    RAG --> G[Genera BB]
    G -.->|Contexto| A

    A --> T[Tools]
    T --> MCP[MCP]
    MCP --> EXT["APIs / Serviços"]
    EXT -.->|Resultado| A

    classDef flow fill:#5858F8,color:#FFFFFF,stroke:#8B8DFF,stroke-width:2px;
    classDef rag fill:#31D49D,color:#12372D,stroke:#65E0B7,stroke-width:2px;
    classDef tools fill:#FF9A3D,color:#392000,stroke:#FFBA78,stroke-width:2px;
    classDef multi fill:#9B6CFF,color:#FFFFFF,stroke:#B99AFF,stroke-width:2px;
    classDef neutral fill:#F7F8FF,color:#252F91,stroke:#A8ACD8,stroke-width:2px;

    class LG flow;
    class S,A multi;
    class RAG,G rag;
    class T,MCP,EXT tools;
    class U,API,R neutral;
```

**LangGraph** — Fluxo  
**RAG** — Conhecimento  
**Tools** — Capacidades  
**MCP** — Integração  
**Multiagentes** — Especialização

### Pessoa 1

Se a gente juntar tudo o que vimos, fica mais fácil entender o papel de cada peça.

O **LangGraph** organiza o fluxo do agente.

O **RAG** traz conhecimento externo para o contexto do modelo.

As **Tools** permitem que o agente utilize outras capacidades e sistemas.

O **MCP** padroniza a disponibilização dessas ferramentas.

E os **sistemas multiagentes** permitem separar responsabilidades quando a solução cresce.

### Pessoa 2

E várias dessas peças já aparecem no template que a empresa provisiona.

A ideia desse primeiro contato não é sair daqui sabendo implementar tudo isso.

É reconhecer esses componentes e entender o papel de cada um.

Quando vocês encontrarem um `graph.py`, uma configuração de RAG, uma Tool ou uma integração MCP durante o onboarding, esses elementos já vão ter algum contexto.

E a principal mensagem é esta:

**um agente moderno não é apenas um prompt conectado a um modelo.**

Ele é uma aplicação em que diferentes componentes trabalham juntos para executar um fluxo e entregar uma resposta.
