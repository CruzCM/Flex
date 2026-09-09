# Do Pengwin ao primeiro Hello World do CONSULT FIN

Manual de onboarding local — edição de 08/09/2026.

## 1. Objetivo e como usar este guia

Você já abriu o Pengwin Terminal, já clonou o projeto e está dentro da pasta dele. Vamos entender o ambiente, preparar o Python, instalar o projeto, conferir testes locais e chegar a uma resposta real do Agent pelo endpoint `POST /chat`.

Não é necessário conhecer Linux, Python ou APIs de antemão. Execute um bloco por vez. Leia seu resultado antes de avançar. Se um checkpoint falhar, siga “Se der erro”; não pule a falha para tentar compensá-la depois.

**Limite desta edição:** o material entregue para análise contém cópias locais do projeto, sem `.git`. O cenário “repositório clonado do GitHub” é o ponto de partida pretendido para o leitor, não algo comprovado sobre essas cópias. URL GitHub, remote, branch, commit e checkout atual: **NÃO DETERMINADO**. Quando um clone com histórico for fornecido, essas partes serão revisadas.

**Estado da validação:** este manual resulta de leitura e comparação de arquivos. Não foram executados instalação de dependências, testes do Agent, startup, health checks ou `/chat` real na sua elaboração. Todos os blocos “Resultado esperado” são exemplos ou critérios, não registros de execução bem-sucedida.

O sucesso final exige, em conjunto:

- HTTP 200 no `/chat` local;
- resposta produzida pelo fluxo original do Agent;
- chamada real ao LLM através do Gateway Outbound.

Um servidor aberto, um health check verde ou um teste com resposta simulada ainda não concluem o Hello World.

### Convenções

| Expressão | Significado neste manual |
|---|---|
| **CONFIRMADO** | Está demonstrado em arquivo local, com o escopo indicado. Não significa execução aprovada |
| **INFERIDO** | Interpretação fundamentada, mas sem observação direta suficiente |
| **NÃO DETERMINADO** | Falta evidência; não será preenchido por suposição |
| Raiz do projeto | Pasta que contém `setup.py`, `requirements.txt`, `agent_config.yaml` e `plg_agent_consult_fin/` |
| Terminal A | Pengwin Terminal usado para preparar e manter o Agent rodando |
| Terminal B | Outro Pengwin Terminal, usado para enviar requisições ao Agent |
| `<...>` | Marcador a substituir localmente; nunca é uma credencial pronta |

Os comandos são para o shell Linux dentro do Pengwin, salvo indicação explícita. Não cole esses blocos em PowerShell. Não copie os delimitadores de Markdown nem o texto dos resultados esperados.

## 2. Visão geral: ambiente e projeto são coisas diferentes

### Parte A — Ambiente de desenvolvimento

**CONFIRMADO na documentação de ambiente:** Pengwin é o instalador/configurador; Pengwin-WSL é uma distribuição baseada no Ubuntu; Pengwin-rede é outra imagem com serviços de conectividade. Ubuntu não é uma distribuição adicional instalada “abaixo” do Pengwin-WSL.

```text
Windows
  └── WSL2
       ├── Pengwin-WSL = Ubuntu customizado para desenvolvimento no BB
       │    └── Pengwin Terminal → shell → Git / Python / ferramentas
       │                             └── certificados e proxy configurados
       └── Pengwin-rede → serviços de conexão corporativa

Aplicação Pengwin → instala/configura as partes do ambiente
Pengwin-CLI       → oferece comandos dentro do ambiente
```

O shell ativo ainda precisa ser verificado: a documentação não prova que seja zsh. O capítulo 6 faz essa verificação sem abrir arquivos pessoais de inicialização.

### Parte B — Projeto CONSULT FIN

```text
GitHub [origem concreta NÃO DETERMINADA nesta edição]
  → clone já realizado → raiz do projeto → branch pessoal
  → Python escolhido → .venv → dependências → configuração
  → Uvicorn / FastAPI
       └── startup: descoberta MCP → construção do LLM → compilação LangGraph

Terminal B: POST /chat
  → FastAPI → guardrails de entrada → LangGraph
  → Gateway Outbound (AppKey + mTLS) → LLM
  → validação do texto → guardrails de saída → resposta JSON

Se houver ferramentas carregadas:
  LangGraph → ferramentas MCP / RAG habilitado → LangGraph → LLM
```

**CONFIRMADO:** o YAML fornecido tem RAG e curador externo desativados. Os controles locais de entrada/saída continuam ativos. MCP é uma integração separada; ele não fica entre o Gateway e o LLM. Sem ferramentas, o grafo chama o LLM diretamente.

## 3. O que é Pengwin

Segundo [ambiente_pengwin.md](ambiente_pengwin.md), Pengwin automatiza a configuração do computador de desenvolvimento no BB. O aplicativo desktop instala/configura componentes; o Pengwin-CLI fornece utilitários no terminal.

| Tema | Evidência e classificação |
|---|---|
| Pengwin-WSL | **CONFIRMADO:** variação da imagem oficial Ubuntu, com arquivos de trabalho e ferramentas |
| WSL2 | **CONFIRMADO:** a documentação identifica Pengwin-WSL como distribuição WSL2 |
| Pengwin-rede | **CONFIRMADO:** imagem responsável por serviços de conexão à rede empresarial |
| Sistemas suportados documentados | **CONFIRMADO:** Windows 11 e Ubuntu 24.04 LTS. Há trechos históricos citando Ubuntu 22.04; isso não determina a versão instalada no seu computador |
| Shell zsh | **NÃO DETERMINADO:** menções a `.zshrc` não comprovam shell padrão nem shell ativo |
| Atualização | **CONFIRMADO:** atualizar o aplicativo Pengwin e atualizar/reconfigurar a distribuição são etapas distintas |

Você não precisa reinstalar o WSL para seguir este guia. Não use opções de remoção ou recriação de imagem para corrigir um erro isolado do projeto: elas podem atingir seus arquivos de trabalho.

### 3.1 Identificar o Pengwin instalado

#### O que vamos fazer

No **Terminal A, dentro da raiz do projeto**, consultar os comandos oferecidos pelo ambiente. Essas consultas não alteram o projeto.

#### Comando

```bash
versao
ajuda
```

#### O que esse comando significa

`versao` informa a versão do Pengwin-CLI. `ajuda` lista os comandos habilitados nessa instalação. Versão do CLI não é versão do Python nem prova de que todos os pacotes opcionais foram instalados.

#### Resultado esperado

```text
Informação de versão do Pengwin-CLI
Lista de comandos disponíveis nessa instalação
```

O formato e o número da versão são **NÃO DETERMINADOS** nesta análise.

#### Se der erro

`command not found` pode significar terminal errado, CLI não configurado ou versão diferente. Confirme que abriu o atalho Pengwin Terminal. Não tente instalar um pacote de mesmo nome por tentativa. Procure o suporte de ambiente se a instalação não oferecer esses comandos.

#### Próximo passo

Leia como rede e certificados participam do ambiente.

## 4. Como o ambiente local funciona

### 4.1 Proxy, certificados e rede corporativa

Proxy é um intermediário usado para determinadas conexões. Ele não substitui DNS, rota de rede ou autenticação da aplicação.

**CONFIRMADO na documentação fornecida:**

- Desde a versão 1.8.0 documentada, o WSL usa por padrão o proxy Windows/NTLM. Stunnel é opcional no WSL; a instalação Ubuntu nativa usa o proxy Linux/Stunnel.
- A configuração é feita pelo Pengwin. Aplicações instaladas manualmente podem exigir análise específica.
- Funcionários devem habilitar o proxy conforme o procedimento Pengwin; contratados podem ter outra necessidade. Este guia não muda esse estado automaticamente.
- Pengwin-rede e VPNKIT participam da conectividade. A documentação exige rota VPN funcional para os recursos internos citados.
- As CAs corporativas citadas são AC Raiz v3, AC Servidores v3 e AC Usuários v3. O documento aponta PKI BB para certificados adicionais, mas não entrega um roteiro completo de instalação manual.
- `reconfigurar` atualiza configurações/credenciais e instala certificados recentes; é indicado quando a senha SISBB muda ou ferramentas deixam de funcionar.

**NÃO DETERMINADO:** modo de proxy atualmente ativo, endereços efetivos dos resolvedores, rotas do seu computador, versão do VPNKIT e se o Gateway está liberado para sua estação. Não copie endereços de proxy, senhas ou arquivos de outra pessoa.

DNS traduz nomes de máquinas em endereços. Resolver o nome não prova autorização na aplicação. Acessar um repositório corporativo não prova acesso ao Gateway; são destinos e autenticações diferentes.

### 4.2 Ferramentas fornecidas

| Ferramenta/grupo | O que o documento permite afirmar |
|---|---|
| Git, certificados e configuração de proxy | Fazem parte do ambiente descrito |
| Windows Terminal | Instalado por padrão segundo o documento |
| OaaS-CLI | Descrito como pré-instalado |
| Node/NVM/GAW-Reverse | Ofertados no pacote Plataforma |
| Java/Maven/Docker/Kubernetes/OpenShift | Ofertados no pacote ARQ3 |
| Ferramentas Android | Ofertadas no pacote Mobile |
| pyenv | Pacote opcional para gerenciar versões Python |
| core | Sempre instalado segundo o documento |

Oferta não equivale a presença no seu computador. O manual não pressupõe Docker, pyenv ou Python 3.11 instalados só porque são citados.

### 4.3 Docker não é necessário para este Hello World

O caminho principal usa Python e `.venv`. O Dockerfile foi analisado, mas construir a imagem não é um pré-requisito para rodar localmente.

**CONFIRMADO:** o Pengwin configura DNS do Docker no daemon, incluindo referências Windows/VPNKIT e VPN. A documentação explica que configurações de proxy precisam chegar aos containers conforme cada projeto. Um hostname existente apenas na rede Docker não passa a existir automaticamente fora dela.

Certificados do WSL também não aparecem automaticamente dentro de um container. O exemplo de `docker run` do README não monta os certificados: caminhos locais no `.env` não criam arquivos na imagem. O `.dockerignore` não exclui genericamente certificados/chaves; mantenha esse material fora do repositório e do contexto de build. Não é necessário fazer build neste percurso.

### 4.4 Acesso a aplicações no WSL

Dentro do próprio WSL, `localhost` identifica o ambiente local. Para acesso pelo Windows, a documentação Pengwin recomenda iniciar a aplicação escutando em `0.0.0.0`. Isso significa aceitar conexões nas interfaces disponíveis, não navegar para um servidor chamado “0.0.0.0”.

O documento menciona o endereço `192.168.127.2`, mas o IP efetivo da estação é **NÃO DETERMINADO**. Não o fixe como endereço obrigatório. Primeiro valide pelo Terminal B dentro do Pengwin; depois, se necessário, tente `http://localhost:8080/docs` no navegador Windows. Não configure exposição pública: este Agent não implementa autenticação própria no `/chat`.

### 4.5 Recuperação de configuração Pengwin, somente se necessária

#### O que vamos fazer

Se houve troca de senha SISBB ou falha de configuração corporativa, usar o procedimento documentado. **Terminal Pengwin, qualquer pasta**. Essa ação afeta configurações do ambiente, não apenas CONSULT FIN; não é um passo obrigatório para um ambiente saudável.

#### Comando

```bash
reconfigurar
```

#### O que esse comando significa

Abre o fluxo do Pengwin para solicitar dados e reconfigurar ferramentas. Informe credenciais somente no fluxo local autorizado. Não acrescente senha como argumento de comando e não a cole em chats.

#### Resultado esperado

```text
Solicitações interativas do Pengwin
Conclusão da reconfiguração sem erro
```

O texto exato depende da versão. Isso não fornece, por si só, o certificado cliente do Agent.

#### Se der erro

Use `ajuda` do passo 3.1 para confirmar disponibilidade. Se continuar falhando, acione suporte Pengwin com descrição do sintoma e versão, sem anexar arquivos pessoais. **Não execute `diagnosticar` neste roteiro:** o documento informa que ele captura `.bashrc`, `.zshrc` e `.profile`. Não compartilhe logs completos sem revisão de dados sensíveis.

