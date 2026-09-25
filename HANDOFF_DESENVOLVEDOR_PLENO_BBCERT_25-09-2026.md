# Handoff para o desenvolvedor pleno — incidente BBCert

**Data prevista da sessão:** 25/09/2026  
**Solicitante:** responsável funcional com pouca experiência em OpenShift/Kubernetes  
**Papel esperado do desenvolvedor pleno:** ler o contexto, interpretar as saídas e guiar a execução passo a passo  
**Ambiente autorizado:** somente Desenvolvimento (`des`)

## 1. Pedido ao desenvolvedor pleno

Preciso de acompanhamento técnico para executar um diagnóstico já estruturado. Hoje, 24/09/2026, não tenho acesso ao ambiente e não foi possível validar o estado atual. Amanhã o estado pode estar diferente das evidências históricas.

Antes de sugerir comandos ou alterações, por favor:

1. leia integralmente o guia autônomo;
2. leia o diagnóstico e as evidências já coletadas;
3. examine o dump bruto dos recursos;
4. aguarde a coleta ao vivo da sessão de 25/09/2026;
5. confirme seu entendimento separando fatos, hipóteses e informações ainda ausentes;
6. conduza um bloco por vez e explique o resultado em linguagem simples;
7. respeite todos os pontos de parada e o limite de uma reciclagem.

Não preciso que você memorize o ambiente corporativo BBCert. Se alguma operação pertencer ao operador, broker, registry ou PSC e não estiver visível no namespace, registre a limitação e ajude a preparar a escalada. Não tente compensar a falta de acesso com alterações especulativas.

## 2. Arquivos que devem ser lidos antes da execução

Leia nesta ordem:

1. [`GUIA_AUTONOMO_BBCERT_25-09-2026.md`](./GUIA_AUTONOMO_BBCERT_25-09-2026.md) — roteiro operacional que será seguido durante a sessão.
2. [`DIAGNOSTICO_E_EVIDENCIAS_DEPLOY_DESENV.md`](./DIAGNOSTICO_E_EVIDENCIAS_DEPLOY_DESENV.md) — diagnóstico consolidado, evidências e estado conhecido em 24/09/2026.
3. [`apiVersion networking.k8s.iov1.txt`](./apiVersion%20networking.k8s.iov1.txt) — dump bruto de Ingress, BBCert, Deployment, Service e Pod.
4. Pasta `evidencias-bbcert-2026-09-25` — será criada pelo guia no diretório em que o terminal for aberto. Ela conterá as saídas coletadas ao vivo.

O dump `.txt` é uma captura de console com linhas quebradas. Ele serve como evidência e não deve ser aplicado no cluster como YAML.

## 3. Resumo do problema para leitura rápida

A aplicação Python não era o bloqueio na última coleta. O pod atual estava `Running`, `Ready 1/1`, e o Deployment possuía uma réplica disponível.

A cadeia causal comprovada até 24/09/2026 era:

```text
PKI emitiu o certificado
        ↓
BBCert tentou exportá-lo para o OpenShift
        ↓
copy_to_openshift.yml falhou com ErrImagePull
        ↓
Secret TLS não foi criada
        ↓
Ingress foi rejeitado por TLS ausente
        ↓
status.loadBalancer permaneceu vazio
        ↓
Argo CD permaneceu com Health Progressing
```

O motivo técnico final do `ErrImagePull` ainda não foi identificado. Faltavam a imagem, a tag, o pod/job, o namespace real da automação e a mensagem completa do pull.

## 4. Identificação exata do ambiente

| Item | Valor |
|---|---|
| Ambiente | Desenvolvimento (`des`) |
| Cluster | `https://api.k8sdesbb211d.nuvem.bb.com.br:6443` |
| Namespace | `iaa-agent-mf-assist-financeir` |
| Aplicação Argo CD | `DES-BB2-D1-IAA-AGENT-MF-ASSIST-FINANCEIR` |
| BBCert | `agent-mf-assist-financeir-iaa-desenv-bb-com-br` |
| Secret TLS esperada | `iaa-agent-mf-assist-financeir-tls` |
| Ingress | `iaa-agent-mf-assist-financeir` |
| Service | `iaa-agent-mf-assist-financeir` |
| Deployment | `iaa-agent-mf-assist-financeir-regular` |
| Host | `agent-mf-assist-financeir.iaa.desenv.bb.com.br` |
| Custodiante configurado | `F6745399` |

