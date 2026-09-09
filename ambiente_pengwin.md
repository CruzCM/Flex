# Pengwin

O Pengwin automatiza a configuração do WSL/Ubuntu para desenvolvimento no BB.
Esta documentação é melhor visualizada na Plataforma techbb.
Veja os vídeos de utilização e explicação do Pengwin aqui.
Consulte nosso histórico de mudanças por versão.

## Instalação

O Pengwin atualmente é compatível com Windows 11 e Ubuntu 24.04 LTS.
Pode ser que funcione em versões anteriores destes sistemas operacionais, mas não garantimos o funcionamento e nosso suporte será limitado. Recomendamos que atualize seu sistema operacional quando possível.

### Windows 11

#### Pré-requisitos

Verifique se a virtualização está ativa para seu computador:

Abra o Gerenciador de Tarefas > Desempenho > CPU > campo "Virtualização"

Certifique-se que o seu sistema esteja atualizado sem nenhuma atualização pendente no Windows Update.

VDI Windows: Verifique atualizações online também conforme imagem:
Se não souber como ativar, pesquise no Google sobre ativação de virtualização na BIOS para o modelo do seu computador.

Certifique-se que o WSL esteja instalado e atualizado:

- Abra o PowerShell de Administrador e instale o WSL: wsl --install --no-distribution;
- No PowerShell de Administrador, atualize o WSL: wsl --update;
- Quando o processo concluir, reinicie a máquina.

O Pengwin só funcionará se a virtualização estiver habilitada, e o WSL operacional.

#### Instalando no Windows 11

Para o 1o passo, escolha uma das 2 opções a seguir:

##### Via Portal da Empresa:

Abra o aplicativo Portal da Empresa pelo Menu Iniciar, procure por Pengwin e o instale:

##### Via PowerShell:

Use esta alternativa caso esteja com problemas utilizando o Portal da Empresa ou não o tenha instalado. Além disso, o Portal da Empresa pode demorar a atualizar, usando o comando a seguir garante a instalação da última versão disponível:
Abra um PowerShell de usuário e instale o Pengwin utilizando o comando abaixo (copie e cole o comando inteiro - utilize a opção A se solicitado confirmação):

```powershell
$urlScript="https://binarios.intranet.bb.com.br:443/artifactory/generic-bb-binarios-dev-local/publico/pengwin/scripts/instalar-pengwin.ps1"
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser;
Invoke-RestMethod $urlScript | Invoke-Expression
```

Execute o atalho Pengwin na sua Área de Trabalho ou no Menu Iniciar:

Siga as instruções do configurador.

Em caso de problemas acesse nosso guia de ajuda e suporte.

### Instalando no Ubuntu 24

- Baixe o DEB da versão mais recente na página de releases do Pengwin;
- Localize a pasta onde o arquivo DEB foi baixado e abra um terminal nesta pasta;
- Instale o arquivo DEB: sudo apt-get install -y ./pengwin-ubuntu-x64-X.X.X.deb (troque X.X.X pelo número da versão baixada);
- Localize o atalho do Pengwin no Menu do Ubuntu e abra o instalador (ou execute pengwin no Terminal);
- Siga as instruções do instalador.

Em caso de problemas acesse nosso guia de ajuda e suporte.

## Remoção

Antes de prosseguir, faça backup ou garanta que seu trabalho está salvo no Fontes para todos os projetos que você clonou.

### Windows 11

Abra um PowerShell de usuário e execute o script abaixo em sua totalidade:

```powershell
$urlScript="https://binarios.intranet.bb.com.br:443/artifactory/generic-bb-binarios-dev-local/publico/pengwin/scripts/remover-pengwin.ps1"
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser;
Invoke-RestMethod $urlScript | Invoke-Expression
```

### Ubuntu 24

Abra um terminal e execute: sudo apt-get remove -y pengwin

## Atualização

Atente-se: Para atualizar a sua distribuição WSL (Pengwin-WSL), é preciso realizar as 2 etapas abaixo: (1) Atualizar a aplicação desktop Pengwin; e (2) Atualizar a distro Pengwin-WSL via o app Pengwin recém-atualizado. Para entender o motivo, veja: O que é o Pengwin.

### Atualizando no Windows

Use uma das opções de atualização abaixo, de acordo com a forma que você escolheu para instalar o Pengwin no Windows:

- Se instalou via comando: execute o mesmo comando PowerShell de instalação e depois siga para os próximos passos a seguir;
- Se instalou via Portal da Empresa: abra o Portal e confira se existe alguma atualização pendente para o Pengwin. Se tiver, basta atualizá-lo. Este passo atualizará o Pengwin em si, mas ainda será necessário atualizar as ferramentas instaladas por ele conforme instruído a seguir.

- Inicie o instalador pelo Atalho do Menu do seu Sistema Operacional, chamado "Pengwin";
- Siga para a seção adiante para escolher a opção de atualização;

### Atualizando no Ubuntu

- Siga o mesmo processo de instalação do Ubuntu e depois continue com os passos a seguir;
- Inicie o instalador pelo Atalho do Menu do seu Sistema Operacional, chamado "Pengwin";
- Siga para a seção adiante para escolher a opção de atualização;

### Opções de atualização

Depois de iniciar o instalador e realizar o login, será apresentado as seguintes opções quando você estiver atualizando o Pengwin, escolha conforme a ação desejada:
- Atualizar a existente: Usa sua imagem Pengwin-WSL atual, atualizando apenas para o novo Pengwin-CLI e reconfigurando as ferramentas. Esta opção é útil para recuperar uma imagem do Pengwin que foi desconfigurada por algum descuido e para atualizar a configuração da imagem e os comandos (CLI) para a versão mais recente. Vale lembrar que nem sempre a atualização da sua imagem atual é possível por alguma quebra de versão antiga;
- Remover e instalar uma nova: Remove a imagem atual, faz uma instalação limpa utilizando a imagem Pengwin-WSL mais recente, instalando e configurando os utilitários. Esta opção é equivalente a uma instalação limpa, usando a imagem mais recente com o CLI mais recente;
- Fazer backup e instalar uma nova: Faz o backup da sua imagem atual, remove e instala a imagem mais nova, e, instala um novo Pengwin-CLI. Esta opção é equivalente a "Remover e instalar", com o passo adicional de realização de backup da sua imagem "Pengwin-WSL" atual. Não restauramos o backup para evitar conflitos com versões de imagens e configurações mais novas. Mas você pode acessá-lo e copiar o que desejar para a imagem nova.

