# Radar Financeiro — Conceitos Negociais

## 1. Propósito deste documento

Este documento explica o Radar Financeiro para pessoas que conhecem clientes e finanças, mas não precisam conhecer sua implementação técnica.

Ele separa três camadas que não devem ser confundidas:

1. **conceito de negócio:** a história financeira que o Radar procura contar;
2. **regra vigente:** o comportamento objetivo aplicado aos dados;
3. **representação:** o que precisa ser mostrado para que a pessoa compreenda o resultado.

As explicações não criam novas regras. Quando um código possui efeito conhecido, mas não possui significado empresarial comprovado, ele é apresentado como técnico, sem receber uma interpretação inventada.

Esta primeira parte cobre:

- visão geral do produto;
- entrada e formação do público;
- CPF;
- conta corrente BB elegível;
- ciclo financeiro;
- janela oficial e contexto de leitura;
- renda presumida e bases financeiras.

## 2. Perguntas-mãe

### 2.1 Qual pergunta de negócio o Radar responde?

> Como a pessoa distribui sua renda presumida e o que essa distribuição revela sobre sua saúde financeira e sua prioridade de orientação?

O Radar observa movimentações reais, organiza essas movimentações em temas financeiros e compara as saídas com uma capacidade financeira de referência. A visão principal utiliza a renda presumida ajustada à quantidade de ciclos analisados.

“Saúde financeira”, neste contexto, não significa uma aprovação geral nem uma nota de crédito. Significa compreender:

- como os recursos foram distribuídos;
- quanto foi destinado a despesas, obrigações e formação de reserva;
- qual foi a relação entre saídas e a base financeira;
- qual tema deve receber primeiro a orientação financeira.

### 2.2 O que significa dizer que “tudo é calculado com renda presumida”?

Essa frase não se aplica literalmente a todo o Radar.

Na visão principal `RENDA_PRESUMIDA`, a renda presumida ajustada é usada como base para:

- o orçamento da visão;
- os percentuais dos cinco temas;
- as pontuações dependentes desses percentuais e do orçamento;
- a completude;
- o máximo, o empate e o tema vencedor.

Não dependem da renda presumida para existir:

- seleção e elegibilidade do cliente;
- CPF e conta;
- ciclo e janela;
- leitura das movimentações;
- reconciliação;
- classificação;
- quantidades de transações;
- valores temáticos de entradas e saídas;
- flags de moeda e Agro.

Portanto, a formulação correta é:

> A cadeia de diagnóstico dependente de base da visão principal usa a renda presumida; os fatos transacionais são formados independentemente dela.

### 2.3 Qual é o produto principal?

O produto principal é a visão `RENDA_PRESUMIDA`.

Ela procura responder como as saídas do cliente se relacionam com sua capacidade financeira estimada durante os ciclos analisados. A renda mensal encontrada é multiplicada pela quantidade de ciclos para manter base e movimentações no mesmo horizonte.

### 2.4 Qual é o papel de `ENTRADAS_REALIZADAS`?

`ENTRADAS_REALIZADAS` é uma comparação secundária entre:

- capacidade estimada, representada pela renda presumida; e
- créditos efetivamente observados no período, dentro das condições desse cenário.

Ela permite verificar como o diagnóstico se comporta quando a base deixa de ser a estimativa de renda e passa a ser a soma dos créditos efetivos, classificados e em BRL.

Não é uma nova classificação do cliente nem uma correção da renda presumida. É outra lente aplicada aos mesmos fatos financeiros.

### 2.5 O que representa o resultado oficial?

O resultado oficial é uma referência híbrida do contrato:

- os percentuais temáticos usam a renda presumida;
- o orçamento oficial compara entradas orçamentárias realizadas com saídas orçamentárias realizadas.

Consequentemente, ele não deve ser descrito como se todas as suas medidas utilizassem uma única base. Na visão principal `RENDA_PRESUMIDA`, a mesma renda presumida ajustada é aplicada ao orçamento e aos percentuais para formar uma leitura coerente sob essa base.

### 2.6 Qual é a diferença entre renda, entrada financeira e crédito?

**Renda presumida** é uma estimativa mensal de capacidade financeira obtida em uma fonte própria de renda. Ela não é a soma das movimentações da conta.

**Crédito** é uma direção contábil da movimentação. Indica um valor creditado na conta, mas não informa sozinho sua origem econômica. Um crédito pode ser salário, estorno, resgate, receita Agro ou outro recebimento.

**Entrada financeira** é um crédito interpretado pelo Radar dentro de uma finalidade. Dependendo da categoria, ele pode participar de um tema, do orçamento, dos dois ou de nenhum deles.

Assim:

```text
crédito na conta ≠ renda presumida
crédito na conta ≠ necessariamente renda
entrada realizada ≠ necessariamente entrada orçamentária
```

### 2.7 Renda de R$ 10 mil e créditos de R$ 30 mil: qual é a capacidade financeira?

Na visão principal, a capacidade financeira é a renda presumida ajustada ao período.

Se a renda presumida mensal for R$ 10 mil e `periodo = 1`, a base principal será R$ 10 mil. Os R$ 30 mil em créditos formarão a comparação `ENTRADAS_REALIZADAS`, desde que atendam às condições desse cenário.

Se `periodo = 3`, a mesma renda mensal será ajustada para R$ 30 mil, porque a análise cobre três ciclos. Esse ajuste não afirma que três registros mensais de renda foram encontrados; ele estende a mesma estimativa mensal ao horizonte analisado.

### 2.8 O que “orçamento” compara?

Na visão principal, orçamento compara:

```text
renda presumida ajustada ao período
versus
saídas orçamentárias realizadas
```

Na comparação `ENTRADAS_REALIZADAS`, usa-se a base de créditos realizados do cenário no lugar da renda presumida.

No resultado oficial, o orçamento compara entradas orçamentárias realizadas com saídas orçamentárias realizadas. Por isso, qualquer texto de apresentação precisa indicar qual base está ativa.

### 2.9 Existe diagnóstico sem renda presumida?

Sim, existe um diagnóstico parcial.

Ainda podem existir:

- cliente, CPF, conta, ciclo e perfil;
- janela financeira;
- movimentações efetivas;
- classificação;
- quantidades e valores temáticos;
- valores orçamentários realizados;
- flags de moeda e Agro.

Sem renda presumida, os percentuais que dependem dessa base não podem ser calculados. As pontuações finais ficam incompletas e não existe tema vencedor. Isso não apaga os fatos transacionais; significa que a cadeia completa de priorização não pôde ser concluída.

### 2.10 O que significa o tema vencedor?

Tema vencedor significa **prioridade de orientação**.

