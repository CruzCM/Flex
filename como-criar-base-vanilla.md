# GENERA: Como Criar uma Base no Modo Vanilla
### Guia de Curadoria e Preparação de Conteúdo para Bases de Conhecimento RAG

---

## 1. Introdução — A Lógica da Recuperação por Trechos

### 1.1 O Papel da Modalidade Vanilla no GENERA
Ao estruturar uma base de conhecimento para um assistente virtual no GENERA na modalidade **Vanilla**, a dinâmica de consulta aos documentos orienta-se pela busca granular. Em vez de percorrer arquivos inteiros a cada pergunta formulada pela pessoa usuária, o sistema localiza e recupera passagens pontuais e específicas distribuídas ao longo dos textos cadastrados.

Essa característica torna a modalidade Vanilla a opção indicada para compêndios amplos, manuais detalhados, regulamentos operacionais extensos e acervos normativos oficiais. A recuperação pontual favorece que a resposta formulada pelo modelo de linguagem seja fundamentada nas cláusulas, artigos ou orientações pertinentes à dúvida apresentada, sem sobrecarregar a janela de contexto de entrada com trechos irrelevantes de outras partes do material.

### 1.2 A Atitude de Curadoria: Escrever para a Segmentação
A preparação de acervos para a modalidade Vanilla exige uma atitude editorial própria. Todo arquivo inserido na base passa por um processo automatizado de fatiamento (*chunking*), no qual o texto corrido é subdividido em blocos menores (*chunks* ou segmentos) antes da conversão em vetores de busca semântica. Cada segmento passa a existir no índice como uma unidade autônoma de consulta.

Diante desse comportamento da plataforma, o papel da equipe responsável pela base não é tentar controlar a linha exata onde cada corte ocorrerá, mas sim **preparar o texto para que ele possa ser segmentado sem perder o sentido original**. 

Se um parágrafo contiver uma regra importante, mas os pré-requisitos essenciais para essa regra tiverem sido mencionados páginas antes sob termos genéricos, o assistente poderá recuperar a regra e não capturar os pré-requisitos, favorecendo respostas incompletas ou imprecisas. A curadoria atua, portanto, para aumentar a probabilidade de que a informação necessária acompanhe a regra que ela qualifica.

### 1.3 O Princípio da Autossuficiência Contextual do Trecho
O princípio fundamental que orienta toda a preparação de conteúdo no modo Vanilla pode ser resumido na seguinte diretriz de curadoria:

> **Princípio Central:**  
> *"Estruturar o texto para que cada trecho, ao ser consultado de forma autônoma pelo assistente, contenha contexto explícito suficiente para responder à dúvida com exatidão, sem depender de premissas ocultas ou referências distantes."*

Para aplicar esse princípio no dia a dia, a equipe de negócio deve submeter cada seção, parágrafo ou procedimento ao **teste da leitura isolada**:

> **O Teste da Leitura Isolada:**  
> *"Se o assistente localizar e ler exclusivamente este trecho para responder à dúvida de uma pessoa usuária, ele terá as condições, exceções e identificações necessárias para fornecer uma orientação correta, segura e inequívoca?"*

Se a resposta for afirmativa, o trecho tende a ser adequado para a segmentação. Se a resposta for negativa — porque o trecho utiliza termos vagos como *"ele"*, *"esse benefício"*, *"o procedimento acima"* ou porque a exceção que invalida a regra ficou dispersa em outra parte do documento —, convém intervir editorialmente na estrutura do texto antes de disponibilizá-lo para indexação.

---

## 2. Organização e Escopo dos Arquivos `.txt`

### 2.1 O Papel do Arquivo no Modo Vanilla
No modo Vanilla, o arquivo de texto (`.txt`) atua primordialmente como um **invólucro de transporte e compêndio temático**, e não como a unidade final de busca. Como o processamento da plataforma subdivide internamente o material em múltiplos segmentos, um mesmo arquivo pode reunir textos de médio ou grande porte, abrangendo seções, capítulos e procedimentos articulados.

Dessa constatação decorre uma diretriz operacional relevante: **a equipe responsável pela base não precisa recortar previamente seus manuais e regulamentos em dezenas de microarquivos individuais**. A segmentação é executada pelos algoritmos da plataforma. O esforço humano de curadoria deve concentrar-se na qualidade interna da redação e na delimitação temática dos arquivos.

### 2.2 Agrupamento por Domínio Funcional vs. Fragmentação Excessiva
Para determinar a fronteira de cada arquivo `.txt`, o critério orientador é a **coesão por domínio funcional ou macroprocesso**:

