# Referência detalhada — estudo local e preparação para homologação

> Material de consulta anterior à definição final do ambiente. A execução escolhida é **Pengwin/WSL + VS Code**, com objetivo limitado a **deploy HML e obtenção dos certificados**. Este arquivo contém exemplos PowerShell e testes adicionais fora desse escopo. Siga o [guia principal atualizado](PASSO_A_PASSO_PRIMEIRO_DEPLOY_HOMOLOGACAO.md) para o trabalho atual.

**Projeto:** `iaa-agent-mf-assist-financeir`  
**Ambiente atual:** máquina local de estudo, fora do ambiente corporativo  
**Ambiente de destino:** homologação corporativa  
**Revisão documental:** 18/09/2026  
**Base:** arquivos extraídos dos ZIPs pós-migração, código da aplicação e documentação corporativa disponível nesta pasta.

O objetivo atual é estudar os arquivos disponíveis localmente, identificar os ajustes e preparar sua aplicação posterior no ambiente corporativo. A migração GitLab → GitHub já foi informada como concluída; a transição tratada aqui é do material de estudo local para a execução na infraestrutura corporativa.

O guia contém duas partes: **Parte A — trabalho local agora** e **Parte B — execução futura no ambiente corporativo**. Os comandos de clone, push, CI, Argo, OpenShift e acesso ao LLM pertencem à Parte B. Os exemplos de terminal usam **PowerShell no Windows**; em Pengwin/WSL, adapte caminhos e comandos com o guia corporativo indicado adiante.

**Limite da validação:** os ZIPs foram inspecionados; não foram executados builds, alterações no GitHub, renderização dos charts privados ou consultas ao cluster durante a preparação deste documento. Host, permissões, versões de charts e situação do ambiente precisam ser confirmados nos serviços corporativos.

## Como usar este guia

- `/values.yaml` significa o arquivo na raiz do repositório indicado, não na raiz do disco Windows.
- Os ZIPs extraídos são a base de estudo atual. Não é necessário acesso ao GitHub corporativo para examiná-los.
- Falta de acesso à intranet nesta máquina não é defeito da aplicação e não impede o estudo local.
- Texto entre `<...>` deve ser substituído pelo valor real. Não execute comandos com esses marcadores ainda presentes.
- Blocos YAML parciais são para editar a seção existente. Não cole uma segunda seção com o mesmo nome.
- Em YAML, os espaços à esquerda definem a hierarquia. Use espaços, não Tab.
- `Resultado esperado` informa como verificar a etapa. `Se não acontecer` indica onde parar e corrigir.
- A AppKey, a chave privada e os certificados exportados não devem ser colocados neste documento, em commits, em issues ou em screenshots compartilhados.

### Vocabulário mínimo

| Termo | Significado neste trabalho |
|---|---|
| Repositório de código | Guarda Python, testes e instruções para construir a imagem. |
| Repositório de deploy | Guarda a configuração que será aplicada ao cluster. |
| Branch | Linha de trabalho dentro de um repositório. |
| Commit / push | Registrar alterações no Git / enviá-las ao GitHub. |
| PR / merge | Pedido de revisão / incorporação das alterações à branch de destino. |
| CI | Processo automático de testar, construir e publicar a imagem. |
| Imagem / tag | Pacote executável da aplicação / identificador de sua versão. |
| Chart / values | Modelo Helm de recursos / configurações fornecidas ao modelo. |
| Namespace | Espaço da aplicação dentro do cluster. Também aparece como projeto no OpenShift. |
| Pod | Unidade na qual o container da aplicação executa. |
| Secret | Objeto do cluster que guarda credenciais ou certificados. |
| Argo CD / sync | Ferramenta que aplica a configuração do Git / operação de sincronização. |
| Gateway / ingress | Entrada corporativa autorizada da API / roteamento até o serviço no cluster. Seus endereços podem ser diferentes. |

## 1. O que foi corrigido em relação ao roteiro anterior

O roteiro anterior era útil como visão geral, mas ainda não era seguro para execução por um iniciante. Esta versão corrige os seguintes pontos:

1. **URL de LLM em homologação não comprova a existência do cluster do agente em homologação.** É preciso confirmar os dois no OAS.
2. **A CI do ZIP não dispara em `chore/**`.** Para o código, este guia usa `fix/preparar-hml`, reconhecida pelo workflow.
3. **A documentação Python reserva versões abertas para branches auxiliares.** O primeiro build HML será feito nessa branch, sem exigir merge de `0.1.0.dev0` em `main`.
4. **O push do código pode acionar CD-des e CD-hom.** Antes do primeiro push, é preciso controlar esses jobs para que o preparo seja restrito a HML.
5. **O IDH não depende de um pod saudável para emitir certificados.** Um primeiro sync pode provisionar certificados antes de a imagem estar pronta, conforme a documentação de agentes.
6. **Existência da AppKey não significa autorização ao LLM.** É preciso vincular o agente ao catálogo e autorizar o consumo da API provedora.
7. **`0.1.0-SNAPSHOT` pode ser uma tag válida.** O erro é usá-la sem comprovar a publicação; não é obrigatório eliminar esse texto.
8. **Readiness e testes de exemplo não comprovam integração com o LLM.** O teste funcional pelo gateway continua necessário.
9. **Criar `.env` não carrega as variáveis automaticamente.** A etapa opcional de execução numa estação corporativa usa explicitamente `uvicorn --env-file`.
10. **Os YAMLs do README são referências.** As dependências privadas e os recursos gerados devem ser conferidos antes do merge.

## Parte A — estudar e preparar neste ambiente local

### A1. Localizar o material recebido

Trabalhamos com estas pastas extraídas, que não são clones Git:

```text
C:\Users\manue\.0_PROG\UAN\AGENT-OPS\
├── iaa-agent-mf-assist-financeir-main\
│   └── iaa-agent-mf-assist-financeir-main\
├── deploy-iaa-agent-mf-assist-financeir-cloud-producao\
├── ESTEIRA_AGENTS_OPS\
├── DOCUMENTACAO_GERAL\
└── AMBIENTE_PENGWIN\
```

O primeiro diretório contém o código. O segundo contém a configuração antiga de deploy de produção. Os demais contêm documentação de apoio. A pasta chamada `cloud-producao` não é um cluster de produção nesta máquina; é apenas a referência exportada.

**Como começar:** abra essas pastas no editor de sua preferência e consulte os arquivos da tabela A2. Não é preciso executar `git clone`, criar credenciais ou acessar o Argo nesta fase.

### A2. Estudar o que existe e registrar o que precisará mudar

Os caminhos abaixo são relativos à raiz de cada pasta extraída.

