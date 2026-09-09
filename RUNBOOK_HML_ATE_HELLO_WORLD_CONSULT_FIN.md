# Runbook HML do CONSULT FIN até o primeiro Hello World real

Este runbook orienta uma execução manual, etapa por etapa, no Pengwin. O Agent roda primeiro no computador local e consome exclusivamente serviços funcionais de **homologação (HML)**.

```text
Pengwin local
  → Agent local
  → Gateway Outbound HML
  → LLM HML
  → resposta no POST /chat local
```

Execute um bloco por vez. Depois de cada comando, valide o resultado, interprete o cenário e decida se pode avançar.

> **Regra absoluta:** a primeira etapa obrigatória que falhar encerra a execução. Escreva **`PARE AQUI`** e registre todas as etapas dependentes como **`NÃO EXECUTADO — bloqueado pela etapa X`**. Uma etapa bloqueada não é um erro independente.

## Escopo HML e segurança

Não use DES, PRD ou produção em nenhum teste funcional. O índice corporativo compartilhado está autorizado somente para instalar e resolver pacotes, inclusive pelo proxy e pelas CAs corporativas necessárias. Essa autorização não alcança Gateway, AppKey, certificado cliente, modelo, MCP, API, Kubernetes, deploy ou telemetria.

| Item | Deve pertencer a |
| --- | --- |
| AppKey usada no teste | HML e aplicação autorizada para HML |
| Certificado cliente | Fluxo outbound autorizado de HML |
| Chave privada | Mesmo par do certificado HML |
| CA ou bundle | Confiança correta para o Gateway HML |
| Gateway URL | HML |
| Modelo | Autorizado em HML |
| MCP | HML |
| Cluster, namespace e deploy | HML |
| API externa, se testada | HML |

Se a origem de qualquer item não puder ser associada inequivocamente a HML, registre:

```text
PARAR — AMBIENTE DA CREDENCIAL NÃO CONFIRMADO
```

Nunca solicite, registre ou compartilhe AppKey, token, senha, `.env`, chave privada, conteúdo de certificados ou CAs, Secret Kubernetes, connection string, headers autenticados ou credenciais GitHub. Não compartilhe logs antes de remover dados pessoais, caminhos internos, hosts não necessários, identificadores e credenciais.

Não use como solução: `curl -k`, `verify=False`, `sslVerify=false`, `chmod 777`, `git reset --hard`, `git clean -fd`, `sudo pip`, pip global, `--trusted-host`, desativação do proxy sem diagnóstico ou edição de `/etc/hosts` para contornar DNS.

## Como classificar evidências

| Classificação | Uso |
| --- | --- |
| **CONFIRMADO POR INSPEÇÃO** | Demonstrado pelo código ou arquivo atual analisado; não prova execução |
| **CONFIRMADO POR EXECUÇÃO** | Observado nesta jornada real e registrado sem secrets |
| **HISTÓRICO** | Veio de snapshot, manifest antigo, Wiki ou execução anterior; exige reconfirmação |
| **INFERIDO** | Conclusão técnica fundamentada, ainda não observada diretamente |
| **NÃO DETERMINADO** | Não há evidência suficiente; não preencher por suposição |

Um resultado esperado é apenas critério para a futura execução. Nunca o registre como resultado observado antes de executar.

## Checkpoints independentes

Os checkpoints abaixo são independentes e acumulativos:

- **A — `CHECKPOINT LOCAL = CONFIRMADO`:** Git, Python, dependências e testes locais aprovados.
- **B — `HELLO WORLD LOCAL → HML GATEWAY = CONFIRMADO`:** `localhost → Agent local → Gateway Outbound HML → LLM HML → resposta` foi comprovado.
- **C — `HELLO WORLD AGENT IMPLANTADO EM HML = CONFIRMADO`:** o `/chat` real do Agent implantado em HML chegou ao Gateway/LLM HML.
- **D — `API EXTERNA HML = CONFIRMADA`:** checkpoint opcional da camada externa/catalogada.

O checkpoint B **não depende** da Fase D deste runbook. Se não houver acesso ao OpenShift depois que B estiver confirmado, mantenha B como concluído e marque as etapas 21 a 24 como **`NÃO EXECUTADO — acesso HML ao cluster não disponível`**.

> **Endpoints diferentes:** `POST /chat` é a rota do FastAPI do Agent. Uma eventual `/v1/chat` pertence à camada externa/catalogada. O primeiro Hello World local usa `/chat` e não depende de `/v1/chat`.

## Termos essenciais

- **pyenv:** escolhe entre versões de Python instaladas. Seu *shim* é um encaminhador; o interpretador é o Python real.
- **venv:** ambiente Python isolado do sistema para este projeto.
- **pip:** instala pacotes Python dentro da venv.
- **AppKey:** credencial da aplicação enviada ao Gateway.
- **TLS:** protege e valida uma conexão HTTPS. **CA** é a autoridade usada para confiar no servidor.
- **mTLS:** TLS mútuo; além de validar o servidor, o cliente apresenta certificado e prova que possui a chave privada correspondente.
- **Gateway:** porta de saída corporativa usada pelo Agent para chegar ao modelo.
- **LLM:** modelo que produz a resposta.
- **MCP:** protocolo pelo qual o Agent descobre e chama ferramentas externas.
- **pod:** unidade em execução no Kubernetes/OpenShift. **Service** oferece endereço estável para pods.
- **Ingress/Route:** camada que publica o Service para outros clientes.

Para explicações detalhadas, consulte [o guia Pengwin](GUIA_PENGWIN_AO_HELLO_WORLD_CONSULT_FIN.md), [a continuação operacional](CONTINUACAO_HELLO_WORLD_CONSULT_FIN.md), [o guia de certificados e secrets](GUIA_CERTIFICADOS_E_SECRETS_CONSULT_FIN.md) e [a baseline](../BASELINE_V0_CONSULT_FIN.md).

## Fontes e precedência

Este runbook confronta o código atual (`agent_config.yaml`, `.env.example`, `requirements.txt`, `setup.py`, `README.md`, pacote `plg_agent_consult_fin/` e testes), as evidências reais [`firstClone.txt`](../firstClone.txt) e [`RESP_TESTE_PWG.txt`](../RESP_TESTE_PWG.txt), os guias acima, os arquivos de deploy HML disponíveis e os documentos históricos [`Home.md`](../plg-agent-consult-fin.wiki/Home.md) e [`validacao-agente-des-e-jornada-mcp.md`](../plg-agent-consult-fin.wiki/validacao-agente-des-e-jornada-mcp.md).

Para comportamento da aplicação, aplique sempre:

```text
CÓDIGO ATUAL > DOCUMENTAÇÃO HISTÓRICA
```

O clone real confirmou o GitHub `https://github.com/bbvinet/plg-agent-consult-fin.git`, a default branch `main`, o commit inicial já registrado e a branch local `feature/mccf-local`. O código disponibilizado para inspeção foi informado como download de `main`; sua igualdade byte a byte com o commit do clone não foi comprovada por Git neste workspace.

# Fase A — Preparação local para consumir HML

Estado já confirmado por execução anterior: Pengwin 1.10.1, WSL2, Ubuntu 24.04.4 LTS, zsh 5.9, Git 2.43.0, pyenv 2.4.10 e Python 3.11.9 instalado. Não repita diagnósticos gerais enquanto essas condições permanecerem válidas.