* **Convém manter no mesmo arquivo:** Todas as matérias, rotinas e diretrizes que pertençam a um mesmo processo ou domínio negocial coeso. Por exemplo, um compêndio unificado sobre *"Gestão de Benefícios e Auxílios"* pode reunir auxílio-creche, auxílio-alimentação e vale-transporte em um único arquivo `.txt`, desde que cada tópico seja desenvolvido com contexto próprio.
* **Convém separar em arquivos distintos:** Matérias pertencentes a domínios de negócio substancialmente diferentes e sem intersecção operacional. Por exemplo, reunir diretrizes de auditoria interna com políticas de concessão de crédito imobiliário em um mesmo `.txt` tende a dispersar a coerência temática do arquivo e dificulta a governança do acervo.

A fragmentação manual excessiva — isto é, criar um arquivo `.txt` para cada pequeno parágrafo ou pergunta pontual — deve ser evitada no Vanilla. Ela cria sobrecarga desnecessária na gestão do pacote `.zip`, dispersa a visão de conjunto do processo e desconsidera a inteligência de fatiamento dos algoritmos de indexação.

### 2.3 Quando Manter Documentos Consolidados e Quando Desmembrar
A tabela abaixo sintetiza os critérios de decisão para a montagem dos arquivos:

| Situação do Acervo de Origem | Recomendação de Curadoria | Racional Negocial |
| :--- | :--- | :--- |
| **Manual de operações volumoso (ex.: dezenas de páginas sobre um único produto)** | Manter em um único arquivo `.txt` consolidado. | O fatiador segmentará os capítulos automaticamente; manter o compêndio íntegro facilita o versionamento e a substituição do lote. |
| **Documento que compila assuntos totalmente desconexos em anexo** | Desmembrar os anexos não correlacionados em arquivos `.txt` próprios. | Reduz o risco de que o final de uma matéria operacional se una indevidamente ao início de uma matéria puramente administrativa no mesmo segmento. |
| **Acervo extenso cuja edição paralela é dividida entre vários analistas** | Dividir o material em arquivos por submódulos funcionais coesos. | Facilita a governança operacional interna da equipe, permitindo atualizar partes do acervo sem conflito de edição. |

---

## 3. Diretrizes de Redação para Textos Segmentáveis

### 3.1 O Parágrafo como Unidade Natural de Sentido
Na modalidade Vanilla, a redação deve estruturar-se em torno de parágrafos funcionais. No algoritmo padrão de segmentação do GENERA, a quebra de parágrafo (duplo salto de linha `\n\n`) é o divisor preferencial de blocos. Isso significa que parágrafos bem articulados funcionam como blocos de construção adequados para a recuperação semântica.

Para favorecer respostas seguras, convém observar dois cuidados em relação à extensão dos parágrafos:
1. **Evitar parágrafos excessivamente extensos e sem pausas:** Blocos textuais contínuos e maciços podem exceder a capacidade planejada dos segmentos e forçar o algoritmo a cortar o texto no meio de frases ou em quebras de linha casuais, gerando fragmentos truncados.
2. **Evitar orações fragmentadas e descontextualizadas:** Frases isoladas soltas pelo texto costumam carregar pouco peso semântico e podem ter sua relevância reduzida na busca vetorial por falta de densidade contextual.

O padrão recomendado é construir cada parágrafo em torno de **uma unidade de sentido completa**, curta o suficiente para não misturar assuntos distintos, acompanhada de sua contextualização essencial e encerrada formalmente com ponto final.

### 3.2 Eliminação de Referências Remotas e Ancoragem de Sujeito
Um dos fatores mais frequentes de respostas imprecisas em assistentes virtuais é a presença de **anáforas e referências dependentes**. Em textos corporativos tradicionais, é comum encontrar redações como:

* *"Conforme estabelecido no artigo anterior, ele terá direito ao reembolso..."*
* *"Nesses casos, a solicitação deve ser remetida à gerência..."*
* *"O referido benefício não contempla dependentes indiretos..."*

Quando o documento é lido por uma pessoa do início ao fim, essas referências são compreensíveis. Porém, quando o algoritmo recupera apenas o trecho que contém *"o referido benefício"*, o assistente pode não identificar a qual benefício a frase se refere, podendo omitir a resposta ou associá-la a um produto incorreto.

A orientação prática de curadoria é aplicar a **Técnica da Âncora de Abertura**:
* A primeira frase de cada parágrafo ou de cada nova regra deve declarar explicitamente o **sujeito substantivo** e o **objeto da orientação** (ex.: *"O Auxílio-Natalidade destina-se às pessoas colaboradoras ativas..."* ou *"Nas solicitações de Cancelamento de Viagem a Serviço, a pessoa solicitante deve..."*).
* No interior do parágrafo, após fixada a âncora inicial, a redação pode fluir naturalmente com pronomes e coesão textual regular.

### 3.3 A Regra da Proximidade: Conectando Regras, Condições e Exceções
Muitas regras de negócio possuem requisitos de elegibilidade, prazos estritos e hipóteses de vedação. Se a regra geral for enunciada em um parágrafo e sua exceção for colocada em páginas distantes (ou relegada a uma nota remota), eleva-se o risco de o sistema recuperar a regra geral e desconsiderar a exceção.