Dica: Ao abrir o aplicativo Pengwin, confira se a versão dele é a mais atual. Dessa forma, ao seguir o fluxo de configuração da distro, terá a garantia que seu ambiente estará na versão mais recente.

## O que é o Pengwin

O Pengwin é uma aplicação que automatiza a configuração do computador de trabalho de desenvolvimento para funcionários da Ditec e interessados.
O Pengwin é entregue em 3 partes:
Duas imagems WSL: Pengwin-WSL e Pengwin-rede;
A imagem Pengwin-WSL é onde reside seus arquivos de projeto e ferramentas utilizadas para desenvolvimento. Estamos falando do Node, JDK, Git, certificados TLS do BB, configuração de proxy, etc... Esta imagem é uma variação da imagem oficial Ubuntu customizada pela equipe do Pengwin para melhor funcionamento no BB. É o ambiente acessado através do atalho Pengwin Terminal.
A imagem Pengwin-rede gerencia serviços responsáveis pela conexão na rede empresarial do BB.

Um CLI (Command Line Interface) chamado Pengwin-CLI;
O CLI é responsável pelos comandos que você pode usar via Pengwin Terminal (e.g., ajuda, usarJDK8, diagnosticar, etc.). O CLI está localizado dentro da distro Pengwin-WSL WSL2 instalada pelo Pengwin.

Um instalador chamado Pengwin.
O instalador é responsável por fazer ajustes no Windows relacinados ao WSL, baixar a imagem Pengwin-WSL mais recente, instalar o Pengwin-CLI mais recente nesta imagem e realizar as instalações e configurações de ferramentas.

## Como usar o Pengwin

A seguir, os principais pontos para o usuário se atentar ao utilizar o pengwin:
- Abra o Terminal do Pengwin e realize seu trabalho através dele (e.g., git clone ... > code . > git push). Evite usar o Windows Explorer para manipulação de arquivos envolvendo o WSL;
- Terminal do Pengwin é um atalho para aplicação Terminal no profile Pengwin-WSL ;
- Ao utilizar o Pengwin não é necessário instalar nenhuma aplicação extra no Windows;
- No Terminal do Pengwin, utilize o comando ajuda para listar os comandos ofertados pelo Pengwin;
- Sempre que trocar a senha no SISBB, lembre-se de atualizar sua senha no Pengwin (Terminal do Pengwin > reconfigurar);
- O Pengwin vem configurado para funcionar na maioria dos casos. Caso seja necessário algum ajuste, converse com seus companheiros de equipe;
- Avalie se é possível integrar os ajustes no Pengwin. Você pode abrir uma issue fazendo uma sugestão ou até mesmo contribuir com código diretamente.
Teve problemas? Veja como obter ajuda em nosso guia de ajuda e suporte.

### Pengwin CLI

Para auxiliar na configuração do ambiente, o Pengwin oferece um conjunto de comandos acessíveis pelo terminal. Estes comandos podem ser utilizados para realizar algumas tarefas de forma simplificada, como atualizar credenciais do usuário no maven, npm, docker. O CLI também pode ser utilizado para instalar o Pengwin de forma personalizada.
Os comandos disponíveis e a forma de utilização podem ser conferidos no README do CLI.
Na documentação do CLI é possível consultar os pacotes ofertados pelo Pengwin e suas respectivas documentações.

### VS Code com o WSL

Para o VS Code funcionar corretamente com o WSL e com os comandos do Pengwin, são necessárias algumas configurações.
- Atualize seu VS Code para a versão mais recente. Seja via download, no site oficial, ou checando por updates no ícone de engrenagem dentro do aplicativo;
- Após atualizar, abra seu VS Code na parte de extensões e pesquise pelo pacote de extensão ms-vscode-remote.vscode-remote-extensionpack. Se não tiver instalado ainda, instale;
- Após a instalação do pacote de extensões, reinicie seu VS Code e abra a janela de configurações dele. Pesquise pela configuração Remote.WSL2: Connection Method e coloque wslExeProxy. Se esta configuração não existir, ignore.

### Pengwin Terminal

Para iniciar um Pengwin Terminal, basta usar o atalho Pengwin Terminal que foi criado na sua Área de Trabalho e no Menu Iniciar.
Você também pode procurar por WSL no Menu Iniciar ou usar o comando wsl numa janela do PowerShell.
O Pengwin instala o Windows Terminal por padrão:

### PlataformaBB

Para desenvolver para PlataformaBB com o Pengwin, o fluxo principal é:
- Abra uma instância do Pengwin Terminal;
- Clone seu repositório na pasta HOME do WSL. Ex.: cd $HOME; git clone https://fontes.bb/sigla/repositorio.git;
- Entre na pasta clonada: cd repositorio_clonado;
- Instale as dependências: npm install ou yarn install;
- Abra o VS Code para desenvolver no WSL com o comando code . dentro da pasta do projeto;
- Inicie sua aplicação com npm start;
- Rode o gaw reverse com o comando do pengwin reverse ou use o npx gaw-reverse -b 0.0.0.0 do seu repositório;
- Abra seu navegador no Windows no login em desenv da plataforma.

Para mais detalhes acerca do desenvolvimento para Plataforma 3.0, veja estes guias.

#### PlataformaBB 3.0 com AngularJS

Para desenvolver para PlataformaBB 3.0 usando o AngularJS com o Pengwin, você deve seguir os mesmos passos acima. Contudo, é possível que você enfrente dificuldades para rodar os testes em alguns casos. A seguir explicaremos como contornar este problema:
Isso acontece devido à incompatibilidade de algumas dependências do projeto em AngularJS com versões recentes do openssl (como a do Ubuntu 22.04, usado no Pengwin). Neste caso, ao rodar os testes o comando pode falhar e nenhuma mensagem de erro específica será mostrada.
Uma forma de resolver é fazer o npm ignorar as configurações atuais do OpenSSL, utilizando o comando: OPENSSL_CONF=/dev/null npm run test.
Se não quiser colocar a variável antes de cada comando de teste, pode adicionar no script "test" que fica no package.json.
Outra alternativa (menos recomendada), é carregar esta variável ao iniciar o terminal automaticamente, colocando ela no ~/.profile: echo 'export OPENSSL_CONF=/dev/null' >> ~/.profile. Esta forma é menos recomendado pois pode produzir erros em alguns serviços que utilizam o openssl.

#### GAW-Reverse

