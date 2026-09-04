# GENERA: Como Criar uma Base no Modo File
### Guia de Curadoria de Conteúdo para Bases de Conhecimento

---

## 1. Introdução — O Princípio da Unidade de Conhecimento

Ao estruturar uma base de conhecimento no modo File do GENERA, a principal decisão não é de natureza técnica — é de curadoria.

Antes de escrever qualquer arquivo, a área responsável pelo conteúdo precisa responder uma pergunta fundamental:

> **"Quais informações precisam permanecer juntas para que este arquivo represente corretamente uma mesma situação, regra ou unidade de resposta de negócio?"**

No modo File, cada arquivo `.txt` que você preparar será tratado como uma unidade completa e indivisível. O assistente não divide o arquivo em partes menores para consultar — ele considera o conteúdo do arquivo como um conjunto. Por isso, o que estiver dentro de cada arquivo importa tanto quanto o que está fora: arquivos bem delimitados tendem a favorecer respostas mais coerentes; arquivos que reúnem conteúdos demais ou de menos podem comprometer a qualidade da consulta.

O princípio central deste guia é:

> **Cada arquivo deve representar uma unidade de conhecimento coerente e autocontida.**

"Coerente" significa que todo o conteúdo do arquivo pertence à mesma situação, regra ou resposta de negócio.

"Autocontida" significa que o arquivo faz sentido por si só — sem depender do conteúdo de outro arquivo para ser corretamente compreendido.

Este guia ensina como encontrar as fronteiras dessa unidade.

---

## 2. O que Define uma Unidade de Conhecimento

Uma unidade de conhecimento é o conjunto de informações que precisam ser lidas juntas para que o assistente responda corretamente a uma situação específica.

Para identificar o que pertence à mesma unidade, considere cinco elementos:

**A unidade de resposta ou regra sendo representada**
É o núcleo da unidade. Convém que todo o conteúdo do arquivo contribua para uma mesma unidade de resposta ou regra de negócio. Se o arquivo começa a responder a uma situação substancialmente diferente, provavelmente chegou a outra unidade.

**O contexto necessário para compreendê-la**
Algumas respostas só fazem sentido dentro de um determinado contexto. Quando esse contexto é indispensável para interpretar corretamente a resposta, convém incluí-lo na mesma unidade — mesmo que esse contexto seja compartilhado com outros arquivos.

**As condições de aplicação**
Muitas regras se aplicam apenas em determinadas circunstâncias. Quando as condições são parte integrante da resposta — ou seja, sem elas a resposta estaria incompleta ou incorreta —, convém mantê-las no mesmo arquivo.

**As exceções**
Quando uma exceção modifica ou limita a regra representada no arquivo, convém mantê-la na mesma unidade. Separar a exceção da regra que ela restringe pode gerar uma resposta incompleta em situações nas quais a exceção deveria prevalecer.

**As diferentes perguntas que levam àquela mesma unidade**
Um mesmo conjunto de informações pode ser buscado de formas diferentes. Variações de formulação que se dirigem à mesma unidade de resposta são parte da mesma unidade de conhecimento.

### O teste da autocontenção

Antes de finalizar um arquivo, faça este teste: **se alguém ler apenas este arquivo, terá contexto suficiente para compreender e aplicar corretamente a resposta ou orientação que ele contém?**

Se a resposta for sim, é um bom sinal de que o arquivo está autocontido; verifique também se todo o conteúdo pertence à mesma unidade de conhecimento.

Se a resposta for não — porque falta contexto que está em outro arquivo, ou porque a resposta depende de uma condição que está em outro lugar —, convém revisar o que está incluído e o que está faltando.

---

## 3. Quando Juntar — Critérios para o Mesmo Arquivo

Os indicadores abaixo sugerem que informações pertencem ao mesmo arquivo:

### Mesma unidade de resposta ou regra

Quando o conteúdo compõe uma mesma unidade de resposta ou representa uma única regra de negócio, convém mantê-lo no mesmo arquivo — independentemente de quantas formas diferentes alguém pode chegar a essa informação.

*Exemplo:* diferentes perguntas sobre o prazo de um mesmo benefício, quando o prazo é único e o processo é o mesmo, tendem a pertencer ao mesmo arquivo.

### Contexto compartilhado