Para mitigar esse risco, adota-se a **Regra da Proximidade Contextual**:

```
[Estrutura Recomendada de Regra de Negócio]
┌────────────────────────────────────────────────────────┐
│ ENUNCIADO DA REGRA GERAL (com sujeito e objeto claros) │
├────────────────────────────────────────────────────────┤
│ CONDIÇÕES DE APLICAÇÃO (prazos, público e requisitos)  │
├────────────────────────────────────────────────────────┤
│ EXCEÇÕES E VEDAÇÕES (hipóteses impeditivas e limites)   │
└────────────────────────────────────────────────────────┘
   ▲ Elementos integrados no mesmo parágrafo
     ou em parágrafos imediatamente contíguos.
```

A aproximação física entre regra, condição e exceção não representa uma garantia matemática absoluta de que tudo caberá no mesmo segmento, mas **tende a manter os elementos na mesma vizinhança textual**, aumentando a chance de que sejam capturados de forma coordenada pelo processo de recuperação.

### 3.4 O Papel de Títulos e Cabeçalhos Informativos
Títulos e subtítulos atuam como metadados semânticos para o conteúdo que os sucede. Títulos vagos, puramente numéricos ou telegráficos prejudicam a qualidade da busca.

* **Evitar títulos genéricos:** *"1.1 Regras"*, *"Condições Gerais"*, *"Diversos"*, *"Importante"*, *"Tabela"*.
* **Preferir títulos descritivos e autônomos:** *"Critérios de Elegibilidade para o Adiantamento do 13º Salário"*, *"Hipóteses de Indeferimento do Reembolso de Despesas Médicas"*, *"Prazos Operacionais para Abertura de Conta por Pessoa Não Residente"*.

Um título informativo ajuda a situar o tema com clareza, permitindo que o modelo de linguagem compreenda a matéria mesmo quando herda apenas o início daquela seção.

---

## 4. Estratégias de Divisão de Conteúdo (Text Splitters)

A plataforma GENERA disponibiliza dois métodos algorítmicos para fatiamento do texto no modo Vanilla. A escolha adequada do método simplifica a curadoria e melhora a aderência das respostas.

### 4.1 Divisão Recursiva (`RecursiveCharacterTextSplitter`) — O Padrão para Texto Livre
O `RecursiveCharacterTextSplitter` é a estratégia padrão recomendada para a generalidade dos documentos corporativos. 

#### Como Funciona
O algoritmo opera de forma recursiva tentando preservar as unidades semânticas naturais do texto antes de recorrer à quebra de caracteres. Ele segue esta hierarquia de separadores:
1. Quebra de parágrafo (`\n\n`) — tenta manter o parágrafo inteiro;
2. Quebra de linha simples (`\n`) — se o parágrafo for maior que o tamanho configurado, divide nas linhas;
3. Espaço entre palavras (` `) — se a linha for muito longa, divide entre palavras;
4. Caracteres individuais — último recurso, utilizado apenas se uma única palavra for maior que o bloco.

#### Quando Utilizar
* Manuais e relatórios redigidos em texto corrido;
* Políticas corporativas e procedimentos normativos comuns;
* Acervos em texto livre sem sintaxe de marcação prévia.

#### O que a Área de Negócio Deve Fazer
* Cuidar da arquitetura de parágrafos, mantendo ideias fechadas com salto de linha duplo padrão;
* Assegurar que frases terminem com ponto final;
* Manter regras e exceções em parágrafos adjacentes.

### 4.2 Divisão por Cabeçalhos (`MarkdownHeaderTextSplitter`) — Para Estruturas Hierárquicas
O `MarkdownHeaderTextSplitter` é uma estratégia especializada projetada para documentos que já possuam (ou possam receber) uma estruturação formal de títulos por hierarquia Markdown (`#`, `##`, `###`).

#### Como Funciona
O algoritmo utiliza os marcadores de título cadastrados na interface para orientar os pontos de quebra do documento. Cada seção situada sob um cabeçalho tende a gerar um segmento específico, associando o título da seção ao corpo do texto fatiado.

#### Quando Utilizar
* Manuais técnicos amplos e bases exportadas de wikis institucionais;
* Compêndios extensos claramente organizados em capítulos, títulos e subtítulos;
* Acervos onde a hierarquia dos tópicos é indispensável para contextualizar os procedimentos descritos.

#### Requisitos de Preparação
* Os títulos devem utilizar a sintaxe padrão Markdown (`# Título Principal`, `## Subtítulo`, `### Seção`);
* Títulos em níveis equivalentes devem manter coerência temática e nomenclatura descritiva;
* O campo de cabeçalhos na interface deve ser preenchido com os mesmos marcadores utilizados no texto (ex.: `#`, `##`).

