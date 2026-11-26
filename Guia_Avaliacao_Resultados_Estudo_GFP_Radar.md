# Estudo dos seis indicadores GFP — Guia de avaliação dos resultados

**Projeto:** Radar Financeiro  
**Versão:** 1.0 · 26/11/2026  
**Destinatário:** desenvolvedor/analista responsável pela avaliação independente do pacote de resultados  
**Estado:** protocolo de análise; resultados reais ainda não recebidos para esta documentação.

## 1. Missão do avaliador

O objetivo central é compreender o comportamento real dos seis indicadores da tabela `DB2GFP.TRAN_RLZD_INST_PCT` e determinar, com evidências, **quais devem ser utilizados como filtros no Radar Financeiro, quais não devem ser utilizados e quais exigem condições adicionais**.

O estudo deve responder o que cada indicador representa, como o GFP o utiliza, quais lançamentos são retidos ou excluídos por cada predicado, qual a magnitude da exclusão e em quais tipos de operação ela é adequada ou problemática. Não se pretende reproduzir a interface do GFP, nem assumir que suas regras de apresentação sejam regras de validade econômica.

O trabalho do avaliador começa pelo ZIP de resultados da extração corporativa, não pela criação de novos gerenciadores ou pela reescrita do estudo. A entrega esperada é um parecer analítico independente, quantitativo, rastreável e acompanhado de recomendações. **Não alterar a regra 7 nem o código do Radar nesta etapa.** A aprovação de qualquer alteração será posterior.

### Perguntas que a análise precisa responder

1. Quais valores e combinações dos seis indicadores ocorrem efetivamente? Há valores fora de S/N?
2. O que os filtros isolados e combinados retêm/excluem em quantidade e valor absoluto, por produto e natureza?
3. Como as marcações variam por tipo de transação, categoria atual/original, instituição e características de cartão/conta-corrente?
4. O predicado atual do Radar perde operações relevantes ou mantém registros potencialmente redundantes? Quais são os exemplos agregados e respectivas magnitudes?
5. A exclusão de originais divididos pode omitir lançamentos se seus derivados não forem incorporados? A cobertura dos derivados é suficiente no recorte?
6. Quais diferenças são explicáveis por perspectivas de consumo, caixa e eventos, e quais permanecem sem explicação?
7. Que filtros são recomendáveis por finalidade, com quais ressalvas, e quais precisam de evidências adicionais?

## 2. Contexto da regra 7 do Radar

A especificação de referência está no notebook `radar_todos_v1.ipynb`, seção 7, e em `Documentacao_GFP_Regra_7_QT_MOV_CICLO.md`, seção 8. A métrica planejada `QT_MOV_CICLO BIGINT` conta IDs distintos `NR_TRAN_INST_PCT` por cliente (`CD_CLI = CD_CLI_REF`) participante do Radar, dentro de seu ciclo fechado, antes da reconciliação/neutralização. O predicado de elegibilidade vigente na especificação é:

```sql
CD_PRD IN (6, 9)
AND CD_EST_TRAN_INST = 0
AND CD_TIP_MOE_CRR = 'BRL'
AND (CD_NTZ_CTB_TRAN = 'C'
     OR (CD_NTZ_CTB_TRAN = 'D' AND IN_VSLO_CSM = 'S'))
```

| Natureza | CSM | Resultado do predicado, com demais condições atendidas |
|---|---|---|
| C | qualquer valor | Mantém |
| D | S | Mantém |
| D | N ou outro valor | Exclui |
| Outra | qualquer valor | Exclui |

CX, EVT, DVS, OCTR e IR não são filtros diretos dessa especificação. O estudo precisa testar a adequação dessa assimetria, não simplesmente ratificá-la. Não existe obrigação de adicionar os demais indicadores como filtros.

A regra 7 conta registros elegíveis, não operações econômicas únicas, receitas, despesas ou saldo. Crédito não significa necessariamente renda; débito não significa necessariamente consumo. O desenho do Radar prevê cinco dias externos a cada ciclo somente como contexto de pareamento, sem incrementar `QT_MOV_CICLO`. Um filtro pode eliminar uma contraparte necessária; apontar esse risco quando demonstrável. Não calcular pares, não alterar a lógica de reconciliação nem usar a janela coletiva como se fosse um ciclo individual. A extração agregada não permite medir diretamente o efeito por MCI, por ciclo, nem quantificar pares perdidos.

