# Primeiro deploy em homologação e obtenção dos certificados

**Projeto:** `iaa-agent-mf-assist-financeir`  
**Onde executar:** estação corporativa com Pengwin/WSL, VS Code e acesso à rede corporativa.  
**Objetivo:** clonar, preparar os arquivos, publicar a imagem, abrir o PR de deploy, aplicar em homologação e obter os certificados.  
**Fim do roteiro:** aplicação iniciada no cluster e arquivos de certificado disponíveis na estação corporativa.

## Antes de começar

Este é um roteiro de execução. Faça uma etapa de cada vez e só avance quando alcançar o resultado esperado. Não precisamos configurar RAG, desenvolver ferramentas MCP, testar conversas do agente ou promover para produção para concluir este objetivo.

Os exemplos de configuração são baseados no projeto recebido após a migração. Se o repositório oficial já tiver alterações posteriores do time, compare antes de substituir. Os charts são privados: suas versões e o resultado da renderização precisam ser confirmados dentro da rede corporativa.

### Onde executar cada ação

| Indicação | Onde fazer |
|---|---|
| **Terminal Pengwin** | Pengwin Terminal ou terminal Linux de uma janela VS Code conectada ao WSL. |
| **VS Code — código** | Janela aberta na pasta do repositório Python. |
| **VS Code — deploy** | Janela aberta na pasta do repositório de deploy. |
| **Navegador** | GitHub corporativo, Tech.bb, Argo CD ou OpenShift. |

**Comandos deste guia são Linux.** Não os execute no PowerShell.

### Como interpretar os caminhos

Usaremos estes diretórios conceituais:

```text
$HOME/<codigo>
$HOME/deploy-<codigo>
$HOME/certificados/hml-<codigo>
```

No primeiro terminal do trabalho, defina as variáveis abaixo. O valor já está preenchido com o nome do projeto deste roteiro:

```bash
export CODIGO="iaa-agent-mf-assist-financeir"
export CODIGO_DIR="$HOME/$CODIGO"
export DEPLOY_DIR="$HOME/deploy-$CODIGO"
export CERT_DIR="$HOME/certificados/hml-$CODIGO"
export REVIEW_DIR="$HOME/revisao-$CODIGO"
```

Os caminhos reais serão `$HOME/iaa-agent-mf-assist-financeir`, `$HOME/deploy-iaa-agent-mf-assist-financeir` e `$HOME/certificados/hml-iaa-agent-mf-assist-financeir`. Se o nome oficial do repositório for diferente, altere somente o valor de `CODIGO` e execute novamente as quatro linhas seguintes.

Sempre que abrir um novo terminal Pengwin/VS Code, execute novamente esse mesmo bloco de cinco `export` antes de usar `$CODIGO_DIR`, `$DEPLOY_DIR`, `$CERT_DIR` ou `$REVIEW_DIR`. As variáveis existem apenas no terminal em que foram definidas.

`$HOME` é sua pasta pessoal Linux. O terminal substitui esse nome automaticamente. Para descobrir o caminho completo real:

```bash
printf '%s\n' "$HOME"
```

Se aparecer `/home/f1234567`, por exemplo, o primeiro repositório ficará em `/home/f1234567/iaa-agent-mf-assist-financeir`. Não altere a variável `HOME`.

Em cada etapa de edição haverá o caminho do arquivo, o comando para abri-lo e o que mudar. Campos entre `<...>` são marcadores: substitua pelo valor real antes de publicar.

### Valores que você precisará obter

No **Tech.bb → instância OAS do agente**, consulte os recursos de homologação e registre:

| Informação | Como usar |
|---|---|
| URL do repositório de código | Clone de `iaa-agent-mf-assist-financeir`. |
| URL do repositório de deploy | Clone de `deploy-iaa-agent-mf-assist-financeir`. |
| Link da aplicação Argo CD HML | Acompanhar o deploy. |
| Link do OpenShift HML | Criar/conferir Secrets e consultar o pod. |
| Namespace HML | Selecionar o projeto correto no cluster. |
| Host oficial do ingress HML | Preencher Ingress e BBCert; somente hostname, sem `https://` ou `/chat`. |
| Matrícula do custodiante | Responsável pelo certificado BBCert. |
| AppKey da aplicação e autorização de consumo | Alimentar a Secret operacional; obtenha pelo mecanismo corporativo. |

**Atenção ao ambiente:** ter uma URL de LLM em HML não prova que os recursos HML do agente já foram provisionados. Confirme que a aplicação Argo, o namespace e a branch `cloud/homologacao` existem. Se a esteira exigir uma promoção prévia a partir de desenvolvimento, essa regra precisa ser resolvida antes de seguir diretamente para HML.

### Sequência que vamos seguir

```text
Clone dos dois repositórios
→ branches de trabalho
→ ajustes e testes do código
→ CI publica a imagem, sem autodeploy
→ ajustes do chart e values
→ Secret operacional
→ validação e PR do deploy
→ merge em cloud/homologacao
→ sync no Argo CD
→ conferência do pod e dos certificados
→ download dos certificados
```

## 1. Abrir o Pengwin e conferir as ferramentas

**Onde:** Terminal Pengwin.

```bash
pwd
git --version
code --version
python3 --version
```

Para as etapas posteriores:

```bash
helm version
oc version --client
openssl version
```

**Resultado esperado:** ferramentas disponíveis. Para os testes Python deste projeto, usaremos Python 3.11, alinhado à imagem-base fornecida.

Se uma ferramenta não existir, instale-a pelo procedimento corporativo do Pengwin. Não mude proxy, certificados ou a distribuição inteira para tentar resolver uma única ferramenta ausente.

