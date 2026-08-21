# REGRAS DE OURO DE ENGENHARIA DE DADOS
## Norma Universal para Projetos de Dados, ETL, ELT, SQL, PySpark e Processamento Distribuído

---

# 0. Objetivo

Este documento estabelece uma **norma universal de Engenharia de Dados** para construção, manutenção, revisão e publicação de pipelines.

Ele deve ser aplicável a qualquer projeto, independentemente de:

- domínio de negócio;
- banco de dados;
- engine de processamento;
- ambiente;
- linguagem;
- tecnologia de storage;
- ferramenta de orquestração.

A prioridade é:

```text
CORRETUDE
→ CONTRATO
→ SEGURANÇA OPERACIONAL
→ OBSERVABILIDADE
→ PERFORMANCE
→ ELEGÂNCIA
```

Performance nunca justifica perda de corretude.

Elegância nunca justifica aumento de risco.

Automação nunca justifica ausência de controle.

---

# 1. Classificação das regras

## P0 — Bloqueante

Se uma regra P0 não for atendida:

```text
NÃO EXECUTAR
NÃO PUBLICAR
NÃO PROMOVER
```

Regras P0 protegem:

- integridade;
- origem;
- destino;
- schema;
- chave;
- cardinalidade;
- idempotência;
- rastreabilidade;
- regra de negócio.

---

## P1 — Obrigatória para produção

Pode ser flexibilizada em exploração controlada, mas precisa estar resolvida antes de produção.

Regras P1 protegem:

- previsibilidade;
- performance;
- custo;
- manutenção;
- troubleshooting;
- estabilidade operacional.

---

## P2 — Padrão de qualidade

São práticas esperadas para manter:

- clareza;
- consistência;
- legibilidade;
- manutenibilidade.

Exceções são permitidas quando conscientes e documentadas.

---

# 2. REGRA MESTRA

## GOLD-000 — Antes do código, defina o contrato

**Severidade: P0**

Antes de escrever uma transformação relevante, responder:

```text
1. Onde este código executa?
2. Qual é a fonte?
3. Qual é o grão da entrada?
4. Qual é o grão da saída?
5. Qual é a chave?
6. Qual data de referência vale?
7. Qual volume será lido?
8. Quais filtros reduzem esse volume?
9. Quais joins existem?
10. Qual cardinalidade é esperada?
11. Qual schema final é obrigatório?
12. Existe escrita?
13. A escrita é idempotente?
14. Como o resultado será validado?
15. Qual regra de negócio está sendo implementada?
```

Se essas respostas não existem, o código ainda está em fase de exploração.

---

# 3. Ambiente de execução

## GOLD-001 — Todo código deve ter ambiente de execução conhecido

**Severidade: P0**

Antes de qualquer célula, função ou etapa, saber:

```text
onde executa
quem possui os dados
onde está o processamento
onde está o driver
onde estão os workers
```

Não assumir que:

```text
variável
função
biblioteca
arquivo
configuração
```

existe automaticamente em outro ambiente de execução.

---

## GOLD-002 — Configuração estrutural deve nascer antes da execução

**Severidade: P0**

Configurações que alteram a estrutura de execução devem ser definidas antes do início do processamento.

Exemplos:

- memória;
- executores;
- workers;
- cores;
- paralelismo;
- bibliotecas;
- drivers;
- conectores;
- parâmetros de engine;
- configurações de shuffle.

### Proibido

Alterar configuração estrutural no meio do pipeline para tentar corrigir comportamento inesperado.

---

## GOLD-003 — Configuração deve ser centralizada

**Severidade: P0**

Um pipeline deve possuir um ponto único e identificável para configuração.

Evitar:

```text
configuração espalhada
estado implícito
dependência da ordem de execução
```

O pipeline precisa ser reexecutável de forma previsível.

---

## GOLD-004 — Não existe configuração universal de performance

**Severidade: P1**

Valores de:

```text
partições
memória
cores
workers
broadcast
timeouts
```

não devem virar dogma.

A configuração deve resultar de:

```text
baseline
+
característica do workload
+
evidência de execução
```

---

# 4. Identidade das fontes

## GOLD-005 — Toda leitura crítica deve usar identificação completa da fonte

**Severidade: P0**

Sempre que houver catálogo, schema ou namespace, utilizar:

```text
schema.tabela
```