## 3. Universo, recortes e princípios metodológicos

| Parâmetro | Definição do estudo |
|---|---|
| Fonte principal | `DB2GFP.TRAN_RLZD_INST_PCT` |
| Período padrão | 26/10/2026 a 24/11/2026, inclusive (30 datas-calendário) |
| Limites SQL | `DT_TRAN >= DATE('2026-10-26') AND DT_TRAN < DATE('2026-11-25')` |
| Produtos | 6 (conta-corrente), 9 (cartão) |
| Estado | `CD_EST_TRAN_INST = 0` (efetivada) |
| Moeda | `CD_TIP_MOE_CRR = 'BRL'` |
| Clientes | População disponível/autorizada, sem filtro por MCI |
| Naturezas e categorias | Todas; inclusive valores não esperados, categoria zero e não mapeados |
| Seis indicadores | Sem filtragem no universo-base |
| Granularidade | Registros institucionais; agregados por dimensões de cada SQL |
| Execução | Leitura JDBC nativa, sequencial, READ_COMMITTED e autocommit, sem snapshot comum |

A janela aceita pelo módulo é de 15 a 30 dias completos; este estudo planejou 30. Confirmar as datas efetivas no manifesto e no SQL arquivado. Q01/Q01B não são temporais. Q05 e Q06 são recortes dos produtos 9 e 6. Q07 investiga uma tabela diferente, `TRAN_INCD_CLI`. Q08 restringe-se a originais divididos e derivados no escopo definido. Q10 amplia produto, estado e moeda, mantendo a janela. Q09 e Q10 são complementares, selecionadas na configuração planejada. Q12 está fora do escopo desta entrega.

Não aplicar o filtro do Radar à população original durante a análise: isso esconderia precisamente os registros que precisamos investigar. Não excluir ausência de complemento, categoria/grupo desconhecido ou valor fora do domínio. Não solicitar dados individualizados de clientes. A autorização para analisar ou compartilhar agregados deve respeitar as políticas corporativas; granularidade elevada pode exigir avaliação adicional de risco de reidentificação.

## 4. Dicionário dos indicadores e evidência anterior aos resultados

Os seis campos são documentados como `CHAR(1) NOT NULL` na tabela institucional. S/N é o domínio conceitual; não presumir que todas as linhas obedecem ao domínio. O catálogo anterior registra defaults CSM=S, CX=S, DVS=N, OCTR=N e IR=N; EVT não tem default declarado naquele catálogo (ERwin documenta S). Default não é regra de atribuição.

| Indicador | S | N | Interpretação e cuidado |
|---|---|---|---|
| `IN_VSLO_CSM` | Visível no consumo | Não visível no consumo | Perspectiva de consumo; não é sinônimo universal de despesa. ERwin O_Id 10603. |
| `IN_VSLO_CX` | Visível no caixa | Não visível no caixa | Perspectiva de fluxo de caixa; não prova alteração de saldo ou renda. O_Id 10601. |
| `IN_VSLO_EVT` | Visível nos eventos | Não visível nos eventos | Perspectiva de eventos; não é filtro geral de validade econômica. O_Id 9812. |
| `IN_DVS_LCTO` | Original dividido | Não dividido | Excluir o original sem considerar derivados pode causar omissão. O_Id 10995. |
| `IN_OCTR_TRAN` | Oculto | Não oculto | Ocultação não equivale a exclusão lógica ou invalidação. Respeitar finalidade e autorização. O_Id 10605. |
| `IN_TRAN_IR` | Marcado como dedutível | Não marcado | Marcação tributária, não comprovação de dedutibilidade nem regra de elegibilidade geral. O_Id 10599. |

### 4.1 O que já sabemos do código de leitura do GFP V7

O arquivo `tran.txt` contém consultas de seleção da versão V7. Na parte institucional, foram identificados os predicados abaixo. A coluna de estado distingue a lógica do GFP da especificação mais restritiva do Radar.

