# GENERA: Vanilla vs. File — Como Decidir a Modalidade da sua Base de Conhecimento
### Guia Consultivo de Apoio à Decisão Negocial

---

## 1. Introdução — O Papel da Modalidade no Uso da Base de Conhecimento

Ao estruturar uma base de conhecimento para um assistente virtual no GENERA, uma das decisões mais importantes é definir como o sistema consultará os documentos disponibilizados. Essa escolha determina a estratégia de leitura adotada pelo assistente no momento de responder às dúvidas dos usuários.

No GENERA, as duas modalidades fundamentais para bases textuais são **Vanilla** e **File**:

* Na modalidade **Vanilla**, o assistente examina os materiais localizando passagens e trechos específicos distribuídos ao longo dos textos;
* Na modalidade **File**, o assistente considera cada documento em sua totalidade, tratando o arquivo como uma unidade de contexto indivisível.

A escolha entre essas modalidades não depende de preferências visuais ou de interface, mas sim da **natureza dos seus documentos** e da **forma como as regras precisam ser interpretadas**. Definir a modalidade adequada alinha a consulta à estrutura real do material, favorecendo respostas coerentes com o conteúdo corporativo e reduzindo o risco de omissões ou leituras descontextualizadas.

---

## 2. Ponto de Partida — Condições de Elegibilidade do Material

Antes de analisar as diferenças funcionais entre Vanilla e File, a equipe responsável pela base deve verificar duas condições preliminares:

### Formato do Conteúdo
Tanto a modalidade **Vanilla** quanto a modalidade **File** operam exclusivamente sobre conteúdos disponibilizados em **texto simples** (arquivos com extensão `.txt`).
* Se o seu acervo já estiver em texto simples ou puder ser convertido para esse formato mantendo sua clareza, ele está apto para avaliação entre Vanilla e File;
* Se a equipe dispuser de materiais em outros formatos documentais (como apresentações, planilhas, mensagens de correio ou documentos formatados) que não possam ser convertidos em texto simples, deve consultar as orientações específicas voltadas a acervos com formatos diversificados.

### Integração Direta de Instruções Normativas (IN)
A modalidade **Vanilla** possui uma facilidade própria para órgãos e setores que utilizam normas corporativas oficiais: ela permite a integração direta a partir da informação do **número da norma**, realizando o aproveitamento automático do acervo normativo correspondente. A modalidade File não conta com essa funcionalidade de busca automática por numeração.

---

## 3. Modalidade Vanilla — Consulta a Trechos Específicos em Textos Mais Amplos

### Como Funciona
Na modalidade **Vanilla**, o conteúdo dos arquivos é organizado para que o assistente consulte e recupere partes pontuais do texto. Quando uma pessoa faz uma pergunta ao assistente, ele localiza os trechos mais pertinentes espalhados pelo documento e utiliza essas passagens específicas para compor a resposta, sem a necessidade de examinar o arquivo inteiro a cada interação.

### Quando Escolher
A modalidade Vanilla é a escolha indicada quando:
* O acervo é composto por **documentos extensos, manuais volumosos, procedimentos detalhados ou regulamentos amplos**;
* O material é estruturado em **capítulos, artigos, seções ou tópicos com sentido autônomo**;
* As dúvidas dos usuários buscam respostas pontuais (como prazos, valores, condições específicas ou procedimentos passo a passo) que se encontram em pontos bem delimitados do texto;
* O conteúdo baseia-se em **Instruções Normativas oficiais** que podem ser integradas diretamente pela sua numeração.

### Benefício para o Negócio
Permite que o assistente recupere trechos específicos e pontuais do acervo, extraindo a informação necessária de onde quer que ela esteja no documento, sem sobrecarregar a consulta com partes do texto que não guardam relação com a dúvida apresentada.

---

## 4. Modalidade File — Consideração Integral de Documentos Coesos

### Como Funciona
Na modalidade **File**, cada arquivo de texto é tratado como um bloco completo, indivisível e único de conhecimento. Quando o assistente identifica que o assunto de uma consulta está relacionado àquele documento, a integralidade do arquivo é considerada para a formulação da resposta. Não ocorre fragmentação nem busca por trechos isolados dentro do arquivo.

### Quando Escolher
A modalidade File é a escolha indicada quando:
* O documento é **naturalmente breve, conciso e condensado**;
* As informações contidas no arquivo são **fortemente interdependentes**, de modo que uma cláusula, requisito ou orientação só pode ser corretamente compreendida à luz das premissas gerais, do público-alvo e das exceções descritas no próprio texto;
* A fragmentação do texto em partes menores geraria risco de interpretação equivocada ou resposta incompleta;
* Trata-se de materiais como **políticas condensadas, termos de referência compactos, comunicados circunscritos ou páginas únicas de orientações**.