## 2. Clonar o repositório do código

### 2.1 Copiar a URL no GitHub

**Onde:** navegador.

1. Abra `bbvinet/iaa-agent-mf-assist-financeir`.
2. Clique no botão **Code**.
3. Selecione **HTTPS**.
4. Copie a URL.

O endereço esperado pelo nome do projeto é:

```text
https://github.com/bbvinet/iaa-agent-mf-assist-financeir.git
```

Se o endereço exibido pelo GitHub for diferente, use o endereço oficial exibido.

### 2.2 Executar o clone

**Onde:** Terminal Pengwin.

```bash
mkdir -p "$HOME"
git clone --branch main https://github.com/bbvinet/iaa-agent-mf-assist-financeir.git "$CODIGO_DIR"
```

Conclua a autenticação corporativa/SSO quando solicitada. Não coloque senha ou token dentro da URL.

Se `"$CODIGO_DIR"` já existir, confira se é o clone correto; não apague a pasta para repetir o comando.

### 2.3 Conferir o clone

```bash
cd "$CODIGO_DIR"
git status -sb
git remote -v
```

**Resultado esperado:** branch `main`, origem no repositório correto e nenhum arquivo modificado.

## 3. Clonar o repositório de deploy

**Onde:** navegador → `bbvinet/deploy-iaa-agent-mf-assist-financeir` → **Code → HTTPS**.

Confirme o endereço e execute no Pengwin:

```bash
git clone --branch cloud/homologacao https://github.com/bbvinet/deploy-iaa-agent-mf-assist-financeir.git "$DEPLOY_DIR"
cd "$DEPLOY_DIR"
git status -sb
git remote -v
```

**Resultado esperado:** branch `cloud/homologacao`, origem correta e pasta sem alterações.

Se aparecer que a branch não existe, confira seu nome no GitHub. Não crie uma branch HML vazia por conta própria nem substitua por `cloud/producao`.

## 4. Criar as duas branches de trabalho

Uma branch é uma área de trabalho dentro do Git. Ela permite revisar a alteração antes de incorporá-la ao destino.

### 4.1 Branch do código

```bash
cd "$CODIGO_DIR"
git switch main
git pull --ff-only
git switch -c fix/preparar-hml
git status -sb
```

**Resultado esperado:** `fix/preparar-hml`.

Usamos `fix/` porque o workflow recebido dispara em `fix/**`, `feat/**`, `feature/**` e `main`. Uma branch chamada `chore/...` não dispararia essa CI automaticamente.

### 4.2 Branch do deploy

```bash
cd "$DEPLOY_DIR"
git switch cloud/homologacao
git pull --ff-only
git switch -c chore/preparar-primeiro-deploy-hml
git status -sb
```

**Resultado esperado:** `chore/preparar-primeiro-deploy-hml`, criada a partir de `cloud/homologacao`.

Se já criou uma dessas branches anteriormente, use `git switch NOME_DA_BRANCH`, sem `-c`. Se houver arquivos modificados, preserve-os e revise antes de trocar de branch.

## 5. Abrir os projetos no VS Code

**Onde:** Terminal Pengwin.

```bash
code -n "$CODIGO_DIR"
code -n "$DEPLOY_DIR"
```

Serão duas janelas. No canto inferior esquerdo, confirme a indicação de conexão WSL com sua distribuição Pengwin.

Para abrir um arquivo na janela correspondente, pressione **Ctrl+P**, digite o caminho relativo, como `.github/workflows/ci.yaml`, e pressione Enter. Use **Ctrl+S** para salvar.

O terminal integrado deve ser Linux. No menu do VS Code, use **Terminal → New Terminal** e execute `pwd` para confirmar se está em `$CODIGO_DIR` ou `$DEPLOY_DIR`.

## 6. Preparar a CI sem disparar o deploy antes da hora

**Arquivo:**

```text
$CODIGO_DIR/.github/workflows/ci.yaml
```

**Abrir pelo Pengwin:**

```bash
code "$CODIGO_DIR/.github/workflows/ci.yaml"
```

Esse arquivo possui três jobs: `CI`, `CD-des` e `CD-hom`. Neste roteiro, vamos publicar a imagem primeiro e iniciar o deploy pelo PR do repositório de deploy.

### 6.1 Desabilitar temporariamente o autodeploy de desenvolvimento

Localize o job `CD-des`. Troque somente sua linha `if:`:

```yaml
    if: needs.CI.outputs.autodeploy == 'true'
```

por:

```yaml
    if: ${{ false }} # primeiro build: publicar imagem sem autodeploy
```

### 6.2 Desabilitar temporariamente o autodeploy de homologação

No job `CD-hom`, troque:

```yaml
    if: needs.CI.outputs.autodeploy == 'true' && needs.CI.outputs.autodeploy-hom == 'true'
```

por:

```yaml
    if: ${{ false }} # homologacao sera iniciada pelo PR de deploy
```

Mantenha os outros campos dos jobs e o job `CI` intactos. Não acrescente um segundo `if:` ao mesmo job.

**Por quê:** a configuração original pode acionar desenvolvimento junto com homologação. Ter a imagem publicada ainda não significa que o chart esteja pronto.

**Como conferir:** na primeira execução de Actions, o job `CI` deverá executar; `CD-des` e `CD-hom` deverão aparecer como **Skipped**. Essas alterações entram na revisão do código e sua política permanente deve ser definida depois; não reative desenvolvimento automaticamente.

Se a organização controla esse comportamento por configuração central ou bloqueia edição do workflow, use o mecanismo corporativo equivalente para **build sem autodeploy** antes de enviar o código.

## 7. Corrigir `aic.json`