| Consulta Java V7 | Estado | Predicados relevantes |
|---|---|---|
| Listar transações / contar total | `!= 9` | `EVT = 'S'`, `DVS = 'N'` |
| Listar por categoria | `!= 9` | natureza D, `CSM = 'S'`, `DVS = 'N'` |
| Movimentação financeira | `!= 9` | natureza parametrizada, `CX = 'S'`, `DVS = 'N'`, exclusão do grupo 13 |
| Agendadas | `= 1` | produto 6, `EVT = 'S'`, `DVS = 'N'` |
| Imposto de renda | `!= 9` | natureza D, `CSM = 'S'`, `DVS = 'N'`, `OCTR != 'S'`, código IR parametrizado e grupo 13 excluído |

O GFP inclui manuais/derivados em determinadas consultas e tem condições adicionais de contas, marcas, categorias e grupos. A consulta IR utiliza `CD_TRAN_IR IN (...)`, não o predicado global `IN_TRAN_IR = 'S'`. A regra `OCTR = 'N'` avaliada na Q04 não é necessariamente equivalente a `OCTR != 'S'` se houver outros valores. `estado != 9` também não equivale a `estado = 0`.

Essas são evidências da lógica de leitura presente no arquivo, não da lógica de atribuição dos indicadores, nem garantia da versão implantada no ambiente. A análise deve classificar cada afirmação como **documentada**, **observada**, **inferida** ou **pendente**. Não transformar associações estatísticas em causalidade.

## 5. Mapa de consultas e interpretação dos resultados

Usar os SQLs arquivados dentro do ZIP efetivamente executado como contrato definitivo de colunas, condições e agrupamentos. O mapa abaixo descreve o desenho previsto, conferido no módulo de extração e na documentação/SQLs anteriores disponíveis.

| Consulta | Finalidade e retorno esperado | O que o avaliador deve fazer |
|---|---|---|
| Q00 | Uma linha de controle: limites, dias, mínimo/máximo observado, contagem e valores | Fixar denominadores, verificar período e existência de dados. Se zero, não emitir conclusão comportamental. |
| Q01 | Cadastro de categorias, descrição, natureza, grupo, código IR | Enriquecer Q03 e demais recortes, por categoria atual e original; preservar não mapeados. |
| Q01B | Cadastro de grupos | Identificar o significado real do grupo 13 e verificar unicidade. Não excluí-lo automaticamente. |
| Q02 | Combinações dos seis indicadores com `QT_TRAN`, `VL_TOTAL`, `VL_ABS` | Quantificar S/N/outros, combinações predominantes e raras; comparar com Q00/Q03. Até 64 combinações estritamente S/N. |
| Q03 | Matriz por produto, natureza, tipo, categoria atual/original e seis indicadores | Base explicativa principal: identificar quais operações e categorias são afetadas; reproduzir cenários Q04; segmentar C/D e produtos. |
| Q04 | Impacto dos predicados de retenção por produto e natureza | Comparar universo original, seis filtros isolados, regra do Radar e aproximações das perspectivas GFP. Quantificar retidos e excluídos. |
| Q05 | Produto 9: complemento cartão, tipo, pagamento/lançamento, parcelas, tarifas/crédito e relação com data da fatura | Investigar compras, parcelas, faturas, tarifas, estornos e créditos; comparar combinações de visibilidade. Não inferir pareamento individual. |
| Q06 | Produto 6: histórico/sub-histórico, relação entre documentos (sem exportar documentos) | Investigar transferências, Pix/TED, saques, salários, aplicações, resgates, empréstimos e tarifas conforme códigos identificáveis. Documento igual sugere mesma titularidade, não prova vínculo econômico. |
| Q07 | Inclusões em `TRAN_INCD_CLI`: manual ou derivado segundo referência ao original | Medir comportamento dos cinco indicadores disponíveis nessa extração; distinguir lançamentos manuais de derivados. Não somar automaticamente com universo institucional. |
| Q08 | Originais DVS=S e cobertura de derivados relacionados | Avaliar ausência de derivados, um derivado, dois ou mais com valor igual/diferente. Quantificar risco da exclusão de originais e limites temporais. |
| Q11 | Indicador IR × código IR × categorias e demais marcações selecionadas | Verificar correspondência e divergências; avaliar por que IR não deve ser generalizado sem finalidade tributária. |
| Q09 | Complementar: instituição participante e marca, com dimensões transacionais | Identificar heterogeneidade institucional e separar diferença de mix de operações de possíveis diferenças de marcação. |
| Q10 | Complementar: todos os produtos, estados e moedas na janela | Verificar comportamento fora do recorte, inclusive agendadas e estados excluídos. Reproduzir Q02 apenas no recorte principal. Nunca somar valores de moedas distintas. |