## Etapa 1 — Confirmar Git

### Objetivo

Confirmar que a execução ocorre no clone real, na branch já escolhida, sem mudanças locais. Um commit diferente do inicial pode ser legítimo, mas precisa ser explicado antes de continuar.

### Comando

```bash
cd /home/wsl/plg-agent-consult-fin
pwd
git branch --show-current
git status --short
git rev-parse HEAD
```

### Resultado esperado

Diretório `/home/wsl/plg-agent-consult-fin`, branch `feature/mccf-local`, nenhuma linha em `git status --short` e um commit registrado. O commit inicial conhecido é `7f81629cc47bf5092c96dcbb55fd281a00e61dba`.

### Possíveis cenários

| Resultado | Significado provável | O que fazer |
| --- | --- | --- |
| Branch correta, status vazio | Clone pronto | Registre o commit e avance |
| Commit diferente do inicial | Pode haver avanço autorizado | Identifique a origem e registre a autorização; não conclua erro automaticamente |
| Arquivos modificados ou não rastreados | Working tree não está limpa | Registre somente nomes/status, pare e decida com o responsável |
| Branch diferente | Contexto de trabalho incorreto | Pare; não crie terceira branch e não troque automaticamente |

### Critério para avançar

Branch `feature/mccf-local`, working tree limpa e commit atual conhecido e explicado.

### Se não passar

**PARE AQUI — categoria GIT.** Guarde a saída sanitizada de `pwd`, branch, hash e `git status --short`. Não use reset, clean, stash ou descarte automático. Etapas 2 a 24: `NÃO EXECUTADO — bloqueado pela etapa 1`.

## Etapa 2 — Confirmar Python 3.11.9

### Objetivo

Usar o interpretador real já instalado, sem alterar o Python global e sem criar `.python-version`. O shim é apenas um encaminhador e pode falhar quando outra versão está selecionada.

### Comando

```bash
"$(pyenv root)/versions/3.11.9/bin/python" --version
```

### Resultado esperado

`Python 3.11.9`.

### Possíveis cenários

| Resultado | Significado provável | O que fazer |
| --- | --- | --- |
| Python 3.11.9 | Interpretador real disponível | Avance |
| Caminho não existe | Instalação mudou | Execute apenas `pyenv versions` e pare |
| `python3.11` via shim falha, mas o caminho direto funciona | 3.11 está instalado, porém não selecionado pelo pyenv | Ignore o shim nesta jornada e use o caminho direto |
| Outra versão no caminho direto | Ambiente foi alterado | Classifique como AMBIENTE e pare |

### Critério para avançar

O comando direto responde exatamente com Python 3.11.9.

### Se não passar

**PARE AQUI — categoria PYTHON/AMBIENTE.** Registre versão do pyenv, saída de `pyenv versions` e mensagem do caminho direto, sem arquivos pessoais de configuração. Não use `pyenv global`, `sudo` ou reinstalação por tentativa. Etapas 3 a 24: `NÃO EXECUTADO — bloqueado pela etapa 2`.

## Etapa 3 — Criar ou validar `.venv`

### Objetivo

Criar um ambiente isolado com o Python 3.11.9. Não reutilize a virtualenv antiga `Teste_env`.

### Comando

```bash
test -e .venv && echo "venv existe" || echo "venv ausente"
# Se existir, valide primeiro:
test ! -e .venv || .venv/bin/python --version
# Somente se estiver ausente:
test -e .venv || "$(pyenv root)/versions/3.11.9/bin/python" -m venv .venv
test -x .venv/bin/python && echo "venv: OK" || echo "venv: ERRO"
```

### Resultado esperado

`.venv/bin/python` existe, é executável e responde `Python 3.11.9`.

### Possíveis cenários

| Resultado | Significado provável | O que fazer |
| --- | --- | --- |
| Ausente e criada com 3.11.9 | Ambiente novo correto | Avance |
| Existente e usa 3.11.9 | Ambiente já compatível | Avance sem recriar |
| Existente e usa 3.12 ou outra versão | Venv incorreta para esta jornada | Pare; não apague automaticamente |
| Falha em `ensurepip` ou `venv` | Instalação Python incompleta | Classifique como VENV/AMBIENTE e pare |

### Critério para avançar

`.venv/bin/python --version` confirma Python 3.11.9.

### Se não passar

**PARE AQUI — categoria VENV.** Registre a mensagem completa da criação e a versão encontrada. Não use sudo e não remova `.venv` sem decisão explícita. Etapas 4 a 24: `NÃO EXECUTADO — bloqueado pela etapa 3`.

## Etapa 4 — Ativar e conferir o ambiente virtual

### Objetivo

Garantir que `python` e `pip` da sessão pertencem à `.venv`. Isso evita instalar pacotes no Python global.

### Comando

```bash
source .venv/bin/activate
which python
python --version
python -m pip --version
```

### Resultado esperado

O executável termina em `/plg-agent-consult-fin/.venv/bin/python`, a versão é 3.11.9 e o pip pertence à mesma `.venv`.

### Possíveis cenários

| Resultado | Significado provável | O que fazer |
| --- | --- | --- |
| Python e pip dentro da `.venv` | Isolamento correto | Avance |
| Python 3.12 | Venv incorreta | `PARAR — VENV INCORRETA` |
| pip ausente | Venv/Python incompleta | `PARAR — PYTHON/VENV INCOMPLETA` |
| Caminho fora do projeto | Ativação não ocorreu ou outra venv interferiu | Pare e registre os caminhos |

### Critério para avançar

Python 3.11.9 e pip executado por `python -m pip`, ambos dentro da `.venv`.

### Se não passar

**PARE AQUI — categoria VENV/PYTHON.** Registre somente caminhos dos executáveis, versões e erro do pip. Etapas 5 a 24: `NÃO EXECUTADO — bloqueado pela etapa 4`.

## Etapa 5 — Instalar requirements

### Objetivo

Instalar as dependências de runtime na `.venv` pelo índice corporativo autorizado para preparação. A conexão ao índice deve continuar com validação TLS.

### Comando

```bash
python -m pip config list
# Avance somente se não houver relaxamento TLS ativo:
python -m pip install -r requirements.txt
```

### Resultado esperado

Instalação concluída sem `ERROR`. Um índice corporativo compartilhado é aceitável nesta etapa; `trusted-host` ativo, `cert` inexistente ou bypass TLS não são aceitáveis.

### Possíveis cenários

| Resultado | Significado provável | O que fazer |
| --- | --- | --- |
| Instalação concluída | Dependências baixadas e instaladas | Avance |
| DNS não resolve | Rede corporativa/DNS | Categoria REDE; conferir Pengwin e resolução do índice |
| HTTP 407 | Proxy exige autenticação | Categoria PROXY; revisar `proxyStatus` e configuração autorizada |
| Falha de verificação TLS | CA/configuração do índice | Categoria TLS/AMBIENTE; corrigir confiança corporativa |
| `No matching distribution` | Versão Python, índice ou pacote indisponível | Conferir esses três itens e parar |
| `ResolutionImpossible` | Conflito entre dependências | Categoria DEPENDÊNCIAS; preservar o relatório e parar |
| `trusted-host` efetivamente ativo | TLS do índice foi relaxado | Pare e peça correção da configuração; não prossiga com essa exceção |

