# Continuação — Próximos passos até o primeiro `/chat` real

> Documento operacional. Criado em 08/09/2026.
>
> **NÃO altera e NÃO substitui:**
> - [`GUIA_PENGWIN_AO_HELLO_WORLD_CONSULT_FIN.md`](GUIA_PENGWIN_AO_HELLO_WORLD_CONSULT_FIN.md) — onboarding completo; consulte para explicações detalhadas.
> - [`BASELINE_V0_CONSULT_FIN.md`](BASELINE_V0_CONSULT_FIN.md) — baseline de análise do código.

---

## 1. Estado atual

| Item | Estado |
| --- | --- |
| Pengwin | confirmado pelo usuário |
| WSL / Ubuntu | WSL2 · Pengwin-WSL · Ubuntu 24.04.4 LTS · zsh |
| Git | 2.43.0 · funcional |
| Código analisado | download da branch `main` do GitHub · sem `.git` |
| Clone real GitHub | existe no ambiente do usuário · não acessível nesta análise |
| Commit / origin / histórico | **NÃO DETERMINADO** pela cópia analisada |
| Python 3.12.5 | observado no sistema |
| Python 3.11.x | referência preferencial do projeto; disponibilidade a verificar |
| venv | funcional |
| pip global | não estava disponível via `python3 -m pip` naquele momento |
| pyenv | não disponível naquele momento |
| Dependências | ainda precisam ser validadas no clone real |
| DNS corporativo | funcional |
| HTTPS fontes/binários | funcional |
| Gateway Outbound (DNS) | resolve por DNS |
| HTTPS sem certificado cliente | chegou ao Gateway · recebeu `certificate required` |
| AppKey | **pendente** — não configurada |
| mTLS (cert + chave + CA) | **pendente** — caminhos não configurados |
| MCP local | DNS `*.svc.cluster.local` não resolve fora do cluster |
| Agent local | não validado |
| `/chat` | não validado |

> Para explicações sobre cada item, consulte o [guia completo](GUIA_PENGWIN_AO_HELLO_WORLD_CONSULT_FIN.md).

---

## 2. Decisões já tomadas

- Não alterar o código para obter o primeiro Hello World; testar a versão original.
- Python 3.11.x é a referência preferencial do projeto; `setup.py` aceita `>=3.11`.
- Não alterar o Python global desnecessariamente.
- MCP não é tratado como bloqueante enquanto o comportamento confirmado por inspeção do código for `tools=[]`; será confirmado novamente durante o startup real.
- `/health/live` e `/health/ready` **não** comprovam acesso real ao LLM.
- O critério de sucesso exige `POST /chat` com chamada real ao LLM — não apenas servidor aberto.

---

## 3. Sequência operacional

Execute um passo por vez. Leia o resultado antes de avançar.

### Passo -1 — VS Code e validações pré-clone

Fonte: [`ambiente_pengwin.md`](ambiente_pengwin.md).

#### VS Code (primeira vez)

O VS Code é instalado no **Windows** — não pelo Pengwin. O Pengwin configura apenas a integração WSL.

```text
1. Instalar VS Code no Windows: https://code.visualstudio.com
2. Instalar a extensão: ms-vscode-remote.vscode-remote-extensionpack
3. Reiniciar o VS Code
4. Configurações → "Remote.WSL2: Connection Method" → wslExeProxy
   (se não existir, ignorar)
```

Após configurado, abrir qualquer projeto do Pengwin Terminal com:

```bash
code .
```

Não usar o Explorer do Windows para manipular arquivos do WSL.

#### Validações antes do clone

**Pengwin operacional:**

```bash
versao
ajuda
```

Se `command not found`: você não está no Pengwin Terminal. Abrir pelo atalho correto.

**Proxy e conectividade:**

```bash
proxyStatus
```

**Git configurado:**

```bash
git --version
git config user.name
git config user.email
```

Confirmar nome e e-mail corporativos. Sem isso, commits ficam com identidade incorreta.

**Localização correta:**

```bash
cd $HOME
pwd
```

Resultado esperado: `/home/<usuario>`. Não clonar em `/mnt/c/...`.

**Acesso ao repositório (sem clonar):**

```bash
git ls-remote https://fontes.bb/<sigla>/<repositorio>.git HEAD
```

Se retornar o hash do HEAD → acesso ao Fontes OK.
Se retornar erro de certificado ou autenticação → resolver antes de clonar.

**Python (antecipar):**