### Contexto de Porte
A modalidade File é indicada para documentos curtos que devem ser tratados como uma única unidade indivisível de contexto (ex.: políticas condensadas, termos de referência, FAQs de página única); para documentos mais longos ou compostos por tópicos independentes, a indicação da plataforma é o uso da modalidade Vanilla.

---

## 5. Quadro Comparativo — Vanilla vs. File sob a Ótica de Negócio

| Critério Negocial | Modalidade Vanilla | Modalidade File |
| :--- | :--- | :--- |
| **Unidade de Consulta** | Passagens e trechos específicos do texto. | O documento considerado em sua totalidade. |
| **Porte Típico do Material** | De médio a extenso (manuais, regulamentos, compêndios). | Curto e condensado (termos compactos, comunicados breves). |
| **Estrutura Interna** | Tópicos, seções ou itens com relativo grau de autonomia. | Texto contínuo, coeso e com regras mutuamente dependentes. |
| **Tipo de Busca do Usuário** | Consultas pontuais por regras, prazos, definições e passos específicos. | Consultas que demandam visão de conjunto e consideração de todas as cláusulas do documento. |
| **Instruções Normativas por Número** | Suporte direto à importação a partir do número da norma. | Não disponível (demanda arquivos próprios). |
| **Foco de Mitigação de Risco** | Mitiga o risco de sobrecarregar a consulta com partes irrelevantes de documentos longos. | Mitiga o risco de leituras parciais de regras que dependem de premissas gerais e exceções. |

---

## 6. Roteiro Prático de Decisão — Da Triagem à Escolha da Modalidade

Para orientar a escolha da modalidade mais apropriada para a sua base de conhecimento, considere a sequência de perguntas abaixo:

```
[Etapa 1: Formato]
O material está em texto simples (.txt) ou pode ser convertido?
  ├─ Não ──► Consultar opções voltadas a formatos diversificados.
  └─ Sim ──► Avançar para a Etapa 2.
               │
[Etapa 2: Origem Normativa]
O acervo consiste em Instruções Normativas oficiais com número próprio?
  ├─ Sim ──► Modalidade indicada: VANILLA (integração direta por número).
  └─ Não ──► Avançar para a Etapa 3.
               │
[Etapa 3: Relação entre as Informações]
As regras exigem leitura do conjunto ou funcionam por tópicos autônomos?
  ├─ Tópicos autônomos que fazem sentido isolados ──► Avançar para Etapa 4A.
  └─ Regras interdependentes que exigem visão do todo ──► Avançar para Etapa 4B.
               │
[Etapa 4A: Porte para Conteúdo Autônomo]
O material é de médio ou grande porte?
  ├─ Sim ──► Modalidade indicada: VANILLA.
  └─ Não (é curto com tópicos autônomos) ──► VANILLA (para consulta pontual) ou avaliar desmembramento (Seção 7).
               │
[Etapa 4B: Porte para Conteúdo Interdependente]
O material é naturalmente curto e conciso?
  ├─ Sim ──► Modalidade indicada: FILE.
  └─ Não (é longo e interdependente) ──► Consultar Seção 7 (Casos Mistos).
```

### Síntese do Roteiro
1. **Material conciso + leitura do conjunto indispensável** → **File**;
2. **Material extenso ou modular + busca por trechos específicos** → **Vanilla**;
3. **Instruções Normativas oficiais catalogadas** → **Vanilla**;
4. **Situações de conflito entre tamanho e interdependência** → Avaliar conforme a Seção 7.

---

## 7. Casos Mistos e Zonas Cinzentas — Como Analisar Situações Conflitantes

Na prática do dia a dia corporativo, nem todo acervo se encaixa de imediato em uma categoria pura. Abaixo estão as orientações para os dilemas mais frequentes:

### Dilema 1: O documento é extenso, mas suas regras são interdependentes
* **A situação**: Trata-se de um regulamento ou manual longo no qual conceitos dispostos na introdução regem artigos distribuídos por todo o texto. A modalidade File não é a indicada para documentos dessa extensão, mas a consulta por trechos em Vanilla pode recuperar uma regra sem capturar suas premissas gerais.
* **Orientação de negócio**: Recomenda-se uma intervenção de curadoria textual antes da carga:
  * *Opção A (Desmembramento em arquivos autocontidos)*: Dividir o compêndio em documentos menores e independentes por assunto (por exemplo, transformando capítulos em documentos próprios breves, cada qual contendo seu público e suas premissas), viabilizando o uso da modalidade **File**;
  * *Opção B (Reestruturação de tópicos)*: Manter o documento unificado na modalidade **Vanilla**, mas revisar a redação dos tópicos para que cada seção faça menção expressa às suas condicionantes e exceções, favorecendo que o trecho recuperado tenha sentido completo por si só.