### Critério para avançar

O comando termina com código zero, sem bypass TLS e sem pacote ausente ou conflito.

### Se não passar

**PARE AQUI — categoria REDE, PROXY, TLS/AMBIENTE ou DEPENDÊNCIAS.** Registre pacote envolvido, tipo de erro e últimas linhas sanitizadas; remova URLs internas desnecessárias e qualquer token. Etapas 6 a 24: `NÃO EXECUTADO — bloqueado pela etapa 5`.

## Etapa 6 — Instalar o pacote editável

### Objetivo

Instalar o próprio CONSULT FIN na `.venv` sem alterar seu código. Isso valida metadados e empacotamento básicos.

### Comando

```bash
python -m pip install -e .
```

### Resultado esperado

Instalação editável concluída para `plg_agent_consult_fin`.

### Possíveis cenários

| Resultado | Significado provável | O que fazer |
| --- | --- | --- |
| Instalação concluída | Pacote reconhecido | Avance |
| Metadados/build falham | Problema de empacotamento | Categoria PROJETO/EMPACOTAMENTO; pare |
| Dependência adicional falha | Árvore ainda incompleta | Categoria DEPENDÊNCIAS; pare |
| Permissão negada | Local/venv incorretos ou permissões | Confirme diretório e `.venv`; não use sudo |

### Critério para avançar

O pacote editável é instalado com código zero.

### Se não passar

**PARE AQUI — categoria PROJETO/EMPACOTAMENTO.** Registre a fase do build e mensagem sanitizada. Não altere `setup.py` automaticamente. Etapas 7 a 24: `NÃO EXECUTADO — bloqueado pela etapa 6`.

## Etapa 7 — Verificar consistência com `pip check`

### Objetivo

Confirmar que os pacotes instalados satisfazem as dependências declaradas.

### Comando

```bash
python -m pip check
```

### Resultado esperado

`No broken requirements found.`

### Possíveis cenários

| Resultado | Significado provável | O que fazer |
| --- | --- | --- |
| Nenhum requisito quebrado | Ambiente coerente | Avance |
| Pacote requer versão diferente | Conflito instalado | Categoria DEPENDÊNCIAS; pare |
| Pacote requerido ausente | Instalação incompleta | Categoria DEPENDÊNCIAS; pare |

### Critério para avançar

`pip check` termina com código zero e nenhum requisito quebrado.

### Se não passar

**PARE AQUI — categoria DEPENDÊNCIAS.** Registre apenas nomes e versões envolvidos. Etapas 8 a 24: `NÃO EXECUTADO — bloqueado pela etapa 7`.

## Etapa 8 — Importar o Agent

### Objetivo

Validar que o pacote principal pode ser carregado pela `.venv`. Isso ainda não inicia o Agent nem acessa HML.

### Comando

```bash
python - <<'PY'
import plg_agent_consult_fin
print("IMPORT: OK")
PY
```

### Resultado esperado

`IMPORT: OK`.

### Possíveis cenários

| Resultado | Significado provável | O que fazer |
| --- | --- | --- |
| Import OK | Pacote básico acessível | Avance |
| `ModuleNotFoundError` do pacote | Instalação editável não efetiva | Categoria INSTALAÇÃO/PROJETO; pare |
| Módulo de dependência ausente | Requirements incompletos | Categoria DEPENDÊNCIAS; pare |
| Erro de configuração ou efeito colateral | Import executou lógica inesperada | Categoria PROJETO/CONFIGURAÇÃO; pare |

### Critério para avançar

O import termina com código zero e imprime `IMPORT: OK`.

### Se não passar

**PARE AQUI — categoria PROJETO, INSTALAÇÃO ou DEPENDÊNCIAS.** Registre tipo da exceção e traceback sanitizado. Etapas 9 a 24: `NÃO EXECUTADO — bloqueado pela etapa 8`.

## Etapa 9 — Instalar e validar extras de teste

### Objetivo

Instalar os extras declarados para testes unitários e de integração. Confirmar o executor antes de rodar a suíte.

### Comando

```bash
python -m pip install -e ".[unit,integration]"
python -m pytest --version
python -m pip check
```

### Resultado esperado

pytest disponível dentro da `.venv` e `pip check` sem requisitos quebrados.

### Possíveis cenários

| Resultado | Significado provável | O que fazer |
| --- | --- | --- |
| Extras, pytest e pip check OK | Ambiente de teste pronto | Avance |
| Extra desconhecido | Metadados divergentes | Categoria PROJETO/EMPACOTAMENTO; pare |
| pytest ausente | Instalação incompleta | Categoria DEPENDÊNCIAS; pare |
| Novo conflito no pip check | Extras tornaram a árvore inconsistente | Categoria DEPENDÊNCIAS; pare |

### Critério para avançar

Os três comandos terminam com código zero.

### Se não passar

**PARE AQUI — categoria DEPENDÊNCIAS ou PROJETO.** Registre mensagem e versões envolvidas. Etapas 10 a 24: `NÃO EXECUTADO — bloqueado pela etapa 9`.

## Etapa 10 — Executar testes unitários

### Objetivo

Validar o comportamento local coberto pela suíte unitária. Mocks e respostas simuladas não comprovam Gateway ou LLM HML.

### Comando

```bash
python -m pytest tests/unit
```

### Resultado esperado

Todos os testes coletados passam, sem `failed` ou `errors`.

### Possíveis cenários

| Resultado | Significado provável | O que fazer |
| --- | --- | --- |
| Todos passaram | Cobertura unitária aprovada | Registre apenas `collected/passed/failed/errors` e avance |
| `FAILED` | Comportamento não atende teste | Categoria TESTES/PROJETO; pare |
| `ERROR` na coleta/fixture | Ambiente ou teste não inicializou | Categoria TESTES/DEPENDÊNCIAS; pare |
| Teste pulado | Cobertura parcial | Registre motivo e só avance se o skip for declarado e não afetar o fluxo obrigatório |

### Critério para avançar

Zero testes `failed` e zero `errors`; qualquer skip está explicado e fora do fluxo obrigatório.

### Se não passar

**PARE AQUI — categoria TESTES.** Registre contagens, primeiro teste afetado e primeira exceção sanitizada. Não corrija código automaticamente. Etapas 11 a 24: `NÃO EXECUTADO — bloqueado pela etapa 10`.

## Etapa 11 — Executar testes de integração existentes

### Objetivo

Executar exatamente a suíte classificada pelo projeto como integração. No código analisado, ela contém apenas um teste demonstrativo de soma e não chama o Gateway HML.

### Comando

```bash
python -m pytest tests/integration
```

### Resultado esperado

Todos os testes coletados passam, sem `failed` ou `errors`.

### Possíveis cenários

| Resultado | Significado provável | O que fazer |
| --- | --- | --- |
| Todos passaram | Suíte existente aprovada | Registre contagens e avance |
| `FAILED` ou `ERROR` | Falha de teste/ambiente | Categoria TESTES; pare |
| Nenhum teste coletado | Suíte ausente ou descoberta divergente | Registre e pare para decisão |
| Teste passa | Não prova integração HML | Mantenha Gateway/LLM como NÃO DETERMINADO até `/chat` real |