```bash
python3.11 --version
python3 --version
```

---

### Passo 0 — Verificar o ambiente Pengwin antes de começar

Fonte: [`ambiente_pengwin.md`](ambiente_pengwin.md) — boas práticas oficiais da documentação do Pengwin.

O Pengwin Terminal é o ponto recomendado para trabalhar no ambiente Pengwin/WSL configurado pelo BB. Proxy, certificados e ferramentas são configurados no ambiente Pengwin; o estado efetivo deve ser validado pelos comandos apropriados.

```bash
# Verificar status do proxy corporativo
proxyStatus
```

Se algo parou de funcionar ou a senha do SISBB foi trocada:

```bash
reconfigurar
```

**Localização do clone:** é recomendado manter o clone no filesystem Linux do WSL, preferencialmente dentro do `$HOME`, em vez de `/mnt/c/...`, conforme o fluxo documentado do Pengwin.

**Credenciais e secrets:** não coloque AppKey, token ou caminhos de certificado no `.zshrc`, `.bashrc` ou `.profile` — o comando `diagnosticar` captura esses arquivos. Carregue o `.env` manualmente na sessão (Passo 8), não na inicialização do shell.

**Binding `0.0.0.0`:** o Agent usa `--host 0.0.0.0` no Passo 9, o que é necessário para que serviços no Windows (como `curl`) alcancem a aplicação rodando no WSL.

---

### Passo 1 — Identificar o clone real

No Pengwin Terminal, dentro da raiz do clone:

```bash
pwd
git rev-parse --show-toplevel
git status
git remote -v
git branch --show-current
git rev-parse HEAD
git ls-remote --symref origin HEAD
```

**Registre:** caminho absoluto, remote `origin`, branch atual, hash HEAD.
Se a árvore não estiver limpa (`git status` com alterações), entenda o que mudou antes de prosseguir.

---

### Passo 2 — Criar branch pessoal

Somente após confirmar árvore limpa:

```bash
git switch -c feature/manuel-local-validation
```

Não faça `push`. Esta branch é apenas para rastrear eventuais ajustes locais sem contaminar `main`.

---

### Passo 3 — Verificar Python disponível

```bash
python3.11 --version
python3 --version
```

- Se `python3.11` existir → use-o nos passos seguintes.
- Se não existir → verifique se outro Python `>=3.11` está disponível. Registre o resultado na tabela da Seção 6.

---

### Passo 4 — Criar `.venv`

Com o Python adequado identificado no Passo 3:

```bash
python3.11 -m venv .venv
source .venv/bin/activate

which python
python --version
python -m pip --version
```

Adapte somente se o Python efetivamente escolhido for outro compatível (`>=3.11`).

---

### Passo 5 — Instalar runtime

```bash
python -m pip install -r requirements.txt
python -m pip install -e .
python -m pip check
```

Observe erros de compilação ou dependências conflitantes. Não ignore warnings de `pip check`.

---

### Passo 6 — Executar testes

```bash
python -m pip install -e ".[unit,integration]"
python -m pytest tests/unit tests/integration
```

> **Atenção:** esses testes validam a lógica local. Eles **não** comprovam conectividade real com o Gateway ou o LLM.

---

### Passo 7 — Configuração de ambiente

Você precisará obter, por canais autorizados, os valores de:

```text
GATEWAY_OUTBOUND_GW_APP_KEY
KEY_STORE_CERT_PATH
KEY_STORE_KEY_PATH
TRUST_STORE_CA_PATH
```

**Não registre esses valores neste documento.**
Prepare um arquivo `.env` local (não versionado) apenas quando tiver os valores autorizados.

---

### Passo 8 — Carregar `.env`

Somente após preparar e revisar o `.env`:

```bash
set -a
source .env
set +a
```

Confirme que as variáveis foram carregadas sem expor seus valores:

```bash
# AppKey: verifica presença (comprimento > 0) sem imprimir o valor
[ -n "$GATEWAY_OUTBOUND_GW_APP_KEY" ] && echo "AppKey: presente" || echo "AppKey: AUSENTE"

# Certificado cliente: variável preenchida e arquivo legível
[ -n "$KEY_STORE_CERT_PATH" ] && [ -r "$KEY_STORE_CERT_PATH" ] && echo "cert: legível" || echo "cert: PROBLEMA"

# Chave privada: variável preenchida e arquivo legível
[ -n "$KEY_STORE_KEY_PATH" ] && [ -r "$KEY_STORE_KEY_PATH" ] && echo "key: legível" || echo "key: PROBLEMA"

# CA: variável preenchida e arquivo legível
[ -n "$TRUST_STORE_CA_PATH" ] && [ -r "$TRUST_STORE_CA_PATH" ] && echo "CA: legível" || echo "CA: PROBLEMA"
```