Evitar leitura ambígua baseada apenas em:

```text
tabela
```

Motivo:

> contexto implícito pode direcionar silenciosamente para a fonte errada.

---

## GOLD-006 — Nome canônico e ambiente são responsabilidades diferentes

**Severidade: P0**

Separar:

```text
nome canônico
+
contexto de ambiente
```

O nome lógico deve permanecer estável.

O ambiente deve resolver:

```text
schema
catálogo
namespace
database
```

sem espalhar hardcodes.

---

## GOLD-007 — Nome físico nunca deve ser inferido

**Severidade: P0**

Nome de:

```text
schema
tabela
atributo
indicador
partição
```

deve vir de:

- DDL;
- catálogo;
- metastore;
- contrato;
- documentação oficial;
- schema real.

Nunca corrigir abreviação por memória.

---

## GOLD-008 — Tabela catalogada é tabela; path é storage

**Severidade: P0**

Quando existe uma entidade catalogada, tratá-la como entidade catalogada.

Usar path físico apenas quando a intenção for realmente operar sobre storage.

Não substituir silenciosamente:

```text
schema.tabela
```

por:

```text
path físico
```

---

# 5. Fontes externas e bancos relacionais

## GOLD-009 — Banco relacional deve ser tratado como banco relacional

**Severidade: P0**

Uma tabela relacional deve ser acessada por:

```text
schema.tabela
```

Não misturar semântica de banco relacional com semântica de arquivos.

---

## GOLD-010 — Fonte gigante nunca é varrida apenas para diagnóstico

**Severidade: P0**

Em tabelas de alta volumetria, operações como:

```text
COUNT(*) global
DISTINCT global
MIN/MAX global
GROUP BY global
```

não devem ser executadas gratuitamente.

Antes de uma leitura grande, responder:

```text
qual pergunta preciso responder?
qual recorte mínimo responde?
qual atributo reduz a leitura?
qual agregação pode ocorrer na origem?
```

---

## GOLD-011 — Pushdown deve ser usado quando reduz transferência com segurança

**Severidade: P1**

Empurrar para a origem, quando adequado:

- filtros;
- seleção de atributos;
- agregações redutoras;
- envelopes temporais;
- amostras limitadas.

Evitar trazer grande volume para o engine distribuído para descartar depois.

---

## GOLD-012 — Paralelismo sobre fonte externa precisa respeitar a origem

**Severidade: P0**

Paralelismo de leitura não é recurso gratuito.

Avaliar:

- capacidade da origem;
- concorrência;
- distribuição;
- atributo de particionamento;
- bounds;
- impacto em outros consumidores.

Nunca aumentar paralelismo apenas porque o cluster suporta.

---

## GOLD-013 — Atributo de particionamento precisa ser adequado

**Severidade: P1**

Escolher atributo que possua:

- distribuição razoável;
- domínio conhecido;
- limites conhecidos;
- baixa concentração extrema;
- semântica compatível.

Não particionar por atributo altamente enviesado sem estudo.

---

# 6. Data de referência e reprocessamento

## GOLD-014 — Data de referência é parte do contrato

**Severidade: P0**

Todo pipeline temporal deve declarar explicitamente:

```text
data de execução
data de referência
competência
janela analisada
```

Evitar esconder regra em funções como:

```text
data atual
agora
hoje
```

quando o pipeline precisa permitir reprocessamento histórico.

---

## GOLD-015 — Todo pipeline relevante precisa ser reexecutável

**Severidade: P0**

Reexecutar a mesma competência deve produzir:

```text
mesma regra
mesmo contrato
sem duplicação
```

Idempotência é requisito de produção.

---

# 7. Schema como contrato

## GOLD-016 — Schema final não é consequência acidental do pipeline

**Severidade: P0**

Antes da persistência, definir:

- nomes;
- ordem;
- tipos;
- nulabilidade;
- partições;
- chave;
- grão.

A saída deve ser projetada contra contrato explícito.

---

## GOLD-017 — Nome de atributo deve ser único no DataFrame

**Severidade: P0**

Após etapa crítica:

```text
nenhum atributo duplicado
```

Exemplo de validação:

```python
duplicados = [
    atributo
    for atributo in set(df.columns)
    if df.columns.count(atributo) > 1
]

if duplicados:
    raise RuntimeError(
        f"Atributos duplicados encontrados: {duplicados}"
    )
```