Quando uma informação só faz sentido se acompanhada de outra — porque define o cenário em que a regra se aplica —, convém mantê-las juntas. Isso vale mesmo quando esse contexto também aparece em outros arquivos: a necessidade de compreensão local prevalece sobre a duplicidade.

*Exemplo:* uma regra sobre aprovação de despesas que só se aplica a despesas acima de determinado valor. O valor e a regra compõem a mesma unidade.

### Condições vinculadas à mesma unidade de resposta

Quando diferentes condições levam a variações de uma mesma unidade de resposta — e não a orientações completamente diferentes —, todas as condições e suas variações podem permanecer no mesmo arquivo.

*Exemplo:* uma regra de reembolso com prazo diferente para solicitações internas e externas representa variações da mesma regra. Se a natureza do processo for a mesma e apenas os prazos diferirem, o conteúdo tende a pertencer ao mesmo arquivo.

### Exceções que modificam a regra do arquivo

Quando a exceção não cria uma nova regra, mas delimita ou modifica a regra representada no arquivo, convém mantê-la ali. Separar a exceção da regra que ela restringe pode levar o assistente a fornecer uma resposta aplicável em um contexto em que a exceção deveria prevalecer.

### Diferentes perguntas que levam à mesma unidade

Quando perguntas com formulações distintas se dirigem à mesma unidade de resposta, todas podem estar no mesmo arquivo. O que as une não é a semelhança de vocabulário, mas o fato de serem atendidas por aquele mesmo conjunto integrado de informações.

*Exemplo:* "Como solicito reembolso de despesas médicas?", "Qual é o processo para pedir reembolso de saúde?" e "Minha conta médica pode ser reembolsada pelo plano?" — como pertencem à mesma unidade de resposta integrada, as três perguntas representam a mesma unidade de conhecimento.

---

## 4. Quando Separar — Critérios para Arquivos Distintos

Os sinais abaixo indicam que o conteúdo provavelmente precisa de um arquivo próprio:

### A unidade de resposta muda substancialmente

Quando a resposta ou regra aplicável a uma situação é significativamente diferente daquela aplicável a outra, trata-se de unidades distintas — mesmo que os assuntos pareçam relacionados superficialmente.

*Exemplo:* regras de reembolso de despesas médicas e regras de reembolso de despesas de viagem podem parecer próximas, mas se os processos, os prazos, os aprovadores e as condições forem diferentes, cada uma tende a representar uma unidade independente.

### O contexto é diferente

Quando o conteúdo faz sentido por si só — sem depender do restante do arquivo para ser compreendido —, ele provavelmente representa outra unidade.

### A situação de negócio é distinta

Quando o usuário que pergunta sobre uma situação não teria razão para querer saber a outra no mesmo momento, as situações são distintas. Uma forma útil de testar isso: se a pergunta de um usuário levaria ao arquivo mas outra pergunta, de outro usuário com necessidade diferente, não levaria — podem ser unidades diferentes.

### As condições de aplicação são incompatíveis

Quando as condições são tão diferentes que reunir as regras em um único arquivo criaria confusão — por exemplo, regras que se excluem mutuamente conforme o perfil do solicitante —, cada conjunto de condições pode merecer seu próprio arquivo.

### O arquivo começa a tratar de assuntos demais

Quando ao ler o arquivo é difícil responder em uma frase do que ele trata, provavelmente ele abrange unidades distintas. Um arquivo bem delimitado tem um assunto central claro o suficiente para ser descrito em uma única frase.

---

## 5. O Papel das Perguntas

Perguntas não são a estrutura obrigatória de todo arquivo File. Elas são uma forma de representar como os usuários buscam determinado conhecimento — úteis quando ajudam a tornar o arquivo mais próximo da linguagem real de quem vai consultar o assistente.

### Quando perguntas são úteis

Perguntas são especialmente úteis quando:
* o conteúdo responde a dúvidas específicas e recorrentes dos usuários;
* existem múltiplas formas de formular a mesma dúvida;
* a linguagem usada pelos usuários ao perguntar é diferente da linguagem formal do conteúdo corporativo.

Nesse caso, perguntas representativas podem aproximar a redação do arquivo das formas como os usuários expressam aquela necessidade.

### Quando várias perguntas representam a mesma unidade

Quando perguntas diferentes pertencem à mesma unidade de resposta integrada, elas representam a mesma unidade de conhecimento e podem estar no mesmo arquivo. O que as une é o conjunto compartilhado de regras e informações que as atende — não a mera semelhança de palavras.