O GAW-Reverse é uma solução do BB para fazer um proxy reverso e servir nossa aplicação local no contexto da PlataformaBB.
O Pengwin oferta o comando reverse que pode ser executada em qualquer pasta/projeto, desde que este contenha o arquivo de configuração do gaw-reverse (i.e., gaw-reverse-conf.json). Este comando executa o gaw-reverse presente no projeto (ou baixa um temporário, caso não o encontre instalado no projeto) com a flag -b 0.0.0.0.
Isso fará um binding na rede local virtual entre WSL e Windows e você conseguirá acessar a plataforma em localhost normalmente pelo seu navegador do lado do Windows.
Em versões anteriores do gaw-reverse ainda não havia o parâmetro de binding. Portanto, caso você tenha problemas de acessar a PlataformaBB localmente no Windows, enquanto o gaw-reverse roda no WSL, será necessário você atualizar o gaw-reverse no seu projeto (npm i -D gaw-reverse) ou globalmente (npm i -g gaw-reverse).

### ARQ3

Para desenvolver usando Quarkus para a ARQ3 do BB com o Pengwin, siga os passos abaixo:
- Abra uma instância Pengwin Terminal;
- Clone seu repositório na pasta HOME do WSL. Ex.: cd $HOME; git clone https://fontes.bb/sigla/repositorio.git;
- Entre na pasta clonada: cd repositorio_clonado;
- Use o maven instalado pelo Pengwin para instalar suas dependências: mvn clean install;
- Abra o VS Code para desenvolver no WSL com o comando code . dentro da pasta do projeto;
- Faça as configurações de ambiente do seu projeto (arquivo .env se necessário, etc.);
- Inicie seu projeto com o maven global mvn quarkus:dev ou pelo script de run.sh, caso precise do curió: run/run.sh -c -f (a flag -f é necessária para ignorar alterações no settings.xml, já que o Pengwin já configura isso pra você);

#### Dicas

##### Abri o projeto no vscode, instalei as dependências mas meu linter não funciona

#autocomplete, #linter, #java, #maven, #vscode

- As extensões do java foram instaladas? (Na loja procure por: vscjava.vscode-java-pack);

- Com o pom.xml aberto, pressione Shift+Alt+U para atualizar o vscode com as novas alterações do projeto;

- Se não resolver, experimente criar um arquivo .classpath com o comando mvn eclipse:eclipse. Este arquivo contém os caminhos de todas as dependências do projeto (uma espécie de índice) que é utilizado pelas extensões do vscode.

### Mobile (beta)

O Pengwin agora conta com a possibilidade de rodar projetos mobile com react-native. Consideramos ainda uma fase beta, já que ainda cabem melhorias que só podem ser detectadas com o uso. Mas algumas coisas são importantes destacar:
- Você precisa instalar e configurar o Android Studio e o emulador no Windows;
- O Emulador e o WSL juntos consomem bastante memória, mas consome menos do que KDI-BOX + Emulador;
- Caso você use o BBHosts, é necessário que ele aponte para 10.0.2.2:8701, já que 10.0.2.2 é o host (Windows) e 8701 é a porta que configuramos para rodar o Metro no WSL (Existem serviços no Windows que utilizam a porta 8081);
- O EXPO não funciona com o Pengwin ainda, talvez funcione em versões futuras;
- O Emulador no Windows precisa ser iniciado pelo Android Studio ou através de um Terminal PowerShell. Se o emulador não estiver visível no WSL (adb devices), talvez seja necessário iniciar o servidor adb no Windows: adb start-server;
- No momento, os projetos Mobile necessitam do stunnel para o download correto das dependências. A partir da v1.8.1, existe o comando proxyStunnelOn para ativar o uso do stunnel.

Até a v1.7.3, o Pengwin utilizava o stunnel por padrão. Na v1.8.0 ele foi desativado (!239). E, a partir da v1.8.1, ele é opcional via proxyStunnelOn.
Com isso em mente, o guia a baixo mostra como rodar o mov-react-native-login:

#### Passo-a-passo: AAPF + login 

#### Dicas

- Rode o metro com o comando do Pengwin reactStart;
- Se precisar compilar seu APF e enviar para o emulador, use o comando do Pengwin reactAndroid;
- Demais comandos do adb no WSL devem funcionar como esperado (adb install, etc.).

#### Rodando o projeto em seu dispositivo físico Android

### Pyenv

O Pengwin oferta o pyenv como um pacote para instalação. O pyenv é um gerenciador de versões do python e conta com recursos como espaços de trabalhos virtuais (virtualenv). O pengwin tem uma documentação sucinta sobre a utilização do pyenv.

### Intellij Community no WSL

Existe um script utilitário para facilitar a instalação do Intellij. Deve funcionar no WSL e no Linux Ubuntu.
É possível configurar o Intellij nativo do Windows para funcionar com projetos dentro do WSL (i.e., Pengwin-WSL), porém envolve mais etapas e não é uma solução robusta. Assim, recomendados que utilize o script ofertado e instale o Intellij dentro do WSL.

#### Passos para instalação no Linux Ubuntu/WSL:

Na home (cd $HOME) crie o arquivo instala-idea.sh com o conteúdo presente em app/CLI/misc/instala-idea.sh. Conforme:

- Abra o arquivo especificando o nome desejado: code instala-idea.sh
- Copie o conteúdo do link acima e cole no VSCode, salve o arquivo, feche o VSCode.

- Dê privilégio de execução: chmod +x instala-idea.sh

- Agora basta executar e seguir as intruções: ./instala-idea.sh

Após a instalação, é necessário configurar o proxy da IDE para funcionar na rede do banco. Para mais informações veja o vídeo de Demonstração de uso na Wiki.

#### Configuração de Proxy para Funci a partir da v1.8.0

### OaaS-CLI

O Pengwin fornece o CLI do Portal OaaS pré-instalado, que permite executar algumas tarefas do portal via terminal, para ver as opções e comandos disponíveis, basta executar oaas-cli no Terminal do Pengwin ou verificar a documentação oficial da ferramenta.

## Benefícios do WSL no Windows

Tanto o WSL como o Vagrant são superiores ao Windows para desenvolvimento, devido a diversos fatores, especialmente por serem ambientes UNIX e à forma como acessam o sistema de arquivos, independente aos processos do Windows (evitando a bendita varredura do McAfee). Contudo, existem ainda benefícios do WSL que não são atingidos pelo Vagrant atualmente, como os elencados abaixo (sem a pretenção de ser exaustivo).

### Integração com o Visual Studio Code