Q12 (cadastro/visibilidade de contas) foi retirada do escopo final. Não exigir seu CSV e não confundir visibilidade de conta com indicadores transacionais. Se uma hipótese exigir Q12, registrar a lacuna para uma investigação futura autorizada.

### 5.1 Cenários da Q04

Cada cenário mede **retenção**, não exclusão. As colunas são `QT_<CENARIO>` e `VL_ABS_<CENARIO>`; o controle é `ORIGINAL`. Os nomes abaixo correspondem ao contrato de `CENARIOS_Q04` no módulo.

| Cenário | Predicado adicional ao universo-base |
|---|---|
| ORIGINAL | Nenhum |
| CSM | CSM = S |
| CX | CX = S |
| EVT | EVT = S |
| DVS | DVS = N |
| OCTR | OCTR = N |
| IR | IR = S |
| RADAR | C ou (D e CSM = S) |
| CSM_D | D e CSM = S |
| GFP_EVT_INST | EVT = S e DVS = N |
| GFP_CX_INST | CX = S e DVS = N |
| GFP_CSM_INST | D e CSM = S e DVS = N |

As três últimas são aproximações da seleção institucional do GFP dentro do recorte do estudo, não reproduções integrais de suas consultas. Não incluem manuais/derivados, todas as restrições de contas, estado e demais regras do aplicativo. Usar os cenários como comparativos, não como escolhas automaticamente corretas.

## 6. Aceite técnico do pacote antes de interpretar resultados

### 6.1 Inventário e integridade

O pacote desejado é `ESTUDO_GFP_COMPLETO.zip`, com 29 arquivos: 13 CSVs, 13 SQLs, `Manifesto_Execucao.md`, `ESTUDO_RADAR.ipynb` e `estudo_indicadores_gfp.py`. Confirmar integridade ZIP/CRC, nomes únicos, ausência de caminhos perigosos na extração e, se fornecido separadamente, SHA-256 do recibo. O hash verifica igualdade de conteúdo, não substitui autorização ou autenticidade da fonte.

`HOMOLOGACAO_GFP.zip` contém apenas `teste.txt` e comprova infraestrutura, não resultados GFP. Não aceitá-lo como resposta ao estudo. A homologação reduzida já foi aprovada no driver e o usuário relatou download; isso não homologa as consultas transacionais.

O manifesto usa quatro estados de pacote: `COMPLETO`, `COMPLETO_COM_DIVERGENCIAS`, `PARCIAL` e `SEM_RESULTADOS`. Verificar cada estado de consulta, existência de seu CSV/SQL, contagem de linhas, horários, duração, erros e controles. O estado COMPLETO significa que o módulo concluiu as consultas selecionadas e não detectou divergência nos controles implementados; não prova cobertura econômica ou correção metodológica. Para o escopo integral, exigir também Q09/Q10. Em pacote parcial, analisar somente hipóteses sustentadas e enumerar lacunas; não descartar automaticamente dados válidos. Não considerar CSV ausente equivalente a zero.

### 6.2 Leitura correta dos dados

- CSV UTF-8, separador `;`, cabeçalho e decimal com ponto. Nulo é o token `\N`; texto que começa com barra invertida recebe uma barra adicional no começo. Decodificar sem confundir vazio, zero, N e nulo.
- Ler com biblioteca CSV que respeite aspas e quebras de linha. Usar inteiro para contagens e Decimal para dinheiro; evitar float e arredondamento prematuro. Conservar códigos/categorias como identificadores, inclusive zeros à esquerda se presentes.
- `QT_TRAN`: contagem de registros agregados. `VL_TOTAL`: soma do valor registrado (sem impor sinal por natureza). `VL_ABS`: soma de valores absolutos por registro, não valor de receita/despesa, saldo ou montante econômico líquido. Não usar `ABS(VL_TOTAL)` como substituto de `VL_ABS`.
- Q04 tem métricas de cenários e Q08 métricas próprias (`QT_ORIGINAIS`, `QT_DERIVADOS`, `VL_ORIGINAIS`, `VL_DERIVADOS`); não exigir esquema Q03 dessas consultas. Q01/Q01B são cadastros, não movimentações.
- O módulo usa uma triagem de cabeçalhos para impedir certas colunas identificadoras. Conferir também o conteúdo e o nível de agregação conforme a política corporativa. Não pedir chaves pessoais, CPF/CNPJ, IDs transacionais ou descrições livres para esclarecer hipóteses.