---

## GOLD-018 — Join de enriquecimento não pode reintroduzir atributo canônico duplicado

**Severidade: P0**

Depois de join, decidir:

```text
qual atributo antigo permanece?
qual atributo novo entra?
qual nome intermediário será usado?
```

### Anti-padrão

```python
select(
    "origem.*",
    F.col("enriquecimento.atributo").alias("atributo")
)
```

quando `origem.*` já contém `atributo`.

### Correto

Projetar conscientemente:

```python
resultado = (
    origem.alias("origem")
    .join(
        enriquecimento.alias("enriquecimento"),
        condicao,
        "left"
    )
    .select(
        F.col("origem.chave"),
        F.col("origem.atributo_a"),
        F.col("enriquecimento.atributo").alias("atributo"),
    )
)
```

---

## GOLD-019 — Atributo canônico deve ter um único dono por etapa

**Severidade: P0**

Quando uma etapa substitui estado:

```text
estado anterior
→ estado novo
```

não manter ambos com o mesmo nome.

Quando ambos forem necessários:

```text
atributo_anterior
atributo_novo
```

ou nomes equivalentes definidos pelo contrato.

---

# 8. Joins

## GOLD-020 — Join precisa ser semanticamente explícito

**Severidade: P0**

Antes do join, definir:

```text
lado esquerdo
lado direito
tipo de join
chave
cardinalidade
comportamento de NULL
atributos preservados
atributos incorporados
```

---

## GOLD-021 — `alias()` de DataFrame é qualificador, não namespace composto

**Severidade: P1**

Correto:

```python
a = df_a.alias("a")
b = df_b.alias("b")

resultado = a.join(
    b,
    F.col("a.chave") == F.col("b.chave"),
    "left",
)
```

Não assumir hierarquias como:

```text
a.b.atributo
```

---

## GOLD-022 — `alias()` de coluna serve para projeção

**Severidade: P1**

Usar para:

- `select`;
- `withColumn`;
- projeção final.

Não usar renomeação como substituto de condição booleana de join.

---

## GOLD-023 — `join(on=...)` deve usar formato válido

**Severidade: P1**

Permitido:

```python
on="chave"
```

```python
on=["chave_1", "chave_2"]
```

```python
on=condicao_booleana
```

Evitar estruturas ambíguas ou não suportadas.

---

## GOLD-024 — DataFrame limpo pode usar lista de chaves; DataFrame misturado deve qualificar

**Severidade: P1**

### Caso limpo

```python
df_a.join(
    df_b,
    on=["chave_1", "chave_2"],
    how="left",
)
```

### Caso com múltiplos joins prévios

```python
a = df_a.alias("a")
b = df_b.alias("b")

resultado = a.join(
    b,
    on=(
        (F.col("a.chave_1") == F.col("b.chave_1")) &
        (F.col("a.chave_2") == F.col("b.chave_2"))
    ),
    how="left",
)
```

---

## GOLD-025 — Join bom termina com projeção consciente

**Severidade: P0**

Regra:

```text
JOIN
→ SELECT
→ SCHEMA LIMPO
```

Não carregar colunas duplicadas para o restante do pipeline.

---

## GOLD-026 — Cardinalidade do join precisa ser conhecida

**Severidade: P0**

Antes do join, classificar:

```text
1:1
N:1
1:N
N:N
```

Se um lado deveria ser único:

```text
prove a unicidade
```

antes do join.

---

## GOLD-027 — `DISTINCT` não corrige cardinalidade errada

**Severidade: P0**

Anti-padrão:

```sql
SELECT DISTINCT *
FROM resultado
```

usado para esconder multiplicação de linhas.

Quando existe duplicidade, definir:

```text
qual registro deve vencer?
por qual regra?
```

Usar critérios explícitos:

- `ROW_NUMBER`;
- data mais recente;
- prioridade;
- regra de negócio;
- agregação semanticamente válida.

---

## GOLD-028 — Comparação null-safe é exceção de negócio

**Severidade: P1**

Chave nula normalmente precisa ser investigada.

Só tratar:

```text
NULL = NULL
```

como equivalência quando a regra de negócio exigir.

---

# 9. Projeção e flatten

## GOLD-029 — Flatten segue contrato, não conveniência