### Critério para avançar

Zero `failed`, zero `errors` e pelo menos um teste coletado.

### Se não passar

**PARE AQUI — categoria TESTES.** Registre contagens e primeira mensagem sanitizada. Etapas 12 a 24: `NÃO EXECUTADO — bloqueado pela etapa 11`.

## Checkpoint A — preparação local

Só registre **`CHECKPOINT LOCAL = CONFIRMADO`** quando todos estiverem confirmados por execução:

```text
Git                   OK
Python 3.11.9         OK
.venv                 OK
pip                   OK
requirements          OK
editable install      OK
pip check             OK
import                OK
unit                   OK
integration            OK
```

Se qualquer item falhar, não inicie a configuração HML.

# Fase B — Configuração exclusiva de HML

A partir daqui entram itens sensíveis. Consulte o [guia de certificados e secrets](GUIA_CERTIFICADOS_E_SECRETS_CONSULT_FIN.md) sem copiar valores para este runbook.

## Etapa 12 — Confirmar a configuração efetivamente carregada

### Objetivo

Confirmar provider, Gateway, modelo, API version, MCP e integrações habilitadas a partir do mesmo carregador usado pelo Agent. A inspeção atual já encontrou valores HML no código, mas a execução deve reconfirmar o clone em uso.

### Comando

```bash
python - <<'PY'
from plg_agent_consult_fin.config import load_agent_config
c = load_agent_config()
print("provider:", c.llm.provider)
print("base_url:", c.llm.gateway_outbound.base_url)
print("model:", c.llm.gateway_outbound.model)
print("api_version:", c.llm.gateway_outbound.api_version)
print("mcp:", [s.transport.endpoint for s in c.mcp.servers])
print("rag_enabled:", c.rag.enabled)
print("external_guardrails_enabled:", c.guardrails.enabled)
PY
```

### Resultado esperado

Os valores carregados devem coincidir com os valores confirmados por inspeção do código atual:

```text
provider: gateway_outbound
base_url: https://llms-agentes-ia.outbound.api.hm.bb.com.br/v1
model: cambio-non-prod-gpt4o
api_version: 2024-12-01-preview
```

Registre a conferência sem copiar cegamente os valores esperados:

```text
Gateway HML confirmado no código: SIM
Modelo confirmado no código: SIM
API version confirmada: SIM
```

Na execução, registre novamente `SIM/NÃO`. O endpoint MCP `*.svc.cluster.local` deve ter sua associação a HML confirmada por fonte atual autorizada; o nome sozinho não identifica o ambiente.

### Possíveis cenários

| Resultado | Significado provável | O que fazer |
| --- | --- | --- |
| Gateway, modelo e API version HML; MCP associado a HML | Configuração funcional pertence a HML | Avance |
| Gateway contém DES ou produção | Configuração fora do escopo | `PARAR — CONFIGURAÇÃO NÃO ESTÁ EM HML` |
| Modelo ou MCP sem ambiente confirmado | Risco de mistura | `PARAR — AMBIENTE DA CREDENCIAL NÃO CONFIRMADO` |
| RAG ou guardrail externo habilitado | Existe outro destino funcional | Só avance se esse destino e acesso forem confirmadamente HML; caso contrário, pare |
| Valores diferentes da inspeção atual | Clone/configuração divergente | Registre a divergência e solicite decisão; não edite automaticamente |

### Critério para avançar

Provider, Gateway, modelo, API version e toda integração externa habilitada pertencem inequivocamente a HML; integrações opcionais não HML estão desabilitadas.

### Se não passar

**PARE AQUI — categoria CONFIGURAÇÃO HML.** Registre somente valores não sensíveis e o arquivo carregado. Não modifique YAML ou código. Etapas 13 a 24: `NÃO EXECUTADO — bloqueado pela etapa 12`.

## Etapa 13 — Confirmar os itens de acesso HML necessários

### Objetivo

Conferir os nomes que o código atual lê, sem procurar ou mostrar seus valores. O procedimento detalhado e os limites de compartilhamento estão no guia de secrets.

### Comando

```bash
rg -n 'GATEWAY_OUTBOUND_GW_APP_KEY|KEY_STORE_CERT_PATH|KEY_STORE_KEY_PATH|TRUST_STORE_CA_PATH|REQUESTS_CA_BUNDLE' \
  .env.example plg_agent_consult_fin/llm/gateway_outbound.py
```

### Resultado esperado

Os nomes necessários aparecem no exemplo e/ou provider:

```text
GATEWAY_OUTBOUND_GW_APP_KEY
KEY_STORE_CERT_PATH
KEY_STORE_KEY_PATH
TRUST_STORE_CA_PATH ou REQUESTS_CA_BUNDLE ou trust store padrão suficiente
```

### Possíveis cenários

| Resultado | Significado provável | O que fazer |
| --- | --- | --- |
| Nomes coincidem | Interface de configuração compreendida | Confirme com a equipe a origem HML e avance |
| Nome diverge no provider | Código mudou | Use o código como fonte principal, registre divergência e pare para decisão |
| AppKey/certificados HML ainda não foram disponibilizados | Dependência externa | Registre `ACESSO/SEGREDO — BLOQUEIO EXTERNO` e pare corretamente |
| Origem ambiental não comprovada | Pode ser DES/PRD/outro | Não use |

### Critério para avançar

Nomes atuais confirmados e origem HML de AppKey, certificado, chave e confiança TLS confirmada por canal autorizado, sem expor conteúdo.

### Se não passar

**PARE AQUI — categoria APPKEY, mTLS ou AUTORIZAÇÃO.** Não solicite valores no chat. Registre qual item está pendente e qual equipe/processo deve confirmar sua origem. Etapas 14 a 24: `NÃO EXECUTADO — bloqueado pela etapa 13`.

### Evidência histórica sobre certificados

Manifests e snapshots anteriores registram material HML com Secret chamado `idh-mtls` e arquivos `tls.crt`, `tls.key` e `ca.crt`. Isso é **HISTÓRICO**, não prova existência, validade ou autorização atuais. Se o procedimento operacional atual de obtenção não estiver confirmado, registre:

```text
PROCESSO OPERACIONAL ATUAL DE OBTENÇÃO = CONFIRMAR COM A EQUIPE
```

Este runbook não fornece comandos para imprimir ou extrair Secrets.

> **`idh-mtls ≠ bbcert`**: `idh-mtls` representa a identidade usada na saída `Agent → Gateway HML`. `bbcert` atende TLS de entrada `cliente → Ingress/Route → Agent`. Não substitua o certificado cliente outbound por certificado de ingress.

## Etapa 14 — Preparar o `.env` HML local

### Objetivo

Criar ou revisar um `.env` somente local, ignorado pelo Git e com permissão restrita. Preserve `.env.example` e não copie cegamente seu conteúdo: o exemplo analisado contém `DEPLOY_ENV=desenv` e placeholders.

### Comando

```bash
git check-ignore -q .env && echo ".env ignorado" || echo ".env NÃO ignorado"
test -e .env && echo ".env já existe — revisar sem exibir" || (umask 077 && touch .env)
chmod 600 .env
nano .env
zsh -n .env
set -a
source .env
set +a
```