*Exemplos de perguntas que representam a mesma unidade:*
* "Quem pode solicitar licença-saúde?"
* "A licença-saúde está disponível para todos os servidores?"
* "Tenho direito a licença médica remunerada?"

Se todas pertencem à mesma unidade de resposta integrada, convém mantê-las no mesmo arquivo.

### Quando diferentes formulações são variações da mesma dúvida

Variações de formulação ocorrem quando usuários diferentes escolhem palavras diferentes para expressar a mesma necessidade. Não é necessário incluir todas as formas possíveis de perguntar nem multiplicar paráfrases desnecessariamente: convém manter apenas variações que tragam formas realmente diferentes de expressar a mesma necessidade.

### Quando perguntas aparentemente relacionadas exigem arquivos separados

Quando perguntas que parecem próximas levam a respostas substancialmente diferentes — processos distintos, responsáveis distintos, condições distintas —, cada uma tende a representar uma unidade diferente e convém estar em arquivos separados.

A semelhança de assunto não é suficiente para manter perguntas juntas. O critério é a identidade da unidade de resposta: convém juntar perguntas quando uma única unidade de resposta integrada e autocontida cobre todas elas sem acrescentar conteúdo independente; convém separar quando as respostas pertencem a situações de negócio substancialmente diferentes.

*Exemplo:* "Qual é o processo para afastamento por doença?" e "Qual é o processo para afastamento por acidente de trabalho?" podem parecer variações do mesmo tema, mas se os processos, os prazos e os responsáveis forem diferentes, representam unidades distintas e convém estar em arquivos separados.

### Quando manter apenas conteúdo declarativo

Nem todo conteúdo precisa ser apresentado em formato de pergunta e resposta. Políticas, procedimentos e normas condensadas frequentemente funcionam bem como texto declarativo — descrevendo o que é, como funciona ou o que se aplica, sem estruturar o conteúdo em torno de uma pergunta explícita.

Convém usar conteúdo declarativo quando:
* o material é uma política ou diretriz que o assistente usa como referência;
* o conteúdo define critérios, regras ou condições de forma abrangente;
* o público do assistente consultará o conteúdo como fonte normativa, não como resposta a uma dúvida pontual.

---

## 6. Tipos de Conteúdo Negocial e Como Organizá-los

As orientações abaixo aplicam os critérios anteriores aos tipos de conteúdo corporativo mais comuns:

### FAQs

Em uma base File, cada arquivo pode reunir um conjunto de perguntas frequentes quando pertencem à mesma unidade de resposta integrada e autocontida. O critério não é o tema amplo — é a unidade de resposta ou a necessidade de que as informações sejam lidas em conjunto para a situação de negócio fazer sentido.

**Convém juntar:** perguntas sobre o mesmo processo, que levam à mesma orientação, ou cujas respostas são inseparáveis — condições, exceções e contexto que precisam ser compreendidos em conjunto.

**Convém separar:** perguntas que, embora pareçam do mesmo assunto, têm processos, prazos ou responsáveis substancialmente diferentes — a semelhança de vocabulário não basta para mantê-las juntas.

### Regras e normas

Uma regra de negócio completa — incluindo sua aplicação, suas condições e suas exceções — é uma unidade de conhecimento. Convém mantê-la em um único arquivo.

**Convém juntar:** a regra principal, as condições em que ela se aplica, as exceções que a modificam e as variações da mesma regra para perfis diferentes, quando a estrutura da regra for a mesma e apenas os valores diferirem.

**Convém separar:** regras diferentes que se aplicam a situações de negócio distintas, mesmo que pertençam ao mesmo domínio temático.

### Políticas condensadas

Convém que uma política caiba em um único arquivo quando trata de um conjunto coeso de diretrizes aplicáveis à mesma situação. Quando uma política de origem cobre múltiplos temas claramente distintos, convém avaliar a divisão em arquivos menores, cada um representando uma unidade temática própria.

**Convém juntar:** diretrizes que se aplicam à mesma situação, ao mesmo processo ou ao mesmo perfil de usuário.

**Convém separar:** diretrizes que se aplicam a situações claramente distintas, mesmo que façam parte do mesmo documento corporativo de origem.

### Procedimentos

Um procedimento é uma sequência de ações para realizar uma única tarefa ou atingir um único resultado. Convém mantê-lo em um arquivo.