**Severidade: P0**

Quando existe schema alvo:

```text
projetar explicitamente
```

Não depender de:

```text
*
alias.*
```

em pipeline longo.

---

## GOLD-030 — Não depender de alias eterno

**Severidade: P1**

Depois de múltiplos joins e transformações, qualificadores podem deixar de ser uma abstração segura.

Na projeção final:

```text
selecionar explicitamente
renomear explicitamente
```

---

## GOLD-031 — `SELECT *` é proibido em transformação produtiva grande

**Severidade: P1**

Aceitável somente em:

- exploração;
- amostra;
- cópia controlada;
- fonte comprovadamente pequena.

Em produção:

```text
selecionar apenas o necessário
```

---

# 10. Construção de SQL

## GOLD-032 — Query relevante não começa pelo `SELECT`

**Severidade: P0**

Antes da query, definir:

```text
objetivo
fontes
grão
chave
data
filtros
joins
destino
validações
```

Depois escrever SQL.

---

## GOLD-033 — CTE deve possuir responsabilidade clara

**Severidade: P2**

Preferir nomes como:

```text
parametros
base_filtrada
base_elegivel
dimensao_unica
agregado
resultado_final
```

Evitar:

```text
tmp1
x
abc
final2
```

---

## GOLD-034 — Filtrar e projetar cedo

**Severidade: P1**

Fluxo preferencial:

```text
fonte
→ filtro
→ seleção de atributos
→ joins
→ agregações
```

Quanto menor o dado antes do primeiro shuffle, melhor.

---

## GOLD-035 — `ORDER BY` global exige justificativa

**Severidade: P1**

Não ordenar grandes volumes apenas para apresentação.

Para amostra:

```sql
SELECT
    atributo
FROM schema.tabela
ORDER BY atributo
LIMIT 100
```

---

# 11. Funções nativas e UDF

## GOLD-036 — Função nativa antes de UDF

**Severidade: P1**

Preferir funções nativas da engine para:

- string;
- data;
- condicionais;
- regex;
- agregações;
- parsing.

UDF deve ser exceção, pois pode:

- reduzir otimização;
- aumentar serialização;
- criar fronteira entre runtimes;
- dificultar troubleshooting.

---

# 12. Actions e driver

## GOLD-037 — Driver não é storage

**Severidade: P0**

Proibido em grande volume:

```python
df.collect()
df.toPandas()
```

Aceitável quando o resultado está previamente reduzido:

```python
df.limit(100).collect()
df.limit(1000).toPandas()
```

---

## GOLD-038 — Toda action cara precisa de propósito

**Severidade: P1**

Exemplos de actions:

```text
count
show
collect
take
write
toPandas
```

Não criar actions apenas para imprimir progresso.

Uma action deve:

- validar;
- materializar com propósito;
- escrever;
- produzir métrica necessária.

---

# 13. Cache, persistência intermediária e lineage

## GOLD-039 — Cache só com reuso real

**Severidade: P1**

Usar quando houver:

```text
subplano caro
+
mais de uma action
```

Padrão:

```python
df = df.persist(...)
df.count()

validar(df)
escrever(df)

df.unpersist()
```

---

## GOLD-040 — Todo cache possui dono e fim

**Severidade: P1**

Para cada persistência, responder:

```text
quem materializa?
quantas vezes reutiliza?
quando libera?
```

---

## GOLD-041 — Checkpoint resolve problema real

**Severidade: P1**

Usar checkpoint ou materialização quando houver:

- lineage excessiva;
- self-join problemático;
- reaproveitamento caro;
- plano instável;
- necessidade de isolamento.

Não usar apenas para “testar se melhora”.

---

# 14. Performance

## GOLD-042 — Query antes de recurso

**Severidade: P0**

Ordem obrigatória:

```text
1. reduzir leitura
2. reduzir atributos
3. revisar filtros
4. revisar joins
5. revisar cardinalidade
6. revisar skew
7. revisar shuffle
8. revisar cache
9. revisar escrita
10. só então revisar recursos
```

Não começar aumentando:

```text
memória
cores
workers
executores
```

---

## GOLD-043 — Plano físico deve ser inspecionável

**Severidade: P1**

Em processamento relevante, saber identificar:

- scans;
- filtros;
- exchanges;
- joins;
- agregações;
- broadcast;
- sort;
- adaptive execution.