**Arquivo:**

```text
$CODIGO_DIR/aic.json
```

**Abrir:**

```bash
code "$CODIGO_DIR/aic.json"
```

### 7.1 Versão Python

Troque:

```json
"versaoPython": "3.8"
```

por:

```json
"versaoPython": "3.11"
```

O projeto exige Python >= 3.11. A documentação da oferta informa que a migração pode deixar esse campo incorretamente como 3.8.

### 7.2 Publicação da imagem

Para preparar a publicação, ajuste:

```json
"publicarPacoteEImagem": true
```

O arquivo recebido ficará assim, preservando os outros campos:

```json
{
  "$schema": "https://binarios.intranet.bb.com.br:443/artifactory/generic-bb-binarios-aic-local/publico/json-schemas/aic.schema.json",
  "pipeline": {
    "versaoPython": "3.11",
    "publicarPacoteEImagem": true,
    "habilitarValidacaoEstatica": true,
    "habilitarValidacaoSeguranca": false,
    "pacoteSource": false
  }
}
```

Confirme que o schema vigente aceita os valores. O exemplo preserva as flags recebidas; não dispensa verificações de segurança obrigatórias pela esteira. A comprovação da publicação será a etapa Docker concluída e a imagem no registry, não apenas o valor `true`.

### 7.3 Conferir a sintaxe

```bash
cd "$CODIGO_DIR"
python3 -m json.tool aic.json
```

**Resultado esperado:** o JSON é exibido formatado, sem erro. Se aparecer erro, confira aspas, chaves e vírgulas.

## 8. Conferir a versão do pacote

**Arquivo:**

```text
$CODIGO_DIR/iaa_agent_mf_assist_financeir/__init__.py
```

**Abrir:**

```bash
code "$CODIGO_DIR/iaa_agent_mf_assist_financeir/__init__.py"
```

O valor recebido é:

```python
__version__ = '0.1.0.dev0'
```

Essa é uma versão aberta do pacote Python. A documentação da esteira associa versões abertas às branches auxiliares e versões fechadas à `main`.

Para o primeiro build HML, mantenha a versão aberta se aceita e ainda publicável. Se já foi publicada e a esteira recusar repetição, escolha a próxima versão aberta conforme o padrão do projeto. Não sobrescreva uma imagem existente por tentativa.

**Não troque a versão por `0.1.0-SNAPSHOT` só para coincidir com o `values.yaml`.** A tag final será obtida da publicação da imagem.

Neste fluxo, faremos o build na branch `fix/preparar-hml`; o merge do código em `main` não é pré-requisito para esse primeiro deploy HML. O PR que aplicará o deploy terá como destino `cloud/homologacao`, no outro repositório.

## 9. Conferir `agent_config.yaml`

**Arquivo:**

```text
$CODIGO_DIR/agent_config.yaml
```

**Abrir:**

```bash
code "$CODIGO_DIR/agent_config.yaml"
```

### 9.1 URL de homologação

O projeto recebido contém:

```yaml
llm:
  provider: "gateway_outbound"
  gateway_outbound:
    base_url: "https://llms-agentes-ia.outbound.api.hm.bb.com.br/v1"
    model: "cambio-non-prod-gpt4o"
    api_version: "2024-12-01-preview"
    max_tokens: 4096
```

A URL já é de homologação. Mantenha-a se o catálogo confirmar o endpoint e o modelo para a aplicação. Não use essa URL como hostname do ingress do agente: são serviços diferentes.

### 9.2 Retirar a dependência do MCP de exemplo

Como o objetivo é subir o agente e obter os certificados, sem integrar ferramentas MCP agora, localize a seção `mcp:` e substitua **essa seção inteira** por:

```yaml
mcp:
  servers: []
```

Isso remove a tentativa de acessar o MCP de exemplo em `localhost:9000`, que dentro do container apontaria para o próprio pod.

Preserve as demais configurações. `rag.enabled` e `guardrails.enabled` já estão `false` no modelo recebido; não configure essas integrações neste primeiro deploy técnico.

## 10. Instalar dependências e executar os testes

**Onde:** Terminal Pengwin, repositório de código.

### 10.1 Selecionar Python 3.11

```bash
cd "$CODIGO_DIR"
python --version
```

Se o Pengwin já usa Python 3.11, prossiga. Se usa outra versão e o projeto utiliza pyenv:

```bash
pyenv versions
```

Selecione uma versão 3.11 instalada e suportada na estação:

```bash
pyenv local <VERSAO_3.11_INSTALADA>
python --version
```

Substitua o marcador antes de executar. Se não houver Python 3.11 instalado, use o procedimento corporativo do Pengwin para instalá-lo. Não altere o Python do sistema por tentativa.

O comando `pyenv local` pode criar o arquivo `$CODIGO_DIR/.python-version`; só o versione se o projeto adotar essa convenção.

### 10.2 Criar o ambiente de testes

```bash
python -m venv .venv
source .venv/bin/activate
python --version
python -m pip install -r requirements.txt
python -m pip install -e ".[unit,integration]"
python -m pip check
python -m pytest -q
```

**Arquivos lidos para instalar dependências:**

```text
$CODIGO_DIR/requirements.txt
$CODIGO_DIR/setup.py
```

Use os dois porque o projeto recebido tem diferenças entre suas listas de dependências. Resolva incompatibilidades apontadas; os testes e o build Docker da esteira continuam necessários.

**Resultado esperado:** nenhuma incompatibilidade em `pip check` e testes aprovados.

Não é necessário iniciar o agente na estação nem obter certificados para executar testes isolados. O teste de integração de exemplo do projeto não comprova comunicação real com o LLM; essa validação funcional está fora deste roteiro.