| Base local | Arquivo e campo | O que foi encontrado | Preparação para o ambiente corporativo |
|---|---|---|---|
| Código | `aic.json → pipeline.versaoPython` | `3.8` | Propor `3.11`, conforme a documentação de agentes e o Dockerfile. |
| Código | `aic.json → pipeline.publicarPacoteEImagem` | `false` | Conferir a flag na esteira e preparar a publicação da imagem. |
| Código | `.github/workflows/ci.yaml` | Gatilhos `fix/`, `feat/`, `feature/`, `main`; jobs CD DES e HML | Planejar branch reconhecida e impedir autodeploy indesejado antes do primeiro push corporativo. |
| Código | `iaa_agent_mf_assist_financeir/__init__.py` | Versão `0.1.0.dev0` | Preservar a distinção entre versão Python e tag da imagem; a esteira confirmará a tag publicada. |
| Código | `agent_config.yaml → llm.gateway_outbound.base_url` | URL `.hm.bb.com.br` | Manter como referência HML; sua autorização/disponibilidade serão confirmadas lá. |
| Código | `agent_config.yaml → mcp.servers` | MCP em `localhost:9000` | Decidir se o primeiro teste dispensa MCP ou exige endpoint corporativo real. |
| Código | `requirements.txt`, `setup.py`, `tests/` | Dependências e testes, com integração apenas de exemplo | Preparar os testes; não confundir aprovação de testes locais com integração corporativa. |
| Código | `pip.conf` e `Dockerfile` | Índice de pacotes e imagem-base da intranet | Registrar dependência da rede corporativa; não usar sua indisponibilidade local para reprovar o projeto. |
| Deploy | `Chart.yaml` | `bb-aplic`, alias antigo e ausência de dependência IDH | Comparar com o modelo Helm no README do código e preparar a atualização. |
| Deploy | `values.yaml → deployment.containers.tag` sob a raiz antiga | `0.1.0-SNAPSHOT`, linha 40 do ZIP | Localizar o campo agora; só preencher a versão definitiva após publicação corporativa. |
| Deploy | `values.yaml` | Hosts antigos, PKI `prd`, recursos desabilitados | Preparar adaptação HML com campos desconhecidos explicitamente pendentes. |
| Deploy | `.github/workflows/cd.yaml` e `cd.yml` | Dois workflows com filtros diferentes | Registrar a duplicidade para resolução conforme o modelo corporativo. |

**Exemplo de leitura da tag:** abra o `values.yaml` da pasta de deploy extraída, pressione `Ctrl+F` e procure `0.1.0-SNAPSHOT`. O endereço interno é `dia-agent-azure-template-python → deployment → containers → tag`. Na proposta corrigida, a raiz passará a `iaa-agent-mf-assist-financeir`. Isso não significa que exista uma imagem com essa tag: só observamos o valor do arquivo.

### A3. Separar validação local de validação corporativa

| Podemos avaliar aqui | Só confirmar no ambiente corporativo |
|---|---|
| Estrutura dos arquivos e caminhos | Estado atual das branches oficiais e permissões |
| Campos conflitantes, placeholders e diferenças entre código e README | Schema vigente e versões dos charts privados |
| Sintaxe de JSON/YAML e lógica dos workflows | Execução real da CI, publicação e digest da imagem |
| Testes isolados que usem dependências disponíveis e respostas simuladas | Autorização da AppKey e chamada real ao LLM |
| Preparação de configurações HML sem credenciais | Host, namespace, quotas, rede, Argo e operadores |
| Documentação e proposta de alterações | Emissão e validade dos certificados corporativos |

Uma simulação local de LLM/MCP pode ajudar a testar o código, mas deve ser identificada como simulação. Não substitui a integração HML. Não é necessário trazer AppKeys ou chaves privadas para a máquina de estudo.

**Estado desta revisão:** análise de arquivos e documentação realizada; links e sintaxe dos exemplos do guia conferidos. Não foram executados testes da aplicação, build Docker ou deploy corporativo. As propostas descritas neste documento ainda não foram aplicadas aos arquivos originais.

### A4. Preparar o material a levar

O material de transição deve conter:

1. Este guia, com a lista de arquivos a alterar e a ordem de execução.
2. Uma proposta de alterações revisável, quando preparada, identificando cada arquivo e o motivo. Pode ser uma comparação antes/depois ou um patch, conforme o meio de transferência autorizado.
3. Registro do que foi efetivamente testado aqui e do que ficou pendente.
4. Lista de dados que serão preenchidos no ambiente corporativo: host, namespace, custodiante, versão de chart, tag da imagem, autorizações e URLs de catálogo.

Não use um arquivo com `<HOST_INGRESS_HML>` ou `<TAG_PUBLICADA>` como configuração pronta para deploy. Esses marcadores são aceitáveis na proposta local, mas devem ser resolvidos antes da publicação corporativa.

Este documento é o roteiro e a avaliação. Ele não afirma que um pacote de código corrigido ou um patch já foi produzido. Os ZIPs originais continuam sendo a referência para comparação.

### A5. Aplicar a preparação quando chegar ao ambiente corporativo

Na estação corporativa, use o meio de transferência autorizado para levar o guia e a proposta revisada. Então:

1. Clone os repositórios oficiais lá.
2. Compare a versão atual com os ZIPs que estudamos; eles podem ter ficado desatualizados.
3. Aplique somente as alterações ainda necessárias, preservando as mudanças do time.
4. Substitua os campos pendentes pelos dados oficiais.
5. Execute os testes e a esteira corporativa.
6. Siga os passos de deploy HML da Parte B.

Não substitua um repositório corporativo inteiro pela pasta do ZIP de estudo. O alvo é incorporar ajustes revisados à versão oficial atual.

Para a preparação de Linux/WSL na estação corporativa, consulte também [Guia Pengwin/WSL corporativo](AMBIENTE_PENGWIN/guia-pengwin-wsl-corporativo.md). Os comandos PowerShell deste documento não devem ser colados literalmente em um terminal Bash.

**A fase atual termina com entendimento dos arquivos, proposta de ajustes e pendências documentadas. Acesso corporativo é requisito da fase seguinte, não do estudo local.**

## Parte B — roteiro para executar depois, no ambiente corporativo

Todas as etapas 2 a 22 abaixo são instruções de execução futura na estação/rede corporativa autorizada. Sua presença neste arquivo serve para preparar a transição. Não implica que GitHub corporativo, intranet, registry, Argo ou OpenShift estejam acessíveis a partir da máquina de estudo.

## 2. Confirmar os dados de homologação

**Onde:** Tech.bb → instância OAS da aplicação → recursos/links associados. Os nomes dos menus podem variar.

Preencha esta ficha com informações não sensíveis:

| Informação | Onde obter | Valor a registrar |
|---|---|---|
| Repositório do código | Oferta de migração / GitHub | URL oficial de `iaa-agent-mf-assist-financeir` |
| Repositório do deploy | Oferta de migração / GitHub | URL oficial de `deploy-iaa-agent-mf-assist-financeir` |
| Branch de deploy HML | Seletor de branches do deploy | `cloud/homologacao` |
| Aplicação no Argo CD | Link HML da instância OAS | Nome e URL |
| Console OpenShift HML | Link HML da instância OAS | URL |
| Namespace HML | Instância OAS / aplicação Argo | Nome exato |
| Host do ingress HML | Configuração oficial da instância | Host sem `https://` e sem caminho |
| URL pública/interna do agente pelo gateway | Catálogo de IA/API em HML | URL completa, incluindo o caminho do chat |
| Custodiante do certificado | Responsável pelo projeto | Matrícula real |
| AppKey e autorização | Catálogo de Aplicações / equipe provedora | Registrar apenas se foram obtidas/aprovadas |

**Convenções que não devem ser confundidas:**