A engine não deve ser uma caixa-preta.

---

## GOLD-044 — Shuffle deve ser esperado

**Severidade: P1**

Operações típicas:

```text
join
groupBy
distinct
orderBy
repartition
```

Antes da execução, saber onde haverá redistribuição.

---

## GOLD-045 — Skew é problema de distribuição

**Severidade: P1**

Sinais:

```text
uma task muito mais lenta
execução presa no final
spill concentrado
poucos workers ativos no final
```

Ações:

```text
1. medir distribuição
2. separar NULL/códigos dominantes
3. pré-agregar
4. usar broadcast quando aplicável
5. usar salting somente em último caso
```

---

## GOLD-046 — Spill não implica automaticamente falta de memória

**Severidade: P1**

Antes de aumentar memória:

```text
reduzir linhas
reduzir atributos
revisar partições
revisar skew
revisar join
revisar cache
```

---

# 15. Broadcast

## GOLD-047 — Broadcast precisa ser consciente

**Severidade: P1**

Broadcast é apropriado quando:

```text
estrutura pequena
+
cardinalidade controlada
+
cabe em memória
+
enriquece estrutura maior
```

Não usar quando:

- tamanho é desconhecido;
- dimensão não é única;
- estrutura é grande;
- risco de memória é relevante.

---

# 16. Partições

## GOLD-048 — `repartition` é operação intencional

**Severidade: P1**

Usar para:

- redistribuir;
- aumentar paralelismo;
- corrigir distribuição física;
- preparar escrita específica.

Nunca usar como decoração.

---

## GOLD-049 — `coalesce` é ferramenta de redução de saída

**Severidade: P1**

Útil quando existem partições demais antes da escrita.

Evitar:

```python
coalesce(1)
```

em produção, salvo requisito explícito e volume pequeno.

---

# 17. Escrita e publicação

## GOLD-050 — Escrita física é operação crítica

**Severidade: P0**

Antes de escrever:

```text
chave validada
schema validado
cardinalidade validada
resultado vazio tratado
modo de escrita conhecido
destino confirmado
```

---

## GOLD-051 — Nunca publicar resultado vazio sem regra explícita

**Severidade: P0**

Quando população > 0 é requisito:

```python
if quantidade_final == 0:
    raise RuntimeError(
        "Resultado vazio. Escrita bloqueada."
    )
```

---

## GOLD-052 — Overwrite precisa ser idempotente e isolado

**Severidade: P0**

Evitar ler o mesmo destino que será sobrescrito dentro da mesma linhagem lógica sem isolamento.

Quando necessário:

```text
fonte segura
→ resultado
→ validação
→ staging
→ readback
→ destino
```

---

## GOLD-053 — Readback prova persistência

**Severidade: P0 em carga crítica**

Após escrita relevante:

```text
quantidade persistida
=
quantidade validada antes da escrita
```

Quando aplicável, validar também:

- schema;
- chave;
- partição;
- invariantes.

---

## GOLD-054 — `DROP TABLE` não é operação normal de pipeline

**Severidade: P0**

Drop só é aceitável em:

- migração deliberada;
- alteração estrutural aprovada;
- procedimento excepcional controlado.

Nunca como mecanismo rotineiro de reprocessamento.

---

# 18. Qualidade e gates

## GOLD-055 — Gate de chave é bloqueante

**Severidade: P0**

Antes da publicação:

```text
chave única quando exigida
chave não nula quando exigida
```

---

## GOLD-056 — Gate de cardinalidade é bloqueante

**Severidade: P0**

Comparar:

```text
entrada esperada
resultado
destino persistido
```

Qualquer divergência exige explicação.

---

## GOLD-057 — Gate de schema é bloqueante

**Severidade: P0**

Validar:

```text
nomes
ordem
tipos
quantidade de atributos
partições
```

---

## GOLD-058 — Invariantes de negócio são testes técnicos

**Severidade: P0**

Se uma regra funcional produz identidade verificável, ela deve virar teste.

Exemplo genérico:

```text
valor_total
=
valor_componente_1
+
valor_componente_2
+
valor_componente_3
```

---

# 19. Observabilidade

## GOLD-059 — Toda etapa relevante deve registrar duração

**Severidade: P1**

Registrar:

```text
nome da etapa
início
fim
duração
linhas quando já obtidas por action necessária
partições quando relevante
status
```