## 11. Fazer commit e push do código

**Onde:** Terminal Pengwin, pasta `$CODIGO_DIR`.

```bash
cd "$CODIGO_DIR"
git status -sb
git diff --check
git diff
```

Confirme a branch `fix/preparar-hml`. O `git diff` mostra exatamente o que você alterou. Para sair da visualização paginada, pressione `q`.

Prepare os arquivos:

```bash
git add aic.json agent_config.yaml .github/workflows/ci.yaml
```

Se você alterou a versão, prepare também:

```bash
git add iaa_agent_mf_assist_financeir/__init__.py
```

Confira o conteúdo que entrará no commit:

```bash
git diff --cached
git commit -m "fix: preparar primeiro build de homologacao"
git push -u origin fix/preparar-hml
```

`commit` registra as alterações; `push` as envia ao GitHub. Se houver exigência de assinatura ou identidade corporativa do Git, ajuste pelo padrão da organização; não desative a exigência.

## 12. Acompanhar a CI e anotar a tag real

**Onde:** navegador → repositório `iaa-agent-mf-assist-financeir` → **Actions**.

1. Abra **Esteira de Build Python**.
2. Selecione a execução da branch `fix/preparar-hml` e do commit enviado.
3. Abra o job `CI` e confira testes, verificações, build e publicação Docker.
4. Confirme que `CD-des` e `CD-hom` estão **Skipped** neste fluxo.
5. No resumo/log de publicação, localize a imagem publicada.

Registre:

```text
Execução da CI:
Commit do código:
Repositório da imagem:
Tag publicada:
Digest, se disponível:
```

O workflow usa a saída `versao_projeto`, mas esse nome não é a versão concreta. Procure o valor efetivamente publicado no log ou no registry corporativo.

**Resultado esperado:** imagem publicada e tag conhecida. CI verde com a publicação marcada como `Skipped` não satisfaz esta etapa.

Se o workflow não executar, confirme branch e filtros. Uma alteração exclusivamente em `.github/workflows/**` pode ser ignorada pelo filtro recebido. Nosso commit também altera `aic.json`.

### PR do código, se exigido para revisão

No GitHub → repositório de código → **Pull requests → New pull request**, abra a revisão conforme a estratégia do projeto, usando `fix/preparar-hml` como branch de origem. Se a revisão usar `main` como base, mantenha o PR como draft até resolver a regra de versionamento; não faça merge de uma versão aberta na `main` apenas para obter o build HML.

O PR de deploy, descrito na etapa 20, é o que publicará os manifests em `cloud/homologacao`.

## 13. Abrir o projeto de deploy e o modelo Helm

**Onde:** Terminal Pengwin.

```bash
cd "$DEPLOY_DIR"
git status -sb
code -n "$DEPLOY_DIR"
```

Confirme `chore/preparar-primeiro-deploy-hml`.

**Modelo de referência:**

```text
$CODIGO_DIR/README.md
```

Abra-o em outra janela:

```bash
code "$CODIGO_DIR/README.md"
```

Pesquise por **Configuração Inicial do Helm Chart**. Essa seção apresenta `Chart.yaml` e `values.yaml` para o agente. Ela contém exemplos de produção: usaremos a estrutura com adaptações para HML, não o conteúdo sem revisão.

## 14. Corrigir `Chart.yaml`

**Arquivo:**

```text
$DEPLOY_DIR/Chart.yaml
```

**Abrir:**

```bash
code "$DEPLOY_DIR/Chart.yaml"
```

O arquivo antigo usa `bb-aplic` e nomes do template. O modelo do projeto usa as dependências abaixo:

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

Se o arquivo ainda é o template antigo sem customizações, substitua pelo modelo acima, usando as versões aprovadas pela esteira. As versões mostradas são as do README recebido; não são uma afirmação de que continuam sendo as versões atualmente recomendadas.

**Como conferir:** o chart da aplicação é `dia-chart-agent`, seu alias é `iaa-agent-mf-assist-financeir` e há uma dependência IDH. Não use `dia-chart-mcp`, que tem outra finalidade.

`version` e `appVersion` deste arquivo não são o campo que escolhe a imagem Docker do pod.

## 15. Preparar `values.yaml`

**Arquivo a editar:**

```text
$DEPLOY_DIR/values.yaml
```

**Abrir:**

```bash
code "$DEPLOY_DIR/values.yaml"
```

### 15.1 Usar a estrutura completa do modelo

No arquivo de referência:

```text
$CODIGO_DIR/README.md
```

1. Encontre **Configuração Inicial do Helm Chart**.
2. Localize o subtítulo `values.yaml` abaixo do exemplo de `Chart.yaml`.
3. Copie todo o conteúdo do bloco YAML, sem as linhas de três crases.
4. Se o `values.yaml` de HML ainda é o template inicial, use esse conteúdo como base.
5. Se ele já contém configurações do time, compare e incorpore as diferenças; não substitua essas configurações cegamente.
6. Aplique todas as adaptações 15.2 a 15.9 antes do commit.

Os próximos trechos são seções do mesmo arquivo. **Edite as seções existentes; não acrescente uma segunda seção com o mesmo nome.**

### 15.2 Nome principal e Service

A primeira chave deverá ser:

```yaml
iaa-agent-mf-assist-financeir:
```

Ela precisa coincidir com o alias do `Chart.yaml`.

Dentro dela, configure:

```yaml
  service:
    name: iaa-agent-mf-assist-financeir
    enable: true
    type: ClusterIP
    ports:
      - name: http
        port: 80
        targetPort: 8080
```