#### Próximo passo

Confira os pré-requisitos do projeto.

## 5. Pré-requisitos e pontos de parada

| Pré-requisito | Necessário para | Se estiver ausente |
|---|---|---|
| Pengwin funcional e pasta Linux do projeto | Todos os passos | Resolver o ambiente primeiro |
| Clone Git com origem esperada | Branch e identificação da versão | Parar no capítulo 7; uma pasta extraída não comprova clone |
| Python adequado e pip/venv | Instalação local | Seguir capítulo 9; não alterar Python global |
| Acesso aos pacotes necessários | Instalação | Resolver acesso/proxy/CA com o ambiente BB |
| AppKey autorizada para o Gateway/modelo | Startup e chamada útil | Obter pelo processo autorizado da equipe |
| Certificado cliente, chave correspondente e CA | mTLS | Obter material autorizado para uso local |
| DNS/rota/acesso ao Gateway | Chamada real | Resolver conectividade com responsáveis |
| MCP | Uso de ferramentas | Não bloqueia obrigatoriamente o Hello World sem ferramentas |

O README e `.env.example` dizem que a AppKey é recebida por e-mail e que certificados vêm de secrets do container provisionado. Isso é evidência de origem descrita, **não um procedimento completo nem autorização para extração**. Responsável, solicitação, permissões e forma aprovada de entrega local: **NÃO DETERMINADO**. Solicite esses itens pelos canais internos autorizados; não extraia secrets Kubernetes com comandos deste guia.

Guarde certificados e chave fora da pasta do projeto. Este manual não contém e não solicita valores reais, conteúdo de `.env`, chave privada ou credenciais GitHub.

## 6. Conhecendo o terminal

### 6.1 Descobrir onde você está

#### O que vamos fazer

No **Terminal A**, confirmar a pasta atual antes de criar qualquer arquivo.

#### Comando

```bash
pwd
```

#### O que esse comando significa

`pwd` mostra o caminho da pasta atual. Um caminho Linux usa `/`. O exemplo abaixo representa uma pasta de projeto dentro da área pessoal do usuário `wsl`; seu usuário e nome de pasta podem ser outros.

#### Resultado esperado

```text
/home/wsl/plg-agent-consult-fin
```

#### Se der erro

Se aparecer uma pasta inesperada, não avance. Se estiver em `/mnt/c/...`, os arquivos estão no disco Windows; a documentação orienta trabalhar com projetos na área Linux do WSL. Não mova automaticamente arquivos ou clones durante este roteiro: confirme a localização apropriada com a equipe.

#### Próximo passo

Confirme os arquivos da raiz.

### 6.2 Reconhecer a raiz e guardar seu caminho

#### O que vamos fazer

No **Terminal A, na pasta mostrada por `pwd`**, conferir quatro arquivos que identificam o projeto e guardar seu caminho apenas neste terminal.

#### Comando

```bash
ls README.md setup.py requirements.txt agent_config.yaml
```

```bash
CONSULT_FIN_DIR="$PWD"
```

#### O que esse comando significa

`ls` lista os nomes solicitados. `CONSULT_FIN_DIR` é uma variável local para lembrar o caminho; `$PWD` já contém a pasta atual. As aspas preservam espaços. A atribuição não cria arquivo e não modifica uma variável do sistema.

#### Resultado esperado

```text
README.md  agent_config.yaml  requirements.txt  setup.py
```

A ordem pode mudar. O segundo bloco normalmente não imprime nada. Anote o caminho não secreto para abrir o Terminal B depois; a variável não aparecerá automaticamente nele.

#### Se der erro

`No such file or directory` indica pasta errada ou cópia incompleta. Não instale dependências até localizar a raiz. Nas cópias analisadas existe uma pasta duplicada dentro da externa; o leitor deve trabalhar na raiz efetiva do seu clone, sem instalar ambas.

#### Próximo passo

Confira distribuição e shell.

### 6.3 Verificar distribuição e shell ativo

#### O que vamos fazer

No **Terminal A, raiz do projeto**, consultar somente identificação do sistema e nome do processo do shell.

#### Comando

```bash
grep '^PRETTY_NAME=' /etc/os-release
ps -p $$ -o comm=
```

#### O que esse comando significa

`grep` seleciona a linha de identificação do sistema. `$$` é o identificador do shell atual; `ps` mostra seu nome, sem listar argumentos de outros processos nem ler arquivos de inicialização.

#### Resultado esperado

```text
PRETTY_NAME="Ubuntu 24.04..."
zsh
```

Isso é apenas um exemplo. Se aparecer `bash`, registre bash como shell ativo. Não o renomeie como zsh no seu registro.

#### Se der erro

Se não for Ubuntu/Pengwin ou os comandos não existirem, confirme o terminal com suporte. Os comandos deste guia são preparados para bash/zsh. Outros shells exigem adaptação; não altere o shell padrão para contornar isso.

#### Próximo passo

Valide o repositório Git.

## 7. Conhecendo o Git e identificando sua versão de trabalho

Git guarda o histórico local de arquivos. GitHub hospeda repositórios e colaboração. Um commit identifica uma versão; branch é uma linha de trabalho. `origin` é um nome convencional de conexão com outro repositório, não prova de que o destino é GitHub.

**NÃO DETERMINADO nesta edição:** remote/URL GitHub, branch atual/default, commit e identidade do checkout. Os passos abaixo permitem ao leitor verificá-los em seu clone. Referências a Fontes BB nos arquivos e workflows GitHub não comprovam a URL de origem.

### 7.1 Confirmar o repositório e o estado dos arquivos

#### O que vamos fazer

No **Terminal A, raiz do projeto**, verificar se Git reconhece a pasta e se já existem alterações.

#### Comando

```bash
git rev-parse --is-inside-work-tree
git rev-parse --show-toplevel
git status --short
```

#### O que esse comando significa

O primeiro comando confirma a área de trabalho Git. O segundo mostra a raiz reconhecida pelo Git. O terceiro lista arquivos modificados, adicionados ou não rastreados sem mostrar seu conteúdo. Nenhum deles muda arquivos.

#### Resultado esperado

```text
true
/home/wsl/plg-agent-consult-fin
```

Para uma árvore limpa, o terceiro comando não imprime nada. `M` indica modificação; `??` indica arquivo não rastreado. Ausência de saída aqui é um resultado útil.

#### Se der erro

`fatal: not a git repository` significa que este checkpoint não passou. Não execute `git init` para fingir que a cópia é o clone esperado. Localize o clone correto. Se houver alterações, entenda com o proprietário o que são; não use reset, limpeza, stash ou descarte automático. Se a raiz Git for uma pasta diferente da raiz do projeto, confirme a organização antes de continuar.

#### Próximo passo

Confira o destino de `origin`.

### 7.2 Ver o remote sem imprimir credenciais embutidas usuais

#### O que vamos fazer

No **Terminal A, raiz do projeto**, mostrar os remotes com ocultação de usuário/senha em URLs HTTP e parâmetros de consulta. Observe o resultado localmente; não compartilhe URLs que ainda contenham material sensível.

#### Comando

```bash
git remote -v | sed -E \
  's#(https?://)[^/@[:space:]]+@#\1[CREDENCIAL_OCULTA]@#g; s#[?][^[:space:]]*#[PARAMETROS_OCULTOS]#g'
```

#### O que esse comando significa