### 4.3 Quando Utilizar Separadores Opcionais (e Quando Evitá-los)
A tela de cadastro do GENERA oferece o campo opcional **Separadores**, onde o usuário pode cadastrar marcadores arbitrários (como `###`, `---` ou `///`), confirmando com a tecla ponto e vírgula `;`.

* **Quando utilizar:** O uso de separadores customizados justifica-se estritamente quando houver necessidade de **induzir uma fronteira de corte deliberada** entre matérias totalmente distintas agrupadas em um mesmo arquivo. Por exemplo, ao compilar instruções operacionais não correlacionadas no mesmo `.txt`, a inserção de `###` entre elas orienta o pipeline a não unificar o fim da primeira com o início da segunda no mesmo segmento.
* **Quando evitar:** Não se deve espalhar separadores ao final de cada parágrafo ou subtítulo. O excesso de separadores artificiais gera microfragmentação, polui o texto e prejudica o fluxo semântico natural do fatiamento recursivo.

---

## 5. Compreendendo Granularidade de Segmentos e Sobreposição (*Overlap*)

### 5.1 O Equilíbrio da Granularidade: Especificidade Semântica vs. Amplitude de Contexto
A calibração do tamanho do segmento (*chunk size*) expressa em tokens é um dos elementos centrais para o comportamento do RAG. Sob a ótica de negócio, essa decisão não é puramente matemática, mas sim um balanço entre **especificidade semântica** e **amplitude de contexto**:

```
MENOR TAMANHO DE SEGMENTO                      MAIOR TAMANHO DE SEGMENTO
(Ex.: 300 – 800 tokens)                         (Ex.: 4.000 – 6.000 tokens)
┌───────────────────────────────┐               ┌───────────────────────────────┐
│ • Alta especificidade         │               │ • Ampla visão de conjunto     │
│ • Favorece regras curtas      │     VS        │ • Preserva processos longos   │
│ • Risco: omitir exceções ou   │               │ • Risco: diluir o foco e      │
│   condições em outros blocos  │               │   consumir espaço de entrada  │
└───────────────────────────────┘               └───────────────────────────────┘
```

* **Segmentos menores:** Tendem a localizar com grande especificidade semântica termos pontuais (como uma alíquota, um prazo ou um canal de atendimento). Contudo, se a resposta demandar entender a justificativa ou uma série de pré-requisitos, o segmento pode ser insuficiente.
* **Segmentos maiores:** Oferecem amplitude contextual para procedimentos encadeados, aumentando a chance de que regras e exceções permaneçam no mesmo segmento. Contudo, blocos muito amplos ocupam mais espaço da janela de contexto de entrada da consulta e podem reduzir a precisão da recuperação em buscas muito específicas.

### 5.2 O Papel da Sobreposição (*Overlap*) como Proteção de Fronteira
Quando um texto longo é dividido sequencialmente em blocos, existe a possibilidade de uma frase, conceito ou regra ser seccionada na linha de transição entre um bloco e outro.

Para mitigar esse efeito, a plataforma oferece o mecanismo de **sobreposição (*overlap*)**. O overlap compartilha uma proporção do conteúdo final de um segmento no início do segmento subsequente:

```
Segmento 1: [ ... Início da Regra ──► Requisitos ──► [Área de Sobreposição] ]
                                                     │
                                                     ▼
Segmento 2:                                [ [Área de Sobreposição] ──► Exceções ──► Conclusão ... ]
```

Dessa forma, o overlap atua como uma margem de proteção na fronteira, que **pode preservar parte do contexto adjacente** caso o corte algorítmico ocorra próximo a uma sentença relevante. 

No entanto, o overlap não reconhece automaticamente fronteiras gramaticais completas nem impede de forma absoluta o truncamento. Além disso, convém evitar sobreposições desnecessariamente elevadas, pois valores excessivos podem gerar redundância no índice vetorial e reduzir a diversidade de informações distintas aproveitadas na resposta. A calibragem deve ser progressiva e empiricamente validada.

### 5.3 Parâmetros da Plataforma e Faixas de Referência Inicial
Na interface de gestão de indexação do GENERA, a configuração de parâmetros deve ser compreendida conforme as seguintes diretrizes:

1. **Teto Técnico Documentado:** Com os modelos Azure suportados, o campo de tamanho de segmento aceita configurações de **até 8.192 tokens** por bloco.
2. **Campo de Sobreposição na Interface:** O campo é expresso em formato **percentual (0 a 100%)**, permitindo ajustar a proporção de compartilhamento entre blocos conforme o perfil do conteúdo.
3. **Faixas de Referência Empírica para Partida:** As faixas a seguir representam sugestões orientadoras de partida, devendo ser testadas e refinadas na prática:

| Porte e Perfil do Acervo | Tamanho Sugerido (Tokens) | Racional Negocial de Aplicação |
| :--- | :---: | :--- |
| **Acervos Concêntricos e Pequenos**<br>*(FAQs, comunicados curtos, políticas breves)* | **300 a 800** | Favorece que respostas a dúvidas pontuais sejam localizadas com boa especificidade semântica. |
| **Manuais Operacionais e Procedimentos Médios**<br>*(Manuais de rotina, regulamentos de produtos)* | **1.000 a 3.000** | Faixa de equilíbrio que permite acomodar a regra geral, suas condicionantes e etapas executivas. |
| **Compêndios Amplos e Acervos Consolidados**<br>*(Documentos densos, grandes compêndios de crédito)* | **4.000 a 6.000** | Ajuda a preservar a continuidade de processos longos e narrativas extensas. |

---

## 6. Curadoria Aplicada aos Diferentes Gêneros de Conteúdo

A preparação do texto deve adequar-se à natureza do gênero documental trabalhado. A seguir, destacam-se as recomendações práticas para os formatos corporativos mais comuns:

### 6.1 Manuais e Guias de Instrução
* **Articulação em Capítulos e Tópicos:** Organize o manual em tópicos bem delimitados. Se optar pelo splitter recursivo, separe os tópicos com linhas duplas e títulos expressivos; se optar pelo splitter Markdown, utilize `#` para módulos e `##` para rotinas.
* **Autonomia de Seções:** Evite que o capítulo de um procedimento dependa de uma leitura obrigatória de muitas páginas anteriores. Cada procedimento operacional deve enunciar sucintamente seu objetivo logo na abertura.

### 6.2 Procedimentos Operacionais e Fluxos Sequenciais
* **Linearidade dos Passos:** Apresente os passos em sequência ordenada textual (ex.: *"Passo 1: Acessar o sistema X..."; "Passo 2: Preencher o formulário Y..."*).
* **Condições Intermediárias:** Se uma etapa do fluxo contiver uma condição de desvio (ex.: *"Se o valor for superior a R$ 10.000, solicitar autorização prévia..."*), mantenha essa condição explicitada junto ao próprio passo executivo correspondente, e não ao final de todo o procedimento.

### 6.3 Políticas Corporativas e Requisitos de Elegibilidade
* **Contiguidade de Critérios:** Ao definir quem tem direito a determinado benefício ou linha de financiamento, enumere os requisitos de elegibilidade de forma direta e contínua.
* **Explicitação de Vedações:** As vedações e hipóteses impeditivas devem suceder imediatamente a lista de direitos, utilizando frases declarativas pontuadas (ex.: *"É vedada a concessão deste benefício a colaboradores em período de experiência."*).

### 6.4 Perguntas Frequentes (FAQs) — A Regra da Contiguidade
No modo Vanilla, a curadoria de perguntas frequentes exige disciplina editorial:

> **Diretriz Prática para FAQ no Vanilla:**  
> **A pergunta e a resposta devem formar uma unidade temática imediata e contígua.**

* **Estrutura recomendada:** Cada item do FAQ deve conter a pergunta na primeira linha e o texto da resposta iniciando nas linhas seguintes, encerrando com ponto final.
* **Prática incorreta a evitar:** Evite elaborar uma lista com perguntas no início do arquivo `.txt` para depois colocar as respostas páginas adiante. O fatiamento tende a separar as perguntas das respostas, prejudicando a recuperação semântica.
* **Manuais não devem ser convertidos em FAQs artificiais:** Conteúdos expositivos e manuais formais funcionam muito bem em formato declarativo narrativo; não é recomendável forçar a conversão de regulamentos em perguntas simuladas.

### 6.5 Normas Oficiais e Instruções Normativas (Regime de Salvaguarda)
A curadoria de normas regulatórias institucionais e Instruções Normativas (INs) exige respeito a requisitos rigorosos de segurança e conformidade:

1. **Priorização da Integração Automática:** Sempre que a norma fizer parte do repositório oficial do GENERA, deve-se priorizar a importação automática informando o número oficial da norma no campo de cadastro.
2. **Inviolabilidade da Redação Jurídica Oficial:** Caso a carga de uma norma seja realizada via arquivo `.txt`, **é vedado resumir, parafrasear ou alterar a redação legal dos artigos e incisos**. Alterações de redação em textos normativos geram divergência com a legislação corporativa vigente e criam riscos institucionais.
3. **Preservação Estrutural:** Não reorganize a ordem dos artigos nem suprima títulos, capítulos e remissões normativas oficiais sem autorização formal do órgão detentor da norma.
4. **Segregação de Notas Autorais:** Se a equipe de negócio desejar incluir orientações práticas ou comentários sobre a aplicação da norma, esses comentários devem ser redigidos em arquivo `.txt` próprio ou claramente segregados sob uma seção intitulada *"Comentários Operacionais e Interpretação Prática"*, evitando que o assistente confunda a interpretação local com o texto legal estrito.

