# Radar Financeiro — Perfil, Movimentações, Reconciliação e Classificação

## 1. Propósito e limites

Este documento apresenta, em linguagem de negócio, como o Radar Financeiro interpreta o perfil financeiro e transforma movimentações em fatos financeiros classificados.

O conteúdo está organizado em quatro camadas:

1. perfil financeiro recebido pelo Radar;
2. movimentações observadas;
3. neutralização de transferências entre contas próprias;
4. classificação das movimentações que permanecem efetivas.

As definições são declarativas. Quando o dado comprova um efeito, mas não comprova uma interpretação empresarial, o limite é informado expressamente. Não são criados significados a partir de nomes técnicos.

## 2. Perfil financeiro

### 2.1 Síntese comportamental consumida pelo Radar

O perfil financeiro é uma síntese comportamental produzida por outra área do banco. O Radar não calcula nem reclassifica esse perfil: recebe o resultado atribuído ao cliente e o utiliza como contexto do diagnóstico.

Clientes diferentes podem possuir sínteses com datas de referência diferentes. Um cliente pode ter uma síntese referenciada em abril e outro em julho. Essa diferença é preservada porque informa o momento ao qual a leitura comportamental está associada.

O Radar procura a síntese mais recente cuja data de referência não seja posterior à data da análise. Essa escolha cumpre dois objetivos:

- usar o contexto comportamental mais atual disponível para o cliente;
- impedir que uma informação referenciada no futuro seja aplicada a uma análise anterior.

A data não aumenta nem reduz uma pontuação por ser mais nova ou mais antiga. Ela seleciona qual síntese pode ser usada e informa a atualidade dessa síntese.

### 2.2 `DT_REF_PRFL`

**Nome de negócio:** Data de referência do perfil financeiro.

**Significado:** Data associada pela área produtora à síntese comportamental recebida para o cliente.

**Motivo de existência:** Permite identificar a referência temporal do macroperfil e do microperfil utilizados no diagnóstico.

**Utilização:** Entre as sínteses não posteriores à análise, o Radar utiliza a de maior data de referência.

**Significado de nulo:** Não existe perfil financeiro elegível para o cliente na data analisada.

**Necessidade na apresentação:** Deve acompanhar o perfil, preferencialmente com o rótulo “Data de referência do perfil financeiro”. Não deve ser apresentada como data de cálculo, publicação ou observação, pois esses eventos não são comprovados pelo dado disponível.

**Classificação:** Contexto.

**Observação importante:** A data pertence à síntese recebida. Não é produzida pelo Radar e não representa a data de execução do diagnóstico.

### 2.3 Macroperfil financeiro

O macroperfil é o nível mais amplo da síntese comportamental. Ele representa uma leitura consolidada recebida de outra área e funciona como contexto do cliente para a priorização temática.

O macroperfil é uma característica atribuída ao cliente pela síntese externa, e não uma interpretação criada a partir das movimentações do Radar. O Radar apenas aplica o código recebido à regra de prioridade correspondente.

O domínio reconhecido possui três resultados:

| Código | Macroperfil | Interpretação autorizada no Radar |
|---:|---|---|
| 1 | Endividado | Rótulo da síntese comportamental recebida. Influencia a prioridade dos temas conforme a regra de perfil. |
| 2 | Equilibrista | Rótulo da síntese comportamental recebida. Influencia a prioridade dos temas conforme a regra de perfil. |
| 3 | Investidor | Rótulo da síntese comportamental recebida. Influencia a prioridade dos temas conforme a regra de perfil. |

Os nomes não autorizam, isoladamente, afirmar nível de dívida, patrimônio, inadimplência, estabilidade, propensão futura ou qualquer critério usado pela área produtora. Esses critérios não fazem parte dos dados consumidos pelo Radar.

O perfil influencia a prioridade porque acrescenta ao comportamento observado no ciclo um contexto comportamental já atribuído ao cliente. Assim, uma mesma distribuição financeira pode receber pesos temáticos diferentes conforme o macroperfil recebido. Essa influência não significa que o Radar tenha recalculado ou validado a síntese externa.

### 2.4 `CD_MAC_PRFL_CLI` e `NM_MAC_PRFL_CLI`

`CD_MAC_PRFL_CLI` é o código que determina qual regra de perfil pode ser aplicada. `NM_MAC_PRFL_CLI` é o nome informativo recebido na mesma síntese.

O código é o atributo funcional. O nome permite que uma pessoa compreenda o perfil sem interpretar códigos numéricos. Ambos devem se referir à mesma linha e à mesma data de referência.

Quando o código está nulo, o Radar não possui macroperfil utilizável. Quando o código está fora do domínio reconhecido, ele é preservado como dado recebido, mas não pode dirigir a priorização dependente de perfil.

### 2.5 Microperfil financeiro

O microperfil é um contexto complementar mais detalhado da síntese recebida. Ele ajuda a descrever o cliente com maior granularidade, mas não participa das pontuações e não interfere na completude ou no tema vencedor.

