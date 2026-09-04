# GENERA RAG — Guia Técnico de Vanilla e File

Guia interno para escolha, preparação, configuração e validação de bases RAG no GENERA.

## 1. Modalidades de indexação

A modalidade define como o conteúdo será transformado em unidades vetoriais recuperáveis pelo RAG.

| Modalidade  | Unidade indexada                |
| ----------- | ------------------------------- |
| **Vanilla** | Segmentos (*chunks*) do arquivo |
| **File**    | Arquivo completo                |

A escolha depende principalmente de **como o conteúdo precisa ser recuperado para responder corretamente**.

---

# 2. Vanilla

## O que é

No Vanilla, o conteúdo de cada arquivo `.txt` é dividido em **segmentos menores, chamados chunks**, antes da geração dos embeddings.

Cada chunk passa a ser uma unidade independente no índice vetorial e pode ser recuperado isoladamente durante uma consulta.

Por isso, o arquivo pode conter conteúdos mais amplos, desde que suas partes tenham contexto suficiente para serem compreendidas separadamente.

## Quando escolher

Use Vanilla quando:

* o documento é médio ou extenso;
* o conteúdo possui capítulos, tópicos ou regras relativamente independentes;
* as consultas normalmente buscam informações pontuais;
* diferentes partes do documento podem ser úteis isoladamente;
* o acervo contém manuais, normas, regulamentos ou procedimentos amplos;
* houver integração de Instruções Normativas por número.

> **Princípio do Vanilla:** o conteúdo deve ser preparado para que cada trecho recuperado consiga manter seu significado.

## Splitter

O campo **Método de divisão** define o algoritmo utilizado para segmentar o conteúdo.

### Recursive Character Text Splitter

`RecursiveCharacterTextSplitter`

Indicado para textos livres, manuais, normas, procedimentos e regulamentos.

O algoritmo tenta preservar unidades maiores de texto antes de realizar divisões menores, priorizando parágrafos, linhas, palavras e caracteres.

É a opção padrão para conteúdos textuais sem estrutura Markdown formal.

### Markdown Header Text Splitter

`MarkdownHeaderTextSplitter`

Indicado para documentos estruturados por cabeçalhos Markdown, como `#`, `##` e `###`.

A divisão considera a hierarquia dos títulos e associa essa estrutura aos segmentos gerados.

## Chunk size

Define a quantidade máxima de tokens por segmento.

O limite configurável documentado é de até **8.192 tokens por chunk**.

Referências iniciais:

| Perfil           |      Tokens |
| ---------------- | ----------: |
| Conteúdo pequeno |     300–800 |
| Conteúdo médio   | 1.000–3.000 |
| Conteúdo amplo   | 4.000–6.000 |

Chunks menores aumentam a granularidade da recuperação.

Chunks maiores preservam mais contexto dentro de cada unidade vetorial.

Os valores devem ser calibrados por testes.

## Overlap

Define o percentual de conteúdo compartilhado entre chunks consecutivos.

Na interface Vanilla, o campo é configurável entre **0 e 100%**.

O objetivo é reduzir perda de contexto nas fronteiras de segmentação.

Overlap excessivo aumenta redundância no índice e não substitui uma boa estruturação textual.

## Separadores

O campo **Separadores** permite definir marcadores adicionais para induzir fronteiras de segmentação.

Exemplos documentados:

`###`, `***`, `---`, `FIM`, `///`.

Use apenas quando houver necessidade de estabelecer uma quebra deliberada entre blocos.

## Cabeçalhos

Quando utilizado o `MarkdownHeaderTextSplitter`, os cabeçalhos configurados na interface devem corresponder à estrutura existente no conteúdo.

Exemplos:

`#`, `##`, `###`.

## Curadoria Vanilla

O texto deve favorecer a recuperação autônoma dos chunks.

Priorize:

* títulos descritivos;
* parágrafos semanticamente completos;
* identificação explícita do assunto;
* regras, condições e exceções próximas;
* pergunta e resposta contíguas em FAQs.

Evite referências dependentes de trechos distantes, pois o segmento recuperado pode não conter o contexto original.

---

# 3. File

## O que é

No File, cada arquivo `.txt` é tratado integralmente como **uma única unidade de conhecimento**.

O arquivo não é dividido em chunks internos. Seu conteúdo completo é utilizado para formar a unidade vetorial recuperável.

Isso significa que tudo que estiver no mesmo arquivo deve fazer sentido em conjunto.

## Quando escolher

Use File quando:

* o conteúdo é curto e coeso;
* as informações são fortemente interdependentes;
* regra, condição e exceção precisam ser consideradas juntas;
* a leitura parcial pode gerar interpretação incorreta;
* o documento representa uma única situação, regra ou resposta integrada;
* o conteúdo funciona melhor como unidade completa do que como trechos independentes.

> **Princípio do File:** cada arquivo deve representar uma unidade de conhecimento coerente e autocontida.

## Unidade de conhecimento

Uma unidade pode reunir:

* regra ou resposta principal;
* contexto indispensável;
* condições de aplicação;
* exceções;
* diferentes perguntas relacionadas à mesma resposta integrada.

O principal critério de divisão é a mudança da unidade de conhecimento, e não apenas o tamanho do arquivo.

## Teste de autocontenção

Antes da indexação, valide:

**O arquivo contém contexto suficiente para ser interpretado corretamente sem depender de outro arquivo?**

Se não, a unidade está incompleta.

Também valide:

**Existe conteúdo independente dentro deste arquivo?**

Se sim, pode haver mais de uma unidade de conhecimento agrupada.

## Limite técnico

Na documentação fornecida, a modalidade File registra limite de até **8.000 tokens por arquivo `.txt`** para o modelo `Azure Embeddings API 700 TPM`.

O limite técnico não substitui o critério semântico de delimitação do arquivo.

---

# 4. Requisitos do corpus

Para Vanilla e File:

* arquivos em texto simples `.txt`;
* codificação UTF-8;
* frases encerradas com ponto final sempre que possível;
* evitar bullet points;
* evitar tabulações;
* evitar linhas em branco consecutivas;
* nome de arquivo com até 130 caracteres;
* arquivos reunidos em um único `.zip`;
* estrutura plana, sem subpastas.

A documentação consolidada registra limite de **100 MB para o pacote `.zip`**, mas também mantém esse valor como ponto pendente de confirmação técnica.

---

# 5. Configuração do índice

Na criação de um novo índice RAG, os principais campos documentados são:

| Campo                    | Configuração            |
| ------------------------ | ----------------------- |
| **Vector Store**         | Open Search             |
| **Nome do índice**       | Até 60 caracteres       |
| **Modelo de embeddings** | Modelo Azure disponível |
| **Modalidade**           | Vanilla ou File         |
| **Origem**               | Arquivo ou IN           |

A origem **Arquivo** utiliza o pacote `.zip`.

A origem **IN** permite informar o número de uma Instrução Normativa para obtenção automática do conteúdo e está associada ao fluxo Vanilla.

---

# 6. Modelos de embeddings

A documentação registra os seguintes modelos na interface:

* `Azure Embeddings 3 Large`;
* `Azure Embeddings API 700 TPM`.

Também registra os identificadores:

* `AZURE_EMBEDDINGS_3_LARGE`;
* `AZURE_EMBEDDINGS_API_700_TPM`.

A capacidade documentada da rota de embeddings é de até **8.192 tokens por entrada**.

---

# 7. Atualização da base

Sempre que arquivos forem incluídos, alterados ou removidos, é necessária nova indexação.

Para atualizar um índice existente:

1. utilize exatamente o mesmo nome do índice;
2. envie o novo corpus;
3. execute novamente a indexação.

O conteúdo anterior é substituído pelo novo lote.

Os agentes associados ao índice permanecem vinculados.

---

# 8. Validação

A validação deve verificar tanto **recuperação** quanto **qualidade do conteúdo**.

## Vanilla

Avalie:

* chunk recuperado;
* contexto disponível no chunk;
* presença de condições e exceções;
* adequação do splitter;
* chunk size;
* overlap;
* separadores e cabeçalhos, quando utilizados.

## File

Avalie:

* coerência da unidade;
* autocontenção;
* presença de condições e exceções;
* ausência de assuntos independentes no mesmo arquivo;
* limite de tokens.

Ajustes devem distinguir problemas de **curadoria textual** de problemas de **configuração da indexação**.

---

# 9. Síntese técnica

**Vanilla:** o arquivo é segmentado e cada chunk gera uma unidade recuperável. É indicado quando o conteúdo pode ser consultado por partes. A qualidade depende da estrutura textual e da configuração de splitter, chunk size e overlap.

**File:** o arquivo inteiro gera uma unidade recuperável. É indicado quando o conteúdo precisa ser interpretado em conjunto. A qualidade depende principalmente da correta delimitação e autocontenção de cada arquivo.