Ele indica o tema cuja pontuação final atingiu o maior valor e que, por isso, deve receber primeiro a atenção educativa. Não significa automaticamente:

- maior risco de crédito;
- pior comportamento;
- maior despesa absoluta;
- reprovação financeira.

Quando mais de um tema divide a maior pontuação, o resultado é empate. Quando a pontuação está incompleta, não existe tema vencedor.

### 2.11 Participação, dados suficientes, completude e vencedor são a mesma coisa?

Não.

| Conceito | Significado |
|---|---|
| Participar do Radar | O cliente foi selecionado e pertence à formação do público. |
| Possuir dados para uma etapa | A informação necessária àquela etapa está disponível. Isso pode variar entre CPF, conta, ciclo, renda e perfil. |
| Possuir fatos financeiros | Existe janela e podem existir movimentações, quantidades e valores, ainda que renda ou perfil estejam ausentes. |
| Pontuação completa | As cinco pontuações finais são não nulas. |
| Tema vencedor | A pontuação está completa e um tema, ou um empate, ocupa o máximo. |

Um cliente pode participar do Radar e ainda ter diagnóstico parcial.

### 2.12 O que significa `NULL`?

Depende da variável.

`NULL` pode significar:

- fonte não consultada porque uma pré-condição não foi atendida;
- registro não encontrado;
- valor não aplicável;
- ausência de base para cálculo;
- resultado permitido, porém indisponível.

`NULL` não significa automaticamente erro ou reprovação. Bloqueios contratuais interrompem o processamento e são diferentes de campos nulos permitidos.

Zero também não é ausência:

- `0` ou `0.00` significa valor calculável cujo resultado foi efetivamente zero;
- ausência de registro pode resultar em `NULL`, fallback ou bloqueio, conforme a etapa.

### 2.13 Qual história o negócio deve compreender em dois minutos?

A narrativa ideal é:

1. qual cliente foi analisado e quando ele foi observado utilizando o aplicativo;
2. qual conta corrente BB permitiu localizar seu ciclo;
3. quais ciclos financeiros foram analisados;
4. qual renda presumida foi usada como capacidade financeira;
5. quais movimentações realmente permaneceram após a reconciliação;
6. como essas movimentações foram distribuídas entre os temas;
7. o que essa distribuição revela sobre a saúde financeira;
8. qual tema representa a primeira prioridade de orientação;
9. como a leitura muda ao comparar renda presumida com entradas realizadas.

## 3. Bloco A — Entrada e formação do público

### 3.1 `HOJE`

**Nome de negócio:** Relógio da execução.

**O que significa:** Valor temporal fornecido ao processamento para determinar em que data o Radar está sendo executado.

**Por que existe:** Todas as referências de execução e formação do público precisam partir de uma data comum.

**Como é usada:** Seus primeiros dez caracteres formam `DATA_EXECUCAO`.

**O que significa quando está vazia, nula ou inválida:** As referências temporais não podem ser formadas e o processamento não pode continuar normalmente.

**O que o negócio precisa enxergar no HTML:** A data de execução, não o valor técnico bruto de `HOJE`.

**Classificação:** Contexto.

**Observação importante:** `HOJE` não é a data econômica de uma movimentação nem a data de referência da renda.

### 3.2 `DATA_EXECUCAO` / `DT_EXEA`

**Nome de negócio:** Data de execução do Radar.

**O que significa:** Data em que o diagnóstico foi produzido.

**Por que existe:** Define a referência temporal da execução, a formação recente do público e o limite de elegibilidade do perfil.

**Como é usada:** É derivada de `HOJE`; também origina `DT_MES_EXEA` e os limites da formação do público.

**O que significa quando está vazia ou nula:** A execução não possui referência temporal válida.

**O que o negócio precisa enxergar no HTML:** A data da fotografia analítica, apresentada como “Execução do Radar”.

**Classificação:** Contexto.

**Observação importante:** Não significa que todas as fontes tenham sido atualizadas nessa data.

### 3.3 `DT_MES_EXEA`

**Nome de negócio:** Competência mensal da execução.

**O que significa:** Primeiro dia do mês de `DATA_EXECUCAO`.

**Por que existe:** Permite identificar a competência mensal associada ao resultado, independentemente do dia exato de execução.

**Como é usada:** É armazenada no resultado final como referência mensal.

**O que significa quando está vazia ou nula:** É uma inconsistência, pois deve sempre ser derivável de uma data de execução válida.

**O que o negócio precisa enxergar no HTML:** Normalmente basta exibir a data de execução. A competência pode aparecer em detalhe técnico ou em usos mensais do resultado.

**Classificação:** Contexto.

**Observação importante:** Não define a janela financeira; a janela usa ciclos da conta.

### 3.4 `periodo`

**Nome de negócio:** Quantidade de ciclos analisados.

**O que significa:** Número de ciclos financeiros completamente fechados incluídos no diagnóstico.

**Por que existe:** Permite escolher a profundidade temporal da análise sem incluir o ciclo ainda aberto.

**Como é usada:** Aceita somente inteiros de `1` a `6`; determina o início da janela e multiplica a renda mensal pelo mesmo número de ciclos.

**O que significa quando vale 1, 2, ..., 6:** O Radar observa, respectivamente, um a seis ciclos fechados. Não significa meses-calendário obrigatoriamente, pois o ciclo pode começar em qualquer dia do mês.

**O que significa quando está vazio, nulo ou fora do domínio:** É entrada inválida e bloqueia a execução.

**O que o negócio precisa enxergar no HTML:** “Período considerado: N ciclos fechados”.

**Classificação:** Insumo.

**Observação importante:** O mesmo `periodo` alinha o horizonte das movimentações e da renda presumida ajustada.

### 3.5 `DATA_INICIAL_PUBLICO`

**Nome de negócio:** Início da observação de utilização recente.

**O que significa:** Limite inicial da janela usada para verificar se o cliente utilizou recentemente o aplicativo com inclusão de suas fontes.

**Por que existe:** O público é formado por clientes com inclusão de transação no mês-calendário anterior à execução.

**Como é usada:** Corresponde ao mesmo dia do mês anterior a `DATA_EXECUCAO`; quando o dia não existe no mês anterior, usa seu último dia. O limite é inclusivo.

**O que significa quando está vazia ou nula:** A janela de formação não pode ser definida.

**O que o negócio precisa enxergar no HTML:** O início do período consultado para formação do cliente.

**Classificação:** Regra.

**Observação importante:** Esta não é a data inicial das movimentações financeiras analisadas. Essa função pertence a `DT_REF_INI`.

### 3.6 `DATA_FINAL_EXCLUSIVA_PUBLICO`

**Nome de negócio:** Fim exclusivo da observação de utilização recente.