Um dos maiores benefícios do WSL em relação ao Vagrant é a integração que o WSL tem com o Visual Studio Code.
No Vagrant, o usuário precisa se conectar via SSH através do VSCode com senha ou precisa configurar uma conexão com SSH via certificado.
No WSL, basta que você digite code <nome_da_pasta> dentro do Pengwin Terminal para abrir o Visual Studio Code no Windows já dentro da pasta especificada. Sem necessidade de senhas ou de configuração.

### Aplicações GNU/Linux com Interface Gráfica

Ao contrário do Vagrant, versões recentes do WSL (como a que o Pengwin requer) já vem preparadas para utilização de aplicações GNU/Linux com Interface Gráfica.
Você pode instalar e rodar aplicações com interface gráfica para GNU/Linux, como Gedit, Gimp, Inkscape, Chrome, etc. Basta instalá-los pelo gerenciador de pacote via terminal: sudo apt <nome_aplicacao>.

### Instalação de software sem administrador

No WSL você não precisa ser administrador para instalar softwares.
Você pode instalar novas aplicações que rodem no Linux, mesmo as com GUI (interface gráfica), sem a necessidade de ser administrador da máquina. Isso abre inúmeras possibilidades.

### Gerenciamento de memória escalável

Ao contrário do Vagrant, o gerenciamento da memória disponível é realizado dinamicamente pelo Windows, não sendo necessário configurar quantidades estáticas de memória para uma máquina virtual.

### Número de processos

No Vagrant, uma instância inteira do Linux é carregada, com diversos processos rodando em background, aumentando significativamente a quantidade de memória alocada à máquina virtual.
No WSL, isso não acontece, porque o Windows faz o espelhamento de diversos processos já abertos no Windows, deixando a instância do Linux muito enxuta e com pouquíssimo uso de memória RAM.

### Acesso aos arquivos do Linux

No WSL o acesso aos arquivos do Linux é transparente ao usuário, com um ícone (a partir das versões recentes do Windows 10) na seção de pastas do Explorer.
No Vagrant este acesso é um pouco mais obscuro.

### Menor consumo de memória

Devido ao número de processos e ao gerenciamento de memória escalável, o WSL utiliza muito menos memória da máquina do que o Vagrant. Deixando mais memória disponível para utilização dos softwares de desenvolvimento.

## Comandos disponíveis no CLI

Considere que nesta documentação usaremos o termo terminal para nos referir ao Pengwin Terminal, em caso de instalações no Windows+WSL, e ao terminal da distribuição Linux utilizada, em casos de instalação no Linux.
Os comandos a seguir devem ser executados no terminal.

### Geral

#### ajuda

Mostra a documentação resumida de cada comando habilitado pelo CLI do Pengwin.

#### versao

Mostra a versão do Pengwin-CLI instalada.

#### reconfigurar

Deve ser utilizado quando a senha do SISBB do usuário foi alterada ou quando alguma ferramenta instalada pelo Pengwin parar de funcionar.
Este comando também instala os certificados mais recentes.
Como o Pengwin utiliza a senha do usuário para configurar proxy e conexões com os repositórios do binários, é necessário que este comando seja executado sempre que a senha for alterada no SISBB para evitar bloqueios.
O comando irá pedir os dados do usuário novamente e configurará as ferramentas necessárias com a nova senha.

#### diagnosticar

Deve ser utilizado quando deseja-se produzir arquivos de log de diagnóstico para identificação e solução de problemas. Ao abrir uma issue, é interessante executá-lo para prover informações necessárias de antemão.
Este comando roda uma série de comandos para produzir um log detalhado de funcionamento dos principais componentes: rede, services, proxy, vpnkit, etc. Ao final de todos os comandos e da geração do log, ele é compactado juntamente com os últimos logs de instalação do Pengwin. Assim, o usuário pode anexar o arquivo gerado com informações fundamentais para identificação de problemas.
Não coloque dados sensíveis nos arquivos de inicialização.
Os dados do .bashrc, .zshrc e .profile são capturados pelo diagnosticar. Caso tenha necessidade de usar dados sensíveis, aponte para outro arquivo via sourcing, que não será capturado pelo diagnosticar:

```bash
# Exemplo de como ficam arquivos .zshrc, .bashrc e .profile
source ~/.minhas-credenciais

# Exemplo do novo arquivo .minhas-credenciais
TOKEN1=dafasdfa
TOKEN2=asblkj
SENHA=12345678
```

#### atualizar

Atualiza programas e bibliotecas instaladas via APT.

#### corrigir

Corrige instalações de programas instalados via APT.

#### instalar <nome_programa>

Substitua <nome_programa> pelo nome do programa APT que você deseja instalar.
Este comando instala o programa informado utilizando o APT, em caso de falha, é feito 3 tentativas.
Este comando não instala pacotes do Pengwin. Ele serve para simplificar a instalação de programas no Linux, via APT.

#### mostrarLogs

Abre diretório contendo os logs de execução do Pengwin pela interface gráfica (instalação de pacotes).

#### proxyStatus

Este comando lista o status do Proxy em cada serviço/ferramenta pertinente e faz uma checagem de conexão.

#### proxyOn

Este comando habilita o uso da chave e senha do usuário para bater no Proxy do BB e validar o acesso a endereços externos.
Contratados podem ter a necessidade de usar o proxy da própria empresa. Então é possível que o proxy do BB tenha que ser desativado.

#### proxyOff

Este comando desabilita o uso da chave e senha do usuário para bater no Proxy do BB e validar o acesso a endereços externos.

#### proxyStunnelOn (Disponibilidade: WSL)

Este comando habilita o uso do Stunnel para autenticação no proxy Linux (cachessl.intranet.bb.com.br).

#### proxyStunnelOff (Disponibilidade: WSL)

Este comando desabilita o uso do Stunnel para autenticação no proxy. Utilizando o proxy nativo do Windows (proxy.bb.com.br/proxy.pac).
Desde a versão 1.8.0, o Pengwin utiliza o proxy do Windows (NTLM) por padrão no WSL. Na instalação nativa Ubuntu, o proxy utilizado é do Linux (Stunnel).

#### responderNPS

Responde a pesquisa de NPS do Pengwin. 1 vez por mês, o Pengwin irá pedir para você responder o NPS.

### Plataforma

#### reverse

Este comando deve ser executado dentro da pasta de um projeto da Plataforma BB.
Este comando inicia o gaw-reverse utilizando o pacote instalado de um projeto da Plataforma BB, ou usa a última versão diretamente do repositório do BB.
Este comando é um atalho que adiciona a opção -b 0.0.0.0 automaticamente para o usuário, permitindo que o gaw-reverse seja visível do navegador do usuário no Windows. É o equivalente a executar npx gaw-reverse -b 0.0.0.0.