### 6.6 Conversão e Linearização de Tabelas e Matrizes
A plataforma orienta a não utilizar tabulações nem marcadores gráficos visuais nos arquivos `.txt`. Por isso, tabelas de alçadas, matrizes de decisão e quadros de prazos não devem ser desenhados com arte ASCII (grades de barras `|`, hífens `-` ou cruzes `+`), pois as quebras de linha podem desestruturar a matriz e dificultar a interpretação dos dados.

A solução de curadoria é a **Linearização Semântica**:
* Cada linha da tabela original é convertida em uma oração declarativa completa e independente, que carrega as coordenadas da parametrização (critério, alçada, prazo e condição).
* *Exemplo original em grade:* Linha indicando faixa de valor, prazo e aprovador.
* *Conversão linear recomendada:*  
  *"Para propostas de crédito com valor entre R$ 10.001 e R$ 50.000, o prazo máximo de amortização é de até 36 meses e a competência de aprovação é da Gerência Geral de Agência."*

Com essa redação, caso aquele trecho específico seja recuperado isoladamente pelo assistente, ele conterá as informações necessárias para fundamentar a resposta à pessoa usuária.

---

## 7. Validação Prática da Base de Conhecimento

### 7.1 O Ciclo de Teste Empírico por Amostragem Representativa
A verificação da qualidade de uma base Vanilla deve ser prática, ágil e proporcional ao risco e à complexidade do processo de negócio. O objetivo é garantir que o acervo preparado atenda às reais necessidades do público-alvo com método e rastreabilidade.

Recomenda-se adotar o **Ciclo de Validação em Quatro Etapas**:

```
[1. Amostra Representativa] ──► [2. Gabarito Prévio] ──► [3. Consulta e Inspeção] ──► [4. Diagnóstico e Ajuste]
 (Dúvidas do negócio)           (Trecho do texto)         (Avaliar resposta e exceções)   (Ajustar texto ou parâmetros)
```

1. **Elaboração da Amostra de Perguntas:** Selecionar uma quantidade de perguntas proporcional ao porte e à criticidade da base, cobrindo dúvidas frequentes, perguntas sobre prazos/valores, cenários com exceções e formulações alternativas de linguagem.
2. **Definição do Gabarito Negocial:** Antes de consultar o agente, registrar qual parágrafo ou seção do material cadastrado detém a resposta completa e esperada para cada pergunta.
3. **Consulta e Inspeção de Evidências:** Submeter as perguntas ao assistente e avaliar a resposta gerada. Verificar se a resposta foi direta, se respeitou os valores da documentação e se as condições e exceções pertinentes foram consideradas.
4. **Diagnóstico Orientado a Sintomas:** Se uma resposta for incorreta ou omissa, identificar a causa provável para intervir de forma direcionada.

### 7.2 Como Inspecionar se a Resposta Carrega o Contexto Adequado
Durante a validação, a equipe deve atentar aos seguintes sintomas nas respostas do assistente:

* **Sintoma: O assistente informou a regra geral, mas omitiu a exceção impeditiva.**  
  *Causa provável:* A exceção estava descrita em um parágrafo muito distante da regra geral ou o segmento (*chunk*) utilizado é curto para alcançar ambos.
* **Sintoma: O assistente confundiu o público-alvo ou atribuiu uma regra a um produto diferente.**  
  *Causa provável:* O trecho recuperado utilizava pronomes vagos (*"ele"*, *"este produto"*) em vez de identificar o nome formal da matéria na abertura do parágrafo.
* **Sintoma: O assistente respondeu que não encontrou a informação sobre uma linha de tabela.**  
  *Causa provável:* A tabela foi formatada em grade visual com tabulações, sendo desestruturada no fatiamento.

### 7.3 Diagnóstico de Ajustes: Correção de Redação vs. Calibração de Configuração
Ao constatar falhas de recuperação na validação, a equipe deve ponderar se a solução reside na redação do texto ou nos parâmetros da plataforma:

| Problema Observado no Teste | Ação Recomendada no Conteúdo (Texto) | Ação Recomendada na Configuração |
| :--- | :--- | :--- |
| Regra recuperada sem a respectiva exceção | Reposicionar a exceção para o mesmo parágrafo ou para a linha imediatamente subsequente à regra. | Se o texto já estiver contíguo, avaliar aumento gradual do tamanho de segmento (*chunk size*). |
| Frases truncadas ou respostas cortadas no meio | Dividir parágrafos muito extensos em unidades menores fechadas com ponto final. | Avaliar ajuste progressivo na sobreposição (*overlap*) percentual para proteger bordas de corte. |
| Trecho recuperado perde o sujeito da frase | Reescrever a abertura do parágrafo aplicando a técnica da âncora contextual substantiva. | Não requer ajuste de parâmetro; intervenção estritamente textual. |
| Dados de tabela recuperados de forma distorcida | Linearizar as linhas da tabela em frases declarativas completas. | Não requer ajuste de parâmetro; intervenção estritamente de formatação. |

---

## 8. Requisitos de Formatação do Arquivo e do Pacote