Não executar action extra apenas para preencher log.

---

## GOLD-060 — Log deve permitir localizar gargalo e falha

**Severidade: P1**

Um resumo de execução deve responder:

```text
onde gastou tempo?
onde falhou?
qual volume chegou?
qual etapa domina?
qual etapa publicou?
```

---

## GOLD-061 — Métrica sem decisão não merece custo alto

**Severidade: P1**

Antes de calcular uma estatística cara:

```text
qual decisão muda se essa métrica vier alta ou baixa?
```

Se nenhuma decisão muda, reavaliar sua necessidade.

---

# 20. Documentação

## GOLD-062 — Source, regra e target são documentos diferentes

**Severidade: P1**

Separar:

```text
SOURCE
o que existe na origem

REGRA
como transformamos

TARGET
o que entregamos
```

Não misturar semântica física da origem com significado derivado do target.

---

## GOLD-063 — Comentário documenta decisão, não sintaxe

**Severidade: P2**

Bom comentário:

```text
# materialização necessária porque o mesmo subplano
# é reutilizado por validação e escrita
```

Comentário inútil:

```text
# faz join
```

---

# 21. Mudança de regra

## GOLD-064 — Regra de negócio nunca muda silenciosamente

**Severidade: P0**

Fluxo:

```text
origem
→ valores reais
→ comportamento atual
→ impacto
→ decisão
→ alteração mínima
→ comparação antes/depois
```

Engenharia não deve inventar regra de negócio para preencher lacuna.

---

## GOLD-065 — Alteração mínima é preferência em sistema auditado

**Severidade: P1**

Se o problema é uma regra:

```text
alterar a regra
```

Não usar a correção como oportunidade para refatorar componentes não relacionados.

Isso reduz:

- regressão;
- superfície de teste;
- dificuldade de comparação.

---

# 22. Governança de versão

## GOLD-066 — Versão nova precisa de motivo

**Severidade: P1**

Criar nova versão quando houver:

- mudança funcional;
- correção relevante;
- alteração estrutural;
- necessidade operacional;
- ganho comprovado.

Não criar versão apenas por reorganização estética.

---

## GOLD-067 — Baseline precisa ser explícita

**Severidade: P1**

Todo projeto deve saber:

```text
qual versão é referência funcional?
qual versão é baseline técnica?
qual versão está em produção?
```

Esses papéis podem ou não coincidir.

---

# 23. Gates oficiais de aprovação

## GATE 1 — Intenção

Obrigatório:

- objetivo;
- ambiente;
- data;
- fonte;
- grão;
- chave;
- destino.

Sem isso:

```text
BLOQUEADO
```

---

## GATE 2 — Dados

Obrigatório:

- filtros;
- atributos;
- joins;
- cardinalidades;
- nulidade das chaves;
- schema final.

Sem isso:

```text
BLOQUEADO
```

---

## GATE 3 — Segurança operacional

Obrigatório:

- volume estimado;
- impacto na origem;
- paralelismo;
- risco de full scan;
- modo de escrita;
- isolamento origem/destino.

Sem isso:

```text
BLOQUEADO
```

---

## GATE 4 — Performance

Obrigatório para rotina relevante:

- shuffle conhecido;
- skew avaliado;
- broadcast consciente;
- partições justificadas;
- cache justificado;
- plano inspecionável.

---

## GATE 5 — Publicação

Obrigatório:

- chave;
- cardinalidade;
- schema;
- resultado vazio tratado;
- invariantes;
- escrita;
- readback;
- log final.

Sem isso:

```text
NÃO PUBLICAR
```

---

# 24. Anti-patterns bloqueantes

## Ambiente

```text
configuração estrutural tardia
ambiente implícito
dependência da ordem manual de execução
contexto de fonte implícito
```

## Fontes

```text
schema omitido
nome físico inferido
full scan diagnóstico
leitura de atributos desnecessários
```

## Dados

```text
SELECT * em fato grande
DISTINCT para esconder duplicidade
join sem cardinalidade
atributo duplicado após join
chave nula ignorada
```

## Processamento distribuído

```text
collect grande
toPandas grande
cache por hábito
coalesce(1) em produção
repartition sem objetivo
mais memória antes de diagnóstico
```

## Escrita