### 6.3 Dez controles cruzados implementados

Reproduzir os controles do manifesto independentemente, com as mesmas chaves e medidas. Para cada divergência, registrar observado, esperado e diferença; não ajustar números para forçar igualdade.

| Nº | Controle | Condição de aceite |
|---|---|---|
| 1 | Q00 × Q02 | Igualdade de quantidade, valor registrado e absoluto |
| 2 | Q00 × Q03 | Igualdade das três medidas |
| 3 | Q02 × Q03 | Igualdade das três medidas em cada combinação dos seis indicadores |
| 4 | Q04 × Q03 | Reproduzir todos os cenários por produto e natureza, em quantidade e valor absoluto |
| 5 | Q05 × Q03 | Igualdade das três medidas para produto 9 |
| 6 | Q06 × Q03 | Igualdade das três medidas para produto 6 |
| 7 | Q08 × Q03 | Originais DVS=S por produto, natureza e CSM/CX/EVT |
| 8 | Q09 × Q03 | Igualdade das três medidas no universo principal |
| 9 | Q11 × Q03 | Igualdade das três medidas no universo principal |
| 10 | Q10 × Q02 | Igualdade por combinação e três medidas somente em produtos 6/9, estado 0, BRL |

Controles adicionais recomendados: unicidade das chaves de Q01/Q01B; integridade da granularidade dos agrupamentos; `QT_TRAN >= 0`; `VL_ABS >= ABS(VL_TOTAL)` por grupo comparável; `0 <= QT_CENARIO <= QT_ORIGINAL` e `0 <= VL_ABS_CENARIO <= VL_ABS_ORIGINAL`; datas observadas dentro da janela; domínios anômalos preservados; ausência de dados pessoais. Q07 tem outra população e não deve ser reconciliada por simples soma com Q03.

As consultas foram planejadas em sequência, sem snapshot comum. Diferenças podem resultar de atualização legítima entre execuções, multiplicidade de junções, ausência de registros, recortes distintos, SQL divergente, conversões ou falhas de exportação. Não atribuir automaticamente toda divergência à concorrência. Inspecionar os SQLs reais e, se necessário, solicitar reexecução dirigida, não repetir o estudo inteiro por padrão.

## 7. Roteiro analítico obrigatório

### Passo A — Dimensionar universo e indicadores

1. Fixar totais Q00 e validar Q02/Q03. Separar produto 6/9 e natureza C/D; manter naturezas atípicas identificadas.
2. Para cada indicador, apresentar frequência e valor absoluto de S, N, outros e nulo, no total e por produto/natureza. Mostrar denominadores.
3. Produzir as oito combinações teóricas CSM/CX/EVT e a distribuição observada; identificar DVS/OCTR/IR dentro de cada combinação. Preservar combinações fora do domínio. Distinguir ausência observada de impossibilidade.
4. Destacar as categorias/tipos que explicam maiores volumes afetados e casos economicamente relevantes mesmo se raros.

### Passo B — Medir o impacto dos filtros

Para cada cenário Q04, no total e por produto/natureza, calcular:

```text
QT_EXCLUIDA      = QT_ORIGINAL - QT_CENARIO
PCT_QT_EXCLUIDA  = 100 * QT_EXCLUIDA / QT_ORIGINAL
VL_ABS_EXCLUIDO  = VL_ABS_ORIGINAL - VL_ABS_CENARIO
PCT_VL_EXCLUIDO  = 100 * VL_ABS_EXCLUIDO / VL_ABS_ORIGINAL
```