Para reduzir falhas de validação e formatação durante a indexação, os arquivos da base Vanilla devem observar as diretrizes técnicas documentadas pela plataforma:

### 8.1 Diretrizes Estruturais do Arquivo `.txt`
* **Extensão e Formato:** Arquivos estritamente em texto simples com extensão `.txt`.
* **Codificação:** Padrão **UTF-8**.
* **Pontuação das Frases:** As frases devem ser encerradas com ponto final sempre que possível, facilitando a identificação dos cortes sintáticos.
* **Elementos a Evitar:**
  - Não utilizar marcadores gráficos de tópicos (*bullet points* como `•`, `*`, `-`);
  - Não utilizar tabulações (tecla *Tab*);
  - Não utilizar linhas em branco consecutivas (utilizar no máximo um salto de linha duplo entre parágrafos);
  - Não utilizar caracteres de controle, símbolos gráficos fora do padrão ou caracteres ocultos gerados por editores ricos (essa restrição não se aplica a pontuações regulares nem a marcadores textuais expressamente configurados, como `#` em Markdown ou separadores cadastrados).

### 8.2 Diretrizes do Pacote `.zip`
* **Arquivo Compactado Único:** Todos os arquivos `.txt` devem ser agrupados e enviados em um único pacote `.zip`.
* **Estrutura Estritamente Plana:** O arquivo `.zip` **não deve conter pastas ou subpastas**. Todos os arquivos `.txt` devem residir diretamente na raiz do pacote compactado.
* **Nomenclatura:** Os nomes dos arquivos devem conter no máximo **130 caracteres**.
* **Tamanho do Pacote:** Até **100 MB** (referência registrada na interface, pendente de confirmação técnica de gateway corporativo).

---

## 9. Modelos Orientadores e Casos Práticos

Os modelos abaixo são estruturas conceituais orientadoras que ilustram a aplicação prática das diretrizes deste guia. A ordem dos blocos pode ser adaptada conforme a realidade de cada documento, desde que preservadas a completude do contexto e a conformidade técnica.

---

### 9.1 Modelo 1: Tópico de Procedimento / Manual (Texto Declarativo)

```
[NOME DESCRITIVO DO PROCEDIMENTO OU REGRA]
Escreva um título contextualizado que identifique a rotina e o domínio.

[ENUNCIADO DA REGRA E ÂNCORA DE SUJEITO]
Declare na primeira frase quem é o público-alvo e qual é o direito, dever ou objetivo
da rotina corporativa. Utilize frases completas encerradas com ponto final. Evite
pronomes vagos como sujeito de abertura.

[CRITÉRIOS E PRÉ-REQUISITOS]
Apresente em parágrafo contíguo as condições de elegibilidade, canais oficiais de
atendimento e documentação exigida para a solicitação.

[EXCEÇÕES E RESTRIÇÕES IMEDIATAS]
Declare expressamente, logo na sequência, as hipóteses de indeferimento, os prazos
limites e os casos em que a orientação geral não se aplica.

[ETAPAS OPERACIONAIS] (quando aplicável)
Descreva os passos executivos lineares em frases completas:
Passo 1: Acessar o sistema institucional e selecionar o módulo específico.
Passo 2: Anexar a documentação comprobatória em formato digital legível.
Passo 3: Confirmar o envio da solicitação e registrar o número de protocolo.
```

---

### 9.2 Modelo 2: Acervo de Perguntas Frequentes (FAQ Contíguo)

```
Qual é o prazo para solicitação do Auxílio-Creche por colaboradores ativos?
O colaborador ativo pode solicitar o Auxílio-Creche a partir do nascimento ou adoção
da criança até que ela complete seis anos de idade. A solicitação deve ser aberta
pelo portal de benefícios corporativo, acompanhada da certidão de nascimento e da
comprovação de matrícula em instituição regular de ensino.

Quais são as condições de cancelamento automático do Auxílio-Creche?
O pagamento do Auxílio-Creche é cancelado automaticamente no mês subsequente àquele
em que a criança completar seis anos de idade, ou em caso de rescisão contratual do
colaborador titular. Nos casos de licença não remunerada superior a trinta dias, o
benefício permanece suspenso durante todo o período de afastamento.
```

*(Nota: Repare na separação por salto duplo de linha entre um par pergunta-resposta e o seguinte, favorecendo a delimitação natural de cada unidade temática).*

---

### 9.3 Modelo 3: Linearização de Matriz de Alçadas e Prazos

```
Diretrizes e alçadas decisórias para concessão de adiantamento emergencial.

Para solicitações de adiantamento emergencial com valor até R$ 2.000,00, o prazo de
análise é de até dois dias úteis e a alçada competente de aprovação é a Chefia Imediata
do colaborador solicitante.

Para solicitações de adiantamento emergencial com valor entre R$ 2.001,00 e R$ 5.000,00,
o prazo de análise é de até quatro dias úteis e a alçada competente de aprovação é a
Gerência de Área ou unidade equivalente.

Para solicitações de adiantamento emergencial com valor acima de R$ 5.000,00, o prazo de
análise é de até sete dias úteis e a competência decisória exclusiva é do Comitê de
Recursos Humanos. Não são admitidas concessões para colaboradores com pendências de
prestação de contas em adiantamentos anteriores.
```