`CD_MIC_PRFL_CLI` preserva o código recebido e `NM_MIC_PRFL_CLI` preserva seu nome. O Radar não deriva um do outro nem atribui significado a códigos ou nomes não explicados pela área produtora.

Uma apresentação como a seguinte é adequada:

```text
Perfil utilizado: Investidor
Detalhamento recebido: Acelerado
Data de referência do perfil financeiro: 31/07/2026
```

O termo “detalhamento recebido” é preferível a uma afirmação de que o microperfil explica ou causa o macroperfil. O vínculo conceitual exato entre os dois níveis pertence à metodologia da área produtora.

Vale a pena mostrar o microperfil porque ele amplia o contexto disponível para atendimento e orientação. A apresentação deve deixar claro que se trata de informação complementar, sem efeito no resultado calculado pelo Radar.

### 2.6 Ausência e ambiguidade de perfil

Na ausência de perfil, deixam de ser conhecidos:

- o macroperfil comportamental recebido;
- o detalhamento de microperfil;
- a data de referência desses dois resultados.

As movimentações, sua reconciliação e sua classificação continuam existindo. O que fica indisponível é a parcela do diagnóstico que depende do contexto de macroperfil. Por isso, as quatro prioridades de Gestão de Orçamento, Consumo Planejado, Formação de Reserva e Uso Consciente do Crédito ficam incompletas. Categorização dos Gastos possui tratamento próprio e não depende do macroperfil.

Quando existem duas ou mais sínteses na maior data de referência elegível, não é possível escolher univocamente qual perfil representa o cliente naquela data. Aceitar uma linha arbitrariamente poderia aplicar outro macroperfil e mudar a prioridade temática. Essa ambiguidade é bloqueante.

A explicação empresarial adequada é:

> Não foi possível determinar univocamente o perfil financeiro vigente na data de referência mais recente.

Ausência e ambiguidade não são equivalentes. Ausência permite continuar sem o componente de perfil; ambiguidade apresenta resultados concorrentes e impede uma escolha confiável.

## 3. Movimentações financeiras

### 3.1 O que o Radar considera uma movimentação relevante

Uma movimentação financeira relevante para o Radar é um registro válido associado ao cliente, datado dentro do ciclo ou de seu contexto de reconciliação, com natureza contábil reconhecida e, no caso de débito, marcado como valor visível para consumo.

Essa definição forma o universo de leitura. Para se tornar fato financeiro efetivo do ciclo, a movimentação também precisa:

- estar dentro da janela oficial;
- não ser neutralizada pela reconciliação;
- conservar sua natureza, moeda e valor original para a classificação posterior.

Movimentações externas à janela não pertencem ao ciclo. Elas existem apenas como possíveis evidências para reconciliar uma movimentação oficial próxima à borda.

### 3.2 `NR_TRAN_INST_PCT`

**Nome de negócio:** Identificador da movimentação.

**Significado:** Identificador técnico usado para distinguir e rastrear uma linha específica.

**Motivo de existência:** Permite formar pares de reconciliação, impedir que uma linha seja consumida mais de uma vez e relacionar o fato aos detalhes de apresentação.

**Utilização:** Participa da seleção determinística das linhas neutralizadas e da rastreabilidade do detalhe. Depois de concluída a reconciliação, não participa da interpretação financeira nem das fórmulas do diagnóstico.

**Significado de nulo:** Uma linha sem identificador não pode ser consumida por um par de reconciliação, pois não há como garantir sua unicidade.

**Necessidade na apresentação:** Deve ficar restrito ao detalhe técnico, à rastreabilidade ou à auditoria. Não agrega significado ao resumo executivo.

**Classificação:** Técnico.

### 3.3 `DT_TRAN`

**Nome de negócio:** Data da movimentação.

**Significado:** Data econômica usada para posicionar a movimentação no tempo.

**Motivo de existência:** Determina se o fato pertence ao ciclo oficial, ao contexto anterior ou ao contexto posterior.

**Utilização:** Define a participação temporal no ciclo e a distância em dias entre possíveis contrapartes de borda.

**Significado de nulo:** A linha não possui evidência temporal suficiente para formar um par de reconciliação e não pode ser corretamente posicionada na análise.

**Necessidade na apresentação:** Deve ser exibida como “Data da movimentação”.

**Classificação:** Fato financeiro.

**Observação importante:** `DT_TRAN` pode ser diferente do momento de inclusão do registro na fonte. A primeira posiciona economicamente a movimentação; o segundo informa quando o registro foi disponibilizado.

### 3.4 `CD_NTZ_CTB_TRAN`

**Nome de negócio:** Natureza contábil da movimentação.

Os valores reconhecidos são:

| Código | Nome humano | Leitura usual |
|:---:|---|---|
| C | Crédito | Valor creditado na conta, normalmente associado a uma entrada. |
| D | Débito | Valor debitado da conta, normalmente associado a uma saída. |