`git remote -v` consulta nomes e endereços. O símbolo `|` envia a saída para `sed`, que substitui possíveis credenciais antes da impressão. A barra `\` continua o comando na linha seguinte: não coloque espaços depois dela. Essa ocultação cobre formatos usuais, não todos os possíveis formatos de segredo.

#### Resultado esperado

```text
origin  https://github.com/<ORGANIZACAO>/<REPOSITORIO>.git (fetch)
origin  https://github.com/<ORGANIZACAO>/<REPOSITORIO>.git (push)
```

Também pode aparecer formato SSH com `git@github.com:`. Organização e repositório precisam ser os esperados pela equipe. `fetch` e `push` aqui são rótulos; nenhuma transferência foi solicitada.

#### Se der erro

Sem `origin`, host diferente ou projeto desconhecido: pare e confirme a origem. Um host corporativo só deve ser identificado como GitHub Enterprise com evidência da equipe. Não substitua o remote por um endereço presumido nem desative validação de certificado Git. Autenticação GitHub não está estabelecida pela documentação Pengwin disponível.

#### Próximo passo

Registre branch e commit iniciais.

### 7.3 Registrar branch e commit de partida

#### O que vamos fazer

No **Terminal A, raiz do projeto**, identificar a versão exata que será usada, sem modificar histórico.

#### Comando

```bash
git branch --show-current
git rev-parse HEAD
```

```bash
CONSULT_FIN_BRANCH_INICIAL="$(git branch --show-current)"
CONSULT_FIN_COMMIT_INICIAL="$(git rev-parse HEAD)"
```

#### O que esse comando significa

O primeiro bloco imprime branch e identificador completo do commit. Anote-os no seu registro de onboarding. O segundo guarda esses valores somente neste terminal; `$(...)` usa a saída do comando como valor. Isso não cria commit nem branch.

#### Resultado esperado

```text
<BRANCH_ATUAL>
<IDENTIFICADOR_COMPLETO_DO_COMMIT>
```

Os marcadores acima representam saídas reais a observar, não texto para executar.

#### Se der erro

Branch vazia pode significar `detached HEAD`: há commit selecionado sem branch ativa. Não escolha uma base arbitrária. Confirme com a equipe qual versão usar. Commit ausente também impede registrar a versão original.

#### Próximo passo

Identifique a branch default remota.

### 7.4 Consultar a branch default

#### O que vamos fazer

No **Terminal A, raiz do projeto**, após validar `origin`, consultar seu HEAD remoto. Isso faz uma consulta de rede, mas não faz push, merge ou checkout.

#### Comando

```bash
git ls-remote --symref origin HEAD
```

#### O que esse comando significa

`ls-remote` consulta referências do servidor. `--symref` permite mostrar para qual branch o HEAD remoto aponta. O valor abaixo é ilustrativo; não assuma `main` antes de ler sua saída.

#### Resultado esperado

```text
ref: refs/heads/main HEAD
<IDENTIFICADOR_DO_COMMIT_REMOTO> HEAD
```

#### Se der erro

Falha de autenticação, DNS ou certificado: a default remota continua **NÃO DETERMINADA**. Não forneça token como argumento de terminal. Use o mecanismo corporativo de autenticação autorizado. A branch default não é necessariamente a versão que sua equipe quer validar; não troque de branch nem faça pull automaticamente.

#### Próximo passo

Crie sua branch pessoal a partir do commit inicial autorizado.

## 8. Criando sua branch pessoal

**CONFIRMADO:** `.github/workflows/ci.yaml` aceita eventos em `main`, `fix/**`, `feat/**` e `feature/**`. Isso confirma padrões aceitos pela configuração, não a existência de branches nem uma convenção obrigatória da equipe. Usaremos `feature/` como escolha compatível com esse arquivo. Branches realmente existentes: **NÃO DETERMINADO** nesta edição.

### 8.1 Criar a branch sem publicar

#### O que vamos fazer

No **Terminal A, raiz do projeto**, com árvore limpa e commit inicial confirmado, criar uma linha de trabalho pessoal. Substitua `seu-nome` por um identificador simples, sem espaços, antes de executar.

#### Comando

```bash
git switch -c feature/seu-nome-local-validation
```

```bash
git status --short
git branch --show-current
git rev-parse HEAD
```

#### O que esse comando significa

`switch -c` cria a branch no commit atual e passa a usá-la. Não baixa alterações. Os comandos seguintes conferem que a árvore continua limpa, o nome mudou e o commit permanece o inicial. Criar uma branch não copia a pasta inteira.

#### Resultado esperado

```text
Switched to a new branch 'feature/seu-nome-local-validation'
feature/seu-nome-local-validation
<MESMO_COMMIT_INICIAL>
```

Mensagens podem estar em português. Nenhum push será feito neste roteiro.

#### Se der erro

Se a branch já existir, não a apague nem a sobrescreva. Confirme se é sua e se deve ser reutilizada ou escolha outro nome pessoal autorizado. Para voltar à branch inicial, use o procedimento opcional seguinte somente com árvore limpa.

#### Próximo passo

Confira o Python no capítulo 9.

### 8.2 Voltar à branch inicial, somente se necessário

#### O que vamos fazer

No **mesmo Terminal A, raiz do projeto**, abandonar a seleção da branch nova sem apagá-la. Execute apenas se deseja voltar e se `git status --short` estiver sem alterações.

#### Comando

```bash
git switch "$CONSULT_FIN_BRANCH_INICIAL"
```

#### O que esse comando significa

Seleciona a branch cujo nome foi guardado no passo 7.3. A branch pessoal permanece disponível. Não há exclusão de histórico.

#### Resultado esperado

```text
Switched to branch '<BRANCH_INICIAL>'
```

#### Se der erro

Em outro terminal, a variável pode estar vazia. Não substitua o nome por suposição. Consulte o registro feito no passo 7.3. Se Git recusar devido a alterações, preserve-as e peça orientação.

#### Próximo passo

Confira o Python.

## 9. Python: sistema, projeto e gerenciador de versões

| Camada | Para que serve |
|---|---|
| Python do sistema | Faz parte do ambiente Linux e pode ser usado por suas ferramentas. Não será substituído |
| Python escolhido para o projeto | Interpretador usado para criar o ambiente do CONSULT FIN |
| pyenv | Gerencia instalações de diferentes versões Python; ofertado como pacote opcional pelo Pengwin |
| `.venv` | Pasta de isolamento de pacotes deste projeto, criada a partir do Python escolhido |
| pip da `.venv` | Instalador que colocará bibliotecas nesse ambiente isolado |

**CONFIRMADO:** `setup.py` aceita Python `>=3.11`; `aic.json` indica `3.11`; o Dockerfile usa imagem `3.11.6`. **Escolha deste guia:** Python **3.11.x como referência preferencial**, para alinhar com a linha de execução declarada. A evidência não exige instalar exatamente o patch antigo 3.11.6 no desktop.

Python 3.12 não está excluído pelo `setup.py`. Sua compatibilidade efetiva com a combinação resolvida de dependências é **NÃO DETERMINADA**, não “incompatível”. A menção histórica a Python 3.12.x também não comprova o que existe no terminal atual.

### 9.1 Conferir o interpretador disponível

#### O que vamos fazer

No **Terminal A, raiz do projeto**, procurar Python 3.11 sem alterar a versão global.

#### Comando

```bash
command -v python3.11
python3.11 --version
```

#### O que esse comando significa

`command -v` informa onde o shell encontra o executável; pode ser um caminho do sistema ou um shim do pyenv. `--version` mostra a versão executada de fato.

#### Resultado esperado

```text
<CAMINHO_DO_EXECUTAVEL_OU_SHIM>
Python 3.11.x
```

#### Se der erro

Se aparecer `command not found`, ou se um shim do pyenv disser que a versão não está selecionada, siga o passo 9.2. Não crie links simbólicos sobre o Python do sistema, não execute instalação global com sudo e não substitua automaticamente 3.11 por 3.12 para esconder a pendência.

#### Próximo passo

Se 3.11 funcionou, crie a `.venv` no capítulo 10; caso contrário, confira o pyenv.

### 9.2 Identificar a disponibilidade do pyenv

#### O que vamos fazer

No **Terminal A, raiz do projeto**, verificar o gerenciador ofertado pelo Pengwin. Este é um diagnóstico opcional; não instala Python.

#### Comando

```bash
command -v pyenv
pyenv versions
```

#### O que esse comando significa

O primeiro comando verifica presença. O segundo lista versões conhecidas pelo gerenciador e indica a seleção ativa. Uma lista que só contenha `system` não comprova Python 3.11 instalado.

#### Resultado esperado

```text
<CAMINHO_DO_PYENV>
Lista de versões Python instaladas, ou somente system
```

#### Se der erro

**Ponto de parada:** a documentação de `ambiente/` confirma o pacote pyenv, mas apenas remete a outro documento, não fornecido, para seu uso detalhado. Procedimento completo BB de instalação de 3.11.x, dependências de compilação, origem do download e configuração dos shims: **NÃO DETERMINADO**. Solicite ao suporte Pengwin a disponibilização/seleção local de Python 3.11.x pelo pacote pyenv, sem alterar o Python global. Não invente comandos de instalação corporativa a partir de tutoriais genéricos.

Mesmo com pyenv presente, a conclusão desse passo é ter `python3.11 --version` funcionando no projeto. Este manual não promete resolver a lacuna de provisionamento com a evidência atual.

#### Próximo passo

Depois que 9.1 apresentar Python 3.11.x, crie a `.venv`.

## 10. Ambiente virtual

### 10.1 Verificar se já existe uma `.venv`

#### O que vamos fazer

No **Terminal A, raiz do projeto**, evitar misturar uma instalação anterior com o primeiro onboarding.

#### Comando

```bash
if [ -e .venv ]; then
  printf '%s\n' '.venv já existe: confirme sua origem antes de continuar.'
else
  printf '%s\n' '.venv ainda não existe.'
fi
```

#### O que esse comando significa

`[ -e ... ]` testa a existência do caminho. `if/else/fi` escolhe uma das mensagens. `printf` apenas imprime texto. Não há exclusão nem instalação.

#### Resultado esperado

```text
.venv ainda não existe.
```

#### Se der erro

Se já existir, não recrie por cima. Confirme se é uma venv Linux deste projeto e qual Python a originou. Se for reutilizá-la por orientação da equipe, avance para ativação e valide os caminhos/versão. Uma `.venv` criada no Windows não deve ser reaproveitada como venv Linux.

#### Próximo passo

Crie a venv se ela ainda não existir.

### 10.2 Criar o isolamento

#### O que vamos fazer

No **Terminal A, raiz do projeto**, criar a pasta `.venv` usando Python 3.11.

#### Comando

```bash
python3.11 -m venv .venv
```

#### O que esse comando significa

`python3.11` escolhe o interpretador. `-m venv` pede para executar o módulo de criação de ambientes virtuais. `.venv` é o diretório de destino. Nele ficarão executáveis, configuração e bibliotecas locais; o código do Agent continua fora dessa pasta.

#### Resultado esperado

```text
O comando termina sem mensagem de erro e devolve o prompt.
```

É normal não imprimir nada. A ativação e a conferência seguintes verificarão o resultado.

#### Se der erro

`No module named venv`, erro de `ensurepip` ou permissão: o Python selecionado pode estar incompleto ou a pasta pode não ser gravável. Resolva a instalação pelo procedimento Pengwin da equipe. Não use sudo para criar a venv. Não continue com uma venv parcialmente criada sem revisão.

#### Próximo passo

Ative a venv.

### 10.3 Ativar e conferir

#### O que vamos fazer

No **Terminal A, raiz do projeto**, fazer este terminal preferir os programas da `.venv`.

#### Comando

```bash
source .venv/bin/activate
```

```bash
which python
python --version
python -m pip --version
```

#### O que esse comando significa

`source` executa o arquivo de ativação no shell atual. Ele muda a busca de executáveis desse terminal. `which python` mostra qual será usado; `python -m pip` garante que o pip pertence ao Python selecionado.

#### Resultado esperado

```text
/home/wsl/plg-agent-consult-fin/.venv/bin/python
Python 3.11.x
pip <VERSAO> from /home/wsl/plg-agent-consult-fin/.venv/lib/python3.11/site-packages/pip (python 3.11)
```

O prompt pode ganhar o prefixo `(.venv)`, mas isso sozinho não basta. Caminho e versão são a confirmação. A ativação vale somente neste terminal.

#### Se der erro

Se Python apontar para fora da `.venv`, não instale pacotes ainda. Confira a pasta e repita a ativação. `No module named pip` indica venv incompleta: retorne à preparação do Python; não use um pip global como substituto.

#### Próximo passo

Instale as dependências de runtime no capítulo 11.

### 10.4 Sair da venv, somente quando precisar

#### O que vamos fazer

No **terminal em que a venv está ativa**, desfazer a ativação sem apagar arquivos. Não execute agora se vai continuar a instalação.

#### Comando

```bash
deactivate
```

#### O que esse comando significa

Restaura a busca de executáveis anterior. Não desinstala pacotes, não apaga `.venv` e não descarrega variáveis que você tenha carregado do `.env`.

#### Resultado esperado

```text
O prompt retorna; o prefixo (.venv), se existia, desaparece.
```

#### Se der erro

`command not found: deactivate` geralmente indica que a venv não está ativa nesse shell. Não é necessário apagar nada. Para recomeçar uma instalação, peça revisão da pasta `.venv` exata antes de removê-la; este guia não oferece limpeza recursiva automática.

#### Próximo passo

Quando retomar, repita 10.3 antes de usar pip ou executar o Agent.

## 11. Dependências de runtime

Dependência é uma biblioteca usada pelo projeto. FastAPI recebe HTTP; Uvicorn mantém o servidor; LangGraph organiza o fluxo; LangChain/OpenAI conectam ao modelo; HTTPX faz requisições; PyYAML lê configuração; OpenTelemetry participa da observabilidade.

### 11.1 O que foi encontrado nos arquivos

**CONFIRMADO:** não há `pyproject.toml`, arquivo de lock, `setup.cfg` ou `pytest.ini` na cópia analisada. O empacotamento está em `setup.py`. As dependências usam mínimos ou não fixam versão; por isso dois dias de instalação podem resolver versões diferentes.

| Diferença | `requirements.txt` | `setup.py` |
|---|---|---|
| LangGraph | `>=1.0.0` | `>=0.2` |
| `langchain` | Incluído | Não listado diretamente |
| `rapidfuzz` | `>=3.9` | Não listado diretamente |
| `requests` | Comentário diz substituído por HTTPX | Incluído como dependência |
| Testes | Não instala pytest diretamente | Extras `unit` e `integration` |

O procedimento documenta os dois passos do README: requirements e pacote editável. Isso preserva a configuração original. Não há conflito de resolução comprovado, nem instalação bem-sucedida comprovada nesta edição.

### 11.2 Como interpretar `pip.conf`

**Análise, não instrução de configuração:** o arquivo do projeto define índice PyPI corporativo, timeout 60, CA `etc/ssl/certs/bb.bundle.crt` e uma opção `trusted-host` para o host corporativo. O caminho da CA é relativo, sem `/` inicial; não equivale automaticamente a um caminho válido no Pengwin.

O Dockerfile copia esse arquivo para `/etc/pip.conf` e instala com `uv`; a precedência efetiva entre uv, ambiente e imagem base não foi validada. Um `pip.conf` apenas dentro da raiz do projeto não é automaticamente a configuração de pip da sua venv.

**Não copie esse arquivo para a configuração global ou da venv como solução automática. Não use desativação de TLS, `--trusted-host` ou `sslVerify=false` para consertar erros.** As duas instalações seguintes usam a configuração de pip já existente no ambiente. Se falharem por índice, proxy ou certificado, resolva o ambiente e o acesso autorizado com a equipe BB.

Não imprima a configuração completa do pip/proxy: ela pode conter credenciais. Não há caminho de CA corporativa efetivamente validado na estação nesta análise. A configuração segura de índice/CA, caso necessária, deve vir do procedimento Pengwin/BB aplicável, não de uma cópia indiscriminada do arquivo do projeto.

### 11.3 Instalar a lista de runtime

#### O que vamos fazer

No **Terminal A, raiz do projeto, `.venv` ativa**, instalar as bibliotecas declaradas em requirements.

#### Comando

```bash
python -m pip install -r requirements.txt
```

#### O que esse comando significa

`install` instala pacotes. `-r` informa que a lista está em um arquivo. As bibliotecas vão para a venv validada no capítulo 10. Este passo acessa o índice de pacotes configurado e pode demorar.

#### Resultado esperado

```text
Collecting ...
Installing collected packages ...
Successfully installed ...
```

`Requirement already satisfied` também pode ser normal. Versões e quantidade de pacotes variam. Não copie logs de instalação para chats sem verificar se contêm URLs autenticadas.

#### Se der erro

Certificado, proxy 407, timeout ou resolução de nomes são falhas de acesso, não razão para desabilitar TLS. `No matching distribution found` pode indicar versão Python, pacote indisponível ou índice incorreto. `ResolutionImpossible` exige análise de dependências; não altere os requisitos originais apenas para passar. Se interromper com Ctrl+C, a venv pode ficar parcialmente instalada; resolva a causa e repita este passo antes de avançar.

#### Próximo passo

Instale o pacote do projeto em modo editável.

### 11.4 Instalar o próprio projeto

#### O que vamos fazer

No **Terminal A, raiz do projeto, `.venv` ativa**, registrar o pacote Python do Agent.

#### Comando

```bash
python -m pip install -e .
```

#### O que esse comando significa

`.` significa a pasta atual. `-e` significa editável: o pacote instalado referencia o código dessa pasta, facilitando desenvolvimento. Não manda alterações ao GitHub e não cria branch. Dependências adicionais de `setup.py` também podem ser instaladas.

#### Resultado esperado

```text
Successfully installed plg_agent_consult_fin-0.1.1
```

O nome pode aparecer com hífens normalizados e junto de outros pacotes. A versão 0.1.1 está confirmada na cópia analisada; outro clone deve ser identificado pelo seu próprio commit.

#### Se der erro

Arquivo `setup.py`/README ausente: confira a raiz. Falha de build ou resolução: registre a categoria do erro sem secrets. Não use instalação global nem modifique o código para contornar. O fato de Python importar algo da pasta atual não prova que este passo foi concluído.

#### Próximo passo

Confira a consistência das dependências.

### 11.5 Conferir a instalação

#### O que vamos fazer

No **Terminal A, raiz do projeto, `.venv` ativa**, verificar requisitos dos pacotes instalados sem chamar o Agent.

#### Comando

```bash
python -m pip check
```

#### O que esse comando significa

Verifica se as dependências declaradas pelos pacotes instalados estão presentes em versões compatíveis. Não abre servidor nem valida comportamento do LLM.

#### Resultado esperado

```text
No broken requirements found.
```

#### Se der erro

Não avance com conflito conhecido. Revise os passos 11.3 e 11.4 e a versão Python. A ausência de lock exige registrar as versões resolvidas na investigação, mas não justifica atualizar tudo indiscriminadamente. Para desfazer o isolamento, use 10.4; não desinstale pacotes globais.

#### Próximo passo

Instale os extras e execute os testes locais.

## 12. Testes antes de subir o Agent

Um mock é um substituto controlado de um componente real. Um teste pode simular “LLM respondeu” para verificar o código ao redor; isso não significa que houve acesso ao Gateway.

**CONFIRMADO por inspeção dos testes:**

| Grupo | O que existe | Dependência externa real |
|---|---|---|
| `tests/unit/` | Configuração, grafo, provider, transporte, RAG, guardrails e validators | Chamadas relevantes substituídas por mocks ou casos locais |
| API em `tests/unit/test_app.py` | HTTP em memória via ASGI; grafo mockado | Não requer servidor Uvicorn ou LLM reais |
| `tests/integration/` | Apenas exemplo dummy que soma números | Nenhuma; não comprova integração do Agent |
| Hello World real | Procedimento do capítulo 19 | Gateway, AppKey, mTLS, rede e modelo |

São 14 arquivos unitários e um `test_*.py` de integração na cópia analisada. Não há aprovação registrada aqui. Testes ASGI não exercitam por si só o startup real: readiness é simulado em teste. Testes dos judges substituem o prompt que contém o defeito já descrito na baseline; eles não comprovam funcionamento desse prompt original com o LLM.

Faça este checkpoint **antes de carregar o `.env` real**, em terminal sem credenciais de runtime previamente exportadas. Se já carregou credenciais nesta sessão, feche esse terminal e abra outro Pengwin, volte à raiz e ative a venv; não imprima o ambiente para conferir. Configurações persistentes externas de telemetria também precisam ser consideradas pela equipe.

### 12.1 Instalar somente agora as ferramentas de teste

#### O que vamos fazer

No **Terminal A, raiz do projeto, `.venv` ativa**, acrescentar pytest e seus auxiliares.

#### Comando

```bash
python -m pip install -e ".[unit,integration]"
```

#### O que esse comando significa

Os extras `unit` e `integration` são listas opcionais declaradas em `setup.py`: pytest, pytest-asyncio e HTTPX. As aspas protegem os colchetes de interpretação pelo shell, especialmente zsh. O modo editável continua usando o mesmo código local.

#### Resultado esperado

```text
Successfully installed ...
```

Pacotes já presentes podem aparecer como satisfeitos. Esse comando instala ferramentas; ainda não executa os testes.

#### Se der erro

`no matches found` no zsh costuma indicar falta de aspas. Erros de acesso a pacote seguem o capítulo 11. Não adicione `--cov`: o extra não declara pytest-cov.

#### Próximo passo

Execute a suíte local.

### 12.2 Executar o checkpoint local

#### O que vamos fazer

No **Terminal A, raiz do projeto, `.venv` ativa e sem `.env` real carregado**, executar a suíte dos dois diretórios explicitamente.

#### Comando

```bash
python -m pytest tests/unit tests/integration
```

#### O que esse comando significa

Executa pytest pelo Python da venv. Os diretórios explícitos evitam coletar também uma eventual cópia duplicada do projeto. Em um clone sem duplicatas, `python -m pytest` é a forma geral; este guia mantém a seleção explícita para tornar o alvo claro.

#### Resultado esperado

```text
collected ... items
...
... passed in ...s
```

Esta é a condição desejada, **não um resultado observado**. Não há número de casos aprovados a prometer. Pytest pode criar cache e arquivos temporários de teste, sem exigir certificados cliente reais.

#### Se der erro

`No module named pytest`: volte a 12.1. Erro de importação: confira venv e runtime. `FAILED` ou `ERROR`: não declare o checkpoint aprovado nem edite o Agent para mascarar a falha. Registre o nome do teste e categoria do erro; investigue com a equipe preservando a versão original.

#### Próximo passo

Se os testes passaram, prepare a configuração do Agent.

### 12.3 Separar grupos, somente para investigação

#### O que vamos fazer

No **Terminal A, raiz do projeto, `.venv` ativa, sem credenciais reais carregadas**, isolar o grupo que precisa de diagnóstico. Não é necessário repetir testes aprovados sem motivo.

#### Comando

```bash
python -m pytest tests/unit
```

```bash
python -m pytest tests/integration
```

#### O que esse comando significa

O primeiro seleciona os unitários, incluindo ASGI com mocks. O segundo seleciona somente o diretório de integração, que nesta cópia é um exemplo genérico.

#### Resultado esperado

```text
Resumo do grupo selecionado, sem FAILED ou ERROR para aprovação
```

#### Se der erro

Investigue o grupo selecionado sem atribuir falha de mock a falta de certificado real. O teste dummy passar não compensa uma falha nos testes do Agent.

#### Próximo passo

Concluído o diagnóstico, prepare o `.env`.

## 13. Configuração do Agent

Existem duas fontes principais. `agent_config.yaml` define modelo, instruções e integrações. As variáveis do processo fornecem credenciais e caminhos. O código não faz uma conversão geral de variáveis de ambiente para todos os campos YAML.

**CONFIRMADO:** o loader busca `agent_config.yaml` primeiro na raiz acima do pacote e depois na pasta atual; mantém a configuração em memória. A aplicação não chama `load_dotenv`. Copiar `.env` não exporta suas variáveis automaticamente.

### 13.1 Variáveis do `.env.example`, uma por uma

| Variável | Função e necessidade |
|---|---|
| `GATEWAY_OUTBOUND_GW_APP_KEY` | AppKey enviada ao Gateway. Lida obrigatoriamente na construção do LLM; ausente causa `KeyError`. Presença não prova validade nem autorização |
| `KEY_STORE_CERT_PATH` | Caminho absoluto para certificado público do cliente, como `tls.crt`. Necessário para o mTLS descrito pelo projeto |
| `KEY_STORE_KEY_PATH` | Caminho absoluto para chave privada correspondente, como `tls.key`. O código só fornece o par ao transporte quando ambos os caminhos estão definidos |
| `TRUST_STORE_CA_PATH` | Caminho para CA/bundle usado para validar o servidor Gateway. Tem precedência sobre `REQUESTS_CA_BUNDLE`. O guia exige preparar uma CA apropriada para o cenário local descrito |
| `RAG_CLIENT_ID` | Token de identificação do RAG. Condicional a RAG habilitado e configurado. Deixar vazio no Hello World com YAML original |
| `GUARDRAIL_EXTERNAL_CLIENT_ID` | Token do curador externo. Condicional a `guardrails.enabled`. O comentário do exemplo menciona `guardrails.external.enabled`, mas esse não é o campo do loader |
| `APPLICATION_INSIGHTS_CONNECTION_STRING` | Configuração sensível do Azure Application Insights. Deixar vazia no percurso mínimo, evitando habilitar o callback/exporter opcional |
| `REQUESTS_CA_BUNDLE` | Bundle de CAs; lido diretamente por RAG/curador e como fallback pelo Gateway. Não é certificado de cliente nem substitui sua chave |
| `SSL_CERT_FILE` | Variável para bibliotecas TLS/SDKs. Não há leitura direta pelo código próprio; seu efeito exato nas dependências resolvidas não foi validado. Se usada, deve apontar para bundle válido |
| `SERVICE_NAME` | Nome incluído nas dimensões das métricas próprias. Substituir o template literal por `plg-agent-consult-fin` |
| `DEPLOY_ENV` | Rótulo de ambiente nas métricas próprias; `desenv` é adequado ao exemplo local. Não muda a URL do Gateway nem o YAML |

O exemplo cita `/etc/ssl/certs/ca-certificates.crt` para WSL/Ubuntu. Isso documenta um caminho esperado de bundle, não comprova que o arquivo da estação contém as CAs necessárias. A CA específica do Gateway continua separada em `TRUST_STORE_CA_PATH`.

### 13.2 Outras configurações relevantes

| Nome | Comportamento confirmado / limite |
|---|---|
| `GUARDRAIL_MAX_INPUT_LEN` | Limite de entrada; padrão 4096 caracteres. Valor não numérico pode falhar durante importação |
| `GUARDRAIL_BLOCK_PII_INPUT` | Padrão `true`; bloqueio local de informações pessoais na entrada |
| `GUARDRAIL_REDACT_PII_OUTPUT` | Padrão `true`; substituição de dados pessoais na resposta |
| `GUARDRAIL_SEMANTIC_ENABLED` | Padrão `true`; comparação lexical aproximada nos validators de toxicidade/conselhos. Não é serviço remoto de embeddings |
| `OTEL_RECORD_CONTENT` | Padrão `true` no callback Azure, quando habilitado. Não é necessário habilitar telemetria para Hello World |
| Nome indicado em `authentication.token_env_var` | Lido se MCP usa bearer. O YAML atual usa `none`; não há token MCP obrigatório nesse arquivo |
| `OTEL_EXPORTER_OTLP_ENDPOINT`, `OTEL_SERVICE_NAME` | Configurações de SDK/instrumentação mencionadas nos artefatos. Não configurar coletor para este percurso mínimo |
| `HOST`, `PORT`, `WORKERS`, `LOG_LEVEL` | README os anuncia, mas o entrypoint próprio usa argumentos de linha de comando, não essas ENV |
| `AZURE_OPENAI_*` | Presentes em fixtures antigas de teste; não são a configuração do provider Gateway ativo |

Não altere o YAML para “simplificar” o teste. Os valores atuais são: provider `gateway_outbound`, modelo `cambio-non-prod-gpt4o`, API version `2024-12-01-preview`, `max_tokens: 4096`, temperatura 0,7 e `top_p: 0,95`. RAG/curador externo desativados; MCP configurado para DNS de cluster. Modelo e URL são configuração, não evidência de autorização efetiva.

### 13.3 Confirmar proteção Git antes de criar o `.env`

#### O que vamos fazer

No **Terminal A, raiz do projeto**, verificar que `.env` e `.venv` são ignorados e não estão rastreados.

#### Comando

```bash
git check-ignore .env .venv
git ls-files -- .env .venv
```

#### O que esse comando significa

`check-ignore` informa caminhos protegidos por regras Git. `ls-files` mostra se já foram incluídos no histórico atual. Ignorar um arquivo não remove seu rastreamento anterior.

#### Resultado esperado

```text
.env
.venv
```

O segundo comando deve ficar sem saída. O `.gitignore` local contém essas regras; não ignora genericamente toda chave/certificado possível.

#### Se der erro

Sem proteção ou com `.env` rastreado, não coloque secrets ali. Confirme o clone e a política com a equipe. Não execute remoção de histórico como parte do onboarding. Certificados continuam fora do repositório.

#### Próximo passo

Crie a cópia local se ainda não existir.

### 13.4 Criar a configuração local sem sobrescrever

#### O que vamos fazer

No **Terminal A, raiz do projeto**, criar `.env` a partir do exemplo somente se o caminho estiver ausente, com permissões restritas na criação.

#### Comando

```bash
if [ -e .env ] || [ -L .env ]; then
  printf '%s\n' '.env já existe: não foi sobrescrito.'
else
  (umask 077; cp .env.example .env)
fi
```

#### O que esse comando significa

O teste verifica arquivo e link simbólico. `cp` copia o exemplo. Os parênteses limitam `umask 077` à cópia: novos arquivos ficam restritos ao usuário, sem mudar permanentemente a configuração do terminal. Se já existe, o conteúdo é preservado.

#### Resultado esperado

```text
Sem saída ao criar; ou aviso de que .env já existe.
```

#### Se der erro

Exemplo ausente: confira raiz. Permissão negada: não use sudo. Se `.env` existente for de origem desconhecida ou for link simbólico, confirme com o proprietário antes de abrir ou executar. Não faça `source` ainda: o exemplo contém marcadores inválidos para uso direto.

#### Próximo passo

Edite o arquivo localmente.

### 13.5 Editar sem expor credenciais no histórico

#### O que vamos fazer

No **Terminal A, raiz do projeto**, abrir o arquivo no editor conectado ao WSL. Esse é o local para preencher valores autorizados, não o histórico do terminal nem uma conversa.

#### Comando

```bash
code .env
```

#### O que esse comando significa

Abre `.env` no VS Code. A documentação Pengwin orienta usar `code` a partir do WSL. Confirme no editor que o arquivo pertence ao projeto Linux correto. Salve em UTF-8 com finais de linha LF.

#### Conteúdo de referência para editar — não executar no terminal

Substitua as atribuições correspondentes no arquivo, sem duplicar nomes. O bloco abaixo contém apenas marcadores; **não é conteúdo lido de um `.env` existente**.

```dotenv
GATEWAY_OUTBOUND_GW_APP_KEY='<APP_KEY>'
KEY_STORE_CERT_PATH='<CAMINHO_CERTIFICADO>'
KEY_STORE_KEY_PATH='<CAMINHO_CHAVE>'
TRUST_STORE_CA_PATH='<CAMINHO_CA>'
```

Preencha valores verdadeiros apenas no editor local. Os caminhos devem começar com `/`, apontando para arquivos Linux fora do clone; um caminho `C:\...` não é um caminho Linux. Aspas simples protegem espaços, `$`, `!` e outros caracteres comuns. Se o valor fornecido contiver uma aspa simples literal, peça orientação para representá-lo corretamente; não o cole em chat. Não inclua comandos, substituições ou scripts dentro do `.env`.

Para o percurso mínimo, ajuste também:

```dotenv
RAG_CLIENT_ID=
GUARDRAIL_EXTERNAL_CLIENT_ID=
APPLICATION_INSIGHTS_CONNECTION_STRING=
REQUESTS_CA_BUNDLE=
SSL_CERT_FILE=
SERVICE_NAME='plg-agent-consult-fin'
DEPLOY_ENV='desenv'
```

Os dois campos de bundle podem ficar vazios neste percurso, que fornece `TRUST_STORE_CA_PATH` explicitamente e não habilita RAG/curador/telemetria. Se o ambiente BB exigir o bundle do sistema para algum SDK, preencha os caminhos validados pela equipe. Não deixe uma variável de caminho preenchida com um arquivo inexistente. Nenhum campo vazio acima fornece autenticação ao Gateway.

#### Resultado esperado

```text
.env salvo localmente, sem marcadores pendentes, sem nomes duplicados
SERVICE_NAME com valor simples, não com {{ codebase_name }}
```

#### Se der erro

Se `code` não estiver disponível, resolva a integração VS Code/WSL descrita na documentação ou use o editor local aprovado pela equipe. Não improvise comandos `echo` contendo secrets. Se não recebeu AppKey/certificados, pare aqui; valores inventados não servem para um Hello World real.

#### Próximo passo

Carregue a configuração neste terminal.

### 13.6 Carregar as variáveis no processo

#### O que vamos fazer

No **Terminal A, raiz do projeto, `.venv` ativa**, carregar somente o `.env` que você acabou de revisar. `source` executa conteúdo como shell; faça isso apenas com arquivo local confiável contendo atribuições.

#### Comando

```bash
set -a
source .env
set +a
```

#### O que esse comando significa

`set -a` passa a exportar as variáveis atribuídas. `source .env` aplica as atribuições no shell atual. `set +a` encerra a exportação automática para atribuições futuras; não apaga o que já foi exportado. O Python iniciado depois herdará esses valores. O Terminal B não precisa receber essas credenciais.

#### Resultado esperado

```text
Os três comandos terminam sem mensagens de erro.
```

#### Se der erro

Erros próximos de `<`, `>` ou `codebase_name` indicam placeholders/aspas não corrigidos. Erros com `\r` podem indicar finais de linha Windows: ajuste LF no editor. Se `source` falhar, execute `set +a` mesmo assim, não inicie o Agent e revise localmente. Um erro de shell pode mostrar a linha problemática: não compartilhe a saída se ela contiver valores sensíveis. Após corrigir, repita o carregamento completo; a tentativa anterior pode ter aplicado apenas parte das variáveis.

Para descarregar as credenciais deste shell ao encerrar o trabalho, feche o Terminal A depois de parar o Agent. `deactivate` não faz isso. Não adicione o `.env` aos arquivos de inicialização pessoal.

#### Próximo passo

Confira presença e caminhos sem revelar valores.

### 13.7 Validar os campos essenciais sem imprimir conteúdo

#### O que vamos fazer

No **Terminal A, raiz do projeto, `.venv` ativa e `.env` carregado**, verificar campos específicos. O código abaixo não abre certificado/chave nem imprime valores das variáveis.

#### Comando

```bash
python - <<'PY'
import os
from pathlib import Path

names = (
    'GATEWAY_OUTBOUND_GW_APP_KEY',
    'KEY_STORE_CERT_PATH', 'KEY_STORE_KEY_PATH', 'TRUST_STORE_CA_PATH',
)
for name in names:
    value = os.getenv(name, '')
    ok = bool(value.strip()) and '<' not in value and '{{' not in value
    if name.endswith('_PATH'):
        ok = ok and Path(value).is_absolute()
        ok = ok and Path(value).is_file() and os.access(value, os.R_OK)
    print(name + ': ' + ('OK local' if ok else 'PENDENTE'))
PY
```

#### O que esse comando significa

`python -` lê um pequeno programa da entrada. `<<'PY'` delimita o bloco sem expandir variáveis do shell. O programa lê apenas quatro nomes, rejeita campos vazios/marcadores e verifica caminhos absolutos de arquivos legíveis. A última linha `PY` deve ficar sozinha, sem espaços antes.

#### Resultado esperado

```text
GATEWAY_OUTBOUND_GW_APP_KEY: OK local
KEY_STORE_CERT_PATH: OK local
KEY_STORE_KEY_PATH: OK local
TRUST_STORE_CA_PATH: OK local
```

`OK local` não valida AppKey, validade do certificado, correspondência entre chave/certificado ou autorização no Gateway. É somente uma verificação de preenchimento/arquivo.

#### Se der erro

Para `PENDENTE`, volte ao editor, revise o campo e recarregue `.env`. Não imprima a variável nem use leitura da chave privada para investigar. Erro Python/importação aqui sugere problema de interpretador, não do LLM.

#### Próximo passo

Entenda o Gateway antes de iniciar o servidor.

## 14. Gateway Outbound

Gateway é a porta de acesso intermediária ao serviço LLM. No código fornecido, o provider ativo é `gateway_outbound`; não se conecta diretamente a um endpoint Azure escolhido por `AZURE_OPENAI_*`.

**CONFIRMADO no YAML/provider:**

| Item | Valor/comportamento |
|---|---|
| Base URL | `https://llms-agentes-ia.outbound.api.hm.bb.com.br/v1` |
| Modelo | `cambio-non-prod-gpt4o` |
| Caminho assíncrono reescrito | `/chat/completions` vira `/cambio-chat-completion` |
| Autenticação HTTP | Remove header Authorization e injeta `X-Application-Key` |
| Versão da API | Acrescenta query `api-version=2024-12-01-preview` |
| Caminho usado pelo grafo | Invocação assíncrona do LLM com transporte customizado |

O valor `api_key="dummy"` dentro do provider é um detalhe de adaptação do SDK; não é a credencial de acesso. A AppKey real vem da variável do processo. Não copie a AppKey para comandos curl de diagnóstico: o `/chat` local faz a chamada autenticada por dentro do Agent.

**INFERIDO:** funcionamento do pip, navegador ou curl externo não garante que o transporte HTTPX customizado tenha o mesmo comportamento de proxy. O código não apresenta configuração explícita de proxy nesse transporte. O roteamento efetivo do Gateway pela combinação instalada de SDK/Pengwin é **NÃO DETERMINADO**. Se houver exigência de proxy incompatível com o caminho original, registre o bloqueante; não altere o Agent nesta validação inicial.

### 14.1 Diagnóstico de DNS do Gateway, se houver dúvida de conectividade

#### O que vamos fazer

No **Terminal A, raiz do projeto**, consultar o nome configurado sem enviar AppKey ou conteúdo de chat. Este passo opcional investiga DNS, não autenticação.

#### Comando

```bash
getent hosts llms-agentes-ia.outbound.api.hm.bb.com.br
```

#### O que esse comando significa

Consulta os mecanismos de resolução de nomes do Linux. Não faz uma chamada de geração ao LLM e não modifica DNS.

#### Resultado esperado

```text
<ENDERECO_IP>  llms-agentes-ia.outbound.api.hm.bb.com.br
```

Podem aparecer aliases ou vários endereços. A estação efetiva não foi consultada nesta análise.

#### Se der erro

Sem saída ou falha de resolução: verifique VPN e configuração Pengwin com a equipe. Não edite `/etc/hosts` ou resolvers com IP presumido. Uma rota via proxy pode ter resolução diferente, portanto esse resultado isolado não é prova definitiva do caminho HTTP completo.

#### Próximo passo

Revise mTLS e a diferença entre os três arquivos.

## 15. mTLS explicado desde o início

TLS protege a conexão e permite validar a identidade do servidor. Em mTLS, o cliente também apresenta um certificado e prova que possui a chave correspondente. Assim, “consegui abrir a URL” e “estou autenticado como a aplicação” são etapas diferentes.

| Arquivo usual | Papel | Cuidados |
|---|---|---|
| `tls.crt` | Certificado do cliente: identifica a aplicação que se conecta | Precisa ser o certificado apropriado e válido para o ambiente |
| `tls.key` | Chave privada: permite provar a identidade do cliente | Nunca publicar, colar em chat ou imprimir; manter sob controle local autorizado |
| `ca.crt` | Autoridade/cadeia usada para validar o certificado do servidor | Não substitui o certificado cliente nem sua chave |

Os nomes são convencionais: seu arquivo pode ter outro nome. O que importa é seu papel e o caminho informado na variável correta. A CA pode ser um bundle com mais de um certificado.

### 15.1 O que o Agent faz com esses arquivos

**CONFIRMADO:** quando os dois caminhos de cliente estão definidos, o provider passa o par ao transporte. Para confiança no servidor, escolhe `TRUST_STORE_CA_PATH`; se estiver vazio, tenta `REQUESTS_CA_BUNDLE`. Quando há CA, cria contexto SSL e carrega o arquivo. Sem CA explícita, usa `verify=True`: o comentário “sem verificação” no provider não corresponde ao código.

Não deixe de validar o servidor por causa de erro de CA. Um arquivo existir não significa ser um certificado válido; erros de formato PEM, chave incompatível ou CA incorreta podem aparecer na construção do cliente, antes mesmo de servir HTTP.

O Pengwin instalar CAs do Banco não significa que ele já provisionou o certificado cliente e a chave privada deste Agent. São funções distintas.

### 15.2 Como interpretar `certificate required`

Ao acessar uma URL HTTPS do Gateway sem certificado cliente, pode aparecer:

```text
certificate required
```

**INFERIDO, dependendo da origem do alerta:** isso pode mostrar que houve resolução do destino, caminho de rede e progresso da negociação TLS até um servidor que exigiu certificado cliente. Não significa que o handshake foi concluído com sucesso, que a AppKey foi aceita ou que o modelo respondeu.

Se houver proxy/intermediário, o alerta pode vir dele, e a resolução pode ter ocorrido no proxy. Sem observar o caminho, não declare que o DNS local e o servidor final foram ambos validados. Diferencie esse erro de `certificate verify failed`, que indica problema ao verificar confiança/identidade de certificado recebido.

Este guia não usa uma visita anônima à URL como critério de sucesso. A verificação completa acontecerá pelo `/chat` do Agent.

### 15.3 Obtenção e armazenamento

O processo autorizado para emitir, entregar, renovar e permitir uso local do material é **NÃO DETERMINADO** nas evidências disponíveis. A referência do projeto a secrets provisionadas não permite deduzir comandos de extração nem permissões do desenvolvedor.

Solicite à equipe responsável AppKey e material mTLS apropriados ao Gateway de homologação configurado, informando que o objetivo é execução local. Confirme onde devem ser armazenados no WSL, o acesso restrito e quem trata renovação. Não coloque esses arquivos dentro do clone. Não use valores de produção por suposição.

## 16. MCP: por que ele pode falhar sem impedir o Hello World

MCP é um protocolo para disponibilizar ferramentas ao Agent. No YAML atual, há um servidor com transporte `streamable_http` e autenticação `none`:

```text
http://plg-mcp-consult-fin.plg-mcp-consult-fin.svc.cluster.local/mcp
```

Esse bloco é identificação da configuração, não um comando. **CONFIRMADO:** a descrição no próprio YAML diz “via rede interna do cluster”. **INFERIDO:** o formato serviço.namespace.svc.cluster.local corresponde ao uso típico de DNS interno Kubernetes; um terminal WSL fora dessa rede não deve presumir que consegue resolvê-lo. Não há servidor MCP local implementado no código fornecido.

### Comportamento confirmado na compilação

```text
FastAPI inicia → graph.compile()
  → MultiServerMCPClient.get_tools()
      ├── sucesso: registra ferramentas encontradas
      └── exceção: warning → tools=[]
  → se RAG habilitado: adiciona ferramenta RAG
  → cria LLM → compila grafo
```

O `try/except` envolve a descoberta conjunta. Não há preservação garantida das ferramentas de outros servidores quando um falha. Com o YAML atual, RAG está desligado; uma falha de descoberta permite o grafo sem ferramentas. A AppKey e a configuração do LLM continuam necessárias.

O warning esperado pode começar assim:

```text
Servidor(es) MCP indisponível(eis), prosseguindo sem ferramentas:
Agente compilado com 0 ferramenta(s)
```

A descoberta ocorre no startup/compilação, não a cada `/chat`. O grafo fica guardado; não há mecanismo próprio de redescoberta periódica. O tempo até uma tentativa de discovery falhar depende das bibliotecas e da rede; o projeto não fixa aqui um timeout global que permita prometer conclusão imediata.

MCP indisponível não deve motivar mudança automática do YAML. Primeiro valide o comportamento original. Se MCP estiver acessível, o modelo pode usar suas ferramentas; `tool_calls_made` não tem obrigação de ser zero. Uma falha na execução de ferramenta depois da descoberta não é necessariamente coberta pelo mesmo tratamento do discovery.

O README menciona autenticação MCP por certificado, mas a factory atual só repassa URL, transporte e bearer quando resolvido. Campos de certificado existem na configuração sem serem aplicados nesse caminho. Não confunda essa limitação com o mTLS implementado no provider do Gateway.

## 17. Subindo o Agent

### 17.1 Iniciar o processo original

#### O que vamos fazer

No **Terminal A, raiz do projeto, `.venv` ativa, testes conferidos e `.env` carregado**, iniciar o serviço. Antes, confirme que os quatro campos de 13.7 estão `OK local`.

#### Comando

```bash
python -m plg_agent_consult_fin \
  --host 0.0.0.0 \
  --port 8080
```

#### O que esse comando significa

`python -m` executa um módulo/pacote como programa. Aqui Python entra em `plg_agent_consult_fin/__main__.py`, que configura logs e inicia Uvicorn com a aplicação FastAPI.

`--host 0.0.0.0` escolhe as interfaces de escuta conforme a orientação Pengwin para acesso pelo Windows. `--port 8080` escolhe o número da porta. Porta é como um ponto de atendimento de um processo dentro da máquina. O padrão do entrypoint é um worker; este guia mantém um único processo de aplicação.

Mantenha o terminal aberto: enquanto o servidor roda, ele não devolve o prompt para novos comandos. Isso é esperado, não travamento por si só.

#### Resultado esperado

```text
Started server process [...]
Waiting for application startup.
... descoberta MCP ou warning de indisponibilidade ...
Agente compilado com ... ferramenta(s)
Application startup complete.
Uvicorn running on http://0.0.0.0:8080
```

A ordem/formatação pode variar. O marco importante é startup completo sem falha. Construir o objeto LLM durante startup não faz a geração que comprova acesso ao modelo.

#### Se der erro

`KeyError` da AppKey: revise exportação. Erro de arquivo/SSL: revise caminhos e material mTLS com a equipe. `No module named ...`: confira venv e instalação. `Address already in use`: não mate um processo desconhecido; use o diagnóstico 20.1. Demora no startup pode estar no discovery MCP; não confunda com um `/chat` em execução.

#### Próximo passo

Abra o Terminal B para os health checks.

### 17.2 Parar o servidor quando necessário

#### O que vamos fazer

No **Terminal A onde o servidor está rodando**, encerrar o processo ao terminar ou antes de recarregar uma configuração corrigida. Não pare agora se ainda vai fazer os health checks.

#### Ação de teclado

```text
Ctrl+C
```

#### O que essa ação significa

Segure Ctrl e pressione C uma vez. Isso solicita interrupção ao processo em primeiro plano. Não é texto para digitar. Nenhum arquivo do projeto é apagado.

#### Resultado esperado

```text
Shutting down
Application shutdown complete.
Finished server process [...]
```

O prompt retorna. Para reiniciar após editar `.env`, recarregue 13.6, confira 13.7 e repita 17.1.

#### Se der erro

Confirme que está no terminal do servidor. Se uma operação demorar a encerrar, não execute comandos de encerramento global de Python/WSL. Identifique o processo específico com apoio da equipe.

#### Próximo passo

Se está encerrando o trabalho, feche o Terminal A; se está validando, mantenha o servidor iniciado e siga ao capítulo 18.

## 18. Health checks em outro terminal

Abra outro Pengwin Terminal pelo mesmo atalho e distribuição: esse será o **Terminal B**. Ele serve para fazer perguntas HTTP ao processo do Terminal A. Não carregue o `.env` com secrets nele; curl para a API local não precisa da AppKey.

### 18.1 Localizar o projeto no Terminal B

#### O que vamos fazer

No **Terminal B**, entrar no caminho anotado no passo 6.1. Substitua o marcador pelo caminho Linux real antes de executar.

#### Comando

```bash
cd '<CAMINHO_ABSOLUTO_DO_PROJETO>'
pwd
```

#### O que esse comando significa

`cd` muda a pasta deste terminal. `pwd` confirma o resultado. Para usar curl não seria obrigatório estar na raiz, mas manter o mesmo diretório torna o procedimento mais fácil de acompanhar. Não é necessário ativar venv para os curls.

#### Resultado esperado

```text
/home/wsl/plg-agent-consult-fin
```

#### Se der erro

Confira o caminho anotado, sem adivinhar o nome da pasta. Se o arquivo estiver em outra distribuição WSL, abra o perfil correto; processos e localhost podem não corresponder ao ambiente esperado.

#### Próximo passo

Consulte o liveness.

### 18.2 Liveness: o servidor está respondendo?

#### O que vamos fazer

No **Terminal B, raiz do projeto**, enviar um GET para a aplicação local.

#### Comando

```bash
curl --noproxy localhost,127.0.0.1 --max-time 15 -i \
  http://localhost:8080/health/live
```

#### O que esse comando significa

`curl` faz requisições HTTP. Sem outro método, usa GET. `-i` mostra status e cabeçalhos junto do corpo. `--max-time 15` limita esta consulta a 15 segundos. `--noproxy` vale somente para os destinos locais indicados, evitando enviar localhost ao proxy corporativo; não muda proxy global nem o acesso ao Gateway.

#### Resultado esperado

```text
HTTP/1.1 200 OK
...
{"status":"alive"}
```

**CONFIRMADO:** esse handler retorna `alive`; não consulta LLM nem MCP. O serviço precisa ter conseguido iniciar para atender normalmente. Um processo que abortou no startup não fica automaticamente disponível só porque existe rota de liveness.

#### Se der erro

Conexão recusada: volte ao Terminal A e confira se startup terminou e se a porta é 8080. Timeout: confira distribuição/localidade e processo. `curl: command not found`: ferramenta não disponível; solicite disponibilização pelo ambiente Pengwin, sem instalar substitutos aleatórios.

#### Próximo passo

Consulte o readiness.

### 18.3 Readiness: configuração e grafo estão preparados?

#### O que vamos fazer

No **Terminal B, raiz do projeto**, consultar a prontidão definida pelo código atual.

#### Comando

```bash
curl --noproxy localhost,127.0.0.1 --max-time 15 -i \
  http://localhost:8080/health/ready
```

#### O que esse comando significa

Usa as mesmas opções do passo anterior, mas outra rota. O handler tenta obter configuração e verifica se `graph._compiled` existe.

#### Resultado esperado

```text
HTTP/1.1 200 OK
...
{"status":"ready"}
```

Se a configuração falhar ou o grafo estiver ausente, o código pode responder 503 com `status: not ready`. Como o startup compila o grafo antes de servir, uma falha inicial também pode impedir qualquer resposta HTTP.

**Readiness não valida conectividade real com Gateway/LLM nem saúde atual do MCP.** É possível estar ready depois de o MCP falhar e o grafo ser compilado sem ferramentas.

#### Se der erro

Para 503, leia o detalhe e os logs do Terminal A localmente. Para conexão recusada, trate como falha de processo/startup antes de investigar a lógica do handler. Os health checks são filtrados no log de acesso pelo entrypoint; ausência dessas linhas no Terminal A não prova que as consultas falharam.

#### Próximo passo

Execute o Hello World real.

## 19. Hello World real: `POST /chat`

### 19.1 Enviar a mensagem ao fluxo do Agent

#### O que vamos fazer

No **Terminal B, raiz do projeto**, com o processo original ativo no Terminal A, solicitar a geração de uma resposta. Este é o último passo da sequência principal e faz uso real do serviço LLM se a configuração estiver correta.

#### Comando

```bash
curl --noproxy localhost,127.0.0.1 -i \
  -X POST http://localhost:8080/chat \
  -H 'Content-Type: application/json' \
  -d '{
    "message": "Responda somente: Hello World",
    "session_id": "hello-world-local"
  }'
```

#### O que esse comando significa

`-X POST` escolhe POST: enviamos dados para processamento. `/chat` é o endpoint, isto é, a rota da API que recebe a mensagem. `-H` adiciona um header; `Content-Type: application/json` informa o formato do corpo.

`-d` fornece o corpo JSON. JSON usa chaves, nomes entre aspas duplas e valores. Aqui `message` é o texto obrigatório; `session_id` é um identificador opcional que permite reconhecer a chamada nos logs e na resposta. Ele não é AppKey, não autentica o usuário e não cria memória de conversa: o código começa um novo estado de mensagens para cada requisição.

As aspas simples externas protegem o JSON no shell. Não acrescente vírgula depois do último campo. Não coloque dados pessoais no primeiro teste.

#### Resultado esperado

```text
HTTP/1.1 200 OK
content-type: application/json
...
{"reply":"Hello World","session_id":"hello-world-local","tool_calls_made":0}
```

`reply` é a resposta. O modelo pode variar pontuação/formatação mesmo com essa instrução; a temperatura atual não é zero. `tool_calls_made` conta mensagens de resultado de ferramentas, não chamadas ao LLM. Zero é normal quando não há tools; não significa que o LLM não foi chamado.

No Terminal A, procure a sequência correspondente, sem habilitar logs de credenciais:

```text
chat iniciado: session_id=hello-world-local
...
chat concluído: session_id=hello-world-local tool_calls=... elapsed_ms=...
... POST /chat ... 200 OK
```

**Critério de aprovação:** processo original, provider Gateway original, sem mocks/fallback introduzidos; HTTP 200; `reply` não vazia e coerente com Hello World; fluxo concluído sem erro de geração. O código desse caminho aguarda a chamada assíncrona ao LLM e não possui resposta Hello World fixa. Nessas condições, a resposta demonstra a passagem pelo fluxo real. Logs locais isolados não são comprovante independente do backend remoto; se a equipe exigir auditoria remota, a correlação no Gateway depende de acesso não fornecido.

Uma mensagem genérica de bloqueio do middleware, resposta vazia, print de teste unitário ou apenas health verde não satisfazem o objetivo. Se uma ferramenta foi utilizada, registre isso; não declare operação sem ferramentas nessa execução.

#### Se der erro

HTTP 500 tem corpo genérico `Erro interno do servidor.`: o detalhe causal fica no Terminal A. Pode ser autenticação/autorização, TLS, rede, SDK, modelo ou ferramenta. HTTP 400 pode ser guardrail; HTTP 422 pode ser JSON/campo obrigatório. Investigue pela tabela do capítulo 20, sem colocar a AppKey no curl nem desligar TLS.

Se demorar, acompanhe o Terminal A antes de reenviar. Ctrl+C no Terminal B interrompe o curl, mas não garante cancelamento do processamento remoto; não dispare várias tentativas simultâneas por impaciência.

#### Próximo passo

Registre o resultado no checklist do capítulo 22; ao terminar, pare o servidor conforme 17.2. Se houve falha, consulte o capítulo 20.

## 20. Troubleshooting por camada

As referências de passos abaixo apontam para blocos copiáveis já explicados. Não compartilhe logs completos, `.env`, arquivos de shell, histórico, ambiente completo ou chaves privadas para pedir ajuda.

| Sintoma | Provável camada | Como investigar sem contorno inseguro |
|---|---|---|
| `command not found: python3.11` | Python/Pengwin | Conferir 9.1 e 9.2; provisionamento pelo pyenv/Pengwin é pendência, não motivo para alterar Python global |
| `No module named pip` | Python/venv | Conferir caminhos em 10.3; revisar criação da venv e instalação do interpretador |
| `No module named venv` / `ensurepip` | Instalação Python | Voltar ao provisionamento do capítulo 9; não criar venv com sudo |
| Erro ao instalar pacote | pip/proxy/certificado/índice | Distinguir certificado, 407, DNS e distribuição ausente em 11.3; reconfigurar Pengwin somente quando aplicável |
| `ResolutionImpossible` | Dependências | Revisar 11.1 e `pip check` em 11.5; não editar requisitos da versão original para ocultar o problema |
| `certificate required` | mTLS | Rever par cliente e explicação 15.2; alerta não prova AppKey aceita |
| `certificate verify failed` | CA/confiança TLS | Rever CA correta e precedência em 13.1/15.1; não desabilitar verificação |
| Erro PEM / chave incompatível | Arquivos mTLS | Presença local em 13.7 não prova formato/correspondência; confirmar material com custodiante |
| AppKey ausente / `KeyError` | Configuração do provider | Repetir 13.6 e 13.7 no Terminal A; não imprimir a chave |
| 401/403 do Gateway nos logs | Credencial/autorização | Confirmar autorização para ambiente/modelo com responsáveis; não deduzir que certificado é válido apenas pelo nome do arquivo |
| MCP não resolve | Kubernetes/DNS | Rever capítulo 16; discovery pode resultar em zero tools sem impedir grafo |
| Startup parece parado no MCP | Discovery/rede/SDK | Aguardar conclusão/erro e observar Terminal A; timeout global não está fixado pelo projeto |
| `Address already in use` | Porta/processo | Usar 20.1; não matar processos desconhecidos |
| `/health/live` falha | FastAPI/Uvicorn/processo | Conferir startup completo, porta e mesmo Pengwin em 17.1/18.2 |
| `/health/ready` falha | Configuração/grafo/startup | Rever 18.3 e logs; não atribuir automaticamente a uma consulta ativa ao Gateway |
| `/chat` 500 | Runtime/LLM/ferramenta | Ler causa no Terminal A da sessão correspondente; não é resolvido pelo corpo genérico da API |
| `/chat` 400 | Guardrails | Ler código do erro; manter mensagem simples de Hello World, sem desligar controles |
| `/chat` 422 | Contrato HTTP/JSON | Repetir estrutura do capítulo 19; `message` obrigatório e string |
| `source .env` dá erro | Shell/arquivo local | Corrigir marcadores, `SERVICE_NAME`, aspas e LF em 13.5; sempre encerrar `set -a` com `set +a` |
| `no matches found` | zsh | Conferir aspas nos extras de instalação em 12.1 |
| Windows não acessa, WSL acessa | Binding/rede Windows–WSL | Confirmar `--host 0.0.0.0`, processo e configuração Pengwin; não mexer no firewall sem orientação |
| Git não reconhece repositório | Pasta/cópia sem `.git` | Voltar a 7.1; não fabricar histórico com `git init` |
| Health não aparece no log | Filtro do entrypoint | Esperado: o entrypoint filtra acesso a health/metrics; observe a resposta curl |
| Warning de judge ao usar tools | Validators | Prompts dos judges têm problema de chaves na formatação; já registrado na baseline. Não corrigir fonte neste onboarding |

### 20.1 Identificar escuta na porta, somente se houver conflito

#### O que vamos fazer

No **Terminal B, raiz do projeto**, consultar sockets TCP em escuta na porta 8080. Não encerra processos.

#### Comando

```bash
ss -ltnp 'sport = :8080'
```

#### O que esse comando significa

`-l` seleciona escuta; `-t`, TCP; `-n`, números; `-p`, identificação do processo quando disponível. O filtro limita à porta em questão.

#### Resultado esperado

```text
LISTEN ... 0.0.0.0:8080 ... users:((...pid=...))
```

Pode aparecer apenas cabeçalho se ninguém estiver escutando. Nem toda permissão permite ver detalhes do processo.

#### Se der erro

Não use sudo automaticamente. Se for seu Agent no Terminal A, pare com Ctrl+C conforme 17.2. Se for outro processo, confirme com o responsável. Não encerre todo Python, Docker ou WSL para liberar a porta.

#### Próximo passo

Resolvido o conflito, retome 17.1 e os health checks.

## 21. Glossário

| Termo | Explicação |
|---|---|
| WSL | Windows Subsystem for Linux: ambiente para executar Linux integrado ao Windows |
| WSL2 | Versão do WSL identificada pela documentação como base do Pengwin-WSL |
| Pengwin | Aplicação/configurador corporativo descrito em `ambiente/`; não confundir com nomes homônimos externos |
| Pengwin-WSL | Distribuição Ubuntu customizada onde ficam ferramentas e projetos |
| Pengwin-rede | Imagem com serviços de conexão corporativa |
| Ubuntu | Distribuição Linux usada como base desse ambiente |
| Terminal | Janela onde você interage com programas por texto |
| Shell | Programa que interpreta os comandos digitados |
| zsh | Um tipo de shell; sua utilização efetiva deve ser conferida |
| bash | Outro shell Linux; os blocos deste guia também foram escritos para sua sintaxe |
| Git | Ferramenta de controle de versões |
| GitHub | Serviço de hospedagem de repositórios e colaboração; origem concreta pendente nesta edição |
| Clone | Cópia de um repositório com histórico e metadados Git |
| Remote / origin | Conexão nomeada com outro repositório / nome convencional dessa conexão |
| Branch | Linha de trabalho no histórico |
| Commit | Registro de uma versão, identificado por um hash |
| Checkout | Versão/árvore selecionada para trabalho |
| Working tree | Arquivos de trabalho atuais do repositório |
| Python | Linguagem e interpretador usados para executar o Agent |
| pyenv | Gerenciador de versões do interpretador Python |
| pip | Instalador de pacotes Python |
| venv / `.venv` | Ambiente virtual / nome de sua pasta neste guia |
| Dependência | Biblioteca ou pacote necessário ao programa |
| FastAPI | Framework que define e atende as rotas da API |
| Uvicorn | Servidor que executa a aplicação FastAPI |
| ASGI | Interface usada entre servidor e aplicação Python assíncrona; também permite testes HTTP em memória |
| LangGraph | Biblioteca que organiza o Agent em estados, etapas e transições |
| LangChain | Bibliotecas de integração com modelos, mensagens e ferramentas |
| LLM | Modelo de linguagem que gera a resposta |
| Gateway | Serviço intermediário de acesso ao LLM |
| AppKey | Credencial de identificação/autorização da aplicação no Gateway |
| TLS | Proteção criptográfica da conexão e validação da identidade do servidor |
| mTLS | TLS com autenticação também do cliente por certificado |
| CA | Autoridade certificadora; base de confiança para validar certificados |
| Certificado | Documento digital que vincula identidade a uma chave pública |
| Chave privada | Material secreto necessário para provar a identidade correspondente |
| Bundle de CAs | Arquivo que reúne certificados de confiança |
| MCP | Model Context Protocol: protocolo de integração com ferramentas |
| Tool | Ferramenta que o Agent pode invocar para uma tarefa |
| RAG | Recuperação de informações para apoiar a resposta do modelo |
| Guardrail | Verificação aplicada à entrada ou à saída |
| Mock | Substituto simulado de um componente em teste |
| HTTP | Protocolo de requisição e resposta usado pela API |
| GET | Método HTTP normalmente usado para consultar um recurso |
| POST | Método HTTP usado aqui para enviar uma mensagem para processamento |
| Endpoint | Endereço/rota que recebe uma operação da API |
| Header | Metadado de uma requisição ou resposta HTTP |
| JSON | Formato textual estruturado usado no corpo do `/chat` |
| localhost | Referência ao ambiente local de quem faz a conexão |
| Porta | Número que identifica um ponto de atendimento de rede de um processo |
| Binding | Escolha das interfaces em que o servidor escuta |
| DNS | Resolução de nomes em endereços de rede |
| Proxy | Intermediário de rede configurado para determinadas conexões |
| VPN | Conexão que disponibiliza rotas para uma rede privada |
| Kubernetes | Plataforma que organiza aplicações em containers; seus serviços podem ter DNS interno |
| Docker | Ferramenta de execução de containers; não exigida no percurso principal |
| Variável de ambiente | Configuração herdada por um processo ao iniciar |
| `.env` | Arquivo local de atribuições; neste projeto precisa ser carregado explicitamente |
| YAML | Formato de configuração usado em `agent_config.yaml` |

## 22. Checklist final e registro do onboarding

Preencha apenas depois de executar cada etapa no seu ambiente. As caixas começam vazias porque esta edição não fez validação operacional.

- [ ] Estou no Pengwin correto e identifiquei distribuição/shell sem capturar arquivos pessoais.
- [ ] Confirmei a raiz Git e a raiz do projeto.
- [ ] Confirmei origin esperado, branch default e versão de partida.
- [ ] Registrei branch e commit iniciais; working tree foi conferida.
- [ ] Criei branch pessoal sem push.
- [ ] Escolhi Python 3.11.x como referência, sem substituir Python global.
- [ ] Validei Python e pip dentro da `.venv`.
- [ ] Instalei requirements e pacote editável em etapas separadas.
- [ ] Não copiei automaticamente o `pip.conf` nem desativei TLS.
- [ ] Instalei extras de teste na etapa própria.
- [ ] Executei e registrei os resultados dos testes locais, sem confundi-los com LLM real.
- [ ] Preparei `.env` local confiável, ignorado e não rastreado pelo Git.
- [ ] Tenho AppKey e certificado/chave/CA obtidos por processo autorizado.
- [ ] Mantive certificados e chave fora do clone e do contexto de build.
- [ ] Carreguei `.env` no Terminal A e validei presença sem imprimir valores.
- [ ] Mantive código-fonte e YAML originais.
- [ ] Startup terminou; registrei se MCP carregou ferramentas ou falhou com continuação.
- [ ] Liveness respondeu 200 com `alive`.
- [ ] Readiness respondeu 200 com `ready`, compreendendo seu limite.
- [ ] `/chat` respondeu 200 com resposta não vazia pelo fluxo real do LLM.
- [ ] Ao encerrar, parei o Agent e fechei o terminal que continha credenciais.

| Registro não secreto | Preencher após a execução do leitor |
|---|---|
| Data e hora | Pendente |
| Versão Pengwin-CLI / distribuição / shell | Pendente |
| Origem GitHub validada, sem credenciais na URL | NÃO DETERMINADO nesta edição |
| Branch inicial / default / pessoal | NÃO DETERMINADO nesta edição |
| Commit inicial / identificação do checkout | NÃO DETERMINADO nesta edição |
| Python da venv | Pendente |
| Resultado da instalação e pip check | Não executados nesta análise |
| Resultado pytest | Não executado nesta análise |
| Startup / quantidade de ferramentas | Não executado nesta análise |
| Health live / ready | Não executados nesta análise |
| HTTP de `/chat`, sessão e resposta não sensível | Não executado nesta análise |
| Pendência e equipe responsável | Preencher sem secrets |

### 22.1 O que foi CONFIRMADO

A documentação caracteriza Pengwin/WSL2/Ubuntu e descreve rede, proxy e certificados. O código local confirma a versão mínima Python, entrypoint, contrato de chat, necessidade de exportação do `.env`, provider Gateway, uso de mTLS, degradação no discovery MCP e limites dos health checks. Os testes inspecionados usam mocks/casos locais e não constituem teste externo real. As fontes exatas estão no capítulo 23.

### 22.2 O que continua NÃO DETERMINADO

URL GitHub, remote, branches, commit e checkout atual permanecem pendentes de clone com `.git`. Também não foram determinados o estado real do Pengwin do leitor, shell/versão Python instalados, configuração de rede/proxy/CA efetiva, procedimento completo para disponibilizar Python 3.11.x e processo autorizado de entrega das credenciais/certificados. Versões resolvidas dos pacotes e sucesso operacional permanecem sem execução.

### 22.3 Bloqueantes externos para um Hello World real

Python utilizável; acesso aos pacotes; AppKey autorizada; certificado cliente/chave correspondentes; confiança no servidor; DNS/rota e conectividade compatíveis com o transporte original; autorização e disponibilidade do modelo configurado. MCP indisponível não é, por si só, bloqueante depois de o discovery falhar e o grafo compilar sem ferramentas. Discovery que não conclui ainda pode atrasar/bloquear a conclusão do startup.

### 22.4 Este guia é suficiente sem conhecimento implícito?

Ele explica o percurso operacional e os pontos de verificação para quem já recebeu um ambiente e acessos válidos. **Não é possível prometer conclusão autossuficiente desde qualquer Pengwin com as evidências atuais.** Faltam o provisionamento detalhado do Python quando ausente e a entrega autorizada de AppKey/certificados/acessos. Essas lacunas são pontos explícitos de parada, não tarefas deixadas implicitamente ao iniciante. Satisfeitas as pré-condições, o leitor tem comandos e critérios para chegar ao `/chat`; a execução real ainda precisa ser realizada e registrada.

## 23. Evidências utilizadas e comparação com a baseline

### 23.1 Escopo e método

A pasta `ambiente/` continha somente `ambiente_pengwin.md` antes desta entrega; seu conteúdo completo foi lido. A caracterização corporativa deste manual usa essa fonte, sem substituir trechos ausentes por conhecimento externo. A leitura contém referências a páginas/vídeos sem conteúdo incorporado; não tratamos esses destinos como documentação disponível.

O Agent foi analisado na cópia externa `plg-agent-consult-fin-main/`, incluindo ocultos, metadados, README, configuração, todos os módulos Python e testes. Há 60 arquivos nessa árvore canônica e uma cópia interna correspondente; os pares foram comparados por hash e são idênticos. Não há `.git` nem `AGENTS.md` nas árvores inventariadas. Não foi consultado um GitHub remoto para estabelecer proveniência.

Os arquivos de deploy separados, snapshots ARGO e referências de endpoints da raiz não foram usados como prova de acesso local atual nem como fonte de credenciais. A baseline foi consultada para comparação documental, sem alterar seu conteúdo. Nenhum segredo dessas referências foi transcrito para este guia.

### 23.2 Mapa de fontes

Os links abaixo são relativos a este documento. `A` significa a raiz externa do Agent; `P`, o pacote dentro dela; `T`, seus testes.

| Fonte | O que fundamenta |
|---|---|
| [Documentação Pengwin](ambiente_pengwin.md), “O que é”, “Como usar”, CLI, pacotes, requisitos e perguntas/respostas | Ambiente, proxy, VPNKIT, certificados, Docker, acesso Windows–WSL, pyenv e riscos de diagnóstico |
| [README do Agent](../plg-agent-consult-fin-main/README.md) | Procedimento local documentado, contratos anunciados e exemplos; confrontados com código |
| [setup.py](../plg-agent-consult-fin-main/setup.py) | Python `>=3.11`, instalação editável e extras |
| [requirements.txt](../plg-agent-consult-fin-main/requirements.txt) | Lista de dependências runtime e diferenças de versões/listas |
| [pip.conf](../plg-agent-consult-fin-main/pip.conf) | Índice, CA relativa, timeout e configuração que não será copiada automaticamente |
| [Dockerfile](../plg-agent-consult-fin-main/Dockerfile) e [aic.json](../plg-agent-consult-fin-main/aic.json) | Referência Python 3.11/3.11.6, processo container e flags |
| [agent_config.yaml](../plg-agent-consult-fin-main/agent_config.yaml) | Gateway/modelo, MCP cluster, RAG/curador desligados |
| [.env.example](../plg-agent-consult-fin-main/.env.example) | Nomes das variáveis, carregamento explícito e placeholders |
| [.gitignore](../plg-agent-consult-fin-main/.gitignore) e [.dockerignore](../plg-agent-consult-fin-main/.dockerignore) | Exclusões locais e limites para proteção de certificados |
| [CI GitHub](../plg-agent-consult-fin-main/.github/workflows/ci.yaml) | Padrões de branches aceitos e workflows compartilhados referenciados |
| [Copilot setup](../plg-agent-consult-fin-main/.github/workflows/copilot-setup-steps.yaml) | Apenas checkout; não entrega instalação/teste local completo |
| [Entrypoint](../plg-agent-consult-fin-main/plg_agent_consult_fin/__main__.py) | Flags, Uvicorn e filtro de health logs |
| [Aplicação](../plg-agent-consult-fin-main/plg_agent_consult_fin/app.py) | Startup, schemas, chat, session_id e health checks |
| [Configuração](../plg-agent-consult-fin-main/plg_agent_consult_fin/config.py) | Busca de YAML, cache e leitura de token MCP |
| [Grafo](../plg-agent-consult-fin-main/plg_agent_consult_fin/graph.py) | Discovery, catch global, tools, invocação LLM, validators e cache do grafo |
| [Provider Gateway](../plg-agent-consult-fin-main/plg_agent_consult_fin/llm/gateway_outbound.py) e [factory](../plg-agent-consult-fin-main/plg_agent_consult_fin/llm/factory.py) | Transporte assíncrono, AppKey, mTLS e prioridade de CAs |
| [Middleware](../plg-agent-consult-fin-main/plg_agent_consult_fin/utils/guardrails_middleware.py), demais `P/utils/`, `P/rag/`, `P/validators/` | Controles locais/externos, variáveis e observabilidade; limitações dos judges |
| [Testes](../plg-agent-consult-fin-main/tests/) | Fixtures, mocks e separação entre comportamento local e serviço real |
| [Baseline V0](../BASELINE_V0_CONSULT_FIN.md), seções 7–17, 21–23, 28 e 35 | Comparação com as conclusões anteriores |

Também foram inspecionados `CHANGELOG.md`, `LICENSE`, `bbconfig.yaml`, `.flake8`, `sonar-project.properties`, `Jenkinsfile`, `create_release.sh` e arquivos de inicialização de pacotes. Não definem um procedimento adicional necessário ao Hello World. **CONFIRMADO:** `create_release.sh` realiza commits/push/tags e não deve ser usado neste onboarding; Jenkins declara testes de unidade/integração desligados, o que não prova a execução atual de qualquer esteira compartilhada.

### 23.3 Comparação explícita com `BASELINE_V0_CONSULT_FIN.md`

Sem histórico Git nem snapshot fonte anterior identificável por commit, **diferença de código entre revisões: NÃO DETERMINADO**. A concordância abaixo compara afirmações da baseline com os arquivos hoje disponíveis; não afirma identidade histórica byte a byte com um commit antigo.

| Tema | Reavaliação atual | Relação com a baseline |
|---|---|---|
| Ausência de `.git` | CONFIRMADO localmente | Mantida. Não há novo checkout GitHub comprovado |
| Python | `>=3.11`; AIC 3.11; imagem 3.11.6 | Mantida; agora há distinção didática entre mínimo e preferência 3.11.x |
| Dependências divergentes/sem lock | CONFIRMADO | Mantida; runtime e extras foram separados na sequência |
| `.env` sem carregamento automático | CONFIRMADO | Mantida; explica exportação e risco de executar placeholders |
| `SERVICE_NAME` com template | CONFIRMADO | Já apontado; agora há edição local explícita, sem alterar exemplo versionado |
| `pip.conf` com CA relativa e trusted-host | CONFIRMADO | Análise convertida em orientação de não copiar automaticamente, sem alterar o arquivo |
| Discovery MCP falha e permite continuar | CONFIRMADO no catch de criação | Mantida. A frase de pré-condições da seção 22.2 da baseline sobre acesso/configuração MCP é qualificada: não é requisito absoluto para Hello World sem tools |
| Discovery no startup, não por request | CONFIRMADO | Mantida; README permanece impreciso nesse ponto |
| Health ready | Configuração + grafo compilado | Mantida; não comprova chamada real Gateway/MCP |
| TLS sem CA explícita | `verify=True` | Mantida; comentário do provider continua divergente |
| Variáveis HOST/PORT etc. | Entry point usa flags | Mantida; não reproduz a promessa de ENV do README |
| Autenticação cert MCP | Não aplicada pela factory atual | Mantida; separada de mTLS Gateway |
| Integração em `tests/integration` | Somente dummy | Mantida; não chamar isso de teste externo |
| Judges e testes | JSON com chaves simples nos prompts formatados; testes substituem prompt | Mantida por inspeção; não houve nova execução/reprodução do defeito nesta edição |
| Estado de testes/runtime | Não executados nesta análise | Não se herdou nem inventou aprovação da baseline |
| Ambiente Pengwin | Nova fonte específica em `ambiente/` | Ampliação documental: inclui Pengwin-rede, proxy, CA, shell não comprovado e lacuna pyenv |

### 23.4 Limite da conclusão

Este é um manual da **versão local inspecionada**, preparado para validação no clone do leitor. Não certifica o estado atual do GitHub, do Pengwin, do Gateway, do MCP, da infraestrutura de deploy ou das credenciais. A próxima evidência Git deve atualizar somente identificação de origem/checkout/branches/commit e referências dependentes desses dados. Uma execução real deve ser registrada separadamente, sem transformar os exemplos de resultado deste documento em evidência retroativa.