---

### 9.4 Estudo de Caso: "Antes e Depois" da Curadoria Textual

Para ilustrar o efeito dessas orientações, observe a comparação entre um texto original não preparado e o mesmo conteúdo após a curadoria recomendada:

#### O Texto Antes da Curadoria (Inadequado para Vanilla)
```
1.1 Do Benefício
Ele poderá ser requerido a qualquer momento. Conforme informado no item anterior,
a solicitação deve ser aberta online anexando o comprovante.

O prazo máximo é de 15 dias.

Exceções:
Em casos excepcionais, não se aplica.
```
> **Fragilidades deste texto:** O sujeito (*"Ele"*) é vago; o texto depende de menção remota (*"no item anterior"*); a exceção está isolada sem identificar a que regra se refere nem o que configura o caso excepcional. No fatiamento, essas frases podem ser separadas e perder seu sentido contextual.

#### O Texto Após a Curadoria (Adequado para Vanilla)
```
Solicitação e prazos do Reembolso de Despesas com Cursos e Treinamentos Externos.

A pessoa colaboradora ativa pode requerer o Reembolso de Despesas com Cursos e
Treinamentos Externos a qualquer momento durante o ano civil, desde que o tema do
curso possua correlação direta com as atribuições de seu cargo atual. A solicitação
deve ser protocolada no Portal de Desenvolvimento Corporativo, acompanhada da nota
fiscal comprobatória da instituição de ensino e do certificado de conclusão.

O prazo regular para análise e crédito do Reembolso de Despesas com Treinamento é
de até quinze dias úteis a contar da data de validação da documentação. O reembolso
não se aplica a cursos que não tenham recebido anuência prévia formal da liderança
imediata antes do início das aulas, nem a despesas com aquisição de materiais didáticos
avulsos ou deslocamento.
```
> **Vantagens deste texto:** A âncora inicial identifica o benefício expressamente; a regra geral, o canal, a documentação, o prazo e as vedações impeditivas compõem um bloco coeso. O trecho recuperado tende a oferecer contexto mais consistente para fundamentar a resposta à pessoa usuária.

---

## 10. Checklist de Verificação Pré-Publicação

Antes de compilar o pacote `.zip` e submetê-lo à indexação no GENERA, percorra a lista de verificação abaixo:

### Verificação Semântica e Textual
- [ ] **Ancoragem de Abertura:** Os parágrafos e tópicos iniciam identificando expressamente a matéria e o público, evitando abertura por pronomes vagos?
- [ ] **Contiguidade de Restrições:** Requisitos, vedações e exceções foram redigidos no mesmo parágrafo ou imediatamente após a regra que qualificam?
- [ ] **Arquitetura de Parágrafos:** As ideias estão desenvolvidas em parágrafos coesos e bem delimitados, sem blocos ininterruptos excessivamente longos nem orações isoladas soltas?
- [ ] **Títulos Informativos:** Os títulos e seções são descritivos e situam claramente a matéria tratada?
- [ ] **Contiguidade em FAQs:** Em relações de perguntas e respostas, cada pergunta está conectada à sua respectiva resposta, sem listas iniciais isoladas?
- [ ] **Linearização de Tabelas:** Matrizes, quadros e tabelas foram convertidos em sentenças declarativas completas, sem arte ASCII ou tabulações?

### Governança e Regime Normativo
- [ ] **Autenticidade de Normas Oficiais:** Se a base contiver Instruções Normativas ou textos jurídicos formais, a redação original foi integralmente mantida sem resumos ou paráfrases não autorizadas?
- [ ] **Segregação de Interpretações:** Eventuais comentários e notas explicativas da equipe estão nitidamente separados e identificados como orientações práticas?

### Conformidade Técnica e Empacotamento
- [ ] **Formato do Arquivo:** Todos os arquivos possuem extensão `.txt` e codificação UTF-8?
- [ ] **Pontuação e Higienização:** As frases foram encerradas com ponto final e o texto está livre de *bullet points*, tabulações e linhas em branco consecutivas?
- [ ] **Estrutura do Pacote `.zip`:** Todos os arquivos `.txt` estão na raiz do pacote compactado, sem pastas internas?
- [ ] **Nomenclatura e Porte:** Nomes de arquivo contêm até 130 caracteres e o pacote total observa a referência de limite documentada?

### Validação Prática
- [ ] **Teste Amostral:** Foram realizadas consultas no assistente com perguntas representativas, avaliando se as respostas recuperam o contexto substantivo adequado e consideram as devidas exceções?