**O que significa:** Limite superior da janela de formação do público; é igual a `DATA_EXECUCAO`.

**Por que existe:** Evita incluir registros a partir do início da própria data de execução e forma um intervalo sem sobreposição na extremidade final.

**Como é usada:** A regra exige `TS_INCL_TRAN < DATA_FINAL_EXCLUSIVA_PUBLICO`.

**O que significa quando está vazia ou nula:** A janela de formação não pode ser definida.

**O que o negócio precisa enxergar no HTML:** A data final do período consultado. O detalhe “exclusivo” deve aparecer em explicação técnica, não necessariamente no resumo executivo.

**Classificação:** Regra.

**Observação importante:** O fim exclusivo significa que um registro exatamente nesse limite não pertence à formação desta execução.

### 3.7 `TS_INCL_TRAN`

**Nome de negócio:** Momento de inclusão das fontes na utilização do aplicativo.

**O que significa:** Literalmente, é o timestamp em que o registro foi incluído ou disponibilizado na fonte. No Radar, ele funciona como evidência de utilização recente do aplicativo com inclusão das fontes do cliente.

**Por que existe:** Permite formar o público recente e escolher a utilização mais atual observada.

**Como é usada:** Filtra a janela de formação; na seleção por CPF, também ordena os candidatos do mais recente para o mais antigo.

**O que significa quando está vazia ou nula:** A linha não satisfaz a elegibilidade temporal dependente desse timestamp.

**O que o negócio precisa enxergar no HTML:** A interpretação deve ser “última utilização observada com inclusão das fontes”, nunca “data da compra” ou “data econômica da transação”.

**Classificação:** Regra.

**Observação importante:** `TS_INCL_TRAN` é diferente de `DT_TRAN`. `DT_TRAN` representa a data da movimentação; `TS_INCL_TRAN` representa inclusão/disponibilização na fonte e é usado para identificar utilização recente do aplicativo.

### 3.8 `TS_INCL_TRAN_REF`

**Nome de negócio:** Última utilização observada do cliente.

**O que significa:** Maior `TS_INCL_TRAN` encontrado para o cliente dentro da formação do público.

**Por que existe:** Representa o ponto mais recente de utilização observada e ancora o cálculo do ciclo financeiro aberto.

**Como é usada:** É calculada por `MAX(TS_INCL_TRAN)` e utilizada com o dia do ciclo para localizar o início do ciclo aberto.

**O que significa quando está vazia ou nula:** Depois que o cliente é considerado elegível, não pode ser nula. Sua ausência impede a continuidade coerente da análise.

**O que o negócio precisa enxergar no HTML:** Data e hora da última utilização observada, com texto que deixe claro seu papel de referência.

**Classificação:** Resultado.

**Observação importante:** Não é necessariamente o momento da última movimentação econômica.

### 3.9 `CD_CLI`

**Nome de negócio:** Identificador do cliente analisado.

**O que significa:** Chave que representa a pessoa sobre a qual todo o resultado individual é consolidado.

**Por que existe:** Integra público, perfil, movimentações e resultado em torno do mesmo cliente.

**Como é usada:** Pode ser informado diretamente, localizado por CPF ou escolhido entre os elegíveis. Quando informado, possui prioridade sobre o CPF de entrada.

**O que significa quando está vazio ou inválido:** Se não puder ser selecionado e validado como inteiro INT32, o processamento é bloqueado.

**O que o negócio precisa enxergar no HTML:** Identificação do cliente, protegida pelo mecanismo de privacidade.

**Classificação:** Insumo.

**Observação importante:** O resultado possui exatamente um `CD_CLI`; ele não agrega várias pessoas.

### 3.10 CPF de entrada

**Nome de negócio:** Identificador auxiliar para localizar o cliente.

**O que significa:** CPF informado para descobrir um `CD_CLI` quando este não foi fornecido diretamente.

**Por que existe:** Oferece uma forma alternativa de seleção do cliente.

**Como é usada:** Somente quando `CD_CLI` está nulo. A linha mais recente desse CPF dentro da formação fornece o `CD_CLI`.

**O que significa quando está vazio ou nulo:** Se `CD_CLI` também estiver nulo, um cliente elegível é selecionado aleatoriamente. Se `CD_CLI` estiver preenchido, o CPF de entrada é ignorado.

**O que o negócio precisa enxergar no HTML:** Somente quando for relevante explicar o caminho de seleção, sempre protegido por privacidade.

**Classificação:** Insumo.

**Observação importante:** O CPF de entrada seleciona o cliente; `CD_CPF`, tratado no bloco seguinte, é o CPF consolidado a partir das linhas do cliente.

### 3.11 `CD_EST_TRAN_INST`

**TÉCNICA — não deve orientar a narrativa do HTML.**

**Nome de negócio:** Estado técnico da transação institucional.

**O que significa:** Código de estado usado para restringir as leituras aos registros com valor `0`.

**Por que existe:** Garante que somente o estado aceito pelo contrato forme o público e alimente as movimentações.

**Como é usada:** É filtro na seleção, na formação do cliente e na leitura de movimentações.

**O que significa quando difere de zero:** A linha não participa dessas leituras.

**O que o negócio precisa enxergar no HTML:** Nada além de uma eventual menção técnica de que foram considerados somente registros em estado elegível. Não existe denominação empresarial comprovada para o código `0` neste contrato.

**Classificação:** Técnico.

**Observação importante:** Não atribuir nomes como “aprovada”, “ativa” ou “liquidada” sem definição oficial da fonte.

### 3.12 `CD_TIP_PSS`

**Nome de negócio:** Tipo de pessoa.

**O que significa:** O valor `1` identifica pessoa física para a formação do público.

**Por que existe:** O Radar individual descrito aqui é direcionado a clientes pessoa física.

**Como é usada:** Filtra a seleção e a formação do cliente.

**O que significa quando difere de 1:** A linha não é usada para formar o público deste produto.

**O que o negócio precisa enxergar no HTML:** “Cliente pessoa física”, sem necessidade de mostrar o código.

**Classificação:** Regra.

**Observação importante:** O filtro não é reaplicado na leitura de movimentações Q5; a pessoa já foi definida na formação do cliente.

### 3.13 O que a formação do público prova?

Existir `TS_INCL_TRAN` dentro da janela de formação significa que foi observada utilização recente do aplicativo com inclusão das fontes para aquele cliente, em uma linha de pessoa física e estado aceito.

Isso prova a presença do cliente no público desta execução. Não prova, sozinho:

- que exista CPF único;
- que exista conta única;
- que exista ciclo;
- que exista renda;
- que existam movimentações na futura janela financeira;
- que a pontuação será completa.

## 4. Bloco B — CPF