Mantenha `deployment.enable: true`. HPA, canário, Curió, ingress externo e persistência podem permanecer desabilitados no primeiro deploy se não forem usados pelo projeto.

### 15.3 Onde fica a tag da aplicação

No mesmo arquivo, procure `deployment:`, depois `containers:`, depois `tag:`:

```yaml
iaa-agent-mf-assist-financeir:
  deployment:
    enable: true
    imagePullSecrets: atfregistry
    replicaCount: 1
    containers:
      tag: "<TAG_PUBLICADA_PELA_CI>"
      imagePullPolicy: IfNotPresent
```

O caminho exato é:

```text
$DEPLOY_DIR/values.yaml
→ iaa-agent-mf-assist-financeir
→ deployment
→ containers
→ tag
```

Substitua `<TAG_PUBLICADA_PELA_CI>` pela tag anotada na etapa 12. O modelo traz `0.1.0-SNAPSHOT`; esse valor pode ficar se for exatamente a imagem publicada. O que não pode é assumir sua existência.

Não altere por engano as tags de `deploymentCanario`, `initContainer` ou `curio`.

### 15.4 Variáveis do container

**Caminho interno:** `iaa-agent-mf-assist-financeir → deployment → containers → environments`.

Dentro da lista existente, confira estas entradas:

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

Mantenha cada variável uma única vez. Os caminhos `/app/certs/...` são caminhos **dentro do container**, não no Pengwin. O bundle `/etc/pki/...` vem do modelo de imagem: confira que existe na imagem efetivamente publicada.

Se mantiver `MP_OPENAPI_SERVERS`, use `https://<HOST_INGRESS_HML>`. Preserve a telemetria prevista pelo projeto, sem inserir credenciais no YAML.

### 15.5 Referência à Secret operacional

**Caminho interno:** `iaa-agent-mf-assist-financeir → deployment → containers → envFrom`.

```yaml
      envFrom:
        - secretRef:
            name: env
```

`env` é o nome da Secret que conterá a AppKey. O valor da AppKey não é escrito nesse arquivo.

### 15.6 Montagem dos certificados

**Dentro de `deployment.containers`:**

```yaml
      volumeMounts:
        - name: tls-certs-volume
          mountPath: /app/certs
          readOnly: true
```

**Dentro de `deployment`, no mesmo nível de `containers`:**

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

Observe a diferença de recuo: `volumeMounts` fica dentro de `containers`; `volumes` fica ao lado de `containers`.

### 15.7 Probes e recursos

**Dentro de `deployment.containers`:** mantenha as probes do README:

```yaml
      livenessProbe:
        initialDelaySeconds: 30
        periodSeconds: 10
        timeoutSeconds: 10
        failureThreshold: 6
        successThreshold: 1
        httpGet:
          path: /health/live
          port: 8080
      readinessProbe:
        initialDelaySeconds: 30
        periodSeconds: 10
        timeoutSeconds: 10
        failureThreshold: 6
        successThreshold: 1
        httpGet:
          path: /health/ready
          port: 8080
```

Essas são as verificações que o cluster fará para saber se o processo está vivo e pronto. Confira também `resources.requests` e `resources.limits` com a quota HML. Os números do template são ponto de partida, não garantia de dimensionamento adequado.

### 15.8 Ingress e DNS

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

Substitua todas as ocorrências de `<HOST_INGRESS_HML>` pelo mesmo hostname oficial. Não use `https://`, caminho `/chat` ou hostname de produção nesses campos.

A classe `ingress-interno-iib` e o formato de `paths` vêm do modelo recebido. A validação Helm deve confirmar a compatibilidade com o chart utilizado e com o cluster HML.

### 15.9 IDH e BBCert

**Na coluna inicial do mesmo `values.yaml`:**

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

Substitua matrícula e host pelos valores reais. `commomName` é a grafia do modelo corporativo; não a altere para `commonName` sem consultar o schema.

`alternativesNames: []` evita pedir domínios extras sem necessidade. Preencha somente se o cadastro do certificado exigir nomes adicionais.

Não confunda:

| Campo | Valor |
|---|---|
| Branch do deploy | `cloud/homologacao` |
| `DEPLOY_ENV` | `homol` |
| `ambientePKI` | `hml` |

**Resultado esperado da etapa 15:** um único arquivo coerente, com dados HML reais e sem marcadores `<...>` nos valores que serão publicados.

## 16. Conferir a duplicidade de workflows do deploy

**Arquivos:**

```text
$DEPLOY_DIR/.github/workflows/cd.yaml
$DEPLOY_DIR/.github/workflows/cd.yml
```

**Abrir e comparar:**

```bash
code --diff "$DEPLOY_DIR/.github/workflows/cd.yaml" "$DEPLOY_DIR/.github/workflows/cd.yml"
```

Execute a comparação apenas se ambos existirem. O modelo recebido contém dois workflows que chamam a mesma esteira, mas têm filtros diferentes. Não são arquivos idênticos: `cd.yml` também dispara em abertura/reabertura de PR para HML.

### Como decidir

1. Consulte o workflow padrão disponibilizado pela migração/esteira.
2. Compare os dois arquivos com esse padrão, inclusive gatilhos de PR.
3. Mantenha o que corresponde à configuração corporativa atual e remova apenas o redundante.

Se foi confirmado que o arquivo oficial é `cd.yaml`, faça:

```bash
cd "$DEPLOY_DIR"
git rm .github/workflows/cd.yml
```

Se o oficial for `cd.yml`, remova `cd.yaml` no lugar. Não execute as duas remoções. A diferença de extensão, sozinha, não determina qual é oficial.