| Local | Valor HML |
|---|---|
| Branch do deploy | `cloud/homologacao` |
| `DEPLOY_ENV` | `homol` |
| `bbcert.dadosCertificado.ambientePKI` | `hml` |
| Outbound encontrado no ZIP | `https://llms-agentes-ia.outbound.api.hm.bb.com.br/v1` |

**Resultado esperado:** existem recursos HML do agente e acesso aos dois repositórios, Actions, Argo e namespace OpenShift.

**Se não acontecer:** solicitar o provisionamento/acesso HML à equipe da oferta. Não deduzir o endereço do console trocando letras de um host de desenvolvimento ou produção. Se a governança exigir promoção a partir de desenvolvimento, resolver essa condição com a esteira antes de seguir; ter um endpoint LLM HML não dispensa essa regra.

## 3. Localizar os arquivos e definir os clones de trabalho

### 3.1 ZIPs usados como referência

Código:

```text
C:\Users\manue\.0_PROG\UAN\AGENT-OPS\iaa-agent-mf-assist-financeir-main\iaa-agent-mf-assist-financeir-main
```

Deploy de produção usado apenas para comparação:

```text
C:\Users\manue\.0_PROG\UAN\AGENT-OPS\deploy-iaa-agent-mf-assist-financeir-cloud-producao
```

Mapa rápido dos arquivos:

| Repositório | Arquivo | Para que será usado |
|---|---|---|
| Código | `aic.json` | Python e publicação da imagem |
| Código | `.github/workflows/ci.yaml` | Gatilhos de CI e jobs de autodeploy |
| Código | `iaa_agent_mf_assist_financeir/__init__.py` | Versão do pacote Python |
| Código | `agent_config.yaml` | URL/modelo LLM e servidores MCP |
| Código | `requirements.txt` e `setup.py` | Dependências e instalação para testes |
| Código | `README.md`, seção “Configuração Inicial do Helm Chart” | Modelo de Chart e values |
| Deploy | `Chart.yaml` | Dependências do Helm |
| Deploy | `values.yaml` | Imagem, Service, Deployment, certificados e ingress |
| Deploy | `.github/workflows/cd.yaml` e `cd.yml` | Workflows de deploy a revisar |

### 3.2 Caminhos dos clones

Na estação corporativa, escolha uma pasta de trabalho e use dois clones separados. Os caminhos abaixo são apenas exemplos no mesmo formato Windows do material de estudo; não indicam clones existentes aqui nem obrigam a usar esse usuário/caminho lá:

```text
C:\Users\manue\.0_PROG\UAN\AGENT-OPS\codigo-iaa-hml
C:\Users\manue\.0_PROG\UAN\AGENT-OPS\deploy-iaa-hml
```

Adapte esses dois caminhos em todos os comandos à máquina corporativa. Se os clones já existem lá, não é necessário clonar novamente. Em Pengwin/WSL, adapte também a sintaxe dos comandos.

Caso ainda precise criar os clones, na pasta `AGENT-OPS` execute, usando as URLs confirmadas na etapa 2:

```powershell
git clone --branch main <URL_OFICIAL_CODIGO> codigo-iaa-hml
git clone --branch cloud/homologacao <URL_OFICIAL_DEPLOY> deploy-iaa-hml
```

Não coloque senha ou token na URL. Faça a autenticação corporativa/SSO quando solicitada.

## 4. Conferir o destino do Argo antes de enviar alterações

**Onde:** Argo CD HML → aplicação do agente → detalhes da aplicação.

Confira, com a equipe da esteira se necessário:

- repositório de origem: deploy oficial do agente;
- revisão/branch: `cloud/homologacao`;
- cluster e namespace: os da ficha HML;
- se o sync é automático ou manual;
- se há aprovação/janela de liberação para homologação.

**Resultado esperado:** sabe-se qual alteração no Git poderá aplicar recursos no cluster. Um PR também pode executar Actions: no ZIP, `cd.yml` possui gatilho para abertura de PR em HML. Não assuma que somente o merge tem efeitos sem conferir o workflow reutilizável corporativo.

Se a aplicação já estiver funcionando, este deixa de ser um primeiro deploy vazio: preserve a configuração existente e revise o impacto com o responsável. Não desabilite recursos já ativos para seguir este exemplo.

## 5. Obter a AppKey e autorizar o consumo do LLM

**Onde:** Catálogo de IA / Catálogo de Aplicações / API provedora do LLM.

1. Localize o cadastro do agente e confirme sua vinculação ao Catálogo de IA.
2. Obtenha a AppKey pelo mecanismo corporativo de credenciais.
3. Solicite/confirme a autorização dessa aplicação para consumir o LLM em HML.
4. Confirme o modelo e o endpoint disponibilizados para ela.

A documentação local de agentes identifica a API **Azure AI Foundry – LLMS AGENTES IA (17703978)** e a equipe **IA Generativa Avançada** para a autorização. Confira se esses dados permanecem vigentes no catálogo interno.

A AppKey é usada em `GATEWAY_OUTBOUND_GW_APP_KEY`. O sucesso desta etapa é ter a credencial **e** a autorização; não registrar o valor em texto compartilhado.

## 6. Preparar a branch do código e conter o autodeploy

**Terminal:** PowerShell. **Repositório:** código.

```powershell
Set-Location 'C:\Users\manue\.0_PROG\UAN\AGENT-OPS\codigo-iaa-hml'
git status -sb
git switch main
git pull --ff-only
git switch -c fix/preparar-hml
```

Se `git status` mostrar arquivos modificados antes dessa operação, preserve-os e esclareça sua origem. Se a branch já existe, use `git switch fix/preparar-hml`.

**Por que `fix/`:** o workflow do ZIP aceita `main`, `fix/**`, `feat/**` e `feature/**`. Ele não dispara automaticamente em `chore/**` nem em `develop`.

### 6.1 Antes do primeiro push, abrir `.github/workflows/ci.yaml`

Na raiz do clone, abra a pasta `.github`, depois `workflows` e o arquivo `ci.yaml` no editor.

O arquivo contém três jobs: `CI`, `CD-des` e `CD-hom`. O job HML também depende da flag `autodeploy`; ativá-la não garante que desenvolvimento fique desligado.

Para este roteiro usar build separado do deploy, a alteração temporária proposta na branch é substituir **somente o `if:` de cada um dos dois jobs CD** por:

```yaml
    if: ${{ false }} # primeiro build HML: deploy será feito pelo PR do repositório deploy
```

Deixe o job `CI` e os demais campos dos jobs intactos. Não crie um segundo `if:`. Submeta essa alteração à revisão normal da equipe. Se a organização controlar isso por configuração central, peça à esteira o equivalente “publicar imagem sem autodeploy DES/HML” em vez de alterar um workflow protegido.

**Resultado esperado:** a primeira execução faz CI; `CD-des` e `CD-hom` ficam `Skipped` (não executados). Não restaure o CD de desenvolvimento numa jornada exclusivamente HML. A configuração permanente será decidida na revisão do workflow.

## 7. Corrigir o código para o primeiro build

### 7.1 `aic.json`: Python

**Arquivo:** `codigo-iaa-hml\aic.json`, na raiz, ao lado do `Dockerfile`.