### Resultado esperado

`.env` ignorado, local, com sintaxe válida e contendo somente configurações aprovadas para HML. Deixe telemetria opcional ausente ou vazia no primeiro Hello World, salvo decisão explícita para HML.

### Possíveis cenários

| Resultado | Significado provável | O que fazer |
| --- | --- | --- |
| Ignorado, sintaxe OK, carregado | Configuração local pronta | Avance |
| `.env` já existe | Pode conter configuração anterior | Revise localmente, sem imprimir; confirme cada ambiente antes de carregar |
| Não está ignorado | Risco de versionar secrets | Pare antes de criar/preencher; não altere `.gitignore` automaticamente |
| Placeholder ou `DEPLOY_ENV=desenv` permaneceu | Exemplo foi copiado sem revisão | Não carregue; corrija localmente para HML |
| `source` falha | Sintaxe de shell inválida | Pare e corrija sem exibir valores |

### Critério para avançar

`.env` está ignorado, sintaticamente válido, carregado na sessão e todos os itens funcionais nele pertencem a HML.

### Se não passar

**PARE AQUI — categoria CONFIGURAÇÃO HML/SEGREDO.** Registre apenas “ignorado: SIM/NÃO”, linha da falha de sintaxe sem conteúdo e estado do carregamento. Etapas 15 a 24: `NÃO EXECUTADO — bloqueado pela etapa 14`.

## Etapa 15 — Verificar configuração sensível sem revelar conteúdo

### Objetivo

Confirmar apenas presença da AppKey e legibilidade dos arquivos de mTLS. Também identificar a confiança TLS que o provider escolherá e qualquer telemetria herdada.

### Comando

```bash
[[ -n "${GATEWAY_OUTBOUND_GW_APP_KEY:-}" && "${GATEWAY_OUTBOUND_GW_APP_KEY}" != '<PREENCHER>' ]] && echo "AppKey HML: PRESENTE" || echo "AppKey HML: AUSENTE"
[[ -n "${KEY_STORE_CERT_PATH:-}" && -r "${KEY_STORE_CERT_PATH}" ]] && echo "cert HML: LEGÍVEL" || echo "cert HML: PENDENTE"
[[ -n "${KEY_STORE_KEY_PATH:-}" && -r "${KEY_STORE_KEY_PATH}" ]] && echo "key HML: LEGÍVEL" || echo "key HML: PENDENTE"
if [[ -n "${TRUST_STORE_CA_PATH:-}" ]]; then [[ -r "${TRUST_STORE_CA_PATH}" ]] && echo "CA: LEGÍVEL (TRUST_STORE_CA_PATH)" || echo "CA: PENDENTE"; elif [[ -n "${REQUESTS_CA_BUNDLE:-}" ]]; then [[ -r "${REQUESTS_CA_BUNDLE}" ]] && echo "CA: LEGÍVEL (REQUESTS_CA_BUNDLE)" || echo "CA: PENDENTE"; else echo "CA: TRUST STORE PADRÃO"; fi
[[ -n "${APPLICATION_INSIGHTS_CONNECTION_STRING:-}${OTEL_EXPORTER_OTLP_ENDPOINT:-}" ]] && echo "Telemetria externa: CONFIGURADA" || echo "Telemetria externa: AUSENTE"
# Execute as três verificações abaixo somente se cert e key estiverem legíveis:
openssl x509 -in "${KEY_STORE_CERT_PATH}" -noout -checkend 0 >/dev/null 2>&1 && echo "cert HML: FORMATO/VALIDADE OK" || echo "cert HML: FORMATO/VALIDADE PENDENTE"
openssl pkey -in "${KEY_STORE_KEY_PATH}" -noout >/dev/null 2>&1 && echo "key HML: FORMATO OK" || echo "key HML: FORMATO PENDENTE"
cmp -s <(openssl x509 -in "${KEY_STORE_CERT_PATH}" -pubkey -noout 2>/dev/null | openssl pkey -pubin -outform DER 2>/dev/null) <(openssl pkey -in "${KEY_STORE_KEY_PATH}" -pubout -outform DER 2>/dev/null) && echo "par cert/key: CORRESPONDE" || echo "par cert/key: NÃO CORRESPONDE"
```

### Resultado esperado

AppKey presente; certificado e chave legíveis; confiança TLS definida por CA legível ou trust store padrão explicitamente aceito para o teste. Telemetria ausente ou, se configurada, confirmadamente autorizada para HML.

### Possíveis cenários

| Resultado | Significado provável | O que fazer |
| --- | --- | --- |
| Todos os itens obrigatórios prontos | Pré-condições do startup atendidas | Avance |
| AppKey ausente | Acesso externo pendente, não bug do Agent | `ACESSO/SEGREDO — BLOQUEIO EXTERNO`; pare |
| Arquivo não legível | Caminho, origem ou permissão incorreta | Corrija conforme política; não use `chmod 777` |
| PEM/formato inválido | Material fornecido não pode ser interpretado | Pare e confirme o material com a origem autorizada; não converta por tentativa |
| Certificado fora da validade | Material não está válido no momento do teste | Pare e solicite material HML vigente |
| Certificado e chave não correspondem | Arquivos não formam o mesmo par | Pare e solicite o par HML correto |
| A chave pede senha inesperada | Forma de uso não foi definida para startup não interativo | Pare e confirme o procedimento autorizado; não registre a senha |
| CA explícita não legível | Provider falhará antes de usar alternativa | Corrija; não presuma fallback |
| Trust store padrão selecionado | Pode ser válido | Avance apenas com decisão registrada; aceitação será comprovada no `/chat` |
| Telemetria herdada e não prevista | Pode enviar dados ou interferir | Pare, identifique a origem e remova/ajuste na sessão antes do startup |

### Critério para avançar

Checkpoint B de configuração aprovado: HML confirmado, AppKey presente, cert/key legíveis e confiança TLS definida. Telemetria está ausente ou é HML e autorizada.

### Se não passar

**PARE AQUI — categoria APPKEY, mTLS, TLS ou CONFIGURAÇÃO HML.** Registre apenas PRESENTE/AUSENTE, LEGÍVEL/PENDENTE e a fonte de confiança escolhida. **PRESENTE ≠ VÁLIDA; LEGÍVEL ≠ CERTIFICADO ACEITO.** Etapas 16 a 24: `NÃO EXECUTADO — bloqueado pela etapa 15`.

# Fase C — Agent local consumindo HML

Telemetria não é requisito do primeiro Hello World. Ausência de Application Insights/OTel não bloqueia. Somente uma configuração herdada que interfira ou envie dados de forma não prevista exige parada.

## Etapa 16 — Iniciar o Agent

### Objetivo

Iniciar o FastAPI em primeiro plano no Terminal A, mantendo logs visíveis. Durante o startup, o LangGraph tenta descobrir MCP e constrói o provider do Gateway.

### Comando

```bash
python -m plg_agent_consult_fin \
  --host 0.0.0.0 \
  --port 8080
```

### Resultado esperado

Uvicorn inicia e permanece escutando na porta 8080. O startup conclui sem erro de AppKey, certificado, CA ou configuração.

### Possíveis cenários