O workflow mantido deve reconhecer `cloud/homologacao` e continuar usando a esteira corporativa. Verifique o tratamento de `pull_request` no workflow reutilizável; a abertura do PR pode iniciar uma Action antes do merge.

**Resultado esperado:** um único fluxo efetivo para cada evento de deploy HML.

## 17. Preparar a Secret `env` no OpenShift HML

**Onde:** navegador → link OpenShift HML da instância OAS.

### 17.1 Confirmar namespace e AppKey

1. Selecione o projeto/namespace do agente em homologação.
2. Confira o nome no topo da tela antes de criar recursos.
3. No Catálogo de Aplicações/IA, obtenha a AppKey da aplicação pelo mecanismo corporativo.
4. Confirme a autorização da aplicação para a API provedora do LLM em HML.

A documentação recebida referencia **Azure AI Foundry – LLMS AGENTES IA (17703978)** e a equipe **IA Generativa Avançada** para a autorização. Confira os dados atuais no catálogo. Não precisamos fazer uma conversa de teste agora, mas a credencial não pode ser inventada.

### 17.2 Criar ou conferir a Secret

No OpenShift:

```text
Namespace HML do agente
→ Workloads
→ Secrets
→ Create
→ Key/value secret
```

O menu pode aparecer diretamente como **Secrets**.

Preencha:

```text
Nome: env
Chave: GATEWAY_OUTBOUND_GW_APP_KEY
Valor: AppKey autorizada da aplicação
```

Se `env` já existir, confira e atualize somente o necessário; não apague as outras chaves. Se a plataforma materializa Secrets por um gerenciador corporativo, use esse mecanismo em vez da criação manual.

Confirme também que `atfregistry`, usada para baixar a imagem, está provisionada conforme o padrão do namespace.

**Não colocar a AppKey em nenhum arquivo do repositório.** Seu valor só entra no mecanismo de credenciais.

### O que existe antes e depois do sync

| Secret | Como aparece | Quando é necessária |
|---|---|---|
| `env` | Cadastro pelo processo corporativo | Antes do container iniciar. |
| `atfregistry` | Provisionamento da plataforma | Antes do pod baixar a imagem. |
| `idh-mtls` | Emissão pelo operador IDH | Pode surgir durante o primeiro sync; necessária para montar o volume. |
| `iaa-agent-mf-assist-financeir-tls` | Emissão pelo BBCert | Necessária para o certificado TLS do ingress. |

Os operadores emitem os certificados; o processo Python não os gera. A emissão IDH não depende de uma imagem funcional. Neste roteiro faremos o deploy completo, mas é possível provisionar somente os certificados antes, se o chart renderizar seus recursos separadamente.

## 18. Validar o chart antes do PR

**Onde:** Terminal Pengwin, repositório de deploy.

### 18.1 Conferir os arquivos editados

```bash
cd "$DEPLOY_DIR"
git diff --check
git diff --stat
git diff
```

No VS Code, use **Ctrl+Shift+F** para procurar, em `Chart.yaml` e `values.yaml`:

```text
agent-azure-template-python
dia-agent-azure-template-python
<HOST_INGRESS_HML>
<MATRICULA_CUSTODIANTE>
<TAG_PUBLICADA_PELA_CI>
```

Não devem restar esses nomes/marcadores nos campos ativos. Confira `ambientePKI: hml` e `DEPLOY_ENV: homol`.

Encontrar `0.1.0-SNAPSHOT` não é falha se essa foi a tag realmente publicada.

### 18.2 Baixar e conferir as dependências Helm

```bash
helm dependency update .
helm lint . -f values.yaml
```

Esses comandos exigem acesso aos repositórios privados. Se há erro de rede, autenticação, versão ou certificado, resolva a causa antes de continuar.

`helm dependency update` pode criar:

```text
$DEPLOY_DIR/Chart.lock
$DEPLOY_DIR/charts/
```

Confira a política do repositório antes de versionar esses artefatos; não os inclua automaticamente.

### 18.3 Renderizar os manifests

Defina o namespace real neste terminal:

```bash
export NAMESPACE_HML='<NAMESPACE_REAL_HML>'
```

Substitua o marcador dentro das aspas. Gere uma prévia fora dos clones:

```bash
mkdir -p "$REVIEW_DIR"
helm template iaa-agent-mf-assist-financeir . -f values.yaml --namespace "$NAMESPACE_HML" > "$REVIEW_DIR/manifests-hml.yaml"
```

**Arquivo gerado para leitura:**

```text
$REVIEW_DIR/manifests-hml.yaml
```

**Abrir:**

```bash
code "$REVIEW_DIR/manifests-hml.yaml"
```

Confirme:

- Deployment e Service do agente, portas e namespace esperados;
- imagem completa, incluindo caminho no registry e tag da CI;
- referência a `env`, credencial de pull e volume `idh-mtls`;
- Ingress HML com a Secret TLS correta;
- recurso de solicitação de certificado IDH;
- recurso BBCert com PKI HML;
- recurso de DNS ou mecanismo equivalente previsto pela plataforma.

**Duas verificações essenciais:** o README usa `idhmtls`, embora a dependência se chame `idh-operator-chart`, e usa `dnsingress` sem uma dependência direta de mesmo nome no exemplo de Chart. A renderização deve comprovar que esses valores são consumidos. Se não aparecer o recurso esperado, consulte o schema/valores das dependências no registry e ajuste conforme a esteira. Não invente um alias para fazer o erro desaparecer.

`helm lint` e `helm template` não comprovam permissões, disponibilidade dos operadores ou todas as regras do cluster. Use também as validações exigidas pela plataforma HML. Nenhum desses comandos aplica o deploy.