### 4.1 `NR_CPF_CNPJ_TITR`

**Nome de negócio:** CPF associado ao titular nas linhas do cliente.

**O que significa:** Identificação de CPF/CNPJ do titular informada em cada linha usada na formação. Como o público exige pessoa física, o Radar trata os valores não nulos como candidatos a CPF do cliente.

**Por que existe:** Permite verificar se há uma única identificação não nula consistente para consultar a renda.

**Como é usada:** Entra em `COUNT(DISTINCT ...)`; valores nulos são ignorados por essa contagem.

**O que significa quando está vazio ou nulo:** A linha não acrescenta um CPF distinto. Isso não permite concluir, isoladamente, se o cliente não possui CPF ou se apenas aquela linha veio sem preenchimento.

**O que o negócio precisa enxergar no HTML:** Não é necessário exibir os valores de todas as linhas. O resumo deve usar a flag de unicidade e, quando disponível, o CPF consolidado, sempre sob privacidade.

**Classificação:** Insumo.

**Observação importante:** O contrato comprova associação do CPF às linhas do cliente; não autoriza interpretar cada ocorrência como prova isolada de titularidade principal da conta.

### 4.2 `FL_CPF_UNICO`

**Nome de negócio:** Indicador de CPF único.

**O que significa:** Informa se foi encontrado exatamente um CPF não nulo distinto nas linhas do cliente.

**Por que existe:** A renda somente pode ser procurada quando existe uma chave de CPF única.

**Como é usada:** Recebe `S` quando `COUNT(DISTINCT NR_CPF_CNPJ_TITR) = 1`; recebe `N` nos demais casos.

**O que significa `S`:** Existe exatamente um CPF não nulo distinto, mesmo que também existam linhas com CPF nulo.

**O que significa `N`:** Pode significar nenhum CPF não nulo ou dois ou mais CPFs distintos. A flag não diferencia essas causas.

**O que significa quando está vazia ou nula:** Não pode ser nula na linha final.

**O que o negócio precisa enxergar no HTML:** “CPF único: Sim/Não”, sem transformar `N` automaticamente em uma causa específica.

**Classificação:** Resultado.

**Observação importante:** `N` não torna a linha final inexistente, mas impede a consulta de renda por falta de uma chave única.

### 4.3 `CD_CPF`

**Nome de negócio:** CPF consolidado do cliente.

**O que significa:** CPF propagado pelo Radar quando existe exatamente um valor não nulo distinto.

**Por que existe:** Fornece uma única chave para consultar a renda presumida.

**Como é usada:** Quando `FL_CPF_UNICO = 'S'`, recebe o maior valor de CPF — que é o único valor distinto — convertido para `DECIMAL(14,0)`. Quando a flag é `N`, recebe `NULL`.

**O que significa quando está vazio ou nulo:** Não foi possível formar um CPF único. O resultado não informa se isso ocorreu por ausência total ou multiplicidade.

**O que significa quando é zero:** O contrato não atribui significado negocial especial ao zero. Se a fonte o entregar como único, ele é propagado segundo a regra vigente.

**O que o negócio precisa enxergar no HTML:** “CPF associado”, mascarado enquanto a privacidade estiver ativa; quando nulo, “Não disponível”.

**Classificação:** Resultado.

**Observação importante:** O CPF final não é escolhido por preferência entre vários CPFs. Ele só existe quando a unicidade já foi comprovada matematicamente.

### 4.4 CPF usado na renda

**Nome de negócio:** Chave de CPF para localização da renda.

**O que significa:** É o próprio `CD_CPF`, convertido para o formato usado na consulta da fonte de renda.

**Por que existe:** A renda é armazenada por CPF, enquanto o restante do Radar é consolidado por `CD_CLI`.

**Como é usada:** A consulta exige `NR_CPF_BASE_SRF = CD_CPF` e somente ocorre quando a flag de CPF único é `S` e `CD_CPF` não é nulo.

**O que significa quando está vazio ou nulo:** A fonte de renda não é consultada.

**O que o negócio precisa enxergar no HTML:** O CPF utilizado pode aparecer no detalhe da renda, protegido por privacidade.

**Classificação:** Insumo.

**Observação importante:** O Radar assume que a renda associada ao único CPF consolidado é a renda aplicável ao cliente identificado pelo `CD_CLI`.

### 4.5 Leitura humana dos casos de CPF

| Situação observada | Resultado | Interpretação permitida |
|---|---|---|
| Um CPF não nulo distinto | `FL_CPF_UNICO = S`; `CD_CPF` preenchido | Existe chave única para consultar renda. Isso comprova consistência de CPF no conjunto observado, não a qualidade absoluta do cadastro. |
| Dois ou mais CPFs não nulos distintos | `FL_CPF_UNICO = N`; `CD_CPF = NULL` | O conjunto não oferece uma chave única de renda. O Radar não escolhe um dos CPFs. |
| Nenhum CPF não nulo | `FL_CPF_UNICO = N`; `CD_CPF = NULL` | Não existe chave de renda disponível no conjunto observado. |
| Um CPF não nulo e algumas linhas nulas | `FL_CPF_UNICO = S`; `CD_CPF` preenchido | Os nulos são ignorados pela contagem; permanece exatamente um CPF não nulo distinto. |

Nos dois casos que produzem `N`, o resultado final é igual quanto à flag e ao CPF consolidado. Sem nova informação, a apresentação não deve afirmar qual causa ocorreu.

## 5. Bloco C — Conta corrente BB elegível

### 5.1 Por que o Radar procura uma conta?

O Radar precisa localizar uma conta corrente BB elegível para consultar o dia de ciclo financeiro. A conta não é usada para somar movimentações nem para definir o cliente principal.

O papel da conta é:

```text
agência e conta encontradas
→ normalização da chave
→ consulta da fonte de ciclo
→ dia do ciclo
→ janela financeira
```

Ela não deve ser chamada de “conta principal”, porque essa condição não é comprovada. É a conta corrente BB que atende aos critérios vigentes e permite procurar o ciclo.

### 5.2 `NR_AG_TITR`

**Nome de negócio:** Agência encontrada da conta corrente BB.

**O que significa:** Valor físico de agência associado à conta candidata nas linhas do cliente.

**Por que existe:** Forma, junto com a conta, a chave necessária para localizar o ciclo.

**Como é usada:** Precisa estar preenchida; as contas candidatas são agrupadas por agência e conta físicas antes da normalização.

**O que significa quando está vazia ou nula:** A linha não fornece uma conta candidata elegível.

**O que o negócio precisa enxergar no HTML:** Agência encontrada e, separadamente, agência utilizada após normalização, ambas protegidas por privacidade.

**Classificação:** Insumo.