| Resultado | Significado provável | O que fazer |
| --- | --- | --- |
| Startup concluído | Agent ativo | Mantenha o Terminal A aberto e avance no Terminal B |
| KeyError da AppKey | `.env` não foi carregado ou nome diverge | Pare; volte à etapa 14/15 sem mostrar o valor |
| Cert/key/CA falha | Material ou caminho inválido | Categoria mTLS/TLS; pare |
| MCP `.svc.cluster.local` não resolve e o log confirma continuação sem ferramentas | DNS interno não acessível da estação | Registre `MCP HML inacessível a partir da estação; tools=[]; startup continuou` e avance |
| MCP demora ou impede startup | Discovery não terminou | Categoria MCP/STARTUP; pare e diagnostique timeout/DNS |
| `address already in use` | Porta 8080 ocupada | Execute `ss -ltnp | grep ':8080'`; não mate o processo automaticamente |
| Erro inesperado | Falha não classificada | Pare e colete traceback sanitizado |

### Critério para avançar

O processo está ativo e o startup terminou. MCP pode ter zero ferramentas somente se o log confirmar a continuação; não chame ferramentas no primeiro Hello World.

### Se não passar

**PARE AQUI — categoria PROJETO, CONFIGURAÇÃO HML, MCP HML, APPKEY, TLS ou mTLS.** Registre a primeira exceção e últimas linhas sanitizadas. Etapas 17 a 24: `NÃO EXECUTADO — bloqueado pela etapa 16`.

## Etapa 17 — Validar liveness

### Objetivo

Confirmar que o processo HTTP local responde. Liveness não valida o Gateway nem o LLM.

### Comando

```bash
curl --max-time 10 -i http://localhost:8080/health/live
```

### Resultado esperado

HTTP 200 e corpo com estado `alive`.

### Possíveis cenários

| Resultado | Significado provável | O que fazer |
| --- | --- | --- |
| 200 | Processo vivo | Avance |
| Connection refused | Agent não escuta nessa porta | Volte ao Terminal A e pare |
| 404 | Porta ou rota incorreta | Confirme processo e endpoint; pare |
| 500 | Erro interno | Consulte o Terminal A e pare |
| Timeout | Processo travado ou destino incorreto | Consulte o Terminal A; não prossiga |

### Critério para avançar

Resposta HTTP 200 de `/health/live` no Agent local.

### Se não passar

**PARE AQUI — categoria PROJETO/STARTUP.** Registre status, corpo sanitizado e erro correlato do Terminal A. Etapas 18 a 24: `NÃO EXECUTADO — bloqueado pela etapa 17`.

## Etapa 18 — Validar readiness

### Objetivo

Confirmar que configuração e grafo foram carregados. Readiness não realiza chamada ao LLM HML.

### Comando

```bash
curl --max-time 10 -i http://localhost:8080/health/ready
```

### Resultado esperado

HTTP 200 e estado `ready`.

### Possíveis cenários

| Resultado | Significado provável | O que fazer |
| --- | --- | --- |
| 200 | Configuração/grafo prontos | Avance; `READY ≠ LLM HML comprovado` |
| 503 | Configuração ou grafo não pronto | Consulte o Terminal A e pare |
| 404 | Endpoint/versão divergente | Confirme código em execução e pare |
| 500 ou timeout | Falha interna/startup incompleto | Pare e correlacione logs |

### Critério para avançar

Resposta HTTP 200 de `/health/ready`.

### Se não passar

**PARE AQUI — categoria PROJETO/CONFIGURAÇÃO HML.** Registre status, corpo sanitizado e primeira exceção do Terminal A. Etapas 19 a 24: `NÃO EXECUTADO — bloqueado pela etapa 18`.

## Etapa 19 — Executar o primeiro `/chat` real

### Objetivo

Enviar uma mensagem simples ao FastAPI local. O Agent deve encaminhá-la pelo provider original ao Gateway e LLM HML.

### Comando

```bash
curl --max-time 90 -i -X POST http://localhost:8080/chat \
  -H 'Content-Type: application/json' \
  -d '{
    "message": "Responda somente: Hello World",
    "session_id": "hello-world-hml"
  }'
```

### Resultado esperado

HTTP 200 com `reply` textual produzido pelo modelo. A frase pode variar; a prova é o fluxo real, não correspondência textual perfeita.

### Possíveis cenários

| Resultado | Significado provável | O que fazer |
| --- | --- | --- |
| 200 com Hello World | Resposta candidata a sucesso | Vá à etapa 20 |
| 200 com texto diferente | Modelo/guardrails ajustaram a forma | Verifique se foi resposta real e vá à etapa 20 |
| 400 de guardrail | Entrada bloqueada pelo controle local | Categoria GUARDRAIL; confirme mensagem simples, não desabilite o controle |
| 500 no Agent | Exceção foi encapsulada pelo FastAPI | Consulte o Terminal A para identificar Gateway, TLS, AppKey, MCP ou código |
| Log do Gateway indica 401 | AppKey HML ausente, inválida ou não aceita | Categoria APPKEY; não mostre a chave |
| Log do Gateway indica 403 | Aplicação/modelo sem autorização | Categoria AUTORIZAÇÃO; confirmar acesso HML |
| `certificate required` | Cliente não apresentou certificado aceito | Categoria mTLS; revisar cert/key HML |
| `CERTIFICATE_VERIFY_FAILED` | Confiança no servidor falhou | Categoria TLS/CONFIANÇA HML; revisar CA sem desativar TLS |
| DNS do Gateway falha | Nome HML não resolveu | Categoria REDE HML |
| Timeout | DNS, rota, proxy, Gateway ou modelo | Isole a camada pelos logs e testes autorizados; pare |
| 429 no Gateway | Limite ou quota | Aguarde janela indicada ou acione a equipe; não conclua bug do código |
| 5xx do Gateway | Serviço upstream falhou | Registre status e mensagem sanitizada; acione a operação HML |
| MCP falhou | Integração de ferramentas separada | Para mensagem sem tools, não atribua automaticamente a falha ao LLM |

### Critério para avançar

HTTP 200 com resposta textual candidata e nenhuma evidência de mock, fallback local ou destino fora de HML.

### Se não passar

**PARE AQUI** na categoria identificada. Registre status visto pelo cliente e causa sanitizada do Terminal A. Não tente credenciais de outro ambiente. Etapas 20 a 24: `NÃO EXECUTADO — bloqueado pela etapa 19`.

## Etapa 20 — Confirmar o E2E local para HML

### Objetivo

Confirmar que o 200 veio da cadeia original completa. Evitar marcar sucesso por health, mock ou resposta local não correlacionada.

### Comando

```bash
# No Terminal A, inspecione somente os logs da requisição recém-executada.
# Registre a conclusão sanitizada, nunca headers, AppKey ou caminhos sensíveis.
```

### Resultado esperado

Evidência correlacionada de:

```text
FastAPI local
+ LangGraph original
+ provider gateway_outbound
+ Gateway HML
+ LLM HML
+ resposta devolvida pelo POST /chat
```

### Possíveis cenários