Crédito e débito descrevem a direção contábil. Eles não explicam sozinhos a finalidade econômica da movimentação. Um crédito pode representar renda, restituição ou resgate; um débito pode representar consumo, obrigação, aplicação ou outro uso.

Na apresentação, “Crédito — entrada na conta” e “Débito — saída da conta” são explicações úteis, desde que a natureza e o sinal do valor permaneçam visíveis. A tradução não autoriza corrigir, inverter ou ignorar um sinal inesperado.

### 3.5 `VL_TRAN` e o significado do sinal

**Nome de negócio:** Valor registrado da movimentação.

**Significado:** Importância monetária preservada exatamente com o sinal recebido.

O Radar não aplica valor absoluto, não inverte sinais e não corrige valores negativos. Portanto, tanto um crédito quanto um débito podem chegar com valor negativo, pois não existe uma regra de entrada que proíba essa combinação.

Natureza e sinal são dimensões diferentes:

- a natureza informa se o lançamento foi registrado como crédito ou débito;
- o sinal informa o valor literal associado ao lançamento.

Na apresentação humana, devem aparecer juntos. Um valor negativo não deve ser silenciosamente transformado em positivo nem reinterpretado como natureza oposta.

Quando os valores são posteriormente reunidos por tema, o negócio deve entender que os registros foram somados literalmente. Um sinal negativo pode reduzir o total de sua própria natureza ou classe e produzir uma leitura contraintuitiva; isso é consequência da preservação do fato recebido, não de uma normalização do Radar.

### 3.6 `CD_CTGR_TRAN_OGNL`

**Nome de negócio:** Categoria original da movimentação.

**Significado:** Código de categoria que já chega associado à movimentação antes da interpretação temática do Radar.

**Origem conceitual:** É uma classificação anterior ao Radar. O Radar não cria esse código; usa-o como insumo de seu mapa. Os dados disponíveis não identificam qual mecanismo ou etapa específica atribuiu a categoria original, portanto essa autoria não deve ser inventada.

A categoria descreve o tipo ou a finalidade atribuída ao lançamento na origem, como salário, supermercado, aluguel, aplicação ou transferência. Ela ainda não é a Classe Radar.

A categoria é combinada com a natureza contábil para validar a direção esperada. O mapa atual não possui um mesmo código de categoria classificado simultaneamente como crédito e débito. Assim, a combinação não escolhe entre duas classes para o mesmo código; ela impede um casamento incorreto quando a natureza observada diverge da natureza prevista.

Exemplo:

```text
Categoria Salário + natureza C → casamento com Renda
Categoria Salário + natureza D → classificação Radar não encontrada
```

Não existe, no conjunto vigente, um exemplo real em que o mesmo código mude de classe apenas por alternar entre C e D. Criar esse exemplo seria inventar uma combinação inexistente.

### 3.7 `CD_TIP_MOE_CRR`

**Nome de negócio:** Moeda da movimentação.

**Significado:** Código da moeda em que o valor da movimentação foi registrado.

O fato é preservado quando a moeda não é BRL para manter rastreabilidade e transparência sobre o universo observado. Entretanto, ele não deve ser combinado diretamente com valores em reais, pois o Radar não aplica conversão cambial. Preservar o registro e não somá-lo aos valores em BRL evita misturar grandezas monetárias não comparáveis.

Na apresentação, moeda e valor devem aparecer juntos. O código da moeda não deve ser omitido quando houver possibilidade de valores não expressos em reais.

### 3.8 `TX_DCR_TRAN_OGNL`

**Nome de negócio:** Descrição original da movimentação.

**Significado:** Texto reconhecível que acompanha a própria transação e ajuda a identificar o recebimento, compra ou lançamento observado.

**Motivo de existência:** Categoria e classe resumem a interpretação; a descrição preserva o detalhe que permite responder “que movimentação foi essa?”.

**Utilização:** É informação central no detalhamento e na explicação de pares reconciliados. Não determina classe, orçamento ou prioridade.

**Necessidade na apresentação:** Deve ocupar posição central no drill-down, acompanhada de data, natureza, banco, valor e moeda. No resumo executivo, pode permanecer oculta até que a pessoa abra o detalhe.

**Classificação:** Informação explicativa.

### 3.9 `NR_MCA_PCT_OPB`

**Nome de negócio:** Código do banco da movimentação.

**Significado:** Identifica numericamente o banco associado à conta em que a movimentação foi observada.

Exemplos conhecidos:

```text
145       = Nubank
999999999 = Banco do Brasil
```

O Radar trabalha com o código e não depende de um de-para para nome do banco. A apresentação deve usar “Código do banco”, evitando rótulos ambíguos como “marca” ou “pacote”. Quando houver um nome conhecido fora do motor, ele pode acompanhar o código, mas não deve substituí-lo sem um cadastro confiável.