Troque:

```json
"versaoPython": "3.8"
```

por:

```json
"versaoPython": "3.11"
```

A documentação específica de agentes confirma o problema pós-migração que regride esse campo para 3.8. O `setup.py` exige Python >= 3.11 e o Dockerfile usa uma imagem 3.11.6.

### 7.2 `aic.json`: publicação

No mesmo arquivo há:

```json
"publicarPacoteEImagem": false
```

Ajuste para `true` conforme a configuração de publicação exigida pelo workflow corporativo `@v2`. Confirme a semântica atual dessa flag na esteira: o nome e o arquivo isolados não provam quais etapas serão executadas. A evidência final será a etapa de publicação Docker concluída e a imagem disponível no registry.

Preserve os demais campos. As verificações obrigatórias de segurança/qualidade são as da esteira vigente; não as dispense porque há flags antigas desabilitadas no ZIP.

### 7.3 `__init__.py`: versão aberta

**Arquivo:** `codigo-iaa-hml\iaa_agent_mf_assist_financeir\__init__.py`.

No ZIP:

```python
__version__ = '0.1.0.dev0'
```

Use uma versão aberta aceita e ainda publicável na branch auxiliar. Se a versão já foi usada e a esteira recusar republicação, incremente-a conforme a convenção do projeto; não sobrescreva um artefato publicado por tentativa.

A documentação local da esteira reserva versões fechadas à `main` e abertas às branches auxiliares. Por isso **não é necessário fazer merge deste código em `main` antes de testar HML**. A integração posterior seguirá a estratégia de branches e versões do projeto.

### 7.4 `agent_config.yaml`: outbound e ferramentas

**Arquivo:** `codigo-iaa-hml\agent_config.yaml`.

Mantenha o bloco abaixo se confirmado no catálogo:

```yaml
llm:
  provider: "gateway_outbound"
  gateway_outbound:
    base_url: "https://llms-agentes-ia.outbound.api.hm.bb.com.br/v1"
    model: "cambio-non-prod-gpt4o"
    api_version: "2024-12-01-preview"
    max_tokens: 4096
```

O ZIP também aponta um MCP para `http://localhost:9000/mcp`. Dentro do pod, `localhost` é o próprio pod, não o computador do desenvolvedor.

Para um primeiro teste somente do agente com LLM, sem MCP provisionado, deixe:

```yaml
mcp:
  servers: []
```

Se o teste precisa do MCP, configure seu endpoint HML autorizado e valide a conectividade. RAG e guardrails externos já estão desabilitados no ZIP; isso delimita o teste técnico inicial e não equivale a uma homologação funcional completa do produto.

## 8. Instalar dependências e executar testes

**Terminal:** PowerShell, na pasta `codigo-iaa-hml`.

```powershell
py -3.11 --version
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m pip install -e ".[unit,integration]"
.\.venv\Scripts\python.exe -m pip check
.\.venv\Scripts\python.exe -m pytest -q
```

Os comandos usam o Python do ambiente virtual diretamente; não precisam de `Activate.ps1`.

Instalamos `requirements.txt` **e** os extras de teste porque o ZIP tem diferenças entre as dependências desse arquivo e as do `setup.py`. Resolver inconsistências encontradas é necessário antes de publicar a imagem. A CI e o build Docker também devem passar.

**Resultado esperado:** comandos sem erro, `pip check` sem incompatibilidades e testes aprovados.

**Se não acontecer:** se Python 3.11 não existir, instale pelo canal corporativo; se o download falhar, confira VPN/proxy/CA e o índice de pacotes aprovado. Não desative TLS para contornar o erro. Falha em teste deve ser corrigida antes de prosseguir.

O teste encontrado em `tests/integration/test_dummy.py` é apenas um exemplo de soma. Sua aprovação não valida o gateway, a AppKey, os certificados ou o LLM real.

## 9. Publicar o código da branch e identificar a imagem

Ainda no clone do código:

```powershell
git diff --check
git diff
git add aic.json agent_config.yaml .github/workflows/ci.yaml
git diff --cached
git commit -m "fix: preparar build isolado para homologacao"
git push -u origin fix/preparar-hml
```

Se modificou a versão, inclua também `iaa_agent_mf_assist_financeir/__init__.py` no commit. Revise todos os arquivos listados antes de enviar. No VS Code, a aba Controle do Código-Fonte mostra o mesmo diff.

**Onde acompanhar:** GitHub → repositório do código → **Actions** → **Esteira de Build Python** → execução da branch `fix/preparar-hml`.

Confirme:

1. O SHA (identificador do commit) corresponde ao que você enviou.
2. Testes, build e verificações exigidas passaram.
3. A publicação Docker terminou com sucesso.
4. `CD-des` e `CD-hom` estão `Skipped` no fluxo separado deste guia.
5. O resumo/log não indica publicação ignorada.

Registre **sem credenciais**: URL da execução, SHA, caminho completo da imagem no registry, tag e, se disponibilizado, digest.

O workflow usa `needs.CI.outputs.versao_projeto`; esse texto é uma expressão, não a tag pronta. Procure a versão concreta no resumo ou no log de publicação Docker. Se não aparecer, consulte o artefato no registry com a equipe da esteira. Nunca deduza a conversão `0.1.0.dev0` → `0.1.0-SNAPSHOT`.

**Resultado esperado:** imagem da execução correta acessível no registry. Abertura de PR do código pode ser feita para revisão, mas não exige merge em `main` para este primeiro build HML.

## 10. Preparar a branch de deploy HML

**Terminal:** PowerShell. **Repositório:** deploy.

```powershell
Set-Location 'C:\Users\manue\.0_PROG\UAN\AGENT-OPS\deploy-iaa-hml'
git status -sb
git switch cloud/homologacao
git pull --ff-only
git switch -c chore/preparar-primeiro-deploy-hml
```

Aqui `chore/` é aceitável como branch de edição: a aplicação será publicada por meio do fluxo de PR/branch `cloud/homologacao`, não pela CI Python dessa branch.

Abra a pasta do clone no editor. Todos os arquivos das próximas etapas pertencem a `deploy-iaa-hml`.

## 11. Corrigir `Chart.yaml`

**Onde:** raiz do clone de deploy → `Chart.yaml`.

O ZIP contém `bb-aplic` e alias antigo. O modelo de agente no README do código contém as dependências abaixo:

```yaml
apiVersion: v2
appVersion: "0.0.1"
description: Chart do projeto iaa-agent-mf-assist-financeir
name: chart-iaa-agent-mf-assist-financeir
version: 0.0.1
dependencies:
  - name: dia-chart-agent
    version: 1.0.0
    alias: iaa-agent-mf-assist-financeir
    repository: https://charts-repo.nuvem.bb.com.br/pre-prd/bb/dia
  - name: bbcert
    version: ~1.0.7
    repository: https://charts-repo.nuvem.bb.com.br/pre-prd/bb/psc
  - name: idh-operator-chart
    version: 0.0.13
    repository: https://charts-repo.nuvem.bb.com.br/pre-prd/bb/idh
```

Essas são as versões **do README fornecido**, não versões atuais verificadas no registry privado. Confirme seu uso com a esteira e resolva as dependências na etapa 15.