| Resultado | Significado provável | O que fazer |
| --- | --- | --- |
| Cadeia completa comprovada | Primeiro E2E local HML concluído | Marque o checkpoint B |
| Apenas HTTP 200 e origem não demonstrada | Evidência insuficiente | Mantenha NÃO DETERMINADO e pare para obter correlação segura |
| Mock/fallback detectado | Não foi chamada real | Não marque sucesso |
| Destino não HML | Violação de escopo | Pare e registre a divergência sem continuar |

### Critério para avançar

Todos os seis componentes acima estão comprovados por execução real e evidência sanitizada.

### Se não passar

**PARE AQUI — categoria GATEWAY HML/PROJETO/EVIDÊNCIA.** Registre o elo não comprovado. Etapas 21 a 24: `NÃO EXECUTADO — bloqueado pela etapa 20`.

Quando passar, registre exatamente:

```text
HELLO WORLD LOCAL → HML GATEWAY = CONFIRMADO
```

Inclua data, branch, commit, Python, contagens dos testes, health, status do `/chat`, Gateway HML e conclusão E2E, sempre sem secrets. Esse sucesso permanece válido mesmo que a Fase D não possa ser executada.

# Fase D — Agent implantado em HML

Esta fase começa somente depois do checkpoint B e apenas com acesso autorizado ao cluster HML. Snapshots Argo/Kubernetes, manifests e registros anteriores são **HISTÓRICO** até reconfirmação atual. Não use pod, IP, imagem, branch de deploy, estado Argo ou Secret histórico como evidência atual.

Se o acesso ao cluster não estiver disponível, não falhou o Hello World local. Registre em cada etapa 21 a 24:

```text
NÃO EXECUTADO — acesso HML ao cluster não disponível
```

## Etapa 21 — Confirmar contexto e pod HML atual

### Objetivo

Confirmar o cluster, namespace e recursos atuais antes de consultar o pod. A baseline contém candidatos históricos, mas eles não devem ser usados sem reconfirmação.

### Comando

```bash
oc whoami
oc config current-context
oc whoami --show-server
# Após confirmar por fonte atual o namespace HML:
oc get pods -n <NAMESPACE_HML_CONFIRMADO> \
  -o custom-columns='NAME:.metadata.name,PHASE:.status.phase,READY:.status.containerStatuses[*].ready,RESTARTS:.status.containerStatuses[*].restartCount,IMAGE:.spec.containers[*].image'
```

### Resultado esperado

Servidor/contexto inequivocamente HML e pod atual `Running`, `Ready=true`, com reinícios e imagem registrados. Confirme também, por fonte atual, repositório/revisão de deploy e estado Argo; não derive branch a partir de snapshots.

### Possíveis cenários

| Resultado | Significado provável | O que fazer |
| --- | --- | --- |
| Contexto HML e pod Ready | Implantação atual disponível | Registre imagem/revisão atuais e avance |
| Sem login/permissão | Acesso externo pendente | Marque etapas 21–24 como não executadas; preserve checkpoint B |
| Contexto DES/PRD ou ambíguo | Cluster errado | Pare sem trocar contexto automaticamente |
| Pod não Ready/reiniciando | Problema de deploy/startup | Categoria KUBERNETES HML/DEPLOY HML; pare |
| Imagem/proveniência não confirmada | Não há equivalência com o código analisado | Registre NÃO DETERMINADO e pare para confirmação |

### Critério para avançar

Cluster, namespace, pod, imagem e proveniência atuais confirmados como HML e pod pronto.

### Se não passar

**PARE AQUI — categoria KUBERNETES HML/DEPLOY HML**, ou registre falta de acesso sem invalidar B. Colete somente contexto, estados, contagens e referência de imagem não sensível. Etapas 22 a 24: `NÃO EXECUTADO — bloqueado pela etapa 21` ou `NÃO EXECUTADO — acesso HML ao cluster não disponível`.

## Etapa 22 — Validar health dentro de HML

### Objetivo

Validar liveness/readiness no pod atual e, quando aplicável, pelo Service HML atual. Não reutilize nomes ou IPs históricos sem reconfirmação.

### Comando

```bash
oc exec -n <NAMESPACE_HML_CONFIRMADO> <POD_HML_ATUAL> -- \
  curl --max-time 10 -i http://localhost:8080/health/live
oc exec -n <NAMESPACE_HML_CONFIRMADO> <POD_HML_ATUAL> -- \
  curl --max-time 10 -i http://localhost:8080/health/ready
oc get service -n <NAMESPACE_HML_CONFIRMADO>
# Depois de identificar o Service atual e confirmar sua porta:
oc exec -n <NAMESPACE_HML_CONFIRMADO> <POD_HML_ATUAL> -- \
  curl --max-time 10 -i http://<SERVICE_HML_ATUAL>:<PORTA_SERVICE_ATUAL>/health/ready
```

### Resultado esperado

Ambos os endpoints do pod e o readiness pelo Service atual respondem 200; seus ports/endpoints podem ser correlacionados ao pod. Se a imagem não tiver `curl`, não instale ferramentas no container: use método autorizado, como `oc port-forward`, e registre a limitação.

### Possíveis cenários

| Resultado | Significado provável | O que fazer |
| --- | --- | --- |
| Live e ready 200 | Aplicação implantada pronta | Avance |
| `curl` ausente | Imagem mínima | Use port-forward autorizado; não altere o pod |
| Ready não 200 | Grafo/configuração não pronta | Categoria DEPLOY HML; pare |
| Service sem endpoint pronto | Associação Service/pod falhou | Categoria KUBERNETES HML; pare |
| Sem permissão de exec/port-forward | Acesso insuficiente | Registre não executado; preserve checkpoints anteriores |

### Critério para avançar

Health do pod atual responde 200 e a aplicação/Service HML atual foi identificada sem depender de IP histórico.

### Se não passar

**PARE AQUI — categoria KUBERNETES HML/DEPLOY HML.** Registre status e eventos sanitizados, sem dump de ambiente ou Secrets. Etapas 23 e 24: `NÃO EXECUTADO — bloqueado pela etapa 22`.

## Etapa 23 — Executar `/chat` interno no Agent HML

### Objetivo

Comprovar o fluxo `pod HML → Agent → Gateway HML → LLM HML`. Use a rota FastAPI `/chat`; não use `/v1/chat` dentro do pod.

### Comando

```bash
oc exec -n <NAMESPACE_HML_CONFIRMADO> <POD_HML_ATUAL> -- \
  curl --max-time 90 -i -X POST http://localhost:8080/chat \
  -H 'Content-Type: application/json' \
  -d '{"message":"Responda somente: Hello World","session_id":"hello-world-agent-hml"}'
```

### Resultado esperado

HTTP 200 e resposta real do LLM pelo provider e Gateway HML. A correlação deve usar logs sanitizados da execução atual; Ready e imagem nominal não bastam.

### Possíveis cenários

| Resultado | Significado provável | O que fazer |
| --- | --- | --- |
| 200 e cadeia HML correlacionada | Agent implantado validado | Marque checkpoint C |
| 401/403 upstream | AppKey/autorização HML | Pare e acione responsável sem expor credencial |
| Erro TLS/mTLS | Material outbound ou confiança HML | Pare; não leia/extrate Secret para diagnosticar no chat |
| 500 | Agent encapsulou falha | Identifique a camada nos logs atuais sanitizados |
| MCP falha | Ferramentas são integração separada | Para mensagem sem tools, não confunda automaticamente com falha do LLM |
| Sem `oc exec` autorizado | Teste não executável | Registre acesso pendente; preserve checkpoint B |