As contas representadas nesse universo pertencem ao cliente analisado. O código informa em qual banco está a conta do lançamento; ele não informa o banco destinatário de uma transferência.

Esse atributo é empresarialmente necessário para distinguir possíveis transferências entre contas próprias mantidas em bancos diferentes. Também é útil no detalhe da movimentação e na explicação da reconciliação.

### 3.10 `IN_VSLO_CSM`

**Nome de negócio:** Indicador de valor visível para consumo.

**Significado:** Nos débitos, distingue o valor que representa a saída de consumo considerada no período de uma representação total da operação que não deve ser contada junto com suas parcelas.

Exemplo de compra parcelada:

```text
Compra de R$ 1.000 dividida em 10 parcelas

R$ 1.000,00 — IN_VSLO_CSM = N → valor total da operação, não considerado como saída do ciclo
R$   100,00 — IN_VSLO_CSM = S → parcela considerada como saída de consumo
```

Considerar simultaneamente o total de R$ 1.000 e a parcela de R$ 100 superestimaria o consumo. Por isso, somente débitos com indicador `S` entram no universo lido pelo Radar.

Os créditos não recebem esse filtro porque a regra trata especificamente a duplicidade de representação do consumo parcelado nos débitos. O indicador não deve ser traduzido simplesmente como “aparece ou não aparece no aplicativo”; seu papel negocial é identificar qual representação do débito deve ser considerada como consumo.

## 4. Reconciliação de transferências entre contas próprias

### 4.1 Fenômeno financeiro neutralizado

A reconciliação procura identificar transferências de dinheiro entre contas que pertencem ao mesmo cliente em bancos diferentes.

Quando R$ 500 saem de uma conta do cliente no banco A e R$ 500 entram em outra conta do mesmo cliente no banco B, o patrimônio financeiro apenas mudou de localização. Interpretar o débito como consumo e o crédito como nova renda distorceria o diagnóstico.

O código do banco presente na movimentação identifica onde cada lado foi observado, mas não informa diretamente o destino da saída. Por isso, o Radar infere a transferência própria ao encontrar duas linhas compatíveis.

A regra empresarial exige:

- mesmo cliente;
- mesmo valor;
- mesma moeda;
- naturezas contábeis opostas;
- códigos de banco conhecidos e diferentes;
- compatibilidade temporal exata ou de borda.

Uma entrada e uma saída do mesmo banco não representam, para essa regra, transferência entre contas próprias e não devem ser reconciliadas. Se um dos códigos de banco estiver nulo, também não existe evidência suficiente para formar o par.

O negócio aceita o risco de que duas movimentações independentes coincidam nesses atributos. Dentro dessa premissa, o par é tratado como prova conclusiva para o diagnóstico, embora os dados não demonstrem por si mesmos o vínculo operacional entre os lançamentos.

A explicação curta é:

> A reconciliação neutraliza entradas e saídas compatíveis entre contas do próprio cliente em bancos diferentes, evitando tratar uma transferência interna como renda ou consumo.

### 4.2 Alerta crítico de aderência

> **ALERTA CRÍTICO — CORREÇÃO PRIORITÁRIA**
>
> A regra empresarial exige dois códigos de banco conhecidos e diferentes em todo par exato ou de borda. O processamento vigente ainda não utiliza o código do banco como condição de pareamento. Como consequência, uma entrada e uma saída do mesmo banco podem ser neutralizadas indevidamente.
>
> Essa lacuna pode retirar fatos financeiros legítimos do diagnóstico e deve ser corrigida com prioridade máxima. Até a correção, a reconciliação executada não atende integralmente à definição empresarial descrita neste documento.

O alerta registra uma diferença entre a decisão empresarial e o comportamento efetivamente aplicado. Ele não afirma que a exigência de bancos distintos já esteja implementada.

### 4.3 Par exato

Um par exato representa duas linhas do mesmo cliente que possuem:

- a mesma data de movimentação;
- o mesmo valor literal;
- a mesma moeda;
- naturezas opostas, uma C e outra D;
- a mesma condição temporal, ambas oficiais ou ambas externas;
- pela regra empresarial, bancos conhecidos e diferentes.

Economicamente, essa combinação é interpretada como saída de uma conta própria e entrada em outra conta própria no mesmo dia.

A categoria não participa da chave porque os dois lados podem chegar com descrições ou categorias diferentes. A neutralização procura a transferência patrimonial entre bancos, não a igualdade da classificação atribuída separadamente a cada lançamento.

É correto dizer que os dois lançamentos “se anulam para efeito do diagnóstico”. Uma formulação ainda mais específica é:

> Os dois lançamentos são neutralizados porque representam uma transferência entre contas próprias, e não geração ou consumo de recursos.

Cada par exato corresponde a duas linhas: um crédito e um débito. Assim, “2 pares exatos neutralizados” significa quatro linhas neutralizadas. Essa quantidade pode aparecer em uma explicação de reconciliação, desde que a relação entre pares e linhas fique clara.