#### usarNode

Versões suportadas: 14, 16, 18, 20, 22
Instala e define como padrão a versão do Node escolhida (e.g., usarNode22) utilizando o nvm.
Equivalente a: nvm install v<versao> && nvm alias default v<versao>.

### ARQ3

#### listarJDK

Este comando lista as JDKs disponíveis para desenvolvimento instaladas. É o equivalente a usar o comando update-java-alternatives --list.

#### usarJDK

Versões suportadas: 8, 11, 17, 21
Este comando troca a versão do JDK conforme a opção escolhida (e.g., usarJDK21) e o instala caso necessário.
Equivalente a: sudo update-java-alternatives --set java-1.<versao>.0-openjdk-amd64.
Caso não esteja disponível, instale com o Pengwin ou de forma manual.

#### listarMvn

Este comando lista as versões do Maven disponíveis. É o equivalente a usar o comando update-alternatives --list mvn.

#### usarMvn305

Este comando troca o Maven padrão para a versão 3.0.5 e o instala caso não esteja disponível. É o equivalente a usar o comando sudo update-alternatives --set mvn /opt/apache-maven-3.0.5/bin/mvn.

#### usarMvn363

Este comando troca o Maven padrão para a versão 3.6.3 e o instala caso não esteja disponível. É o equivalente a usar o comando sudo update-alternatives --set mvn /usr/share/maven/bin/mvn.

#### usarMvn395

Este comando troca o Maven padrão para a versão 3.9.5 e o instala caso não esteja disponível. É o equivalente a usar o comando sudo update-alternatives --set mvn /opt/apache-maven-3.9.5/bin/mvn.

#### usarMvn399

Este comando troca o Maven padrão para a versão 3.9.9 e o instala caso não esteja disponível. É o equivalente a usar o comando sudo update-alternatives --set mvn /opt/apache-maven-3.9.9/bin/mvn.

### Mobile

#### reactStart

Este comando deve ser executado dentro da pasta de um projeto da Mobile do BB.
Este comando inicia o Metro utilizando o pacote do react-native-cli instalado de um projeto Mobile.
Este comando é um atalho que adiciona as opções --host 0.0.0.0 --port 8701 automaticamente para o usuário, permitindo que o Metro seja visível do emulador do usuário no Windows. É o equivalente a executar npx react-native start --port 8701 --host 0.0.0.0.

#### reactAndroid

Este comando deve ser executado dentro da pasta de um projeto da Mobile do BB.
Este comando procura o primeiro emulador do usuário no Windows e tenta enviar o bundle do projeto para este emulador. Só deve ser usado caso o primeiro emulador da lista (veja a lista com adb devices) seja o emulador aberto no Windows.
Este comando é um atalho que lista os emuladores disponíveis, pega o primeiro e roda o comando de bundle do Android do react-native-cli. É equivalente a realizar os seguintes comandos:
adb devices
react-native run-android --port 8701 --deviceId 
Em caso de projetos com Expo, o comando tenta extrair o projeto Android com npx expo eject ou npx expo prebuild para depois rodar o React-Native-CLI. O Expo ainda não é suportado pelo Pengwin via WSL.

#### usarAndroidStudio (Disponibilidade: Linux nativo)

Este comando instala o .tar.gz oficial do Android Studio 2025.1.3.7 e configura a aceleração de hardware. Se já o estiver instalado, o usuário terá a opção de remover a anterior ou cancelar a nova instalação.

### WebLogic Plataforma

#### usarWebLogicPlataforma

Este comando reconfigura o WebLogic Portable (GAW). Caso não esteja instalado, o instala.

### Pacotes

Conjunto de utilitários/programas agrupados por esteiras de desenvolvimento oferecidas pelo BB. Cada pacote instala e configura esses programas para funcionar adequadamente na infraestrutura do BB.
O Pengwin oferta os seguintes pacotes:
Pacotes opcionais escolhidos pelo usuário:

- arq3

- plataforma

- mobile (Beta)

- pyenv

- wl-plat

Outros:

- core: Sempre instalado.

- shared: Contém funções compartilhadas para desenvolvimento.

## Instalação Personalizada

Caso você não queira instalar de forma padronizada utilizando o guia do Pengwin, você pode fazer o download da sua distribuição favorita (do Ubuntu e compatíveis) e usar nosso CLI. Lembre-se que o Pengwin foi desenvolvido para ser compatível com o Ubuntu, demais distribuições linux não são suportadas, cabendo a você qualquer ajuste. Nossa equipe não pode dar suporte a situações não padronizadas.

### Windows + WSL personalizado

Para usar no Windows, com WSL e sua distribuição Linux personalizada, siga os passos adicionais abaixo:
- Atualize seu WSL (ou instale, se for o caso), conforme consta em nosso guia.
- Abra o terminal do WSL na distribuição desejada (e.g., na janela do powershell execute wsl -d "Ubuntu");

### Instalação com o CLI no Linux/WSL

#### Pré-requisitos

Distro Ubuntu (24.04 ou posterior) ou Debian com GIT (sudo apt install git);

#### Importar distro para configuração de rede (Pengwin-rede):

- Baixar arquivo pengwin-rede-1.0.0.tar.zst. Basta clicar no link e confirmar o download na pasta Downloads.

- Abrir Terminal PowerShell onde o arquivo foi baixado e rodar os comandos:
<LOCAL_INSTALACAO> (sugestão $env:USERPROFILE\wsl-distros): destino onde a distro será instalada.
<IMAGEM>: imagem a ser importada pelo WSL.

```powershell
    # Execute 1 comando por vez!
    wsl --shutdown
    # Aguade pelo menos 10 segundos antes de continuar.
    New-Item -ItemType Directory -Path "$env:USERPROFILE\.pengwin\bin\" -ErrorAction SilentlyContinue
    New-Item -ItemType Directory -Path  -ErrorAction SilentlyContinue
    wsl --import Pengwin-rede --version 2  
    Copy-Item -Force "\\wsl.localhost\Pengwin-rede\app\*.exe" "$env:USERPROFILE\.pengwin\bin\"
```

Exemplo de comando: wsl --import Pengwin-rede --version 2 $env:USERPROFILE\wsl-distros\Pengwin-rede $env:USERPROFILE\Downloads\pengwin-rede-1.0.0.tar.zst

#### Passo-a-passo

Execute os seguintes comandos:

Pega suas credencias e faz clone do repositório Pengwin no local apropriado:

```bash
    pushd $(mktemp -d) >/dev/null
    git -c http.sslVerify=false clone https://fontes.intranet.bb.com.br/dev/publico/pengwin.git
    cd pengwin
    sudo mkdir -p /usr/lib/pengwin/resources/CLI
    sudo touch /usr/lib/pengwin/resources/CLI/.version
    git tag --merged | tail -1 | tr -d 'v' | sudo tee /usr/lib/pengwin/resources/CLI/.version
    sudo cp -r app/CLI /usr/lib/pengwin/resources
    popd >/dev/null
```

É importante que a pasta de destino seja conforme descrito.

Inicia execução dos scripts:

```bash
/usr/lib/pengwin/resources/CLI/pengwin.sh -chave "FXXXXXXX" -senha "12345678" -nome "Nome Completo Humanograma" -email "email@bb.com.br" -estadoProxy "true/false" -idioma "pt_BR" -pacotes "pacote1,pacote2,..." -comando "instalar"
```

- -chave: Sua chave do SISBB (ex.: F1234567).

- -senha (Opcional): Sua senha do SISBB. Caso esteja executando pelo terminal é melhor não especificar esse parâmetro, assim o Pengwin irá perguntar e sua senha não fica no histórico do terminal.

- -nome: Seu nome completo conforme apresentado no Humanograma (ex.: João Kleber dos Santos).

- -email: Seu email do BB (ex.: joao.kleber@bb.com.br).

- -estadoProxy: true|false Determina se o proxy do BB será ativado (true) ou desativado (false). Funcionários devem ativar o proxy. Contratados depende do caso.

- -idioma (Opcional): Especifica qual idioma desejado para o ambiente. O padrão é pt_BR.

- -pacotes: pacote1,pacote2,...: Lista de pacotes adicionais separados por vírgula e sem espaços, opções:
- plataforma: instala nvm, node e gaw-reverse;
- arq3: instala java, maven, docker, kubernetes e openshift;
- mobile: instala Android commandlinetools, node, jdk11;
- wl-plat: Weblogic Plataforma;
- pyenv: Gerenciador de versões Python;

- -comando: instalar|reconfigurar Determina qual operação deve ser executada.

```bash
Exemplo do comando: /usr/lib/pengwin/resources/CLI/pengwin.sh -chave "F1234567" -nome "João Kleber dos Santos" -email "joao.kleber@bb.com.br" -estadoProxy "true" -idioma "pt_BR" -pacotes "arq3,plataforma" -comando "instalar"
```

Ao concluir a execução:

- WSL: feche e abra o terminal do WSL.

- Linux: renicie o computador.

Seu ambiente deve estar configurado.

## Ajuda e Suporte para o Pengwin

Neste documento você tem perguntas e respostas e uma seção de ajuda com as principais dúvidas e problemas enfrentados, bem como a forma de solicitar atendimento em casos específicos.

### Tive algum problema, como posso obter ajuda?