### Critério para avançar

`POST /chat` dentro do Agent implantado retorna resposta real e a cadeia até Gateway/LLM HML é confirmada.

### Se não passar

**PARE AQUI — categoria DEPLOY HML, GATEWAY HML, APPKEY, AUTORIZAÇÃO, TLS ou mTLS.** Registre apenas status, camada e mensagem sanitizada. Etapa 24: `NÃO EXECUTADO — bloqueado pela etapa 23`.

Quando passar, registre:

```text
HELLO WORLD AGENT IMPLANTADO EM HML = CONFIRMADO
```

Esse checkpoint não exige a API externa.

## Etapa 24 — Validar API externa HML, opcional

### Objetivo

Validar separadamente a cadeia `cliente → API/Ingress/Route HML → Agent HML`. Execute somente se endereço, contrato, autenticação e autorização atuais estiverem confirmados para HML.

### Comando

```bash
curl --max-time 90 -i -X POST '<URL_API_HML_ATUAL_CONFIRMADA>/v1/chat' \
  -H 'Content-Type: application/json' \
  -d '{"message":"Responda somente: Hello World","session_id":"hello-world-api-hml"}'
```

Adicione somente os headers exigidos pelo contrato HML atual, sem registrá-los no runbook ou histórico compartilhado.

### Resultado esperado

HTTP 200 e resposta correlacionada ao Agent HML atual. A URL não deve ser derivada por troca textual de um host DES histórico.

### Possíveis cenários

| Resultado | Significado provável | O que fazer |
| --- | --- | --- |
| 200 e requisição chega ao Agent HML | Camada externa confirmada | Marque checkpoint D |
| 401 | Autenticação do cliente na API | Categoria API HML/AUTENTICAÇÃO |
| 403 | Autorização/política da API | Categoria API HML/AUTORIZAÇÃO |
| 404 | Base path/contrato/publicação divergente | Confirmar catálogo HML atual |
| 503 | Ingress/Route/backend indisponível | Categoria INGRESS/ROUTE HML |
| Erro mTLS do backend | Primeira cadeia externa falhou | Investigar API→Agent; isso não invalida Agent→Gateway já confirmado |
| Timeout | Cliente, rota, proxy, API ou backend | Isolar camada e parar |
| URL ou contrato atual não confirmados | Evidência insuficiente | Registre `OPCIONAL / NÃO EXECUTADA` |

### Critério para avançar

HTTP 200 pela API externa HML atual e chegada ao Agent HML comprovada. Esta etapa é opcional e não altera os checkpoints B ou C já obtidos.

### Se não passar

**PARE AQUI — categoria API HML ou INGRESS/ROUTE HML.** Registre status, camada e mensagem sanitizada. Não use host DES, Route DES ou `curl -k`.

# Registro final da jornada

Use somente `OK`, `ERRO`, `NÃO EXECUTADO — bloqueado pela etapa X`, `NÃO EXECUTADO — acesso HML ao cluster não disponível` ou, no item opcional, `OPCIONAL / NÃO EXECUTADA`.

| Checkpoint | Resultado |
| --- | --- |
| Ambiente/Git | |
| Python 3.11.9 | |
| `.venv` | |
| Dependências | |
| Unit tests | |
| Integration tests | |
| Configuração HML | |
| AppKey HML | |
| mTLS HML | |
| Agent local | |
| Local `/chat` → Gateway HML | |
| Agent implantado HML | |
| HML `/chat` → LLM | |
| API externa HML | OPCIONAL / NÃO EXECUTADA / OK / ERRO |

## Evidência mínima dos checkpoints concluídos

| Campo | Registro sem secrets |
| --- | --- |
| Data e fuso | |
| Branch e commit | |
| Python | |
| Unit tests: collected/passed/failed/errors | |
| Integration tests: collected/passed/failed/errors | |
| `/health/live` local | |
| `/health/ready` local | |
| `/chat` local | |
| Gateway HML confirmado | |
| E2E local HML | |
| Contexto/pod/imagem HML atuais, se executados | |
| `/chat` implantado HML, se executado | |
| API externa HML, se executada | |

## Se a jornada parar

Registre:

```text
HELLO WORLD HML = PENDENTE
```

Se o checkpoint B já tiver sido confirmado e somente a Fase D parar ou não for executada, não use a frase acima para invalidar B. Registre especificamente `HELLO WORLD AGENT IMPLANTADO EM HML = PENDENTE`.

| Campo | Valor |
| --- | --- |
| Primeira etapa não aprovada | |
| Categoria | |
| Sintoma sanitizado | |
| Evidência | |
| O que já foi descartado | |
| Próxima ação | |
| Depende de outra equipe? | |
| Etapas posteriores | `NÃO EXECUTADO — bloqueado pela etapa X` |

Categorias permitidas:

```text
AMBIENTE
GIT
PYTHON
VENV
DEPENDÊNCIAS
TESTES
PROJETO
CONFIGURAÇÃO HML
REDE
PROXY
TLS
mTLS
APPKEY
AUTORIZAÇÃO
GATEWAY HML
MCP HML
KUBERNETES HML
DEPLOY HML
INGRESS/ROUTE HML
API HML
```

## Divergências e limites conhecidos antes da execução

- O código atual analisado aponta para Gateway HML, modelo não produtivo esperado e API version esperada. Isso é **CONFIRMADO POR INSPEÇÃO**; a etapa 12 produzirá a confirmação da execução.
- O registro DES prova historicamente que FastAPI, LangGraph, Gateway Outbound, mTLS, LLM e `/chat` já funcionaram em conjunto. Isso é **HISTÓRICO** e não prova HML atual; nenhum endpoint, IP, certificado ou credencial DES é reutilizado.
- A Wiki histórica pede rename de pacote de template, mas o código atual já usa `plg_agent_consult_fin`. Não faça rename.
- A Wiki menciona `guardrails.external.enabled`; o código atual lê `guardrails.enabled`. O código atual prevalece.
- `.env.example` contém identificação DES e placeholders. Preserve o arquivo e não o carregue como configuração HML.
- O `pip.conf` versionado contém `trusted-host` e um caminho de CA. Não ative relaxamento TLS; a configuração efetiva do pip deve manter validação.
- A suíte `tests/integration` analisada é demonstrativa e não chama Gateway HML.
- O provider usa, nesta ordem, `TRUST_STORE_CA_PATH`, `REQUESTS_CA_BUNDLE` e trust store padrão. Uma CA prioritária configurada e inválida causa erro; não há fallback automático.
- O código captura falha de discovery MCP e tenta continuar com `tools=[]`; a execução real deve confirmar se o erro retorna em tempo hábil. `*.svc.cluster.local` é DNS interno do Kubernetes e normalmente não resolve na estação.
- Exceções durante `/chat` são apresentadas pelo Agent como HTTP 500 genérico. O status upstream real, como 401, 403 ou 429, pode aparecer apenas no log do Terminal A.
- Snapshots históricos indicam Argo/OpenShift HML, namespace, imagem e Secrets, mas nenhum desses estados é atual até ser reconfirmado na Fase D.