As quantidades de créditos, débitos, posições e pares usadas para escolher quais identificadores serão consumidos são mecanismos técnicos. Não precisam aparecer no HTML executivo. O resumo pode exibir o número de pares; o detalhe pode mostrar as duas linhas de cada par.

O pareamento exato é mantido dentro do mesmo universo temporal para não confundir fatos do ciclo com evidências externas. Linhas oficiais são neutralizadas com linhas oficiais; linhas externas podem ser consumidas entre si para não serem reutilizadas, mas não se tornam fatos do ciclo.

### 4.4 Reconciliação de borda

A reconciliação de borda trata a diferença operacional de data entre os dois lados de uma transferência própria. Uma instituição pode registrar um lado perto do encerramento do ciclo e a contraparte aparecer no outro banco poucos dias antes ou depois da janela.

Um par de borda possui:

- uma linha dentro do ciclo e outra fora dele;
- mesmo cliente, valor e moeda;
- naturezas opostas;
- diferença de um a cinco dias corridos;
- pela regra empresarial, bancos conhecidos e diferentes.

O limite de cinco dias é operacional. Ele define até onde uma contraparte externa é aceita como evidência temporal da transferência. Diferença de zero dia pertence ao casamento exato; diferença superior a cinco dias não é reconciliada.

No par de borda:

- a linha interna deixa de representar um fato financeiro efetivo do ciclo;
- a linha externa serve exclusivamente como evidência da contraparte;
- a linha externa nunca passa a integrar o ciclo, seus valores ou suas quantidades.

Uma apresentação adequada é:

> Movimento do ciclo neutralizado por contraparte localizada em outro banco, dois dias antes da janela.

Vale informar tanto o limite de “até cinco dias” na explicação da regra quanto a distância efetivamente encontrada no detalhe do par.

### 4.5 Ordem e escolha dos pares

O casamento exato ocorre antes da reconciliação de borda porque a coincidência no mesmo dia é a evidência temporal mais forte. Somente o que não foi consumido nessa primeira etapa pode procurar uma contraparte com tolerância de data.

A leitura empresarial é:

> Primeiro são neutralizadas as evidências mais fortes; depois o resíduo é analisado com tolerância temporal operacional.

Quando existem várias combinações possíveis na borda, a escolha segue três prioridades:

1. formar a maior quantidade possível de pares, para explicar o maior número de transferências próprias compatíveis;
2. escolher a menor distância total em dias, privilegiando contrapartes temporalmente mais próximas;
3. usar a menor combinação ordenada de identificadores como desempate exclusivamente técnico e determinístico.

Nenhuma linha pode participar de mais de um par. Depois de consumido, seu identificador deixa de estar disponível para outra reconciliação.

### 4.6 Movimento oficial bruto e movimento efetivo

**Movimento oficial bruto** é toda movimentação relevante localizada dentro do ciclo antes da reconciliação.

**Movimento neutralizado** é uma linha oficial interpretada como parte de uma transferência entre contas próprias e retirada do diagnóstico financeiro.

**Movimento efetivo** é um movimento oficial que não foi consumido por par exato nem por par de borda.

Uma formulação empresarial precisa é:

> O Radar leva adiante como fato financeiro efetivo somente o que permaneceu no ciclo depois das neutralizações.

“Efetivo” não significa automaticamente que a linha participará de toda medida posterior. Moeda e classificação ainda determinam como esse fato poderá ser interpretado. A reconciliação responde apenas se a linha permanece como fato do ciclo.

## 5. Mapa de categorias e classificação

### 5.1 Papel do mapa

O mapa transforma a categoria original e a natureza contábil em uma interpretação financeira própria do Radar. Ele organiza cada casamento em grupo, categoria legível, informação de imposto de renda, Classe Radar e indicadores de participação.

O mapa possui 70 registros e 12 atributos:

| Atributo | Significado empresarial |
|---|---|
| `TIPO` | Natureza contábil esperada: C, D ou nula. |
| `CD_GRUPO` | Código do agrupamento do catálogo. |
| `TX_GRUPO` | Nome do agrupamento do catálogo. |
| `CD_CATEGORIA` | Código de categoria usado como chave do mapa. |
| `TX_CATEGORIA` | Nome humano da categoria. |
| `CD_IR` | Código informativo de tratamento no imposto de renda. |
| `TX_IR` | Descrição informativa desse tratamento. |
| `CD_CLASS_RADAR` | Código da interpretação temática atribuída pelo Radar. |
| `TX_CLASS_RADAR` | Nome dessa interpretação temática. |
| `IN_AGRO` | Indicador de tratamento específico reservado ao domínio correspondente. |
| `IN_PARTICIPA_CALCULO` | Indica participação na composição temática. |
| `IN_PARTICIPA_ORCAMENTO` | Indica participação na leitura orçamentária. |

