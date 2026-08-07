---
title: "Catálogo de Categorias de Transações"
source: "CATEGORIAS(1).txt"
document_type: "catálogo estruturado"
total_categories: 71
total_groups: 15
---

# Catálogo de Categorias de Transações

> Versão estruturada em Markdown a partir do arquivo-fonte. O conteúdo das regras foi preservado. A edição reorganiza os registros para consulta, sem corrigir silenciosamente possíveis inconsistências do material original.

## Visão geral

- **Quantidade de grupos:** 15
- **Quantidade de categorias:** 71
- **Organização:** grupos de transações → categorias → definição → inclusões → exclusões → observações.
- **Uso sugerido:** consulta funcional, revisão de regras de classificação e apoio à documentação técnica.

## Estrutura dos campos originais

| Campo original | Significado no documento |
|---|---|
| `CD_GR_CTGR_TRAN` | Código do grupo de categoria da transação |
| `TX_DCR_GR_CTGR` | Nome ou descrição do grupo |
| `CD_CTGR_TRAN` | Código da categoria da transação |
| `TX_DCR_CTGR_TRAN` | Nome ou descrição da categoria |
| `Nota de definição/conceito` | Regra funcional, exemplos, inclusões, exclusões e observações |

## Índice de grupos

| Código | Grupo | Quantidade de categorias |
|---:|---|---:|
| `0` | [Sem categoria](#grupo-0-sem-categoria) | 2 |
| `1` | [Receitas](#grupo-1-receitas) | 5 |
| `2` | [Casa](#grupo-2-casa) | 9 |
| `3` | [Educação](#grupo-3-educacao) | 5 |
| `4` | [Lazer](#grupo-4-lazer) | 5 |
| `5` | [Saúde](#grupo-5-saude) | 4 |
| `6` | [Alimentação](#grupo-6-alimentacao) | 2 |
| `7` | [Transporte](#grupo-7-transporte) | 6 |
| `8` | [Despesas Pessoais](#grupo-8-despesas-pessoais) | 10 |
| `9` | [Comunicação](#grupo-9-comunicacao) | 2 |
| `10` | [Tarifas e impostos](#grupo-10-tarifas-e-impostos) | 8 |
| `12` | [Fatura](#grupo-12-fatura) | 1 |
| `11` | [Outros](#grupo-11-outros) | 5 |
| `14` | [Agro](#grupo-14-agro) | 5 |
| `13` | [Investimentos](#grupo-13-investimentos) | 2 |

## Índice rápido de categorias

| Grupo | Código | Categoria |
|---|---:|---|
| Sem categoria | `0` | [Sem categoria](#categoria-0-sem-categoria) |
| Sem categoria | `83` | [Sem categoria](#categoria-83-sem-categoria) |
| Receitas | `1` | [Salário](#categoria-1-salario) |
| Receitas | `2` | [Vale Alimentação](#categoria-2-vale-alimentacao) |
| Receitas | `3` | [Restituição de IR](#categoria-3-restituicao-de-ir) |
| Receitas | `4` | [Bonificação](#categoria-4-bonificacao) |
| Receitas | `5` | [Outros Rendimentos](#categoria-5-outros-rendimentos) |
| Casa | `6` | [Água](#categoria-6-agua) |
| Casa | `7` | [Eletricidade e Gás](#categoria-7-eletricidade-e-gas) |
| Casa | `9` | [Compra de Imóvel](#categoria-9-compra-de-imovel) |
| Casa | `10` | [Aluguel e Condomínio](#categoria-10-aluguel-e-condominio) |
| Casa | `11` | [Móveis e Utensílios](#categoria-11-moveis-e-utensilios) |
| Casa | `12` | [Serviços e Manutenção](#categoria-12-servicos-e-manutencao) |
| Casa | `13` | [Empregados](#categoria-13-empregados) |
| Casa | `14` | [Animais e Pets](#categoria-14-animais-e-pets) |
| Casa | `3790` | [Seguro Residencial](#categoria-3790-seguro-residencial) |
| Educação | `15` | [Educação Superior](#categoria-15-educacao-superior) |
| Educação | `16` | [Colégio](#categoria-16-colegio) |
| Educação | `17` | [Idiomas](#categoria-17-idiomas) |
| Educação | `18` | [Publicações e Papelaria](#categoria-18-publicacoes-e-papelaria) |
| Educação | `20` | [Outros Gastos](#categoria-20-outros-gastos) |
| Lazer | `21` | [Viagens e Lazer](#categoria-21-viagens-e-lazer) |
| Lazer | `22` | [Esportes e Academia](#categoria-22-esportes-e-academia) |
| Lazer | `25` | [Cultura e Entretenimento](#categoria-25-cultura-e-entretenimento) |
| Lazer | `26` | [Publicações Digitais](#categoria-26-publicacoes-digitais) |
| Lazer | `61` | [Jogos e Loterias](#categoria-61-jogos-e-loterias) |
| Saúde | `27` | [Plano de Saúde](#categoria-27-plano-de-saude) |
| Saúde | `28` | [Serviços de Saúde](#categoria-28-servicos-de-saude) |
| Saúde | `29` | [Dentista](#categoria-29-dentista) |
| Saúde | `30` | [Farmácias e Drogarias](#categoria-30-farmacias-e-drogarias) |
| Alimentação | `32` | [Feira e Supermercado](#categoria-32-feira-e-supermercado) |
| Alimentação | `35` | [Bar](#categoria-35-bar) |
| Transporte | `36` | [Compra de Veículo](#categoria-36-compra-de-veiculo) |
| Transporte | `37` | [Combustível](#categoria-37-combustivel) |
| Transporte | `38` | [Estacionamento e Pedágio](#categoria-38-estacionamento-e-pedagio) |
| Transporte | `39` | [Seguro de Veículo](#categoria-39-seguro-de-veiculo) |
| Transporte | `40` | [Serviços e Manutenção](#categoria-40-servicos-e-manutencao) |
| Transporte | `41` | [Transporte Urbano e Apps](#categoria-41-transporte-urbano-e-apps) |
| Despesas Pessoais | `42` | [Vestuário e Acessórios](#categoria-42-vestuario-e-acessorios) |
| Despesas Pessoais | `43` | [Cuidado Pessoal e Beleza](#categoria-43-cuidado-pessoal-e-beleza) |
| Despesas Pessoais | `44` | [Compras Diversas](#categoria-44-compras-diversas) |
| Despesas Pessoais | `45` | [Pensão Alimentícia](#categoria-45-pensao-alimenticia) |
| Despesas Pessoais | `46` | [Seguros e Previdência](#categoria-46-seguros-e-previdencia) |
| Despesas Pessoais | `47` | [Doação](#categoria-47-doacao) |
| Despesas Pessoais | `48` | [Gasto com Familiares](#categoria-48-gasto-com-familiares) |
| Despesas Pessoais | `49` | [Presentes](#categoria-49-presentes) |
| Despesas Pessoais | `60` | [Serviços Diversos](#categoria-60-servicos-diversos) |
| Despesas Pessoais | `4417` | [Empréstimos e Prestações](#categoria-4417-emprestimos-e-prestacoes) |
| Comunicação | `51` | [Telefonia e Internet](#categoria-51-telefonia-e-internet) |
| Comunicação | `53` | [Assinatura TV e Streaming](#categoria-53-assinatura-tv-e-streaming) |
| Tarifas e impostos | `54` | [IPTU](#categoria-54-iptu) |
| Tarifas e impostos | `55` | [IPVA e Gastos Detran](#categoria-55-ipva-e-gastos-detran) |
| Tarifas e impostos | `56` | [Imposto de Renda](#categoria-56-imposto-de-renda) |
| Tarifas e impostos | `57` | [ISS(Imposto sobre Serviços)](#categoria-57-iss-imposto-sobre-servicos) |
| Tarifas e impostos | `58` | [GPS(Guia de Previdência Social)](#categoria-58-gps-guia-de-previdencia-social) |
| Tarifas e impostos | `59` | [Serviços Financeiros](#categoria-59-servicos-financeiros) |
| Tarifas e impostos | `3787` | [IOF](#categoria-3787-iof) |
| Tarifas e impostos | `3788` | [Encargos e Tarifas](#categoria-3788-encargos-e-tarifas) |
| Fatura | `111` | [Cartão de Crédito](#categoria-111-cartao-de-credito) |
| Outros | `279` | [Gastos Diversos](#categoria-279-gastos-diversos) |
| Outros | `39434` | [Cheque](#categoria-39434-cheque) |
| Outros | `39435` | [Saque](#categoria-39435-saque) |
| Outros | `39436` | [Transferência](#categoria-39436-transferencia) |
| Outros | `39437` | [Boletos Diversos](#categoria-39437-boletos-diversos) |
| Agro | `300` | [Receitas Agro](#categoria-300-receitas-agro) |
| Agro | `310` | [Criações](#categoria-310-criacoes) |
| Agro | `330` | [Cultivos](#categoria-330-cultivos) |
| Agro | `350` | [Insumos](#categoria-350-insumos) |
| Agro | `370` | [Apoio Produtivo](#categoria-370-apoio-produtivo) |
| Investimentos | `448977` | [Aplicação](#categoria-448977-aplicacao) |
| Investimentos | `448978` | [Resgate de Investimentos](#categoria-448978-resgate-de-investimentos) |

# Categorias por grupo

<a id="grupo-0-sem-categoria"></a>

## Grupo `0` — Sem categoria

**Quantidade de categorias:** 2

<a id="categoria-0-sem-categoria"></a>

### Categoria `0` — Sem categoria

| Campo | Valor |
|---|---|
| Código do grupo | `0` |
| Grupo | Sem categoria |
| Código da categoria | `0` |
| Categoria | Sem categoria |

#### Definição

Código utilizado para categporias não identificadas

[↑ Voltar ao índice rápido](#indice-rapido-de-categorias)

---

<a id="categoria-83-sem-categoria"></a>

### Categoria `83` — Sem categoria

| Campo | Valor |
|---|---|
| Código do grupo | `0` |
| Grupo | Sem categoria |
| Código da categoria | `83` |
| Categoria | Sem categoria |

#### Definição

Código de sistema utilizado para que o lançamento seja recategorizado em rotina noturna após erro no processamento da categorização

[↑ Voltar ao índice rápido](#indice-rapido-de-categorias)

---

<a id="grupo-1-receitas"></a>

## Grupo `1` — Receitas

**Quantidade de categorias:** 5

<a id="categoria-1-salario"></a>

### Categoria `1` — Salário

| Campo | Valor |
|---|---|
| Código do grupo | `1` |
| Grupo | Receitas |
| Código da categoria | `1` |
| Categoria | Salário |

#### Definição

Use esta categoria para registrar recebimentos relacionados à remuneração por trabalho, provenientes de vínculo empregatício, prestação de serviços ou créditos laborais formais.

#### Inclui

- Salário mensal oriundo de contrato de trabalho
- Proventos recebidos via TED, DOC, PIX ou crédito automático
- **Lançamentos com descrições como:**
- “Recebimento de Proventos”
- “Honorários” (quando referentes a atividade laboral formal)
- “Salário”
- “Proventos TED”
- “Crédito de Remuneração”
- “Pagamento Empresa X – Proventos”
- Aposentadoria
- BPC
- Créditos recorrentes vinculados a folha de pagamento
- Pagamentos feitos por empresas a empregados, colaboradores ou profissionais cujo vínculo esteja claramente indicado na descrição

#### Não inclui

- Receitas provenientes de atividades agro (categorias 300, 310, 330)
- Transferências pessoais ou PIX sem referência laboral (categoria 39436 – Transferência)
- Pagamentos de prestação de serviços eventuais sem vínculo (Cat 60))
- Créditos referentes a reembolsos, estornos ou devoluções
- Pensões, aposentadorias ou benefícios previdenciários.

#### Observações importantes

- Classifique nesta categoria sempre que o crédito estiver claramente associado a remuneração de trabalho, seja por vínculo formal ou remuneração profissional, conforme indicado na descrição.

[↑ Voltar ao índice rápido](#indice-rapido-de-categorias)

---

<a id="categoria-2-vale-alimentacao"></a>

### Categoria `2` — Vale Alimentação

| Campo | Valor |
|---|---|
| Código do grupo | `1` |
| Grupo | Receitas |
| Código da categoria | `2` |
| Categoria | Vale Alimentação |

#### Definição

Use esta categoria para registrar recebimentos de vale-alimentação, benefício corporativo destinado à compra de alimentos em supermercados, padarias e estabelecimentos autorizados.

#### Inclui

- Créditos mensais de Vale Alimentação fornecidos pela empresa empregadora
- **Recebimentos identificados como:**
- “Vale Alimentação”
- “Pix Recebido – Vale Alimentação”
- “Transferência – Vale Alimentação”
- “Crédito Benefício Alimentação”
- Depósitos recorrentes realizados por empresas conveniadas, operadoras de benefícios ou RH corporativo
- Complementações, ajustes ou regularizações do saldo de VA

#### Não inclui

- Vale Refeição → Categoria específica, se existir
- Salário, pró-labore ou honorários → Categoria 1 (Salário)
- Doações ou PIX entre pessoas → Categoria 39436 (Transferência)
- Reembolso de compras, estornos ou ajustes financeiros

#### Observações importantes

- Esta categoria é usada exclusivamente para recebimentos, não para despesas realizadas com o saldo do vale.
- As compras feitas usando o cartão VA devem ser classificadas conforme o tipo de gasto (ex.: supermercado, padaria etc.).

[↑ Voltar ao índice rápido](#indice-rapido-de-categorias)

---

<a id="categoria-3-restituicao-de-ir"></a>

### Categoria `3` — Restituição de IR

| Campo | Valor |
|---|---|
| Código do grupo | `1` |
| Grupo | Receitas |
| Código da categoria | `3` |
| Categoria | Restituição de IR |

#### Definição

Créditos referentes à restituição de Imposto de Renda.(Ela é a devolução,

pela Receita Federal, de valores pagos a mais pelo contribuinte durante o ano-base, retidos na fonte (salário) ou via Carnê-Leão). Possui palavras como: ""restituição de Imposto de Renda"" | ""Estorno"" | ""Restituição de IRPF"" |

[↑ Voltar ao índice rápido](#indice-rapido-de-categorias)

---

<a id="categoria-4-bonificacao"></a>

### Categoria `4` — Bonificação

| Campo | Valor |
|---|---|
| Código do grupo | `1` |
| Grupo | Receitas |
| Código da categoria | `4` |
| Categoria | Bonificação |

#### Definição

Use esta categoria para registrar recebimentos de bônus, prêmios, participações e remunerações meritórias, provenientes de empresas, empregadores ou programas de incentivo.

#### Inclui

- PLR – Participação nos Lucros e Resultados
- **Prêmios corporativos, como:**
- Bonificações por desempenho
- Premiação PDG
- Incentivos anuais ou mensais
- Bônus salariais ou complementares vinculados à performance
- Dividendos, quando recebidos como parte de remuneração funcional
- Juros sobre Capital Próprio (JCP), quando pagos como forma de ganho remuneratório
- Créditos provenientes de reconhecimento profissional, campanhas internas, gratificações e programas de mérito
- **Lançamentos com descrições típicas como:**
- “Bonificação”
- “Prêmio”
- “PLR”
- “PDG”
- “Bônus”
- “Dividendos”
- “JCP”
- “Participação nos lucros”

#### Observações importantes

- Essa categoria frequentemente recebe lançamentos recategorizados pelo próprio cliente, especialmente quando a descrição é genérica, o que pode dificultar a classificação automática.
- Por isso, quando houver dúvida e o crédito indicar pagamento meritório ou premiação, deve-se priorizar o uso desta categoria.

#### Não inclui

- Salários, honorários e proventos → Categoria 1 – Salário
- Doações recebidas → categoria própria, se existir
- Recebimentos de auxílio, benefícios trabalhistas usuais (VA/VR)
- Receitas financeiras (ex.: rendimentos de investimentos) → categoria adequada (ex.: resgates, aplicações)
- Receitas agropecuárias → Categorias 300, 310, 330
- Transferências pessoais sem vínculo meritório → Categoria 5 ou Categoria 39436, conforme o caso

[↑ Voltar ao índice rápido](#indice-rapido-de-categorias)

---

<a id="categoria-5-outros-rendimentos"></a>

### Categoria `5` — Outros Rendimentos

| Campo | Valor |
|---|---|
| Código do grupo | `1` |
| Grupo | Receitas |
| Código da categoria | `5` |
| Categoria | Outros Rendimentos |

#### Definição

Use esta categoria para registrar créditos recebidos que não se enquadram em nenhuma das demais categorias de receita, incluindo entradas genéricas, transferências recebidas e valores cuja origem não é possível identificar com precisão.

#### Inclui

- **PIX recebido, quando:**
- Não houver identificação clara da origem
- Não estiver associado a salário, benefício, pensão, vendas, atividades agro ou qualquer outra categoria específica
- Transferências recebidas de pessoas físicas ou jurídicas, sem finalidade reconhecida
- **Créditos sem descrição detalhada, como:**
- “Crédito recebido”
- “Recebimento”
- “Pix recebido”
- “Transferência recebida”
- “Crédito em conta”
- Entradas eventuais não classificáveis em categorias como salário, agro, investimentos, restituições ou benefícios
- Recebimentos esporádicos, como ajuda financeira informal, reembolsos pessoais sem vinculação clara ou devoluções não especificadas

#### Não inclui

- Salários, honorários e proventos → Categoria 1
- Benefícios corporativos (VA/VR) → categorias próprias
- Receitas agropecuárias → Categorias 300, 310, 330
- Resgates de investimentos → Categoria 448978
- Doações recebidas → (categoria específica caso exista)
- Transferências entre contas do mesmo titular → Categoria 39436 – Transferência
- Reembolsos claramente identificados relacionados a outras categorias de despesa

#### Observações importantes

- Esta categoria funciona como categoria residual de RECEITAS, utilizada quando o crédito não possui indicação clara de origem.
- Sempre que houver informação suficiente para identificar o tipo de rendimento, deve-se priorizar a categoria correspondente.

[↑ Voltar ao índice rápido](#indice-rapido-de-categorias)

---

<a id="grupo-2-casa"></a>

## Grupo `2` — Casa

**Quantidade de categorias:** 9

<a id="categoria-6-agua"></a>

### Categoria `6` — Água

| Campo | Valor |
|---|---|
| Código do grupo | `2` |
| Grupo | Casa |
| Código da categoria | `6` |
| Categoria | Água |

#### Definição

Use esta categoria para registrar pagamentos de contas residenciais de abastecimento de água e serviços de saneamento básico, realizados por meio de boletos, débito automático, PIX ou outros meios.

#### Inclui

- Pagamentos a companhias de abastecimento de água e empresas de saneamento
- Lançamentos relativos ao consumo de água em residências, apartamentos ou condomínios
- Descrições que indiquem claramente contas de água ou serviços de saneamento
- **Compras de produtos em empresas que comercializam:**
- Galões de água
- Água filtrada ou mineral em grandes volumes
- Gelo
- (somente quando o termo “água” aparece vinculado à aquisição desses produtos)

#### Não inclui

- **Lançamentos com o termo “água” quando o contexto for:**
- Clubes
- Estâncias hidrominerais
- Parques aquáticos
- Resorts ou atividades de lazer relacionadas à água
  - → Nesse caso, utilizar a categoria correspondente a lazer, entretenimento ou serviços.
- Serviços hidráulicos, reparos ou manutenção
  - → Categoria 12 – Serviços e Manutenção
- Compras de água mineral em supermercados
  - → Categoria de alimentação/supermercado, conforme o caso

[↑ Voltar ao índice rápido](#indice-rapido-de-categorias)

---

<a id="categoria-7-eletricidade-e-gas"></a>

### Categoria `7` — Eletricidade e Gás

| Campo | Valor |
|---|---|
| Código do grupo | `2` |
| Grupo | Casa |
| Código da categoria | `7` |
| Categoria | Eletricidade e Gás |

#### Definição

Use esta categoria para registrar pagamentos de despesas residenciais ou prediais relacionadas ao consumo de energia elétrica e gás.

#### Inclui

- Pagamentos de contas de energia elétrica emitidas por concessionárias e distribuidoras de eletricidade
- Pagamentos de gás encanado, gás canalizado ou gás fornecido por distribuidoras regionais
- Lançamentos cuja descrição contenha o nome de empresas distribuidoras de energia elétrica ou gás
- Compras relacionadas a fornecimento de gás em botijão (GLP), quando a cobrança vier de empresas distribuidoras reconhecidas
- Boletos, transferências, PIX ou débitos automáticos referentes ao consumo de energia ou gás
- **Lançamentos que usam os termos:**
- “Energia”
- “Eletricidade”
- “Luz”
- “Gás”
- Nomes de concessionárias (ex.: Enel, Neoenergia, Copel, CEB, Comgás, Ultragaz etc.)

#### Não inclui

- Compras de equipamentos elétricos, lâmpadas, chuveiros ou itens de instalação elétrica
- Serviços de eletricista ou manutenção predial → Categoria 12 – Serviços e Manutenção
- Botijões de gás comprados em supermercados ou estabelecimentos que vendem itens domésticos (quando não vinculado à distribuidora oficial)
- Pagamentos de condomínio → Categoria 10 – Aluguel e Condomínio
- Serviços de telecomunicação ou internet cobrados junto ao boleto (quando separado) → Categoria 51 – Telefonia e Internet

#### Observações importantes

- Classifique nesta categoria qualquer lançamento que envolva o fornecimento de energia elétrica ou gás para uso residencial ou predial, independentemente da forma de pagamento.

[↑ Voltar ao índice rápido](#indice-rapido-de-categorias)

---

<a id="categoria-9-compra-de-imovel"></a>

### Categoria `9` — Compra de Imóvel

| Campo | Valor |
|---|---|
| Código do grupo | `2` |
| Grupo | Casa |
| Código da categoria | `9` |
| Categoria | Compra de Imóvel |

#### Definição

Use esta categoria para registrar pagamentos de prestações de financiamentos imobiliários, independentemente do banco, instituição financeira ou modalidade de crédito utilizada.

Normalmente esses lançamentos são pagos por boleto, mas também podem ocorrer via PIX, débito ou transferência, desde que se refiram exclusivamente ao financiamento ou aquisição de imóvel.

Devem ser incluídos aqui também pagamentos feitos a prefeituras municipais relacionados à compra, regularização ou financiamento de imóveis, quando caracterizados como parte do processo de aquisição.

#### Não inclui

- Pagamentos referentes a aluguéis de imóveis
- Incluíndo construtoras, Incorporadoras

[↑ Voltar ao índice rápido](#indice-rapido-de-categorias)

---

<a id="categoria-10-aluguel-e-condominio"></a>

### Categoria `10` — Aluguel e Condomínio

| Campo | Valor |
|---|---|
| Código do grupo | `2` |
| Grupo | Casa |
| Código da categoria | `10` |
| Categoria | Aluguel e Condomínio |

#### Definição

Use esta categoria para registrar pagamentos de aluguel e de taxas de condomínio, tanto de imóveis residenciais quanto comerciais.

Essa unificação é importante porque muitas imobiliárias cobram aluguel e condomínio no mesmo boleto, ou fazem a gestão integrada desses pagamentos.

#### Inclui

- Pagamentos de aluguel de imóveis residenciais ou comerciais
- Taxas de condomínio mensais
- Boletos unificados emitidos por imobiliárias que incluam aluguel, condomínio ou ambos
- Pagamentos feitos a administradoras de condomínio ou imobiliárias responsáveis pela cobrança
- Taxas extraordinárias de condomínio, quando cobradas pela administradora

#### Não inclui

- Aluguel de veículos ou equipamentos (que possuem categoria específica)
- Pagamentos de financiamento imobiliário
- Gastos com manutenção, reformas, serviços ou reparos, que pertencem à categoria Serviços e Manutenção
- IPTU e outros tributos

[↑ Voltar ao índice rápido](#indice-rapido-de-categorias)

---

<a id="categoria-11-moveis-e-utensilios"></a>

### Categoria `11` — Móveis e Utensílios

| Campo | Valor |
|---|---|
| Código do grupo | `2` |
| Grupo | Casa |
| Código da categoria | `11` |
| Categoria | Móveis e Utensílios |

#### Definição

Use esta categoria para registrar gastos realizados em lojas físicas ou virtuais que comercializam móveis, eletrodomésticos, eletroportáteis e utensílios domésticos.

Inclua nesta categoria compras como:

Móveis (sofás, mesas, cadeiras, camas, armários etc.)

Eletrodomésticos (geladeira, fogão, máquina de lavar, micro-ondas…)

Eletroportáteis (liquidificador, ventilador, aspirador, batedeira etc.)

Utensílios de uso doméstico (panelas, pratos, copos, talheres, potes, itens de organização etc.)

#### Não inclui

- Gastos com reformas, instalações, decoração ou serviços (ex.: marcenaria, montagem, pintura)
- Compras de eletrônicos de uso pessoal que não sejam itens domésticos (ex.: celulares, notebooks, tablets)
- Aluguel de móveis ou equipamentos

[↑ Voltar ao índice rápido](#indice-rapido-de-categorias)

---

<a id="categoria-12-servicos-e-manutencao"></a>

### Categoria `12` — Serviços e Manutenção

| Campo | Valor |
|---|---|
| Código do grupo | `2` |
| Grupo | Casa |
| Código da categoria | `12` |
| Categoria | Serviços e Manutenção |

#### Definição

Use esta categoria para registrar quaisquer gastos relacionados a serviços prestados para a casa, incluindo manutenção, reparos, limpeza e cuidados gerais com o imóvel.

#### Inclui

- Serviços de empresas ou profissionais autônomos.
- Serviços de jardinagem, poda, cuidados com áreas externas ou pequenos serviços de manutenção.
- Gastos em lojas de materiais de construção, incluindo itens para pequenos reparos e manutenção.
- Serviços técnicos como eletricista, encanador, chaveiro, dedetização, instalação, conserto ou manutenção de equipamentos domésticos.

#### Não inclui

- Compras de móveis, eletrodomésticos, utensílios ou eletrônicos, que possuem categoria própria.
- Pagamentos de condomínio, aluguel ou financiamento imobiliário, já classificados em outras categorias.
- Grandes obras ou reformas estruturais, caso exista uma categoria específica para isso.

[↑ Voltar ao índice rápido](#indice-rapido-de-categorias)

---

<a id="categoria-13-empregados"></a>

### Categoria `13` — Empregados

| Campo | Valor |
|---|---|
| Código do grupo | `2` |
| Grupo | Casa |
| Código da categoria | `13` |
| Categoria | Empregados |

#### Definição

Conjunto de profissionais contratados por famílias ou unidades domésticas para executar atividades de suporte direto ao ambiente residencial, garantindo organização, manutenção, bem-estar e segurança dos residentes. Inclui trabalhadores responsáveis por tarefas como limpeza, preparo de refeições, cuidados com roupas e pertences, apoio a crianças e idosos, manutenção de áreas internas e externas, condução veicular para uso da família, e administração cotidiana da casa.

Esses empregados desempenham funções essenciais para o funcionamento adequado do lar e atuam de forma contínua ou periódica, sempre sem caráter empresarial, pois o empregador é a própria família ou indivíduo residente, conforme previsto no CNAE 9700-5/00.

Com base nos descritores oficiais do CNAE, integram esta categoria profissionais como:

Arrumadeira / camareira doméstica

Cozinheiro(a) e copeiro(a)

Babá / acompanhante

Jardineiro(a)

Caseiro(a)

Lavadeira / passadeira

Motorista residencial

Governanta

Essa categoria não inclui:

Prestadores terceirizados ou empresas que fornecem mão de obra temporária (CNAE 78.20-5)

Profissionais autônomos ou empresas de jardinagem, culinária, limpeza ou conservação que atuam como prestadores independentes

[↑ Voltar ao índice rápido](#indice-rapido-de-categorias)

---

<a id="categoria-14-animais-e-pets"></a>

### Categoria `14` — Animais e Pets

| Campo | Valor |
|---|---|
| Código do grupo | `2` |
| Grupo | Casa |
| Código da categoria | `14` |
| Categoria | Animais e Pets |

#### Definição

Use esta categoria para registrar todos os gastos relacionados ao cuidado, saúde, alimentação e bem‑estar de animais domésticos.

#### Inclui

- Compras em petshops (ração, petiscos, brinquedos, acessórios, produtos de higiene etc.)
- Serviços de banho e tosa
- Consultas veterinárias, emergências, exames, internações e procedimentos clínicos
- Medicamentos veterinários
- Compras em lojas agropecuárias quando relacionadas a itens ou serviços para pets
- Serviços como adestramento, hospedagem, creche para cães e transporte especializado

#### Não inclui

- Gastos com animais de produção ou atividades agropecuárias de grande porte, caso exista categoria própria
- Compras em lojas agropecuárias que não estejam relacionadas a animais domésticos (ex.: ferramentas, insumos agrícolas etc.)

[↑ Voltar ao índice rápido](#indice-rapido-de-categorias)

---

<a id="categoria-3790-seguro-residencial"></a>

### Categoria `3790` — Seguro Residencial

| Campo | Valor |
|---|---|
| Código do grupo | `2` |
| Grupo | Casa |
| Código da categoria | `3790` |
| Categoria | Seguro Residencial |

#### Definição

Use esta categoria para registrar pagamentos relacionados ao seguro residencial, independentemente da seguradora, tipo de cobertura ou forma de contratação.

#### Inclui

- Prêmios de seguro residencial (mensais, anuais ou parcelados)
- Pagamentos referentes a renovações de seguro da residência
- Seguros vinculados a imóveis próprios, financiados ou alugados
- **Coberturas relacionadas a:**
- Incêndio
- Roubo e furto
- Danos elétricos
- Responsabilidade civil
- Desastres naturais (tempestade, enchente, vendaval etc.)
- Assistência residencial
- **Lançamentos identificados com nomes de seguradoras e produtos residenciais, como:**
- Porto Seguro Residência
- Bradesco Residencial
- Tokio Marine Residencial
- Mapfre Residência
- Allianz Residência
- Outras seguradoras com produtos específicos para imóveis

#### Não inclui

- Seguros de veículos → Categoria 39 – Seguros de Veículos
- Seguros de vida, acidentes pessoais ou previdência → Categoria 46 – Seguros e Previdência
- Planos de saúde → Categoria 27 – Plano de Saúde
- Serviços de manutenção, reparos ou assistência não vinculados ao seguro (devem ir para categorias específicas)
- Despesas com financiamento ou compra de imóvel → categorias 9 ou 10, conforme o caso

[↑ Voltar ao índice rápido](#indice-rapido-de-categorias)

---

<a id="grupo-3-educacao"></a>

## Grupo `3` — Educação

**Quantidade de categorias:** 5

<a id="categoria-15-educacao-superior"></a>

### Categoria `15` — Educação Superior

| Campo | Valor |
|---|---|
| Código do grupo | `3` |
| Grupo | Educação |
| Código da categoria | `15` |
| Categoria | Educação Superior |

#### Definição

Use esta categoria para registrar gastos relacionados ao pagamento de instituições de ensino superior, incluindo universidades e faculdades, em qualquer modalidade de formação.

#### Inclui

- Pagamento de matrícula
- Mensalidades de cursos de graduação
- Pós‑graduação, incluindo MBA, especialização, mestrado e doutorado
- Pagamentos vinculados a financiamento estudantil (como FIES ou financiadoras privadas)
- Parcelas relacionadas a programas de educação continuada oferecidos por instituições de ensino superior

#### Não inclui

- Cursos livres, técnicos, profissionalizantes ou de curta duração (a menos que ofertados como programa formal de ensino superior)
- Gastos com material didático, livros ou tecnologia (a menos que você queira criar uma categoria específica para isso)
- Pagamentos de escolas, creches ou ensino básico — que pertencem a outra categoria, caso exista

[↑ Voltar ao índice rápido](#indice-rapido-de-categorias)

---

<a id="categoria-16-colegio"></a>

### Categoria `16` — Colégio

| Campo | Valor |
|---|---|
| Código do grupo | `3` |
| Grupo | Educação |
| Código da categoria | `16` |
| Categoria | Colégio |

#### Definição

Use esta categoria para registrar gastos relacionados ao pagamento de instituições de ensino infantil, fundamental e médio, incluindo:

Berçário

Creche

Escola

Colégio

#### Inclui

- Pagamento de matrícula
- Mensalidades escolares
- Parcelas de anuidade escolar
- Pagamentos recorrentes feitos diretamente a instituições de ensino desses níveis

#### Não inclui

- Gastos com ensino superior (graduação, pós‑graduação, MBA etc.)
- Compra de material escolar, uniformes ou livros, caso exista uma categoria específica
- Cursos livres, reforço escolar avulso ou atividades extracurriculares (a menos que a instituição cobre dentro da própria mensalidade)

[↑ Voltar ao índice rápido](#indice-rapido-de-categorias)

---

<a id="categoria-17-idiomas"></a>

### Categoria `17` — Idiomas

| Campo | Valor |
|---|---|
| Código do grupo | `3` |
| Grupo | Educação |
| Código da categoria | `17` |
| Categoria | Idiomas |

#### Definição

Use esta categoria para registrar gastos relacionados ao pagamento de cursos de ensino de idiomas, em qualquer formato ou modalidade.

#### Inclui

- Cursos presenciais de idioma
- Cursos virtuais/online de idioma (plataformas, escolas digitais, aulas ao vivo ou gravadas)
- Pagamento de mensalidades, matrículas, módulos ou planos de cursos de línguas
- Aulas particulares de idiomas realizadas por professores ou escolas especializadas
- Programas de imersão linguística quando cobrados como curso

#### Não inclui

- Cursos técnicos, profissionalizantes ou livres que não tenham foco exclusivo em idioma
- Gastos com material didático, livros ou certificações (a menos que haja categoria própria)
- Cursos de idiomas vinculados a ensino superior ou escolaridade formal (que já possuem categorias específicas)

[↑ Voltar ao índice rápido](#indice-rapido-de-categorias)

---

<a id="categoria-18-publicacoes-e-papelaria"></a>

### Categoria `18` — Publicações e Papelaria

| Campo | Valor |
|---|---|
| Código do grupo | `3` |
| Grupo | Educação |
| Código da categoria | `18` |
| Categoria | Publicações e Papelaria |

#### Definição

Use esta categoria para registrar compras de materiais escolares, itens de papelaria e produtos de livraria adquiridos em livrarias, papelarias e editoras, tanto em lojas físicas quanto virtuais.

#### Inclui

- Materiais escolares (cadernos, agendas, lápis, canetas, estojos, pastas etc.)
- Itens de papelaria e escritório (blocos, folhas, organizadores, marcadores etc.)
- Livros físicos adquiridos em livrarias ou editoras
- Gráficas, xerox, impressões

[↑ Voltar ao índice rápido](#indice-rapido-de-categorias)

---

<a id="categoria-20-outros-gastos"></a>

### Categoria `20` — Outros Gastos

| Campo | Valor |
|---|---|
| Código do grupo | `3` |
| Grupo | Educação |
| Código da categoria | `20` |
| Categoria | Outros Gastos |

#### Definição

Use esta categoria para registrar gastos com cursos profissionalizantes e cursos livres realizados em escolas, instituições de formação ou com profissionais especializados.

#### Inclui

- Cursos técnicos e profissionalizantes (ex.: esteticista, eletricista, marceneiro, manicure, barbeiro)
- Cursos de informática e tecnologia (ex.: computação básica, pacote Office, programação, design gráfico)
- Cursos de artes e habilidades manuais (ex.: percussão, música, pintura, fotografia, artesanato)
- Cursos livres de aperfeiçoamento, capacitação ou desenvolvimento de habilidades gerais
- Pagamentos de matrícula, mensalidade, módulos, workshops e aulas pontuais relacionados a cursos profissionalizantes
- Cursos online, ou via ebooks.

#### Não inclui

- Cursos de idiomas (Categoria 17)
- Cursos vinculados ao ensino superior (Categoria 15)
- Pagamentos de colégio, escola ou creche (Categoria 16)

[↑ Voltar ao índice rápido](#indice-rapido-de-categorias)

---

<a id="grupo-4-lazer"></a>

## Grupo `4` — Lazer

**Quantidade de categorias:** 5

<a id="categoria-21-viagens-e-lazer"></a>

### Categoria `21` — Viagens e Lazer

| Campo | Valor |
|---|---|
| Código do grupo | `4` |
| Grupo | Lazer |
| Código da categoria | `21` |
| Categoria | Viagens e Lazer |

#### Definição

Use esta categoria para registrar gastos relacionados a viagens, sejam elas turísticas, a trabalho ou educacionais.

#### Inclui

- Hospedagem em hotéis, pousadas, hostels ou similares
- Pacotes de viagem adquiridos em agências físicas ou online
- Passagens de avião, transporte turístico e similares
- Translado e deslocamentos vinculados diretamente à viagem (ex.: transfers, shuttle, transporte entre aeroportos)
- Passeios turísticos, excursões, ingressos de atrações e experiências compradas durante a viagem
- Taxas relacionadas à viagem (ex.: taxas de embarque incluídas no bilhete)

#### Não inclui

- Gastos do dia a dia durante a viagem (alimentação, compras, medicamentos), que devem ser classificados em suas categorias específicas
- Combustível e pedágio de viagens feitas com veículo próprio (a menos que sejam parte de pacote turístico)

[↑ Voltar ao índice rápido](#indice-rapido-de-categorias)

---

<a id="categoria-22-esportes-e-academia"></a>

### Categoria `22` — Esportes e Academia

| Campo | Valor |
|---|---|
| Código do grupo | `4` |
| Grupo | Lazer |
| Código da categoria | `22` |
| Categoria | Esportes e Academia |

#### Definição

Use esta categoria para registrar gastos relacionados à prática de atividades físicas, esportes e bem‑estar corporal, em qualquer modalidade, formato ou ambiente.

#### Inclui

- Mensalidades de academias, centros esportivos, estúdios e boxes (ex.: musculação, crossfit, pilates, yoga)
- Aulas e treinamentos presenciais ou online (ex.: dança, natação, artes marciais, musculação guiada)
- Serviços de personal trainer
- Inscrições em eventos esportivos, como corridas, maratonas, competições e torneios
- Assinaturas de plataformas digitais de exercícios, treinos, programas de condicionamento físico e apps fitness
- Compras de roupas esportivas, acessórios ou equipamentos.

#### Não inclui

- Gastos com viagens, hospedagem ou alimentação durante eventos esportivos (categorias próprias)
- Serviços médicos, fisioterapia ou exames esportivos

[↑ Voltar ao índice rápido](#indice-rapido-de-categorias)

---

<a id="categoria-25-cultura-e-entretenimento"></a>

### Categoria `25` — Cultura e Entretenimento

| Campo | Valor |
|---|---|
| Código do grupo | `4` |
| Grupo | Lazer |
| Código da categoria | `25` |
| Categoria | Cultura e Entretenimento |

#### Definição

Use esta categoria para registrar gastos relacionados a atividades de cultura, lazer, diversão e entretenimento, em diferentes formatos e ambientes.

#### Inclui

- Clubes de diversas modalidades, como sociais, esportivos, náuticos, recreativos e clubes de tiro
- Cinema, ingressos e serviços associados
- Teatro, musicais, óperas e espetáculos cênicos em geral
- Espetáculos ao vivo, como shows, stand‑up, performances e apresentações culturais
- Museus, exposições, centros culturais, galerias de arte
- Circos, parques temáticos culturais ou similares
- Ingressos de lazer e atrações culturais adquiridos presencialmente ou online
- Assinaturas ou ingressos relacionados a atividades de entretenimento físico ou digital (exceto quando houver categoria específica)

#### Não inclui

- Atividades esportivas, academias ou eventos esportivos (Categoria 22 – Esportes e Academia)
- Viagens, hospedagem ou deslocamento para eventos culturais (Categoria 21 – Viagens)
- Compras de livros, revistas e materiais escolares (Categorias 18 e 26)
- Cursos ou formações culturais (Categoria 20 – Cursos, ou outras específicas)

[↑ Voltar ao índice rápido](#indice-rapido-de-categorias)

---

<a id="categoria-26-publicacoes-digitais"></a>

### Categoria `26` — Publicações Digitais

| Campo | Valor |
|---|---|
| Código do grupo | `4` |
| Grupo | Lazer |
| Código da categoria | `26` |
| Categoria | Publicações Digitais |

#### Definição

Use esta categoria para registrar compras e assinaturas de conteúdo digital, como jornais, livros e revistas em formato eletrônico.

#### Inclui

- Assinaturas de jornais digitais
- Assinaturas de revistas digitais
- Compra de e‑books
- Assinaturas de plataformas de leitura digital (ex.: apps de livros, revistas ou jornais)
- Pagamentos recorrentes ou avulsos de conteúdo exclusivamente digital

#### Atenção

- Compras em livrarias físicas, papelarias ou editoras que envolvam produtos físicos (livros impressos, material escolar, itens de papelaria) devem ser classificadas na Categoria 18 – Livraria e Papelaria.
- Somente conteúdos digitais devem ser lançados aqui.

#### Não inclui

- Livros impressos, revistas físicas ou materiais escolares
- Assinaturas de cursos, plataformas de estudo ou conteúdos educacionais

[↑ Voltar ao índice rápido](#indice-rapido-de-categorias)

---

<a id="categoria-61-jogos-e-loterias"></a>

### Categoria `61` — Jogos e Loterias

| Campo | Valor |
|---|---|
| Código do grupo | `4` |
| Grupo | Lazer |
| Código da categoria | `61` |
| Categoria | Jogos e Loterias |

#### Definição

Use esta categoria para registrar gastos relacionados a jogos de apostas, loterias e serviços prestados por casas lotéricas.

#### Inclui

- **Apostas em loterias oficiais, como:**
- Mega-Sena
- Quina
- Lotofácil
- Lotomania
- Dupla Sena
- Timemania
- +Milionária
- Super Sete
- Pagamentos realizados em casas lotéricas, quando identificados como jogos ou apostas
- Apostas esportivas ou jogos regulamentados pagos via lotérica ou plataformas oficiais
- Compras de bilhetes, jogos avulsos e recargas específicas vinculadas a loterias
- **exceto:**
- Jogos de plataformas tradicionais como playstation, xbox, nintendo , etc

[↑ Voltar ao índice rápido](#indice-rapido-de-categorias)

---

<a id="grupo-5-saude"></a>

## Grupo `5` — Saúde

**Quantidade de categorias:** 4

<a id="categoria-27-plano-de-saude"></a>

### Categoria `27` — Plano de Saúde

| Campo | Valor |
|---|---|
| Código do grupo | `5` |
| Grupo | Saúde |
| Código da categoria | `27` |
| Categoria | Plano de Saúde |

#### Definição

Use esta categoria para registrar gastos relacionados ao pagamento de planos de saúde.

#### Inclui

- Mensalidades de planos de saúde individuais, familiares, empresariais ou coletivos
- Pagamentos feitos diretamente às operadoras e seguradoras de saúde
- Boletos, débito automático, transferências ou pagamentos via plataformas digitais referentes ao plano contratado

#### Não inclui

- Consultas médicas, exames, procedimentos avulsos ou internações pagas fora do plano.
- Planos exclusivamente odontológicos.
- Seguros de vida ou seguros pessoais não vinculados a plano de saúde.

[↑ Voltar ao índice rápido](#indice-rapido-de-categorias)

---

<a id="categoria-28-servicos-de-saude"></a>

### Categoria `28` — Serviços de Saúde

| Campo | Valor |
|---|---|
| Código do grupo | `5` |
| Grupo | Saúde |
| Código da categoria | `28` |
| Categoria | Serviços de Saúde |

#### Definição

Use esta categoria para registrar gastos relacionados a serviços médicos, procedimentos de saúde, atendimentos clínicos e exames, realizados em hospitais, clínicas, consultórios ou laboratórios.

#### Inclui

- Consultas médicas em diversas especialidades
- Atendimentos em hospitais, clínicas e centros de saúde
- **Tratamentos médicos e terapêuticos, como:**
- Fisioterapia
- Fonoaudiologia
- Acupuntura
- Psicoterapia, se não houver categoria específica
- Exames de saúde realizados em hospitais, clínicas ou laboratórios (exceto os odontológicos)
- Serviços ambulatoriais e procedimentos não odontológicos
- Vacinas aplicadas em clínicas particulares

#### Observações importantes

- Exames e procedimentos odontológicos não devem ser incluídos aqui.
- Para isso, utilize a Categoria 29 – Dentista (Débito).

#### Não inclui

- Pagamentos de plano de saúde (Categoria 27 – Plano de Saúde)
- Medicamentos comprados em farmácias, caso haja categoria específica

[↑ Voltar ao índice rápido](#indice-rapido-de-categorias)

---

<a id="categoria-29-dentista"></a>

### Categoria `29` — Dentista

| Campo | Valor |
|---|---|
| Código do grupo | `5` |
| Grupo | Saúde |
| Código da categoria | `29` |
| Categoria | Dentista |

#### Definição

Use esta categoria para registrar gastos relacionados a serviços odontológicos, realizados em clínicas, consultórios ou profissionais de odontologia.

#### Inclui

- **Tratamentos odontológicos, como:**
- Limpeza
- Restaurações
- Tratamento de canal
- Extrações
- Aparelhos ortodônticos
- Clareamento dental
- Implantes e próteses
- **Exames odontológicos, incluindo:**
- Raios-x
- Panorâmicas
- Tomografias odontológicas
- Planos Odontológicos
- Procedimentos estéticos odontológicos, quando realizados em clínicas odontológicas
- **Pagamentos feitos diretamente a:**
- Clínicas odontológicas
- Consultórios particulares
- Profissionais autônomos da área de odontologia
- planos

#### Não inclui

- Serviços médicos não odontológicos → Categoria 28 – Serviços de Saúde
- Compra de medicamentos odontológicos → Categoria 30 – Farmácias e Drogarias
- Pagamentos administrativos, taxas ou serviços financeiros

#### Observações importantes

- Classifique aqui qualquer gasto odontológico claramente identificado, independentemente da forma de pagamento (PIX, boleto, cartão, débito etc.).

[↑ Voltar ao índice rápido](#indice-rapido-de-categorias)

---

<a id="categoria-30-farmacias-e-drogarias"></a>

### Categoria `30` — Farmácias e Drogarias

| Campo | Valor |
|---|---|
| Código do grupo | `5` |
| Grupo | Saúde |
| Código da categoria | `30` |
| Categoria | Farmácias e Drogarias |

#### Definição

Use esta categoria para registrar gastos com a compra de medicamentos e outros itens adquiridos especificamente em farmácias e drogarias.

#### Inclui

- Medicamentos com ou sem prescrição
- Produtos de tratamento farmacológico
- Itens de saúde vendidos em farmácias quando relacionados ao uso médico (ex.: pomadas, sprays terapêuticos, soluções antissépticas)

#### Não inclui

- Serviços médicos, consultas, exames ou terapias (Categoria 28 – Serviços de Saúde)
- Planos de saúde (Categoria 27 – Plano de Saúde)
- Produtos cosméticos, de higiene pessoal ou perfumaria.
- Despesas com tratamentos odontológicos (Categoria 29 – Dentista)
- Hospitais

[↑ Voltar ao índice rápido](#indice-rapido-de-categorias)

---

<a id="grupo-6-alimentacao"></a>

## Grupo `6` — Alimentação

**Quantidade de categorias:** 2

<a id="categoria-32-feira-e-supermercado"></a>

### Categoria `32` — Feira e Supermercado

| Campo | Valor |
|---|---|
| Código do grupo | `6` |
| Grupo | Alimentação |
| Código da categoria | `32` |
| Categoria | Feira e Supermercado |

#### Definição

Categoria para classificar compras em mercados, feiras, mercearias, cerealistas, açougues, minimercados, distribuidoras de bebidas, hortifrutis (Ver Nota de Exemplo)

Obs.: Classificar os lançamentos que referenciam compra de alimentos in natura. Lançamentos de compras de alimentos prontos para consumir (bares, restaurantes, padarias) devem ser classificados em 35 - Bares e Restaurantes.

VER Bares/Restaurantes (GFP) (Cod. Cat. 35 - Débito)

Não USE Feira (Cod. Cat. 33 - Débito)

[↑ Voltar ao índice rápido](#indice-rapido-de-categorias)

---

<a id="categoria-35-bar"></a>

### Categoria `35` — Bar

| Campo | Valor |
|---|---|
| Código do grupo | `6` |
| Grupo | Alimentação |
| Código da categoria | `35` |
| Categoria | Bar |

#### Definição

Use esta categoria para registrar gastos com alimentação preparada para consumo imediato, adquirida em:

Bares

Restaurantes

Cafés

Padarias

Lanchonetes

Confeitarias

Docerias

Estabelecimentos similares que vendam alimentos prontos

Incluindo Marmitas

Adega

peixaria

quiosque

conveniência

#### Inclui

- Refeições e lanches consumidos no local ou para viagem
- Compras de alimentos prontos em padarias, cafeterias e confeitarias
- Pagamentos feitos em aplicativos de delivery, como iFood (IFD) e outros, desde que o item comprado seja alimento pronto para consumo
- Taxas, entregas e serviços cobrados por plataformas de delivery vinculados ao pedido de comida preparada

#### Atenção

- Utilize esta categoria somente quando o produto for alimento preparado para consumo imediato.
- Compras de insumos, ingredientes ou produtos alimentares crus, feitos em supermercados, mercearias, hortifrutis, açougues ou similares devem ser classificadas em Feira e Supermercado (Código 32 – Débito).
- Não utilizar a categoria Refeição (Cod. 34 – Débito) — esta categoria não deve mais ser usada.

#### Não inclui

- Compras de mercado, açougue, hortifruti ou lojas de insumos alimentares
- Assinaturas ou clubes de assinatura de alimentos não preparados
- Artigos não alimentares vendidos nos estabelecimentos (ex.: presentes, itens de confeitaria para preparo)

[↑ Voltar ao índice rápido](#indice-rapido-de-categorias)

---

<a id="grupo-7-transporte"></a>

## Grupo `7` — Transporte

**Quantidade de categorias:** 6

<a id="categoria-36-compra-de-veiculo"></a>

### Categoria `36` — Compra de Veículo

| Campo | Valor |
|---|---|
| Código do grupo | `7` |
| Grupo | Transporte |
| Código da categoria | `36` |
| Categoria | Compra de Veículo |

#### Definição

Use esta categoria para registrar gastos relacionados à aquisição ou utilização de veículos, incluindo compras financiadas, consórcios e contratos de locação.

#### Inclui

- Parcelas de financiamento para compra de veículos (carros, motos, utilitários etc.)
- Parcelas de consórcios de veículos
- **Pagamentos de aluguel de veículos realizados em locadoras, como:**
- Localiza
- Unidas
- Movida
- Foco
- Outras empresas de locação de veículos
- Boletos, débitos automáticos, PIX ou transferências associados a contratos de aquisição ou locação de veículos

#### Não inclui

- Gastos com manutenção, reparos, peças ou serviços automotivos (devem ir para categoria de Manutenção)
- Combustível, pedágios ou estacionamento
- Seguro de veículo

[↑ Voltar ao índice rápido](#indice-rapido-de-categorias)

---

<a id="categoria-37-combustivel"></a>

### Categoria `37` — Combustível

| Campo | Valor |
|---|---|
| Código do grupo | `7` |
| Grupo | Transporte |
| Código da categoria | `37` |
| Categoria | Combustível |

#### Definição

Use esta categoria para registrar gastos com abastecimento de veículos realizados em postos de combustíveis, independentemente do tipo de combustível adquirido.

#### Inclui

- Abastecimento de gasolina, etanol, diesel, GNV ou outros combustíveis
- Pagamentos feitos diretamente no posto, via cartão, PIX, aplicativo ou programa de fidelidade
- Lançamentos que identifiquem claramente postos de abastecimento ou bombas de combustível

#### Não inclui

- Troca de óleo, serviços automotivos, manutenção, lavagem ou compras em lojas de conveniência do posto (devem ir para outras categorias específicas)
- Pagamentos de pedágio, estacionamento ou serviços relacionados ao trânsito
- Aluguel, financiamento ou consórcio de veículos (Categoria 36 – Compra de Veículo)

[↑ Voltar ao índice rápido](#indice-rapido-de-categorias)

---

<a id="categoria-38-estacionamento-e-pedagio"></a>

### Categoria `38` — Estacionamento e Pedágio

| Campo | Valor |
|---|---|
| Código do grupo | `7` |
| Grupo | Transporte |
| Código da categoria | `38` |
| Categoria | Estacionamento e Pedágio |

#### Definição

Use esta categoria para registrar gastos relacionados a estacionamentos e pedágios, independentemente do local ou do meio de pagamento.

#### Inclui

- Pagamentos de estacionamentos em vias públicas, garagens, estacionamentos privados ou conveniados
- Estacionamento em shoppings centers, já que muitos lançamentos aparecem com o nome do shopping
- **Pagamentos de pedágios, realizados por:**
- Tags automáticas (ex.: Sem Parar, ConectCar, Veloe, Move Mais, etc.)
- Pagamentos manuais em praças de pedágio
- Aplicativos ou plataformas de gestão de pedágio
- Lançamentos que identifiquem serviços de estacionamento ou cobrança automática de passagem em rodovias

#### Não inclui

- Gastos com combustível (Categoria 37 – Combustível)
- Gastos com manutenção, serviços automotivos ou compras em lojas de conveniência de postos
- Multas de trânsito, taxas de licenciamento ou IPVA

[↑ Voltar ao índice rápido](#indice-rapido-de-categorias)

---

<a id="categoria-39-seguro-de-veiculo"></a>

### Categoria `39` — Seguro de Veículo

| Campo | Valor |
|---|---|
| Código do grupo | `7` |
| Grupo | Transporte |
| Código da categoria | `39` |
| Categoria | Seguro de Veículo |

#### Definição

Use esta categoria para registrar gastos relacionados a seguros de veículos, independentemente do tipo de cobertura ou da seguradora contratada.

#### Inclui

- Pagamentos de prêmios de seguro de automóveis, motos, utilitários e outros veículos
- Mensalidades, parcelas ou renovações de seguros veiculares
- Cobranças de seguradoras como: Porto, Bradesco Seguros, Allianz, Zurich, Mapfre, entre outras
- Seguros contratados por meio de locadoras, concessionárias ou bancos, desde que vinculados a um veículo específico

#### Não inclui

- Gastos com manutenção do veículo, peças, oficina ou revisão
- Pagamentos de IPVA, licenciamento ou multas
- Seguros pessoais, de vida ou residenciais (caso existam categorias próprias)
- Aluguel, consórcio ou financiamento de veículos (Categoria 36 – Compra de Veículo)

[↑ Voltar ao índice rápido](#indice-rapido-de-categorias)

---

<a id="categoria-40-servicos-e-manutencao"></a>

### Categoria `40` — Serviços e Manutenção

| Campo | Valor |
|---|---|
| Código do grupo | `7` |
| Grupo | Transporte |
| Código da categoria | `40` |
| Categoria | Serviços e Manutenção |

#### Definição

Use esta categoria para registrar gastos relacionados à manutenção, conservação e serviços automotivos, realizados em oficinas, centros automotivos ou prestadores especializados.

#### Inclui

- Serviços de manutenção mecânica, como troca de óleo, revisão, alinhamento, balanceamento e regulagens
- Troca de peças e autopeças, como filtros, pastilhas de freio, amortecedores, velas, correias, lâmpadas etc.
- Baterias, compra e instalação
- Pneus e serviços associados (troca, montagem, balanceamento)
- Limpeza automotiva, incluindo lavagem simples, detalhada ou especializada
- Estética automotiva, como polimento, vitrificação, higienização interna, cristalização, proteção de pintura
- Serviços realizados em oficinas mecânicas, auto centers, borracharias e estabelecimentos similares

#### Não inclui

- Abastecimento de combustível (Categoria 37 – Combustível)
- Pagamentos de estacionamento ou pedágio (Categoria 38 – Estacionamento e Pedágio)
- Seguros de veículos (Categoria 39 – Seguros de Veículos)
- Financiamento, consórcio ou aluguel de veículos (Categoria 36 – Compra de Veículo)

[↑ Voltar ao índice rápido](#indice-rapido-de-categorias)

---

<a id="categoria-41-transporte-urbano-e-apps"></a>

### Categoria `41` — Transporte Urbano e Apps

| Campo | Valor |
|---|---|
| Código do grupo | `7` |
| Grupo | Transporte |
| Código da categoria | `41` |
| Categoria | Transporte Urbano e Apps |

#### Definição

Use esta categoria para registrar gastos com transportes urbanos, tanto públicos quanto privados, incluindo deslocamentos realizados por aplicativo.

#### Inclui

- **Transporte por aplicativo, como:**
- Uber
- 99
- InDrive
- Aplicativos de táxi ou transporte urbano similares
- Táxi (corridas pagas diretamente ao motorista ou via app)
- **Transporte público urbano, como:**
- Ônibus
- Metrô
- VLT
- BRT
- Trem urbano
- Compra de créditos, recargas ou passes de transporte público
- Pagamentos feitos diretamente no app, via cartão, PIX ou carteira digital

#### Não inclui

- Viagens intermunicipais ou interestaduais (Categoria 21 – Viagens)
- Aluguel de veículos (Categoria 36 – Compra de Veículo)
- Combustível, pedágio ou estacionamento (Categorias 37 e 38)
- Manutenção de veículos ou serviços automotivos (Categoria 40)

[↑ Voltar ao índice rápido](#indice-rapido-de-categorias)

---

<a id="grupo-8-despesas-pessoais"></a>

## Grupo `8` — Despesas Pessoais

**Quantidade de categorias:** 10

<a id="categoria-42-vestuario-e-acessorios"></a>

### Categoria `42` — Vestuário e Acessórios

| Campo | Valor |
|---|---|
| Código do grupo | `8` |
| Grupo | Despesas Pessoais |
| Código da categoria | `42` |
| Categoria | Vestuário e Acessórios |

#### Definição

Use esta categoria para registrar gastos relacionados à compra de roupas, calçados, acessórios e itens de moda, adquiridos em lojas físicas ou virtuais.

#### Inclui

- Roupas em geral: peças femininas, masculinas, infantis, moda íntima, moda praia
- Calçados: tênis, sapatos, sandálias, botas etc.
- Acessórios de moda: bolsas, carteiras, cintos, lenços, chapéus, bonés, luvas, meias, cachecóis
- Bijuterias e joias
- Óculos e demais itens adquiridos em óticas (armações, lentes, óculos de sol)
- Tecidos e aviamentos adquiridos em lojas de moda ou confecção
- Compras feitas em lojas de departamento, boutiques e e‑commerce do setor de moda e acessórios

#### Não inclui

- Serviços de costura, ajustes ou lavanderia.
- Itens esportivos de performance (ex.: equipamentos) — devem ir para categoria específica
- Perfumes, cosméticos e produtos de higiene

[↑ Voltar ao índice rápido](#indice-rapido-de-categorias)

---

<a id="categoria-43-cuidado-pessoal-e-beleza"></a>

### Categoria `43` — Cuidado Pessoal e Beleza

| Campo | Valor |
|---|---|
| Código do grupo | `8` |
| Grupo | Despesas Pessoais |
| Código da categoria | `43` |
| Categoria | Cuidado Pessoal e Beleza |

#### Definição

Use esta categoria para registrar gastos relacionados a produtos e serviços de beleza, cuidados pessoais e estética, realizados em lojas físicas, virtuais ou estabelecimentos especializados.

#### Inclui

- **Produtos de beleza e cuidados pessoais, como:**
- Cosméticos
- Perfumes
- Maquiagem
- Produtos para cabelo, corpo e pele
- **Serviços de beleza, como:**
- Salões de beleza
- Cabeleireiros
- Barbearias
- Manicure e pedicure
- Maquiagem profissional
- Depilação
- **Clínicas de estética, incluindo:**
- Limpeza de pele
- Massagens
- Procedimentos estéticos não médicos
- Tratamentos corporais e faciais

#### Não inclui

- Procedimentos médicos ou clínicos (Categoria 28 – Serviços de Saúde)
- Compra de medicamentos (Categoria 30 – Farmácias e Drogarias)
- Serviços esportivos ou atividades físicas (Categoria 22 – Esportes e Academia)

[↑ Voltar ao índice rápido](#indice-rapido-de-categorias)

---

<a id="categoria-44-compras-diversas"></a>

### Categoria `44` — Compras Diversas

| Campo | Valor |
|---|---|
| Código do grupo | `8` |
| Grupo | Despesas Pessoais |
| Código da categoria | `44` |
| Categoria | Compras Diversas |

#### Definição

Use esta categoria para registrar gastos realizados em lojas de varejo, lojas de departamento e marketplaces, especialmente quando a compra não se enquadra claramente em outra categoria específica.

#### Inclui

- Compras em lojas de departamento (ex.: Americanas, Riachuelo, Magazine Luiza, Casas Bahia) quando o item adquirido não se encaixar em categoria mais específica
- Compras em marketplaces (ex.: Mercado Livre, Amazon, Shopee, AliExpress), quando o tipo de produto não puder ser identificado claramente
- Gastos no cartão de crédito classificados como compra genérica, sem detalhamento suficiente para outra categoria
- Compras em lojas de celulares e acessórios, quando não houver categoria específica definida
- Compras em lojas de informática, quando os itens forem variados ou não se encaixarem em categorias próprias
- Compras em armarinhos, bazares ou lojas de variedades quando os itens não forem identificáveis para outra categoria
- Incluindo Lojas de embalagens.

#### Classificação de aplicativos de pagamento

- Quando a compra no cartão não é especificada, fica como 44
- **PicPay e Mercado Pago:**
- Normalmente devem ser classificados como Categoria 44 – Compras Diversas
- **Exceto quando o lançamento indicar claramente:**
- Tarifa → Categoria 59 (Serviços Financeiros)
- Transferência → Categoria 39436 (Transferência) ou outra categoria correspondente
- Quando o app apenas repassa um pagamento, considerar o tipo de produto/serviço envolvido e não apenas o app

#### Não inclui

- Compras claramente identificáveis como alimentação, farmácia, vestuário, eletrônicos etc. — devem ser classificadas em categorias específicas
- Pagamentos de serviços financeiros (tarifas, juros, transferências)
- Assinaturas digitais (Categoria 26 – Publicações Digitais)
- Contas domésticas ou despesas recorrentes (categorias próprias)

[↑ Voltar ao índice rápido](#indice-rapido-de-categorias)

---

<a id="categoria-45-pensao-alimenticia"></a>

### Categoria `45` — Pensão Alimentícia

| Campo | Valor |
|---|---|
| Código do grupo | `8` |
| Grupo | Despesas Pessoais |
| Código da categoria | `45` |
| Categoria | Pensão Alimentícia |

#### Definição

Use esta categoria para registrar pagamentos de pensão alimentícia, independentemente do meio de pagamento utilizado ou da forma definida entre as partes.

#### Inclui

- Pagamentos de pensão alimentícia determinados judicialmente ou acordados de forma particular
- Pagamentos feitos por PIX, transferência bancária, boleto ou débito automático
- Lançamentos que indiquem claramente termos como pensão, alimentos, auxílio a dependente, financeiro para filho, ou similares
- Transações realizadas com recorrência mensal ou periódica para o mesmo beneficiário, especialmente quando categorizadas pelo próprio cliente

#### Observações importantes

- Grande parte das transações via PIX acaba sendo recategorizada para esta categoria, seja automaticamente pelo cliente ou por padrão de uso.
- A classificação pode ser difícil, pois muitos lançamentos não trazem descrição detalhada — por isso, quando houver dúvida e o pagamento for recorrente a uma pessoa física, costuma‑se direcionar para esta categoria.

#### Não inclui

- Transferências comuns entre pessoas físicas que não tenham relação com pensão
- Pagamentos de pensão ou auxílio eventual sem recorrência, quando claramente não se trata de pensão alimentícia
- Transferências internas entre contas do mesmo titular
- Pagamentos de escola, saúde, lazer ou demais despesas feitas diretamente para terceiros (essas devem ir para as categorias adequadas)

[↑ Voltar ao índice rápido](#indice-rapido-de-categorias)

---

<a id="categoria-46-seguros-e-previdencia"></a>

### Categoria `46` — Seguros e Previdência

| Campo | Valor |
|---|---|
| Código do grupo | `8` |
| Grupo | Despesas Pessoais |
| Código da categoria | `46` |
| Categoria | Seguros e Previdência |

#### Definição

Use esta categoria para registrar gastos relacionados a Quaisquer seguros pessoais e planos de proteção individual, bem como contribuições para previdência privada, quando aplicável.

#### Inclui

- Seguros de vida (individual, familiar ou em grupo)
- Viagem, Veículo, residencial.
- Planos de auxílio‑funeral
- Seguros de acidentes pessoais
- Contribuições, mensalidades ou parcelas de previdência privada (PGBL, VGBL), caso esta seja a orientação da instituição
- Pagamentos feitos a seguradoras, bancos ou empresas especializadas em proteção pessoal e familiar

#### Não inclui

- Planos de saúde (Categoria 27 – Plano de Saúde)
- Serviços médicos, exames ou atendimentos clínicos (Categoria 28 – Serviços de Saúde)
- Produtos financeiros não relacionados a seguro ou previdência

[↑ Voltar ao índice rápido](#indice-rapido-de-categorias)

---

<a id="categoria-47-doacao"></a>

### Categoria `47` — Doação

| Campo | Valor |
|---|---|
| Código do grupo | `8` |
| Grupo | Despesas Pessoais |
| Código da categoria | `47` |
| Categoria | Doação |

#### Definição

Use esta categoria para registrar doações e contribuições voluntárias feitas a entidades, instituições e organizações sem fins lucrativos, bem como a grupos religiosos ou beneficentes.

#### Inclui

- **Doações feitas a:**
- Igrejas e organizações religiosas
- Instituições de caridade
- Associações beneficentes
- ONGs
- Projetos sociais
- Campanhas assistenciais
- Contribuições voluntárias enviadas por PIX, transferência, boleto ou cartão
- **Lançamentos identificados com termos como:**
- Doação
- Contribuição voluntária
- Oferta
- Dízimo
- Apoio institucional
- Campanha solidária

#### Importante

- Contribuições obrigatórias para entidades de classe (como sindicatos, ordens, conselhos ou associações profissionais) NÃO devem ser classificadas aqui.
- Essas contribuições formais e obrigatórias devem ser classificadas na Categoria 3788 – Encargos e Tarifas.

#### Não inclui

- Contribuições obrigatórias a entidades de classe → Categoria 3788
- Taxas, tarifas ou encargos administrativos → Categoria 59 ou 3788, conforme o caso
- Pensões alimentícias → Categoria 45
- Transferências a familiares ou amigos → Categoria 39436 – Transferência
- Pagamentos por serviços ou produtos (não são doações)

#### Observações importantes

- **Quando houver dúvida se o pagamento é voluntário ou obrigatório, a orientação é:**
- Se for voluntário, classificar na Categoria 47 – Doação
- Se for obrigatório, classificar na Categoria 3788 – Encargos e Tarifas

[↑ Voltar ao índice rápido](#indice-rapido-de-categorias)

---

<a id="categoria-48-gasto-com-familiares"></a>

### Categoria `48` — Gasto com Familiares

| Campo | Valor |
|---|---|
| Código do grupo | `8` |
| Grupo | Despesas Pessoais |
| Código da categoria | `48` |
| Categoria | Gasto com Familiares |

#### Definição

Use esta categoria para registrar gastos feitos em benefício de familiares, independentemente do tipo de serviço ou da instituição envolvida.

#### Inclui

- **Pagamentos a funerárias, incluindo:**
- Serviços de velório
- Preparação e cerimônias
- Taxas e serviços correlatos
- Pagamentos a casas de repouso, lares geriátricos, cuidadores ou instituições de acolhimento
- Gastos recorrentes ou eventuais relacionados ao cuidado, assistência ou suporte financeiro a familiares
- Lançamentos identificados como apoio direto a familiares, quando não houver categoria específica para o tipo de despesa
- Transações em que o cliente recategoriza manualmente como gasto familiar, especialmente quando a descrição é genérica (ex.: PIX para familiar sem detalhes)

#### Observações importantes

- **Muitas transações aparecem com descrições pouco claras, dificultando diferenciar:**
- se é um gasto pessoal,
- um pagamento de serviço, ou
- um apoio financeiro direto a um familiar.
- Nesses casos, se houver indício de que o pagamento beneficia um familiar (ou se o cliente recategoriza dessa forma), o lançamento deve ser incluído aqui.
- A categoria também absorve lançamentos que não se encaixam claramente em outra categoria, mas que representam despesas feitas em nome ou benefício de um familiar.

#### Não inclui

- Pensão alimentícia (Categoria 45)
- Gastos pessoais do titular do cartão ou conta que não correspondam ao benefício a um familiar
- Pagamentos de saúde, educação ou serviços quando o beneficiário não for um familiar
- Transferências pessoais sem relação com assistência familiar

[↑ Voltar ao índice rápido](#indice-rapido-de-categorias)

---

<a id="categoria-49-presentes"></a>

### Categoria `49` — Presentes

| Campo | Valor |
|---|---|
| Código do grupo | `8` |
| Grupo | Despesas Pessoais |
| Código da categoria | `49` |
| Categoria | Presentes |

#### Definição

Use esta categoria para registrar gastos relacionados à compra de presentes, adquiridos em lojas físicas, virtuais ou estabelecimentos especializados.

#### Inclui

- Compras em lojas de presentes em geral
- Compras em brinquedarias ou lojas de brinquedos
- Compras em floriculturas, incluindo buquês, arranjos, plantas ornamentais e itens decorativos
- Presentes adquiridos para aniversários, datas comemorativas ou ocasiões especiais
- **Itens comprados em lojas de:**
- Decoração
- Artigos para presentes
- Papelaria de presentes (ex.: kits de presente, cestas, embalagens especiais)
- Compras claramente identificadas como presente, quando constarem na descrição

#### Não inclui

- Compras de roupas ou acessórios → Categoria 42 – Vestuário e Acessórios
- Cosméticos e produtos de beleza → Categoria 43 – Cuidado Pessoal e Beleza
- Eletrônicos, celulares e itens de informática → Categoria 44 – Compras Diversas, ou categoria específica
- Brinquedos adquiridos para uso próprio de uma criança da família (a menos que o cliente classifique como presente)
- Plantas, ferramentas ou itens agrícolas (categorias agro se aplicável)

#### Observações importantes

- **Quando o lançamento ocorrer em lojas multidepartamento (como Americanas, Amazon, Magazine Luiza), só deve ser classificado aqui se:**
- a descrição indicar claramente ser um presente, OU
- o cliente recategorizar manualmente.
- Caso contrário, deve seguir para a categoria correspondente ao tipo do produto.

[↑ Voltar ao índice rápido](#indice-rapido-de-categorias)

---

<a id="categoria-60-servicos-diversos"></a>

### Categoria `60` — Serviços Diversos

| Campo | Valor |
|---|---|
| Código do grupo | `8` |
| Grupo | Despesas Pessoais |
| Código da categoria | `60` |
| Categoria | Serviços Diversos |

#### Definição

Use esta categoria para registrar gastos com serviços personalizados, ocasionais ou criativos, realizados por profissionais independentes ou empresas que prestam serviços específicos que não se enquadram em outras categorias tradicionais.

Essa categoria contempla atividades pontuais, sob demanda e voltadas para necessidades únicas ou projetos especiais, incluindo serviços técnicos, criativos, artesanais ou de suporte.

#### Inclui

- **1. Serviços de digitalização e organização**
- Digitalização de documentos físicos
- Organização de arquivos digitais ou físicos
- Conversão de formatos e tratamento básico de documentos
- **2. Serviços para eventos**
- Planejamento e produção de eventos
- Logística e montagem
- Decoração de eventos ocasionais (festas, conferências, cerimônias)
- **3. Cobertura audiovisual**
- Filmagem e fotografia profissional
- Edição de vídeos e tratamento de imagens
- Criação de conteúdo audiovisual sob demanda
- **4. Suporte técnico para eventos**
- Sonorização e iluminação
- Transmissão ao vivo (streaming de eventos)
- Suporte técnico especializado ligado à operação do evento
- **5. Serviços criativos, artesanais ou personalizados**
- Produção artesanal sob encomenda
- Serviços artísticos para projetos específicos
- Trabalhos independentes fora de padrões comerciais comuns
- Atividades únicas ou altamente personalizadas

#### Características gerais

- São serviços sob medida
- Geralmente têm escopo único ou esporádico
- Envolvem personalização, criatividade ou suporte técnico específico
- Não possuem enquadramento claro em categorias como manutenção, saúde, educação, finanças, beleza ou entretenimento
- Advocacia, Contabilidade, Logística, EMpresas de software.

#### Não inclui

- Serviços financeiros (Categoria 59)
- Serviços de saúde, odontologia ou estética médica
- Manutenção de veículos (Categoria 40)
- Serviços de cuidado pessoal e beleza (Categoria 43)
- Telefonia, internet e TV por assinatura (Categorias 51 e 53)
- Serviços domésticos ou de manutenção residencial (Categoria 12)
- Eventos turísticos ou treinamentos (Categorias 21 e 20)

[↑ Voltar ao índice rápido](#indice-rapido-de-categorias)

---

<a id="categoria-4417-emprestimos-e-prestacoes"></a>

### Categoria `4417` — Empréstimos e Prestações

| Campo | Valor |
|---|---|
| Código do grupo | `8` |
| Grupo | Despesas Pessoais |
| Código da categoria | `4417` |
| Categoria | Empréstimos e Prestações |

#### Definição

Use esta categoria para registrar pagamentos de prestações diversas relacionados a empréstimos, adiantamentos ou créditos contratados, exceto quando o pagamento se referir à compra de veículos ou imóveis, que possuem categorias específicas.

#### Inclui

- **1. Empréstimos pessoais**
- Parcelas de empréstimos pessoais contratados em bancos, fintechs, financeiras ou cooperativas
- Empréstimos com débito em conta
- Empréstimos via aplicativos de crédito
- **2. Cheque especial**
- Pagamentos de uso do cheque especial
- Amortização de saldo devedor de limite utilizado
- Encargos e parcelas relacionadas ao pagamento do cheque especial
- **3. Parcelas de cartão de crédito em atraso**
- Cobranças referentes a parcelamento de fatura
- Renegociação de saldo devedor do cartão
- Pagamentos de parcelamento do rotativo
- Lançamentos relacionados ao parcelamento automático da fatura
- **4. Prestações diversas não classificáveis em outras categorias de crédito**
- Qualquer prestação recorrente ou parcelamento que não esteja vinculado à compra de bem imóvel ou veículo
- Renegociações de dívidas gerais com instituições financeiras
- Importante: categorias específicas devem ser usadas em vez desta quando aplicável
- Prestação de veículos
  - → Categoria 36 – Compra de Veículo
- Prestação de imóveis / financiamento imobiliário
  - → Categoria 9 – Compra de Imóveis

#### Não inclui

- Tarifas e serviços financeiros (Categoria 59)
- Pagamentos de cartão de crédito (Categoria 111 – Cartão de Crédito)
- IOF ou outros impostos (Categorias 3787, 56 etc.)
- Empréstimos entre pessoas físicas (se houver categoria própria)
- Compras parceladas específicas (devem ser classificadas pela natureza do item comprado)

[↑ Voltar ao índice rápido](#indice-rapido-de-categorias)

---

<a id="grupo-9-comunicacao"></a>

## Grupo `9` — Comunicação

**Quantidade de categorias:** 2

<a id="categoria-51-telefonia-e-internet"></a>

### Categoria `51` — Telefonia e Internet

| Campo | Valor |
|---|---|
| Código do grupo | `9` |
| Grupo | Comunicação |
| Código da categoria | `51` |
| Categoria | Telefonia e Internet |

#### Definição

Use esta categoria para registrar gastos relacionados a serviços de telefonia (fixa e móvel) e de acesso à internet, contratados junto a operadoras e provedores.

#### Inclui

- **1. Telefonia fixa**
- Pagamentos a empresas que prestam serviço de telefonia fixa
- Operadoras tradicionais de telefonia ou empresas de informática que fornecem telefonia via internet (VoIP)
- **2. Telefonia móvel**
- Pagamentos de planos de celular (pós, pré ou controle)
- Recargas de créditos para telefonia móvel
- Serviços adicionais contratados junto à operadora (pacotes de dados, SMS, voz, roaming etc.)
- **3. Internet**
- Pagamentos a provedores de internet (ISPs — Internet Service Providers)
- Serviços de internet banda larga, fibra óptica, 4G/5G residencial ou empresarial
- Combos que incluam internet, TV e telefonia, desde que a cobrança esteja associada ao serviço de telecomunicação
- Exemplos de empresas incluídas
- Claro, Vivo, TIM, Oi, Algar, Sky, GVT (quando ainda aparece em faturas)
- Provedores regionais de internet via fibra, rádio ou cabo

[↑ Voltar ao índice rápido](#indice-rapido-de-categorias)

---

<a id="categoria-53-assinatura-tv-e-streaming"></a>

### Categoria `53` — Assinatura TV e Streaming

| Campo | Valor |
|---|---|
| Código do grupo | `9` |
| Grupo | Comunicação |
| Código da categoria | `53` |
| Categoria | Assinatura TV e Streaming |

#### Definição

Use esta categoria para registrar pagamentos de serviços de transmissão de conteúdo audiovisual, incluindo TV por assinatura e plataformas de streaming digital.

De animes como Crunchroll, de música como Spotfy.

#### Inclui

- **1. TV por assinatura**
- Pagamentos de TV a cabo, TV por satélite e TV via internet (IPTV)
- **Lançamentos de operadoras como:**
- SKY*
- Claro TV
- Vivo TV
- Oi TV
- NET (quando ainda aparecer em lançamentos antigos)
- **2. Serviços de streaming**
- **Assinaturas de plataformas digitais, como:**
- Netflix
- Amazon Prime Video
- Disney+
- Globoplay
- HBO Max
- Apple TV+
- Paramount+
- Outras plataformas de vídeo sob demanda (VOD)
- **3. Serviços mistos ou difíceis de identificar**
- **Lançamentos com termos genéricos relacionados a serviços de comunicação, quando não estiver claro se é internet ou TV, especialmente em nomes que aparecem em múltiplos contextos, como:**
- SKY (podendo ser TV, combo internet+TV ou até nome de estabelecimentos comerciais não relacionados)
- Quando houver dúvida e o nome remeter a provedor de TV ou conteúdo audiovisual, classificar nesta categoria.

#### Observações importantes

- O termo SKY aparece também em empreendimentos, shoppings e outros estabelecimentos que não são serviços de TV, o que torna a classificação desafiadora.
- Quando o lançamento não deixar claro o tipo de serviço, mas indicar relação com comunicação/assinatura, ele será classificado nesta categoria (53) por padrão.
- Pacotes combinados de internet + TV podem ser classificados aqui se o lançamento se referir majoritariamente ao serviço de TV ou se a descrição não especificar claramente o componente de internet.

#### Não inclui

- Serviços de telefonia ou internet isolados (Categoria 51 – Telefonia e Internet)
- Compras de equipamentos como TV, roteadores, caixas de som etc.
- Assinaturas digitais relacionadas a jornais, revistas ou livros (Categoria 26 – Publicações Digitais)

[↑ Voltar ao índice rápido](#indice-rapido-de-categorias)

---

<a id="grupo-10-tarifas-e-impostos"></a>

## Grupo `10` — Tarifas e impostos

**Quantidade de categorias:** 8

<a id="categoria-54-iptu"></a>

### Categoria `54` — IPTU

| Campo | Valor |
|---|---|
| Código do grupo | `10` |
| Grupo | Tarifas e impostos |
| Código da categoria | `54` |
| Categoria | IPTU |

#### Definição

Use esta categoria para registrar pagamentos de IPTU (Imposto Predial e Territorial Urbano) e demais cobranças municipais relacionadas a esse tributo.

#### Inclui

- Pagamentos de IPTU realizados diretamente ao município
- Boletos ou guias emitidos por prefeituras municipais
- Parcelas mensais, anuais ou pagamentos à vista do imposto
- Taxas acessórias vinculadas ao IPTU quando incluídas no mesmo boleto (ex.: taxa de coleta de lixo quando cobrada junto)

#### Não inclui

- Pagamentos de condomínio (Categoria 10 – Aluguel e Condomínio)
- Pagamentos de financiamento imobiliário (Categoria 9 – Compra de Imóveis)
- IPVA ou outras taxas de veículos
- Taxas municipais que não estejam associadas ao IPTU

[↑ Voltar ao índice rápido](#indice-rapido-de-categorias)

---

<a id="categoria-55-ipva-e-gastos-detran"></a>

### Categoria `55` — IPVA e Gastos Detran

| Campo | Valor |
|---|---|
| Código do grupo | `10` |
| Grupo | Tarifas e impostos |
| Código da categoria | `55` |
| Categoria | IPVA e Gastos Detran |

#### Definição

Use esta categoria para registrar pagamentos relacionados a tributos e serviços de órgãos de trânsito, especialmente aqueles vinculados a veículos.

#### Inclui

- **1. Tributos**
- IPVA (Imposto sobre a Propriedade de Veículos Automotores)
- Pagamentos de IPVA à Secretaria da Fazenda Estadual (SEFAZ)
- **2. Taxas e serviços do Detran**
- **Taxas do Detran, incluindo:**
- Licenciamento anual
- Emissão de CRLV ou CRV
- Transferência de propriedade
- Emplacamento e lacração
- Segunda via de documentos
- Taxas de vistoria
- Multas de trânsito pagas diretamente ao Detran
- **3. Pagamentos correlatos**
- Boletos, guias e DARFs vinculados a serviços de trânsito

#### Não inclui

- Seguro de veículos (Categoria 39 – Seguros de Veículos)
- Serviços de manutenção, oficinas ou autopeças (Categoria 40 – Serviços e Manutenção)
- Abastecimento de combustível (Categoria 37 – Combustível)
- Pedágios e estacionamentos (Categoria 38 – Estacionamento e Pedágio)
- Financiamento ou consórcio de veículos (Categoria 36 – Compra de Veículo)

[↑ Voltar ao índice rápido](#indice-rapido-de-categorias)

---

<a id="categoria-56-imposto-de-renda"></a>

### Categoria `56` — Imposto de Renda

| Campo | Valor |
|---|---|
| Código do grupo | `10` |
| Grupo | Tarifas e impostos |
| Código da categoria | `56` |
| Categoria | Imposto de Renda |

#### Definição

Use esta categoria para registrar pagamentos relacionados ao Imposto de Renda, seja de pessoas físicas ou jurídicas, incluindo guias e documentos de arrecadação emitidos pela Receita Federal.

#### Inclui

- Pagamentos de DARF relacionados ao Imposto de Renda (IRPF ou IRPJ)
- **Lançamentos identificados como:**
- RFB – Pagamento DARF/RFB
- RFB – Doc. Arrec. e‑Social
- RFB – DARF
- RFB – Pgto DARF/Sist. Dara
- Receita Federal
- Secretaria da Receita Federal do Brasil
- Pagamentos de cotas de Imposto de Renda
- Pagamentos referentes a multas ou juros vinculados ao IR
- Pagamentos de restituições negativas (quando aplicável em pessoa jurídica)

#### Não inclui

- Pagamentos de tributos estaduais, como IPVA (Categoria 55)
- Pagamentos de tributos municipais, como IPTU (Categoria 54)
- Contribuições previdenciárias ou trabalhistas (FGTS, INSS, eSocial doméstico), caso haja categoria própria
- Tarifas bancárias ou serviços financeiros (Categoria 59)

[↑ Voltar ao índice rápido](#indice-rapido-de-categorias)

---

<a id="categoria-57-iss-imposto-sobre-servicos"></a>

### Categoria `57` — ISS(Imposto sobre Serviços)

| Campo | Valor |
|---|---|
| Código do grupo | `10` |
| Grupo | Tarifas e impostos |
| Código da categoria | `57` |
| Categoria | ISS(Imposto sobre Serviços) |

#### Definição

Use esta categoria para registrar pagamentos relacionados ao ISS – Imposto Sobre Serviços, tributo municipal cobrado sobre a prestação de serviços.

#### Inclui

- Pagamentos de ISS realizados diretamente ao município
- Guias de recolhimento emitidas pela prefeitura ou sistema municipal
- DARs, DAMs ou documentos de arrecadação vinculados ao ISS
- **Pagamentos de ISS sobre:**
- Serviços prestados por profissionais autônomos
- Serviços contratados por empresas (quando o contribuinte é responsável pelo recolhimento)
- Notas fiscais de serviços que exijam retenção ou recolhimento do imposto
- **Exemplos de descrições típicas:**
- ISS – Prefeitura Municipal
- ISSQN – Imposto Sobre Serviço
- DAM – ISS
- Guia ISS Municipal

#### Não inclui

- Pagamentos de IPTU (Categoria 54 – IPTU)
- Pagamentos de IPVA ou taxas do Detran (Categoria 55 – IPVA e Gastos Detran)
- Pagamentos de Imposto de Renda (Categoria 56 – Imposto de Renda)
- Pagamentos de serviços em si (estes devem ser classificados na categoria correspondente ao tipo de serviço prestado)

[↑ Voltar ao índice rápido](#indice-rapido-de-categorias)

---

<a id="categoria-58-gps-guia-de-previdencia-social"></a>

### Categoria `58` — GPS(Guia de Previdência Social)

| Campo | Valor |
|---|---|
| Código do grupo | `10` |
| Grupo | Tarifas e impostos |
| Código da categoria | `58` |
| Categoria | GPS(Guia de Previdência Social) |

#### Definição

Use esta categoria para registrar pagamentos relacionados à Guia da Previdência Social (GPS), destinados ao recolhimento de contribuições ao INSS.

#### Inclui

- Pagamentos de GPS feitos por contribuintes individuais, MEIs, empregadores domésticos ou empresas
- **Lançamentos que aparecem com descrições como:**
- INSS arrecadação GPS ident
- INSS arrec GPS ident
- INSS arrecadação MPAS INSS GPS
- Pagamento de GPS RFB
- RFB – Pagamento de GPS
- Guias de contribuição previdenciária emitidas pela Receita Federal ou INSS
- Recolhimento de contribuições mensais, atrasadas, complementares ou regularizações de débitos previdenciários

#### Exemplos comuns de uso

- Profissionais autônomos recolhendo INSS como contribuinte individual
- MEI recolhendo parte previdenciária (GPS complementar, quando houver)
- Empregadores pagando contribuição por empregado doméstico (quando ainda houver uso de GPS)
- Empresas recolhendo contribuições específicas via GPS (situações residuais)

#### Não inclui

- Pagamentos de Imposto de Renda (Categoria 56 – Imposto de Renda)
- Pagamentos de ISS municipal (Categoria 57 – ISS)
- Pagamentos de IPTU (Categoria 54)
- Pagamentos de IPVA ou taxas do Detran (Categoria 55)
- Contribuições previdenciárias via DARF não relacionadas à GPS (devem ir para categorias correspondentes)

[↑ Voltar ao índice rápido](#indice-rapido-de-categorias)

---

<a id="categoria-59-servicos-financeiros"></a>

### Categoria `59` — Serviços Financeiros

| Campo | Valor |
|---|---|
| Código do grupo | `10` |
| Grupo | Tarifas e impostos |
| Código da categoria | `59` |
| Categoria | Serviços Financeiros |

#### Definição

Use esta categoria para registrar gastos relacionados a tarifas, taxas e serviços financeiros cobrados por instituições bancárias, fintechs, cooperativas de crédito e demais instituições do sistema financeiro, bem como operações de câmbio.

#### Inclui

- **1. Tarifas e taxas bancárias**
- Tarifas de manutenção de conta corrente
- Tarifas de pacote de serviços
- Tarifas de transferência (quando identificadas como tarifa e não como transferência em si)
- Tarifas de DOC/TED
- Tarifas PIX quando aplicável
- Taxas de emissão de boletos
- Tarifas de cartão de crédito, anuidade e serviços financeiros associados
- Encargos, ajustes financeiros ou taxas administrativas cobrados pelo banco
- Tarifas de saque ou uso de caixas eletrônicos
- Multas e encargos bancários não relacionados a compras de produtos
- **2. Operações de câmbio**
- Compra ou venda de moeda estrangeira
- Taxas de câmbio e tarifas de remessas internacionais
- IOF sobre operações de câmbio
- Lançamentos de casas de câmbio e plataformas especializadas
- Observação: Contribuições voluntárias ou doações devem ser classificadas na Categoria 47 – Doações.

#### Não inclui

- Pagamentos de serviços ou produtos adquiridos com cartão (devem ir para categorias específicas)
- Transferências bancárias entre contas próprias ou para terceiros (categoria de transferências correspondente)
- Impostos, tributos e contribuições governamentais (IPTU, IPVA, IR, GPS, ISS etc.)
- Mensalidades de assinatura de serviços que não sejam financeiros

[↑ Voltar ao índice rápido](#indice-rapido-de-categorias)

---

<a id="categoria-3787-iof"></a>

### Categoria `3787` — IOF

| Campo | Valor |
|---|---|
| Código do grupo | `10` |
| Grupo | Tarifas e impostos |
| Código da categoria | `3787` |
| Categoria | IOF |

#### Definição

Use esta categoria para registrar lançamentos que referenciam diretamente o IOF (Imposto sobre Operações Financeiras), independentemente do tipo de operação financeira à qual o tributo esteja vinculado.

#### Inclui

- **IOF sobre operações de crédito, como:**
- Empréstimos
- Financiamentos
- Rotativo do cartão de crédito
- Parcelamento de fatura
- IOF sobre operações de câmbio, incluindo compra e venda de moeda estrangeira
- IOF sobre operações de seguro, quando indicado separadamente
- IOF sobre operações de títulos e valores mobiliários
- **Lançamentos com descrições como:**
- IOF
- Imposto IOF
- IOF Crédito
- IOF Câmbio
- IOF Seguro
- IOF Rotativo
- IOF Operações Financeiras

#### Não inclui

- Tarifas bancárias e serviços financeiros que não sejam IOF (Categoria 59 – Serviços Financeiros)
- Impostos de outras naturezas (IPTU, IPVA, IR, ISS, GPS etc.)
- Juros, multas ou encargos que não correspondam ao imposto IOF
- Pagamentos de operações financeiras sem indicação do imposto em si (ex.: empréstimos devem ser classificados na categoria correspondente)

[↑ Voltar ao índice rápido](#indice-rapido-de-categorias)

---

<a id="categoria-3788-encargos-e-tarifas"></a>

### Categoria `3788` — Encargos e Tarifas

| Campo | Valor |
|---|---|
| Código do grupo | `10` |
| Grupo | Tarifas e impostos |
| Código da categoria | `3788` |
| Categoria | Encargos e Tarifas |

#### Definição

Use esta categoria para registrar lançamentos relacionados a tarifas, encargos e cobranças diversas que não estejam vinculadas a serviços financeiros tradicionais.

Também inclui contribuições obrigatórias para entidades de classe, conforme vinculação ao CNAE 9412-0/99 (Entidades de Classe).

#### Inclui

- **1. Encargos e tarifas gerais (não financeiras)**
- Multas diversas que não pertencem a categorias específicas
- Juros cobrados por atraso em pagamentos de serviços ou contratos
- Encargos administrativos aplicados por empresas, instituições ou prestadores de serviços
- Tarifas operacionais que não sejam tarifas bancárias
- (tarifas bancárias pertencem à Categoria 59 – Serviços Financeiros)
- **2. Contribuições obrigatórias para entidades de classe**
- **Contribuições, anuidades ou taxas cobradas por:**
- Sindicatos
- Associações profissionais
- Ordens e conselhos
- Entidades de classe diversas
- Imposto municpio caem aqui nesta categoria
- Lançamentos vinculados ao CNAE 9412099 – Entidades de Classe
- Pagamentos recorrentes de manutenção, contribuição ou representação profissional obrigatória
- **3. Lançamentos genéricos de encargos**
- Cobranças avulsas sem classificação clara que representem penalidades, ajustes ou correções
- Taxas administrativas aplicadas por prestadores de serviço fora do setor financeiro

#### Não inclui

- Tarifas, taxas e serviços financeiros
  - → Categoria 59 – Serviços Financeiros
- Multas de trânsito, licenciamento, IPVA ou taxas de Detran
  - → Categoria 55
- Contribuições voluntárias ou doações
  - → Categoria 47 – Doações
- Encargos dentro de faturas de cartão (ex.: IOF, juros do rotativo)
  - → Categorias 111, 3787, 59, conforme o caso

#### Observações importantes

- Impostos que não sejam os que já possuem categoria específica caem na 3788
- Esta categoria não se refere a serviços financeiros nem a penalidades claramente classificáveis (como multas de trânsito).
- Ela deve ser usada quando o lançamento for um encargo, taxa ou contribuição obrigatória que não se encaixa em nenhuma categoria mais específica, especialmente relacionadas a entidades de classe e cobranças administrativas.

[↑ Voltar ao índice rápido](#indice-rapido-de-categorias)

---

<a id="grupo-12-fatura"></a>

## Grupo `12` — Fatura

**Quantidade de categorias:** 1

<a id="categoria-111-cartao-de-credito"></a>

### Categoria `111` — Cartão de Crédito

| Campo | Valor |
|---|---|
| Código do grupo | `12` |
| Grupo | Fatura |
| Código da categoria | `111` |
| Categoria | Cartão de Crédito |

#### Definição

Use esta categoria para registrar pagamentos de faturas de cartão de crédito, independentemente do banco, instituição financeira ou operadora emissora do cartão.

#### Inclui

- **Pagamentos de faturas de cartão de crédito, em qualquer modalidade:**
- Cartões bancários tradicionais
- Fintechs (ex.: Nubank, Inter, C6, Mercado Pago, etc.)
- Cartões private label (cartões de loja com bandeira própria)
- **Pagamentos realizados por:**
- Boleto
- PIX
- Débito automático
- Transferência
- Pagamentos de faturas de bancos quando claramente identificados como fatura ou cobrança de cartão
- **Lançamentos que referenciam diretamente o código da fatura, como:**
- Pgto Fatura Cartão
- Pagamento Cartão
- FATURA VISA/MASTERCARD/ELO
- Débito Fatura Cartão

#### Observações importantes

- Esta categoria não registra compras feitas com cartão, mas somente o pagamento da fatura.
- Compras individuais devem ser categorizadas conforme o tipo de gasto (alimentação, saúde, serviços etc.).
- Em casos em que o lançamento não é claro, mas aparece como ""fatura"", ""cartão"" ou ""cartão crédito"", deve ser direcionado para esta categoria.

#### Não inclui

- Encargos, multas ou juros lançados dentro da fatura (que seguem normalmente o próprio pagamento da fatura)
- Tarifas bancárias e anuidades (Categoria 59 – Serviços Financeiros)
- Compras parceladas marcadas como ""Cartão"" — devem ser categorizadas pelo tipo de compra
- Pagamentos de empréstimos, financiamentos ou consórcios

[↑ Voltar ao índice rápido](#indice-rapido-de-categorias)

---

<a id="grupo-11-outros"></a>

## Grupo `11` — Outros

**Quantidade de categorias:** 5

<a id="categoria-279-gastos-diversos"></a>

### Categoria `279` — Gastos Diversos

| Campo | Valor |
|---|---|
| Código do grupo | `11` |
| Grupo | Outros |
| Código da categoria | `279` |
| Categoria | Gastos Diversos |

#### Definição

Use esta categoria para registrar lançamentos que não se enquadram em nenhuma das categorias existentes, seja por falta de informação, por descrição genérica ou por natureza não identificada do gasto.

Esta categoria funciona como uma categoria residual — destinada a agrupar despesas que não podem ser classificadas com precisão nas demais categorias disponíveis.

#### Inclui

- Lançamentos com descrições genéricas ou insuficientes, impossíveis de associar a um tipo específico de produto ou serviço
- (ex.: “Pagamento”, “Compra”, “Transação”, sem detalhes).
- Despesas que não pertencem claramente a nenhuma categoria definida no sistema.
- Lançamentos atípicos, pontuais ou não recorrentes que não se adequem às categorias padrão.
- Pagamentos em que o contexto não pode ser identificado (falta de nome do estabelecimento, siglas desconhecidas, códigos internos, etc.).
- Gasto classificado manualmente pelo cliente como “diverso” ou “outros”.

#### Não inclui

- Lançamentos que possam ser identificados e direcionados para categorias já existentes (alimentação, saúde, transporte, serviços financeiros etc.).
- Despesas com serviços ou produtos quando o nome do estabelecimento indicar claramente o tipo da categoria correspondente.
- Transferências entre contas ou operações financeiras específicas (devem ir para categorias adequadas, como Serviços Financeiros).

#### Observações importantes

- A Categoria 279 deve ser utilizada apenas como último recurso, quando realmente não houver elementos suficientes para classificar o lançamento de forma mais precisa.

[↑ Voltar ao índice rápido](#indice-rapido-de-categorias)

---

<a id="categoria-39434-cheque"></a>

### Categoria `39434` — Cheque

| Campo | Valor |
|---|---|
| Código do grupo | `11` |
| Grupo | Outros |
| Código da categoria | `39434` |
| Categoria | Cheque |

#### Definição

Categoria para agrupar lançamentos que relacionam gastos realizados por meio de emissão de cheque.

Lançamentos de custódia de cheques também entram nesta categoria.

[↑ Voltar ao índice rápido](#indice-rapido-de-categorias)

---

<a id="categoria-39435-saque"></a>

### Categoria `39435` — Saque

| Campo | Valor |
|---|---|
| Código do grupo | `11` |
| Grupo | Outros |
| Código da categoria | `39435` |
| Categoria | Saque |

#### Definição

Use esta categoria para registrar lançamentos relacionados a saques de dinheiro em espécie, realizados em agências bancárias, terminais de autoatendimento ou correspondentes autorizados.

#### Inclui

- **Saques em dinheiro efetuados em:**
- Agências bancárias
- Caixas eletrônicos / ATMs
- Terminais de autoatendimento
- Caixas 24h
- Correspondentes bancários (ex.: lotéricas, redes autorizadas)
- Saques realizados com cartão bancário, cartão da conta ou cartão de benefício
- **Lançamentos identificados como:**
- Saque
- Retirada
- ATM
- Cash withdrawal
- Saque 24h

#### Não inclui

- Transferências bancárias entre contas (categoria de transferências específica)
- Pagamentos de compras ou serviços
- Adiantamentos em cartão de crédito (devem ser categorizados como operação de crédito ou financeira)
- Depósitos ou recebimentos em espécie (categoria de receitas correspondente)

#### Observações importantes

- Quando o lançamento aparece apenas como “SAQUE” sem contexto adicional, ele deve ser direcionado para esta categoria, pois a natureza da transação é clara.

[↑ Voltar ao índice rápido](#indice-rapido-de-categorias)

---

<a id="categoria-39436-transferencia"></a>

### Categoria `39436` — Transferência

| Campo | Valor |
|---|---|
| Código do grupo | `11` |
| Grupo | Outros |
| Código da categoria | `39436` |
| Categoria | Transferência |

#### Definição

Use esta categoria para registrar transferências de valores realizadas entre contas, especialmente quando o destinatário é pessoa física.

Essa categoria abrange movimentações financeiras que representam envio de dinheiro, mas que não correspondem a pagamentos de produtos ou serviços — apenas transferência de recursos.

#### Inclui

- **Transferências enviadas para pessoas físicas por:**
- PIX
- TED
- DOC
- Transferência entre contas de diferentes instituições
- Transferências entre contas correntes e poupança de titularidade diferente
- PIX enviados a pessoas físicas sempre entram nesta categoria, salvo quando claramente associados a pagamentos de produtos/serviços (e o cliente reclassificar).
- Transferências enviadas para familiares, amigos ou terceiros, quando não identificadas como pensão, serviço ou qualquer outro tipo de despesa específica.
- Movimentações entre contas do mesmo titular em bancos diferentes, quando registradas como transferência enviada.

#### Não inclui

- PIX enviados para pagamento de produtos, serviços ou estabelecimentos comerciais
  - → devem ir para a categoria correspondente ao tipo de gasto
- Transferências internas entre contas da mesma instituição que aparecem como movimentação automática
  - → categoria interna da instituição, se existir
- Pagamentos de faturas, empréstimos ou boletos
  - → categorias específicas (111, 4417, etc.)
- Transferências que representam pensão alimentícia
  - → Categoria 45 – Pensão Alimentícia
- Envio de valores para entidades de classe, instituições, doações ou pagamentos identificados
  - → categorias específicas

#### Observações importantes

- Como grande parte dos PIX enviados aparece com descrições curtas ou sem finalidade clara, esta categoria funciona como categoria padrão para transferências a pessoas físicas quando não é possível identificar outra natureza de despesa.

[↑ Voltar ao índice rápido](#indice-rapido-de-categorias)

---

<a id="categoria-39437-boletos-diversos"></a>

### Categoria `39437` — Boletos Diversos

| Campo | Valor |
|---|---|
| Código do grupo | `11` |
| Grupo | Outros |
| Código da categoria | `39437` |
| Categoria | Boletos Diversos |

#### Definição

Use esta categoria para registrar pagamentos de boletos quando não for possível identificar claramente a classe ou finalidade do lançamento, mas onde a descrição contém explicitamente o termo “boleto”.

Essa categoria deve ser utilizada somente quando o boleto não puder ser classificado em nenhuma categoria específica, e NÃO deve ser substituída pela categoria 279 (Outros Diversos), já que a presença da palavra boleto garante a natureza da operação.

#### Inclui

- Pagamentos de boletos bancários cuja finalidade não está clara na descrição
- **Boletos pagos via:**
- Internet banking
- Mobile banking
- Correspondentes bancários
- Terminais de autoatendimento
- **Boletos genéricos com descrições como:**
- Pagamento de boleto
- Pgto boleto
- Boleto bancário
- Boleto seguido de código ou referência não identificável
- Lançamentos em que somente a informação “boleto” aparece, sem identificação do serviço, produto ou empresa

#### Não inclui

- **Boletos onde é possível identificar claramente a natureza do gasto, como:**
- Energia, água, internet, telefonia, saúde, educação, condomínio, aluguel, impostos etc.
  - → Sempre usar a categoria correspondente ao tipo de despesa.
- Boletos de financiamento, consórcio ou empréstimo
  - → Categorias 9, 36, 4417 etc.
- Boletos de cartão de crédito
  - → Categoria 111 – Cartão de Crédito.
- Boletos de seguros
  - → Categorias 39, 46, 3790, conforme o caso.
- Boletos claramente vinculados a empresas identificáveis ou a serviços específicos.

#### Observações importantes

- Esta categoria serve como categoria de fallback EXCLUSIVAMENTE para boletos sem identificação clara.
- Se a descrição permitir identificar a empresa, o tipo de serviço ou o tipo de gasto, NÃO utilizar esta categoria.

[↑ Voltar ao índice rápido](#indice-rapido-de-categorias)

---

<a id="grupo-14-agro"></a>

## Grupo `14` — Agro

**Quantidade de categorias:** 5

<a id="categoria-300-receitas-agro"></a>

### Categoria `300` — Receitas Agro

| Campo | Valor |
|---|---|
| Código do grupo | `14` |
| Grupo | Agro |
| Código da categoria | `300` |
| Categoria | Receitas Agro |

#### Definição

Use esta categoria para registrar todos os lançamentos de crédito provenientes de empresas, atividades ou operações do setor agropecuário.

#### Inclui

- Créditos recebidos de empresas do setor agro (agroindústrias, cooperativas, cerealistas, produtores rurais, distribuidores de insumos etc.)
- Recebimentos relacionados a venda de produtos agrícolas ou pecuários
- **Pagamentos provenientes de atividades agropecuárias, como:**
- Grãos
- Pecuária
- Laticínios
- Frutas e hortaliças
- Insumos agrícolas
- Créditos por contratos de produção, parceria agrícola, integração ou entrega de mercadorias agro
- Receitas originadas de cooperativas rurais ou empresas com CNAE relacionado ao agronegócio
- Lançamentos identificados com nomes de empresas reconhecidamente atuantes no segmento agro

#### Não inclui

- Receitas de varejo, comércio ou serviços não relacionados ao setor agrícola
- Créditos originados de operações financeiras (empréstimos, resgates, transferências)
- Receitas pessoais que não estejam relacionadas a atividades agropecuárias
- Créditos com natureza de doação, transferência familiar ou devolução de valores

#### Observações importantes

- **Quando houver dúvida sobre a natureza do crédito, verificar:**
- Nome da empresa,
- CNAE,
- Descrição da operação,
- para confirmar se pertence ao segmento agro.

[↑ Voltar ao índice rápido](#indice-rapido-de-categorias)

---

<a id="categoria-310-criacoes"></a>

### Categoria `310` — Criações

| Campo | Valor |
|---|---|
| Código do grupo | `14` |
| Grupo | Agro |
| Código da categoria | `310` |
| Categoria | Criações |

#### Definição

Use esta categoria para registrar receitas, créditos ou movimentações financeiras relacionadas à criação e manejo de animais destinados à produção de alimentos ou derivados de origem animal.

#### Inclui

- **Receitas provenientes de pecuária, incluindo:**
- Gado de corte
- Gado leiteiro
- Produção de carne, leite e derivados
- **Receitas provenientes de avicultura, incluindo:**
- Criação de aves
- Produção de ovos
- Comercialização de frangos, galinhas, pintinhos etc.
- Receitas da suinocultura, envolvendo criação de suínos para corte e reprodução
- **Receitas associadas a outras atividades de criação animal, como:**
- Caprinocultura
- Ovinocultura
- Piscicultura (criação de peixes)
- Apicultura (mel e derivados)
- Cunicultura (criação de coelhos)
- Créditos de vendas, entregas ou contratos vinculados ao manejo de animais destinados à produção
- Receitas de cooperativas, laticínios, frigoríficos ou integradoras relacionadas à criação animal

#### Não inclui

- Receitas de lavouras, grãos ou agricultura em geral (devem ir para categoria apropriada, se houver)
- Receitas financeiras ou não relacionadas à atividade pecuária
- Créditos provenientes de empresas que não atuam na cadeia animal
- Serviços realizados por terceiros que não envolvam criação de animais

#### Observações importantes

- Usar esta categoria sempre que o crédito estiver diretamente ligado à produção animal, independentemente da espécie ou do modelo de produção (extensiva, intensiva, integrada etc.).

[↑ Voltar ao índice rápido](#indice-rapido-de-categorias)

---

<a id="categoria-330-cultivos"></a>

### Categoria `330` — Cultivos

| Campo | Valor |
|---|---|
| Código do grupo | `14` |
| Grupo | Agro |
| Código da categoria | `330` |
| Categoria | Cultivos |

#### Definição

Use esta categoria para registrar gastos ou movimentações financeiras relacionadas às atividades de plantio, cultivo, manejo e colheita de culturas agrícolas.

Essa categoria abrange toda a cadeia produtiva vegetal, desde a preparação do solo até a pós-colheita, incluindo culturas anuais, perenes e temporárias.

#### Inclui

- **1. Culturas agrícolas em geral**
- **Cultivo de grãos, como:**
- Soja
- Milho
- Arroz
- Trigo
- Feijão
- **Cultivo de plantas industriais, como:**
- Cana-de-açúcar
- Algodão
- Fumo
- **Cultivos perenes, como:**
- Café
- Frutíferas (laranja, limão, maçã, uva, banana etc.)
- Seringueira
- **Cultivos diversos, incluindo:**
- Hortaliças
- Plantas ornamentais
- Oleaginosas
- Cultivos especializados e regionais
- **2. Atividades de pós-colheita**
- **Gastos relacionadas a:**
- Beneficiamento
- Secagem
- Armazenagem
- Limpeza
- Classificação de grãos ou frutas
- Gastos de cooperativas, cerealistas, integradoras e agroindústrias
- **3. Receitas vinculadas à produção agrícola**
- Vendas de safra própria
- Entregas contratuais relacionadas a culturas agrícolas
- Créditos provenientes de indústrias de alimentos, exportadores, cooperativas ou trading companies relacionadas à agricultura

#### Não inclui

- Gastos provenientes de criação animal (Categoria 310 – Criações)
- Gastos relacionados a insumos, consultorias ou serviços — somente produção vegetal entra aqui

#### Observações importantes

- Use esta categoria sempre que o gasto estiver diretamente ligado à produção agrícola, incluindo culturas anuais, perenes, temporárias, industriais ou hortifrutigranjeiras.

[↑ Voltar ao índice rápido](#indice-rapido-de-categorias)

---

<a id="categoria-350-insumos"></a>

### Categoria `350` — Insumos

| Campo | Valor |
|---|---|
| Código do grupo | `14` |
| Grupo | Agro |
| Código da categoria | `350` |
| Categoria | Insumos |

#### Definição

Use esta categoria para registrar gastos, compras ou operações relacionadas a insumos utilizados na produção agrícola e pecuária.

Essa categoria abrange materiais, produtos, insumos biológicos e químicos, além de itens necessários para o desenvolvimento das atividades rurais.

#### Inclui

- **1. Defensivos agrícolas**
- Herbicidas
- Inseticidas
- Fungicidas
- Produtos fitossanitários em geral
- Defensivos biológicos
- **2. Fertilizantes, adubos e corretivos**
- Adubos químicos
- Fertilizantes organominerais
- Calcário e gesso agrícola
- Corretivos de solo
- Nutrição vegetal
- **3. Sementes e mudas certificadas**
- Sementes de soja, milho, arroz, trigo e demais culturas
- Sementes de pastagens
- Mudas de frutíferas, café, hortaliças e espécies perenes
- Material propagativo em geral
- **4. Insumos para pecuária**
- Rações e suplementos minerais
- Sal proteinado
- Núcleos proteicos
- Premixes e aditivos
- Insumos veterinários utilizados na produção animal (exceto serviços veterinários)
- **5. Comércio atacadista e distribuição de insumos**
- Compras realizadas em distribuidoras de insumos agropecuários
- Cooperativas que comercializam insumos
- Atacadistas de materiais e produtos agrícolas
- **6. Insumos de pós-plantio e produção**
- Substratos, bandejas de germinação
- Produtos para manejo e proteção de lavoura
- Itens de reparo e manutenção diretamente ligados à produção agrícola

#### Não inclui

- Máquinas, implementos ou equipamentos agrícolas (categoria própria caso exista)
- Serviços agrícolas ou pecuários (categoria de serviços específicos)
- Receitas de venda de produtos agro (categorias 300, 310, 330)
- Produtos destinados ao consumo pessoal ou doméstico
- Serviços veterinários ou laboratoriais
- Manutenção estrutural de fazenda (categoria de manutenção, se existir)

#### Observações importantes

- Use esta categoria sempre que o lançamento estiver associado a produtos essenciais para o processo produtivo rural, seja agrícola ou pecuário, incluindo insumos químicos, biológicos, nutricionais ou materiais de propagação vegetal.

[↑ Voltar ao índice rápido](#indice-rapido-de-categorias)

---

<a id="categoria-370-apoio-produtivo"></a>

### Categoria `370` — Apoio Produtivo

| Campo | Valor |
|---|---|
| Código do grupo | `14` |
| Grupo | Agro |
| Código da categoria | `370` |
| Categoria | Apoio Produtivo |

#### Definição

Use esta categoria para registrar gastos e serviços que dão suporte direto às atividades de produção agrícola e pecuária, abrangendo atividades operacionais, técnicas e logísticas necessárias para viabilizar, manter ou aprimorar a produção rural.

Essa categoria contempla serviços de apoio, atividades complementares e despesas produtivas que não são insumos nem a produção final, mas que fazem parte do processo produtivo.

#### Inclui

- **1. Serviços de apoio à agricultura**
- Preparação de solo (aração, gradagem, subsolagem)
- Plantio, replantio e tratos culturais
- Colheita mecanizada ou manual
- Atividades de pós-colheita operacional (serviços de terceiros)
- Serviços especializados de pulverização (terrestre ou aérea)
- Controle de pragas e doenças realizados por empresas terceirizadas
- Poda de árvores e manejo de lavouras permanentes
- Irrigação e serviços técnicos ligados à condução de lavouras
- **2. Serviços de apoio à pecuária**
- Manejo de pastagens
- Serviços especializados para manejo de rebanho
- Suporte técnico em confinamentos, nutrição ou manejo
- Serviços operacionais não veterinários
- **3. Locação ou uso de equipamentos produtivos**
- Aluguel de máquinas, implementos ou ferramentas utilizadas na produção
- Uso de tratores, colheitadeiras, pulverizadores, entre outros, quando contratados como serviço
- Equipamentos de apoio para manejo, irrigação ou colheita
- **4. Transporte e logística produtiva**
- Transporte de insumos, animais, grãos, frutas e outros produtos dentro do ciclo produtivo
- Fretes relacionados à produção (entrada ou saída operacional)
- **5. Outras despesas produtivas não classificadas em categorias específicas**
- Serviços personalizados vinculados ao processo produtivo agrícola ou pecuário
- Atividades de apoio não enquadradas em insumos (350), cultivos (330) ou criações (310)

#### Não inclui

- Insumos agrícolas e pecuários → Categoria 350
- Receitas agropecuárias → Categorias 300, 310 e 330
- Serviços administrativos, consultorias gerenciais ou despesas não produtivas
- Manutenção estrutural da propriedade não relacionada ao processo produtivo
- Compra de máquinas, equipamentos ou veículos (categoria própria, se existir)
- Serviços veterinários (categoria adequada, se houver)

#### Observações importantes

- Esta categoria deve ser usada sempre que o gasto der suporte direto ao processo produtivo, mas não for um insumo, não for a produção final e não se encaixar em outra categoria rural já definida.

[↑ Voltar ao índice rápido](#indice-rapido-de-categorias)

---

<a id="grupo-13-investimentos"></a>

## Grupo `13` — Investimentos

**Quantidade de categorias:** 2

<a id="categoria-448977-aplicacao"></a>

### Categoria `448977` — Aplicação

| Campo | Valor |
|---|---|
| Código do grupo | `13` |
| Grupo | Investimentos |
| Código da categoria | `448977` |
| Categoria | Aplicação |

#### Definição

Use esta categoria para registrar lançamentos relacionados a aplicações financeiras e investimentos, realizados por meio de instituições financeiras, corretoras, bancos ou plataformas de investimento.

#### Inclui

- **Aplicações financeiras em geral, como:**
- CDB
- RDB
- LC / LCI / LCA
- Fundos de investimento
- Tesouro Direto
- Poupança
- COE
- Debêntures
- Aportes em corretoras ou plataformas digitais de investimento
- Transferências realizadas para contas de investimento, desde que vinculadas à aplicação
- **Lançamentos identificados como:**
- Aplicação
- Investimento
- Aporte
- Aplicação financeira
- Transferência para investimento
- Investimentos automáticos programados por bancos ou corretoras

#### Não inclui

- Resgates de investimentos (categoria específica)
- Tarifas bancárias, IOF ou taxas — devem ir para categorias como Serviços Financeiros (59) ou IOF (3787)
- Pagamentos de previdência privada (Categoria 46 – Seguros e Previdência)
- Operações de câmbio (Categoria 59 – Serviços Financeiros, quando relacionadas à taxa)

[↑ Voltar ao índice rápido](#indice-rapido-de-categorias)

---

<a id="categoria-448978-resgate-de-investimentos"></a>

### Categoria `448978` — Resgate de Investimentos

| Campo | Valor |
|---|---|
| Código do grupo | `13` |
| Grupo | Investimentos |
| Código da categoria | `448978` |
| Categoria | Resgate de Investimentos |

#### Definição

Use esta categoria para registrar valores recebidos provenientes do resgate de aplicações financeiras, incluindo qualquer crédito decorrente do encerramento, liquidação, venda ou retirada de investimentos.

#### Inclui

- **Resgate de aplicações financeiras, como:**
- CDB / RDB
- LCI / LCA
- Fundos de investimento
- Tesouro Direto
- COE
- Debêntures
- Poupança
- Resgates parciais ou totais de investimentos em bancos, corretoras ou plataformas digitais
- **Créditos identificados por descrições como:**
- “Resgate de investimento”
- “Resgate de aplicação”
- “Crédito investimento”
- “Liquidação de aplicação”
- “Resgate fundo X”
- Valores recebidos após venda de ativos financeiros, quando repassados como crédito em conta
- Resgates programados automáticos realizados pelas instituições financeiras

#### Não inclui

- Aportes ou aplicações financeiras → Categoria 448977 – Aplicação
- Ganhos operacionais independentes (juros, dividendos, rendimentos) — se houver categoria dedicada
- Tarifas de resgate, IOF ou taxas administrativas → Categoria 59 ou 3787, conforme o caso
- Transferências pessoais → Categoria 39436 – Transferência
- Receitas não financeiras ou créditos operacionais de outra natureza

#### Observações importantes

- Classifique nesta categoria somente quando ficar claro que o crédito se refere ao resgate de uma aplicação financeira.
- Se o lançamento não indicar isso explicitamente, deve-se avaliar a categoria correspondente ou solicitar contexto adicional.

[↑ Voltar ao índice rápido](#indice-rapido-de-categorias)

---

# Pontos de atenção para validação

> Os itens abaixo foram mantidos como observações editoriais. Eles não substituem uma validação funcional das regras.

1. **Categoria `1` — Salário:** o texto inclui aposentadoria e BPC entre os exemplos, mas também menciona pensões, aposentadorias ou benefícios previdenciários entre os itens que não devem ser incluídos.
2. **Categoria `9` — Compra de Imóvel:** a linha sobre construtoras e incorporadoras aparece junto às exclusões e deve ser revisada para confirmar a regra desejada.
3. **Categoria `46` — Seguros e Previdência:** a definição inclui seguro de viagem, veículo e residencial, embora existam categorias específicas para seguro veicular (`39`) e seguro residencial (`3790`).
4. **Categoria `330` — Cultivos:** o texto combina receitas, gastos e movimentações financeiras. Vale confirmar se a categoria deve receber todos esses tipos de lançamento.
5. **Categoria `35` — Bar:** a regra abrange bares, restaurantes, cafés, padarias, delivery e outros estabelecimentos. Vale confirmar se o nome resumido da categoria deve permanecer como **Bar**.

# Apêndice — Resumo numérico

| Código do grupo | Grupo | Categorias |
|---:|---|---:|
| `0` | Sem categoria | 2 |
| `1` | Receitas | 5 |
| `2` | Casa | 9 |
| `3` | Educação | 5 |
| `4` | Lazer | 5 |
| `5` | Saúde | 4 |
| `6` | Alimentação | 2 |
| `7` | Transporte | 6 |
| `8` | Despesas Pessoais | 10 |
| `9` | Comunicação | 2 |
| `10` | Tarifas e impostos | 8 |
| `12` | Fatura | 1 |
| `11` | Outros | 5 |
| `14` | Agro | 5 |
| `13` | Investimentos | 2 |

---

_Fim do catálogo estruturado._
