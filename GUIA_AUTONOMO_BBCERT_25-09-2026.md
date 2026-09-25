# Guia autônomo para diagnóstico e recuperação do BBCert

**Execução prevista:** 25/09/2026  
**Ambiente permitido:** Desenvolvimento (`des`)  
**Namespace:** `iaa-agent-mf-assist-financeir`  
**Aplicação Argo CD:** `DES-BB2-D1-IAA-AGENT-MF-ASSIST-FINANCEIR`

> **Se você estiver acompanhado por um desenvolvedor pleno:** entregue primeiro o arquivo [`HANDOFF_DESENVOLVEDOR_PLENO_BBCERT_25-09-2026.md`](./HANDOFF_DESENVOLVEDOR_PLENO_BBCERT_25-09-2026.md). Peça que ele leia o pacote e aguarde a coleta ao vivo antes de sugerir ações.

## Leia isto antes de começar

Este guia foi preparado em **24/09/2026**, quando você **não tinha acesso ao ambiente**. Portanto, nenhum estado descrito aqui representa uma verificação ao vivo de 25/09/2026. O problema pode ter mudado ou até ter sido resolvido automaticamente até amanhã.

O roteiro foi escrito para você executar sozinho, sem depender de contato em tempo real com o desenvolvedor ou com o sênior. Você não precisa entender Kubernetes em profundidade. Execute **um bloco por vez**, leia a decisão logo abaixo e somente depois avance.

> **Regra principal:** se a saída for diferente das opções explicadas neste guia, não improvise. Pare, salve a saída e use a minuta de chamado da seção 9.

### O problema em linguagem simples

A aplicação está funcionando dentro do cluster. O que falhou foi a publicação HTTPS:

```text
certificado emitido
        ↓
falha ao copiar o certificado para o OpenShift (ErrImagePull)
        ↓
Secret TLS não criada
        ↓
Ingress não publicado
        ↓
Argo CD permanece Progressing
```

### O que você nunca deve fazer

- Não executar nada em homologação ou produção.
- Não remover `finalizer` manualmente.
- Não usar `oc delete --force`.
- Não criar ou copiar a Secret `atfregistry`.
- Não copiar Secrets de outro namespace.
- Não consultar, decodificar, imprimir ou salvar `tls.key`.
- Não baixar ou manipular o arquivo `.p12` para tentar corrigir o Ingress.
- Não alterar operadores, registries, ServiceAccounts ou configurações globais.
- Não usar `Sync` com as opções `Force`, `Replace` ou `Prune` para esta recuperação.
- Não excluir o BBCert mais de uma vez.

## Cartão rápido de decisão

Use estas cores durante todo o roteiro:

| Situação | Decisão |
|---|---|
| **VERDE** — Secret existe, Ingress possui IP/hostname e HTTPS responde | Vá para a validação final e encerre |
| **AMARELO** — recurso está processando, sem erro definitivo | Aguarde e consulte novamente; não exclua nada |
| **VERMELHO** — `ErrImagePull`, `Forbidden`, finalizer travado ou resultado desconhecido | Pare a mutação, preserve a saída e prepare o chamado |

## 1. Preparar o terminal e confirmar o ambiente

Abra o Pengwin/WSL. Copie e execute este primeiro bloco:

```bash
NS="iaa-agent-mf-assist-financeir"
BBCERT="agent-mf-assist-financeir-iaa-desenv-bb-com-br"
TLS_SECRET="iaa-agent-mf-assist-financeir-tls"
INGRESS="iaa-agent-mf-assist-financeir"
SERVICE="iaa-agent-mf-assist-financeir"
DEPLOYMENT="iaa-agent-mf-assist-financeir-regular"
HOST="agent-mf-assist-financeir.iaa.desenv.bb.com.br"
EXPECTED_SERVER="https://api.k8sdesbb211d.nuvem.bb.com.br:6443"
EVID="$PWD/evidencias-bbcert-2026-09-25"

mkdir -p "$EVID"
printf 'Namespace: %s\nBBCert: %s\nHost: %s\nEvidencias: %s\n' \
  "$NS" "$BBCERT" "$HOST" "$EVID"
```

Você deve enxergar exatamente o namespace, o nome do BBCert e o host indicados no cabeçalho. Em seguida, confirme que o comando `oc` existe e que a sessão aponta para desenvolvimento:

```bash
command -v oc
oc whoami 2>&1 | tee "$EVID/00-whoami.txt"
oc whoami --show-server 2>&1 | tee "$EVID/01-servidor.txt"

CURRENT_SERVER=$(oc whoami --show-server 2>/dev/null)
if [ "$CURRENT_SERVER" = "$EXPECTED_SERVER" ]; then
  echo "OK: cluster de desenvolvimento confirmado"
else
  echo "PARE: servidor atual diferente do cluster esperado"
  printf 'Esperado: %s\nAtual: %s\n' "$EXPECTED_SERVER" "$CURRENT_SERVER"
fi
```

### Como decidir

- Se aparecer `oc: command not found`: **PARE**. O cliente OpenShift não está instalado nesse terminal.
- Se aparecer `Unauthorized` ou pedido de login: faça login pelo procedimento oficial da Console OpenShift (`Copy login command`) e repita os três comandos.
- Se o servidor não for exatamente `https://api.k8sdesbb211d.nuvem.bb.com.br:6443`: **PARE**. Você está no cluster errado.
- Se o usuário e o servidor estiverem corretos: prossiga.

Todos os comandos restantes informam `-n "$NS"`; você não precisa mudar o projeto ativo do terminal.

## 2. Cenário 1 — verificar se o problema já se resolveu

### Passo 2.1 — consultar o BBCert pelo nome

Execute mesmo que o primeiro comando responda `no`:

```bash
oc auth can-i get bbcerts.certificado.psc.bb.com.br -n "$NS" \
  2>&1 | tee "$EVID/02-permissao-bbcert.txt"

oc get bbcert "$BBCERT" -n "$NS" -o yaml \
  2>&1 | tee "$EVID/03-bbcert-atual.yaml"

oc describe bbcert "$BBCERT" -n "$NS" \
  2>&1 | tee "$EVID/04-bbcert-describe.txt"
```

O `can-i` é apenas informativo. A prova real é o `oc get` com o nome completo.

### Como interpretar

- Se o YAML aparecer: continue.
- Se aparecer `Forbidden`: registre **VERMELHO — BBCert sem acesso nominal**, mas continue apenas com as verificações de Secret e Ingress abaixo.
- Se aparecer `NotFound`: não crie o BBCert manualmente. Verifique no Argo CD se o recurso aparece como `Missing`. Siga a orientação específica da seção 6.
- Se aparecer outro erro: **PARE** e guarde o arquivo `03-bbcert-atual.yaml`.

### Passo 2.2 — verificar Secret, Ingress e aplicação

```bash
oc get secret "$TLS_SECRET" -n "$NS" \
  2>&1 | tee "$EVID/05-secret-tls.txt"

oc get ingress "$INGRESS" -n "$NS" -o yaml \
  2>&1 | tee "$EVID/06-ingress.yaml"

oc get deployment "$DEPLOYMENT" -n "$NS" \
  2>&1 | tee "$EVID/07-deployment.txt"

oc get pods -n "$NS" -l app=iaa-agent-mf-assist-financeir -o wide \
  2>&1 | tee "$EVID/08-pods-aplicacao.txt"
```

Agora obtenha somente o endereço publicado pelo Ingress:

```bash
oc get ingress "$INGRESS" -n "$NS" \
  -o jsonpath='{range .status.loadBalancer.ingress[*]}IP={.ip}{" "}HOSTNAME={.hostname}{"\n"}{end}' \
  2>&1 | tee "$EVID/09-endereco-ingress.txt"

echo
```

### Decisão do Cenário 1

Escolha apenas uma linha:

| Resultado observado | Próxima ação |
|---|---|
| A Secret foi encontrada e o comando do Ingress mostrou `IP=` ou `HOSTNAME=` preenchido | Marque **VERDE** e vá para a seção 7 |
| A Secret existe, mas o endereço do Ingress está vazio | Vá para a seção 7.3; se continuar vazio, abra o chamado da seção 9. Não recicle o BBCert |
| A Secret não existe e o BBCert contém `secretControl.state: failed` com `ErrImagePull` | Vá para a seção 3 |
| O BBCert mostra estado em processamento, sem `failed` | Marque **AMARELO**, aguarde dez minutos e repita a seção 2 |
| O BBCert retornou `Forbidden` ou outro erro, e a Secret não existe | Vá para a seção 9; não exclua nada |