## 5. Fatos já comprovados nas evidências anteriores

- O BBCert estava em `generation: 1` com matrícula `F6745399`.
- `instance.state` estava `succeeded`.
- O certificado de serial `4278` havia sido emitido, com validade informada até 24/09/2027.
- `secretControl.state` estava `failed`.
- A descrição registrava `copy_to_openshift.yml. Erro: ErrImagePull`.
- A Secret `iaa-agent-mf-assist-financeir-tls` não existia.
- O Ingress registrava `Invalid or missing TLS secret`.
- O `status.loadBalancer` problemático era o do Ingress.
- O Service é `ClusterIP`; seu `loadBalancer` vazio é esperado.
- A Secret `idh-mtls` existia e tinha função diferente: mTLS de saída da aplicação.
- Os eventos antigos de `BackOff` pertenciam a pods anteriores; o pod observado por último estava saudável.
- Não há evidência de que a matrícula tenha causado o `ErrImagePull`.
- Não há evidência de que criar ou copiar `atfregistry` resolva a automação APB.

Esses fatos precisam ser comparados com o estado ao vivo de 25/09/2026 antes de qualquer decisão.

## 6. Informações ainda desconhecidas

- O problema continua presente em 25/09/2026?
- O operador tentou reconciliar novamente?
- A Secret TLS foi criada espontaneamente?
- Qual imagem e tag sofreram `ErrImagePull`?
- O pod/job APB foi criado no namespace da aplicação ou em infraestrutura gerenciada?
- A mensagem completa foi `unauthorized`, imagem inexistente, timeout, DNS ou TLS?
- Existe incidente conhecido no registry ou na plataforma BBCert/PSC?
- A política atual do Argo CD é manual ou automática?
- O usuário possui `get` nominal no BBCert e permissão para excluir o card no Argo CD?

Não transformar qualquer item desta lista em afirmação sem evidência da sessão.

## 7. Como conduzir a sessão

### Fase A — leitura e alinhamento

O desenvolvedor pleno deve:

1. ler os três arquivos principais;
2. repetir o problema em cinco frases curtas;
3. dizer quais fatos aceita como comprovados;
4. listar o que precisa ser confirmado ao vivo;
5. declarar que nenhuma mutação será feita durante a coleta inicial.

### Fase B — execução acompanhada

Use o guia autônomo como única sequência operacional. Para cada bloco:

1. o desenvolvedor explica o objetivo do bloco;
2. o solicitante cola e executa o bloco;
3. ambos esperam a saída completa;
4. o desenvolvedor traduz o resultado em linguagem simples;
5. a saída é salva na pasta de evidências;
6. o resultado recebe uma cor: `VERDE`, `AMARELO` ou `VERMELHO`;
7. somente então o próximo bloco é escolhido.

Não despejar vários comandos novos no chat ou terminal. Não substituir o roteiro por tentativa e erro.

### Fase C — decisão antes de alteração

Se houver possibilidade de reciclagem, o desenvolvedor deve ler em voz alta as nove perguntas da seção 4 do guia e registrar `SIM`, `NÃO` ou `NÃO SEI` em cada uma.

- Qualquer `NÃO` ou `NÃO SEI`: não excluir.
- Nove respostas `SIM`: revisar mais uma vez o nome, namespace, ambiente e política de Sync.
- O clique em `Delete` conta como a única reciclagem, mesmo se falhar.

### Fase D — validação ou escalada

- Caminho verde: validar Secret, SAN, Ingress, Route, endpoint, HTTPS e os dois estados do Argo CD.
- Caminho amarelo: aguardar o tempo indicado e repetir somente a consulta.
- Caminho vermelho: parar mutações, revisar a pasta de evidências e preencher a minuta de chamado.

## 8. Forma esperada de orientação

