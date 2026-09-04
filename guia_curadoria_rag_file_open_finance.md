# Guia de Curadoria de Arquivos RAG no Modo File
## Como agrupar conhecimento de negócio usando Open Finance do Banco do Brasil como exemplo

## 1. Objetivo deste guia

Este guia orienta áreas de negócio na preparação de arquivos de conhecimento para um agente RAG no GENERA, na modalidade **File**.

O objetivo não é ensinar a área a “separar um site por assuntos”. O objetivo é ensinar a identificar **unidades de conhecimento**: conjuntos de informações que precisam permanecer juntos para que o agente consiga responder corretamente a uma mesma situação de negócio.

O Open Finance do Banco do Brasil é usado aqui apenas como **modelo de aplicação**.

Este documento distingue duas coisas:

1. **Regras e princípios documentados nas fontes do GENERA.**
2. **Métodos práticos de curadoria derivados desses princípios.**

Essa distinção é importante. Nem toda técnica prática apresentada neste guia aparece literalmente na documentação. Algumas são formas de operacionalizar os critérios oficiais.

---

## 2. Fontes utilizadas

### 2.1 Fontes sobre estruturação do RAG no GENERA

Este guia foi baseado nos seguintes documentos fornecidos para o projeto:

- **GENERA: Como Criar uma Base no Modo File — Guia de Curadoria de Conteúdo para Bases de Conhecimento.**
- **GENERA: Vanilla vs. File — Como Decidir a Modalidade da sua Base de Conhecimento.**
- **GENERA — Criação e Gestão de RAG — Documentação Técnica Oficial.**

Essas fontes definem o comportamento da modalidade File, os critérios de unidade de conhecimento, os requisitos dos arquivos e os limites técnicos da indexação.

### 2.2 Fontes de negócio usadas nos exemplos de Open Finance

Os exemplos de negócio foram baseados em conteúdo oficial do Banco do Brasil:

- [Open Finance — Portal BB](https://www.bb.com.br/site/open-finance/)
- [Categoria Open Finance — Blog BB](https://blog.bb.com.br/categoria/open-finance/)
- [Open Finance é seguro? Entenda como funciona o consentimento](https://blog.bb.com.br/open-finance-e-seguro/)
- [Quais dados são compartilhados no Open Finance?](https://blog.bb.com.br/dados-compartilhados-open-finance/)
- [Open Finance: o que é e como ele melhora sua análise de crédito](https://blog.bb.com.br/open-finance-analise-de-credito/)
- [Como usar o Open Finance para portabilidade de crédito](https://blog.bb.com.br/como-usar-o-open-finance-para-portabilidade-de-credito/)

Os exemplos deste guia não devem ser tratados como uma substituição da fonte de negócio. Na preparação de uma base produtiva, cada unidade deve ser validada novamente contra a fonte oficial vigente.

---

# PARTE I — O QUE A DOCUMENTAÇÃO DO GENERA ESTABELECE

## 3. O que acontece com um arquivo na modalidade File

Na modalidade **File**, cada arquivo `.txt` é tratado como uma unidade completa de contexto.

Isso significa que o arquivo não é dividido internamente em pequenos trechos para recuperação. O documento inteiro representa uma unidade indexada.

Consequência prática:

> O conteúdo colocado dentro do mesmo arquivo precisa fazer sentido quando lido em conjunto.

Portanto, a principal decisão de curadoria não é “quantas páginas o arquivo terá”, mas:

> **Quais informações precisam permanecer juntas para representar corretamente uma mesma situação, regra ou unidade de resposta de negócio?**

---

## 4. O conceito central: unidade de conhecimento

Segundo o guia do modo File, uma unidade de conhecimento reúne as informações que precisam ser lidas juntas para que o assistente responda corretamente a uma situação específica.

Uma unidade pode conter:

- a resposta ou regra principal;
- o contexto indispensável;
- as condições de aplicação;
- as exceções que modificam a regra;
- diferentes perguntas que levam àquela mesma unidade de resposta.

O critério principal de agrupamento é, portanto, a **unidade de resposta**, e não a semelhança de palavras ou o tema amplo.

---

## 5. Quando informações devem ficar no mesmo arquivo

As fontes do GENERA indicam que informações tendem a permanecer juntas quando:

### 5.1 Representam a mesma regra ou unidade de resposta

Se várias perguntas são resolvidas pelo mesmo conjunto integrado de informações, elas podem fazer parte do mesmo arquivo.

### 5.2 O contexto é indispensável para interpretar a resposta

Se uma regra pode ficar errada ou ambígua sem determinado contexto, esse contexto deve acompanhar a regra.

### 5.3 As condições fazem parte da mesma resposta

Se uma orientação muda apenas conforme condições de aplicação, mas continua sendo a mesma regra de negócio, essas condições podem permanecer na mesma unidade.

### 5.4 Uma exceção limita ou modifica a regra

A exceção deve acompanhar a regra que ela restringe quando sua separação puder gerar uma resposta incorreta.

### 5.5 Perguntas diferentes levam à mesma unidade integrada

Perguntas não precisam ter exatamente a mesma formulação ou a mesma resposta textual. Elas podem ficar juntas quando pertencem à mesma situação e exigem o mesmo conjunto de informações.

---

## 6. Quando informações devem ser separadas

As fontes indicam separação quando:

### 6.1 A unidade de resposta muda substancialmente

Se a nova pergunta exige outra regra, outro processo ou outra orientação, há forte indicação de outra unidade.

### 6.2 A situação de negócio é diferente

Assuntos relacionados podem representar necessidades distintas do usuário.

### 6.3 O contexto necessário é diferente

Se uma informação faz sentido de forma independente e atende outra necessidade, ela pode merecer arquivo próprio.

### 6.4 As condições são incompatíveis

Quando reunir regras diferentes no mesmo arquivo aumenta o risco de confusão, a separação é recomendada.

### 6.5 O arquivo começa a responder coisas demais

Um bom teste documentado é verificar se o arquivo pode ser descrito em uma frase. Se isso for difícil, pode haver mais de uma unidade de conhecimento misturada.

---

## 7. Teste de autocontenção

Um arquivo File precisa funcionar sozinho.

A pergunta central é:

> **Se alguém ler apenas este arquivo, terá contexto suficiente para compreender e aplicar corretamente a resposta ou orientação?**

Se a resposta for não, o arquivo precisa ser revisto.

Pode faltar:

- uma condição;
- uma exceção;
- uma definição necessária;
- o contexto do público;
- uma parte inseparável do processo.

Importante: a documentação admite repetir contexto em mais de um arquivo quando essa repetição for necessária para manter cada unidade autocontida.

---

# PARTE II — MÉTODO PRÁTICO DERIVADO DOS PRINCÍPIOS

## 8. O que neste guia é método de trabalho, e não regra literal da documentação

Os itens abaixo são **técnicas de curadoria propostas para facilitar o trabalho do negocial**. Eles são coerentes com os princípios do GENERA, mas não aparecem necessariamente com esses nomes ou formatos na documentação oficial:

- pensar em “caixas de resposta”;
- aplicar um teste de três perguntas;
- construir uma matriz Pergunta → Resposta central → Regra/processo;
- usar a frase “tema macro não vira arquivo automaticamente”;
- criar uma ficha de rastreabilidade da fonte fora do `.txt`;
- definir previamente perguntas de homologação por unidade;
- tratar uma lista inicial de arquivos como hipótese de curadoria, e não como estrutura definitiva.

Esses instrumentos existem para transformar os critérios documentados em um processo mais fácil de executar.

---

## 9. Regra prática principal: não agrupe por tema; agrupe por resposta

Um erro comum seria perguntar:

> “Quais são os temas de Open Finance?”

Isso pode levar a títulos como:

- benefícios;
- segurança;
- crédito;
- funcionalidades;
- vantagens.

Esses rótulos são amplos demais para decidir sozinhos a estrutura de uma base File.

A pergunta mais útil é:

> **Quais dúvidas diferentes do cliente precisam do mesmo conjunto de informações para serem respondidas corretamente?**

Quando várias dúvidas têm a mesma regra central, elas são candidatas ao mesmo arquivo.

Quando exigem regras, processos, condições ou respostas substancialmente diferentes, são candidatas a arquivos diferentes.

---

## 10. A técnica das “caixas de resposta”

Para fins de curadoria, imagine que cada futuro arquivo é uma caixa.

Dentro da caixa entram apenas perguntas que podem ser resolvidas pela mesma resposta integrada.

Exemplo aplicado ao Open Finance:

### Caixa candidata: controle do consentimento

Perguntas:

- O que é consentimento?
- Quem controla os dados?
- Posso escolher a instituição?
- Posso escolher por quanto tempo?
- Meus dados vão para todos os bancos?
- Preciso compartilhar nos dois sentidos?
- Posso cancelar?

Essas perguntas são diferentes, mas as fontes do BB mostram que fazem parte de uma mesma lógica: **o cliente controla a autorização e o compartilhamento**.

Esse é um bom candidato a uma unidade.

---

## 11. Teste prático de três perguntas

Para decidir se dois conteúdos devem ficar juntos, o negocial pode usar:

### Pergunta 1
**Se eu explicar A, preciso explicar B para a resposta ficar correta ou completa?**

Se sim, há indicação de agrupamento.

### Pergunta 2
**A mesma regra ou lógica de negócio explica A e B?**

Se sim, há indicação de agrupamento.

### Pergunta 3
**B poderia existir como resposta independente, com outra regra, processo, condição ou objetivo?**

Se sim, há indicação de separação.

Este teste é uma operacionalização dos critérios de unidade, contexto, condição, exceção e mudança substancial de resposta presentes na documentação do GENERA.

---

# PARTE III — PROCESSO RECOMENDADO PARA O NEGOCIAL

## 12. Etapa 1 — Inventariar as perguntas reais

Antes de criar arquivos, reúna perguntas que o usuário realmente poderia fazer.

Exemplo:

- Posso cancelar o Open Finance?
- Posso escolher qual banco recebe os dados?
- Minha senha é compartilhada?
- Que dados da minha conta podem ser compartilhados?
- Open Finance aumenta meu limite?
- Open Finance reduz minha taxa de juros?
- Como trazer os dados de outro banco para o BB?
- Posso usar Open Finance para portabilidade?

Não agrupe ainda.

Primeiro, apenas registre as necessidades.

---

## 13. Etapa 2 — Escrever a resposta central de cada pergunta

Para cada pergunta, escreva em uma frase o núcleo da resposta oficial.

Exemplo:

| Pergunta | Resposta central |
|---|---|
| Posso cancelar o consentimento? | O cliente pode cancelar o consentimento. |
| Posso escolher a instituição? | O cliente escolhe as instituições envolvidas no compartilhamento. |
| Preciso compartilhar nos dois sentidos? | O compartilhamento não exige reciprocidade automática. |
| Minha senha é compartilhada? | Senhas e informações de autenticação não são compartilhadas. |
| Quais dados podem ser compartilhados? | Apenas dados autorizados, dentro das categorias previstas. |
| Open Finance aumenta meu limite? | O compartilhamento pode melhorar o contexto da análise, mas não garante aumento de limite. |

A resposta deve vir da fonte. Não deve ser inventada para completar a tabela.

---

## 14. Etapa 3 — Identificar a regra ou situação por trás da resposta

Agora adicione uma coluna:

| Pergunta | Resposta central | Regra ou situação |
|---|---|---|
| Posso cancelar? | Pode cancelar. | Controle do consentimento |
| Posso escolher a instituição? | O cliente escolhe. | Controle do consentimento |
| Preciso compartilhar nos dois sentidos? | Não há reciprocidade automática. | Controle do consentimento |
| Minha senha é compartilhada? | Não. | Escopo dos dados / segurança |
| Que dados podem ser compartilhados? | Apenas os autorizados e previstos. | Escopo dos dados |
| Open Finance aumenta meu limite? | Não há garantia. | Análise de crédito |

As linhas cuja regra ou situação é realmente a mesma são candidatas ao mesmo arquivo.

---

## 15. Etapa 4 — Acrescentar condições, exceções e contexto

Depois do agrupamento inicial, pergunte para cada unidade:

- Existe alguma condição que muda a aplicação da resposta?
- Existe alguma exceção?
- Existe algum limite que, se omitido, faria a resposta parecer mais ampla do que a fonte permite?
- Existe um contexto necessário para entender corretamente a regra?

Exemplo em análise de crédito:

A fonte do BB informa que o compartilhamento permite uma visão mais completa para análise, mas também afirma que **não existe garantia de aumento de limite nem de redução de taxa**.

A ressalva é inseparável da unidade de análise de crédito.

Se o arquivo disser apenas que “o Open Finance pode melhorar a análise”, sem trazer o limite da afirmação, ele pode induzir o agente a prometer um resultado que a própria fonte não promete.

---

## 16. Etapa 5 — Fazer o teste de autocontenção

Pergunte:

> Se o agente recuperar somente este arquivo, ele conseguirá responder corretamente às perguntas desta unidade?

Se a resposta depender de outro arquivo para descobrir uma condição essencial, há um problema.

É permitido repetir uma informação geral quando ela for necessária para deixar a unidade autocontida.

---

## 17. Etapa 6 — Fazer o teste de excesso

Pergunte:

> Existe alguma informação neste arquivo que poderia ser retirada sem prejudicar a resposta desta situação?

Se sim, ela pode ser:

- acessória;
- independente;
- pertencente a outra unidade.

Outro teste:

> Consigo descrever este arquivo em uma única frase?

Se não, reavalie o agrupamento.

---

## 18. Etapa 7 — Selecionar perguntas representativas

As perguntas dentro do arquivo não precisam listar todas as paráfrases possíveis.

Escolha formas realmente diferentes pelas quais o usuário pode chegar à mesma necessidade.

Exemplo:

- Posso cancelar o Open Finance?
- Quem controla meus dados?
- Preciso compartilhar nos dois sentidos?

Essas formulações adicionam variedade sem repetir artificialmente a mesma frase.

---

## 19. Etapa 8 — Redigir o arquivo como texto autocontido

O arquivo final deve conter apenas o conhecimento necessário à unidade.

Os rótulos de curadoria, como:

- `[PERGUNTAS REPRESENTATIVAS]`;
- `[CONDIÇÕES]`;
- `[EXCEÇÕES]`;

são úteis durante a preparação, mas não precisam aparecer no arquivo final.

A documentação de curadoria do GENERA orienta que esses rótulos sejam removidos do `.txt` final.

---

# PARTE IV — OPEN FINANCE COMO EXEMPLO DE AGRUPAMENTO

## 20. Exemplo 1 — Conteúdos que fazem sentido juntos

Fonte principal do exemplo:

**“Open Finance é seguro? Entenda como funciona o consentimento” — Blog BB.**

A fonte informa, entre outros pontos, que:

- o cliente controla seus dados;
- o consentimento é explícito;
- o cliente escolhe as instituições;
- o consentimento não libera dados para todo o ecossistema;
- o compartilhamento não exige reciprocidade automática;
- o consentimento pode ser cancelado.

Esses elementos são fortemente relacionados.

### Unidade candidata

**Consentimento, controle e cancelamento no Open Finance.**

### Perguntas representativas

- O que é consentimento?
- Quem controla meus dados?
- Posso escolher a instituição?
- Meus dados vão para todos os bancos?
- Preciso compartilhar nos dois sentidos?
- Posso cancelar?

### Por que agrupar?

Porque todas as perguntas são respondidas por uma mesma lógica integrada de negócio: **o controle do cliente sobre a autorização do compartilhamento**.

---

## 21. Exemplo 2 — Quando um assunto parecido pode merecer outra unidade

Fonte principal:

**“Quais dados são compartilhados no Open Finance?” — Blog BB.**

A fonte organiza os dados compartilháveis em categorias, como:

- dados cadastrais;
- contas e transações;
- cartões;
- crédito;
- investimentos;
- câmbio e outros serviços previstos.

Também delimita informações que não fazem parte do compartilhamento, como senhas e informações de autenticação.

### Unidade candidata

**Dados que podem e que não podem ser compartilhados no Open Finance.**

### Por que pode ser separada do consentimento?

“Posso cancelar?” e “Quais dados da minha conta podem ser compartilhados?” pertencem ao mesmo domínio geral, mas exigem respostas centrais diferentes.

Uma pergunta trata do **controle da autorização**.

A outra trata do **escopo das informações compartilháveis**.

Isso é uma aplicação do critério de mudança de unidade de resposta.

### Observação importante

A decisão final de separar “dados compartilhados” e “segurança” não deve ser tomada apenas pelos títulos.

Se o conteúdo sobre segurança for inseparável das regras sobre o que é ou não compartilhado, uma unidade conjunta pode ser melhor.

Se houver conteúdo de segurança amplo e independente, uma unidade separada pode fazer mais sentido.

O critério é a resposta de negócio, não o rótulo.

---

## 22. Exemplo 3 — Análise de crédito

Fonte principal:

**“Open Finance: o que é e como ele melhora sua análise de crédito” — Blog BB.**

A fonte explica que um histórico financeiro mais completo pode dar mais contexto à avaliação de crédito.

Também traz uma limitação fundamental:

> O compartilhamento não garante aumento de limite nem redução de taxas.

### Unidade candidata

**Uso do Open Finance na análise de crédito.**

### Perguntas que podem pertencer à mesma unidade

- Open Finance melhora minha análise de crédito?
- Open Finance aumenta meu limite?
- Open Finance reduz meus juros?
- Compartilhar meus dados garante uma condição melhor?
- Por que dados de outros bancos ajudam na análise?

### Por que agrupar?

As perguntas fazem parte da mesma situação: **qual é o papel dos dados compartilhados na avaliação de crédito e quais resultados podem ou não ser prometidos**.

A condição de “não garantia” precisa permanecer junto da explicação do benefício potencial.

---

## 23. Exemplo 4 — Portabilidade de crédito

Fonte principal:

**“Como usar o Open Finance para portabilidade de crédito” — Blog BB, publicado em 18 de março de 2026.**

A fonte trata de uma jornada específica:

- compartilhamento dos dados do contrato;
- análise pela nova instituição;
- comparação de condições;
- processo no aplicativo;
- ausência de garantia de proposta melhor;
- informações de escopo e prazo apresentadas no artigo.

### Unidade candidata

**Portabilidade de crédito usando Open Finance.**

### Por que não juntar automaticamente com análise de crédito?

Embora a portabilidade envolva análise de crédito, ela possui uma situação própria, uma jornada própria e condições específicas.

Uma pessoa pode perguntar “Open Finance aumenta meu limite?” sem querer realizar portabilidade.

Outra pode perguntar “Como portar meu crédito?” e precisar de informações de processo que não são necessárias na primeira situação.

Isso indica unidades diferentes.

---

# PARTE V — UM EXEMPLO DE ERRO DE AGRUPAMENTO

## 24. Arquivo amplo demais

Um arquivo chamado:

`beneficios_open_finance.txt`

poderia reunir:

- aumento de limite;
- portabilidade;
- visualização financeira;
- pagamentos;
- ofertas.

O problema é que “benefícios” é um tema editorial amplo, não necessariamente uma unidade de resposta.

Uma pergunta sobre limite poderia recuperar junto regras de portabilidade e outros conteúdos que não são necessários.

Na modalidade File, como o arquivo inteiro é uma unidade, essa mistura reduz a precisão conceitual da base.

---

# PARTE VI — MATRIZ DE AGRUPAMENTO PARA O NEGOCIAL

## 25. Modelo recomendado

Antes de produzir os `.txt`, o negocial pode preencher:

| ID | Pergunta do usuário | Resposta oficial resumida | Regra/situação | Condição | Exceção/limite | Fonte | Unidade candidata | Decisão |
|---|---|---|---|---|---|---|---|---|
| 01 | Posso cancelar? | Pode cancelar o consentimento. | Controle do consentimento | Conforme consentimento vigente | — | Blog BB | Consentimento | Juntar |
| 02 | Posso escolher o banco? | O cliente escolhe as instituições. | Controle do consentimento | Autorização específica | Não libera todo o ecossistema | Blog BB | Consentimento | Juntar |
| 03 | Preciso compartilhar nos dois sentidos? | Não há reciprocidade automática. | Controle do consentimento | — | — | Blog BB | Consentimento | Juntar |
| 04 | Minha senha é compartilhada? | Senhas não são compartilhadas. | Escopo dos dados / segurança | — | Dados de autenticação também não | Blog BB | Dados/segurança | Avaliar |
| 05 | Open Finance aumenta meu limite? | Não existe garantia. | Análise de crédito | Depende da análise | Não prometer resultado | Blog BB | Crédito | Separar de consentimento |

A matriz não é um requisito técnico do GENERA. Ela é um instrumento de curadoria recomendado neste guia.

---

# PARTE VII — FICHA DE CURADORIA DE CADA ARQUIVO

## 26. O que o negocial deve entregar

### Situação de negócio

**Pergunta:** qual situação específica este arquivo precisa resolver?

Exemplo:

> Controle do cliente sobre o consentimento no Open Finance.

### Perguntas representativas

**Pergunta:** como usuários diferentes poderiam buscar essa mesma situação?

Inclua apenas formulações realmente diferentes.

### Resposta oficial

**Pergunta:** qual é a resposta correta segundo a fonte?

Não utilizar conhecimento não documentado para completar lacunas.

### Condições

**Pergunta:** em quais circunstâncias essa orientação vale?

### Exceções e limites

**Pergunta:** quando a resposta muda, não se aplica ou precisa de ressalva?

### Contexto indispensável

**Pergunta:** o que precisa acompanhar a resposta para evitar interpretação errada?

### Fonte de origem

**Pergunta:** qual conteúdo oficial sustenta a informação?

Este campo de rastreabilidade é recomendado como governança do projeto. Ele não é apresentado na documentação consultada como um campo obrigatório dentro do arquivo File.

---

# PARTE VIII — EXEMPLO DE ARQUIVO FINAL

## 27. Consentimento, controle e cancelamento

Exemplo de `.txt` final:

```text
Consentimento, controle e cancelamento no Open Finance.

O que é consentimento no Open Finance?
Quem controla meus dados no Open Finance?
Posso escolher com quais instituições compartilhar meus dados?
Posso definir por quanto tempo meus dados serão compartilhados?
Meus dados são liberados para todos os bancos quando dou consentimento?
O compartilhamento precisa acontecer nos dois sentidos?
Posso cancelar o consentimento depois de ativar o Open Finance?

No Open Finance, os dados são do cliente. O cliente decide se quer compartilhar seus dados, com quais instituições e por quanto tempo.

O consentimento é a autorização explícita dada pelo cliente para que seus dados financeiros sejam compartilhados entre instituições participantes do Open Finance. A autorização exige confirmação do cliente e informa quais dados serão compartilhados. Sem consentimento, nenhum dado é acessado ou transferido.

Dar consentimento não libera os dados para todas as instituições participantes do Open Finance. O compartilhamento acontece exclusivamente entre as instituições escolhidas pelo cliente no momento da autorização. O cliente indica a instituição que envia os dados e a instituição que os recebe.

O compartilhamento não exige reciprocidade automática. O cliente pode autorizar o envio de dados de uma instituição para outra sem necessariamente autorizar o caminho inverso.

O cliente pode cancelar o consentimento a qualquer momento.
```

Observação de curadoria: qualquer detalhe operacional adicional, como canal específico de cancelamento, deve ser incluído apenas quando estiver claramente sustentado pela fonte adotada para a base vigente.

---

# PARTE IX — REQUISITOS TÉCNICOS DO ARQUIVO

## 28. Formato

Para modalidade File, a documentação consultada estabelece:

- arquivo `.txt`;
- codificação UTF-8;
- texto simples;
- frases encerradas com ponto final sempre que possível;
- evitar marcadores de lista no arquivo final;
- evitar linhas em branco consecutivas;
- não usar tabulações;
- pacote `.zip` com estrutura plana.

A documentação técnica informa que, na modalidade File, cada `.txt` é indexado integralmente e registra limite de até **8.000 tokens por arquivo** para o modelo indicado no documento.

A extensão não deve ser usada como principal critério de divisão.

Um arquivo pequeno ainda pode estar mal construído se misturar unidades diferentes.

Um arquivo maior pode continuar coerente se todas as informações forem inseparáveis, respeitados os limites técnicos.

---

# PARTE X — O QUE NÃO FAZER

## 29. Não separar simplesmente pelos títulos do site

A estrutura editorial de uma página não é automaticamente a estrutura ideal do RAG.

Um artigo pode conter várias situações diferentes.

Vários artigos também podem repetir informações necessárias a uma mesma unidade.

---

## 30. Não criar um arquivo para cada pergunta

Perguntas diferentes podem pertencer à mesma unidade integrada.

Criar um arquivo por pergunta pode fragmentar regras, condições e exceções que precisam ser consideradas juntas.

---

## 31. Não criar um arquivo por palavra-chave

“Crédito”, “segurança”, “dados” e “benefícios” são rótulos.

Antes de usá-los como arquivo, identifique qual situação e qual resposta estão representando.

---

## 32. Não separar uma exceção da regra que ela limita

Se a fonte diz que algo “pode acontecer, mas não é garantido”, os dois elementos precisam permanecer juntos.

No exemplo de crédito, o benefício potencial e a ausência de garantia formam uma única unidade de interpretação.

---

## 33. Não completar a fonte

Se a fonte não informa:

- valor;
- taxa;
- prazo;
- público;
- condição;
- canal;
- exceção;

não invente a informação para tornar o arquivo aparentemente completo.

“Autocontido” não significa “completar tudo”.

Significa reunir tudo o que **a fonte sustenta e que é necessário para compreender corretamente aquela unidade**.

---

# PARTE XI — CHECKLIST FINAL DO NEGOCIAL

## 34. Antes de aprovar um arquivo

Verifique:

- [ ] Consigo dizer em uma frase qual situação este arquivo resolve?
- [ ] Todas as perguntas representam a mesma unidade de resposta?
- [ ] A regra principal está claramente sustentada pela fonte?
- [ ] As condições necessárias estão no mesmo arquivo?
- [ ] As exceções que limitam a regra estão no mesmo arquivo?
- [ ] O contexto indispensável está presente?
- [ ] Há conteúdo independente que deveria estar em outro arquivo?
- [ ] O arquivo funciona sozinho?
- [ ] Alguma frase amplia ou promete mais do que a fonte afirma?
- [ ] Perguntas representativas foram escolhidas sem excesso de paráfrases?
- [ ] A fonte de cada informação foi registrada na curadoria?
- [ ] O arquivo final respeita os requisitos técnicos do modo File?

---

# PARTE XII — FLUXO RESUMIDO

## 35. Processo em uma visão

```text
FONTES OFICIAIS
      |
      v
PERGUNTAS REAIS DOS USUÁRIOS
      |
      v
RESPOSTA CENTRAL DE CADA PERGUNTA
      |
      v
IDENTIFICAR REGRA / SITUAÇÃO
      |
      v
AGRUPAR AS QUE EXIGEM A MESMA RESPOSTA INTEGRADA
      |
      v
ADICIONAR CONTEXTO + CONDIÇÕES + EXCEÇÕES
      |
      v
TESTE DE AUTOCONTENÇÃO
      |
      +------ falhou ------> revisar agrupamento
      |
      v
TESTE DE EXCESSO
      |
      +------ falhou ------> separar conteúdo independente
      |
      v
SELECIONAR PERGUNTAS REPRESENTATIVAS
      |
      v
REDIGIR .TXT
      |
      v
VALIDAR FONTE E FORMATAÇÃO
      |
      v
INDEXAR
```

---

# PARTE XIII — PRINCÍPIO FINAL

## 36. Regra que deve orientar toda a curadoria

> **Não pergunte primeiro “qual é o tema deste conteúdo?”. Pergunte “qual situação o agente precisa responder e quais informações precisam ser lidas juntas para que essa resposta esteja correta?”.**

Esse princípio sintetiza a lógica de unidade de conhecimento da modalidade File.

No exemplo de Open Finance:

- “Posso cancelar?” e “preciso compartilhar nos dois sentidos?” podem pertencer à mesma unidade de controle do consentimento.
- “Minha senha é compartilhada?” pode levar à unidade de escopo dos dados ou segurança, conforme a curadoria do conteúdo.
- “Open Finance aumenta meu limite?” leva à unidade de análise de crédito.
- “Como portar meu crédito?” leva a uma jornada específica de portabilidade.

Todos pertencem ao macrotema Open Finance.

Mas **macrotema não é sinônimo de unidade de conhecimento**.

---

## 37. Governança recomendada

Para cada arquivo publicado, recomenda-se manter fora do corpus RAG uma ficha com:

- nome do arquivo;
- unidade de conhecimento;
- fonte oficial;
- URL ou identificação do documento;
- data de consulta/revisão;
- responsável negocial;
- perguntas cobertas;
- data da última validação;
- observações sobre temporalidade.

Essa ficha é uma recomendação de governança deste projeto. Não é apresentada nas fontes consultadas como requisito técnico obrigatório da modalidade File.

Ela ajuda a saber **por que o arquivo existe, de onde veio e quando precisa ser revisado**.