> `NotFound` ao consultar a Secret é esperado enquanto o problema existir. Esse resultado, sozinho, não significa que você executou algo errado.

## 3. Cenário 2 — procurar a causa do ErrImagePull

Estes comandos são somente leitura:

```bash
oc get pods,jobs -n "$NS" -o wide \
  2>&1 | tee "$EVID/10-pods-jobs.txt"

oc get pods -n "$NS" \
  -o custom-columns='NAME:.metadata.name,PHASE:.status.phase,WAITING:.status.containerStatuses[*].state.waiting.reason,IMAGE:.spec.containers[*].image' \
  2>&1 | tee "$EVID/11-pods-imagens.txt"

oc get events -n "$NS" --sort-by='.lastTimestamp' \
  2>&1 | tee "$EVID/12-eventos-completos.txt"

grep -i -E 'bbcert|apb|copy_to_openshift|errimagepull|imagepull|failed|unauthorized|denied|manifest|timeout|tls' \
  "$EVID/12-eventos-completos.txt" \
  | tee "$EVID/13-eventos-filtrados.txt"
```

### Se aparecer um pod claramente relacionado ao APB/BBCert

Copie o nome exato do pod da primeira coluna. Substitua `COLE_AQUI_O_NOME` antes de executar:

```bash
APB_POD="COLE_AQUI_O_NOME"
```

Confira o texto da variável. **Não prossiga se ainda aparecer `COLE_AQUI_O_NOME`:**

```bash
echo "$APB_POD"
```

Depois execute:

```bash
oc describe pod "$APB_POD" -n "$NS" \
  2>&1 | tee "$EVID/14-apb-pod-describe.txt"

oc logs "$APB_POD" -n "$NS" --all-containers --tail=200 \
  2>&1 | tee "$EVID/15-apb-pod-logs.txt"
```

Se houver Job, mas nenhum pod correspondente, apenas preserve o nome e a saída. Não tente recriar o Job.

### Dicionário simples dos erros

| Texto encontrado | Significado provável | Sua ação |
|---|---|---|
| `unauthorized`, `denied` | A automação não conseguiu autenticar no registry | **VERMELHO:** chamado para a plataforma |
| `manifest unknown`, `not found` | A imagem ou tag usada pela automação não existe | **VERMELHO:** chamado para a plataforma |
| `timeout`, `connection refused`, DNS | Registry ou rede indisponível | **VERMELHO:** verifique incidente oficial; não altere o chart |
| `x509`, `tls handshake` durante o pull | Problema de confiança TLS entre infraestrutura e registry | **VERMELHO:** chamado para a plataforma |
| Nenhuma carga APB encontrada | Ela pode ter sido removida ou executada fora do namespace | Registre como não observável; isso não prova que esteja saudável |

O `values.yaml` conhecido não expõe a imagem interna usada por `copy_to_openshift.yml`. Portanto, não altere o chart da aplicação para tentar corrigir a imagem do APB.

## 4. Decidir entre reciclar uma vez ou abrir chamado

A reciclagem é uma tentativa documentada para erros de provisionamento, mas ela pode emitir outro certificado e repetir exatamente o mesmo erro. Ela só é permitida se **todas** as respostas abaixo forem `SIM`.

Preencha amanhã:

| # | Pergunta | SIM/NÃO |
|---|---|---|
| 1 | Salvei o YAML atual do BBCert no arquivo `03-bbcert-atual.yaml`? | |
| 2 | No Argo CD, o manifesto desejado contém `F6745399`, `ambientePKI: des` e `secretNameToExport: iaa-agent-mf-assist-financeir-tls`? | |
| 3 | A Secret TLS continua ausente? | |
| 4 | Não existe pod/job APB em execução neste momento? | |
| 5 | Não existe incidente conhecido do registry ou da plataforma BBCert/PSC? | |
| 6 | Identifiquei no Argo CD se a política de Sync é `Manual` ou `Automated`? | |
| 7 | Registrei `instanceId`, `lastOperationId`, serial e UID atuais? | |
| 8 | Ainda não cliquei em Delete durante esta intervenção? | |
| 9 | Tenho evidência de que a falha foi transitória ou de que sua causa já foi corrigida? | |

### Regra de decisão

- Se **qualquer resposta** for `NÃO` ou `NÃO SEI`: não recicle. Vá para a seção 9.
- Se as nove respostas forem `SIM`: você pode seguir para a reciclagem única da seção 5.
- Ausência de eventos novos não conta, sozinha, como prova de que o registry foi corrigido.