Para resolver o seu problema, siga estes passos:
- Verifique no índice desta página se a sua dúvida ou problema possui uma solução já fornecida;
- Pesquise nas issues abertas por problemas semelhantes que já foram respondidos ou que já tem solução relatada;
- Pesquise na internet por uma solução, especialmente quando você fez alguma modificação manualmente no seu WSL;
- Caso não encontre uma solução, você pode iniciar um atendimento abrindo uma issue (#iniciando-um-atendimento).

### Iniciando um atendimento

Utilize o nosso template como referência.

- Descreva detalhadamente o cenário do problema (onde?) e como ele ocorre (quando?, quais motivos? passos para reproduzir?);

- Utilize o comando diagnosticar (a partir de Pengwin v1.7.0) dentro do WSL para gerar um relatório de possíveis problemas e o anexe;
- Anexe o log da sua instalação do Pengwin (o comando mostrarLogs abre o diretório dos logs);
- Complemente com printscreens e o que mais achar relevante.

Para um atendimento rápido e eficiente, a apresentação de boas informações e do problema é um pré-requisito. Issues de atendimento consideradas incompletas serão marcadas como tal (~"necessita-informações") e estão sujeitas a serem fechadas sem aviso prévio.

### Requisitos de funcionamento

Pela natureza do Pengwin, é necessário que o usuário tenha os módulos do WSL instalados no Windows ou uma máquina Linux com Ubuntu compatível.

Além disso, para acessar os servidores internos do BB, o Pengwin precisa dos certificados do BB atualizados e configurados. Geralmente, o próprio BB os gerencia. Os certificados imprescindíveis são:

- AC Raiz v3

- AC Servidores v3

- AC Usuários v3

Pode ser que outros certificados sejam necessários, podendo ser identificados em https://pki.bb.com.br.
A issue #99 tem o passo-a-passo da instalação dos certificados no Windows.
A rota de rede via VPN também precisa estar funcionando, já que para acesso aos servidores de arquivos e login, precisamos acessá-los. Segue uma lista dos principais domínios que o Pengwin utiliza:

- binarios.intranet.bb.com.br

- sso.intranet.bb.com.br

- sso1.intranet.bb.com.br

- sso2.intranet.bb.com.br

- login.intranet.bb.com.br

## Perguntas e Respostas

### E se eu trocar a senha no SISBB?

Se você trocar a senha no SISBB, precisa atualizar a senha no Pengwin. Na versão mais recente, o Pengwin instala um utilitário para atualização de senhas e reconfiguração. Basta executar o comando reconfigurar (veja o comando exato para sua versão usando o comando ajuda) no Pengwin Terminal para atualizar suas senhas em todas as configurações necessárias dentro do Pengwin.

### Como instalo aplicativos gráficos no WSL?

O WSL permite a execução de várias aplicações com interface gráfica. Para utilizá-los, instale normalmente pelo apt, exemplo: sudo apt install gedit.
O Windows cria atalhos para estes aplicativos automaticamente em Menu Iniciar > Pengwin-WSL (ou o nome da distribuição Linux) > Nome do programa. Pode ser que o aplicativo não tenha atalho desktop, neste caso ele pode ser chamado pelo Pengwin Terminal.

### Como funciona o Proxy no BB?

Para conexão com as áreas corporativas do BB, é necessário que haja um proxy configurado com os certificados de segurança corporativa. Esta configuração de proxy deve ocorrer automaticamente através do Pengwin. Contudo, é possível que ocorram falhas pontuais em aplicações instaladas manualmente pelo usuário e que devem ser analisadas individualmente. Em caso de dúvidas ou problemas, olhe a seção de Obtendo ajuda.

### E se meu WSL quebrar?

Caso isso aconteça, dificilmente será por causa do Pengwin. Basta executar o Pengwin no menu novamente e refazer a configuração.

### Falha na instalação dos módulos do WSL. Como corrigir?

Se ao usar o comando wsl --install --no-distribution como adminsitrador no PowerShell ele causar erro por comando inexistente, mesmo após todas as atualizações do Windows, você deverá incluir o pacote do WSL manualmente.
Ou se caso, o CLI do wsl acusar recurso não existente ao abrir o Pengwin Terminal ou Terminal > Pengwin-WSL (Error code: Wsl/Service/CreateVm/HCS_E_SERVICE_NOT_AVAILABLE).
Siga os seguintes passos:
- Verifique que você tem o Windows 11, versão 22H2 ou posterior. Para conferir, use a tecla Windows + R e execute o comando winver;

- Ative os recursos do Windows necessários para o WSL funcionar:

- Abra um Powershell como Administrador;

- Execute os comandos:

```powershell
dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart
dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart
```

- Reinicie o computador pra concluir as configurações;

- Abra um terminal PowerShell normal (não administrador) e verifique a versão do Kernel com o comando wsl --version;

- Caso a versão do Kernel seja inferior a 5.15, tente fazer a atualização do WSL: wsl --update;

- Caso a atualização falhe, instale o novo kernel wsl manualmente;

- Reinicie o computador após a instalação/atualização;

- Abra um Powershell normal (não administrador);

- Atualize o WSL: wsl --update;

- Aguarde a conclusão e reinicie o computador;

- Siga os passos em Instalação no Windows 11 novamente para ver se o problema foi resolvido.

Em caso de algum erro diferente, abra uma issue e explique o que aconteceu, incluindo print das telas juntamente com arquivos de logs sempre que possível para que possamos auxiliá-lo.
https://learn.microsoft.com/en-us/windows/wsl/troubleshooting#installation-issues

### Coletando logs de diagnóstico do WSL para depuração

Em certos casos, é necessário depurar a inicialização do WSL, para isso:
Feche todas as aplicações abertas no WSL e encerre o processo. Em uma janela do Powershell:

```powershell
wsl --shutdown
```

Abra um nova janela Powershell como admin e execute:

```powershell
Invoke-WebRequest -UseBasicParsing "https://raw.githubusercontent.com/microsoft/WSL/master/diagnostics/collect-wsl-logs.ps1" -OutFile collect-wsl-logs.ps1
Set-ExecutionPolicy Bypass -Scope Process -Force
.\collect-wsl-logs.ps1
```

O script ficará coletando informações até ser interrompido.
- Repita o cenário com erro (abrir o WSL, Pengwin Terminal, VSCode, etc.). A ideia é coletar informações do WSL durante a reprodução do problema;
- Após reproduzir o erro, volte no Powershell rodando o script de coleta e presione ENTER para finalizar a coleta. Se o processo deu certo, ele vai apresentar o caminho do arquivo gerado. Anexe o arquivo gerado na issue para atendimento.

https://github.com/Microsoft/WSL/blob/master/CONTRIBUTING.md#collect-wsl-logs-recommended-method

### Acentuação não funciona corretamente no WSL mas funciona no Windows

Confira se o layout do teclado no Windows está configurado corretamente para o teclado que esteja utilizando. Pode acontecer de você estar utilizando um teclado ABNT2 (tem Alt Gr, do lado direito da barra de espaço) e o Windows estar configurado com ABNT, e vice-versa.
No Windows 11 essa opção está em Configurações > Hora e idioma > Idioma e região > Opções de Idioma (clique nos 3 pontinhos do idioma) > Teclados.
Clique aqui para ver o passo-a-passo:

### Aplicação gráfica no WSL não renderiza corretamente, Google Chrome WSL com janela branca

Adicione a linha export LIBGL_ALWAYS_INDIRECT=1 ao final dos seus arquivos de configurações de Shell, ~/.bashrc e ~/.zshrc. Isso força a renderização via software das aplicações gráficas. Note que dessa forma a aplicação não terá aceleração por hardware, podendo ter impacto no seu desempenho.
Esse problema parece afetar mais usuários do Windows 10. Existem diversas issues abertas sobre isso no GitHub do WSL e até o momento não parece ter uma solução definitiva. Temos uma issue para acompanhamento (#325).

### Problemas ao rodar aplicação em container

Caso você esteja enfrentando problemas de rede ao rodar aplicações em container com docker-compose, docker ou podman, é bem provável que a falha esteja relacionada a DNS dentro do container ou a proxy.

#### DNS

O Pengwin configura o DNS do docker no arquivo de configuração do daemon do docker que roda no WSL. Este arquivo fica em /etc/docker/daemon.json. Dentro deste JSON, existe a propriedade DNS, que incluímos o IP do Windows/VPNKIT e os DNS da VPN do BB.
Caso alguma aplicação containerizada não encontre outra aplicação conteinerizada, por exemplo seu microsserviço acessando um mongodb na sua máquina, atente-se para que todos estejam rodando em container e dentro da mesma rede do docker (este é o padrão). Se você estiver executando seu microsserviço via mvn quarkus:dev e os containers via docker, o microsserviço não irá enxergar o mongodb se o HOST para este serviço estiver em forma de hostname. Pois este hostname só existe dentro da rede do docker, não fora (na sua máquina local).

#### Proxy

É possível que sua API consuma servidores externos, como uma API do Bacen, ou de algum outro serviço externo ao BB. Caso isso seja o caso e você esteja rodando sua aplicação em container, veja a explicação do funcionamento do proxy no WSL e nos containers aqui.
Em suma, você precisa repassar a configuração de proxy feita pelo Pengwin localmente (no WSL) para dentro do seu container. Ou configurar um proxy manualmente dentro do próprio container. Nós não conseguimos fazer isso por você, já que cada projeto é uma realidade diferente.

### Aplicação X não é acessível no navegador do Windows

Os erros mais comuns apresentados pelo navegador são: conexão recusada ou impossível estabelecer conexão. Isso acontece quando a aplicação foi executada dentro do WSL, mas não foi executada no host correto.
Para uma aplicação ser visível no Windows, quando iniciada dentro do WSL, é preciso que você faça o binding do host corretamente. Se, por padrão, a aplicação roda em localhost ou 127.0.0.1, ela não será visível do Windows, somente pelo próprio WSL. Nestes casos, você pode acessar estes serviços com aplicações dentro do WSL, como o Google Chrome instalado no WSL (existe um link para ele no Menu Iniciar > Pengwin-WSL> Google Chrome).
Para ser visível em um navegador ou em outras aplicações do lado do Windows a forma mais correta é iniciar as aplicações com o binding dessa aplicação em 0.0.0.0 ou no IP do WSL que deve ser 192.168.127.2. Isso habilita a descoberta dessa aplicação pela rede virtual entre Windows e WSL.
Exemplos:
- Uma aplicação express deve fazer o listen com o host correto: app.listen(porta, '0.0.0.0', callback);
- Uma aplicação num container docker deve ser iniciado com as flags --ws-external e --rpc-external (veja aqui);
- Uma aplicação react native deve setar a flag host: --host 0.0.0.0;
- Uma aplicação weblogic ou java precisa fazer o listen em 0.0.0.0.

### Extensão do Java (ou outra) não instala no VS Code com WSL

Existem relatos de lentidão na instalação do pacote de extensões do Java no VS Code conectado ao WSL. Isso acontece pela forma como a conexão com as extensões é gerenciadas pelo proxy do BB. Em alguns casos é necessário fazer uma configuração no VS Code.
Verifique a issue #9 para tentar resolver este problema. Caso não seja possível, você pode abrir uma nova issue documentando seu caso específico.

### Script run/run.sh do meu projeto não roda

Às vezes, o script run.sh está desatualizado usando o antigo atf e precisa ser atualizado para o binários. Lembre-se, também, de setar suas variáveis de ambiente do projeto, quando necessário.
Em raras vezes, o settings gerado pelo run.sh ou o maven utilizado podem ter conflitos com as versões instaladas no WSL. Nestes casos, Você pode forçar o script a rodar com o settings global. Para fazer isso, rode o script com a flag -f: run/run.sh -f (adicione a flag -c se quiser subir o Curió localmente: run/run.sh -c -f).
Em outros casos, seu projeto pode ter sido construído no Windows e o Linux/WSL não reconhece alguns caracteres do run.sh que são colocados pelo Windows (i.e., CRLF, https://askubuntu.com/q/803162). Neste caso, você pode "convertê-lo" para o Linux/WSL com este comando: sed -i -e 's/\r$//' run/run.sh. Lembre-se que é necessário que você esteja na pasta do projeto.

### Quarkus não reconhece algum arquivo como o .env

Isso pode acontecer quando há caracteres típicos do Windows no arquivo que não está sendo reconhecido. Assim como ocorre com o arquivo run.sh, pode ser que você precise converter este arquivo (seja o .env, ou qualquer outro) para funcionar no Linux/WSL. Faça a conversão com este comando: sed -i -e 's/\r$//' .env (troque .env pelo nome do arquivo). Lembre-se que é necessário que você esteja na pasta do projeto onde se encontra o arquivo a ser convertido.

### Projeto AngularJS não roda - Falha com PhantomJS (testes)

É possível que este problema seja causado pela versão mais recente do openssl. Para resolver, geralmente basta exportar uma variável no WSL com o comando: export OPENSSL_CONF=/dev/null.
Se quiser que este comando seja executado toda vez que você iniciar o WSL, adicione este comando ao final do arquivo $HOME/.profile assim: echo "export OPENSSL_CONF=/dev/null" >> $HOME/.profile.
Por padrão, não colocamos esta configuração no Pengwin para não causar incompatibilidade com projetos que usem o openssl em versões recentes.

### Quando estou na VPN não consigo acessar a internet no WSL

O vpnkit usado pelo Pengwin costuma resolver os problemas de conectividade quando na VPN do BB. Ainda assim, é possível de acontecer dificuldades pontuais. Isso acontece de forma intermitente, por causa da forma como a VPN do BB cria uma nova interface de rede virtual e pela forma como o Windows atribui a subrede do WSL. Não há como controlar a criação da subrede do WSL pelo Windows.
Optamos por resolver este problema com o vpnkit, contudo, caso ainda aconteça algum problema durante o uso da VPN, tente os seguintes passos:
- Reinicie o computador;
- Conecte à VPN;
- Abra o WSL normalmente e aguarde 30 segundos antes de tentar uma conexão.

Caso não resolva, abra uma issue com seu caso para analisarmos.

### Docker não inicializa

Verifique se o serviço do docker está rodando com o comando systemctl status docker (ou service docker status). Caso não esteja rodando, tente reiniciar o serviço com sudo systemctl restar docker (ou sudo service docker restart).
Caso o problema persista, pode ser necessário restaurar o iptables para o modo antigo com o comando: update-alternatives --set iptables /usr/sbin/iptables-legacy. Depois disso, tente reiniciar o docker com os comandos acima.
Se nada disso funcionar, abra uma issue documentando seu caso com o máximo de informação possível.

### Meu gaw-reverse não funciona

Caso o comando reverse não funcione corretamente, os problemas possíveis são os seguintes:
- Há uma diferença entre a versão do gaw-reverse mais recente e a usada no seu projeto que pode ter quebrado a forma de utilização. Neste caso, você precisa atualizar o gaw-reverse no seu projeto reinstalando o pacote com npm i -D gaw-reverse;
- O gaw-reverse não localizou o arquivo gaw-reverse-conf.json no seu projeto (ou na pasta onde o comando foi executado). Para criar o arquivo de configuração para seu projeto, siga o passo a passo neste link;
- O arquivo HOSTS do Windows não foi configurado. Este é um requisito para desenvolvimento da plataforma e a forma de configurar pode ser encontrada neste link.

Para qualquer outro problema não listado aqui, abra uma issue com a reprodução do problema para verificação.

### PowerShell com problema na instalação de pacotes

Alguns usuários instalaram versões do PowerShell manualmente, substituindo a versão padrão que veio no Windows. Neste caso, algumas incompatibilidades podem ocorrer.
O Pengwin usa a instância do PowerShell padrão que vem com o Windows, portanto a execução de scripts é habilitada diretamente nele. Em outras instâncias, alguns problemas podem ocorrer, especialmente na instalação do Windows Terminal.
Se este for seu caso e você recebeu algum erro semelhante a este:

```text
Add-AppxPackage: The 'Add-AppxPackage' command was found in the module 'Appx', but the module could not be loaded. For more information, run 'Import-Module Appx'.
```

Será necessário rodar o comando para importar o módulo necessário: Import-Module -Name Appx -UseWindowsPowerShell.
Outros casos devem ser analisados separadamente, através de issues.
