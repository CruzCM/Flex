# GENERA — Criação e Gestão de RAG
### Documentação Técnica Oficial

| Metadado | Detalhe |
| :--- | :--- |
| **Versão do Documento** | 1.0 (Consolidação Canônica) |
| **Status** | Vigente (com Apêndice de Validações Técnicas) |
| **Escopo Coberto** | Criação e gestão de índices vetoriais no OpenSearch com modelos Azure |
| **Público-alvo** | Desenvolvedores, mantenedores de agentes e operadores de IA do GENERA |

---

## 1. Visão Geral

O **Agente Indexado (RAG)** do GENERA baseia-se na arquitetura RAG (*Retrieval-Augmented Generation*), que viabiliza a indexação de bases de dados documentais e a utilização de modelos de linguagem para gerar respostas contextuais fundamentadas no acervo corporativo.

### Aplicações Práticas
- Atendimento ao cliente e suporte operacional;
- Chatbots corporativos internos e externos;
- Auxílio e subsídio à tomada de decisões;
- Assistentes virtuais especialistas em bases de conhecimento específicas.

### Ciclo de Vida da Indexação
A indexação da base de conhecimento é necessária e obrigatória em dois momentos:
1. **Criação inicial do agente**: para geração do índice vetorial de consulta;
2. **Atualização do acervo documental**: sempre que arquivos forem incluídos, alterados ou removidos da base.

*(Os processos de declaração e publicação do agente ocorrem exclusivamente durante a criação inicial na plataforma).*

---

## 2. Preparação do Corpus Documental

A preparação dos arquivos que compõem o corpus deve seguir as diretrizes estruturais e de formatação a seguir para assegurar a correta extração textual e a qualidade na recuperação semântica.