O projeto é um agente: não substitua por `dia-chart-mcp`, usado para servidores MCP.

Não copie para cá a tag Docker: `version` e `appVersion` do chart não são o campo que seleciona a imagem do container.

## 12. Preparar `values.yaml` com o modelo correto

### 12.1 Como copiar o modelo sem perder a hierarquia

1. Abra o `README.md` do **clone de código**.
2. Pressione `Ctrl+F` e pesquise `Configuração Inicial do Helm Chart`.
3. Localize o subtítulo `values.yaml` logo após o exemplo de `Chart.yaml`.
4. Copie o conteúdo inteiro do bloco YAML, sem as linhas de três crases.
5. No **clone do deploy**, compare com o `values.yaml` HML atual. Para o template inicial sem customizações, use esse bloco como base do arquivo. Se já houver configurações do time, preserve-as e revise as diferenças.
6. Aplique todas as adaptações abaixo antes de salvar o commit. O exemplo do README é de produção e não deve ser publicado sem essas adaptações.

O arquivo deve ter **uma única ocorrência** da raiz `iaa-agent-mf-assist-financeir:`. As seções `dnsingress:`, `idhmtls:` e `bbcert:` ficam na coluna inicial, fora dessa raiz.

### 12.2 Onde fica exatamente a tag

No ZIP antigo, `values.yaml`, linha 40:

```yaml
dia-agent-azure-template-python:
  deployment:
    containers:
      tag: "0.1.0-SNAPSHOT"
```

No modelo corrigido, procure a mesma sequência com a raiz nova:

```yaml
iaa-agent-mf-assist-financeir:
  deployment:
    containers:
      tag: "<TAG_PUBLICADA>"
```

Substitua `<TAG_PUBLICADA>` pela tag comprovada na etapa 9. Se ela for mesmo `0.1.0-SNAPSHOT`, mantenha esse valor. Não é necessário trocar só porque coincide com o exemplo.

Não altere por engano `deploymentCanario.containers.tag`, `initContainer.tag` ou `curio.tag`.

### 12.3 Service e Deployment

Na raiz da aplicação, confirme:

```yaml
iaa-agent-mf-assist-financeir:
  service:
    name: iaa-agent-mf-assist-financeir
    enable: true
    type: ClusterIP
    ports:
      - name: http
        port: 80
        targetPort: 8080
  deployment:
    enable: true
    imagePullSecrets: atfregistry
    replicaCount: 1
```

Esse trecho mostra apenas essas seções; mantenha `containers` e as demais configurações do modelo. A secret `atfregistry` é usada para baixar a imagem; confirme sua existência/provisionamento pela plataforma no namespace HML, sem copiar credenciais de outro ambiente.

Os recursos `requests`/`limits` do modelo são ponto de partida, não dimensionamento aprovado. Confira limites de CPU/memória e quotas HML com o time; preserve as probes `/health/live` e `/health/ready`, porta 8080.

### 12.4 Variáveis e secret `env`

**Caminho interno:** `iaa-agent-mf-assist-financeir → deployment → containers → environments`.

Dentro da lista existente, mantenha/ajuste cada entrada abaixo; não duplique a variável:

```yaml
        - name: KEY_STORE_CERT_PATH
          value: /app/certs/tls.crt
        - name: KEY_STORE_KEY_PATH
          value: /app/certs/tls.key
        - name: TRUST_STORE_CA_PATH
          value: /app/certs/ca.crt
        - name: REQUESTS_CA_BUNDLE
          value: /etc/pki/tls/certs/ca-bundle.crt
        - name: SSL_CERT_FILE
          value: /etc/pki/tls/certs/ca-bundle.crt
        - name: SERVICE_NAME
          value: iaa-agent-mf-assist-financeir
        - name: DEPLOY_ENV
          value: homol
```

O caminho do bundle do sistema vem do README; confirme que existe na imagem final. Não use esses caminhos Linux no Windows.

Se mantiver `MP_OPENAPI_SERVERS`, ajuste seu valor para `https://<HOST_INGRESS_HML>`. Preserve as configurações de telemetria do modelo conforme a plataforma. `ENABLE_SWAGGER=false` no chart, sozinho, não garante que `/docs` esteja desabilitado: o código deste ZIP configura essa rota diretamente.

**No mesmo nível de `environments`, dentro de `containers`:**

```yaml
      envFrom:
        - secretRef:
            name: env
```

A AppKey não aparece no YAML. `env` é apenas o nome da Secret que fornecerá seu valor ao processo.

### 12.5 Montagem de certificados

**Dentro de `deployment.containers`:**

```yaml
      volumeMounts:
        - name: tls-certs-volume
          mountPath: /app/certs
          readOnly: true
```

**Dentro de `deployment`, ao lado de `containers`:**

```yaml
    volumes:
      - name: tls-certs-volume
        secret:
          secretName: idh-mtls
          items:
            - key: tls.crt
              path: tls.crt
            - key: tls.key
              path: tls.key
            - key: ca.crt
              path: ca.crt
```

O certificado cliente é `tls.crt`, a chave é `tls.key` e a CA é `ca.crt`. A tabela de variáveis da documentação geral de agentes contém esses mapeamentos trocados; este guia segue o código e o README do projeto.

### 12.6 Ingress e DNS: preencher o host certo

**Dentro da raiz `iaa-agent-mf-assist-financeir`:**

```yaml
  ingress:
    enable: true
    hostname: "<HOST_INGRESS_HML>"
    servicePort: 80
    annotations:
      kubernetes.io/ingress.class: ingress-interno-iib
      haproxy.org/timeout-connect: "30s"
      haproxy.org/timeout-server: "1800s"
      haproxy.org/timeout-client: "1800s"
    paths:
      - path: "/"
        backend:
          serviceName: iaa-agent-mf-assist-financeir
          servicePort: 80
    tls:
      - secretName: iaa-agent-mf-assist-financeir-tls
        hosts:
          - "<HOST_INGRESS_HML>"
```

**Na coluna inicial, fora da raiz da aplicação:**

```yaml
dnsingress:
  urls:
    - hostname: "<HOST_INGRESS_HML>"
      ingressClass: ingress-interno-iib
```

O exemplo segue o README. A classe e o formato de `paths` devem ser aceitos pelo chart homologado. O README usa `dnsingress` mesmo sem declará-lo diretamente no `Chart.yaml`; confirme na renderização se ele é fornecido pelo chart de agente. Se não aparecer recurso equivalente, resolver a dependência com a esteira antes do merge.

Não use a URL do LLM como hostname do agente. Não deduza o hostname de HML a partir do ZIP de produção.

### 12.7 IDH e BBCert

Na coluna inicial do `values.yaml`:

```yaml
idhmtls:
  enabled: true
  renewTime: 365
  secretName: idh-mtls
  nomesAlternativos: []

bbcert:
  enabled: true
  custodianteCertificado:
    matriculaBB: "<MATRICULA_CUSTODIANTE>"
  dadosCertificado:
    ambientePKI: hml
    commomName: "<HOST_INGRESS_HML>"
    alternativesNames: []
    ttl: 365
    secretNameToExport: iaa-agent-mf-assist-financeir-tls
  autoRenew:
    enabled: true
    qtDaysBeforeCertExpirion: 30
```

