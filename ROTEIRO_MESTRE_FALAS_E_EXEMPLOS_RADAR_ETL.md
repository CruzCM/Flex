# Manual Mestre de Apresentação — Radar Financeiro ETL
## Roteiro Verbal Completo + Cenários Práticos Integrados

> **Público-alvo:** Comitê de Validação Negocial, Engenharia de Dados e Squad de CRM / Meus Insights.  
> **Estrutura:** Fala verbal contínua em primeira pessoa, atributos físicos de tabelas, provocações de deliberação da mesa e **exemplos práticos simulados aplicados imediatamente a cada etapa**.  
> **Tempo estimado:** 30 a 35 minutos.

---

# Índice Geral

1. [Bloco 1: Abertura e Enquadramento](#bloco-1-abertura-e-enquadramento)
2. [Bloco 2: Filtros Primários, Entrada no App e Exclusões Rígidas](#bloco-2-filtros-primários-entrada-no-app-e-exclusões-rígidas)
   * *Cenário Prático 1: Exclusão por Moeda Estrangeira*
   * *Cenário Prático 2: Exclusão por Categoria Agro*
   * *Cenário Prático 3: Exclusão por Inatividade no Aplicativo*
3. [Bloco 3: Identificação Cadastral (Conta BB e CPF) e Renda Obrigatória](#bloco-3-identificação-cadastral-conta-bb-e-cpf-e-renda-obrigatória)
   * *Cenário Prático 4: Exclusão por Ausência de Renda Presumida*
   * *Cenário Prático 5: Exclusão por Múltiplas Contas no BB*
4. [Bloco 4: Ciclo Financeiro e Janela Fechada (Inclusão com Fallback)](#bloco-4-ciclo-financeiro-e-janela-fechada-inclusão-com-fallback)
   * *Cenário Prático 6: Inclusão com Fallback de Ciclo no Dia 01*
5. [Bloco 5: Renda Presumida e Perfil Financeiro](#bloco-5-renda-presumida-e-perfil-financeiro)
   * *Cenário Prático 5B: Exclusão por Ausência de Perfil Financeiro*
6. [Bloco 6: Captura Transacional e Reconciliação (Higienização de Dados)](#bloco-6-captura-transacional-e-reconciliação-higienização-de-dados)
   * *Cenário Prático 7: Reconciliação de Par Exato (Transferência entre Contas Próprias)*
7. [Bloco 7: Categorização, Agregação e Faixas Orçamentárias](#bloco-7-categorização-agregação-e-faixas-orçamentárias)
8. [Bloco 8: O Motor de Decisão — Como Chegamos aos 5 Públicos](#bloco-8-o-motor-de-decisão--como-chegamos-aos-5-públicos)
   * *Cenário Prático 8: Público 1 — Categorização dos Gastos (Nota 99)*
   * *Cenário Prático 9: Público 2 — Gestão de Orçamento (Déficit em Essenciais)*
   * *Cenário Prático 10: Público 3 — Consumo Planejado (Gastos Flexíveis)*
   * *Cenário Prático 11: Público 4 — Formação de Reserva (Superávit com Poupança Baixa)*
   * *Cenário Prático 12: Público 5 — Uso Consciente do Crédito (Alto Endividamento)*
   * *Cenário Prático 13: Código 9 — Empate Técnico entre Temas*
9. [Bloco 9: Os Três Cenários Comparativos](#bloco-9-os-três-cenários-comparativos)
10. [Bloco 10: Encerramento, Ata de Votação e Guia Visual de Apoio](#bloco-10-encerramento-ata-de-votação-e-guia-visual-de-apoio)

---

## Bloco 1: Abertura e Enquadramento

*(Postura firme e alinhamento de expectativas logo no primeiro slide)*

> "Boa tarde, pessoal.
>
> O Radar, hoje, é um **ETL de público-alvo**.
>
> É fundamental deixar isso claro desde o primeiro minuto: não estamos apresentando aqui um estudo acadêmico, nem uma análise exploratória aberta, nem um modelo estatístico de caixa-preta. Trata-se de um **pipeline de dados determinístico**, que roda em lote para processar a base transacional e comportamental dos nossos clientes e entregar **cinco públicos-alvo bem definidos**.
>
> Esses cinco públicos já foram apresentados e aprovados anteriormente. O nosso objetivo hoje é outro: **abrir o motor desse ETL e validar com vocês cada regra de negócio**, cada filtro de SQL, cada atributo de banco e cada valor de corte que define o enquadramento final do cliente.
>
> Para tornar a conversa prática e transparente, nós vamos percorrer a esteira na ordem exata em que o dado é processado pelo pipeline: desde as regras de corte mais simples de entrada até o motor final de pontuação. E em cada etapa, vamos demonstrar exatamente com números simulados como os clientes reais se comportam."

---

## Bloco 2: Filtros Primários, Entrada no App e Exclusões Rígidas

*(Explicando a elegibilidade inicial na tabela principal e introduzindo as exclusões categóricas e a porta de entrada)*

> "Começamos pela nossa fonte transacional central: a tabela **`DB2GFP.TRAN_RLZD_INST_PCT`**, buscando os registros do cliente (`CD_CLI`).
>
> Aqui aplicamos as regras primárias de corte, que definem quem entra e quem é sumariamente excluído do Radar. E aqui nós adotamos uma postura negocial de **corte rígido**:
>
> * **Primeiro, a regra de Moeda Estrangeira:** o corte é absoluto. Se o cliente tiver **qualquer transação em moeda diferente de Real**, ele **não participa do Radar**. Não tem conversa: não se trata de descartar a linha em dólar ou euro e calcular o restante em reais. A pessoa inteira é desqualificada do público. O Radar atende estritamente clientes com 100% das suas transações em moeda nacional (`CD_TIP_MOE_CRR = 'BRL'`).
> * **Segundo, a regra de Categorias Agro:** exatamente a mesma postura rígida. Se o cliente tiver **qualquer movimentação em categorias agro** (como receitas agro, insumos, cultivos ou criações), **ele é sumariamente excluído do Radar**.  
>   *A razão negocial é indiscutível:* o produtor rural tem uma dinâmica de fluxo de caixa completamente diferente de um assalariado urbano comum. A vida financeira dele é regida por safra, safrinha, custeio e receitas sazonais semestrais ou anuais. Avaliar um cliente agro numa régua mensal de 50/30/20 geraria orientações financeiras sem nenhum sentido — como apontar desequilíbrio orçamentário no mês em que ele comprou fertilizante e maquinário. O público Agro precisa de uma esteira e de um produto próprios; misturá-lo aqui destruiria a qualidade das recomendações.
> * **Terceiro, a situação da transação:** consideramos estritamente transações ativas e confirmadas, filtrando **`CD_EST_TRAN_INST = 0`**.
> * **Quarto, o tipo de pessoa:** o público do Radar é estritamente pessoa física, exigindo **`CD_TIP_PSS = 1`**.
> * **Quinto, a janela de ativação no aplicativo:** e aqui vale uma pausa muito importante sobre qual coluna de data utilizamos.
>
> Naturalmente, a primeira ideia intuitiva seria olhar para a data em que o cliente passou o cartão ou fez o Pix — que é o campo `DT_TRAN`. Mas **não** é esse campo que usamos para formar o público.
>
> Para determinar se o cliente entra ou não no Radar, nós olhamos o atributo **`TS_INCL_TRAN`** (Timestamp de Inclusão da Transação).
>
> **Por que essa escolha é intencional e estratégica para o negócio?**  
> Porque a tabela pertence ao schema `DB2GFP` — o Gestor Financeiro Pessoal. No ecossistema do banco, a movimentação só é carregada e registrada no GFP quando o cliente **acessa ou entra no aplicativo**.
>
> Portanto, ter um `TS_INCL_TRAN` dentro do **mês-calendário anterior à data de execução** significa, na prática, que **o cliente entrou no aplicativo recentemente**.
>
> Se um cliente movimentou a conta no mês passado, mas não abre o aplicativo há seis meses, os dados dele não terão um `TS_INCL_TRAN` no mês anterior. Consequentemente, ele **não sobrevive a esse filtro e não entra no público** — o processamento dele é interrompido ali mesmo.
>
> Isso traz uma enorme eficiência técnica e aderência negocial: como o Radar abastece as mensagens do *Meus Insights* dentro do app, não faz sentido consumir máquina calculando recomendações para quem não utiliza o canal.
>
> Vamos ver três exemplos práticos de como esses cortes funcionam na vida real:"

---

### Exemplos Práticos do Bloco 2

#### Cenário Prático 1: Exclusão por Moeda Estrangeira
* **Perfil do Cliente:** `CD_CLI = 10101` | Data de Execução: `15/09/2026`
* **Transações:** 25 transações normais em Reais no Brasil (R$ 4.200,00) e **1 compra de US$ 12,00** na Steam (`CD_TIP_MOE_CRR = 'USD'`).
* **Comportamento no ETL:** A flag de sentinela é gravada como **`FL_SOMENTE_BRL = 'N'`**.
* **Decisão Negocial:** O cliente **não participa do Radar**. A pessoa inteira é desqualificada do público.

> **Fala do Apresentador:**  
> *"Vejam o Cliente 10101: ele tem dezenas de transações normais em Reais, mas fez uma compra de US$ 12 em moeda estrangeira. A nossa regra não é descartar os 12 dólares e analisar o resto: a regra é desqualificar a pessoa. O atributo `FL_SOMENTE_BRL` fica `'N'` e ele não participa do Radar. O modelo é exclusivo para movimentações 100% em Reais."*

#### Cenário Prático 2: Exclusão por Categoria Agro
* **Perfil do Cliente:** `CD_CLI = 20202` | Data de Execução: `15/09/2026`
* **Transações:** Compras pessoais de supermercado e combustível (R$ 3.000,00) e **1 compra de insumos agrícolas** de R$ 800,00 em cooperativa (`CD_CTGR_TRAN_OGNL = 350`).
* **Comportamento no ETL:** O categorizador marca `IN_AGRO = 'S'`, gravando **`FL_TEM_MOV_AGRO = 'S'`**.
* **Decisão Negocial:** O cliente é **sumariamente excluído do Radar**.

> **Fala do Apresentador:**  
> *"Aqui está o Cliente 20202. Ele é pessoa física, mas comprou insumos agrícolas. O categorizador marcou categoria 350, gerando `FL_TEM_MOV_AGRO = 'S'`. Esse cliente sai imediatamente do Radar. Por quê? Porque o fluxo de caixa rural vive de safra e custeio. Aplicar a régua do 50/30/20 a esse cliente geraria uma recomendação sem sentido. O público Agro precisa de um produto dedicado."*

#### Cenário Prático 3: Exclusão por Inatividade no Aplicativo
* **Perfil do Cliente:** `CD_CLI = 40404` | Data de Execução: `15/09/2026`
* **Transações:** Passou o cartão físico na farmácia em 20/08 (`DT_TRAN`), mas a última vez que abriu o aplicativo do banco foi em 10/05 (`TS_INCL_TRAN`).
* **Comportamento no ETL:** A query de público filtra `TS_INCL_TRAN` entre 15/08 e 15/09. Como seu registro mais recente é de maio, **zero linhas sobrevivem**.
* **Decisão Negocial:** O cliente **não entra no público**. O processamento encerra na primeira etapa.

> **Fala do Apresentador:**  
> *"O Cliente 40404 passou o cartão físico no mercado em agosto (`DT_TRAN`), mas a última vez que abriu o aplicativo foi em maio. Como o Radar avalia o `TS_INCL_TRAN` no mês anterior, ele não pontua na porta de entrada. Ele nem chega a ser consultado em Renda ou Ciclo. Isso economiza máquina, porque não adianta entregar recomendação no app para quem não abre o canal."*

---

### Ponto de Decisão e Validação com a Mesa (Bloco 2)

*(Pausa para a mesa)*  
> **O que precisamos homologar aqui:**  
> 1. O corte rígido e inegociável tanto para moeda estrangeira quanto para agro está aprovado para proteger a coerência das recomendações?  
> 2. O critério de acesso recente ao app (`TS_INCL_TRAN` no mês anterior) é a régua definitiva de corte de entrada?

---

## Bloco 3: Identificação Cadastral (Conta BB e CPF) e Renda Obrigatória

*(Demonstrando a busca por consistência cadastral e a necessidade das chaves)*

> "Uma vez que o cliente entrou no público, o ETL precisa de duas âncoras cadastrais fundamentais: a **conta corrente no Banco do Brasil** e o **CPF**.
>
> E por que precisamos delas se já temos o código do cliente (`CD_CLI`)?  
> Porque as tabelas corporativas de **Ciclo Financeiro** e de **Renda** não são indexadas por `CD_CLI`. Elas exigem chaves específicas: a tabela de ciclo é indexada por Agência e Conta, e a tabela de renda é indexada por CPF.
>
> Por isso, ainda dentro de `DB2GFP.TRAN_RLZD_INST_PCT`, fazemos duas validações cadastrais rígidas:
>
> ---
>
> ### 1. Primeiro: verificamos a sua conta no Banco do Brasil
>
> Para que uma conta seja candidata, aplicamos os seguintes filtros:
> * O marcador de pacote de serviços Open Finance: **`NR_MCA_PCT_OPB = 999999999`**;
> * O código do produto de conta corrente: **`CD_PRD = 6`**;
> * E os atributos de agência (**`NR_AG_TITR`**) e conta (**`CD_CT_TITR`**) preenchidos, não nulos e com até 11 dígitos numéricos.
>
> **O que precisamos aqui?**  
> Precisamos que o cliente tenha **exatamente uma única conta válida** sob essas regras.
>
> **Para que servem a Agência e a Conta?**  
> Elas são a chave de ligação para cruzar com a tabela `DB2GFP.CT_GRDR_FNCO`, convertendo a agência em `CD_UOR_CC` e a conta em `NR_CC`. É essa tabela que guarda o dia de corte (`DD_INC_MM_CLC_BLC`, como dia 05, dia 10 ou dia 25). Sem saber a data de corte da conta do cliente, o ETL não sabe de qual dia até qual dia deve somar as receitas e despesas para fechar o mês financeiro dele.
>
> ---
>
> ### 2. Segundo: verificamos o CPF
>
> Olhamos o atributo **`NR_CPF_CNPJ_TITR`** e contamos os registros distintos e válidos.
>
> **O que precisamos aqui?**  
> Precisamos de **exatamente um CPF válido e único**.
>
> **Para que serve o CPF?**  
> Ele é a chave para cruzar com a tabela corporativa de renda (`DB2DFE.REN_AVLD_PF`), que não utiliza `CD_CLI`, mas sim o campo `NR_CPF_BASE_SRF`. Sem o CPF único, não temos dados suficientes para localizar a renda presumida (`VL_REN_PRES`).
>
> E a regra de negócio aqui é taxativa: **a renda presumida é obrigatória**. Se não tivermos dados suficientes para localizar o CPF único, ou se o cliente não possuir renda avaliada na base, ele é **obrigatoriamente excluído do Radar**.
>
> Vamos ver os dois casos de descarte cadastral:"

---

### Exemplos Práticos do Bloco 3

#### Cenário Prático 4: Exclusão por Ausência de Renda Presumida
* **Perfil do Cliente:** `CD_CLI = 30303` | CPF único: `123.456.789-00`
* **Comportamento no ETL:** Entrou no app, tem conta única BB, mas a busca em `DB2DFE.REN_AVLD_PF` retorna **zero registros**.
* **Decisão Negocial:** Renda presumida é obrigatória. O cliente é **obrigatoriamente excluído do Radar**.

> **Fala do Apresentador:**  
> *"No Cliente 30303, tudo parecia perfeito: ele usa o app, tem conta no BB e CPF único. Mas quando fomos à tabela `REN_AVLD_PF`, ele não tinha renda presumida cadastrada. Aqui a regra é inegociável: sem renda presumida, o cliente é excluído. A renda é o denominador da régua de gastos. Se tentássemos calcular sem renda, dividiríamos por zero e o modelo perderia a âncora de diagnóstico."*

#### Cenário Prático 5: Exclusão por Múltiplas Contas no BB
* **Perfil do Cliente:** `CD_CLI = 50505`
* **Contas Encontradas com `999999999` e produto `6`:** Agência 1234, Conta 11111-1 **e** Agência 5678, Conta 22222-2.
* **Comportamento no ETL:** Como há 2 contas ativas, o ETL seta `FL_CONTA_ELEGIVEL_UNICA = 'N'` e grava o código especial `DD_INC_MM_CLC_BLC = 996`.
* **Decisão Negocial:** O ETL **não escolhe arbitrariamente** e interrompe a geração da janela financeira.

> **Fala do Apresentador:**  
> *"O Cliente 50505 tem duas contas correntes elegíveis no BB. A regra atual não faz suposições: sem uma conta única, nós não sabemos qual ciclo de fatura usar. O ETL marca código 996 e não gera janela. Esse é um ponto que trazemos para a mesa: devemos manter esse rigor ou criar uma regra de desempate pela conta com maior movimentação?"*

---

### Ponto de Decisão e Validação com a Mesa (Bloco 3)

*(Pausa para a mesa)*  
> **O que precisamos validar:**  
> * Sem CPF único e sem renda presumida, a exclusão imediata está homologada?  
> * Para múltiplas contas, mantemos o rigor de não processar sem conta única, ou definimos uma regra de desempate?

---

## Bloco 4: Ciclo Financeiro e Janela Fechada (Inclusão com Fallback)

*(Explicando como definimos o mês financeiro do cliente sem excluir ninguém)*

> "Com a conta única confirmada, vamos responder à pergunta: **qual é o 'mês financeiro' desse cliente?**
>
> Não podemos simplesmente fechar do dia 01 ao dia 30 de forma cega para todo mundo. Cada cliente tem a sua própria data de virada de fatura e balanço.
>
> Para isso, consultamos a tabela corporativa **`DB2GFP.CT_GRDR_FNCO`**, ligando a agência em **`CD_UOR_CC`** e a conta em **`NR_CC`**.
>
> Se houver múltiplos registros históricos, ordenamos pelo timestamp mais recente no atributo **`TS_ULT_EXEA_PSQ`**. O dado que buscamos aqui é:
>
> **`DD_INC_MM_CLC_BLC`** (Dia de Início do Cálculo do Balanço)
>
> **O que precisamos aqui?**  
> Um dia válido do mês, de 1 a 31.
>
> **E aqui temos um ponto de negócio fundamental: esta etapa NÃO é de exclusão.**  
> Diferente da moeda estrangeira e do agro — onde o corte é rígido —, a ausência de ciclo financeiro cadastrado **não elimina o cliente do Radar**.
>
> A regra é muito clara e inclusiva:
> * Se o cliente tem a data de ciclo cadastrada na tabela (ex: dia 10, 15 ou 25), nós usamos o dia dele.
> * Se o cliente **não tiver** dia de ciclo registrado ou se o campo estiver vazio, **ele não é excluído**: acionamos o fallback gravando no banco o campo **`DD_INC_MM_CLC_BLC_FALLBACK = 1`**.
>
> Ou seja: ninguém fica de fora por ausência de ciclo. Adotamos o dia 1º como data de corte mensal dele e o processamento segue normalmente.
>
> ---
>
> ### A Construção da Janela: Trabalhar Exclusivamente com Ciclos Fechados
>
> Agora juntamos três variáveis: o dia do ciclo, a quantidade de ciclos solicitada e o **`TS_INCL_TRAN_REF`** (o maior timestamp de acesso encontrado no público).
>
> E aqui temos uma das decisões mais importantes de todo o projeto:  
> **O Radar só analisa ciclos financeiros fechados.**
>
> O algoritmo identifica qual ciclo estava aberto na data do `TS_INCL_TRAN_REF` e retrocede um dia para cravar o **`DT_REF_FIM`** (data final da janela). A partir dessa data final, voltamos a quantidade de ciclos solicitada para cravar o **`DT_REF_INI`** (data inicial).
>
> Não analisamos mês incompleto, porque comparar despesas de 10 dias com despesas de 30 dias distorceria completamente os indicadores. Se o dia do ciclo for 29, 30 ou 31 e o mês for menor (como Fevereiro), a regra ajusta automaticamente para o último dia existente no mês."

---

### Exemplo Prático do Bloco 4

#### Cenário Prático 6: Inclusão com Fallback de Ciclo no Dia 01
* **Perfil do Cliente:** `CD_CLI = 60606` | Conta única: Agência 3333, Conta 99999-9
* **Comportamento no ETL:** A conta foi encontrada em `DB2GFP.CT_GRDR_FNCO`, mas o atributo `DD_INC_MM_CLC_BLC` estava em branco.
* **Decisão Negocial:** **Regra de inclusão.** Grava **`DD_INC_MM_CLC_BLC_FALLBACK = 1`** e define o ciclo do dia 1º ao dia 30. O cliente permanece e é calculado normalmente.

> **Fala do Apresentador:**  
> *"No Cliente 60606, temos o exemplo perfeito da regra inclusiva: ele tem conta única, mas o sistema não tinha um dia de ciclo cadastrado. Aqui nós NÃO excluímos o cliente. O ETL adota o dia 1º como fallback (`DD_INC_MM_CLC_BLC_FALLBACK = 1`), monta a janela financeira do dia 1º ao dia 30 e calcula o Radar perfeitamente."*

---

### Ponto de Decisão e Validação com a Mesa (Bloco 4)

*(Pausa para a mesa)*  
> **O que precisamos validar:**  
> * O fallback inclusivo no dia 1º está aprovado?  
> * O princípio de analisar estritamente ciclos fechados está homologado?

---

## Bloco 5: Renda Presumida e Perfil Financeiro

*(Camada contextual: capacidade financeira e histórico de relacionamento)*

> "Com a janela temporal delimitada, buscamos duas variáveis fundamentais de contexto antes de somar os gastos:
>
> ---
>
> ### 1. Renda Presumida: Regra Obrigatória e Excludente
>
> Como vimos, **possuir Renda Presumida é obrigatório**.
>
> Usando o CPF único validado, consultamos a tabela **`DB2DFE.REN_AVLD_PF`** com o filtro:  
> **`NR_CPF_BASE_SRF = CD_CPF`**.
>
> Buscamos o registro com a maior data de inclusão no atributo **`DT_INCL_REN_AVLD`** e capturamos o valor no campo **`VL_REN`**.
>
> Se não houver registro, o cliente é descartado. Se houver, gravamos a **`VL_REN_PRES`** (Renda Presumida):  
> `VL_REN_PRES = VL_REN × quantidade de ciclos analisados`.  
> Se estamos analisando 2 ciclos, a renda de referência é duplicada; se são 3 ciclos, triplicada.
>
> *(Nota técnica: a query hoje busca a renda mais recente sem cortar por data de execução).*
>
> ---
>
> ### 2. Perfil Financeiro: Regra Também Obrigatória e Excludente
>
> E aqui temos o mesmo rigor categórico que aplicamos à renda: **possuir Perfil Financeiro é obrigatório e excludente**.
>
> Consultamos a tabela corporativa **`DB2D1D.DVS_GRDR_FNCO_PF`** filtrando pelo `CD_CLI` e com data **`DT_REF <= DT_EXEA`**.
>
> Selecionamos o registro mais recente pela maior `DT_REF` e extraímos o macroperfil no atributo **`CD_MAC_PRFL_CLI`**:
> * **`1` = Endividado**
> * **`2` = Equilibrista**
> * **`3` = Investidor**
>
> **E o que acontece se o cliente não tiver perfil cadastrado, ou se o código estiver nulo ou fora de 1, 2 ou 3?**  
> **O cliente é obrigatoriamente excluído do Radar.**
>
> Não existe a possibilidade de prosseguir com perfil nulo ou zerado.  
> *Por que essa decisão é inegociável para o negócio?*  
> Porque o macroperfil histórico é um dos três pilares que sustentam a pontuação do nosso motor de decisão. Ele traz o peso do comportamento histórico consolidado do cliente no banco. Sem o perfil, o motor perde uma das suas três pernas analíticas, fica descalibrado e não podemos emitir uma recomendação às cegas.
>
> *(O microperfil `CD_MIC_PRFL_CLI` também é capturado como metadado de contexto explicativo, mas quem comanda a validação e pontua no motor é o macroperfil).*
>
> Vamos ver o exemplo prático de descarte por falta de perfil:"
>
> ---
>
> ### Exemplo Prático do Bloco 5
>
> #### Cenário Prático 5B: Exclusão por Ausência de Perfil Financeiro
> * **Perfil do Cliente:** `CD_CLI = 35353` | CPF, Conta BB única e Renda Presumida (R$ 7.000,00) válidos.
> * **Comportamento no ETL:** A consulta em `DB2D1D.DVS_GRDR_FNCO_PF` com `DT_REF <= DT_EXEA` retorna zero registros, ou o campo `CD_MAC_PRFL_CLI` está nulo / fora de 1, 2 e 3.
> * **Decisão Negocial:** **Regra obrigatória e excludente.** O cliente é **sumariamente excluído do Radar**.
>
> > **Fala do Apresentador:**  
> > *"Vejam o Cliente 35353: ele tem conta, tem renda de R$ 7.000 e movimentação regular. Porém, ao consultar a tabela de perfil `DVS_GRDR_FNCO_PF`, ele não tem macroperfil histórico vigente ou o código veio nulo. A nossa regra de negócio é enfática: sem macroperfil (1, 2 ou 3), o cliente não participa do Radar. O perfil é um dos três pilares do motor. Sem ele, a pontuação ficaria manca e não assumimos o risco de emitir um diagnóstico descalibrado."*
>
> ---
>
> ### Ponto de Decisão e Validação com a Mesa (Bloco 5)
>
> *(Pausa para a mesa)*  
> **O que precisamos homologar aqui:**  
> 1. A regra de que possuir Perfil Financeiro (`CD_MAC_PRFL_CLI` 1, 2 ou 3) é **obrigatório e excludente** (cliente sumariamente descartado se ausente) está aprovada?  
> 2. A busca da renda mais recente disponível sem corte por data de execução está homologada?  
> 3. A multiplicação da renda mensal pela quantidade de ciclos atende à expectativa?

---

## Bloco 6: Captura Transacional e Reconciliação (Higienização de Dados)

*(O grande diferencial técnico do ETL para evitar valores inflados por transferências próprias)*

> "Agora voltamos à tabela de transações `DB2GFP.TRAN_RLZD_INST_PCT` para coletar créditos e débitos daquele cliente.
>
> Mas nós **não** buscamos apenas o período estrito de `DT_REF_INI` a `DT_REF_FIM`. Nós aplicamos uma margem de segurança de **5 dias antes e 5 dias depois**:
>
> `WHERE DT_TRAN BETWEEN (DT_REF_INI - 5 dias) AND (DT_REF_FIM + 5 dias)`
>
> Filtramos:
> * Transações ativas: `CD_EST_TRAN_INST = 0`;
> * Créditos: **`CD_NTZ_CTB_TRAN = 'C'`**;
> * Débitos: **`CD_NTZ_CTB_TRAN = 'D'`** exigindo obrigatoriamente o indicador de consumo **`IN_VSLO_CSM = 'S'`**.
>
> ---
>
> ### O Que É a Reconciliação?
>
> Se somássemos todas as entradas e saídas sem higienização, cometeríamos um erro grave. Imagine um cliente que transfere R$ 2.000 da sua conta no BB para a sua conta no Nubank via Pix. Entrou R$ 2.000 num banco e saiu R$ 2.000 no outro. Ele não ficou R$ 2.000 mais rico nem gastou R$ 2.000 em consumo: foi uma simples transferência entre contas próprias.
>
> Para neutralizar essas distorções, o ETL roda dois algoritmos de pareamento:
>
> 1. **Par Exato:**  
>    Busca um crédito e um débito com mesmo `CD_CLI`, mesma data (`DT_TRAN`), mesmo valor (`VL_TRAN`), mesma moeda, naturezas opostas (`C` e `D`), ambos dentro ou ambos fora da janela, e com instituições financeiras diferentes.  
>    *Efeito:* **Ambas as movimentações são consumidas e saem dos cálculos.**
>
> 2. **Par de Borda:**  
>    Depois dos pares exatos, olhamos os movimentos restantes. Se houver um movimento dentro da janela e uma contraparte idêntica fora da janela com diferença de **1 a 5 dias** entre bancos diferentes, entendemos que foi uma transferência em trânsito na virada do ciclo.  
>    *Efeito:* **A movimentação interna é anulada**, e a movimentação externa é descartada sem nunca entrar no orçamento.
>
> Somente os movimentos que sobrevivem a esse pareamento e estão dentro da janela oficial tornam-se **movimentações efetivas**."

---

### Exemplo Prático do Bloco 6

#### Cenário Prático 7: Reconciliação de Par Exato (Transferência entre Contas Próprias)
* **Perfil do Cliente:** `CD_CLI = 70707` | Janela: `10/07/2026` a `09/08/2026`
* **Transações em 22/07/2026:**
  * Débito de R$ 1.500,00 no BB (`VL_TRAN = 1500.00`, `CD_NTZ_CTB_TRAN = 'D'`).
  * Crédito de R$ 1.500,00 via Pix no Nubank (`VL_TRAN = 1500.00`, `CD_NTZ_CTB_TRAN = 'C'`).
* **Comportamento no ETL:** O algoritmo de Par Exato identifica mesmo cliente, data, valor, moeda e naturezas opostas em bancos diferentes.
* **Decisão Negocial:** **Ambas as movimentações são consumidas.** Zero impacto em entradas e zero impacto em saídas.

> **Fala do Apresentador:**  
> *"Olhem o Cliente 70707: no dia 22 de Julho, saíram R$ 1.500 da conta dele no BB e entraram R$ 1.500 no Nubank via Pix. Se somássemos isso cegamente, pareceria que ele teve R$ 1.500 de despesa e R$ 1.500 de renda. O algoritmo de Par Exato casa esses dois movimentos e anula ambos. Somente gastos reais com terceiros passam para o cálculo."*

---

### Ponto de Decisão e Validação com a Mesa (Bloco 6)

*(Pausa para a mesa)*  
> **O que precisamos validar:**  
> * A margem de tolerância de 5 dias de borda é suficiente para acomodar feriados e fins de semana?  
> * A regra de débito exigir `IN_VSLO_CSM = 'S'` está aprovada?

---

## Bloco 7: Categorização, Agregação e Faixas Orçamentárias

*(Como os gastos individuais são classificados e totalizados)*

> "Cada movimentação efetiva passa pelo nosso mapa de categorização, cruzando a categoria original (**`CD_CTGR_TRAN_OGNL`**) com a natureza contábil (**`CD_NTZ_CTB_TRAN`**).
>
> Esse mapa associa cada registro a uma classe analítica e define duas flags booleanas fundamentais:
>
> 1. **`IN_PARTICIPA_CALCULO = 'S'`**: determina se o valor participa da análise temática das 10 classes do Radar:
>    * **Entradas (Classes 0 a 4):** `VL_ENT_OUT` (Outras), `VL_ENT_REN` (Renda), `VL_ENT_EST` (Estorno), `VL_ENT_RESG` (Resgate), `VL_ENT_CRED` (Crédito).
>    * **Saídas (Classes 5 a 9):**  
>      * Classe 5: **`VL_SAI_IND`** (Indeterminadas / Sem Categoria)  
>      * Classe 6: **`VL_SAI_ESS`** (Essenciais: água, luz, mercado, farmácia)  
>      * Classe 7: **`VL_SAI_NAO_ESS`** (Não Essenciais: lazer, streaming, vestuário)  
>      * Classe 8: **`VL_SAI_FUT`** (Futuro: aplicações, previdência, poupança)  
>      * Classe 9: **`VL_SAI_OBR`** (Obrigações: parcelas, empréstimos, faturas)
>
> 2. **`IN_PARTICIPA_ORCAMENTO = 'S'`**: determina se o valor entra na conta orçamentária macro, formando os atributos **`VL_ENT_TOTAL`** e **`VL_SAI_TOTAL`**.
>
> Se uma transação não encontrar correspondência no mapa, ela recebe a etiqueta *'Sem Categoria'*, classe 0, com ambas as flags setadas em `'N'`. Ela fica visível para auditoria e explicabilidade, mas não afeta o cálculo.
>
> ---
>
> ### As Flags Físicas de Sentinela: Moeda e Agro
>
> Na consolidação dos movimentos, o ETL monitora duas colunas booleanas que confirmam as regras de exclusão:
> * **`FL_SOMENTE_BRL`:** se houver qualquer transação em outra moeda, grava `'N'` e o cliente é desqualificado do Radar.
> * **`FL_TEM_MOV_AGRO`:** se houver qualquer transação em rubricas agro, grava `'S'` e o cliente é sumariamente excluído.
>
> ---
>
> ### O Resultado e a Faixa Orçamentária
>
> A partir dos totais orçamentários, calculamos:
> * O resultado financeiro: **`VL_RES_ORC = VL_ENT_TOTAL - VL_SAI_TOTAL`**;
> * A razão entre saídas e entradas: **`PC_SAI_ENT = VL_SAI_TOTAL / VL_ENT_TOTAL`**.
>
> Essa razão gera o código da faixa orçamentária (**`CD_FAIXA_ORC`**):
> * **`0` = Neutro:** saídas entre 95% e 105% das entradas (orçamento em equilíbrio);
> * **`1` = Deficitário Moderado:** saídas entre 105% e 125%;
> * **`2` = Deficitário Acentuado:** saídas superiores a 125% das entradas;
> * **`3` = Superavitário Moderado:** saídas entre 75% e 95%;
> * **`4` = Superavitário Acentuado:** saídas abaixo de 75% das entradas (sobra de caixa expressiva)."

---

### Ponto de Decisão e Validação com a Mesa (Bloco 7)

*(Pausa para a mesa)*  
> **O que precisamos validar:**  
> * As faixas orçamentárias (75%, 95%, 105% e 125%) estão homologadas?  
> * O tratamento de transações não mapeadas como neutras (sem peso no orçamento) está aprovado?

---

## Bloco 8: O Motor de Decisão — Como Chegamos aos 5 Públicos

*(O momento decisivo: como o dado se transforma em um dos 5 públicos-alvo)*

> "Agora chegamos ao objetivo central do ETL: classificar o cliente em um dos **cinco públicos**.
>
> Essa atribuição resulta de uma matriz de pontuação estruturada em **três forças independentes**:
>
> ---
>
> ### Força 1: Pontuação de Concentração
>
> Calculamos o percentual que cada grupo de saída representou sobre a **renda presumida** (`VL_REN_PRES`), adaptando as referências consagradas de educação financeira:
>
> * **Essenciais (`PC_SAI_ESS`):** referência 50%. Abaixo de 50% = 0 pts; de 50% a 75% = 1 pt; 75% ou mais = 2 pts.
> * **Não Essenciais (`PC_SAI_NAO_ESS`):** referência 30%. Abaixo de 30% = 0 pts; de 30% a 45% = 1 pt; 45% ou mais = 2 pts.
> * **Obrigações / Crédito (`PC_SAI_OBR`):** referência 30%. Abaixo de 30% = 0 pts; de 30% a 45% = 1 pt; 45% ou mais = 2 pts.
> * **Futuro / Reserva (`PC_SAI_FUT`):** aqui a lógica é **invertida**: guardar mais de 30% é ótimo, então pontua 0; entre 20% e 30% pontua 1; abaixo de 20% pontua 2 (precisa de orientação).
>
> **A Regra de Exceção Máxima (Trava dos Indeterminados):**  
> Se as despesas sem categoria ultrapassarem 75% do total (`PC_SAI_IND > 0.75`), o atributo **`NR_PONT_CONC_IND` recebe o valor fixo `99`**.  
> Por que isso existe? Porque se mais de 75% dos gastos do cliente não têm classificação conhecida, não faz sentido orientá-lo sobre poupança ou crédito. A prioridade absoluta dele tem que ser categorizar para entender onde o dinheiro está indo.
>
> ---
>
> ### Força 2: Pontuação Orçamentária
>
> A faixa orçamentária (`CD_FAIXA_ORC`) injeta pontos adicionais de contexto:
> * Se o cliente fechou **Deficitário Acentuado**, temas como *Gestão de Orçamento* e *Uso do Crédito* ganham 2 pontos.
> * Se fechou **Superavitário Acentuado**, o tema *Formação de Reserva* ganha 2 pontos.
> * O tema Indeterminado não recebe pontuação orçamentária (pontua 0).
>
> ---
>
> ### Força 3: Pontuação de Perfil
>
> O macroperfil do cliente (`CD_MAC_PRFL_CLI`) adiciona a calibragem histórica:
> * **Macroperfil 1 (Endividado):** soma +2 pontos em *Uso Consciente do Crédito* e +1 em *Consumo Planejado*.
> * **Macroperfil 2 (Equilibrista):** soma +1 ponto em *Gestão de Orçamento* e +1 em *Formação de Reserva*.
> * **Macroperfil 3 (Investidor):** soma +2 pontos em *Formação de Reserva* e +1 em *Gestão de Orçamento*.
>
> ---
>
> ### A Pontuação Final e o Tema Vencedor
>
> O ETL soma as três parcelas para cada um dos cinco temas e armazena o valor mais alto no campo **`NR_PONT_MAX`**.
>
> A coluna final **`CD_TEMA_VENCEDOR`** recebe o código do público:
>
> * **`1` = Categorização dos Gastos** (sempre vence se bateu a trava de 99);
> * **`2` = Gestão de Orçamento** (foco em despesas essenciais e reequilíbrio);
> * **`3` = Consumo Planejado** (foco em gastos não essenciais e compras recorrentes);
> * **`4` = Formação de Reserva** (foco em iniciar ou expandir investimentos);
> * **`5` = Uso Consciente do Crédito** (foco no peso de dívidas e financiamentos);
> * **`9` = Empate:** caso dois ou mais temas atinjam rigorosamente a mesma pontuação máxima (`QT_TEMAS_PONT_MAX > 1`).
>
> Vamos ver agora um exemplo prático completo de cada um dos 5 públicos e de um caso de empate técnico:"

---

### Exemplos Práticos dos 5 Públicos-Alvo e Empate (Bloco 8)

#### Cenário Prático 8: Público 1 — Categorização dos Gastos (Trava dos 75% com Nota 99)
* **Dados do Cliente:** `CD_CLI = 80808` | Renda Presumida: `R$ 5.000,00` | Saídas: `R$ 4.000,00`
* **Composição das Saídas:**
  * R$ 3.200,00 em transferências Pix genéricas sem categorização (`VL_SAI_IND`).
  * `PC_SAI_IND = 3.200 / 4.000 = 80%` (ultrapassou o limite de 75%).
* **Pontuação no Motor:**
  * `NR_PONT_CONC_IND = 99` (trava máxima ativada). Demais temas pontuam entre 0 e 4.
* **Resultado:** **`CD_TEMA_VENCEDOR = 1` (Categorização dos Gastos)**.

> **Fala do Apresentador:**  
> *"No Cliente 80808, 80% do dinheiro dele saiu por Pix genérico sem categoria. A trava de exceção foi disparada: o tema Indeterminado recebeu pontuação direta 99 (`NR_PONT_CONC_IND = 99`). Ele vira automaticamente Público 1: Categorização dos Gastos. Antes de ensiná-lo a investir ou cortar luz, precisamos ajudá-lo a descobrir para onde o dinheiro está indo."*

#### Cenário Prático 9: Público 2 — Gestão de Orçamento (Estouro em Essenciais e Déficit)
* **Dados do Cliente:** `CD_CLI = 90909` | Renda Presumida: `R$ 4.000,00`
* **Balanço:** Entradas: R$ 4.000,00 | Saídas: R$ 4.600,00 (Déficit de 115% $\rightarrow$ `CD_FAIXA_ORC = 1` - Deficitário Moderado).
* **Composição:** Essenciais: R$ 2.600,00 (65% da renda $\rightarrow$ 1 pt na faixa 50%-75%).
* **Macroperfil:** `2` (Equilibrista $\rightarrow$ +1 pt em Essenciais).
* **Pontuação:** Concentração (1) + Orçamento Deficitário (1) + Perfil (1) = **3 pontos** (nota máxima).
* **Resultado:** **`CD_TEMA_VENCEDOR = 2` (Gestão de Orçamento)**.

> **Fala do Apresentador:**  
> *"O Cliente 90909 gastou 65% da renda em contas básicas (água, feira, remédio) e fechou o mês no vermelho com 115% de despesas. A concentração alta em essenciais somada ao déficit moderado e ao perfil equilibrista colocou o tema Gestão de Orçamento no topo. A recomendação aqui é renegociar despesas fixas e reequilibrar o caixa."*

#### Cenário Prático 10: Público 3 — Consumo Planejado (Gastos Flexíveis Elevados)
* **Dados do Cliente:** `CD_CLI = 10111` | Renda Presumida: `R$ 6.000,00`
* **Balanço:** Entradas: R$ 6.000,00 | Saídas: R$ 5.800,00 (Orçamento Neutro / Equilíbrio $\rightarrow$ 1 pt).
* **Composição:** Essenciais controlados (40%), mas **R$ 2.600,00 em Não Essenciais** (lazer, delivery, streaming $\rightarrow$ `43,3%` da renda $\rightarrow$ 1 pt na faixa 30%-45%).
* **Macroperfil:** `1` (Endividado $\rightarrow$ +1 pt em Consumo Planejado).
* **Pontuação:** Concentração (1) + Orçamento (1) + Perfil (1) = **3 pontos** (vencedor).
* **Resultado:** **`CD_TEMA_VENCEDOR = 3` (Consumo Planejado)**.

> **Fala do Apresentador:**  
> *"O Cliente 10111 está com as contas básicas em dia, mas comprometeu mais de 43% da renda com lazer, compras recorrentes e restaurantes — bem acima da referência de 30%. O tema Consumo Planejado venceu a pontuação. O objetivo do insight é provocar a reflexão sobre compras impulsivas e escolhas de consumo."*

#### Cenário Prático 11: Público 4 — Formação de Reserva (Superávit com Baixa Poupança)
* **Dados do Cliente:** `CD_CLI = 11122` | Renda Presumida: `R$ 8.000,00`
* **Balanço:** Entradas: R$ 8.000,00 | Saídas: R$ 5.200,00 (gastou apenas 65% $\rightarrow$ `CD_FAIXA_ORC = 4` - Superavitário Acentuado $\rightarrow$ **2 pts** em Futuro).
* **Composição:** Guardou apenas R$ 600,00 em poupança (`7,5%` da renda $\rightarrow$ abaixo de 20% na régua invertida $\rightarrow$ **2 pts**).
* **Macroperfil:** `3` (Investidor $\rightarrow$ **+2 pts** em Futuro).
* **Pontuação:** Concentração (2) + Superávit Acentuado (2) + Perfil (2) = **6 pontos** (nota máxima).
* **Resultado:** **`CD_TEMA_VENCEDOR = 4` (Formação de Reserva)**.

> **Fala do Apresentador:**  
> *"O Cliente 11122 tem uma excelente sobra de caixa: gastou apenas 65% do que ganhou, sobrando R$ 2.800 no mês. Porém, ele só guardou R$ 600 (menos de 10% da renda). Como a régua de reserva é invertida, guardar pouco dá pontuação máxima de necessidade. Somado ao superávit e ao perfil Investidor, ele bateu 6 pontos. Esse cliente é o público ideal para ser incentivado a criar uma reserva de emergência ou aplicar em CDB/fundos."*

#### Cenário Prático 12: Público 5 — Uso Consciente do Crédito (Endividamento Excessivo)
* **Dados do Cliente:** `CD_CLI = 12133` | Renda Presumida: `R$ 5.000,00`
* **Composição:** R$ 2.300,00 comprometidos com faturas de cartão e parcelas de empréstimo (`PC_SAI_OBR = 46%` $\rightarrow$ acima de 45% = **2 pts**).
* **Balanço:** Orçamento Deficitário Moderado $\rightarrow$ **1 pt** em Obrigações.
* **Macroperfil:** `1` (Endividado $\rightarrow$ **+2 pts** em Obrigações).
* **Pontuação:** Concentração (2) + Orçamento (1) + Perfil (2) = **5 pontos** (vencedor absoluto).
* **Resultado:** **`CD_TEMA_VENCEDOR = 5` (Uso Consciente do Crédito)**.

> **Fala do Apresentador:**  
> *"O Cliente 12133 comprometeu 46% da sua renda com parcelas de empréstimo e cartão — quase metade do salário. Ele fechou o mês deficitário e já tem perfil de endividamento. O tema Uso Consciente do Crédito cravou 5 pontos e foi o vencedor absoluto. A orientação para ele é educativa e preventiva: entender o custo do crédito e reorganizar o fluxo de dívidas."*

#### Cenário Prático 13: Código 9 — Empate Técnico entre Temas
* **Dados do Cliente:** `CD_CLI = 13144`
* **Pontuações:** Gestão de Orçamento = **4 pontos** | Uso Consciente do Crédito = **4 pontos** (demais temas com pontuação inferior).
* **Atributos de Auditoria:** `NR_PONT_MAX = 4` e `QT_TEMAS_PONT_MAX = 2`.
* **Comportamento no ETL:** O pipeline não joga moeda. Grava **`CD_TEMA_VENCEDOR = 9` (Empate)**.

> **Fala do Apresentador:**  
> *"E aqui temos o caso do Cliente 13144: ele pontuou 4 tanto em Gestão de Orçamento quanto em Uso do Crédito. O ETL não escolhe no palpite. Ele grava `CD_TEMA_VENCEDOR = 9` (Empate). O dado fica perfeitamente auditável e o critério de desempate final pode ser definido na estratégia de acionamento do canal CRM."*

---

### Ponto de Decisão e Validação com a Mesa (Bloco 8)

*(Pausa para a mesa)*  
> **O que precisamos validar:**  
> * A regra de exceção com nota 99 para despesas indeterminadas acima de 75% atende à estratégia do banco?  
> * A matriz de bônus dos macroperfis 1, 2 e 3 está calibrada com a visão de negócio?  
> * Em caso de empate (código 9), qual critério de desempate deve ser acionado na esteira de CRM?

---

## Bloco 9: Os Três Cenários Comparativos

*(Robustez analítica: como o ETL entrega três visões do mesmo cliente no mesmo lote)*

> "Para garantir que o negócio tenha flexibilidade de testar e comparar hipóteses, o pipeline grava na tabela final `ANA_RADAR_FIN_CLI` o resultado oficial e **dois cenários alternativos recalculados em lote**:
>
> 1. **Resultado Oficial:** usa entradas realizadas participantes para fechar o orçamento e a renda presumida para calcular os percentuais de concentração.
> 2. **Cenário Renda Presumida (`_RENDA_PRESUMIDA`):** recalcula o motor inteiro utilizando exclusivamente a renda presumida como base tanto para o orçamento quanto para as despesas. É a visão de *capacidade teórica*.
> 3. **Cenário Entradas Realizadas (`_ENTRADAS_REALIZADAS`):** recalcula o motor utilizando a soma real de créditos classificados em BRL como base de tudo. É a visão de *caixa estrito*.
>
> Com isso, a área de negócios consegue simular o impacto de migrar a régua de um cenário para outro sem precisar reprocessar um único byte de transação."

---

## Bloco 10: Encerramento, Ata de Votação e Guia Visual de Apoio

*(Fechamento formal chamando a mesa para a aprovação das regras)*

> "Para encerrar: o Radar não é um modelo intuitivo ou subjetivo.
>
> Ele é um **ETL robusto, rastreável e auditável**. Para qualquer um dos milhões de clientes que cair no público de Crédito, de Orçamento ou de Reserva, nós temos no banco a linha exata que mostra a conta elegível, a data do ciclo, as movimentações anuladas e a pontuação detalhada de cada pilar.
>
> Nós preparamos uma ata com as decisões que discutimos hoje para colher a validação formal de vocês em três status: **Aprovado**, **Alterar** ou **Investigar**:
>
> 1. **Regra de Moeda:** Exclusão total do cliente caso possua qualquer transação em moeda estrangeira (`FL_SOMENTE_BRL = 'N'`);
> 2. **Regra Agro:** Exclusão total do cliente caso possua qualquer movimentação em categorias agro (`FL_TEM_MOV_AGRO = 'S'`);
> 3. **Porta de Entrada:** Janela de acesso ao app (`TS_INCL_TRAN`) no mês anterior como corte de entrada no público;
> 4. **Consistência Cadastral:** Exigência de par único de Agência e Conta no BB (`999999999` e produto `6`) e CPF único;
> 5. **Ciclo Financeiro:** Fallback do dia do ciclo para o dia 1º em contas sem data de corte cadastrada (**regra inclusiva, não exclui**);
> 6. **Régua Temporal:** Delimitação temporal restrita exclusivamente a ciclos financeiros fechados;
> 7. **Renda Obrigatória:** Exclusão obrigatória do cliente caso não possua renda presumida ou dados suficientes para localizá-la em `REN_AVLD_PF`;
> 8. **Perfil Financeiro Obrigatório:** Exclusão obrigatória do cliente caso não possua macroperfil financeiro válido (`CD_MAC_PRFL_CLI` igual a 1, 2 ou 3) em `DVS_GRDR_FNCO_PF`;
> 9. **Higienização:** Regra de reconciliação de pares de borda com tolerância de $\pm 5$ dias para anular transferências entre contas próprias;
> 10. **Faixas Orçamentárias:** As 5 faixas de `CD_FAIXA_ORC` (Neutro 95%-105%, Deficitário e Superavitário);
> 11. **Trava dos Indeterminados:** Atribuição da nota de exceção 99 para despesas sem categoria acima de 75%;
> 12. **Matriz de Macroperfis:** Pesos dos Macroperfis 1 (Endividado), 2 (Equilibrista) e 3 (Investidor);
> 13. **Tratamento de Empates:** Encaminhamento negocial em caso de código 9 (Empate).
>
> Muito obrigado pela atenção de todos. Passo a palavra para passarmos ponto a ponto da ata."

---

## Guia Visual de Apoio ao Apresentador

| Bloco | Assunto Principal | Tabelas Envolvidas | Atributos-Chave | Decisão Crítica de Negócio | Cenário Prático Associado |
|:---:|---|---|---|---|---|
| **01** | Enquadramento | — | — | ETL determinístico de público-alvo (não estudo exploratório). | — |
| **02** | Entrada & Exclusões | `TRAN_RLZD_INST_PCT` | `CD_TIP_MOE_CRR`, `TS_INCL_TRAN`, `CD_EST_TRAN_INST`, `CD_TIP_PSS` | **Exclusão total do cliente** se tiver moeda estrangeira ou agro. Entrada pelo acesso ao app (`TS_INCL_TRAN`). | **Cenários 1, 2 e 3** (Moeda, Agro, Inatividade App) |
| **03** | Conta e CPF | `TRAN_RLZD_INST_PCT` | `NR_MCA_PCT_OPB`, `CD_PRD`, `NR_AG_TITR`, `CD_CT_TITR`, `NR_CPF_CNPJ_TITR` | Exigência de unicidade cadastral absoluta (1 conta BB e 1 CPF) para viabilizar ciclo e renda. | **Cenários 4 e 5** (Renda Ausente e Duas Contas) |
| **04** | Ciclo e Janela | `CT_GRDR_FNCO` | `CD_UOR_CC`, `NR_CC`, `DD_INC_MM_CLC_BLC`, `DD_INC_MM_CLC_BLC_FALLBACK`, `TS_INCL_TRAN_REF` | Fallback para dia 1º (**não exclui**) e análise estrita de **ciclos fechados**. | **Cenário 6** (Fallback Dia 01) |
| **05** | Renda & Perfil | `REN_AVLD_PF`, `DVS_GRDR_FNCO_PF` | `NR_CPF_BASE_SRF`, `VL_REN`, `VL_REN_PRES`, `CD_MAC_PRFL_CLI`, `CD_MIC_PRFL_CLI` | **Renda presumida e Perfil Financeiro são obrigatórios e excludentes** (sem eles, o cliente é sumariamente descartado). Renda multiplicada por ciclos; macroperfis 1, 2, 3. | **Cenário 5B** (Exclusão por Falta de Perfil) e integrado aos Cenários 8 a 12 |
| **06** | Reconciliação | `TRAN_RLZD_INST_PCT` | `DT_TRAN`, `VL_TRAN`, `CD_NTZ_CTB_TRAN`, `IN_VSLO_CSM` | Tolerância de $\pm 5$ dias para anular transferências próprias (pares exatos e bordas). | **Cenário 7** (Par Exato BB $\rightarrow$ Nubank) |
| **07** | Orçamento & Flags | Mapa de Categorias | `IN_PARTICIPA_CALCULO`, `IN_PARTICIPA_ORCAMENTO`, `FL_SOMENTE_BRL`, `FL_TEM_MOV_AGRO`, `CD_FAIXA_ORC` | Se `FL_SOMENTE_BRL = 'N'` ou `FL_TEM_MOV_AGRO = 'S'`, o cliente é desqualificado do Radar. 5 faixas orçamentárias. | — |
| **08** | Os 5 Públicos | Motor de Pontuação | `NR_PONT_CONC_*`, `NR_PONT_ORC_*`, `NR_PONT_PRFL_*`, `NR_PONT_MAX`, `CD_TEMA_VENCEDOR` | Trava de nota 99 para Indeterminado > 75%; atribuição dos públicos 1 a 5 ou 9 (Empate). | **Cenários 8 a 13** (Os 5 Públicos e Empate) |
| **09** | Cenários | `ANA_RADAR_FIN_CLI` | Sufixos `_RENDA_PRESUMIDA` e `_ENTRADAS_REALIZADAS` | Entrega de 3 visões do cliente no mesmo grão. | — |
| **10** | Deliberação | Ata de Decisões | — | Validação formal item a item: *Aprovado / Alterar / Investigar*. | Ata com os 13 itens |