### Dilema 2: Tratamento de Perguntas Frequentes (FAQs)
* **A situação**: Dúvidas sobre se uma relação de perguntas e respostas deve ser tratada como documento integral ou dividida em trechos.
* **Orientação de negócio**: A decisão deve pautar-se na coesão temática e na concisão do acervo:
  * *FAQ breve de tema circunscrito*: Se o material contiver um grupo reduzido de perguntas e respostas sobre um único assunto coeso (por exemplo, "Dúvidas Frequentes sobre Abertura de Conta Universitária"), ele pode ser mantido como documento único na modalidade **File**;
  * *Compêndio amplo de dúvidas gerais*: Se o acervo reunir um número expressivo de perguntas sobre temas variados, procedimentos distintos ou múltiplos produtos, a modalidade indicada é **Vanilla**, pois permite localizar o trecho correspondente à dúvida da pessoa usuária sem carregar perguntas não correlacionadas.

### Dilema 3: Documento curto com múltiplos assuntos não relacionados
* **A situação**: Um arquivo tem extensão reduzida, mas reúne orientações sobre processos operacionais totalmente distintos.
* **Orientação de negócio**: A leitura integral de assuntos misturados em um mesmo arquivo na modalidade File pode dispersar o contexto da resposta. Recomenda-se desmembrar o conteúdo em arquivos separados por tema ou utilizar a modalidade **Vanilla** para que o assistente localize apenas a passagem pertinente à consulta.

---

## 8. Cenários Práticos de Negócio

Para facilitar a identificação com a realidade das áreas funcionais, veja a aplicação dos critérios em casos práticos:

### Casos de Aplicação da Modalidade Vanilla

* **Manual de Políticas de Gestão de Pessoas (RH)**:
  * *Contexto*: Documento volumoso cobrindo tópicos distintos como férias, licenças, auxílios, jornada de trabalho e previdência complementar;
  * *Comportamento esperado*: A pessoa colaboradora pergunta especificamente sobre o prazo para requerer licença-maternidade; o assistente localiza e utiliza a passagem correspondente à licença, sem demandar o exame das demais políticas de pessoal.
* **Catálogo de Linhas de Crédito e Financiamento**:
  * *Contexto*: Documento amplo contendo especificações de diversas linhas de crédito, taxas, públicos-alvo e fluxos de contratação;
  * *Comportamento esperado*: O assistente recupera pontualmente as condições da linha de crédito consultada, mantendo a resposta centrada no produto questionado.
* **Acervo de Instruções Normativas Operacionais**:
  * *Contexto*: Normas corporativas numeradas e oficiais sobre rotinas de agências e controles internos;
  * *Comportamento esperado*: Carga direta a partir do número oficial da norma, com consulta aos artigos pertinentes à dúvida operacional.

### Casos de Aplicação da Modalidade File

* **Termo de Adesão e Condições Gerais de Produto**:
  * *Contexto*: Documento conciso que reúne direitos, deveres, encargos e hipóteses de cancelamento de um serviço;
  * *Comportamento esperado*: O assistente analisa o conjunto do termo para responder sobre uma eventual rescisão, considerando tanto as obrigações do cliente quanto as penalidades aplicáveis, sem isolar cláusulas de forma inadequada.
* **Roteiro Operacional de Contingência de Atendimento**:
  * *Contexto*: Procedimento breve descrevendo a sequência ordenada de passos a serem adotados durante a indisponibilidade temporária de um canal de atendimento;
  * *Comportamento esperado*: O fluxo precisa ser considerado do início ao fim para que a orientação fornecida reflita a totalidade do plano de contingência.
* **Comunicado de Regras de Campanha Promocional**:
  * *Contexto*: Documento conciso com período de vigência, público elegível, metas de pontuação e critérios de bonificação;
  * *Comportamento esperado*: O assistente examina o documento integralmente para confirmar se um determinado cliente tem direito ao benefício, avaliando vigência e requisitos simultaneamente.

---

## 9. Próximos Passos — Encaminhamento Pós-Decisão

Uma vez percorrido este guia e definida a modalidade mais compatível com o seu acervo:

* Se a escolha for a modalidade **File**, consulte o guia de preparação dedicado ao modo File para orientações práticas de estruturação dos seus arquivos de texto simples;
* Se a escolha for a modalidade **Vanilla**, consulte o guia de preparação dedicado ao modo Vanilla para orientações práticas sobre organização de seções, tópicos e acervos normativos.

Seguindo essa rota de decisão, sua base de conhecimento estará estruturada de forma harmônica com o comportamento de consulta do assistente, favorecendo interações coerentes, relevantes e alinhadas aos objetivos da sua área de negócio.