Se denominador for zero, percentual não aplicável. Calcular percentuais sobre somas (ponderados), não a média dos percentuais de grupos. Informar quantidades e valores absolutos junto com os percentuais. Não somar exclusões isoladas: os conjuntos se sobrepõem. Para medir efeito incremental de adicionar um filtro ao Radar, reconstruir a interseção dos predicados usando Q03; o denominador incremental é o universo retido pelo Radar. Comparar RADAR versus CSM_D, perspectivas institucionais e base sem filtro. Isolar créditos CSM=N/outros retidos e débitos CSM=N/outros rejeitados.

### Passo C — Explicar as exclusões por operação

Relacionar Q03 a Q01 por categoria atual e por categoria original, com LEFT JOIN; associar grupos via Q01B. Validar que enriquecimento não multiplica nem perde linhas/medidas. Categoria atual diferente da original não prova quando ou por quem ocorreu mudança. Descrever códigos sem mapeamento como desconhecidos. Usar Q05 e Q06 como recortes explicativos, não como se fossem detalhes linha a linha de Q03. Se comparar agregados, usar somente dimensões comuns compatíveis e pré-agregar cada lado para evitar junção muitos-para-muitos.

| Caso a investigar | Pergunta que deve ser respondida com evidência |
|---|---|
| Compra à vista, compra parcelada, parcelas | CSM e CX selecionam representações diferentes? Em quais tipos, quantidades e valores? (Q03/Q05) |
| Pagamento de fatura e crédito no cartão | Quais representações seriam retidas ou rejeitadas? Pode haver duplicidade econômica? Não afirmar pareamento sem chaves. (Q03/Q05/Q06) |
| Estorno, contestação, devolução | Quais marcações e naturezas aparecem? Existe risco de excluir uma reversão? (Q03/Q05) |
| Juros, IOF, anuidade, tarifas | Quais filtros retêm/excluem esses custos? (Q03/Q05/Q06) |
| Pix/TED/transferências | Há padrões distintos por relação de documento e histórico? Quais casos não são identificáveis? (Q03/Q06) |
| Aplicação, resgate, empréstimo, amortização | Visibilidade de caixa e consumo coincide? Não classificar todo crédito como renda. (Q01/Q03/Q06) |
| Saque/divisão e lançamentos manuais | Retirar DVS=S causaria omissão? Qual a cobertura de derivados? (Q07/Q08) |
| Ocultos e IR | Que operações seriam perdidas? Indicador IR coincide com código? (Q03/Q04/Q11) |
| Eventos sem consumo/caixa | Qual é a distribuição de CSM=N/CX=N/EVT=S e das demais combinações? (Q02/Q03/Q10) |
| Instituições e estados | Os padrões persistem dentro de operações comparáveis ou decorrem do mix? (Q09/Q10) |

### Passo D — Avaliar divisão, ocultação e IR com cuidado especial

- Q08 relaciona derivados ao original por referência e, no desenho anterior, cliente, produto e natureza, dentro dos filtros e do período. Confirmar isso no SQL do ZIP. `SEM_DERIVADO_NO_ESCOPO` não significa inexistência global de derivados. Comparar cobertura por quantidade de originais e por valor registrado, sem chamar essa diferença de perda econômica definitiva. No desenho original, casos com um derivado são classificados antes do teste de igualdade de valores. A soma de valores por grupo pode esconder compensações; não afirmar igualdade individual fora dos cenários que a verificam. Não somar originais e derivados como operações independentes.
- Ocultação: avaliar OCTR=S e valores anômalos em categorias, natureza e cenários. Distinguir regra de apresentação e autorização de uso analítico. Não recomendar expor lançamentos ocultos.
- IR: cruzar indicador com código e categoria, usando Q11/Q01. Não presumir que todo código não nulo é dedutível ou que toda marcação S comprova direito fiscal. Documentar inconsistências sem atribuir erro de negócio antes de verificar a semântica do código.

### Passo E — Avaliar heterogeneidade e limites

Q09 deve comparar taxas dentro de tipos/categorias/produtos/naturezas equivalentes; uma taxa global por instituição pode refletir apenas o mix de operações. Q10 deve manter valores separados por moeda, e distinguir estados e produtos; não extrapolar o recorte efetivado BRL para todo o GFP. A ausência de determinado evento em 30 dias não prova que jamais ocorra. Se faltar evidência de regra de atribuição, propor investigação dirigida de código de escrita, sincronização ou mapeamento, se autorizada.