Antes de cada comando, o desenvolvedor deve informar quatro coisas:

```text
Objetivo: o que vamos descobrir.
Risco: somente leitura ou alteração.
Saída esperada: o que deve aparecer.
Parada: em qual resultado não devemos continuar.
```

Exemplo:

```text
Objetivo: confirmar se a Secret TLS já foi criada.
Risco: somente leitura.
Saída esperada: uma linha com nome, tipo e idade da Secret; ou NotFound.
Parada: se aparecer Forbidden ou outro erro não previsto, salvaremos a saída e não excluiremos nada.
```

O desenvolvedor não deve pedir ao solicitante que escolha sozinho entre opções técnicas sem antes explicar a consequência de cada uma.

## 9. Limites que o desenvolvedor deve proteger

- Ambiente exclusivamente `des`.
- Conferir o servidor do cluster antes de qualquer ação.
- Nenhuma elevação ou contorno de RBAC.
- Nenhuma remoção forçada de finalizer.
- Nenhum `oc delete --force`.
- Nenhuma cópia ou criação especulativa de Secrets.
- Nenhuma leitura ou exibição de `tls.key`.
- Nenhuma manipulação de `.p12`.
- Nenhuma mudança em operador, registry, nó ou configuração global.
- Nenhum `Force`, `Replace` ou `Prune` no Argo CD.
- No máximo uma reciclagem do BBCert.
- Nenhuma alteração em `values.yaml` para adivinhar a imagem interna do APB.

## 10. Mensagem pronta para enviar ao desenvolvedor pleno

```text
Preciso que você me acompanhe como guia técnico em um problema de BBCert no
OpenShift de desenvolvimento. Sou leigo em Kubernetes e amanhã não terei acesso
ao sênior nem ao desenvolvedor que fizeram a análise inicial.

Antes de sugerir qualquer comando ou alteração, peço que leia estes arquivos na
ordem:

1. GUIA_AUTONOMO_BBCERT_25-09-2026.md
2. DIAGNOSTICO_E_EVIDENCIAS_DEPLOY_DESENV.md
3. apiVersion networking.k8s.iov1.txt
4. a pasta evidencias-bbcert-2026-09-25, depois que a coleta começar

O diagnóstico anterior indica: certificado emitido pela PKI, falha ErrImagePull
na ação copy_to_openshift.yml, Secret TLS ausente, Ingress bloqueado e Argo CD
Progressing. A causa específica do pull ainda é desconhecida e o estado ao vivo
precisa ser confirmado.

Quero executar o guia um bloco por vez. Antes de cada bloco, explique:
- o objetivo;
- se é somente leitura ou alteração;
- a saída esperada;
- em qual resultado devemos parar.

Não execute nem sugira Delete antes de preencher comigo as nove condições do
gate. Há limite de uma única reciclagem. Não devemos forçar finalizer, copiar
Secrets, usar Force/Replace/Prune, consultar tls.key ou alterar infraestrutura.

Se a causa estiver na plataforma e não for observável pelo nosso RBAC, preciso
que você me ajude a organizar as evidências e finalizar a minuta de chamado.
```

## 11. Resultado que deve ser produzido ao final da sessão

Mesmo que o incidente não seja resolvido, a sessão deve terminar com um destes resultados claros:

```text
[APROVADO]
Secret criada, Ingress publicado, HTTPS validado e Argo CD Healthy/Synced.

[AGUARDANDO]
Operação em processamento sem falha definitiva; horário e próxima consulta registrados.

[BLOQUEADO — PLATAFORMA]
Falha fora do escopo do namespace/RBAC, evidências anexadas e chamado preparado.

[BLOQUEADO — PERMISSÃO]
Ação necessária não permitida ao usuário; erro literal e recurso afetado registrados.

[FALHOU APÓS RECICLAGEM ÚNICA]
Nova tentativa executada uma vez, erro preservado e novas exclusões proibidas.
```

O sucesso da sessão não depende apenas de corrigir o incidente. Sair com evidências completas, sem causar nova emissão ou alterar o cluster indevidamente, também é um resultado correto e auditável.