`commomName` está escrito assim no modelo corporativo: não “corrija” a grafia para `commonName` sem consultar o schema. Só acrescente SANs/nomes alternativos se a plataforma solicitar os domínios adicionais; não solicite wildcard por hábito.

A dependência se chama `idh-operator-chart`, mas o README apresenta `idhmtls` como chave no values. **A renderização deve demonstrar que esse bloco gerou o recurso IDH esperado.** Se o chart ignorar a chave, confirme o schema/alias com a esteira. Escrever `enabled: true` não comprova que o operador recebeu uma solicitação.

## 13. Criar a Secret operacional no namespace HML

**Onde:** console OpenShift HML → selecionar o projeto/namespace da ficha → **Workloads → Secrets** (ou menu **Secrets**, conforme a versão).

1. Procure `env` antes de criar.
2. Se existe, peça ao responsável para confirmar as chaves; não sobrescreva uma Secret existente sem revisar seu uso.
3. Se não existe, escolha **Create → Key/value secret**; o nome deve ser `env`.
4. Adicione a chave `GATEWAY_OUTBOUND_GW_APP_KEY` e o valor autorizado da etapa 5.
5. Salve e confira apenas o nome e a presença da chave.

Se a instituição usa um gerenciador externo de secrets, faça esse cadastro pelo processo corporativo que materializa `env` no namespace. Se falta permissão ou o namespace ainda não existe, solicite o provisionamento à plataforma; não tente criar no namespace de outro ambiente.

`RAG_CLIENT_ID`, `GUARDRAIL_EXTERNAL_CLIENT_ID` e `APPLICATION_INSIGHTS_CONNECTION_STRING` só entram se suas integrações estiverem em uso. Não crie credenciais fictícias.

| Secret | Origem | Quando precisa estar pronta |
|---|---|---|
| `env` | Processo corporativo de credenciais | Antes de iniciar o container que a referencia |
| `atfregistry` | Plataforma de registry/cluster | Antes de o pod baixar a imagem |
| `idh-mtls` | Operador IDH a partir dos manifests | Pode surgir durante o primeiro sync; deve existir antes da montagem pelo pod |
| `iaa-agent-mf-assist-financeir-tls` | Operador BBCert | Antes de o ingress oferecer o certificado esperado |

## 14. Conferir os workflows de deploy

**Onde:** clone do deploy → `.github/workflows`.

No PowerShell dessa pasta de repositório:

```powershell
Get-ChildItem .github\workflows
git diff --no-index .github/workflows/cd.yaml .github/workflows/cd.yml
```

Execute a comparação apenas se os dois existirem. O código de saída 1 desse `git diff` significa que existem diferenças.

No ZIP, ambos usam o mesmo workflow corporativo, mas têm filtros diferentes de push/PR. Não são cópias idênticas. Solicite à esteira qual revisão deve ser mantida e registre a remoção apenas do arquivo redundante aprovado.

O workflow efetivo deve reconhecer `cloud/homologacao`. Confira também o tratamento de evento `pull_request` no workflow reutilizável: não foi inspecionado no ambiente privado nesta revisão. Abertura/reabertura de PR pode iniciar a Action antes do merge.

**Resultado esperado:** um único fluxo efetivo de deploy e conhecimento do que ocorre no PR e no merge. Não edite as regras corporativas por tentativa.

## 15. Validar os arquivos antes de abrir o PR

### 15.1 Inspeção simples

Na raiz do clone do deploy:

```powershell
git diff --check
git diff --stat
git diff
Select-String -Path Chart.yaml,values.yaml -Pattern 'agent-azure-template|dia-agent-azure|<[^>]+>'
Select-String -Path values.yaml -Pattern 'ambientePKI|DEPLOY_ENV|tag:|hostname:|secretName:'
```

Na primeira pesquisa, não devem sobrar nomes antigos nem marcadores `<...>` usados como valores. A segunda pesquisa ajuda a conferir os valores; encontrar uma tag auxiliar diferente da aplicação é normal.

### 15.2 Validação Helm: necessária com apoio da esteira

Peça ao responsável técnico para executar ou fornecer a prévia de manifests na ferramenta corporativa. Se Helm e acesso aos repositórios privados já estiverem disponíveis, na raiz do deploy:

```powershell
helm version
helm dependency update .
helm lint . -f values.yaml
helm template iaa-agent-mf-assist-financeir . -f values.yaml --namespace <NAMESPACE_HML>
```

Use o namespace real. `helm dependency update` pode criar `Chart.lock` e baixar `charts/`: o time deve confirmar a política de versionamento desses arquivos antes de incluí-los no commit.

Verifique na saída renderizada, sem valores sensíveis:

- Service e Deployment com o nome correto, porta 8080 do container e porta 80 do serviço;
- imagem com repositório/tag exatos da etapa 9, não apenas uma string de tag coincidente;
- referência a `env`, `atfregistry` e montagem de `idh-mtls`;
- solicitação IDH e BBCert HML, incluindo o nome da Secret de saída;
- Ingress com o host correto e Secret TLS correta;
- DNSIngress ou mecanismo de DNS equivalente esperado pela plataforma;
- classe de ingress, recursos/quotas e conectividade de saída para o LLM HML.

**Se IDH ou DNS não aparecerem, não aprove o deploy apenas porque `helm lint` passou.** O chart pode ignorar valores que não entende. A correção exige o schema real da dependência.