**Observação importante:** Representações físicas distintas são consideradas distintas antes da normalização.

### 5.3 `CD_CT_TITR`

**Nome de negócio:** Conta encontrada do titular.

**O que significa:** Valor físico da conta corrente candidato à consulta do ciclo.

**Por que existe:** Completa a chave agência/conta.

**Como é usada:** Precisa estar preenchida e não pode ser texto vazio após remoção de espaços externos.

**O que significa quando está vazia ou nula:** A linha não fornece uma conta candidata elegível.

**O que o negócio precisa enxergar no HTML:** Conta encontrada e conta utilizada após normalização, protegidas por privacidade.

**Classificação:** Insumo.

**Observação importante:** Zeros à esquerda fazem parte da representação física, mas são removidos na chave normalizada.

### 5.4 `NR_MCA_PCT_OPB`

**Nome de negócio:** Marcador da conta corrente BB elegível.

**O que significa:** O valor `999999999`, combinado com o produto `6`, identifica a linha candidata a conta corrente BB usada para localizar o ciclo.

**Por que existe:** Distingue, entre as linhas do cliente, aquelas que podem fornecer a chave de conta esperada pela fonte de ciclo.

**Como é usada:** A linha somente é candidata quando `NR_MCA_PCT_OPB = 999999999`.

**O que significa quando possui outro valor:** A linha não participa da descoberta da conta para ciclo.

**O que o negócio precisa enxergar no HTML:** Como critério explicativo, preferencialmente traduzido para “conta corrente BB elegível”. O código pode permanecer no detalhe técnico.

**Classificação:** Regra.

**Observação importante:** Em outras partes do Radar, o mesmo atributo pode aparecer como marcador explicativo de uma movimentação. O significado deste item refere-se especificamente ao filtro de conta.

### 5.5 `CD_PRD`

**Nome de negócio:** Produto de conta corrente BB elegível.

**O que significa:** O valor `6`, junto com o marcador `999999999`, identifica o produto aceito para descobrir a conta usada no ciclo.

**Por que existe:** Restringe a conta candidata ao produto previsto pela regra vigente.

**Como é usada:** A linha somente é candidata quando `CD_PRD = 6`.

**O que significa quando possui outro valor:** A linha não participa da descoberta da conta para ciclo.

**O que o negócio precisa enxergar no HTML:** O critério pode ser apresentado como “produto de conta corrente BB”; o código deve ficar em detalhe técnico.

**Classificação:** Regra.

**Observação importante:** O código não deve ser usado para afirmar que essa é a conta principal do relacionamento.

### 5.6 `FL_CONTA_ELEGIVEL_UNICA`

**Nome de negócio:** Indicador de conta corrente BB única para ciclo.

**O que significa:** Informa se existe exatamente um par físico distinto de agência e conta que atende aos critérios.

**Por que existe:** A consulta de ciclo precisa de uma única chave de agência e conta.

**Como é usada:** Recebe `S` quando existe exatamente um par candidato; recebe `N` com zero ou mais de um par.

**O que significa `S`:** Há uma única conta corrente BB elegível para localizar o ciclo.

**O que significa `N`:** Pode não haver conta candidata ou podem existir múltiplas contas candidatas. A flag não diferencia as causas.

**O que significa quando está vazia ou nula:** Não pode ser nula no resultado final.

**O que o negócio precisa enxergar no HTML:** “Conta única para ciclo: Sim/Não”. Não apresentar `N` como se significasse necessariamente ausência.

**Classificação:** Resultado.

**Observação importante:** Múltiplas contas representam ambiguidade para escolher a chave do ciclo. Elas não provam múltiplos relacionamentos principais nem permitem escolher uma conta arbitrariamente.

### 5.7 `CD_UOR_CC_NORM`

**Nome de negócio:** Agência utilizada na consulta do ciclo.

**O que significa:** Agência convertida para o formato inteiro esperado pela fonte de ciclo.

**Por que existe:** A representação física de agência precisa ser compatível com a chave `CD_UOR_CC`.

**Como é usada:** A agência é convertida para texto, aparada, validada como numérica e convertida para INT32.

**O que significa quando está vazia ou nula:** A conta normalizada está indisponível e a fonte de ciclo não é consultada.

**O que o negócio precisa enxergar no HTML:** Fluxo “agência encontrada → agência utilizada”. Quando nula, mostrar apenas “Não disponível”.

**Classificação:** Cálculo.

**Observação importante:** Não existe motivo estruturado de falha para apresentação; o HTML não deve inventar um.

### 5.8 `NR_CC_NORM`

**Nome de negócio:** Conta utilizada na consulta do ciclo.

**O que significa:** Conta convertida para o formato numérico de até 11 dígitos significativos esperado pela fonte de ciclo.

**Por que existe:** Permite casar a conta física com a chave `NR_CC` da fonte de ciclo.

**Como é usada:** Remove espaços externos, exige somente dígitos, remove zeros à esquerda e converte o resultado para `DECIMAL(11,0)`. Uma conta formada somente por zeros vira `0`.

**O que significa quando está vazia ou nula:** A conta normalizada está indisponível e a fonte de ciclo não é consultada.

**O que o negócio precisa enxergar no HTML:** Fluxo “conta encontrada → conta utilizada”. Quando nula, mostrar “Não disponível”.

**Classificação:** Cálculo.

**Observação importante:** Agência e conta normalizadas ficam ambas nulas quando qualquer condição de normalização falha.

### 5.9 Como interpretar ausência ou multiplicidade de contas?

Sem exatamente uma conta elegível:

- agência e conta físicas não são propagadas;
- a chave normalizada fica indisponível;
- a fonte de ciclo não é consultada;
- o dia de fallback fica nulo;
- a janela financeira fica indisponível;
- a leitura de movimentações financeiras não ocorre.

Esse estado pode permitir uma linha final parcial, mas impede a construção da análise financeira baseada em ciclos.

## 6. Bloco D — Ciclo financeiro

### 6.1 O que é um ciclo financeiro?

É o intervalo recorrente delimitado pelo dia de início do ciclo da conta. Ele organiza a vida financeira entre dois marcos mensais equivalentes.

Se o dia do ciclo for `20`:

- um novo ciclo começa no dia 20;
- o ciclo anterior termina no dia 19;
- `20/07 → 19/08` representa a vida financeira observada entre esses dois marcos.

O Radar usa ciclos em vez de meses-calendário para alinhar a análise ao ritmo financeiro da conta. Esse intervalo pode ser entendido como uma competência financeira entre fechamentos, mas não deve ser confundido com competência contábil oficial.

### 6.2 `CD_UOR_CC`

**Nome de negócio:** Agência na fonte de ciclo.

**O que significa:** Chave de agência utilizada para localizar os registros de ciclo.