## 5. Reciclagem única — etapa com alteração

> Ao clicar em Delete, sua única reciclagem será considerada utilizada, mesmo que a exclusão falhe. Leia toda esta seção antes de clicar.

### Passo 5.1 — registrar o UID antigo

```bash
OLD_UID=$(oc get bbcert "$BBCERT" -n "$NS" -o jsonpath='{.metadata.uid}')
printf 'UID antigo: %s\n' "$OLD_UID" | tee "$EVID/16-uid-antigo.txt"
```

Se `OLD_UID` ficar vazio, **PARE**.

### Passo 5.2 — conferir a política de sincronização

No Argo CD, abra a aplicação `DES-BB2-D1-IAA-AGENT-MF-ASSIST-FINANCEIR` e anote se a política é:

- `Manual`; ou
- `Automated`/auto-sync.

### Passo 5.3 — excluir somente o BBCert

No diagrama de recursos do Argo CD:

1. Localize o recurso de **Kind `BBCert`**.
2. Confirme o nome `agent-mf-assist-financeir-iaa-desenv-bb-com-br`.
3. Confirme o namespace `iaa-agent-mf-assist-financeir`.
4. Abra o menu do card e escolha `Delete`.
5. Não marque `Force`, não altere propagation policy e não escolha outros recursos.
6. Confirme uma única vez.

Se o botão estiver ausente ou a interface informar falta de permissão, pare e use a seção 9. Não tente excluir pela CLI como alternativa.

### Passo 5.4 — acompanhar sem forçar o finalizer

Execute o comando abaixo novamente a cada 30–60 segundos:

```bash
oc get bbcert "$BBCERT" -n "$NS" \
  -o custom-columns='NAME:.metadata.name,UID:.metadata.uid,CREATED:.metadata.creationTimestamp,DELETING:.metadata.deletionTimestamp'
```

Interprete assim:

- Mesmo UID e `DELETING` preenchido: a exclusão ainda está em andamento.
- `NotFound`: o objeto antigo foi excluído.
- UID diferente do `OLD_UID`: o Argo CD já recriou o objeto; não clique em Sync novamente.
- Mesmo UID em exclusão por mais de dez minutos: **PARE**. Finalizer retido; não force.

### Passo 5.5 — recriar conforme a política do Argo CD

#### Se a política for `Automated`

O Argo CD deve recriar o BBCert sozinho. Não clique em Sync se um novo UID já apareceu. Se continuar `NotFound` por mais de dois minutos, abra a aplicação e examine a mensagem de Sync. Depois, pare e use a seção 9; não force a sincronização.

#### Se a política for `Manual`

Somente depois de obter `NotFound`, abra a aplicação no Argo CD:

1. Clique em `Sync`.
2. Selecione somente o BBCert, se a interface permitir seleção de recursos.
3. Não use `Prune`, `Force` ou `Replace`.
4. Confira a relação de recursos que serão alterados.
5. Se houver qualquer mudança além da recriação do BBCert, cancele e use a seção 9.
6. Confirme uma única sincronização.

### Passo 5.6 — acompanhar a única tentativa

Execute a cada dois minutos, durante até quinze minutos:

```bash
oc get bbcert "$BBCERT" -n "$NS" \
  -o jsonpath='UID={.metadata.uid}{"\n"}INSTANCE={.status.instance.state}{"\n"}SECRET={.status.secretControl.state}{"\n"}DESCRICAO={.status.secretControl.description}{"\n"}'

oc get secret "$TLS_SECRET" -n "$NS"

oc get ingress "$INGRESS" -n "$NS" \
  -o jsonpath='{range .status.loadBalancer.ingress[*]}IP={.ip}{" "}HOSTNAME={.hostname}{"\n"}{end}'

echo
```

Decida:

- Secret criada e Ingress preenchido: **VERDE**, vá para a seção 7.
- Estado ainda processando, sem falha: **AMARELO**, continue observando até quinze minutos.
- Novo `ErrImagePull`: **VERMELHO**, pare imediatamente e vá para a seção 9.
- Quinze minutos sem conclusão: pare as tentativas, preserve o estado e vá para a seção 9. Não exclua novamente.

## 6. Caso especial — BBCert aparece como NotFound antes de qualquer Delete