## 8. Como tomar a decisão sobre cada indicador

A decisão precisa ser específica à finalidade: contagem bruta da regra 7, consumo, caixa ou eventos. O escopo principal é **decidir filtros**, não implementar classificação financeira abrangente. Recomendações abaixo são hipóteses de trabalho, não resultados do estudo:

| Indicador | Hipótese a testar | Evidência decisiva esperada |
|---|---|---|
| CSM | O filtro atual para D pode ser útil para uma perspectiva de consumo, mas inadequado como única definição de movimento | Q03/Q04/Q05/Q06: operações excluídas, magnitudes e efeitos da assimetria C/D |
| CX | Pode ser mais adequado para uma perspectiva de caixa; não assumir que substitui CSM | Q02–Q06: diferenças de visibilidade e tipos afetados |
| EVT | Provavelmente específico de eventos, não filtro global | Q02–Q04/Q10: eventos exclusivos e operações sem EVT |
| DVS | Não excluir automaticamente o original sem evidência de tratamento dos derivados | Q07/Q08 e impacto Q04; distinguir elegibilidade da apresentação GFP |
| OCTR | Não converter ocultação em invalidação econômica; avaliar política de uso e apresentação | Q03/Q04/Q11 e orientação corporativa aplicável |
| IR | Não usar como filtro global salvo finalidade tributária demonstrada | Q11: relação indicador/código e distribuição de operações |

Para cada indicador, escolher uma disposição: **manter o filtro atual**, **não aplicar filtro**, **aplicar condicionalmente** (predicado exato e escopo), **propor substituição** (comparativo completo) ou **pendente de evidência**. Não estabelecer um percentual arbitrário de perda aceitável; materialidade deve considerar magnitude, natureza econômica, risco e finalidade. Caso a decisão dependa de um limiar de negócio, explicitar que requer aprovação do responsável pelo Radar.

A recomendação final pode ser manter a regra 7 como está, modificá-la de forma pontual ou manter uma base analítica sem filtros adicionais e aplicar perspectivas posteriormente. Nenhuma opção está predeterminada. Sempre apresentar efeito versus a regra atual, inclusive contrapartes potencialmente ausentes e limitações de medição. Não emitir SQL de produção sem validação posterior; pode fornecer predicado candidato para avaliação.

## 9. Entregáveis do desenvolvedor avaliador

Entregar três produtos, podendo ser consolidados em um relatório e tabelas auxiliares:

### 9.1 Parecer executivo e técnico

- Situação do pacote e qualidade dos dados; identificação da janela, consultas bem-sucedidas, totais Q00 e controles cruzados.
- Conclusão por indicador com argumentos a favor/contra seu uso como filtro, evidências e exceções. Explicitar impacto sobre a regra 7 e, se aplicável, o risco para etapas posteriores.
- Principais achados quantitativos, tabelas por produto/natureza, tipo/categoria e instituições quando pertinente. Citar Qxx, agrupamento, numerador, denominador, valores e SQL de origem. Indicar incertezas e lacunas.
- Diagnóstico de desempenho com tempos do manifesto, distinguindo duração observada de hipóteses de gargalos. Não confundir bom desempenho técnico com validade analítica.

### 9.2 Matriz de evidências e comportamento (CSV ou tabela)

Campos mínimos sugeridos:

```text
ID_ACHADO;INDICADOR;PRODUTO;NATUREZA;TIPO_TRAN;CATEGORIA_ATUAL;CATEGORIA_ORIGINAL;GRUPO;RECORTE;PREDICADO;QT_BASE;QT_RETIDA;QT_EXCLUIDA;PCT_QT_EXCLUIDA;VL_ABS_BASE;VL_ABS_RETIDO;VL_ABS_EXCLUIDO;PCT_VL_EXCLUIDO;CONSULTAS_FONTE;EVIDENCIA;NIVEL_EVIDENCIA;LIMITACAO;DECISAO_PROPOSTA
```