O casamento exige simultaneamente:

```text
categoria original da movimentação = categoria do mapa
natureza da movimentação = tipo do mapa
```

Essa chave composta impede que uma categoria seja interpretada em direção contábil incompatível.

### 5.2 Grupo, categoria e Classe Radar

**Grupo** é uma camada de organização do catálogo, como Casa, Saúde, Alimentação, Transporte ou Investimentos. Ele permite navegar e reunir categorias relacionadas. Não dirige, por si só, os cálculos temáticos.

**Categoria** é o nome mais específico e reconhecível da finalidade atribuída à movimentação, como Água, Salário, Supermercado ou Aplicação. `TX_CATEGORIA` é o melhor rótulo humano para apresentar essa classificação, acompanhado da descrição original quando houver necessidade de detalhe.

`CD_CTGR_TRAN_OGNL` e `CD_CATEGORIA` pertencem ao mesmo domínio de códigos, mas têm papéis de linhagem diferentes:

- `CD_CTGR_TRAN_OGNL` vem associado ao fato observado;
- `CD_CATEGORIA` é a chave de referência existente no mapa.

`CD_CATEGORIA` não é uma “versão Radar” da categoria original. Ele é o valor de referência usado para verificar se o código recebido possui um casamento reconhecido.

**Classe Radar** é a interpretação financeira que organiza uma movimentação em uma classe de entrada ou de saída usada pela leitura temática do produto.

A Classe Radar não substitui o grupo nem a categoria:

- o grupo organiza o catálogo;
- a categoria explica o tipo específico de movimentação;
- a classe traduz essa categoria para o papel financeiro relevante ao Radar.

No HTML, a categoria e a Classe Radar são mais úteis no drill-down. O grupo pode organizar a navegação. Códigos devem permanecer em detalhe técnico, enquanto nomes servem à leitura humana.

### 5.3 Informação de imposto de renda

`IR` significa imposto de renda. O código e o texto registram se a categoria possui associação informativa com pagamentos efetuados, bens e direitos, dívidas e ônus reais, doações ou nenhuma dessas classificações.

Essa informação existe como característica do catálogo, mas não interfere na interpretação temática vigente. Ela não define orçamento, prioridade ou vencedor.

No produto atual, deve aparecer somente quando houver valor explicativo para um detalhe fiscal ou para rastreabilidade. Não precisa ocupar o resumo executivo e não deve ser apresentada como orientação tributária.

### 5.4 Relação entre classes e temas

As classes de entrada descrevem a origem financeira atribuída aos créditos. As classes de saída descrevem a destinação atribuída aos débitos.

As cinco classes de saída correspondem às cinco dimensões temáticas da distribuição financeira:

| Classe de saída | Dimensão temática |
|---|---|
| Indeterminado | Categorização dos Gastos |
| Essenciais | Gestão de Orçamento |
| Não Essenciais | Consumo Planejado |
| Futuro | Formação de Reserva |
| Obrigações | Uso Consciente do Crédito |

As classes de entrada formam a explicação dos créditos observados, mas não constituem cinco temas concorrentes de prioridade.

### 5.5 Classe 0 — Outras Entradas

**Representação financeira:** Classe prevista para créditos que seriam reconhecidos como entrada, mas não pertenceriam a Renda, Estorno, Resgate ou Crédito.

**Motivo de separação:** Mantém um espaço conceitual para outras origens de recursos sem misturá-las com classes específicas.

**Situação vigente:** As linhas próprias dessa classe possuem natureza nula e não casam com movimentações C ou D. Portanto, nenhuma movimentação reconhecida produz atualmente uma entrada temática nessa classe.

**Participação:** O texto também é usado como fallback técnico para movimentos sem casamento, mas nesses casos os indicadores de participação são `N`. Esse fallback não transforma um débito em entrada.

**Explicação ao negócio:** “Classe prevista para outras entradas reconhecidas; sem movimentação classificável no conjunto atual.”

### 5.6 Classe 1 — Renda

**Representação financeira:** Créditos reconhecidos como recursos recebidos, como salário, vale-alimentação, bonificação e outros rendimentos.

**Motivo de separação:** Distingue recebimentos associados a renda de restituições, resgates patrimoniais e outras entradas.

**Participação:** Depende dos indicadores da categoria. A classe sozinha não autoriza inclusão automática em toda leitura.

**Explicação ao negócio:** “Recursos recebidos e classificados como renda na origem do movimento.”

Renda classificada em movimentações não é sinônimo de renda presumida. A primeira é um crédito observado; a segunda é uma estimativa de capacidade financeira obtida em fonte própria.

### 5.7 Classe 2 — Estorno

**Representação financeira:** Crédito que devolve ou restitui um valor, em vez de representar renda recorrente nova. No mapa vigente, essa classe é materializada pela restituição de imposto de renda.

**Motivo de separação:** Evita misturar devoluções e restituições com renda habitual.