## 19. Fazer commit e push do deploy

**Onde:** Terminal Pengwin, clone de deploy.

```bash
cd "$DEPLOY_DIR"
git status -sb
git add Chart.yaml values.yaml
git add .github/workflows
git diff --cached --stat
git diff --cached
```

Se a política exigir `Chart.lock`, inclua-o após conferência:

```bash
git add Chart.lock
```

Não inclua a prévia renderizada, credenciais, certificados ou arquivos de editor. Confira a branch `chore/preparar-primeiro-deploy-hml`.

```bash
git commit -m "chore: preparar primeiro deploy em homologacao"
git push -u origin chore/preparar-primeiro-deploy-hml
```

## 20. Abrir o PR de deploy

**Onde:** navegador → repositório `deploy-iaa-agent-mf-assist-financeir`.

1. Clique em **Pull requests**.
2. Clique em **New pull request**.
3. Em **base**, selecione `cloud/homologacao`.
4. Em **compare**, selecione `chore/preparar-primeiro-deploy-hml`.
5. Confirme que as alterações são as esperadas.
6. Clique em **Create pull request**.

O sentido precisa ser:

```text
chore/preparar-primeiro-deploy-hml
                 ↓
         cloud/homologacao
```

**Não use `main` ou `cloud/producao` como destino desse PR.**

### Modelo de descrição do PR

```text
Preparação do primeiro deploy do agente em homologação.

Imagem publicada:
Tag:
Execução da CI:
Commit do código:
Namespace HML:
Host HML:

Alterações:
- Atualização do chart de agente e configuração IDH/BBCert.
- Configuração da imagem, Service, Deployment e ingress HML.
- Referência à Secret operacional env e montagem de idh-mtls.
- Revisão dos workflows de deploy.

Validações:
- CI e publicação da imagem concluídas.
- Helm lint e prévia dos manifests conferidos.
- Secrets operacionais e destino HML conferidos.

Objetivo: iniciar a aplicação e obter os certificados de homologação.
```

Preencha os campos sem incluir valores de Secrets. Abertura/reabertura do PR pode disparar Actions, dependendo do workflow corporativo; acompanhe os checks desde esse momento.

## 21. Revisar e fazer o merge

**Onde:** página do PR no GitHub.

Abra **Files changed** e confira:

- base do PR: `cloud/homologacao`;
- tag corresponde à imagem publicada;
- host e namespace são HML;
- `ambientePKI` é `hml`;
- não restam nomes do template ou marcadores sem preencher;
- IDH/BBCert aparecem na prévia renderizada;
- Secret `env` está pronta no namespace correto;
- só há um fluxo de deploy efetivo;
- checks e aprovações obrigatórias foram satisfeitos.

Clique no botão de merge disponibilizado pelo projeto e confirme a operação. Se a proteção exigir revisão por outra pessoa, siga essa regra mesmo tendo privilégios; não use bypass para encurtar o roteiro.

Registre o SHA do commit incorporado. Ele permite conferir se o Argo aplicou a revisão certa.

## 22. Acompanhar o primeiro deploy

### 22.1 GitHub Actions

**Onde:** repositório de deploy → **Actions → Deploy**.

Abra a execução da branch `cloud/homologacao` correspondente ao merge. Confira status, mensagens de liberação e ambiente de destino.

### 22.2 Argo CD

**Onde:** Tech.bb → instância OAS → link Argo CD de homologação → aplicação do agente.

Antes de sincronizar, confira:

- repositório de deploy correto;
- branch/revisão `cloud/homologacao`;
- cluster e namespace HML;
- commit aplicado ou a aplicar.

Se o **auto-sync** estiver habilitado, o Argo detectará a mudança no Git. Isso pode acontecer enquanto você acompanha a Action; não presuma que a Action precisa terminar primeiro para qualquer reconciliação.

Se o sync for manual, siga a liberação da plataforma, clique em **Sync**, revise os recursos e confirme o sync normal. Não marque **Force**, **Replace**, **Prune** ou outras opções sem uma necessidade revisada; não use essas opções para “tentar fazer subir”.

Para o deploy completo, procure:

```text
Sync Status: Synced
Health Status: Healthy
```

Confira também os recursos individualmente, pois operadores podem apresentar estados próprios de emissão de certificado.

### 22.3 Pod no OpenShift

**Onde:** OpenShift HML → namespace do agente → **Workloads → Pods**.

Abra o pod e confira:

- estado `Running`;
- container da aplicação pronto (`Ready`);
- imagem e tag esperadas;
- ausência de reinícios contínuos;
- probes aprovadas;
- eventos e logs sem erros persistentes.

Pode haver uma espera inicial pela Secret `idh-mtls`. Se a espera persistir, consulte o recurso IDH e seus eventos; não copie um certificado de outro ambiente.

Readiness aprovada confirma o estado técnico verificado pelo código, mas não é teste de conversa com o LLM. Esse teste não faz parte do objetivo deste roteiro.

## 23. Conferir as Secrets de certificados

**Onde:** OpenShift HML → namespace do agente → **Secrets**.

Procure:

| Nome | Conteúdo esperado | Finalidade |
|---|---|---|
| `idh-mtls` | `tls.crt`, `tls.key`, `ca.crt` | Certificado cliente, chave e CA para mTLS outbound. |
| `iaa-agent-mf-assist-financeir-tls` | `tls.crt`, `tls.key` | Certificado do ingress, emitido pelo BBCert. |

Abra `idh-mtls` e confira os nomes das três chaves. Não é preciso exibir os valores em uma captura de tela.

O certificado cliente é `tls.crt`; a chave privada é `tls.key`; a CA é `ca.crt`. Não troque esses arquivos ao configurar caminhos.