Usar uma linha por achado/recorte compatível; não forçar dimensões não presentes no agregado. Referenciar as consultas e chaves reais para que outra pessoa possa reproduzir os cálculos. Se métrica não for aplicável, registrar como tal, não zero.

### 9.3 Matriz final de decisão dos seis filtros

Preencher uma linha por indicador; adicionar sublinhas se a decisão variar por produto/natureza/finalidade.

| Indicador | Predicado atual / candidato | Decisão proposta | Escopo e condições | Impacto Q04/Q03 | Evidência e confiança | Riscos/lacunas |
|---|---|---|---|---|---|---|
| IN_VSLO_CSM | D e CSM=S (atual) | A preencher | A preencher | A preencher | A preencher | A preencher |
| IN_VSLO_CX | CX=S (candidato) | A preencher | A preencher | A preencher | A preencher | A preencher |
| IN_VSLO_EVT | EVT=S (candidato) | A preencher | A preencher | A preencher | A preencher | A preencher |
| IN_DVS_LCTO | DVS=N (candidato) | A preencher | A preencher | A preencher | A preencher | A preencher |
| IN_OCTR_TRAN | OCTR=N (candidato) | A preencher | A preencher | A preencher | A preencher | A preencher |
| IN_TRAN_IR | IR=S (candidato) | A preencher | A preencher | A preencher | A preencher | A preencher |

Concluir com: (a) recomendação para o predicado da regra 7, (b) efeito estimado sobre registros no universo agregado, (c) casos a preservar/investigar, (d) limitações e testes dirigidos necessários para futura implementação. Não converter hipótese em regra definitiva sem aceite.

## 10. Referências, rastreabilidade e estado do conhecimento

Fontes internas que fundamentaram este guia:

| Fonte | Referência e uso |
|---|---|
| `Estudo_Indicadores_GFP_Radar.md` | Seções 2–7, 10–13: desenho da investigação, semântica e controles; documentos anteriores incluem Q12, que foi removida na configuração final. |
| `Documentacao_GFP_Regra_7_QT_MOV_CICLO.md` | Seção 8: especificação da regra 7, contexto de ciclo e granularidade. |
| `tran.txt` | Predicados Java V7, especialmente linhas 74–79, 320–327, 569–575, 818–824, 969–977 e 1217–1222; são regras de leitura. |
| `GFP.json` e `db2gfp_estrutura_sysibm.json` | Fontes conceitual e física referenciadas nos documentos anteriores; consultar se houver dúvida sobre os atributos ou chaves. |
| `Consultas_Estudo_Indicadores_GFP.sql` | Versão anterior, utilizada para entender desenho dos agrupamentos e cenários. Não utilizar como SQL de execução definitivo. |
| `ESTUDO_RADAR(8).ipynb` | Última revisão de notebook disponibilizada nesta análise; parâmetros, modo de homologação/extração e download. |
| `estudo_indicadores_gfp(7).py` | Último módulo disponibilizado; constantes de consultas, `ResumoConsulta`, `verificar_resultados`, `publicar_pacote` e `executar_estudo`. |
| ZIP real da execução | Fonte primária dos resultados observados e do SQL efetivamente executado; deve acompanhar este guia. |

**Limitação conhecida:** os 13 SQLs definitivos após as correções de sintaxe não foram fornecidos separadamente para esta redação. A versão histórica de Q05 contém um placeholder posteriormente reportado como corrigido. A execução reduzida corporativa confirmou CTE sintética, data, Decimal, criação de ZIP e transferência relatada, mas não prova a execução bem-sucedida das consultas reais. Validar os SQLs arquivados no pacote recebido; não propagar erros ou placeholders de versões históricas. Nenhum resultado quantitativo real foi recebido para elaboração deste guia. Todos os critérios, cálculos e hipóteses aqui apresentados são um protocolo para avaliar os resultados, não conclusões empíricas.

**Critério final de sucesso:** o avaliador deve conseguir explicar, com números e rastreabilidade, o que cada um dos seis indicadores faz no universo observado, quais exclusões são úteis ou perigosas e qual predicado recomenda para o Radar — ou declarar de forma fundamentada que a evidência ainda é insuficiente. O trabalho não termina com a aprovação do ZIP: termina com uma decisão técnica defensável sobre os filtros, pronta para discussão e homologação de negócio.