**Por que existe:** A fonte de ciclo organiza os registros por agência e conta.

**Como é usada:** Precisa ser igual a `CD_UOR_CC_NORM`.

**O que significa quando está vazia ou nula:** Não existe registro utilizável para aquela linha; sem chave normalizada, a consulta nem ocorre.

**O que o negócio precisa enxergar no HTML:** A agência utilizada já pode ser explicada pela etapa de normalização. Não é necessário repetir o nome técnico da coluna.

**Classificação:** Técnico.

**Observação importante:** É a agência da chave de ciclo, não uma nova agência descoberta nessa etapa.

### 6.3 `NR_CC`

**Nome de negócio:** Conta na fonte de ciclo.

**O que significa:** Chave de conta utilizada para localizar os registros de ciclo.

**Por que existe:** Completa a chave com a agência.

**Como é usada:** Precisa ser igual a `NR_CC_NORM`.

**O que significa quando está vazia ou nula:** Não existe registro utilizável para aquela linha; sem chave normalizada, a consulta não ocorre.

**O que o negócio precisa enxergar no HTML:** A conta utilizada já aparece na normalização; o nome técnico pode ficar no detalhe.

**Classificação:** Técnico.

**Observação importante:** Não é o número físico original com zeros e espaços, mas a chave normalizada.

### 6.4 `TS_ULT_EXEA_PSQ`

**TÉCNICA — não deve orientar a narrativa do HTML.**

**Nome de negócio:** Referência técnica de atualização do registro de ciclo.

**O que significa:** Timestamp usado para ordenar os registros da mesma agência e conta e escolher o mais recente.

**Por que existe:** Pode haver histórico de registros de ciclo para a mesma chave.

**Como é usada:** Ordenação decrescente; a primeira linha é escolhida. Não existe segundo desempate nem corte pela data de execução.

**O que significa quando está vazia ou nula:** O contrato não define uma interpretação empresarial específica. Seu comportamento depende da ordenação entregue pela fonte.

**O que o negócio precisa enxergar no HTML:** Se necessária, mostrar apenas a referência da linha escolhida, sem traduzir o nome técnico como um evento empresarial não comprovado.

**Classificação:** Técnico.

**Observação importante:** Não chamar de “último fechamento” ou “última movimentação” sem definição oficial da fonte.

### 6.5 `TS_DD_INC_MM_CLC_BLC_REF`

**Nome de negócio:** Referência do dia de ciclo selecionado.

**O que significa:** Cópia de `TS_ULT_EXEA_PSQ` da linha que forneceu o dia físico do ciclo.

**Por que existe:** Preserva a linhagem temporal do valor escolhido.

**Como é usada:** É informativa no resultado; a escolha da linha já ocorreu pela maior referência técnica.

**O que significa quando está vazia ou nula:** Não havia linha de ciclo escolhida ou a conta normalizada estava indisponível.

**O que o negócio precisa enxergar no HTML:** “Referência do ciclo”, como detalhe explicativo. Não esconder quando o dia utilizado veio de fallback.

**Classificação:** Contexto.

**Observação importante:** A data ajuda a compreender a origem do dia, mas não altera o ciclo depois de selecionada.

### 6.6 `DD_INC_MM_CLC_BLC`

**Nome de negócio:** Dia encontrado do ciclo financeiro.

**O que significa:** Dia do mês em que se inicia o ciclo da conta segundo a linha selecionada.

**Por que existe:** Define o marco mensal usado para separar ciclo aberto e ciclos fechados.

**Como é usada:** Quando preenchida, fornece o dia efetivamente utilizado; valores fora de `1..31` bloqueiam o processamento.

**O que significa quando está vazia ou nula:** Pode não existir linha de ciclo ou a linha pode não fornecer dia. Se a conta estiver normalizada, o fallback será `1`.

**O que o negócio precisa enxergar no HTML:** “Dia encontrado”, separado de “Dia utilizado”.

**Classificação:** Resultado.

**Observação importante:** Meses curtos ajustam a ocorrência do ciclo para o último dia disponível sem alterar o dia contratual original nos meses seguintes.

### 6.7 `DD_INC_MM_CLC_BLC_FALLBACK`

**Nome de negócio:** Dia utilizado no ciclo financeiro.

**O que significa:** Dia efetivamente aplicado para construir a janela.

**Por que existe:** Permite formar ciclos mensais mesmo quando uma conta normalizada não possui registro ou dia de ciclo utilizável.

**Como é usada:** Recebe o dia físico quando disponível; recebe `1` quando há conta normalizada, mas não há linha ou dia; fica nula sem conta normalizada.

**O que significa quando vale `1`:** Pode ser o dia físico encontrado ou o fallback. Só é possível afirmar que houve fallback quando `DD_INC_MM_CLC_BLC` é nulo e o dia utilizado é `1`.

**O que significa quando está vazia ou nula:** Não existe conta normalizada, portanto não é possível construir a janela.

**O que o negócio precisa enxergar no HTML:** “Dia encontrado → Dia utilizado”. Quando o fallback for comprovado pelos campos existentes, apresentá-lo como alternativa legítima: “Ciclo mensal iniciado no primeiro dia”.

**Classificação:** Regra.

**Observação importante:** Fallback não significa erro. É um tratamento previsto. Não há fallback `1` quando a própria conta normalizada está indisponível.

## 7. Bloco E — Janela oficial e contexto

### 7.1 `DT_REF_INI`

**Nome de negócio:** Início da janela financeira oficial.

**O que significa:** Primeiro dia incluído na quantidade de ciclos fechados solicitada.

**Por que existe:** Define onde começa o universo financeiro oficial do diagnóstico.

**Como é usada:** É calculada recuando `periodo` ciclos a partir do início do ciclo aberto e é inclusiva.

**O que significa quando está vazia ou nula:** Não foi possível resolver um dia de ciclo; `DT_REF_FIM` também deve ser nula.

**O que o negócio precisa enxergar no HTML:** Início claramente marcado da “Janela oficial”.

**Classificação:** Resultado.

**Observação importante:** Não é o início da formação do público. Formação e análise financeira possuem janelas diferentes.

### 7.2 `DT_REF_FIM`

**Nome de negócio:** Fim da janela financeira oficial.

**O que significa:** Último dia do ciclo fechado mais recente, imediatamente anterior ao início do ciclo aberto.

**Por que existe:** Impede que movimentações de um ciclo ainda em andamento entrem no diagnóstico.

**Como é usada:** É inclusiva: movimentações com `DT_TRAN = DT_REF_FIM` pertencem à janela.

**O que significa quando está vazia ou nula:** Não foi possível construir a janela; `DT_REF_INI` também deve ser nula.