`helm template` é uma conferência local: não valida por si só permissões, operadores instalados ou todas as regras do cluster. A checagem corporativa HML continua necessária. [Referência oficial do Helm](https://helm.sh/docs/helm/helm_template/).

### 15.3 E se o objetivo imediato for só obter os certificados?

A documentação de agentes diz explicitamente que a emissão IDH **não exige imagem válida ou finalizada**. É possível aplicar antes os recursos de certificados, sem esperar os testes reais do LLM.

Esse é um caminho alternativo ao deploy completo das etapas anteriores: prepare Chart/IDH/BBCert, valide com a esteira que os recursos de certificados continuam renderizando com `service.enable: false`, `deployment.enable: false` e ingress desabilitado, e aplique esse PR de infraestrutura primeiro. Confirme a emissão em OpenShift. Depois publique um segundo PR habilitando a aplicação com a imagem válida e `env` pronta.

Não presuma que essa separação funciona em toda versão do chart: é a renderização que deve comprová-la. Não é preciso “fazer o pod subir quebrado” para emitir certificado se os recursos puderem ser aplicados separadamente.

## 16. Revisar e abrir o PR do deploy

**Resultado necessário antes do envio:** campos reais preenchidos, tag publicada, Secret operacional encaminhada/pronta, manifests revisados e somente HML como destino.

Na raiz do clone do deploy:

```powershell
git add Chart.yaml values.yaml
git add .github/workflows
git diff --cached --stat
git diff --cached
git commit -m "chore: preparar primeiro deploy em homologacao"
git push -u origin chore/preparar-primeiro-deploy-hml
```

Inclua `Chart.lock` apenas se a política do projeto exigir. Não use `git add .` sem inspecionar arquivos baixados ou gerados.

No GitHub:

1. Abra o repositório **de deploy**.
2. Clique em **Pull requests → New pull request**.
3. Em **base**, escolha `cloud/homologacao`.
4. Em **compare**, escolha `chore/preparar-primeiro-deploy-hml`.
5. Revise **Files changed**; verifique novamente que não é produção.
6. Descreva o objetivo, a tag, a execução da CI, o namespace/host HML, as validações e eventuais pendências. Não inclua credenciais.
7. Solicite a revisão prevista pelo projeto e acompanhe as Actions que o PR disparar.

Antes do merge, confirme:

- [ ] O PR mira `cloud/homologacao` e o Argo mira o mesmo destino.
- [ ] O build da branch auxiliar correta publicou a imagem informada.
- [ ] A CI não está acionando desenvolvimento.
- [ ] O chart foi renderizado e os recursos IDH/BBCert/DNS foram conferidos.
- [ ] Namespace, `env` e credenciais de pull foram conferidos, ou o PR é explicitamente só de certificados.
- [ ] AppKey autorizada e caminho de rede HML confirmados.
- [ ] O cadastro e a URL do gateway do agente estão definidos para o teste funcional.
- [ ] Há um único fluxo de CD efetivo, com tratamento de PR conhecido.
- [ ] Não há nomes antigos, placeholders ou valores sensíveis no diff.
- [ ] A aprovação de homologação exigida foi obtida.

Faça o merge pelo botão disponibilizado pelo GitHub conforme a política do repositório. Registre o SHA do merge.

## 17. Acompanhar a sincronização em HML

**GitHub:** repositório do deploy → **Actions → Deploy** → execução referente ao commit e à branch `cloud/homologacao`.

**Argo CD:** abra a aplicação HML pela instância OAS. Confira a revisão aplicada, o destino e os eventos. Com sync automático habilitado, o Argo pode reconciliar alterações do Git sem esperar uma sequência visual “Action terminou, depois Argo começou”. Se for manual, siga a aprovação e o Sync previstos pela plataforma; não use Force/Replace para tentar resolver erros desconhecidos. [Referência oficial de auto-sync](https://argo-cd.readthedocs.io/en/stable/user-guide/auto_sync/).

Para o deploy completo, confira:

- revisão correta e ausência de diferenças inesperadas (`Synced`);
- saúde dos recursos e disponibilidade do Deployment;
- pod em execução e container pronto, sem reinícios contínuos;
- imagem e tag reais do pod iguais às esperadas;
- emissão dos certificados e montagem do volume.

`Healthy`/`Synced` não comprova, isoladamente, a autorização ao LLM. CRs de operadores também podem ter uma apresentação de saúde específica; confira seu status de emissão, não apenas a cor do agregado.

Para o PR opcional só de certificados, não se espera um pod do agente funcionando: o resultado a verificar são os recursos de emissão e as Secrets produzidas.

## 18. Conferir Secrets e aplicação no OpenShift

**Onde:** OpenShift HML → namespace correto → **Secrets**.

| Nome | Chaves esperadas |
|---|---|
| `env` | `GATEWAY_OUTBOUND_GW_APP_KEY` |
| `idh-mtls` | `tls.crt`, `tls.key`, `ca.crt` |
| `iaa-agent-mf-assist-financeir-tls` | `tls.crt`, `tls.key` |

Confirme existência, nomes e condições de emissão. Os operadores geram as Secrets de certificado; a emissão não é uma ação executada pelo processo Python. Não crie um certificado improvisado se o operador apresentar erro.

Para verificar saúde sem presumir exposição pública das probes: OpenShift → **Workloads → Pods → pod do agente** → status, readiness, eventos e logs. Se há terminal autorizado no container e `curl` instalado, a equipe pode consultar `http://127.0.0.1:8080/health/live` e `/health/ready` a partir do próprio pod.

No código fornecido, as respostas são `{"status":"alive"}` e `{"status":"ready"}`. Readiness verifica configuração/grafo compilado; não faz uma chamada de teste ao LLM.

## 19. Testar o agente pelo gateway autorizado

**Antes:** confirme o vínculo do agente ao Catálogo de IA/API, a publicação em HML, a URL exata, o caminho e a autenticação do consumidor. A credencial para chamar o agente pode não ser a mesma AppKey que o agente usa no outbound.

O código expõe `POST /chat`. Um endereço publicado como `/v1/chat` depende de configuração explícita do gateway. Não experimente caminhos aleatórios nem assuma que o host do ingress é o endereço autorizado do consumidor.

Se a chamada não requer certificado cliente e sua sessão tem as autorizações necessárias, use no PowerShell:

```powershell
$chatHmlUrl = 'https://<HOST_GATEWAY_HML>/<CAMINHO_PUBLICADO_DO_CHAT>'
$chatHmlBody = @{
    message = 'Responda apenas: teste de conectividade concluido'
    session_id = 'teste-hml-001'
} | ConvertTo-Json

Invoke-RestMethod -Method Post -Uri $chatHmlUrl -ContentType 'application/json' -Body $chatHmlBody
```

Substitua pela URL completa do catálogo. Se forem exigidos headers de autorização ou certificado cliente, use o cliente/testador corporativo configurado com as credenciais do consumidor; o comando acima, sozinho, não será suficiente. Essa configuração depende do cadastro real e não pode ser inferida dos ZIPs.

**Resultado esperado:** HTTP 200, campos `reply`, `session_id` e `tool_calls_made`, com resposta coerente do modelo. Confira os logs do agente para excluir degradações de MCP e erros de outbound. Não use dados reais de clientes no teste inicial.

Depois teste as funcionalidades que compõem o escopo de homologação. O exemplo acima comprova uma integração técnica mínima, não todos os requisitos do agente financeiro.

## 20. Execução na estação corporativa com certificados — opcional, após a emissão

Nesta etapa, “local” significa executar na estação de desenvolvimento corporativa autorizada, e não na máquina externa usada para estudar os ZIPs. Só exporte as credenciais se o processo corporativo permitir esse uso. Se exportação não for permitida, faça a validação no cluster ou no ambiente autorizado.

No OpenShift HML → namespace → **Secrets → idh-mtls**, use o download dos arquivos decodificados oferecido pelo console. Se a tela exibir apenas Base64 em um YAML, não salve esse texto como se fosse PEM; peça apoio técnico para a exportação correta.

Salve os arquivos numa pasta pessoal protegida, fora dos clones, por exemplo:

```text
C:\Users\manue\.certs\iaa-agent-hml\
├── tls.crt
├── tls.key
└── ca.crt
```

No clone do código, copie `.env.example` para `.env` somente se ainda não existir:

```powershell
Set-Location 'C:\Users\manue\.0_PROG\UAN\AGENT-OPS\codigo-iaa-hml'
if (-not (Test-Path .env)) { Copy-Item .env.example .env }
git check-ignore .env
```

O último comando deve mostrar `.env`. Edite esse arquivo local, usando caminhos com `/` para facilitar a leitura do dotenv:

```dotenv
GATEWAY_OUTBOUND_GW_APP_KEY=<VALOR_AUTORIZADO_HML>
KEY_STORE_CERT_PATH=C:/Users/manue/.certs/iaa-agent-hml/tls.crt
KEY_STORE_KEY_PATH=C:/Users/manue/.certs/iaa-agent-hml/tls.key
TRUST_STORE_CA_PATH=C:/Users/manue/.certs/iaa-agent-hml/ca.crt
SERVICE_NAME=iaa-agent-mf-assist-financeir
DEPLOY_ENV=homol
```

Substitua usuário/caminhos conforme a máquina. `REQUESTS_CA_BUNDLE` e `SSL_CERT_FILE`, se usados localmente, devem apontar para o bundle corporativo válido dessa máquina, não para `/etc/pki/...` do container.

O código não contém carregamento automático de `.env`. Para carregá-lo explicitamente ao iniciar:

```powershell
.\.venv\Scripts\python.exe -m uvicorn iaa_agent_mf_assist_financeir.app:app --host 127.0.0.1 --port 8080 --env-file .env
```

Esse modo requer `python-dotenv`, normalmente instalado por `uvicorn[standard]` dos requirements. Se o ambiente não o possuir, instale pelo índice corporativo aprovado. Em outro PowerShell:

```powershell
Invoke-RestMethod 'http://127.0.0.1:8080/health/live'
Invoke-RestMethod 'http://127.0.0.1:8080/health/ready'
$localHmlBody = @{ message = 'Responda apenas: teste local concluido'; session_id = 'local-hml-001' } | ConvertTo-Json
Invoke-RestMethod -Method Post -Uri 'http://127.0.0.1:8080/chat' -ContentType 'application/json' -Body $localHmlBody
```

A aplicação é local, mas o LLM continua sendo o de HML. Para encerrar, pressione `Ctrl+C` no terminal que executa Uvicorn. A renovação dos certificados no cluster não atualiza automaticamente os arquivos exportados.

## 21. Quando algo não funcionar

| Sintoma | Conferir primeiro | Ação seguinte |
|---|---|---|
| Não apareceu execução de CI | Branch enviada e filtros de `.github/workflows/ci.yaml` | Usar a branch `fix/` deste roteiro; não fazer merge em `main` só para forçar execução. |
| CI falha na versão | Etapa Configure, versão Python e PEP 440 | Ajustar conforme o erro e a política; não inventar tag Docker. |
| CI verde, imagem ausente | Etapa de publicação, possíveis `Skipped` | Confirmar flag/configuração e localizar artefato antes do deploy. |
| Dois Deploys para o mesmo push | `cd.yaml` e `cd.yml` | Resolver duplicidade com a esteira. |
| `ImagePullBackOff` | Caminho/tag, registry e `atfregistry` | Corrigir imagem/permissão de pull, mantendo credenciais na plataforma. |
| Secret `env` ausente | Namespace e grafia | Provisionar `env` no namespace HML correto. |
| Secret `idh-mtls` ausente | Manifest IDH gerado, operador e eventos de emissão | Resolver chart/operador; não trocar por certificado de outro ambiente. |
| `CrashLoopBackOff` | Logs do container e eventos | Verificar AppKey, arquivos montados, configuração, dependências e limites. |
| `OOMKilled` | Limite de memória e consumo | Ajustar com base em evidência e quota aprovada. |
| `Synced`, mas chat falha | Gateway, AppKey autorizada, modelo e TLS outbound | Fazer diagnóstico funcional, não repetir Sync sem mudança. |
| HTTP 401/403 | Qual ponta negou: consumidor → agente ou agente → LLM | Conferir autorização da credencial correspondente. |
| HTTP 404 | URL publicada e reescrita `/v1/chat` → `/chat` | Corrigir cadastro/rota; health pode nem estar publicado no gateway. |
| Erro TLS | CA, validade, par certificado/chave e ambiente | Corrigir confiança/certificado. Não usar `-k` ou desabilitar validação TLS. |
| Timeout | DNS, rota, proxy/política de saída e LLM | Conferir conectividade corporativa antes de aumentar timeouts. |

Se o primeiro deploy falhar, não há necessariamente uma versão anterior saudável para voltar. Registre o SHA, eventos e erros sem secrets; corrija por novo PR. Reversão de certificado exige cuidado: o modelo BBCert declara campos de identidade imutáveis. Não exclua recursos nem use Force/Replace por tentativa.

## 22. Critério de conclusão

- [ ] Instância, namespace, host e catálogo HML confirmados.
- [ ] Imagem publicada, execução da CI, commit e tag registrados.
- [ ] Deploy HML aplicado na revisão esperada e sem efeito em desenvolvimento/produção.
- [ ] Secrets de runtime e de certificados presentes e válidas.
- [ ] Pod estável, probes aprovadas e eventos sem erros persistentes.
- [ ] Chamada real pelo gateway retorna resposta do LLM autorizado.
- [ ] Funcionalidades fora do teste mínimo (MCP, RAG, guardrails, observabilidade) estão explicitamente registradas como testadas ou pendentes.
- [ ] Alterações temporárias no autodeploy e integração posterior do código têm responsável definido.

## Fontes e decisões desta revisão

1. [Documentação corporativa de agentes](ESTEIRA_AGENTS_OPS/AGENTSOPS_AGENTES_IA.md): correção Python pós-migração, catálogo/AppKey, autorização ao LLM e emissão IDH sem imagem finalizada. A tabela de caminhos de certificados tem inconsistência; prevaleceram código e README do projeto.
2. [Esteira Python](DOCUMENTACAO_GERAL/esteira-python.md): branches aceitas, versões abertas/fechadas e etapas da CI. O workflow real do ZIP foi usado para os gatilhos específicos.
3. [README do código](iaa-agent-mf-assist-financeir-main/iaa-agent-mf-assist-financeir-main/README.md): modelo Helm. As versões e os recursos dependentes exigem validação com os charts privados.
4. [Workflow de CI](iaa-agent-mf-assist-financeir-main/iaa-agent-mf-assist-financeir-main/.github/workflows/ci.yaml): condições de CD-des/CD-hom e saída `versao_projeto`.
5. [Values do ZIP de produção](deploy-iaa-agent-mf-assist-financeir-cloud-producao/values.yaml) e [Chart do ZIP](deploy-iaa-agent-mf-assist-financeir-cloud-producao/Chart.yaml): localização da tag e configurações antigas; não comprovam o estado atual da branch HML.
6. [Aplicação](iaa-agent-mf-assist-financeir-main/iaa-agent-mf-assist-financeir-main/iaa_agent_mf_assist_financeir/app.py): endpoints e limites do readiness.
7. [Cliente outbound](iaa-agent-mf-assist-financeir-main/iaa-agent-mf-assist-financeir-main/iaa_agent_mf_assist_financeir/llm/gateway_outbound.py): AppKey, certificado, chave, CA e transformação do caminho de chamada.
8. [Teste de integração de exemplo](iaa-agent-mf-assist-financeir-main/iaa-agent-mf-assist-financeir-main/tests/integration/test_dummy.py): não valida integração real.

Este roteiro pode ser usado por uma pessoa iniciante para estudar os arquivos nesta máquina e, depois, conduzir os passos operacionais na estação corporativa. Validação de chart privado, permissões e decisões de publicação continuam exigindo a equipe responsável, nos pontos identificados nas etapas. Conclusão do estudo local não equivale a conclusão de deploy ou homologação.