---

### Passo 9 — Iniciar o Agent

Terminal A:

```bash
python -m plg_agent_consult_fin \
  --host 0.0.0.0 \
  --port 8080
```

Observe os logs de startup: descoberta de ferramentas MCP, construção do LLM, compilação do grafo LangGraph.

---

### Passo 10 — Health checks

Terminal B:

```bash
curl http://localhost:8080/health/live
curl http://localhost:8080/health/ready
```

Resultado esperado: `200 OK` em ambos.
Lembre-se: health OK **não** confirma LLM acessível.

---

### Passo 11 — Hello World

Terminal B:

```bash
curl -X POST http://localhost:8080/chat \
  -H 'Content-Type: application/json' \
  -d '{
    "message": "Responda somente: Hello World",
    "session_id": "hello-world-local"
  }'
```

Resultado esperado: `HTTP 200` com resposta textual gerada pelo LLM via Gateway.

---

## 4. Bloqueantes reais atuais

### Não bloqueantes por enquanto

- MCP de cluster não resolver localmente (comportamento `tools=[]` confirmado por inspeção do código; será verificado novamente no startup real).
- pip global ausente não é necessariamente bloqueante; o pip da `.venv` será validado no Passo 4.
- Python 3.12 existir no sistema — desde que um Python `>=3.11` seja usado para a `.venv`.

### Potencialmente bloqueantes

| Bloqueante | Status |
| --- | --- |
| Python compatível `>=3.11` disponível para criar a `.venv` | a verificar (Passo 3) |
| Python 3.11.x: referência preferencial para alinhamento com AIC/Docker | a verificar (Passo 3) |
| Instalação das dependências sem erros | a verificar (Passo 5) |
| AppKey autorizada e disponível | **pendente** |
| Certificado cliente (`.crt` / `.pem`) | **pendente** |
| Chave privada correspondente | **pendente** |
| CA correta configurada | **pendente** |
| Autorização do modelo no Gateway | **pendente** |
| Conectividade TCP/TLS Agent → Gateway | a verificar após configuração |

---

## 5. Critério de sucesso

```text
HELLO WORLD E2E = CONFIRMADO
```

somente quando houver **tudo ao mesmo tempo**:

```text
✓ Agent local iniciado sem erro
✓ POST /chat → HTTP 200
✓ Resposta produzida pelo fluxo original do Agent
✓ Chamada real ao Gateway/LLM confirmada nos logs
```

Health check isolado, resposta simulada ou mock **não contam**.

---

## 6. Registro de execução

Preencha conforme os passos forem executados:

| Etapa | Resultado | Evidência | Data |
| --- | --- | --- | --- |
| VS Code e pré-clone verificados | PENDENTE | | |
| Ambiente Pengwin verificado | PENDENTE | | |
| Git / clone real identificado | PENDENTE | | |
| Branch pessoal criada | PENDENTE | | |
| Python verificado | PENDENTE | | |
| `.venv` criada e ativa | PENDENTE | | |
| Dependências instaladas | PENDENTE | | |
| Testes unitários/integração | PENDENTE | | |
| `.env` carregado | PENDENTE | | |
| Startup do Agent | PENDENTE | | |
| `/health/live` | PENDENTE | | |
| `/health/ready` | PENDENTE | | |
| `POST /chat` | PENDENTE | | |
| **Hello World E2E** | **PENDENTE** | | |

---

## 7. Referências

| Documento | Finalidade |
| --- | --- |
| [`GUIA_PENGWIN_AO_HELLO_WORLD_CONSULT_FIN.md`](GUIA_PENGWIN_AO_HELLO_WORLD_CONSULT_FIN.md) | Onboarding completo: conceitos, checkpoints, troubleshooting |
| [`BASELINE_V0_CONSULT_FIN.md`](BASELINE_V0_CONSULT_FIN.md) | Baseline de análise estática do código |
| [`ambiente_pengwin.md`](ambiente_pengwin.md) | Documentação oficial do Pengwin |

---

> **Segurança:** nunca registre neste documento AppKey, senha, token, chave privada, conteúdo de certificado, secret Kubernetes ou credencial GitHub.