**Convém juntar:** todos os passos necessários para completar o mesmo processo, incluindo variações do processo para casos diferentes, quando as variações forem do mesmo fluxo geral.

**Convém separar:** processos distintos — mesmo que relacionados ou sequenciais —, quando cada um tem sua própria lógica e pode ser consultado de forma independente.

### Situações e casos de uso

Quando o conteúdo descreve como agir em uma situação específica — incluindo o contexto, as condições, as orientações e as exceções —, trata-se de uma unidade de conhecimento completa.

**Convém juntar:** o contexto da situação, as orientações, as condições de aplicação, as exceções e as diferentes perguntas que levam àquela mesma situação.

**Convém separar:** situações distintas, mesmo que envolvam o mesmo processo ou o mesmo sistema.

---

## 7. Como Saber se o Arquivo Está Bem Delimitado

Antes de finalizar cada arquivo, percorra este conjunto de verificações:

**Sobre o que o arquivo representa:**
* Este arquivo trata de uma única situação, regra ou unidade de resposta de negócio?
* Consigo descrever em uma frase o que este arquivo representa?

**Sobre a completude:**
* Se eu remover qualquer parte do conteúdo, a resposta ficará incompleta?
* O arquivo faz sentido por si só, sem depender do conteúdo de outro arquivo?
* Se alguém ler apenas este arquivo, terá contexto suficiente para compreender e aplicar corretamente a resposta ou orientação que ele contém?

**Sobre os limites:**
* Existe algum conteúdo aqui que seja independente e dispensável para esta unidade? Informações compartilhadas indispensáveis à compreensão da resposta podem permanecer; convém excluir ou manter em arquivo próprio apenas o que for acessório ou independente.
* O arquivo cobre mais de uma situação de negócio claramente distinta? Se sim, avaliar a divisão em arquivos separados.
* O arquivo está centrado em uma única unidade de conhecimento? O critério principal de separação é a mudança de unidade; a extensão é apenas um critério secundário e funciona como sinal de alerta (se o arquivo estiver excessivamente longo, convém checar se não acumulou assuntos distintos).

**Sobre as perguntas (quando utilizadas):**
* As perguntas incluídas no arquivo pertencem à mesma unidade de resposta integrada e autocontida?
* Existe alguma pergunta no arquivo cuja resposta seja substancialmente diferente ou exija processo independente? Se sim, avaliar se convém separá-la em outro arquivo.

---

## 8. Requisitos do Arquivo e Template `.txt`

### Requisitos técnicos do arquivo e do pacote

Cada arquivo `.txt` da base File deve atender às seguintes condições técnicas e de formatação:

* **Formato:** arquivo de texto simples com extensão `.txt`;
* **Codificação:** UTF-8;
* **Frases:** encerradas com ponto final sempre que possível;
* **Marcadores de lista:** não utilizar *bullet points*;
* **Linhas em branco:** não utilizar linhas em branco consecutivas;
* **Tabulações:** não utilizar.

Todos os arquivos devem ser reunidos em um único pacote compactado (`.zip`) de até 100 MB, com estrutura plana (sem subpastas) e nomes de arquivo com até 130 caracteres.

### Orientação de curadoria sobre extensão e delimitação

O principal critério para decidir a separação ou agrupamento de arquivos é sempre a **mudança da unidade de conhecimento** (quando mudam substancialmente a regra, o contexto, as condições ou a situação de negócio).

A extensão do arquivo é um critério estritamente secundário:
* O modo File é indicado para conteúdos concisos, voltados a uma única situação de negócio;
* Convém que o arquivo seja suficientemente curto para representar uma única unidade de conhecimento coerente e autocontida;
* Um arquivo excessivamente longo funciona apenas como um **sinal de alerta** de que mais de uma unidade de conhecimento pode ter sido indevidamente reunida no mesmo texto;
* Por outro lado, um arquivo curto que misture assuntos distintos continua inadequado: a coesão da unidade de conhecimento prevalece sempre sobre o tamanho.

### Template `.txt`

O template abaixo é um modelo orientador que pode ser usado e adaptado pelas áreas responsáveis pelo conteúdo ao preparar os arquivos da base File. Ele materializa as orientações deste guia em uma estrutura copiável. A ordem dos blocos não é uma obrigação rígida, desde que o arquivo final preserve a unidade de conhecimento, a completude do contexto e as regras de formatação documentadas.