**O que o negócio precisa enxergar no HTML:** Fim claramente marcado da “Janela oficial”.

**Classificação:** Resultado.

**Observação importante:** A janela oficial é fechada nas duas extremidades.

### 7.3 `DT_LEITURA_INI` / início do contexto

**Nome de negócio:** Início do contexto de reconciliação.

**O que significa:** Data situada cinco dias corridos antes de `DT_REF_INI`.

**Por que existe:** Algumas movimentações que se anulam podem ser registradas em lados diferentes da borda do ciclo. Observar dias anteriores permite encontrar a contraparte externa de uma linha oficial.

**Como é usada:** Amplia somente a leitura de movimentações; não amplia a janela financeira oficial.

**O que significa quando está vazia ou nula:** Sem janela financeira, não existe contexto e a fonte de movimentações não é consultada.

**O que o negócio precisa enxergar no HTML:** “Contexto consultado: cinco dias antes”, visualmente separado da janela oficial.

**Classificação:** Contexto.

**Observação importante:** Este nome representa um conceito derivado; não é atributo do resultado 1×80.

### 7.4 `DT_LEITURA_FIM` / fim do contexto

**Nome de negócio:** Fim do contexto de reconciliação.

**O que significa:** Data situada cinco dias corridos depois de `DT_REF_FIM`.

**Por que existe:** Permite localizar contraparte registrada logo depois do encerramento do ciclo.

**Como é usada:** Amplia a consulta, sem tornar as linhas posteriores parte do ciclo.

**O que significa quando está vazia ou nula:** Sem janela financeira, não existe contexto.

**O que o negócio precisa enxergar no HTML:** “Contexto consultado: cinco dias depois”, separado da janela oficial.

**Classificação:** Contexto.

**Observação importante:** Este nome também é conceitual e não pertence ao contrato final de 80 atributos.

### 7.5 `IN_JANELA`

**Nome de negócio:** Indicador de pertencimento à janela oficial.

**O que significa:** Distingue uma movimentação financeira do ciclo de uma movimentação lida apenas como contexto.

**Por que existe:** A reconciliação precisa usar evidências externas sem transformar essas evidências em fatos financeiros do ciclo.

**Como é usada:** Recebe `S` quando `DT_REF_INI <= DT_TRAN <= DT_REF_FIM`; recebe `N` nas linhas do contexto externo.

**O que significa `S`:** Movimento oficial bruto, antes da reconciliação.

**O que significa `N`:** Movimento externo ao ciclo, disponível apenas para auxiliar a reconciliação.

**O que significa quando está vazio ou nulo:** O contrato funcional forma explicitamente o indicador; a ausência não possui estado negocial previsto.

**O que o negócio precisa enxergar no HTML:** Uma separação inequívoca entre “Dentro do ciclo” e “Contexto externo”.

**Classificação:** Regra.

**Observação importante:** Uma linha externa pode neutralizar uma linha oficial em um par de borda, mas nunca entra nas quantidades, valores, orçamento ou pontuação do ciclo.

### 7.6 Uma transação externa pertence à análise financeira?

Não.

Ela pode servir como evidência de que uma linha interna possui uma contraparte de natureza oposta, mesmo valor e mesma moeda registrada até cinco dias além da borda. Quando isso ocorre, a linha interna pode ser removida pela reconciliação de borda.

A contraparte externa:

- não se torna movimento oficial;
- não entra no universo efetivo;
- não entra em quantidades ou valores;
- não participa do orçamento;
- não participa da pontuação.

Seu papel é exclusivamente explicar e sustentar a neutralização da linha oficial correspondente.

## 8. Bloco F — Renda presumida e base financeira

### 8.1 `NR_CPF_BASE_SRF`

**TÉCNICA — não deve orientar a narrativa do HTML.**

**Nome de negócio:** Chave de CPF da fonte de renda.

**O que significa:** Campo usado para localizar a renda associada ao `CD_CPF` único.

**Por que existe:** Faz a ligação entre o cliente consolidado e a fonte de renda.

**Como é usada:** A consulta exige igualdade com `CD_CPF`.

**O que significa quando está vazio ou nulo:** A linha não casa com o CPF consultado.

**O que o negócio precisa enxergar no HTML:** O CPF utilizado, e não o nome técnico da coluna, sempre protegido pela privacidade.

**Classificação:** Técnico.

**Observação importante:** O CPF é chave de busca; a fonte de renda é que fornece a estimativa financeira.

### 8.2 `DT_INCL_REN_AVLD`

**Nome de negócio:** Data de inclusão da renda avaliada.

**O que significa:** Data associada ao registro de renda na fonte.

**Por que existe:** Permite selecionar a renda mais recentemente incluída para o CPF.

**Como é usada:** Os registros são ordenados em ordem decrescente e a primeira linha é escolhida.

**O que significa quando está vazia ou nula:** Não há referência temporal utilizável naquela linha. A interpretação exata da ordenação de nulos depende do ambiente da fonte.

**O que o negócio precisa enxergar no HTML:** A data derivada `DT_REN_PRES_REF`, apresentada como referência da renda.

**Classificação:** Regra.

**Observação importante:** Não existe corte por `DATA_EXECUCAO`; a maior data disponível é elegível mesmo que seja posterior à execução.

### 8.3 `DT_REN_PRES_REF`

**Nome de negócio:** Referência da renda presumida.

**O que significa:** Data de inclusão da linha mais recente de renda escolhida para o CPF.

**Por que existe:** Permite ao negócio saber de qual registro temporal veio a estimativa usada.

**Como é usada:** É a conversão para data de `DT_INCL_REN_AVLD` na linha vencedora.

**O que significa quando está vazia ou nula:** Não havia CPF único, a consulta não ocorreu ou nenhum registro elegível de renda foi encontrado.

**O que o negócio precisa enxergar no HTML:** “Referência da renda”, sem chamá-la de mês de recebimento ou competência salarial.

**Classificação:** Resultado.

**Observação importante:** É referência de inclusão do registro, não prova de que a renda foi recebida nessa data.

### 8.4 `VL_REN`

**Nome de negócio:** Renda mensal estimada na fonte.

**O que significa:** Valor mensal de renda avaliada associado ao CPF na linha selecionada.

**Por que existe:** Fornece a capacidade financeira mensal de referência.

**Como é usada:** É multiplicada por `periodo` para formar `VL_REN_PRES`.

**O que significa quando está vazia ou nula:** A renda presumida ajustada também fica nula.

**O que significa quando é zero:** Existe um valor explícito igual a zero; não é o mesmo que ausência de registro.

**O que o negócio precisa enxergar no HTML:** O fluxo atual não preserva `VL_REN` isoladamente depois do ajuste. Portanto, deve ser mostrado apenas `VL_REN_PRES` e a quantidade de ciclos.