Se o BBCert já estiver ausente no início do roteiro:

1. Confirme que você não clicou em Delete nesta intervenção.
2. Abra o Argo CD e localize o BBCert como `Missing`.
3. Abra o manifesto **Desired** e confira:
   - matrícula `F6745399`;
   - `ambientePKI: des`;
   - `secretNameToExport: iaa-agent-mf-assist-financeir-tls`;
   - hostname `agent-mf-assist-financeir.iaa.desenv.bb.com.br`.
4. Se algum valor divergir: não sincronize; abra chamado ou corrija o Git pelo fluxo normal.
5. Se todos os valores estiverem corretos e a política for manual, faça um Sync somente do BBCert, sem `Force`, `Replace` ou `Prune`. Se a tela propuser alterações em outros recursos, cancele.
6. Se a política for automática, aguarde dois minutos e verifique a mensagem apresentada pelo Argo CD antes de qualquer ação.

Essa criação conta como a única tentativa de recuperação do dia. Depois dela, não delete o recurso.

## 7. Validação final — caminho VERDE

### Passo 7.1 — confirmar a Secret sem revelar conteúdo

Este comando mostra apenas o tipo e os nomes das chaves, nunca seus valores:

```bash
oc get secret "$TLS_SECRET" -n "$NS" \
  -o go-template='TIPO={{.type}}{{"\n"}}CHAVES={{range $k,$v := .data}}{{$k}} {{end}}{{"\n"}}' \
  2>&1 | tee "$EVID/17-secret-metadados.txt"
```

Esperado:

```text
TIPO=kubernetes.io/tls
CHAVES=... tls.crt tls.key ...
```

Não execute nenhum comando usando `.data.tls\.key`.

### Passo 7.2 — examinar somente o certificado público

```bash
oc get secret "$TLS_SECRET" -n "$NS" -o jsonpath='{.data.tls\.crt}' \
  | base64 -d \
  | openssl x509 -noout -subject -issuer -dates \
      -ext subjectAltName -fingerprint -sha256 \
  | tee "$EVID/18-certificado-publico.txt"
```

Confira:

- `notAfter` está no futuro;
- o emissor é a autoridade corporativa esperada;
- a lista `Subject Alternative Name` contém o host exato `agent-mf-assist-financeir.iaa.desenv.bb.com.br`.

Se o SAN não contiver o host exato, não considere aprovado, mesmo que o Subject pareça correto.

### Passo 7.3 — validar Ingress, Route e backend

```bash
oc get ingress "$INGRESS" -n "$NS" -o yaml \
  2>&1 | tee "$EVID/19-ingress-final.yaml"

oc get route -n "$NS" -o wide \
  2>&1 | tee "$EVID/20-routes.txt"

oc get endpoints "$SERVICE" -n "$NS" \
  2>&1 | tee "$EVID/21-endpoints.txt"

oc get events -n "$NS" --sort-by='.lastTimestamp' \
  2>&1 | tee "$EVID/22-eventos-finais.txt"
```

Esperado:

- Ingress com IP ou hostname em `status.loadBalancer`;
- Route referente ao host da aplicação;
- pelo menos um endpoint pronto na porta `8080`;
- nenhum evento novo `IncompleteIngressToRouteRules`.

O IP antigo do pod não é critério: IPs de pods podem mudar normalmente.

### Passo 7.4 — testar HTTPS sem esconder erro TLS

```bash
curl --verbose --fail --show-error \
  "https://$HOST/health/live" \
  2>&1 | tee "$EVID/23-curl-https.txt"
```

Interpretação:

- HTTP `200`: teste aprovado.
- `Could not resolve host`: DNS ainda não está pronto.
- Erro de hostname/certificado: certificado ou host incorreto.
- `unable to get local issuer certificate`: o WSL pode não possuir a CA corporativa. Não use `-k` para aprovar. Preserve a saída e valide também pelo navegador corporativo ou pelo procedimento oficial de CA.
- HTTP `404`/`503`: TLS e rota podem existir, mas o caminho ou backend ainda tem problema; preserve a saída.

### Passo 7.5 — conferir o Argo CD

Na aplicação, confirme separadamente:

- `Health Status: Healthy`;
- `Sync Status: Synced`.

Se estiver `Healthy` e `OutOfSync`, o HTTPS pode estar funcionando, mas o Git e o cluster ainda divergem. Não use Force para corrigir.