**Resultado esperado:** Secrets emitidas no namespace HML, com as chaves previstas. Agora podemos obter os arquivos IDH na estação corporativa.

## 24. Baixar os certificados no Pengwin

O procedimento abaixo pressupõe que a política corporativa permite exportar esses arquivos para sua estação autorizada. Eles ficarão fora dos repositórios.

### 24.1 Autenticar o cliente OpenShift

**Onde:** navegador, console OpenShift HML.

Use o mecanismo de login CLI oferecido pelo console, normalmente no menu do usuário em **Copy login command**, e execute-o privadamente no Pengwin conforme o procedimento corporativo. Não cole token no guia, no Git ou em mensagens. Se o fluxo fornece token em comando, evite sua persistência em histórico/transcrição conforme a configuração corporativa do shell.

**Conferir no Pengwin:**

```bash
oc whoami
oc whoami --show-server
```

Confirme que o servidor é o HML. Defina o namespace real, se abriu outro terminal:

```bash
export NAMESPACE_HML='<NAMESPACE_REAL_HML>'
oc get secret idh-mtls -n "$NAMESPACE_HML"
```

Esse comando mostra metadados, sem imprimir certificado ou chave.

### 24.2 Criar a pasta de destino

**Pasta dos arquivos:**

```text
$CERT_DIR
```

**Executar:**

```bash
umask 077
mkdir -p "$CERT_DIR"
chmod 700 "$CERT_DIR"
```

Essa pasta é irmã de `$CODIGO_DIR` e `$DEPLOY_DIR`, não fica dentro deles.

### 24.3 Extrair os arquivos IDH

```bash
oc extract secret/idh-mtls -n "$NAMESPACE_HML" --keys=tls.crt,tls.key,ca.crt --to="$CERT_DIR"
```

O comando extrai os arquivos decodificados. Se já existirem arquivos com esses nomes, não force sobrescrita: confira se são uma extração anterior e use uma nova pasta para preservar a versão existente.

Os caminhos finais serão:

```text
$CERT_DIR/tls.crt
$CERT_DIR/tls.key
$CERT_DIR/ca.crt
```

Se o login CLI não estiver disponível, use o download dos três arquivos decodificados na tela da Secret no console. Não salve o Base64 do YAML como se fosse PEM. Guarde os arquivos em pasta corporativa protegida, fora dos clones.

### 24.4 Conferir sem revelar a chave

```bash
chmod 600 "$CERT_DIR/tls.crt" "$CERT_DIR/tls.key" "$CERT_DIR/ca.crt"
ls -l "$CERT_DIR"
openssl x509 -in "$CERT_DIR/tls.crt" -noout -subject -issuer -dates
openssl x509 -in "$CERT_DIR/tls.crt" -checkend 0 -noout
```

**Resultado esperado:** três arquivos não vazios, certificado legível, identidade/emissor coerentes com a emissão e não expirado. Essa inspeção não substitui uma validação completa de cadeia/uso mTLS.

Não use `cat tls.key` para conferir a chave: isso expõe o conteúdo privado. Não é necessário exportar a chave do certificado de ingress para concluir a obtenção dos certificados cliente IDH.

## 25. Conferência final e encerramento

- [ ] O merge ocorreu em `cloud/homologacao`.
- [ ] A imagem aplicada corresponde à CI e à tag registradas.
- [ ] O Argo aplicou a revisão esperada.
- [ ] O container do agente está pronto e estável.
- [ ] A Secret `idh-mtls` contém `tls.crt`, `tls.key` e `ca.crt`.
- [ ] A Secret TLS do ingress foi emitida, conforme a configuração BBCert.
- [ ] Os três arquivos IDH foram obtidos e guardados fora dos repositórios.
- [ ] Nenhuma AppKey ou chave privada entrou nos commits.
- [ ] A configuração temporária de autodeploy e a integração posterior do código ficaram registradas no PR/revisão.

**Objetivo concluído:** primeiro deploy técnico em homologação realizado e certificados obtidos. Encerramos aqui, sem iniciar testes de conversa, integrações adicionais ou promoção para produção.

## Problemas mais comuns

| Mensagem/situação | O que conferir |
|---|---|
| Clone falha por autenticação | SSO, acesso à organização e mecanismo de credenciais do Git corporativo. |
| Não existe `cloud/homologacao` | Provisionamento/branch oficial; não criar vazia como atalho. |
| CI não aparece | Nome da branch, gatilhos e filtro `paths-ignore` do workflow. |
| CI falha na versão | Python 3.11, versão aberta na branch auxiliar e regras da etapa Configure. |
| CI verde, sem imagem | Se a publicação foi executada ou ficou `Skipped`. |
| Dois deploys para o mesmo evento | Duplicidade de `cd.yaml` e `cd.yml`. |
| `helm lint` passa, mas IDH não aparece | Chave/alias aceito pela dependência e recursos realmente renderizados. |
| `ImagePullBackOff` | Caminho/tag da imagem, acesso ao registry e `atfregistry`. |
| `secret "env" not found` | Nome da Secret e namespace em que ela foi criada. |
| `secret "idh-mtls" not found` | Recurso IDH, operador e condições de emissão. |
| `CrashLoopBackOff` | Logs da aplicação, credencial obrigatória, caminhos de certificados e configuração. |
| `OOMKilled` | Memória utilizada, limite e quota HML. |
| Ingress ou BBCert não fica pronto | Host, PKI `hml`, custodiante, nomes TLS e eventos do operador. |
| Erro TLS ao baixar dependências | Rede/trust store corporativos; não desativar verificação TLS. |