### 2.1 Requisitos do Pacote (.zip)
- **Arquivo único**: Todos os documentos da base devem ser agrupados e enviados em um único pacote compactado no formato `.zip`;
- **Estrutura plana**: O arquivo `.zip` não deve conter pastas ou subpastas; todos os arquivos devem residir diretamente na raiz do pacote;
- **Tamanho do pacote**: O arquivo `.zip` aceita até **100 MB**;
- **Formatos aceitos**: As extensões admitidas dentro do pacote variam conforme a modalidade de indexação selecionada (veja a [Seção 4](#4-modalidades-de-indexação-e-segmentação)).

### 2.2 Diretrizes de Formatação dos Arquivos
- **Nomenclatura**: Nomes de arquivos com até **130 caracteres**;
- **Codificação**: Arquivos de texto devem utilizar a codificação **UTF-8**;
- **Pontuação e semântica**:
  - Encerrar as frases com ponto final sempre que possível;
  - Manter assuntos semanticamente correlacionados no mesmo arquivo, evitando quebras de linha no meio de frases.
- **Elementos a evitar**:
  - Caracteres especiais e caracteres ocultos;
  - Marcadores de tópicos (*bullet points*);
  - Linhas em branco consecutivas;
  - Tabulações.

### 2.3 Pré-validação da Base de Conhecimento
Os arquivos enviados passam por verificações de consistência executadas pelo pipeline da plataforma no início do processamento da indexação.

Para conveniência das equipes, existe a referência a um *notebook* em Python disponibilizado na wiki corporativa para pré-validação voluntária dos arquivos antes do envio (veja pendências na [Seção 8](#8-apêndice--divergências-e-pendências-para-validação)).

---

## 3. Gestão e Configuração de Índices no OpenSearch

Esta seção cobre os fluxos operacionais e campos de configuração para índices gerenciados no **OpenSearch**.

### 3.1 Fluxo de Cadastro
Ao configurar um agente indexado que ainda não possua base associada, selecione a opção **"Não, preciso criar um novo índice"** (Etapa 1.2 — Gestão de indexação).

> ⚠️ **Bloqueio Operacional**: Esta etapa é obrigatória e bloqueante para agentes RAG sem índice existente. O avanço no fluxo de criação só é liberado após a conclusão bem-sucedida da indexação.

### 3.2 Campos de Configuração

| Campo | Descrição e Regras |
| :--- | :--- |
| **Vector Store** | **Open Search** |
| **Nome do índice** | Até 60 caracteres. Recomenda-se utilizar identificadores claros (ex.: `idx-meu-indice-01` ou `idx-gecap10-v1`). O campo aceita hífens na composição do nome. |
| **Modelo de embeddings** | Seleção do modelo responsável por converter os textos em vetores (veja a [Seção 3.3](#33-modelos-de-embeddings-azure)). |
| **Modalidade de indexação** | Define a estratégia de processamento e fatiamento dos arquivos: **Vanilla**, **File** ou **Simple Directory Reader** (veja a [Seção 4](#4-modalidades-de-indexação-e-segmentação)). |
| **Origem da indexação** | Opção entre **Arquivo** ou **IN**: <br>• **Arquivo**: Exibe o campo de upload para envio do pacote `.zip` com o corpus documental;<br>• **IN (Instrução Normativa)**: Permite informar o número da norma e pressionar a tecla vírgula `,` para validação e download automático do acervo. |

### 3.3 Modelos de Embeddings Azure
Os modelos de embeddings Azure disponíveis para seleção na interface e cobertos nesta documentação são identificados conforme abaixo:

- **Rótulos exibidos na Tela de Cadastro**:
  - `Azure Embeddings 3 Large`
  - `Azure Embeddings API 700 TPM`
- **Identificadores técnicos registrados**:
  - `AZURE_EMBEDDINGS_3_LARGE`
  - `AZURE_EMBEDDINGS_API_700_TPM`

#### Características Técnicas
- **Janela por segmento**: Capacidade de processamento de até **8.192 tokens** por bloco de texto;
- **Amplitude contextual**: Segmentos extensos reduzem a fragmentação semântica e preservam a integridade de sentenças longas;
- **Densidade vetorial**: Ao acomodar mais contexto em cada vetor individual, gera-se uma menor quantidade total de embeddings no índice, otimizando o desempenho e a velocidade nas buscas semânticas em bases volumosas;
- **Entrada da API**: O *input* de texto nas requisições da API do agente suporta até 8.192 tokens.

### 3.4 Atualização e Reindexação de Índice Existente
Para atualizar a base de conhecimento de um índice já em produção sem desvincular os agentes associados:
1. No fluxo de indexação do OpenSearch, informe no campo **Nome do índice** exatamente o mesmo nome do índice já cadastrado;
2. Envie o novo arquivo `.zip` com o corpus documental atualizado;
3. O conteúdo anterior é integralmente substituído pelo novo lote indexado;
4. **Vínculos preservados**: Os agentes associados ao índice permanecem vinculados normalmente, sem necessidade de reconfiguração ou recriação.

### 3.5 Feedback da Interface durante a Indexação
- **Durante o processamento**: O botão **Avançar** permanece desabilitado e a interface exibe mensagens com o progresso contínuo;
- **Ao concluir**: Um ícone verde indica sucesso, a conclusão é confirmada por mensagem e o botão **Avançar** é habilitado.

---

## 4. Modalidades de Indexação e Segmentação

A modalidade de indexação define a estratégia algorítmica utilizada para transformar os arquivos do corpus em blocos de informação (*chunks*) consultáveis pelo agente.

```
                  ┌──────────────────────────────────────────────┐
                  │          Modalidades de Indexação            │
                  └──────────────────────┬───────────────────────┘
                                         │
         ┌───────────────────────────────┼───────────────────────────────┐
         ▼                               ▼                               ▼
    ┌─────────┐                     ┌─────────┐                     ┌─────────┐
    │ Vanilla │                     │  File   │                     │ Simple  │
    │         │                     │         │                     │Directory│
    └────┬────┘                     └────┬────┘                     └────┬────┘
         │                               │                               │
  • Por segmentos (chunks)        • Arquivo inteiro               • Múltiplos formatos
  • Formato .txt ou IN            • Formato .txt                  • .pdf, .docx, .md,
  • Splitters LangChain           • Máx. 8.000 tokens             • .csv, .epub, .mbox
  • Overlap e Separadores         • Unidade única                 • Overlap fixo
```

---

### 4.1 Modalidade Vanilla (Segmentação por Segmentos)

Na modalidade Vanilla, cada vetor gerado corresponde a um segmento (*chunk*) de texto dentro de cada arquivo `.txt`. É a opção indicada para buscas granulares e recuperação de trechos pontuais.

#### Formatos Suportados
- Arquivos `.txt`;
- Instruções Normativas (INs) via download automático informando o número da norma.

#### Métodos de Divisão de Texto (LangChain Text Splitters)
O campo **Método de divisão** define o algoritmo de fatiamento dos textos:

1. **`Recursive Character Text Splitter` (`RecursiveCharacterTextSplitter`)**:
   - Fatiamento recursivo que prioriza unidades semânticas naturais antes de dividir por caracteres;
   - Ordem de divisão: Parágrafos (`\n\n`) → Linhas (`\n`) → Palavras → Caracteres;
   - Indicado para textos livres, normas, procedimentos, relatórios e como escolha padrão geral.
2. **`Markdown Header Text Splitter` (`MarkdownHeaderTextSplitter`)**:
   - Fatiamento baseado nos cabeçalhos de marcação (`#`, `##`, `###` etc.);
   - Preserva a hierarquia lógica: cada seção sob um título gera um segmento autônomo, gravando o título como metadado do bloco;
   - Indicado para documentos técnicos, wikis e manuais já formatados em Markdown.

| Método de Divisão | Indicado para | Respeita Títulos | Preserva Metadados |
| :--- | :--- | :---: | :---: |
| **Recursive Character Text Splitter** | Texto livre em geral (padrão) | Não necessariamente | Não |
| **Markdown Header Text Splitter** | Bases estruturadas em Markdown | Sim (foco principal) | Sim |

#### Parâmetros de Configuração
- **Tamanho do segmento (em tokens)**: Quantidade máxima de tokens por bloco de texto. O teto máximo configurável na interface é de **8.192 tokens** (sugestão inicial de 450 tokens por linha, aproximadamente 1.800 caracteres);
- **Sobreposição entre segmentos (%)**: Percentual de tokens compartilhados entre blocos consecutivos. Valor configurável entre **0 e 100** (este valor é dividido por 100 no envio);
- **Separadores (opcional)**: Marcadores que delimitam quebras forçadas de blocos (ex.: `###`, `***`, `FIM`, `---`, `///`). Digite o separador e pressione a tecla ponto e vírgula `;` para validar;
- **Cabeçalhos para divisão (opcional)**: Delimitadores de títulos quando utilizado o formato Markdown (ex.: `#`, `Header 1`).

---

### 4.2 Modalidade File (Indexação por Documento Completo)

Na modalidade File, cada vetor corresponde a um arquivo `.txt` integral, sem qualquer divisão em segmentos menores.

#### Aplicação
- Documentos curtos que devem ser tratados como uma única unidade indivisível de contexto (ex.: políticas condensadas, termos de referência, FAQs de página única).

#### Parâmetros e Regras
- **Formato**: Envio em pacote `.zip` contendo exclusivamente arquivos `.txt`;
- **Limite por arquivo**: Cada arquivo `.txt` deve ter no máximo **8.000 tokens** (aproximadamente 28.000 caracteres) para o modelo `Azure Embeddings API 700 TPM`.

---

### 4.3 Modalidade Simple Directory Reader (Múltiplos Formatos)

Indicada para acervos heterogêneos que reúnem diferentes tipos de documentos em uma mesma base.

#### Formatos de Arquivo Aceitos (dentro do `.zip`)
- `.pdf`
- `.csv`
- `.docx`
- `.md`
- `.epub`
- `.hwp`
- `.mbox`

> ⚠️ **Tratamento de Extensões Não Suportadas**: O envio de arquivos com extensões não aceitas (por exemplo, imagens `.png`) causa a falha imediata da indexação. A plataforma retorna mensagem orientando a remoção do arquivo incompatível ou a alteração para Vanilla/File se o conteúdo for puramente `.txt`.

#### Parâmetros de Configuração
- **Quantidade de tokens por segmento**: Tamanho máximo de cada bloco de texto, com teto de até **8.192 tokens** (faixa de referência entre 300 e 6.000 tokens);
- **Quantidade de tokens sobrepostos (overlap)**: Número fixo de tokens compartilhados entre blocos adjacentes para manter continuidade contextual, com teto de até **100 tokens** (faixa de referência entre 10 e 50 tokens).

---

## 5. Recomendações de Parâmetros por Porte de Arquivo

A calibração entre tamanho do segmento e sobreposição (*overlap*) equilibra precisão na busca e contexto para a resposta. 

As faixas abaixo representam **referências iniciais sugeridas, que devem ser validadas empiricamente conforme o caso de uso**:

| Porte do Arquivo | Tokens por Segmento | Overlap de Tokens | Racional Técnico |
| :--- | :---: | :---: | :--- |
| **Pequeno** <br>*(poucas páginas, FAQs, políticas curtas)* | 300 – 800 | 10 – 20 | Segmentos menores evitam a diluição de trechos relevantes em documentos concisos. |
| **Médio** <br>*(manuais, procedimentos, normas)* | 1.000 – 3.000 | 20 – 35 | Equilíbrio entre especificidade na busca e contexto suficiente para a resposta. |
| **Grande** <br>*(documentos extensos, acervos consolidados)* | 4.000 – 6.000 | 35 – 50 | Overlap maior assegura a continuidade entre blocos contíguos; a ampla janela do Azure (até 8.192 tokens) reduz a fragmentação semântica. |

---

## 6. Janela de Contexto, Limites de Tokens e Casos Práticos

A execução do RAG no GeneraBB (via Plataforma BB) combina a recuperação vetorial com a chamada à API conversacional, exigindo atenção ao dimensionamento dos tokens consumidos.

### 6.1 Componentes da Entrada da LLM
A requisição enviada ao modelo conversacional é estruturada pelos seguintes elementos:
1. **`user_query`**: Pergunta realizada pelo usuário final (vetorizada pela rota de embeddings);
2. **`knowledge`**: Chunks documentais recuperados do índice vetorial pelo mecanismo de RAG;
3. **`prompt (template base)`**: Instruções operacionais e variáveis de sistema cadastradas na Engenharia de Prompts (medidas sem a injeção da query e do knowledge para evitar contagens duplicadas);
4. **`histórico das mensagens`**: Histórico dos turnos anteriores da conversação;
5. **`max_tokens`**: Parâmetro que reserva a quantidade máxima de tokens destinada à resposta gerada pelo modelo.

---

### 6.2 Casos Limite e Dimensionamento

#### Caso Limite 1 — Limite da Rota de Embeddings
O tamanho do texto submetido à vetorização possui limite de **8.192 tokens**.
- Se a `user_query` ultrapassar 8.192 tokens, a rota de embeddings retorna **Erro HTTP 400**:
  > *"This model's maximum context length is 8192 tokens. Please reduce your prompt; or completion length."*

#### Caso Limite 2 — API Conversacional sem RAG (Janela de 128k)
Para modelos conversacionais com janela de 128.000 tokens (ex.: GPT-4 128k), a restrição orçamentária engloba:
$$\text{user\_query} + \text{prompt} + \text{histórico} + \text{max\_tokens} \le 128.000$$

- **Cenário de Estouro (Erro)**:
  $$\text{Entrada} = 127.500 \text{ tokens} \quad | \quad \text{max\_tokens} = 800$$
  $$128.000 - 127.500 - 800 = -300 \text{ tokens (Limite excedido em 300 tokens)}$$
- **Cenário no Limite Exato (Sucesso)**:
  $$\text{Entrada} = 127.500 \text{ tokens} \quad | \quad \text{max\_tokens} = 500$$
  $$128.000 - 127.500 - 500 = 0 \text{ tokens (Operação dentro do limite)}$$
- **Cenário com Margem de Segurança (Sucesso)**:
  $$\text{Entrada} = 126.000 \text{ tokens} \quad | \quad \text{max\_tokens} = 1.000$$
  $$128.000 - 126.000 - 1.000 = 1.000 \text{ tokens (Margem de folga de 1.000 tokens)}$$

#### Caso Limite 3 — API Conversacional com RAG (Janela de 128k)
Com a injeção do RAG, o acervo recuperado (`knowledge`) passa a compor o orçamento da janela:
$$\text{user\_query} + \text{prompt (template)} + \text{knowledge} + \text{histórico} + \text{max\_tokens} \le 128.000$$

Como a `user_query` já está restrita pelo teto de embeddings (8.192 tokens), o fator determinante para o consumo da janela de contexto no RAG é o **tamanho total do prompt base somado ao volume do knowledge recuperado**:

- **Cenário de Estouro no RAG (Erro)**:
  $$\text{Prompt base + knowledge} = 126.000 \quad | \quad \text{user\_query} = 1.000 \quad | \quad \text{histórico} = 1.000 \quad | \quad \text{max\_tokens} = 800$$
  $$128.000 - 126.000 - 1.000 - 1.000 - 800 = -800 \text{ tokens (Limite excedido em 800 tokens)}$$
- **Cenário Válido no RAG (Sucesso)**:
  $$\text{Prompt base + knowledge} = 125.000 \quad | \quad \text{user\_query} = 1.000 \quad | \quad \text{histórico} = 1.000 \quad | \quad \text{max\_tokens} = 800$$
  $$128.000 - 125.000 - 1.000 - 1.000 - 800 = 200 \text{ tokens (Operação válida com folga de 200 tokens)}$$

---

## 7. Diretrizes para Otimização e Assertividade

Para aperfeiçoar a assertividade e a relevância das respostas fornecidas pelo agente:

1. **Ajuste do Tamanho do Chunk**: Chunks menores aumentam a precisão em respostas pontuais; chunks maiores fornecem maior cobertura de contexto;
2. **Calibração do Overlap**: Aumentar a sobreposição mitiga a perda de contexto semântico nas fronteiras entre blocos;
3. **Seleção da Modalidade e do Splitter**:
   - Utilize **Vanilla** para busca granular por trechos;
   - Utilize **File** para tratar documentos curtos como blocos indivisíveis;
   - Utilize **Simple Directory Reader** para formatos heterogêneos;
   - Em Vanilla, selecione `Markdown Header Text Splitter` se a base possuir cabeçalhos formatados, ou `Recursive Character Text Splitter` para textos contínuos;
4. **Capacidade do Modelo**: Prefira modelos com maior janela de tokens (como os modelos Azure de até 8.192 tokens) quando a base documental for extensa;
5. **Estrutura Prévia dos Documentos**: Organize e padronize a hierarquia textual antes da indexação, pois acervos bem estruturados melhoram a recuperação por similaridade;
6. **Engenharia de Prompts**: No template de prompt, inclua diretrizes explícitas orientando a LLM sobre como sintetizar, citar e fundamentar as respostas nas informações extraídas do `knowledge`.

---

## 8. Apêndice — Divergências e Pendências para Validação

Este apêndice reúne os pontos de divergência entre os materiais de apoio e inventaria ativos externos pendentes de validação técnica futura.

### 8.1 Divergências de Valores entre Fontes (Precedência: Tela > Doc Nova > Legado)

| Item | Regra Adotada (Maior Precedência) | Alternativa (Menor Precedência) | Status / Ação Necessária |
| :--- | :--- | :--- | :--- |
| **Limite do pacote .zip** | **100 MB** *(Doc Nova)* | **9 MB** *(Legado)* | Provisório (100 MB). Confirmar com o time de infraestrutura se o limite do gateway de upload é 100 MB ou 9 MB. |
| **Sobreposição em Vanilla (%)** | **0 a 100, divisão por 100** *(Tela)* | **0 a 50, divisão por 50** *(Doc Nova)* | Adotado o campo da Tela de Cadastro (0–100%). Confirmar o algoritmo de normalização da API no backend. |
| **Extensão de e-mail em Simple Directory Reader** | **`.mbox`** *(Doc Nova)* | **`MBO`** *(Legado)* | Adotado `.mbox`. Confirmar se `MBO` tratava-se de erro de digitação de `.mbox` no legado. |
| **Abrangência de regras de arquivos** | **Gerais para todo o corpus** *(Doc Nova)* | **Específicas para `.txt`** *(Legado)* | Adotada a diretriz geral. Confirmar se restrições como ausência de bullets aplicam-se a arquivos `.docx` e `.pdf`. |

### 8.2 Pontos Técnicos e de Implementação a Validar
1. **Validação do payload real da rota conversacional**: Validar com a equipe técnica da Plataforma BB se o `prompt` medido na janela de contexto engloba ou não a injeção do `knowledge` e do `user_query` em tempo de execução, para padronizar a métrica de tokens sem ambiguidades conceituais;
2. **Conjunto de caracteres aceitos no Nome do Índice**: Validar a regex completa aceita pelo frontend e backend para o campo Nome do Índice (confirmado suporte a hífens);
3. **Mapeamento de modelos de embeddings**: Confirmar a correspondência oficial de contrato da API entre os rótulos visíveis na tela (`Azure Embeddings 3 Large` / `Azure Embeddings API 700 TPM`) e seus respectivos identificadores de deployment;
4. **Identificador da rota de embeddings**: Confirmar se o deployment ativo do serviço de vetorização mantém o modelo `ada-embeddings-002` ou se já utiliza modelos Azure de geração mais recente.

### 8.3 Ativos Externos Pendentes de Fornecimento
- **Imagens e Telas**:
  - `Figura 5.1` (Interface da tela de indexação);
  - `Figura 5.2` (Interface do fluxo de integração de Instruções Normativas);
  - `Figura 8` (Fluxograma conceitual da arquitetura RAG com LLM);
  - `Print Opensearch` (Captura da tela de cadastro preenchida).
- **Scripts de Suporte**:
  - *Notebook* em Python de pré-validação da base de conhecimento referenciado na wiki corporativa.