**Classificação:** Insumo.

**Observação importante:** Não criar outra consulta ou dividir o valor ajustado para tentar reconstruir uma nova informação de fonte.

### 8.5 `VL_REN_PRES`

**Nome de negócio:** Renda presumida disponível no período analisado.

**O que significa:** Estimativa de capacidade financeira para a quantidade de ciclos fechados selecionada.

**Por que existe:** Movimentações de vários ciclos precisam ser comparadas com uma base que cubra o mesmo horizonte.

**Como é usada:** `VL_REN_PRES = VL_REN × periodo`, com resultado `DECIMAL(17,2)`. Na visão principal, é convertida para `BASE_FINANCEIRA` e aplicada ao orçamento e aos percentuais.

**O que significa quando está vazia ou nula:** Não existe renda utilizável, seja por ausência de CPF único, ausência de registro ou renda física nula. Os percentuais dependentes da base ficam nulos e a pontuação não se completa.

**O que significa quando é zero:** A estimativa está explicitamente zerada. Percentuais sobre a base não são calculados; zero não deve ser apresentado como renda não encontrada.

**O que o negócio precisa enxergar no HTML:** Valor da renda presumida ajustada, referência da renda e texto “N ciclos considerados”.

**Classificação:** Resultado.

**Observação importante:** Multiplicar por três ciclos significa usar três vezes a mesma estimativa mensal como capacidade do horizonte. Não significa que foram localizados três registros mensais de renda.

### 8.6 `BASE_FINANCEIRA`

**Nome de negócio:** Base de comparação financeira.

**O que significa:** Valor que uma visão utiliza simultaneamente como referência de entrada no orçamento e como denominador dos percentuais temáticos.

**Por que existe:** Permite aplicar as mesmas regras a duas lentes comparáveis sem alterar os fatos transacionais.

**Como é usada:** Na visão principal, recebe a renda presumida ajustada. Na comparação secundária, recebe as entradas realizadas elegíveis do cenário.

**O que significa quando está vazia ou nula:** A visão não possui base comparável. Orçamento e percentuais dependentes ficam parcial ou totalmente indisponíveis conforme suas fórmulas.

**O que significa quando é zero:** A base existe e vale zero; razões que exigem divisão não são calculadas.

**O que o negócio precisa enxergar no HTML:** Um nome humano para a base ativa — “Renda presumida” ou “Entradas realizadas” — e seu valor. O termo técnico `BASE_FINANCEIRA` pode ficar no detalhe.

**Classificação:** Insumo.

**Observação importante:** A base alternativa recalcula somente os campos dependentes. Ela não altera movimentos, classificações, quantidades nem valores temáticos observados.

### 8.7 A renda presumida representa renda mensal?

Sim. O valor físico selecionado é tratado como renda mensal. O ajuste pelo número de ciclos estende essa estimativa ao horizonte analisado:

```text
VL_REN_PRES = renda mensal estimada × quantidade de ciclos
```

Se `periodo = 3`, o Radar interpreta que a capacidade financeira presumida dos três ciclos corresponde a três vezes a estimativa mensal.

### 8.8 A renda presumida é denominador de tudo?

Não.

Na visão principal, ela é denominador dos cinco percentuais temáticos e base de entrada do orçamento. Ela não é denominador ou origem de:

- quantidades de transações;
- valores classificados;
- valores temáticos;
- reconciliação;
- flags de moeda e Agro.

Esses fatos são calculados diretamente das movimentações efetivas.

### 8.9 Qual é o papel de `VL_ENT_TOTAL` na visão principal?

`VL_ENT_TOTAL` continua registrando as entradas realizadas que participam do orçamento segundo o mapa. Ele permanece como fato financeiro no resultado, mas não é a base usada para recalcular o orçamento da visão principal `RENDA_PRESUMIDA`.

Isso permite distinguir:

- o que efetivamente entrou e foi considerado orçamentário; e
- qual capacidade estimada foi usada para o diagnóstico principal.

No resultado oficial, `VL_ENT_TOTAL` é a própria entrada usada pelo orçamento. Na visão `RENDA_PRESUMIDA`, o orçamento é recalculado com a renda presumida, embora `VL_ENT_TOTAL` permaneça registrado sem substituição.

### 8.10 O que são `ENTRADAS_REALIZADAS` perto da renda presumida?

São uma comparação entre realidade observada e capacidade estimada.

A base de entradas realizadas soma créditos que:

- pertencem ao universo efetivo;
- estão em BRL;
- possuem classificação válida no mapa.

Ela não exige participação temática nem participação orçamentária. Por isso pode incluir, entre outros, resgates e receitas Agro. Não deve ser confundida com `VL_ENT_TOTAL`, que segue a flag de participação no orçamento.

Em termos de produto:

```text
RENDA_PRESUMIDA
→ leitura principal da capacidade estimada

ENTRADAS_REALIZADAS
→ comparação secundária com os créditos observados
```

## 9. Resumo conceitual dos blocos A–F

```text
Utilização recente do aplicativo
→ forma o cliente da execução

CPF único
→ fornece uma chave segura para buscar renda

Conta corrente BB elegível e única
→ fornece agência e conta para localizar o ciclo

Dia do ciclo
→ separa ciclo aberto de ciclos fechados

Janela oficial
→ delimita os fatos financeiros do diagnóstico

Contexto de ±5 dias
→ fornece evidência de reconciliação sem entrar no ciclo

Renda mensal estimada × ciclos
→ forma a capacidade financeira presumida do período

Renda presumida
→ sustenta a visão principal de orçamento, percentuais e prioridade

Entradas realizadas
→ oferece uma comparação secundária com os créditos observados
```

## 10. Limites de interpretação

As seguintes afirmações não são autorizadas por estes conceitos:

- a conta encontrada é a conta principal do cliente;
- `CD_EST_TRAN_INST = 0` significa “aprovada”, “ativa” ou outro nome não definido;
- `TS_INCL_TRAN` é a data econômica da transação;
- `TS_ULT_EXEA_PSQ` é a data do último fechamento;
- `FL_CPF_UNICO = N` identifica sozinho ausência ou multiplicidade;
- `FL_CONTA_ELEGIVEL_UNICA = N` identifica sozinho ausência ou multiplicidade;
- fallback de ciclo significa falha do cliente;
- movimento externo pertence ao ciclo financeiro;
- crédito observado é necessariamente renda;
- ausência de renda elimina todos os fatos do diagnóstico;
- tema vencedor é sinônimo automático de maior risco ou pior problema.

Essas fronteiras preservam a diferença entre dado observado, regra vigente e interpretação de negócio.