**Participação:** A categoria atualmente associada participa da composição temática e da leitura orçamentária.

**Explicação ao negócio:** “Valor creditado como devolução ou restituição, separado da renda.”

O nome da classe não autoriza afirmar que todo crédito de natureza reversora será reconhecido como Estorno. O casamento continua dependente da categoria prevista no mapa.

### 5.8 Classe 3 — Resgate

**Representação financeira:** Crédito decorrente do resgate de um recurso que já pertencia ao cliente sob a forma de investimento.

**Motivo de separação:** Resgatar converte patrimônio investido em saldo disponível; não cria renda nova.

**Participação:** Participa da composição temática das entradas, mas não do orçamento.

**Explicação ao negócio:** “Retorno à conta de um valor que já fazia parte do patrimônio investido do cliente.”

### 5.9 Classe 4 — Crédito

**Representação financeira:** Classe reservada no modelo para uma modalidade de entrada distinta das demais.

**Motivo de separação:** Preserva uma posição no domínio de classes de entrada.

**Participação:** Nenhuma das 70 categorias está atualmente associada a essa classe. Consequentemente, não existe conteúdo negocial observável que permita definir sua origem com segurança.

**Explicação ao negócio:** “Classe reservada, ainda sem categoria associada.”

Essa classe não deve ser confundida com natureza contábil C. Natureza C descreve qualquer lançamento creditado; a Classe Crédito seria uma interpretação específica dentro dos créditos, mas ainda não possui materialização no mapa.

### 5.10 Classe 5 — Indeterminado

**Representação financeira:** Débito reconhecido pelo mapa cuja finalidade não é distribuída entre Essenciais, Não Essenciais, Futuro ou Obrigações.

**Motivo de separação:** Permite tratar conscientemente despesas de finalidade ampla ou insuficientemente específica, como gastos diversos, saque, cheque, transferência e boletos diversos.

**Participação:** As categorias ordinárias dessa classe participam da composição temática e do orçamento quando seus indicadores são `S`.

**Explicação ao negócio:** “Saída reconhecida, mas sem informação suficiente para atribuí-la a um tema financeiro mais específico.”

Indeterminado é uma classe válida e intencional. Não é sinônimo de movimentação sem classificação. Uma linha indeterminada encontrou o mapa; uma linha sem classificação não encontrou casamento algum.

### 5.11 Classe 6 — Essenciais

**Representação financeira:** Despesas associadas à manutenção das necessidades correntes da pessoa ou da família, como moradia, serviços básicos, saúde, alimentação e outros itens classificados dessa forma no mapa.

**Motivo de separação:** Identifica a parcela da capacidade financeira destinada à sustentação da vida cotidiana.

**Participação:** As categorias dessa classe participam da composição temática e do orçamento conforme seus indicadores.

**Explicação ao negócio:** “Gastos necessários para manter as necessidades correntes.”

### 5.12 Classe 7 — Não Essenciais

**Representação financeira:** Despesas de consumo discricionário ou ajustável, como lazer, presentes, vestuário e outras categorias classificadas dessa forma.

**Motivo de separação:** Permite observar a parcela de recursos destinada a escolhas de consumo que, em geral, possuem maior possibilidade de planejamento.

**Participação:** As categorias dessa classe participam da composição temática e do orçamento conforme seus indicadores.

**Explicação ao negócio:** “Gastos de consumo planejável que não foram classificados como necessidades correntes ou compromissos financeiros.”

O rótulo não constitui julgamento moral sobre a compra nem afirma que o gasto seja desnecessário para a realidade individual do cliente.

### 5.13 Classe 8 — Futuro

**Representação financeira:** Recursos direcionados à construção ou à proteção da capacidade financeira futura, incluindo aplicação financeira e contribuição previdenciária classificada como GPS.

**Motivo de separação:** Distingue valores orientados a reserva, investimento ou proteção futura dos gastos de consumo corrente.

**Participação:** Participa da composição temática. A participação no orçamento depende da categoria: a contribuição previdenciária participa, enquanto a aplicação não participa.

**Explicação ao negócio:** “Recursos destinados à proteção e à capacidade financeira futura.”

Uma aplicação não é interpretada como saída orçamentária oficial porque o dinheiro continua pertencendo ao cliente sob outra forma patrimonial. Ainda assim, ela informa quanto foi direcionado ao Futuro e, por isso, participa da composição temática.

### 5.14 Classe 9 — Obrigações

**Representação financeira:** Compromissos patrimoniais, dívidas, prestações, encargos e serviços financeiros classificados pelo mapa.

**Motivo de separação:** Distingue compromissos financeiros assumidos de despesas necessárias à vida corrente e de consumo discricionário.

**Participação:** A maior parte das categorias participa da composição temática e do orçamento. Categorias explicitamente excluídas conservam a classificação, mas obedecem aos próprios indicadores de participação.

**Explicação ao negócio:** “Valores destinados a compromissos financeiros, patrimoniais ou de crédito já assumidos.”

