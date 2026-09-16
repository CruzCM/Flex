# Educador Financeiro (`mf-edu-fin`) — Passo a Passo Operacional

> **IMPORTANTE:** Este guia foi construído para ser seguido **na ordem**, passo a passo. Cada vez que você precisar falar com alguém, o guia diz **com quem**, **o que pedir** (com texto modelo pronto), **por que** e **como usar** o que receber.

**Projeto:** Agente de IA Educador Financeiro (`mf-edu-fin`)
**Sigla informada:** `IAA`
**Ponto de partida:** Aprovação já obtida
**Objetivo:** Primeiro deploy funcionando em HML com teste de `/chat` respondendo

Base: documentos e arquivos disponíveis neste workspace, consultados em 15/09/2026. Os caminhos abaixo foram encontrados nesse material; não foram conferidos em uma sessão autenticada dos portais. Um registro antigo de sucesso ou de erro não comprova a situação atual do ambiente.

---

## Passo 1 — Confirmar que o provisionamento terminou

### O que fazer

1. Abra [TechBB](https://tech.bb.com.br/) no navegador corporativo.
2. Vá em **Meus Microsserviços** e pesquise a instância `mf-edu-fin`.
3. Abra a página da instância/solicitação aprovada.
4. Leia o resultado da execução/provisionamento.
5. Localize e anote:

| Informação | O que registrar |
|---|---|
| Link da instância/solicitação | ______________________ |
| Nome completo do componente entregue | ______________________ |
| Link do repositório de código | ______________________ |
| Link do repositório de deploy | ______________________ |
| Link do ArgoCD HML | ______________________ |
| Namespace HML no OpenShift | ______________________ |
| Console OpenShift HML | ______________________ |
| DES existe? (sim/não) | ______________________ |
| Status (concluído/em andamento/erro) | ______________________ |

### Se o provisionamento não terminou ou não aparece

**🗣 COM QUEM FALAR:** Equipe de suporte da oferta de Agente de IA no TechBB.

**📋 O QUE PEDIR (texto modelo):**

> Olá. Minha solicitação do agente de IA **Educador Financeiro** (`mf-edu-fin`), sigla `IAA`, foi aprovada, mas o provisionamento não apresenta resultado / apresenta erro.
>
> - Identificação da solicitação: [cole o número/link]
> - Nome do componente: `mf-edu-fin`
> - Etapa com problema: [descreva o que a tela mostra]
> - Mensagem de erro: [copie textualmente]
>
> Preciso que o provisionamento seja concluído para acessar os repositórios e iniciar o desenvolvimento.

**❓ POR QUE ESTOU PEDINDO:** Sem o provisionamento concluído, os repositórios, o namespace no cluster e as configurações não existem. Nada mais pode ser feito.

**🔧 COMO VOU USAR:** O resultado me dará os links de repositórios, ArgoCD e namespace que são a base de todo o restante.

---

## Passo 2 — Verificar se o código já está no GitHub

### O que fazer

1. Olhe os links entregues no Passo 1.
2. Se o repositório de código já for `github.com/bbvinet/...`, **pule para o Passo 3**.
3. Se for `fontes.intranet.bb.com.br/...` (GitLab), precisa migrar.

### Se precisar migrar

1. Abra a [Oferta AIC no TechBB](https://tech.bb.com.br/p/aic/ofertas).
2. Clique em **Migrar Repositório**.
3. Preencha os dados organizacionais da sua equipe.
4. No campo **Nome do Componente**, coloque o nome exato do repositório no GitLab (o trecho final da URL, sem `.git`).
5. Confirme e acompanhe.

**Se der erro na migração:**

**🗣 COM QUEM FALAR:** Suporte da Oferta AIC (o canal é apresentado na própria tela da oferta).

**📋 O QUE PEDIR (texto modelo):**

> Solicitação de migração do repositório do Educador Financeiro (`mf-edu-fin`) falhou.
>
> - Componente: [nome completo entregue]
> - Identificação da solicitação de migração: [número/link]
> - Erro apresentado: [copie textualmente]
>
> Preciso do repositório no GitHub para iniciar o desenvolvimento e o pipeline de CI/CD.

---

## Passo 3 — Garantir seu acesso ao GitHub

### O que fazer

1. Entre no GitHub com sua identidade corporativa (SSO).
2. Abra o repositório de **código** (link do Passo 1).
3. Confirme se consegue ver a aba **Code** com os arquivos.
4. Abra separadamente o repositório de **deploy**.
5. Confirme se consegue ver suas branches (`cloud/homologacao`, etc.).

### Se o acesso for negado

**🗣 COM QUEM FALAR:** Seu **gestor técnico** ou **administrador do repositório**.

**📋 O QUE PEDIR (texto modelo):**

> Preciso de acesso aos repositórios do Educador Financeiro (`mf-edu-fin`) no GitHub.
>
> - Repositório de código: [link]
> - Repositório de deploy: [link]
> - Minha identificação: [sua matrícula/chave]
> - Nível de permissão necessário: **write** (preciso fazer push de código e alterações de deploy)
> - Equipe/time: [informe o nome cadastrado no GENTI/BusinessMap, se souber]
>
> A solicitação do agente foi aprovada e o provisionamento concluído. Preciso ser incluído no time do GitHub para desenvolver e implantar o agente.

**❓ POR QUE ESTOU PEDINDO:** O GitHub BB usa modelo de acesso por **time/equipe**. Ter o papel de cluster (ALMFD/ALMFE) **não** garante acesso ao GitHub — são sistemas separados. Preciso ser incluído no time correto.

**🔧 COMO VOU USAR:** Com acesso de escrita, posso clonar o código, fazer alterações, abrir PRs e fazer push na branch de deploy para acionar o pipeline.

**Detalhes importantes:**
- O nome do time precisa ser **exatamente** igual ao cadastrado no GENTI/BusinessMap.
- Selecione sempre o **menor papel necessário** (write, não manutenção).
- Depois de aprovado, aguarde até **2 horas** para a sincronização completar.
- Se após 2 horas o acesso não funcionar: abra uma issue no [atendimento da devCloud](https://fontes.intranet.bb.com.br/dev/publico/atendimento/-/issues).

---

## Passo 4 — Garantir seu acesso ao cluster (OpenShift e ArgoCD)

### O que fazer

1. Abra o link do ArgoCD HML (anotado no Passo 1).
2. Tente visualizar a aplicação do Educador.
3. Abra o console do OpenShift HML (anotado no Passo 1).
4. Tente navegar até o namespace do Educador.

### Se o acesso for negado

**🗣 COM QUEM FALAR:** Seu **gestor responsável** pela concessão de papéis.

**📋 O QUE PEDIR (texto modelo):**

> Preciso de acesso ao cluster OpenShift e ao ArgoCD para o projeto Educador Financeiro.
>
> - Projeto/sigla: `IAA`
> - Minha identificação: [sua matrícula/chave]
> - Ambiente: HML (homologação) — é o ambiente principal para validação inicial
>
> Papéis que identifiquei na documentação:
> - `ALMFDIAA` — perfil de desenvolvimento (acesso ao cluster/ArgoCD)
> - Se houver necessidade específica de HML com exec+secrets, o papel `IAARTEC` pode ser necessário (conforme tabela de papéis Kubernetes)
>
> Preciso para:
> 1. Acompanhar o deploy da aplicação no ArgoCD
> 2. Verificar se os pods estão rodando
> 3. Conferir se as Secrets foram criadas pelos operadores
> 4. Executar testes de saúde dentro do pod
>
> Peço que confirme qual papel exato devo solicitar no Painel de Acesso para ter essas permissões em HML.

**❓ POR QUE ESTOU PEDINDO:** O ArgoCD e o OpenShift exigem papéis específicos vinculados à sigla do projeto. Sem eles, não consigo acompanhar o deploy nem diagnosticar problemas.

**🔧 COMO VOU USAR:**
- **ArgoCD:** para ver se a aplicação está `Synced` e `Healthy` depois do deploy.
- **OpenShift:** para ver os pods, logs, eventos e confirmar que as Secrets existem.

**Referência de papéis (documentação consultada):**

| Papel | DES | HML | PRD |
|---|---|---|---|
| `ALMFD<SIGLA>` | Admin Local (exec + secrets) | Atualização de Workloads | Visualização |
| `ALMFE<SIGLA>` | Admin Local (exec + secrets) | Atualização de Workloads | Visualização |
| `<SIGLA>RTEC` | Admin Local | Atualização + Exec + Secrets | Visualização |
| `<SIGLA>#SCRT` | Exec + Secrets | Exec + Secrets | Exec + Secrets |

**Após a aprovação do papel:** Se o sistema continuar negando acesso, sincronize manualmente:
1. Acesse o [Portal AIC](https://portal.aic.intranet.bb.com.br/#/home).
2. Clique em **Meus acessos**.
3. Clique em **Sincronizar meus acessos**.

---

## Passo 5 — Conferir o template recebido

### O que fazer

1. No repositório de **código** (GitHub), abra estes arquivos e anote:

| Arquivo | O que procurar | Anotação |
|---|---|---|
| `README.md` | Instruções de setup, versão Python | ______________________ |
| `aic.json` | Valor de `versaoPython` — **deve ser `"3.11"`** | ______________________ |
| `setup.py` | Nome do pacote Python e `python_requires` | ______________________ |
| `Dockerfile` | Imagem base Python | ______________________ |
| `agent_config.yaml` | URL do Gateway, modelo, nome do agente | ______________________ |
| `.env.example` | Lista de variáveis necessárias | ______________________ |

2. **⚠ ALERTA CRÍTICO:** Se `aic.json` tiver `versaoPython` diferente de `"3.11"`, o build vai falhar. Na jornada do MCP, o template veio com `"3.8"` e o pipeline quebrou porque `fastmcp` exige Python ≥ 3.10. Se estiver errado, corrija antes de qualquer build.

3. Confira em `agent_config.yaml` se o `base_url` do Gateway aponta para o ambiente correto:
   - HML: `https://llms-agentes-ia.outbound.api.hm.bb.com.br/v1`
   - DES: `https://llms-agentes-ia.outbound.api.desenv.bb.com.br/v1`

---

## Passo 6 — Obter a AppKey do Educador

> **⛔ SEGURANÇA:** A AppKey é a credencial que autoriza o agente a chamar o Gateway/modelo de IA. Sem ela, o agente inicia mas **não consegue responder** a nenhuma pergunta. Nunca registre o valor em código, Wiki, chat, print ou commit.

### 🗣 COM QUEM FALAR

**Equipe responsável pelo Catálogo de Aplicações** na TechBB. A referência do Consultor diz que a AppKey vem do "Catálogo de Aplicações — origem da AppKey da aplicação, disponível para os três ambientes e recebida por e-mail."

### 📋 O QUE PEDIR (texto modelo)

> Preciso da **AppKey** do agente Educador Financeiro para o ambiente de **homologação (HML)**.
>
> - Nome do agente/aplicação: `mf-edu-fin`
> - Sigla: `IAA`
> - Tipo: Agente de IA (mesma oferta do Consultor Financeiro)
> - Ambiente solicitado: HML (e DES, se houver)
> - Gateway que será consumido: Gateway Outbound BB (`llms-agentes-ia.outbound.api.hm.bb.com.br`)
>
> Essa AppKey será usada como valor da variável `GATEWAY_OUTBOUND_GW_APP_KEY`, que o agente envia no header `x-application-key` ao chamar o modelo de linguagem (LLM) via Gateway Outbound.
>
> Por favor, envie-a pelo canal seguro autorizado (a referência do projeto anterior indica recebimento por e-mail). Não a incluirei em código, repositório ou documentação.

### ❓ POR QUE ESTOU PEDINDO

O código em `gateway_outbound.py` faz `os.environ["GATEWAY_OUTBOUND_GW_APP_KEY"]` — leitura estrita sem fallback. Se a variável não existir, o agente levanta `KeyError` e **não inicia**. Se existir mas for inválida, o Gateway rejeita a chamada.

### 🔧 COMO VOU USAR

1. **No cluster (HML):** O valor será colocado dentro de uma **Secret OpenShift** chamada `env`, na chave `GATEWAY_OUTBOUND_GW_APP_KEY`. O `values.yaml` do deploy importa essa Secret via `envFrom.secretRef.name: env`. O pod lê a variável automaticamente ao iniciar.
2. **Localmente (se precisar testar):** O valor vai no arquivo `.env` local, que **nunca** é enviado ao GitHub.

### O que fazer quando receber

- Guarde o valor em local seguro (gerenciador de senhas, não em arquivo texto aberto).
- Não cole em chat, print, ou documentação.
- Use no Passo 7 para criar a Secret.

---

## Passo 7 — Criar a Secret `env` no OpenShift HML

> **⚠ ATENÇÃO:** Só faça este passo depois de ter a AppKey (Passo 6) e o acesso ao cluster (Passo 4). Se a equipe de plataforma já criou essa Secret automaticamente, **não a recrie nem substitua**.

### O que fazer primeiro

1. Abra o console OpenShift HML do Educador (link do Passo 1).
2. Navegue até o namespace do Educador.
3. Vá em **Secrets**.
4. Procure se já existe uma Secret chamada `env`.

### Se a Secret `env` já existir

**🗣 COM QUEM FALAR:** O **responsável pelo namespace** ou a equipe de plataforma.

**📋 O QUE PEDIR (texto modelo):**

> No namespace HML do Educador Financeiro (`mf-edu-fin`), sigla `IAA`, já existe uma Secret chamada `env`.
>
> Preciso confirmar, **sem que o valor seja revelado**, que essa Secret contém a chave `GATEWAY_OUTBOUND_GW_APP_KEY` com a AppKey válida do Educador para HML.
>
> O agente importa essa Secret via `envFrom.secretRef.name: env` no `values.yaml`. Se a chave não estiver presente ou estiver vazia, o pod vai falhar ao iniciar (`KeyError`).

### Se a Secret `env` NÃO existir

Você vai criá-la. Para isso precisa do papel `IAA#SCRT` (confirme com o gestor se você tem, ou solicite conforme Passo 4).

**Procedimento:**

1. No console OpenShift, confirme que está no **namespace correto do Educador em HML**.
2. Clique em **Secrets**.
3. Clique em **Create** → **Key/Value Secret**.
4. Preencha:
   - **Secret name:** `env`
   - **Key:** `GATEWAY_OUTBOUND_GW_APP_KEY`
   - **Value:** [cole a AppKey recebida no Passo 6, diretamente no campo protegido]
5. Clique em **Create**.
6. **Não tire print da tela com o valor visível.**

### Se você não tiver o papel para criar Secrets

**🗣 COM QUEM FALAR:** Seu **gestor responsável**.

**📋 O QUE PEDIR (texto modelo):**

> Preciso criar uma Secret OpenShift no namespace HML do Educador Financeiro (`mf-edu-fin`), sigla `IAA`.
>
> - Nome da Secret: `env`
> - Chave: `GATEWAY_OUTBOUND_GW_APP_KEY`
> - Valor: [a AppKey do Educador que recebi — posso fornecer pelo canal seguro que indicar]
>
> Para criar Secrets, a documentação indica o papel `IAA#SCRT`. Esse papel deveria ter sido criado automaticamente com base nos dados da sigla no DPR.
>
> Preciso de uma dessas alternativas:
> 1. Receber o papel `IAA#SCRT` para criar a Secret eu mesmo, OU
> 2. Que alguém autorizado crie a Secret com os dados que forneço pelo canal seguro
>
> Sem essa Secret, o pod do agente não inicia (`envFrom.secretRef.name: env`).

---

## Passo 8 — Conferir o `values.yaml` de HML antes do deploy

### O que fazer

1. Abra o repositório de **deploy** do Educador no GitHub.
2. Mude para a branch `cloud/homologacao`.
3. Abra `values.yaml`.
4. Confira estes campos:

| Campo | Valor esperado | Está correto? |
|---|---|---|
| `service.enable` | `true` | ☐ |
| `deployment.enable` | `true` | ☐ |
| `deployment.containers.tag` | A tag da imagem publicada pelo build | ☐ |
| `envFrom.secretRef.name` | `env` | ☐ |
| `idhmtls.enabled` | `true` | ☐ |
| `idhmtls.secretName` | Um nome que faça sentido (ex: `idh-mtls`) | ☐ |
| `bbcert.enabled` | `true` (se ingress HTTPS for necessário) | ☐ |
| `bbcert.custodianteCertificado.matriculaBB` | A matrícula correta no formato `F99999999` | ☐ |
| `bbcert.dadosCertificado.ambientePKI` | `"hml"` | ☐ |
| `bbcert.dadosCertificado.commomName` | O hostname do Educador em HML | ☐ |

**⚠ `enable` vs `enabled`:** No template de referência, `service` e `deployment` usam **`enable`** (sem "d"). Mas `idhmtls` e `bbcert` usam **`enabled`** (com "d"). São chaves diferentes em blocos diferentes do chart.

5. **ATENÇÃO ao `service.enable`:** No template padrão, o Service vem **desabilitado** (`false`). Se estiver `false`, o pod sobe mas ninguém consegue se comunicar com ele. O primeiro problema documentado na jornada do MCP foi exatamente esse.

### Se a matrícula do custodiante estiver errada ou for do Consultor

**🗣 COM QUEM FALAR:** O **responsável pela PKI/certificados** da equipe.

**📋 O QUE PEDIR (texto modelo):**

> No `values.yaml` de HML do Educador Financeiro, o campo `bbcert.custodianteCertificado.matriculaBB` precisa ter a matrícula de quem receberá os e-mails da PKI BB e do Portal OaaS sobre este certificado.
>
> - Qual matrícula devo usar para o Educador? (formato `F99999999`)
> - Essa pessoa receberá notificações de emissão e renovação do certificado TLS de ingresso.

---

## Passo 9 — Verificar o build e a publicação da imagem

### O que fazer

1. Abra o repositório de **código** no GitHub.
2. Clique em **Actions**.
3. Selecione **⚙ Esteira de Build Python**.
4. Veja se já existe uma execução bem-sucedida em `main`.
5. Abra-a e confirme:
   - Qual commit foi processado
   - Se o job **CI** passou
   - Se a **imagem foi publicada** (procure no log a tag publicada)
   - Se os jobs **CD (desenvolvimento)** e **CD (homologação)** executaram ou foram ignorados

### Se nenhum build foi feito ainda

Antes de executar, confirme que:
- [ ] O `aic.json` tem `versaoPython: "3.11"` (Passo 5)
- [ ] A Secret `env` já existe no namespace HML (Passo 7)
- [ ] O `values.yaml` de HML está configurado (Passo 8)

Depois, execute manualmente:

```text
Repositório de código → Actions → ⚙ Esteira de Build Python
→ Run workflow → escolher branch (main ou a branch correta)
→ manter "Publicar versão fechada fora da branch main" desmarcada (a menos que tenha motivo)
→ Run workflow
```

### Se o build passou mas a imagem não foi publicada

**Causa provável:** O build foi feito numa branch auxiliar (`feat/**`, `fix/**`) que não publica imagem automaticamente, a menos que `publica_versao_fechada_branch_auxiliar` esteja marcado ou que o código chegue a `main` via merge.

**Solução:** Faça o merge do PR para `main`. O push em `main` publica a imagem oficial e pode disparar autodeploy para DES e HML.

### Se o build falhou com erro de dependência Python

**Causa provável:** `aic.json` está com versão Python incorreta (ex: 3.8 em vez de 3.11).

**Solução:** Corrija o `aic.json`:
```json
{
  "pipeline": {
    "versaoPython": "3.11"
  }
}
```
Faça commit e push. O build deve ser reenviado.

### Anote a tag da imagem publicada

| Dado | Valor |
|---|---|
| Tag publicada | ______________________ |
| Branch/commit usados | ______________________ |
| Execução do Actions (link) | ______________________ |

---

## Passo 10 — Garantir que o deploy chegou a HML

### Cenário A: O autodeploy CD funcionou

Se na execução do Passo 9 o job **CD (homologação)** concluiu com sucesso, a tag já foi atualizada no `values.yaml` automaticamente. Vá direto ao Passo 11.

### Cenário B: O autodeploy foi ignorado/não executou

O job CD depende de duas condições: `autodeploy == 'true'` **E** `autodeploy-hom == 'true'`. Se alguma falhou, você precisa atualizar manualmente:

1. Abra o repositório de **deploy** → branch `cloud/homologacao`.
2. Abra `values.yaml`.
3. Clique no lápis (**Edit this file**).
4. Altere `containers.tag` para a tag publicada no Passo 9.
5. Confirme que `service.enable: true` e `deployment.enable: true`.
6. No campo de commit, escreva: `chore(hml): configura primeira imagem do Educador v[TAG]`
7. Faça commit diretamente na branch `cloud/homologacao` (se permitido) ou abra PR.
8. O push dispara **Actions → Deploy** no repositório de deploy.
9. Abra **Actions** e acompanhe a execução do workflow **Deploy**.

---

## Passo 11 — Verificar no ArgoCD

### O que fazer

1. Abra o ArgoCD HML (link do Passo 1).
2. Localize a aplicação do Educador.
3. Confirme:

| Indicador | Esperado | Está OK? |
|---|---|---|
| Sincronização | `Synced` | ☐ |
| Saúde | `Healthy` | ☐ |
| Pod | `Running` com contêineres prontos | ☐ |
| Imagem do pod | A tag do Passo 9 | ☐ |
| Secret `env` | Existe no namespace | ☐ |
| Secret `idh-mtls` | Existe (provisionada pelo operador) | ☐ |

### Se o pod estiver em `ImagePullBackOff`

**Significa que:** A plataforma não encontra a imagem no registry. Na jornada do MCP, isso aconteceu porque a imagem nunca foi publicada (build em branch auxiliar + Python 3.8).

**O que fazer:** Volte ao Passo 9 e confirme que a imagem realmente foi publicada com aquela tag exata.

### Se o pod estiver em `CrashLoopBackOff`

**Significa que:** O contêiner inicia e morre repetidamente. Causas comuns:
- Secret `env` não existe ou não contém `GATEWAY_OUTBOUND_GW_APP_KEY` → `KeyError`
- Caminho de certificado inválido
- Erro de configuração em `agent_config.yaml`

**O que fazer:** No OpenShift, abra os **logs do pod** e leia a mensagem de erro.

### Se as Secrets de certificado (`idh-mtls`) não foram criadas

**🗣 COM QUEM FALAR:** Equipe de **plataforma/operações do cluster** ou suporte da oferta AIC.

**📋 O QUE PEDIR (texto modelo):**

> O operador `idhmtls` está habilitado no `values.yaml` de HML do Educador Financeiro, mas a Secret `idh-mtls` não foi criada no namespace após o primeiro deploy.
>
> - Namespace: [nome do namespace HML]
> - Aplicação ArgoCD: [nome/link]
> - O `values.yaml` declara `idhmtls.enabled: true` com `secretName: "idh-mtls"`
>
> Preciso que a Secret seja provisionada para que o agente consiga fazer mTLS de saída para o Gateway Outbound (LLM).

**❓ POR QUE ESTOU PEDINDO:** O `values.yaml` monta um volume chamado `tls-certs-volume` a partir da Secret `idh-mtls`, com os arquivos `tls.crt`, `tls.key` e `ca.crt` em `/app/certs`. O código em `gateway_outbound.py` lê esses caminhos via `KEY_STORE_CERT_PATH`, `KEY_STORE_KEY_PATH` e `TRUST_STORE_CA_PATH` para montar o contexto SSL de mTLS. Se a Secret não existir, o volume não é montado e o agente não consegue autenticar no Gateway.

---

## Passo 12 — Testar o agente dentro do pod

### O que fazer

1. No console OpenShift HML, abra o terminal do pod do Educador.
2. Execute o health check:

```bash
curl --max-time 10 -i http://localhost:8080/health/ready
```

**Esperado:** HTTP `200` com `{"status": "ready"}`.

3. Se o health passou, execute a chamada funcional:

```bash
curl --max-time 90 -i -X POST http://localhost:8080/chat \
  -H 'Content-Type: application/json' \
  -d '{"message":"Quanto é 2 + 2?"}'
```

**Esperado:** HTTP `200` com algo como:
```json
{
  "reply": "2 + 2 = 4",
  "session_id": null,
  "tool_calls_made": 0
}
```

### Se o health retornar 503

**Significa que:** O agente não está pronto. Provavelmente `graph.compile()` falhou no startup.

**O que fazer:** Leia os logs do pod. A mensagem de `detail` no 503 indica o motivo.

### Se o `/chat` retornar erro de Gateway/mTLS

**Significa que:** O agente está saudável, mas não consegue se comunicar com o modelo de IA. O problema está na combinação AppKey + certificado + configuração do Gateway.

**🗣 COM QUEM FALAR:** Equipe responsável pelo **Gateway Outbound / AgentOps**.

**📋 O QUE PEDIR (texto modelo):**

> O agente Educador Financeiro (`mf-edu-fin`) está rodando em HML. O health check retorna 200, mas ao chamar `/chat`, o agente retorna erro ao tentar se comunicar com o modelo via Gateway Outbound.
>
> - Endpoint configurado: `https://llms-agentes-ia.outbound.api.hm.bb.com.br/v1`
> - Modelo configurado: [copie de `agent_config.yaml`]
> - AppKey: está provisionada na Secret `env` no namespace HML (não revelo o valor)
> - Certificado IDH: Secret `idh-mtls` existe no namespace com `tls.crt`, `tls.key` e `ca.crt`
> - Erro retornado: [copie o erro do log do pod, removendo qualquer credencial]
>
> Preciso confirmar:
> 1. A AppKey do Educador está autorizada para esse endpoint em HML?
> 2. O modelo configurado está disponível para a aplicação `mf-edu-fin`?
> 3. O certificado IDH emitido no namespace é aceito pelo Gateway?

**❓ POR QUE ESTOU PEDINDO:** O agente usa mTLS com AppKey para chamar o LLM. A autenticação depende de 3 peças (AppKey + certificado + autorização no Gateway) que precisam estar alinhadas. O erro na chamada geralmente vem de uma delas.

**🔧 COMO VOU USAR:** A resposta me diz se preciso corrigir a AppKey, o certificado ou a configuração do modelo. O código em `gateway_outbound.py` substitui o path `/chat/completions` por `/cambio-chat-completion`, adiciona `api-version` como query parameter e injeta a AppKey no header `x-application-key`. Se algum desses elementos não estiver autorizado no Gateway, a chamada falha.

---

## Passo 13 — Testar pela API catalogada (acesso externo)

### O que fazer

1. Obtenha o endereço catalogado do Educador em HML. O formato de referência do Consultor é:
   `https://[nome-educador].ai-interno.api.hm.bb.com.br/v1/chat`

2. Faça uma chamada de teste usando a autorização exigida pelo catálogo.

### Se der erro 503 ou erro de mTLS na API catalogada

**Atenção:** Na validação do Consultor em DES, o pod funcionava internamente (health OK, `/chat` OK), mas o acesso externo pela API catalogada retornava erro `9502: "Falha ao validar mTLS no backend: mTLS obrigatório não configurado"`. Isso foi diagnosticado como problema na camada de Route/Ingress/Catalogação, **não na aplicação**.

**🗣 COM QUEM FALAR:** Equipe responsável pela **catalogação da API / Ingress / infraestrutura de rede**.

**📋 O QUE PEDIR (texto modelo):**

> O agente Educador Financeiro funciona internamente (health e /chat respondem dentro do pod em HML), mas a chamada pela API catalogada retorna erro.
>
> - Endpoint catalogado: [endereço]
> - Erro retornado: [copie o erro HTTP e o corpo da resposta]
> - Teste interno (dentro do pod): health 200, /chat 200 com resposta do modelo
>
> Preciso que seja verificado:
> 1. O Ingress/Route está configurado para o hostname do Educador em HML?
> 2. O certificado TLS de ingresso (provisionado pelo BBcert) está válido e associado?
> 3. A rota no catálogo de APIs está apontando para o Service correto?

**❓ POR QUE ESTOU PEDINDO:** O caminho externo passa por mais camadas (Ingress Controller, Route, TLS de ingresso, catálogo) que o caminho interno. Se o pod funciona mas a chamada externa falha, o problema está nessas camadas, não no agente. Na jornada do Consultor, nenhuma requisição externa chegou ao pod — os logs da aplicação estavam limpos.

---

## Passo 14 (Opcional) — Preparar ambiente local para desenvolvimento

> **NOTA:** Este passo só é necessário se você precisar alterar código ou testar localmente com o modelo real. Se o objetivo for apenas acompanhar o deploy e testar em HML, os passos anteriores são suficientes.

### O que você vai precisar pedir

Para rodar o agente localmente com chamada real ao modelo, você precisa de **3 coisas que não pode gerar sozinho:**

#### 14.1 — AppKey (já obtida no Passo 6)

#### 14.2 — Certificado cliente e chave privada

**🗣 COM QUEM FALAR:** Equipe responsável pela **entrega de certificados / AgentOps / PKI**.

**📋 O QUE PEDIR (texto modelo):**

> Preciso do certificado cliente (mTLS) e da chave privada correspondente para executar o agente Educador Financeiro **localmente** no meu ambiente de desenvolvimento, conectando ao Gateway Outbound de HML.
>
> - Agente: `mf-edu-fin`, sigla `IAA`
> - Ambiente de Gateway: HML
> - Uso: preencher `KEY_STORE_CERT_PATH` e `KEY_STORE_KEY_PATH` no `.env` local
> - Formato esperado: arquivos `.crt` e `.key` (os nomes no cluster de referência são `tls.crt` e `tls.key`)
>
> No cluster, esses arquivos vêm da Secret `idh-mtls` provisionada pelo operador. Para uso local, preciso de uma cópia autorizada entregue pelo canal seguro que a equipe determinar.
>
> **Não extrairei a Secret do cluster por conta própria.** Peço que indiquem o canal aprovado para essa entrega.

**❓ POR QUE ESTOU PEDINDO:** O código em `gateway_outbound.py` monta um `ssl.SSLContext` com esses arquivos para autenticação mTLS. Sem eles, a conexão com o Gateway é rejeitada.

**🔧 COMO VOU USAR:** Colocarei os arquivos em um diretório local (ex: `~/certs/`) e apontarei seus caminhos absolutos no `.env`:
```
KEY_STORE_CERT_PATH=/home/usuario/certs/edu-fin-hml-tls.crt
KEY_STORE_KEY_PATH=/home/usuario/certs/edu-fin-hml-tls.key
```

#### 14.3 — CA corporativa (se necessário)

**Pergunte junto com o item 14.2:** "Preciso também de um arquivo CA (`ca.crt`) para `TRUST_STORE_CA_PATH`, ou a confiança padrão do sistema é suficiente para validar o certificado do Gateway em HML?"

O código tem esta prioridade: `TRUST_STORE_CA_PATH` > `REQUESTS_CA_BUNDLE` > sem verificação customizada. Se nenhum for configurado, usa `verify=True` (confiança do sistema).

---

## Mapa de equipes e contatos

| Quando | Com quem falar | O que pedir |
|---|---|---|
| Provisionamento não concluiu (Passo 1) | Suporte da oferta de Agente de IA no TechBB | Conclusão do provisionamento |
| Migração de repositório falhou (Passo 2) | Suporte da Oferta AIC | Resolução da migração |
| Sem acesso ao GitHub (Passo 3) | Gestor técnico ou admin do repositório | Inclusão no time GitHub com permissão write |
| Sem acesso ao cluster/ArgoCD (Passo 4) | Gestor responsável pela concessão de papéis | Papéis `ALMFDIAA`, `IAARTEC` ou equivalente |
| Precisa da AppKey (Passo 6) | Equipe do Catálogo de Aplicações (TechBB) | AppKey do Educador para HML |
| Precisa criar Secret e não tem papel (Passo 7) | Gestor responsável | Papel `IAA#SCRT` ou criação assistida |
| Secret `env` existe mas precisa confirmar conteúdo (Passo 7) | Responsável pelo namespace | Confirmação da chave sem revelar valor |
| Matrícula do custodiante BBcert errada (Passo 8) | Responsável pela PKI da equipe | Matrícula correta no formato `F99999999` |
| Operador de certificado não criou Secret (Passo 11) | Suporte da plataforma/oferta AIC | Investigação do operador idhmtls |
| `/chat` falha com erro de Gateway (Passo 12) | Equipe do Gateway Outbound / AgentOps | Validação de AppKey, modelo e certificado |
| API catalogada retorna erro externo (Passo 13) | Equipe de catalogação / Ingress / infra de rede | Verificação de Route, TLS e catálogo |
| Precisa de certificados para uso local (Passo 14) | Equipe de certificados / AgentOps / PKI | Cópia autorizada dos arquivos mTLS |
| Grupo ITSM necessário | Gestor/admin da sigla IAA | Qual grupo ITSM da equipe IAA vincular |
| Problemas técnicos genéricos com cluster | Time da devCloud | Issue em `fontes.intranet.bb.com.br/dev/publico/atendimento/-/issues` |

---

## Checklist de progresso

- [ ] **Passo 1:** Provisionamento confirmado, links anotados
- [ ] **Passo 2:** Repositório de código está no GitHub
- [ ] **Passo 3:** Tenho acesso de escrita ao GitHub (código e deploy)
- [ ] **Passo 4:** Tenho acesso ao ArgoCD e OpenShift HML
- [ ] **Passo 5:** Template conferido, `aic.json` com Python 3.11
- [ ] **Passo 6:** AppKey do Educador recebida e guardada
- [ ] **Passo 7:** Secret `env` existe no namespace HML com a AppKey
- [ ] **Passo 8:** `values.yaml` de HML revisado e correto
- [ ] **Passo 9:** Build executado e imagem publicada com tag conhecida
- [ ] **Passo 10:** Deploy chegou a HML (autodeploy ou manual)
- [ ] **Passo 11:** ArgoCD mostra Synced + Healthy, pod pronto, Secrets existem
- [ ] **Passo 12:** Health 200 e `/chat` respondendo dentro do pod
- [ ] **Passo 13:** API catalogada testada
- [ ] **Passo 14:** Ambiente local preparado (se necessário)

---

Fontes: arquivos do workspace consultados em 15/09/2026, incluindo [wiki do Consultor](plg-agent-consult-fin.wiki/Home.md), [provisionamento](DOCUMENTACAO_GERAL/provisionar-microsservico.md), [onboarding GitHub](DOCUMENTACAO_GERAL/onboarding-github.md), [deploy Cloud](DOCUMENTACAO_GERAL/deploy-plataforma-cloud.md), [criação de Secrets](DOCUMENTACAO_GERAL/roteiros-master/openshift/Como_criar_secret.md), [papéis Kubernetes](DOCUMENTACAO_GERAL/papeis-niveis-acesso-kubernetes.md), [guia de certificados](ambiente/GUIA_CERTIFICADOS_E_SECRETS_CONSULT_FIN.md), [values.yaml HML](deploy-plg-agent-consult-fin-cloud-homologacao/values.yaml), [ci.yaml](plg-agent-consult-fin-main/.github/workflows/ci.yaml), [cd.yaml](deploy-plg-agent-consult-fin-cloud-homologacao/.github/workflows/cd.yaml), [gateway_outbound.py](plg-agent-consult-fin-main/plg_agent_consult_fin/llm/gateway_outbound.py), [validação DES](plg-agent-consult-fin.wiki/validacao-agente-des-e-jornada-mcp.md) e [jornada MCP](plg-agent-consult-fin.wiki/MCP-Server-Oficial-Consultor-PJ.md).
