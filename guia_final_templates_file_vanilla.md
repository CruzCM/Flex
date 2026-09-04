# GENERA RAG — Guia Final de Templates

Guia interno para preenchimento dos templates de conteúdo nas modalidades **File** e **Vanilla**.

Este documento trata somente da estrutura dos templates e de como preenchê-los.

---

# 1. Guia File

## Quando usar

Use este template quando cada arquivo `.txt` representar **uma única unidade de conhecimento coerente e autocontida**.

O conteúdo do arquivo deve fazer sentido como um conjunto e não depender de outro arquivo para ser corretamente compreendido.

## Template

```text
[SITUAÇÃO OU ASSUNTO]

[PERGUNTAS REPRESENTATIVAS] (quando aplicável)

[CONTEÚDO OU RESPOSTA PRINCIPAL]

[CONDIÇÕES] (quando aplicável)

[EXCEÇÕES] (quando aplicável)

[INFORMAÇÕES COMPLEMENTARES] (quando aplicável)
```

## Como preencher

### [SITUAÇÃO OU ASSUNTO]

Descreva qual situação, regra ou assunto específico o arquivo representa.

Pergunta de apoio:

**Qual situação este arquivo precisa resolver?**

### [PERGUNTAS REPRESENTATIVAS]

Inclua formas diferentes pelas quais o usuário pode buscar aquela mesma unidade de conhecimento.

As perguntas devem levar à **mesma resposta integrada**.

Evite excesso de paráfrases.

Pergunta de apoio:

**Quais dúvidas diferentes levam a esta mesma situação ou regra?**

### [CONTEÚDO OU RESPOSTA PRINCIPAL]

Registre a regra, orientação, política, procedimento ou resposta principal.

Pergunta de apoio:

**Qual é a informação principal que o agente precisa conhecer?**

### [CONDIÇÕES]

Inclua requisitos, público, prazo, contexto ou circunstâncias que determinem quando a regra se aplica.

Pergunta de apoio:

**Em quais condições essa orientação é válida?**

### [EXCEÇÕES]

Inclua os casos em que a regra muda, não se aplica ou exige ressalva.

A exceção deve permanecer junto da regra que modifica.

Pergunta de apoio:

**Quando essa regra deixa de valer ou precisa de limitação?**

### [INFORMAÇÕES COMPLEMENTARES]

Inclua apenas contexto, definições ou orientações necessárias para tornar a unidade completa.

Não inclua informações independentes apenas porque pertencem ao mesmo tema.

Pergunta de apoio:

**O que ainda precisa estar neste arquivo para que ele funcione sozinho?**

## Arquivo final

Os rótulos entre colchetes são apenas orientadores de curadoria e **não devem aparecer no `.txt` final**.

---

# 2. Guia Vanilla — Splitter

## Quando usar

Use este template quando o conteúdo Vanilla for preparado como **texto livre**, normalmente com `RecursiveCharacterTextSplitter`.

O objetivo é estruturar o conteúdo para que os chunks gerados tenham contexto suficiente para serem compreendidos isoladamente.

## Template

```text
[NOME DESCRITIVO DO PROCEDIMENTO OU REGRA]

[ENUNCIADO DA REGRA E ÂNCORA DE SUJEITO]

[CRITÉRIOS E PRÉ-REQUISITOS]

[EXCEÇÕES E RESTRIÇÕES IMEDIATAS]

[ETAPAS OPERACIONAIS] (quando aplicável)
```

## Como preencher

### [NOME DESCRITIVO DO PROCEDIMENTO OU REGRA]

Use um título que identifique claramente o assunto.

Evite títulos genéricos como “Regras”, “Condições Gerais” ou “Importante”.

### [ENUNCIADO DA REGRA E ÂNCORA DE SUJEITO]

Abra o conteúdo identificando explicitamente o assunto, público ou objeto da orientação.

Evite referências vagas como:

- “ele”;
- “este benefício”;
- “conforme item anterior”;
- “nas condições acima”.

O objetivo é permitir que o trecho mantenha significado mesmo quando recuperado sozinho.

### [CRITÉRIOS E PRÉ-REQUISITOS]

Apresente as condições necessárias para aplicação da regra.

Mantenha público, requisitos, prazos e demais condicionantes próximos da regra principal.

### [EXCEÇÕES E RESTRIÇÕES IMEDIATAS]

Registre limitações, vedações e hipóteses em que a regra não se aplica.

Mantenha as exceções no mesmo parágrafo ou em parágrafos imediatamente próximos da regra que modificam.

### [ETAPAS OPERACIONAIS]

Quando houver processo sequencial, descreva os passos de forma linear, explícita e autocontida.

Exemplo:

```text
Passo 1: Acessar o sistema institucional.
Passo 2: Selecionar a funcionalidade correspondente.
Passo 3: Anexar a documentação necessária.
Passo 4: Confirmar a solicitação.
```

## Regra de preenchimento

No Vanilla com splitter, o conteúdo deve ser escrito pensando que **qualquer trecho poderá ser recuperado separadamente**.

---

# 3. Guia Vanilla — Markdown

## Quando usar

Use este template quando o conteúdo Vanilla estiver organizado com cabeçalhos Markdown e a indexação utilizar `MarkdownHeaderTextSplitter`.

Os títulos devem representar a hierarquia real do conteúdo e ajudar a delimitar seções semanticamente coerentes.

## Template

```markdown
# [TEMA PRINCIPAL]

Breve contextualização do domínio ou documento.

## [SUBTEMA OU PROCESSO]

Texto que apresenta o assunto desta seção com contexto suficiente para ser compreendido isoladamente.

### [REGRA, SITUAÇÃO OU PROCEDIMENTO]

Regra ou orientação principal.

Condições necessárias para aplicação da regra.

Exceções e restrições relacionadas.

### [OUTRA REGRA, SITUAÇÃO OU PROCEDIMENTO]

Regra ou orientação principal.

Condições necessárias para aplicação da regra.

Exceções e restrições relacionadas.

## [OUTRO SUBTEMA]

Texto referente ao novo assunto.
```

## Como preencher

### `# [TEMA PRINCIPAL]`

Identifique o domínio geral do documento.

Exemplo:

```markdown
# Open Finance
```

### `## [SUBTEMA OU PROCESSO]`

Use para separar os principais assuntos ou processos do domínio.

Prefira títulos específicos e descritivos.

Exemplo:

```markdown
## Consentimento e Compartilhamento de Dados
```

Evite títulos genéricos como:

```markdown
## Regras
## Informações
## Diversos
```

### `### [REGRA, SITUAÇÃO OU PROCEDIMENTO]`

Use para unidades mais específicas dentro do subtema.

Exemplo:

```markdown
### Cancelamento do Consentimento
```

O conteúdo abaixo do cabeçalho deve apresentar a regra, condições e exceções necessárias para que a seção faça sentido isoladamente.

## Regras de preenchimento

- mantenha uma hierarquia consistente de `#`, `##` e `###`;
- use títulos que representem a estrutura semântica real do conteúdo;
- evite depender de informações localizadas em seções distantes;
- mantenha regra, condição e exceção próximas;
- os cabeçalhos configurados na indexação devem corresponder aos utilizados no conteúdo.

---

# 4. Síntese

**File:** o template organiza uma unidade de conhecimento completa e autocontida.

**Vanilla — Splitter:** o template organiza texto livre para gerar chunks semanticamente compreensíveis.

**Vanilla — Markdown:** o template organiza o conteúdo por hierarquia de cabeçalhos para orientar a segmentação.