## 8. Encerramento bem-sucedido

Você pode declarar o problema resolvido apenas quando todos forem verdadeiros:

- [ ] BBCert sem `secretControl.state: failed`.
- [ ] Secret TLS criada como `kubernetes.io/tls`.
- [ ] SAN contém o hostname exato.
- [ ] Ingress possui IP ou hostname.
- [ ] Route e endpoint existem.
- [ ] HTTPS responde, preferencialmente com HTTP 200.
- [ ] Argo CD está `Healthy` e `Synced`.
- [ ] Nenhuma chave privada foi exibida ou salva.

Registre no relatório:

```text
[APROVADO]
Data/hora:
UID atual do BBCert:
Estado instance:
Estado secretControl:
Secret TLS:
Ingress IP/hostname:
HTTPS:
Argo Health:
Argo Sync:
Reciclagem utilizada: SIM/NÃO
```

## 9. Cenário 3 — parar com segurança e abrir chamado

Parar e escalar também é uma execução correta. Faça isso quando houver `Forbidden`, `ErrImagePull` persistente, causa desconhecida, finalizer por mais de dez minutos, ausência de acesso à carga APB ou qualquer resultado não previsto.

Anexe os arquivos da pasta indicada por:

```bash
echo "$EVID"
```

Antes de anexar, confira que nenhum arquivo contém senha, `.p12` ou chave privada. Os comandos deste guia não leem `tls.key`.

### Minuta pronta do chamado

```text
Assunto: BBCert em desenv falha ao exportar Secret TLS — ErrImagePull

Solicito análise da sustentação PSC/BBCert/PKI para falha na exportação de
certificado já emitido para o OpenShift.

Ambiente: desenvolvimento (des)
Cluster: https://api.k8sdesbb211d.nuvem.bb.com.br:6443
Namespace: iaa-agent-mf-assist-financeir
Recurso: bbcert/agent-mf-assist-financeir-iaa-desenv-bb-com-br
Aplicação Argo CD: DES-BB2-D1-IAA-AGENT-MF-ASSIST-FINANCEIR

Emissão PKI observada:
- instanceId: 5e9d170a-ea00-4ced-8b6c-b06a67e329d1
- lastOperationId: 0d73b0d4-3b7d-44d5-b895-4af8d64ca301
- serial: 4278
- UID original: 9e5b4864-59fa-44fb-b489-f0224538d4a9
- validade informada: 24/09/2027

Falha registrada:
Oferta pki-certificado-interno-v2, ação copy_to_openshift.yml,
secretControl.state=failed, erro ErrImagePull.

Impacto:
A Secret iaa-agent-mf-assist-financeir-tls não foi criada. O Ingress registra
Invalid or missing TLS secret, permanece sem status.loadBalancer e o Argo CD
permanece Progressing.

Solicito:
1. identificar namespace, pod/job, imagem, tag e ServiceAccount usados pela operação;
2. informar a mensagem completa do pull (auth, tag inexistente, rede ou TLS);
3. corrigir a causa na automação/registry;
4. avaliar reexecução apenas da exportação para OpenShift, evitando nova emissão
   de certificado se tecnicamente possível.

Reciclagem executada nesta intervenção: SIM/NÃO
Resultado da reciclagem, se realizada:
Arquivos de evidência anexados:
```

## 10. Checklist curto para imprimir ou manter ao lado

```text
[ ] Estou no cluster k8sdesbb211d de desenvolvimento.
[ ] Defini as variáveis e criei a pasta de evidências.
[ ] Consultei BBCert, Secret e Ingress sem alterar nada.
[ ] Classifiquei o resultado como VERDE, AMARELO ou VERMELHO.
[ ] Se houve ErrImagePull, procurei pod/job e eventos.
[ ] Não alterei values.yaml para tentar corrigir imagem interna do APB.
[ ] Preenchi as nove perguntas antes de considerar Delete.
[ ] Se alguma resposta foi NÃO/NÃO SEI, não deletei.
[ ] Se deletei, fiz isso uma única vez e somente no card BBCert correto.
[ ] Não forcei finalizer, Sync, Replace ou Prune.
[ ] Não consultei tls.key nem manipulei .p12.
[ ] Validei Secret, SAN, Ingress, Route, endpoint, HTTPS e Argo CD.
[ ] Em caso de bloqueio, preservei as evidências e abri o chamado.
```