```text
overwrite sem validação
resultado vazio publicado
origem e destino em conflito de linhagem
DROP TABLE como rotina
schema acidental persistido
```

## Regra de negócio

```text
regra alterada sem decisão
sentinela reinterpretada sem validação
NULL convertido para zero sem regra
exceção tratada por conveniência técnica
```

---

# 25. Checklist Master antes da execução

## Ambiente

- [ ] Sei onde cada etapa executa.
- [ ] Configuração está centralizada.
- [ ] Nenhuma configuração estrutural será alterada no meio.
- [ ] Dependências estão disponíveis no ambiente correto.

## Fontes

- [ ] `schema.tabela` está explícito.
- [ ] Nome físico foi confirmado.
- [ ] Volume da origem é conhecido.
- [ ] Recorte mínimo foi definido.
- [ ] Não existe varredura global gratuita.
- [ ] Apenas atributos necessários serão lidos.

## Query

- [ ] Grão definido.
- [ ] Chave definida.
- [ ] Data de referência explícita.
- [ ] Filtro aplicado cedo.
- [ ] Joins justificados.
- [ ] Cardinalidade validada.
- [ ] Não há `DISTINCT` corretivo.
- [ ] Regra de NULL está definida.

## Schema

- [ ] Nenhum atributo duplicado.
- [ ] Tipos conhecidos.
- [ ] Ordem final definida.
- [ ] Nulabilidade conhecida.
- [ ] Partição definida quando aplicável.

## Performance

- [ ] Gargalo foi localizado antes de tuning.
- [ ] Shuffle esperado conhecido.
- [ ] Skew avaliado.
- [ ] Spill interpretado corretamente.
- [ ] Broadcast é consciente.
- [ ] Cache possui reuso real.
- [ ] Partições têm justificativa.

## Escrita

- [ ] Chave validada.
- [ ] Schema validado.
- [ ] Cardinalidade validada.
- [ ] Resultado vazio tratado.
- [ ] Idempotência confirmada.
- [ ] Readback previsto.
- [ ] Destino correto confirmado.
- [ ] Modo de escrita confirmado.

## Pós-execução

- [ ] Carga fechou com cardinalidade esperada.
- [ ] Caches foram liberados.
- [ ] Sumário de execução foi registrado.
- [ ] Desvios foram documentados.
- [ ] Regra e target foram atualizados quando necessário.

---

# 26. As 25 regras que devem ser lembradas de cabeça

1. **Ambiente primeiro.**
2. **Contrato antes do código.**
3. **`schema.tabela` sempre explícito.**
4. **Nome físico nunca é inferido.**
5. **Fonte gigante só com recorte.**
6. **Filtro cedo.**
7. **Seleção de atributos cedo.**
8. **Join só com cardinalidade conhecida.**
9. **Join termina com schema limpo.**
10. **Atributo canônico nunca duplica.**
11. **`DISTINCT` não corrige modelagem.**
12. **Chave nula é decisão, não detalhe.**
13. **Schema final é contrato.**
14. **Data de referência é explícita.**
15. **Pipeline precisa ser idempotente.**
16. **Driver não recebe volume grande.**
17. **Cache só com reuso.**
18. **Checkpoint só com causa.**
19. **Query antes de recurso.**
20. **Shuffle precisa ser esperado.**
21. **Skew é problema de distribuição.**
22. **Broadcast só com estrutura realmente pequena.**
23. **Escrita só depois dos gates.**
24. **Readback prova persistência.**
25. **Regra de negócio nunca muda silenciosamente.**

---

# 27. Regra final

O erro mais perigoso em Engenharia de Dados não é a exception.

É o pipeline:

```text
executar
terminar
gravar
```

e estar semanticamente errado.

Por isso, a engenharia pronta para produção exige:

```text
AMBIENTE EXPLÍCITO
+
FONTE EXPLÍCITA
+
GRÃO EXPLÍCITO
+
CHAVE EXPLÍCITA
+
JOIN EXPLÍCITO
+
SCHEMA CONTROLADO
+
VALIDAÇÃO BLOQUEANTE
+
ESCRITA IDEMPOTENTE
+
OBSERVABILIDADE
+
REGRA DE NEGÓCIO RASTREÁVEL
```

Se qualquer um desses elementos estiver implícito em uma etapa crítica, o pipeline ainda não está pronto para produção.