A diferença central é:

```text
Essencial  → necessidade corrente de vida e manutenção
Obrigação  → compromisso financeiro, patrimonial ou contratual assumido
```

### 5.15 Participação na composição temática

`IN_PARTICIPA_CALCULO` informa se a movimentação classificada pode contribuir para a composição financeira de sua classe.

Em linguagem de negócio, o melhor rótulo é “Participa da composição temática”. A expressão “participa do tema” também pode ser usada no detalhe, desde que fique claro que:

- créditos contribuem para classes temáticas de entrada;
- débitos contribuem para as cinco classes temáticas de saída.

Quando o indicador vale `N`, a movimentação continua existindo e conserva sua classificação, mas não altera os valores atribuídos às distribuições temáticas.

### 5.16 Participação no orçamento

`IN_PARTICIPA_ORCAMENTO` informa se a movimentação compõe a leitura de recursos que entraram ou saíram efetivamente do orçamento.

Participação temática e participação orçamentária respondem a perguntas diferentes:

- composição temática: para qual finalidade financeira o valor foi direcionado;
- orçamento: o valor representa recurso novo ou consumo efetivo na leitura orçamentária?

Aplicação e resgate demonstram essa diferença:

| Movimento | Composição temática | Orçamento | Explicação |
|---|:---:|:---:|---|
| Aplicação | Sim, em Futuro | Não | O recurso mudou para uma forma investida, mas continua pertencendo ao cliente. |
| Resgate | Sim, em Resgate | Não | O recurso voltou do investimento para a conta, mas não é renda nova. |

No mapa vigente, existem combinações `S/S`, `S/N` e `N/N`. Não existe categoria configurada com participação temática `N` e participação orçamentária `S`. Portanto, não deve ser inventado um exemplo de movimento que entre no orçamento sem participar de alguma composição temática reconhecida.

### 5.17 Movimentação sem casamento no mapa

Uma movimentação sem casamento é um fato efetivo cuja combinação de categoria original e natureza não foi reconhecida pelas 70 chaves do mapa.

A expressão adequada é:

> Movimentação não reconhecida pelo mapa de classificação.

Essa linha:

- permanece disponível para rastreabilidade;
- conserva data, natureza, banco, moeda, descrição e valor;
- não participa da composição temática;
- não participa do orçamento;
- não deve receber uma interpretação financeira inventada.

O fallback técnico pode carregar os textos “Sem Categoria” e “Outras Entradas”, mas “Outras Entradas” não descreve empresarialmente uma linha sem casamento. Em especial, um débito continua sendo débito e nunca deve parecer que foi transformado em entrada.

A apresentação recomendada é:

```text
Natureza original: Débito
Classificação Radar: não encontrada
Categoria original: 999
Descrição original: <texto recebido>
```

Esse tratamento diferencia claramente:

- **Indeterminado:** a movimentação encontrou o mapa e recebeu uma classe válida;
- **não classificada:** a movimentação não encontrou uma chave compatível e ficou fora das participações.

## 6. Ordem da narrativa empresarial

A explicação do Radar não deve começar pela pontuação. Antes de apresentar qualquer prioridade, a narrativa precisa estabelecer:

```text
utilização recente
→ conta e ciclo analisados
→ capacidade financeira de referência
→ fatos financeiros oficiais
→ transferências próprias neutralizadas
→ fatos financeiros efetivos
→ significado e classificação das movimentações
→ prioridade de orientação
```

Essa ordem permite que a pessoa compreenda primeiro quais fatos foram observados, quais desapareceram por neutralização e como os fatos restantes foram interpretados. Somente então uma prioridade temática possui contexto suficiente.

## 7. Limites de interpretação

As definições deste documento não autorizam afirmar que:

- o perfil financeiro foi calculado pelo Radar;
- os nomes Endividado, Equilibrista e Investidor revelam critérios não fornecidos pela área produtora;
- o microperfil altera pontuação ou vencedor;
- a data de referência do perfil é necessariamente data de cálculo, publicação ou observação;
- o identificador da movimentação possui significado financeiro próprio;
- todo crédito é renda ou todo débito é consumo;
- um valor negativo deve ser convertido para positivo;
- a categoria original foi atribuída pelo Radar;
- o código do banco identifica o destino de uma transferência;
- movimentações no mesmo banco podem formar uma transferência própria válida;
- banco nulo é evidência suficiente de bancos diferentes;
- uma contraparte externa pertence ao ciclo;
- todo movimento efetivo participa da composição temática ou do orçamento;
- Indeterminado significa ausência de classificação;
- o fallback “Outras Entradas” transforma um débito sem casamento em entrada;
- aplicação representa perda do patrimônio do cliente;
- resgate representa geração de renda nova.

Esses limites preservam a diferença entre o fato observado, a interpretação financeira, a regra empresarial e a lacuna crítica ainda existente na reconciliação.