**Instruções de uso do template:**
* Os rótulos entre colchetes `[ ]` são apenas orientadores de curadoria — **não devem aparecer no arquivo final entregue à base**. Remova-os ao preparar o conteúdo real;
* Os campos marcados como **(quando aplicável)** são opcionais. Inclua-os apenas quando o conteúdo existir e for necessário para aquela unidade de conhecimento;
* O arquivo final deve conter apenas texto corrido: sem marcadores de lista, sem tabulações e sem linhas em branco consecutivas.

---

```
[SITUAÇÃO OU ASSUNTO]
Descreva em uma ou duas frases o tema central deste arquivo. Este campo orienta
a curadoria e pode ser incorporado como parte do texto principal ou removido do
arquivo final, conforme o conteúdo.

[PERGUNTAS REPRESENTATIVAS] (quando aplicável)
Liste as formas principais como os usuários podem buscar este conteúdo. Inclua apenas
variações que tragam formas realmente diferentes de expressar a mesma necessidade,
evitando o excesso de paráfrases, e que se dirijam a esta mesma unidade de resposta integrada.
Escreva cada formulação em linha própria, encerrada com ponto de interrogação.

[CONTEÚDO OU RESPOSTA PRINCIPAL]
Escreva o texto principal que responde à situação ou representa a regra, política
ou procedimento. Utilize parágrafos com frases completas, encerradas com ponto
final. Não utilize marcadores de lista nem tabulações.

[CONDIÇÕES] (quando aplicável)
Descreva as condições nas quais a resposta ou regra acima se aplica. Integre ao
texto corrido, em parágrafos, sem marcadores. Se as condições forem parte
inseparável da resposta principal, podem ser incorporadas diretamente a ela.

[EXCEÇÕES] (quando aplicável)
Descreva os casos em que a regra ou resposta não se aplica, ou em que uma
orientação diferente prevalece. Integre ao texto corrido, sem marcadores. Inclua
apenas as exceções que modificam diretamente a regra representada neste arquivo.

[INFORMAÇÕES COMPLEMENTARES] (quando aplicável)
Inclua apenas informações que precisem fazer parte desta mesma unidade de
conhecimento — contexto, definições ou orientações que, se ausentes, tornariam a
resposta incompleta ou difícil de aplicar para esta situação. Informações de contexto
geral podem ser mantidas (e até repetidas em outros arquivos) quando forem indispensáveis
à compreensão local. Convém excluir apenas conteúdos que sejam independentes e
dispensáveis para esta unidade de negócio.
```

---

### Exemplo de arquivo bem formado

O arquivo abaixo ilustra como o template orientador pode ser preenchido para uma situação hipotética. Note como as três perguntas representativas não possuem isoladamente a "mesma resposta" textual, mas pertencem à mesma **unidade de resposta integrada**: abordam facetas inseparáveis e complementares da mesma situação de negócio (direito ao benefício, canal e prazo de solicitação, e despesas elegíveis), respondidas de forma conjunta pelo texto corrido, condições e exceções. Os rótulos entre colchetes não aparecem no arquivo final.

---

```
Solicitação de reembolso de despesas médicas por servidor ativo.

Como solicitar reembolso de despesa médica?
Quais despesas médicas podem ser reembolsadas pelo plano?
Tenho direito a reembolso pelo plano de saúde corporativo?

O servidor ativo tem direito ao reembolso de despesas médicas comprovadas e
elegíveis conforme as diretrizes do plano de saúde corporativo. A solicitação
deve ser realizada pelo portal de benefícios, com anexo do comprovante de
pagamento e do documento de identificação da despesa, em até noventa dias
corridos a partir da data do atendimento.

O reembolso aplica-se a despesas realizadas com prestadores credenciados ao
plano. Nos casos de urgência e emergência, o reembolso também é aplicável a
atendimentos realizados com prestadores não credenciados, desde que a urgência
seja devidamente justificada no formulário de solicitação.

Não são elegíveis para reembolso: despesas com medicamentos de uso contínuo
adquiridos fora da rede conveniada, tratamentos estéticos e procedimentos não
cobertos pela tabela vigente do plano. Em caso de dúvida sobre a elegibilidade
de uma despesa específica, o servidor deve consultar a central de atendimento
do plano antes de realizar o procedimento.
```
