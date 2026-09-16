# Educador Financeiro (mf-edu-fin) — AgentOps após a aprovação

Este guia começa no ponto informado por você: **a solicitação já foi aprovada**. O caminho principal é confirmar a entrega dos recursos, acessar os repositórios e acompanhar a primeira versão funcionando em HML. Se DES também tiver sido provisionado ou for exigido pelo fluxo da equipe, o guia indica onde validar esse ambiente antes.

Base: documentos e arquivos disponíveis neste workspace, consultados em 15/09/2026. Os caminhos abaixo foram encontrados nesse material; não foram conferidos em uma sessão autenticada dos portais. Um registro antigo de sucesso ou de erro não comprova a situação atual do ambiente.

O projeto deste guia é o **Agente de IA Educador Financeiro (`mf-edu-fin`)**, começando do zero. Você confirmou que a oferta segue o mesmo processo do Consultor Financeiro. Por isso, usamos os arquivos e registros do Consultor como referência do processo e do template, enquanto os recursos do Educador serão identificados na nova entrega.

**Confirmado por você:** nome `mf-edu-fin`, sigla `IAA`, tipo Agente de IA, aprovação obtida e projeto novo. **Ainda não verificado:** conclusão do provisionamento, associação da sigla na entrega, nome completo dos repositórios, pacote Python, endereços e credenciais do Educador. O nome informado não permite deduzir todos esses valores.

**Como ler esta versão:** conforme combinado, os links do **Consultor Financeiro** aparecem como exemplos concretos para estudar o caminho completo. Os links corretos do **Educador Financeiro** serão informados posteriormente. Sempre que aparecer **“EXEMPLO — CONSULTOR”**, aquele endereço pertence ao Consultor; na execução do Educador, substitua-o pelo endereço correspondente da sua entrega. A falta desses links agora não impede a leitura e preparação do guia.

### Nossa primeira tarefa prática

1. Abrir a solicitação aprovada do **Educador Financeiro / mf-edu-fin** no TechBB.
2. Conferir o resultado do provisionamento.
3. Localizar o link do repositório de código entregue.
4. Localizar os links de deploy entregues.
5. Se o código estiver no GitLab, seguir a etapa 4 deste guia; se estiver no GitHub, seguir a etapa 5.

Os comandos deste guia pedem os endereços reais entregues ao Educador. As pastas locais `mf-edu-fin-codigo` e `mf-edu-fin-deploy` são nomes escolhidos apenas para organizar as cópias no seu computador; não são nomes presumidos de repositórios corporativos.

## 1. Entenda os nomes antes de começar

| Nome | Significado neste guia |
|---|---|
| Aprovação | Autorização para a plataforma atender à solicitação. |
| Provisionamento | Criação dos recursos: repositórios, configurações e espaço para a aplicação no ambiente corporativo. |
| Instância | O registro do serviço que você solicitou no portal. |
| Repositório | Pasta de projeto com histórico de alterações, hospedada no GitLab ou GitHub. |
| Repositório de código | Contém o programa do agente e seus testes. |
| Repositório de deploy | Contém as instruções para colocar uma versão do programa em um ambiente. |
| Template | Projeto inicial entregue pela plataforma, com arquivos prontos para adaptação. |
| Branch | Linha de trabalho dentro de um repositório. Permite preparar mudanças separadamente. |
| Commit | Registro de uma alteração no histórico. |
| Push | Envio dos commits locais ao GitHub. Pode iniciar automações. |
| Pull Request / PR | Pedido para revisar e incorporar mudanças de uma branch em outra. |
| Merge | Incorporação das mudanças aprovadas. |
| Build / CI | Processo que prepara, testa e empacota o código. |
| Imagem | Pacote executável do programa e suas dependências. |
| Tag da imagem | Identificador da versão do pacote publicado. |
| Deploy / CD | Colocação de uma imagem em execução no ambiente escolhido. |
| ArgoCD | Ferramenta que aplica e acompanha as configurações de deploy. |
| OpenShift | Plataforma em que a aplicação executa. |
| Namespace | Espaço que agrupa os recursos da aplicação no cluster. |
| Pod | Unidade em que o contêiner da aplicação executa. |
| Secret OpenShift | Recurso que fornece à aplicação credenciais ou arquivos protegidos. Neste guia, `env` e `idh-mtls` são exemplos de nomes de Secrets. |
| `.env` | Arquivo de configurações para carregar no processo executado no computador; não é enviado ao GitHub. |
| AppKey | Credencial que identifica/autoriza a aplicação ao chamar o Gateway. |
| Chart / `values.yaml` | Modelo dos recursos de deploy e arquivo com os valores usados para configurá-los. |
| Operador de certificado | Automação no cluster que processa solicitações e acompanha os certificados declarados pelo chart. |
| Service | Endereço interno que encaminha chamadas aos pods. |
| Endpoint | Endereço usado para chamar uma função do serviço. |
| DES, HML, PRD | Desenvolvimento, homologação e produção, respectivamente. |

## 1.1 Papéis de acesso — o que pedir e para quê

Esta costuma ser a parte mais confusa porque **ter uma sigla de projeto não significa que seu usuário já tem os acessos**, e porque aprovação da solicitação e acesso técnico são coisas diferentes.

### As três peças

| Peça | Para que serve | Exemplo neste projeto |
|---|---|---|
| Sigla | Identifica a unidade/projeto usada na seleção de acessos | `IAA`, conforme informado por você |
| Papel de acesso | Permite ao seu usuário fazer determinadas ações em um sistema | A referência cita `ALMFD<<SIGLA>>` e `ALMFE<<SIGLA>>` |
| Aprovação da oferta | Autoriza a solicitação de criação do serviço | Já obtida para `mf-edu-fin`, conforme informado por você |

Um **grupo ITSM** é um vínculo organizacional que o guia de provisionamento lista como pré-requisito. O material não diz que ele é um papel ALMFD/ALMFE nem informa o código do grupo de IAA. Se o formulário ou a área de acesso pedir esse vínculo, confirme qual grupo ITSM da equipe deve ser usado.

### Papéis citados para o agente de referência

A wiki do Consultor registra estes nomes:

| Código que aparece na referência | Aplicando a sigla IAA | O que a fonte diz |
|---|---|---|
| `ALMFD<<SIGLA>>` | `ALMFDIAA` | Cluster e ArgoCD; perfil de desenvolvimento. O guia genérico também diz que o acesso ALMFD à sigla é requisito do provisionamento e libera a sigla para seleção. |
| `ALMFE<<SIGLA>>` | `ALMFEIAA` | Cluster e ArgoCD; perfil chamado `RT` na wiki. O guia genérico cita ALMFE para criação automática de grupos; outro roteiro usa acesso ALMFE para visualizar siglas num formulário de operações administrativas. |
| `DEVMSAPV` | `DEVMSAPV` (não recebe sufixo de sigla nos documentos) | A documentação genérica da oferta de microsserviço afirma que, desde 02/04/2026, a aprovação deve ser feita por usuário com esse papel. Isso descreve o aprovador; não significa automaticamente que todo desenvolvedor do projeto precise recebê-lo. |
| `DEVARQAP` | `DEVARQAP` (não recebe sufixo de sigla nos documentos) | A documentação genérica diz que siglas diferentes de T99 exigem aprovação de arquiteto com esse papel. É um papel do aprovador da etapa arquitetural, quando essa etapa se aplica. |

`<<SIGLA>>` é um espaço reservado usado na documentação. Para o projeto cujo código de sigla você informou como `IAA`, a substituição textual produz `ALMFDIAA` e `ALMFEIAA`. Confirme no painel de acesso se os itens aparecem exatamente assim antes de enviar a solicitação: os guias consultados não mostram um pedido de acesso feito para a sigla IAA.

**“RT” não é definido na wiki.** Não vou expandir essa sigla nem afirmar que `ALMFEIAA` equivale automaticamente a HML ou PRD. O roteiro do agente o relaciona a Cluster/ArgoCD e perfil RT; essa definição precisa vir do catálogo do painel ou do gestor responsável.

### O que a equipe do Consultor também registrou, mas ainda não esclareceu

Na lista do Consultor aparecem `CTL02000`, `CTL00030` e um papel anotado apenas como `RFG...`. A própria wiki marca a finalidade dos dois códigos `CTL` como pendente. `RFG...` está incompleto; a nota associa-o ao acesso do repositório de deploy no GitHub, mas não revela o código correto. **Não peça esses códigos por tentativa.** O gestor ou administrador do repositório deve confirmar se também se aplicam ao Educador e fornecer seus nomes completos.

Para o GitHub, o guia geral descreve acesso baseado em time/equipe e menor permissão necessária. Assim, permissão do cluster não substitui inclusão no time do GitHub, e acesso ao código não garante acesso de escrita ou ao repositório de deploy.

### Aplicando isso à sigla IAA

O que podemos concluir sem adivinhar:

1. Use `IAA` quando o formulário pedir a sigla do projeto, desde que o registro aprovado do Educador também confirme esse código.
2. Para o perfil de desenvolvimento na referência, consulte no painel o item `ALMFDIAA`.
3. Consulte `ALMFEIAA` somente para identificar o perfil RT/necessidade de criação de grupos mencionada nos roteiros; peça ao gestor para confirmar seu uso no trabalho do Educador.
4. `DEVMSAPV` e `DEVARQAP` descrevem pessoas/papéis que aprovam etapas. Como sua solicitação já foi aprovada, não há razão documentada para você solicitá-los para si.
5. Confirme à parte a equipe/time de GitHub, o grupo ITSM e se `CTL02000`, `CTL00030` ou o código completo `RFG...` são realmente necessários para o Educador.

### Como solicitar sem pedir acesso em excesso

O guia de onboarding do GitHub orienta selecionar o menor papel necessário, usando o nome da equipe cadastrado no GENTI/BusinessMap. A referência do Consultor afirma que a concessão dos papéis de cluster é feita pelo gestor responsável.

Prepare para o gestor uma solicitação objetiva com: projeto Educador Financeiro, sigla `IAA`, sua matrícula/identificação, atividade que você precisa executar e ambiente/ferramenta necessária. Peça que confirme o item exato no catálogo de acessos antes de aprová-lo. Separe as necessidades:

| Preciso fazer isto | Pergunta de acesso a confirmar |
|---|---|
| Ver/desenvolver o código | Qual time GitHub do Educador deve me incluir e com qual nível de permissão? |
| Acompanhar/atuar em HML no cluster e ArgoCD | Qual papel permite as ações necessárias no namespace HML de IAA? Os arquivos não comprovam o código exato para HML. |
| Acompanhar/atuar em DES, se houver | O papel apropriado é `ALMFDIAA`? |
| Acessar RT, criar grupo ou executar tarefa de operação | `ALMFEIAA` é necessário para qual ação concreta e em qual ambiente? |
| Usar formulário que exige vínculo organizacional | Qual grupo ITSM da equipe IAA devo selecionar? |
| Usar acesso legado referido como `CTL` ou `RFG` | Qual é o código completo, a finalidade atual e a confirmação de que se aplica a este serviço? |

Se um papel aparecer como aprovado mas o sistema continuar negando acesso, um roteiro de OpenShift informa que pode ser necessário sincronizar: Portal AIC → **Meus acessos** → **Sincronizar meus acessos**. Esse passo é documentado para o acesso à criação de Secrets; não está comprovado como correção universal de todos os papéis.

Para criar Secrets no OpenShift, existe outro papel específico citado pelo roteiro: `<SIGLA>#SCRT`, que para IAA seguiria o padrão textual `IAA#SCRT`. O mesmo roteiro diz que em produção somente gestores podem criar Secrets. **Isso não é requisito para navegar no GitHub ou acompanhar um deploy**, e só deve ser considerado se a equipe decidir que você precisa criar Secrets.

Fontes: [papéis registrados pelo Consultor](plg-agent-consult-fin.wiki/Home.md#1-acessos-e-pré-requisitos), [pré-requisitos e aprovações da oferta](DOCUMENTACAO_GERAL/provisionar-microsservico.md), [onboarding GitHub](DOCUMENTACAO_GERAL/onboarding-github.md#modelo-de-acesso--solicitação) e [permissão de Secrets](DOCUMENTACAO_GERAL/roteiros-master/openshift/Como_criar_secret.md).

### Certificados: dois fluxos que não devem ser confundidos

Na referência do Consultor aparecem certificados para **duas conexões diferentes**. O nome “Secret” quer dizer que o OpenShift guarda material protegido; não quer dizer que todo desenvolvedor deva ou possa copiar seu conteúdo.

| Material na referência | Serve para | Como aparece configurado |
|---|---|---|
| IDH/mTLS | O agente sair do cluster e se autenticar no Gateway Outbound para acessar o modelo. | O chart declara o operador `idhmtls`, habilitado, que provisiona uma Secret montada no contêiner. No snapshot de HML, o nome da Secret é `idh-mtls`, com arquivos `tls.crt`, `tls.key` e `ca.crt`. |
| BBcert/TLS de ingresso | Proteger a conexão **de entrada** de quem chama o agente por HTTPS. | O chart declara `bbcert`, com o nome da Secret TLS da aplicação e o hostname que o certificado deve atender. A matrícula em `custodianteCertificado` identifica quem receberá notificações da PKI/OaaS no exemplo. |

Esse contraste explica a ordem registrada pela wiki do Consultor: primeiro publicar um deploy inicial com os operadores configurados; depois conferir, no OpenShift, se as Secrets foram criadas. A documentação descreve o resultado automatizado do chart; ela **não manda cada desenvolvedor pedir um certificado de usuário VPN para a aplicação**.

Há ainda uma diferença de grafia entre documentos do Consultor: a wiki chama a Secret de IDH `idhmtls`; o `values.yaml` HML declara `idh-mtls`. Use o nome definido no `values.yaml` que foi entregue para o Educador, não escolha entre esses nomes por conta própria. Os arquivos do Educador ainda serão conferidos.

### O que `IAA#SCRT` permite — e o que não permite

O roteiro geral de OpenShift diz que o papel `<SIGLA>#SCRT` é requisito para **criar** um Secret pela interface do OpenShift. Aplicando a sigla informada, o formato esperado seria `IAA#SCRT`, sujeito a confirmação no painel. O roteiro também diz que, em PRD, somente gestores podem criar Secrets.

Isso não comprova que `IAA#SCRT` permita ler ou exportar as Secrets geradas pelos operadores. Também não é necessário só para navegar nos repositórios, acompanhar o ArgoCD ou deixar o chart provisionar os certificados. Não solicite esse papel para obter a chave privada sem confirmação explícita do responsável por segurança/OpenShift.

### Como o certificado passa a existir e o que falta saber

O caminho descrito para o agente de referência é:

```text
Chart e values configuram IDH e BBcert
→ primeiro deploy do serviço
→ operadores tentam provisionar as Secrets no cluster
→ equipe confere estado e eventos no ArgoCD/OpenShift
→ aplicação usa a Secret IDH em runtime para mTLS de saída
```

O chart declara a intenção de provisionar; por si só, o arquivo não comprova sucesso, emissão ou validade atual do certificado. No Educador, será preciso conferir o `values.yaml`, a saúde do ArgoCD e se as Secrets existem, sem registrar seus valores.

Para executar o agente **localmente**, a referência diz que ele precisa de AppKey, certificado cliente e chave privada apropriados; a CA pode depender da configuração de confiança. O material local não estabelece um processo oficial e autorizado para entregar esses arquivos a uma pessoa desenvolvedora. Embora a wiki antiga do Consultor mencione copiar dados das Secrets pelo console, o guia mais recente de certificados do workspace marca o canal/responsável exato como **não determinado** e recomenda pedir a disponibilização autorizada à equipe. Portanto, o passo comprovável é perguntar à equipe responsável qual canal aprovado usar; não presumir que o papel de criar Secrets autoriza extrair a chave privada existente.

### Páginas em `roteiros-master` que ajudam

| Página local | O que acrescenta para nós | Limite |
|---|---|---|
| [`kubernetes/Ref_papeis_de_acesso.md`](DOCUMENTACAO_GERAL/roteiros-master/kubernetes/Ref_papeis_de_acesso.md) | Aponta para o roteiro de papéis e níveis de acesso no TechBB. | O arquivo local apenas redireciona; não contém a tabela de papéis. |
| [`openshift/Como_criar_secret.md`](DOCUMENTACAO_GERAL/roteiros-master/openshift/Como_criar_secret.md) | Informa o papel `SIGLA#SCRT`, sincronização possível pelo Portal AIC e o fluxo de criação de um Secret na interface. | É sobre criar um Secret; não é procedimento para obter a Secret IDH nem copiar chave privada. |
| [`certificado/Como_configurar_BBCert.md`](DOCUMENTACAO_GERAL/roteiros-master/certificado/Como_configurar_BBCert.md) | Direciona à documentação atual do chart BBcert no TechBB. | O arquivo local não contém o procedimento atual; configurações específicas do Educador ainda devem ser conferidas. |
| [`certificado/Como_solicitar_certificados_PKI_SSL_interno.md`](DOCUMENTACAO_GERAL/roteiros-master/certificado/Como_solicitar_certificados_PKI_SSL_interno.md) | Direciona à página atual de solicitação de certificado PKI SSL interno. | Esse é um roteiro genérico de PKI/SSL; não demonstra sozinho que esse certificado seja o IDH mTLS do Gateway. |
| [`certificado/Como_configurar_mtls_gateway_api.md`](DOCUMENTACAO_GERAL/roteiros-master/certificado/Como_configurar_mtls_gateway_api.md) | Aponta para configuração mTLS entre Quarkus e API Gateway. | O exemplo é Quarkus e API Gateway; a aplicação de agente Python e o Gateway Outbound podem exigir configuração distinta. |
| [`FAQ/certificados.md`](DOCUMENTACAO_GERAL/roteiros-master/FAQ/certificados.md) | Explica CA/PKI, certificados por ambiente e problemas comuns de HTTPS/Ingress. | Certificados raiz/intermediários para confiar em servidores não são a identidade cliente IDH nem a chave privada do agente. |
| [`enxovalBB/Como_solicitar_acessos_BB.md`](DOCUMENTACAO_GERAL/roteiros-master/enxovalBB/Como_solicitar_acessos_BB.md) | Explica como obter certificado pessoal `vpn_cert.p12` para acesso à VPN. | **Não é o certificado da aplicação** para o Gateway nem o certificado HTTPS provisionado pelo BBcert. |

Os roteiros antigos de solicitação PKI, configuração BBcert e papéis Kubernetes informam que foram **movidos para páginas da TechBB**. Os links de destino estão dentro desses arquivos. A busca web desta consulta não retornou essas páginas internas, então a tabela acima descreve o material disponível localmente e não substitui a leitura autenticada das páginas atuais.

Você está neste ponto:

```text
Aprovação obtida
   ↓
Confirmar provisionamento e localizar recursos
   ↓
Verificar onde estão os repositórios
   ├─ Ainda no GitLab → solicitar migração pela oferta AIC
   └─ Já no GitHub → conferir acesso e arquivos
   ↓
Conferir template e execução do build
   ↓
Confirmar publicação da imagem
   ↓
Configurar/conferir deploy HML e acompanhar ArgoCD
   ↓
Testar aplicação, chamada real ao modelo e API em HML
   ↓
Concluir validação HML e preparar a liberação para PRD
```

Antes de disparar um build que possa implantar automaticamente, prepare os acessos, a Secret de AppKey e a configuração dos operadores descritos na etapa 8. Se DES existir, aplique também as verificações a esse ambiente, respeitando a sequência exigida pela equipe. Algumas automações podem já ter executado etapas posteriores; confira os resultados existentes antes de repetir ações.

## 2. Confirmar que o provisionamento terminou

**Onde:** [TechBB](https://tech.bb.com.br/), na solicitação/instância que recebeu a aprovação.

1. Abra o link da solicitação que vocês acompanharam durante a aprovação.
2. Confira se a solicitação é do Educador Financeiro, identificado por você como `mf-edu-fin`.
3. Leia o resultado da execução/provisionamento disponível nessa página.
4. Localize os links dos recursos entregues, principalmente os repositórios e o ArgoCD.
5. Abra cada link e confira se o recurso existe e se você consegue acessá-lo.

No roteiro da **oferta genérica de microsserviços**, o caminho documentado depois do provisionamento é:

```text
Meus Microsserviços → pesquisar a instância criada → validar os recursos
```

Na referência do Consultor Financeiro, a página de origem é uma instância OAS, de onde se acessam ArgoCD e catálogos. Para o Educador, abra a sua própria solicitação aprovada. O link da instância `mf-edu-fin` ainda não foi fornecido; não substitua palavras no endereço de outro agente para tentar encontrá-la.

**Resultado esperado:** os recursos estão identificados e acessíveis. A indicação de aprovação, sozinha, não demonstra que a criação terminou.

**Ambiente inicial deste guia: HML.** Confirme na entrega o namespace/projeto HML, a aplicação ArgoCD e o repositório/branch de deploy correspondente. A documentação disponível mostra caminhos por ambiente, mas não comprova se a oferta do Educador exige uma validação prévia em DES. Se DES existir, registre seus recursos e confirme a sequência da equipe; sua ausência não permite presumir que HML já esteja provisionado.

Se houver falha ou os links não aparecerem, registre: identificação da solicitação, nome do componente, etapa que falhou e mensagem exibida. O roteiro de provisionamento pede essas informações ao solicitar suporte. O endereço exato do canal de suporte da oferta de agente não consta no material local.

Fontes: [provisionamento de microsserviços](DOCUMENTACAO_GERAL/provisionar-microsservico.md#validação-final) e [origem da instância do agente](plg-agent-consult-fin.wiki/Home.md).

### Anote os dados da entrega

| Informação | O que registrar |
|---|---|
| Solicitação/instância | Educador Financeiro / `mf-edu-fin`; registrar o link da aprovação |
| Componente | Copiar o nome completo entregue, incluindo prefixos, se existirem |
| Código | Link do repositório do programa |
| Deploy | Todos os links de deploy entregues |
| ArgoCD HML | Link fornecido pela instância ou pelo README |
| OpenShift HML e namespace | Console e nome do projeto fornecidos na entrega; não deduzir o endereço por substituição de DES por HML |
| DES, se houver | Registrar existência, links, namespace e sua participação no fluxo; se não houver, registrar “não provisionado/não aplicável” conforme a entrega |
| Equipe | Nome da equipe responsável conforme cadastro corporativo |
| Resultado | Concluído, em andamento ou mensagem de erro efetivamente exibida |

## 3. Identificar os repositórios: um detalhe importante da entrega

Use esta tabela para acompanhar os exemplos. A última coluna será preenchida quando os links do Educador estiverem disponíveis.

| Finalidade | EXEMPLO — CONSULTOR | Educador Financeiro (`mf-edu-fin`) |
|---|---|---|
| Código original no GitLab | [plg-agent-consult-fin](https://fontes.intranet.bb.com.br/plg/plg-agent-consult-fin/plg-agent-consult-fin.git) | Substituir pelo link correto |
| Deploy DES original no GitLab | [des-plg-agent-consult-fin](https://fontes.intranet.bb.com.br/plg/plg-agent-consult-fin/des-plg-agent-consult-fin.git) | Substituir pelo link correto, se houver DES |
| Deploy HML original no GitLab | [hml-plg-agent-consult-fin](https://fontes.intranet.bb.com.br/plg/plg-agent-consult-fin/hml-plg-agent-consult-fin.git) | Substituir pelo link correto |
| Deploy PRD original no GitLab | [prd-plg-agent-consult-fin](https://fontes.intranet.bb.com.br/plg/plg-agent-consult-fin/prd-plg-agent-consult-fin.git) | Substituir pelo link correto |
| Código no GitHub | [bbvinet/plg-agent-consult-fin](https://github.com/bbvinet/plg-agent-consult-fin) | Substituir pelo link correto |
| Deploy no GitHub | [bbvinet/deploy-plg-agent-consult-fin](https://github.com/bbvinet/deploy-plg-agent-consult-fin) | Substituir pelo link correto |

Os endereços gerais do [TechBB](https://tech.bb.com.br/) e da [Oferta AIC](https://tech.bb.com.br/p/aic/ofertas) são os caminhos documentados de entrada na plataforma. Os links de repositório, instância e ArgoCD identificam recursos específicos de cada projeto.

Na referência do Consultor Financeiro, a entrega original contém quatro repositórios GitLab: código e deploys DES, HML e PRD. A wiki posterior registra dois repositórios GitHub: código e deploy. No deploy GitHub da referência, os ambientes ficam nas branches `cloud/desenvolvimento`, `cloud/homologacao` e `cloud/producao`. Confira se essa estrutura foi entregue ao Educador.

**Não está documentado como os três repositórios originais de deploy foram transformados nesse repositório com branches.** Portanto, este guia não manda migrar os quatro isoladamente nem afirma que uma solicitação migra todos. Essa parte precisa ser esclarecida pelo resultado da oferta AIC ou pelo suporte da oferta.

Fontes de referência: endereços de repositórios em `endpoint consult.txt` e [wiki do Consultor](plg-agent-consult-fin.wiki/Home.md#2-repositórios-e-git). O registro original também contém credenciais; compartilhe somente os links dos repositórios necessários, sem o arquivo completo.

## 4. Se o código ainda estiver no GitLab: solicitar a migração

Se o repositório correto já estiver entregue no GitHub, siga para a etapa 5. A existência de um espelho no GitLab não significa que é preciso migrar novamente.

**Onde:** [Oferta AIC no TechBB](https://tech.bb.com.br/p/aic/ofertas).

1. Abra o endereço acima no navegador corporativo e autentique-se se solicitado.
2. Clique em **Migrar Repositório**.
3. Na seção **Identificação**, preencha os dados organizacionais solicitados.
4. Para projetos do Movimento Aceleração Digital, o roteiro pede **Linha de Negócio / CoE** e **Squad**.
5. Para projetos fora desse movimento, pede **Gerência Executiva** e **Equipe Lógica**.
6. Use os dados da equipe responsável. O nome do componente não permite deduzir esses campos.
7. Na seção **Dados do Projeto**, preencha **Nome do Componente** com o nome do repositório no GitLab.
8. Revise o resumo e confirme a solicitação.
9. Acompanhe o status na mesma tela.
10. Quando a oferta apresentar o resultado, abra o repositório de destino e confira o nome e o conteúdo.

**EXEMPLO — CONSULTOR: como transformar o link em nome do componente:**

```text
Link entregue:
https://fontes.intranet.bb.com.br/plg/plg-agent-consult-fin/plg-agent-consult-fin.git

Campo Nome do Componente:
plg-agent-consult-fin
```

Esse preenchimento serve para explicar o formulário. Ao solicitar a migração do Educador, use o nome do repositório dele. Não envie uma nova solicitação para o Consultor ao acompanhar o exemplo.

**Como aplicar a mesma regra ao Educador:**

```text
Se o último trecho do endereço entregue for:
.../mf-edu-fin.git

Nome do Componente será:
mf-edu-fin
```

Esse exemplo é condicional. Se o nome entregue tiver sigla ou outro prefixo, mantenha o nome completo. O campo recebe o nome real do repositório, sem a URL completa e sem `.git`. Não presuma que o nome curto da solicitação seja também o nome final do repositório.

**Resultado esperado:** solicitação concluída e acesso ao repositório correspondente no GitHub.

**Se falhar:** o roteiro manda abrir uma Issue, isto é, um registro de suporte. Ele não informa o endereço exato desse registro; use o canal apresentado pela oferta AIC. Informe componente, solicitação e mensagem do erro.

**Antes de solicitar migração dos deploys:** confira se a entrega já inclui o repositório de deploy do Educador no GitHub. Se não incluir, a informação que falta é: “Para o componente entregue para mf-edu-fin, como migrar os repositórios de deploy por ambiente para o repositório de deploy no GitHub?”. Não há resposta comprovada nas fontes locais.

Fonte: [roteiro de migração](DOCUMENTACAO_GERAL/onboarding-solicitacao-migracao-repositorios.md).

## 5. Conferir o acesso ao GitHub

**Onde:** link de destino fornecido pela migração ou pela instância.

**EXEMPLO — CONSULTOR:** abra o [repositório de código](https://github.com/bbvinet/plg-agent-consult-fin) e observe a aba **Code**. Depois, abra o [repositório de deploy](https://github.com/bbvinet/deploy-plg-agent-consult-fin). Para o Educador, os dois endereços serão substituídos pelos links corretos.

1. Entre no GitHub com a identidade corporativa, pelo SSO — a autenticação corporativa centralizada.
2. Abra o repositório de código.
3. Confira se a aba **Code** mostra os arquivos do projeto.
4. Abra separadamente o repositório de deploy.
5. Confira se você consegue visualizar seus arquivos e suas branches.

Conseguir ver código não comprova permissão para alterar código ou fazer deploy. Os repositórios podem ter acessos diferentes.

Se o acesso for negado, o onboarding documenta este caminho:

```text
Painel de Acesso → Gerência/Linha/CoE → equipe correspondente
```

O roteiro pede o nome da equipe conforme GENTI/BusinessMap. Também orienta verificar permissões com o gestor ou administrador do repositório. A URL exata desse painel não está no material consultado.

Fonte: [onboarding GitHub](DOCUMENTACAO_GERAL/onboarding-github.md).

## 6. Conferir o template recebido

**Onde:** repositório de **código**, aba **Code**. Comece lendo `README.md`.

| Arquivo/pasta | Para que serve | O que conferir |
|---|---|---|
| `README.md` | Instruções do próprio projeto | Preparação, execução e requisitos do template entregue |
| `aic.json` | Configuração do build corporativo | Versão Python utilizada pela esteira |
| `setup.py` | Metadados e requisitos do programa | Nome do pacote e requisito de Python |
| `Dockerfile` | Receita da imagem | Versão de Python usada no contêiner |
| `<pacote_python>/__init__.py` | Versão do programa, conforme o template de referência | Nome real do pacote entregue e valor de `__version__` |
| `agent_config.yaml` | Configurações do agente | Ambiente do Gateway, modelo e integrações configuradas |
| `.env.example` | Modelo de variáveis de ambiente | Nomes das configurações necessárias |
| `tests/` | Testes do projeto | Testes unitários e de integração disponíveis |
| `.github/workflows/ci.yaml` | Acionamento da esteira | Nome do workflow, branches e execução manual |

No snapshot do Consultor Financeiro, o README pede **Python 3.11**, `aic.json` declara `3.11` e `setup.py` exige `>=3.11`. Para reproduzir essa referência, use Python 3.11. Um guia local menciona 3.12 em algumas seções; isso não deve substituir o requisito do projeto recebido.

O Educador começa do zero: confira no README e no `setup.py` qual pacote foi entregue e se há instrução de renomeação. O nome `plg_agent_consult_fin` pertence ao Consultor e não deve ser copiado para o Educador. A sequência exata de renomeação depende dos arquivos do novo template; eles ainda não foram inspecionados.

O primeiro marco é conseguir construir e executar o template entregue ao Educador. Depois, personalize as instruções e a lógica para educação financeira nos arquivos indicados pelo README. Ainda não temos esses arquivos nem as regras de negócio do Educador para prescrever alterações linha a linha.

O roteiro corporativo trata os workflows como administrados pela integração contínua. Não é necessário criar ou reescrever `ci.yaml` para iniciar esta jornada.

Fontes: [README do agente](plg-agent-consult-fin-main/README.md), [aic.json](plg-agent-consult-fin-main/aic.json), [setup.py](plg-agent-consult-fin-main/setup.py) e [acionar build](DOCUMENTACAO_GERAL/acionar-build.md).

## 7. Verificar o build existente antes de executar outro

**Onde:** repositório de **código** → **Actions**.

**EXEMPLO — CONSULTOR:** [Actions do repositório de código](https://github.com/bbvinet/plg-agent-consult-fin/actions). Use a página para entender onde ficam as execuções; ao executar o fluxo do Educador, abra **Actions** no repositório dele.

1. Abra **Actions**.
2. Selecione **Esteira de Build Python** — o arquivo local também contém um símbolo de engrenagem no nome.
3. Abra a execução correspondente à branch e à versão que você pretende usar.
4. Confira qual commit foi processado. Ele identifica exatamente o código usado.
5. Leia o resultado dos jobs, que são as tarefas da automação.
6. Se houver erro, abra o job que falhou e leia seu log.
7. Procure o resultado da **publicação da imagem**, além do resultado do build.
8. Anote o nome/endereço da imagem publicada e sua tag.

**Build bem-sucedido não basta para concluir que a imagem foi publicada.** Na jornada documentada do MCP, uma imagem chegou a ser construída, mas sua publicação foi bloqueada pela combinação de branch e versão. O deploy depois não conseguia encontrá-la.

### Se for necessário executar manualmente

**Antes:** confirme o repositório de código do Educador e a versão a executar. Como esse build pode iniciar um deploy, confira previamente a preparação de credenciais e do ambiente na etapa 8. O workflow precisa declarar `workflow_dispatch` e estar na branch padrão do repositório para disponibilizar o acionamento manual; você também precisa de acesso de escrita. Depois, no botão, escolhe a branch que será executada. Fonte: [execução manual no GitHub](https://docs.github.com/en/actions/how-tos/manage-workflow-runs/manually-run-a-workflow).

Para o exemplo, o acionamento pela interface é:

```text
Repositório do código → Actions → Esteira de Build Python
→ Run workflow → escolher a branch → revisar a opção → Run workflow
```

Passo a passo na tela:

1. Na página do repositório, clique em **Actions** na barra superior.
2. Na lista à esquerda, clique em **Esteira de Build Python**.
3. No lado direito, clique em **Run workflow**. Se o botão não aparecer, confira os requisitos acima com o administrador do repositório.
4. No campo de branch, escolha a branch cujo código você quer compilar. Para o primeiro deploy do Educador, não escolha uma branch só pelo nome: confirme com a equipe qual versão deve ser integrada/publicada.
5. Se aparecer `publica_versao_fechada_branch_auxiliar`, mantenha o padrão desmarcado até saber que a equipe precisa publicar uma versão fechada fora de `main`. Essa opção não deve ser marcada como tentativa de “consertar” um build.
6. Clique novamente em **Run workflow** para iniciar.
7. A execução nova aparece na lista. Clique nela para acompanhar o estado e abrir os jobs.

Executar o workflow pode publicar uma imagem e acionar deploys, dependendo da branch, da versão e dos resultados. Confira branch e opções antes de iniciar; não rode uma segunda execução enquanto outra estiver processando a mesma versão.

No workflow local, pushes em `main`, `feat/**`, `feature/**` e `fix/**` podem disparar CI. `develop` não consta nessa lista. O arquivo também oferece uma opção específica para publicação de versão fechada em branch auxiliar; portanto, não é correto afirmar que branches auxiliares “nunca publicam”.

Os jobs de deploy automático para DES e HML dependem de resultados da CI. Eles podem aparecer como não executados. Confira os logs e a publicação antes de tentar disparar novamente.

**Resultado esperado desta etapa:** versão da imagem comprovadamente publicada, com execução identificada. Essa é a versão que poderá ser usada no deploy.

### Como essas Actions se encadeiam no exemplo do Consultor

O workflow de código verificado tem jobs de CI, `CD (desenvolvimento)` e `CD (homologação)`. Os jobs CD chamam workflows reutilizáveis da AIC e recebem como dados a versão, o ambiente e o repositório de deploy. Eles só são executados se a CI devolver os indicadores de autodeploy correspondentes.

Na tela **Actions** do repositório de código, você pode ver a sequência numa mesma execução:

```text
push no código
→ CI / Esteira de Build Python
→ testes e construção/publicação da imagem
→ jobs CD conforme os indicadores devolvidos pela CI
→ atualização automatizada da configuração de deploy
```

No arquivo verificado, `CD (desenvolvimento)` depende de `autodeploy == 'true'`; `CD (homologação)` depende desse mesmo indicador e de `autodeploy-hom == 'true'`. Ambos declaram dependência da CI; HML não declara dependência do sucesso do job DES. Quando os dois indicadores são verdadeiros, o workflow também tenta DES. Portanto, **começar o guia por HML não transforma automaticamente essa esteira em uma execução exclusiva de HML**. Se DES não existir, confirme com a equipe AIC como a esteira do Educador tratará esse job; não altere o workflow corporativo por tentativa.

Se o job `CD (homologação)` concluiu e o ArgoCD mostra a versão nova em HML, **não é necessário repetir a mesma troca de tag manualmente** no repositório de deploy. Se o autodeploy ficou como ignorado/não executado ou se a versão não chegou a HML, investigue o resultado e então avalie o fluxo manual da próxima seção, usando a imagem cuja publicação foi comprovada. Se houver DES, confira seu job e ambiente separadamente.

> No histórico da jornada do MCP há uma explicação antiga dizendo que branches auxiliares “nunca” publicam imagens. O workflow efetivo do Consultor tem um input para publicação de versão fechada fora de `main`, e a condição depende das regras da AIC. Não trate a frase “nunca publica” como regra geral: use o resultado do job e os outputs desta execução.

Fontes: [acionar build](DOCUMENTACAO_GERAL/acionar-build.md), [workflow efetivo do agente](plg-agent-consult-fin-main/.github/workflows/ci.yaml) e [problemas registrados na jornada MCP](plg-agent-consult-fin.wiki/MCP-Server-Oficial-Consultor-PJ.md#jornada-de-deploy).

## 8. Conferir o primeiro deploy em HML (e DES, se houver)

### A ordem das credenciais: o que entra antes e o que nasce no primeiro deploy

Há credenciais necessárias **antes de a aplicação iniciar** e certificados cujo provisionamento o chart/operador **solicita na implantação inicial**. A emissão pode levar tempo ou falhar; confirme o resultado no ambiente.

| Item | Quando configurar | Onde fica no exemplo | Para que serve |
|---|---|---|---|
| AppKey do Gateway Outbound | Obter/autorizá-la e disponibilizá-la antes do primeiro pod tentar iniciar o agente | Secret OpenShift chamada `env`, injetada no contêiner por `envFrom`; a chave esperada no exemplo é `GATEWAY_OUTBOUND_GW_APP_KEY` | Autoriza o agente a chamar o Gateway/modelo |
| Certificado IDH e chave privada | Configurar o operador no `values.yaml`; o operador provisiona a Secret na implantação inicial | Secret `idh-mtls` no snapshot HML; o pod monta `tls.crt`, `tls.key`, `ca.crt` em `/app/certs` | Permite mTLS de saída para o Gateway |
| Certificado BBcert | Configurar o operador BBcert no `values.yaml`; ele solicita/provisiona o certificado para o host do serviço | Secret TLS de ingresso, por exemplo `plg-agent-consult-fin-tls` | Protege o acesso HTTPS de entrada ao agente |
| Arquivo `.env` do desenvolvedor | Só ao executar o agente no próprio computador | Arquivo local `.env` na raiz do código; não vai para o GitHub | Fornece AppKey e caminhos locais de certificados ao processo local |

**Antes do primeiro deploy HML (caminho principal deste guia):**

1. Obtenha a AppKey do Educador pelo processo autorizado para a aplicação e o Gateway. A referência diz que a AppKey vem do Catálogo de Aplicações, mas não documenta o passo a passo específico do Educador nem confirma se o recebimento será por e-mail.
2. Abra o `values.yaml` da branch HML do Educador e confira se o contêiner importa `env` (`envFrom.secretRef.name: env`) e se o chart ativa o operador IDH (`idhmtls.enabled`). Se BBcert estiver habilitado, confira também a matrícula custodiante, o ambiente PKI, o hostname do Educador e o nome da Secret onde o certificado será exportado. No código de referência, o agente lê `GATEWAY_OUTBOUND_GW_APP_KEY` ao iniciar; sem essa variável, não consegue construir o provedor do modelo. Se DES existir, confira sua branch separadamente.
3. No console OpenShift do namespace HML correto, confira se já existe uma Secret `env`. Se existir, não a recrie nem a substitua: peça ao responsável para confirmar, sem revelar o conteúdo, que a chave do Gateway está provisionada. Se DES existir, não presuma que a Secret dele também esteja disponível em HML.
4. Se `env` não existir e sua equipe for responsável por criá-la, o roteiro local de OpenShift ensina: **Secrets → selecionar o Project correto → Create → Key/Value Secret**; informe nome `env`, chave `GATEWAY_OUTBOUND_GW_APP_KEY` e o valor da AppKey no próprio formulário protegido. Para isso o roteiro cita `<SIGLA>#SCRT` — na sigla informada, o padrão seria `IAA#SCRT`, a confirmar no painel. Em PRD, o roteiro diz que somente gestores criam Secrets.
5. Não inclua AppKey em `values.yaml`, código, commit, PR, print ou chat. Não mostre o valor da Secret ao conferir sua existência.
6. Faça/acompanhe a primeira publicação e deploy HML. O operador IDH deverá provisionar a Secret de certificado; o operador BBcert deverá provisionar o certificado de entrada se estiver habilitado. Se DES existir e fizer parte da entrega, valide-o também com as configurações desse ambiente.
7. Só considere a etapa pronta quando o ArgoCD e os recursos no namespace mostrarem que o pod está pronto e que as Secrets referenciadas pelo `values.yaml` existem. Confira nomes e estado, nunca copie o conteúdo da chave privada.
8. Faça a primeira chamada `/chat` a partir do ambiente autorizado. Isso valida a combinação em runtime: variável AppKey + certificado/chave IDH + configuração do Gateway/modelo.

Se a equipe de plataforma criou a Secret `env` automaticamente, os passos de criação manual não se aplicam. O `values.yaml` de referência comprova a referência a `env`, mas o material disponível **não comprova quem cria essa Secret nem de onde vem a AppKey do Educador**. Confirme isso no namespace HML antes do primeiro pod; não trate `IAA#SCRT` como autorização automática para ler Secrets já existentes. Se DES existir, faça a mesma confirmação separadamente no namespace DES.

Para uso **local**, obtenha AppKey/certificado/chave por canal oficialmente autorizado e então prepare o `.env` conforme o Apêndice A. No caminho descrito pela wiki, o IDH é provisionado pelo primeiro deploy, portanto a entrega desse material depende dessa emissão; o material disponível não comprova que esse seja o único caminho possível. No fluxo de cluster verificado, a AppKey entra pela Secret `env` e os arquivos IDH são montados da Secret indicada no chart, sem depender do `.env` do computador.

Fontes da referência: [valores HML](deploy-plg-agent-consult-fin-cloud-homologacao/values.yaml), [provider que exige AppKey ao iniciar](plg-agent-consult-fin-main/plg_agent_consult_fin/llm/gateway_outbound.py), [inicialização do agente](plg-agent-consult-fin-main/plg_agent_consult_fin/app.py), [wiki sobre AppKey e certificados](plg-agent-consult-fin.wiki/Home.md), [guia para criar Secret](DOCUMENTACAO_GERAL/roteiros-master/openshift/Como_criar_secret.md) e [guia de certificados](ambiente/GUIA_CERTIFICADOS_E_SECRETS_CONSULT_FIN.md).

**Caminho principal — HML:** repositório de **deploy** → branch `cloud/homologacao` → `values.yaml`. Se DES existir e fizer parte do fluxo, use também `cloud/desenvolvimento`, sempre com os valores próprios daquela branch.

**EXEMPLO — CONSULTOR:** comece em [bbvinet/deploy-plg-agent-consult-fin](https://github.com/bbvinet/deploy-plg-agent-consult-fin), selecione a branch e abra o arquivo. As alterações para `mf-edu-fin` serão feitas no repositório próprio do Educador, quando identificado.

1. Abra o repositório de deploy entregue para o agente.
2. Selecione `cloud/homologacao` no seletor de branches para seguir o caminho principal deste guia.
3. Confirme a branch antes de abrir qualquer edição.
4. Abra `values.yaml`.
5. Localize o bloco do componente do Educador. Seu nome deve corresponder ao alias do chart entregue; não use o nome do Consultor.
6. Dentro dele, confira `service` → `enable`.
7. Confira `deployment` → `enable`.
8. Confira `deployment` → `containers` → `tag`.
9. Compare a tag com a imagem cuja publicação você verificou na etapa 7.

**Exemplo de estrutura; não substitua o arquivo inteiro por este trecho:**

```yaml
ALIAS_DO_COMPONENTE_ENTREGUE:
  service:
    enable: true
  deployment:
    enable: true
    containers:
      tag: "VERSAO_PUBLICADA"
```

`ALIAS_DO_COMPONENTE_ENTREGUE` e `VERSAO_PUBLICADA` são indicações para leitura, não valores para copiar. Preserve a chave real do arquivo entregue e use a tag real publicada pelo build do Educador. A versão do Consultor não identifica uma imagem do Educador.

`service.enable` habilita o Service, que encaminha chamadas internas. `deployment.enable` habilita a criação do Deployment, que administra os pods. São recursos distintos. Um guia anterior escreveu `enabled`; no arquivo verificado, a chave é **`enable`**, sem “d” no final.

**Se os valores de HML já estiverem corretos e a versão já estiver implantada, siga para a verificação no ArgoCD.** Se DES existir e também precisar de implantação, confira a branch `cloud/desenvolvimento` separadamente.

Se precisar alterar, faça uma alteração pontual nesses campos, preservando os espaços de indentação do YAML. Confira a diferença antes de salvar. O apêndice B mostra como enviar uma alteração pelo Git. O push na branch de ambiente aciona o fluxo de deploy; não é apenas um salvamento de arquivo.

Fontes: [deploy Cloud](DOCUMENTACAO_GERAL/deploy-plataforma-cloud.md), [estrutura verificada em HML](deploy-plg-agent-consult-fin-cloud-homologacao/values.yaml) e [README do agente](plg-agent-consult-fin-main/README.md#configuração-inicial-do-helm-chart). O snapshot local é de HML do Consultor; os arquivos do Educador em HML e em DES, se houver, ainda precisam ser conferidos.

### Como o workflow de deploy entra

O repositório de deploy de referência também tem uma Action chamada **Deploy**. Seu [workflow local](deploy-plg-agent-consult-fin-cloud-homologacao/.github/workflows/cd.yaml) permite estas entradas:

| O que você faz | O que está configurado no exemplo |
|---|---|
| Envia uma mudança pela branch `cloud/desenvolvimento` | Dispara o workflow de deploy DES. |
| Envia uma mudança pela branch `cloud/homologacao` | Dispara o workflow de deploy HML. |
| Envia uma mudança pela branch `cloud/producao` | Dispara o workflow de deploy PRD, sujeito ao processo de liberação aplicável. |
| Abre/reabre PR destinado a `cloud/producao` | Também dispara o workflow para o evento de PR configurado. Isso não quer dizer que o PR foi aprovado ou que a produção já foi atualizada. |
| Usa **Actions → Deploy → Run workflow** | Execução manual está declarada; revise branch/evento e orientações da equipe antes de rodar. |

Para DES/HML pelo caminho manual documentado: faça a mudança necessária em `values.yaml` na branch daquele ambiente e envie o commit. O push dispara **Actions → Deploy**, que chama um workflow reutilizável da AIC. A documentação de deploy informa que o ArgoCD então reflete a configuração. Depois confira os logs da Action e, separadamente, a aplicação no ArgoCD.

#### Caminho pela tela do GitHub quando o `values.yaml` precisa mudar

Este é o procedimento manual para o caminho principal em HML. Ele altera uma configuração que pode atualizar o cluster, então faça-o apenas depois de confirmar a imagem publicada e a branch correta. Para DES, aplique o mesmo princípio usando `cloud/desenvolvimento` apenas se esse ambiente existir e fizer parte do fluxo aprovado.

1. Abra o repositório de deploy do Educador. Confirme o nome no topo do GitHub; os links do Consultor são apenas exemplo.
2. No seletor de branches, escolha `cloud/homologacao`.
3. Abra `values.yaml` e confirme que está vendo o arquivo nessa branch.
4. Clique no lápis (**Edit this file**) se sua conta e a proteção da branch permitirem edição direta.
5. Altere somente os valores necessários no bloco do serviço: habilitação de Service/Deployment conforme o template entregue e a tag que corresponde à imagem publicada.
6. Role até a área de commit. Escreva uma mensagem curta, por exemplo `chore(hml): configura primeira imagem do Educador`.
7. Se o GitHub oferecer **Commit directly to the `cloud/homologacao` branch**, essa opção envia a mudança diretamente e inicia a Action configurada para essa branch.
8. Se a branch for protegida ou o GitHub exigir PR, crie a branch/PR oferecida pela tela, selecione como destino `cloud/homologacao` e siga as regras de aprovação do repositório. O deploy só deve ser esperado depois que a mudança chegar à branch de ambiente.
9. Volte à aba **Actions** do repositório de deploy. Abra a execução **Deploy** iniciada pelo push/merge e acompanhe o job `deploy`.
10. Quando a Action terminar, abra o link de ArgoCD do ambiente e confirme sincronização, saúde e versão.

Se a tela mostrar outra branch, nome de workflow ou regra de aprovação, pare e confira o README e as proteções do repositório do Educador. Os detalhes exatos dele só serão confirmados quando tivermos seu link.

#### Acionamento manual pelo botão `Run workflow` no deploy

O workflow de deploy da referência declara `workflow_dispatch`. Para usar o botão, também precisam estar satisfeitos os requisitos de branch padrão e permissão descritos na etapa 7. O caminho em HML é:

```text
Repositório de deploy → Actions → Deploy → Run workflow
→ escolher `cloud/homologacao` → Run workflow
```

No YAML de referência, o workflow recebe o nome da branch selecionada e o evento. Ele não declara campo para digitar outra tag nem outro ambiente. Portanto, antes de executar, confira no `values.yaml` da branch escolhida se a tag e os toggles já estão corretos. O botão reaplica/processa a configuração existente; ele não substitui a publicação da imagem e não corrige um `values.yaml` errado.

Para o procedimento normal de DES/HML, a documentação descreve mudança de `values.yaml` e push na branch do ambiente. Use o disparo manual só quando houver um motivo para reaplicar a configuração existente ou quando o README/equipe do próprio Educador orientar esse caminho.

**Não existe um botão “subir cluster” nessas instruções.** Actions processa o workflow corporativo; ArgoCD reconcilia os arquivos de deploy com o estado do cluster. É essa reconciliação que resulta nos recursos atualizados.

### Qual caminho usar para o primeiro deploy?

1. **Verifique o build:** no repositório de código, abra **Actions → Esteira de Build Python**. Confirme branch/commit e publicação da imagem.
2. **Verifique o CD automático para HML:** na mesma execução, abra `CD (homologação)`. Se concluiu, veja se atualizou o deploy HML. Se aparece ignorado/não executado, leia a condição/log; não conclua que houve erro sem examiná-los. Se DES existir, confira também `CD (desenvolvimento)` separadamente.
3. **Evite duplicidade:** se o autodeploy atualizou a tag, vá ao ArgoCD. Se não atualizou, continue pelo repositório de deploy.
4. **Confira o `values.yaml`:** na branch `cloud/homologacao`, verifique Service, Deployment e tag real publicada. Não copie a configuração de outro ambiente para HML.
5. **Faça a mudança necessária:** use edição/commit direto se permitido; se a branch pedir PR, abra PR para `cloud/homologacao` e aguarde a incorporação.
6. **Acompanhe a Action `Deploy`:** abra a execução disparada no repositório de deploy. Verifique o job e mensagens de erro.
7. **Acompanhe o ArgoCD:** confirme `Synced` e `Healthy`, o pod pronto e a versão da imagem esperada.
8. **Teste o serviço:** valide health e `/chat` no ambiente correto. Só depois considere o primeiro deploy concluído.

Não acione autodeploy no código e workflow manual do deploy em paralelo para a mesma alteração. Primeiro descubra qual deles já está atualizando a tag, para evitar corridas entre duas execuções.

### Resultado: parece o deploy já observado?

**Sim, no resultado final.** A validação anterior do Consultor mostrou a imagem construída, o `values.yaml` atualizado, o ArgoCD sincronizado e um pod DES executando a nova versão. Isso é uma referência de resultado, não evidência de que HML do Educador já foi executado. O fluxo do MCP também documenta Actions de deploy acionando recursos e o ArgoCD chegando a `Healthy`/`Synced`.

**As etapas têm responsabilidades distintas:**

| Etapa | Onde acontece | O que deve aparecer ao final |
|---|---|---|
| Build/publicação | Actions no repositório de código | CI passou e uma tag de imagem foi publicada. |
| CD automático ou atualização manual | Job CD no código ou `values.yaml` no deploy | A configuração de ambiente aponta para a tag publicada. |
| Workflow de deploy | Actions no repositório de deploy | Workflow reutilizável de deploy executou sem erro. |
| Reconciliação/execução | ArgoCD e cluster | Aplicação sincronizada/saudável e pod pronto com a imagem esperada. |
| Teste funcional | Dentro do pod ou endpoint de serviço autorizado | Health e chamada `/chat` respondem conforme o teste. |

O resultado não é garantido só porque o repositório está no GitHub. A história do MCP registra um deploy acionado corretamente que sincronizou os recursos, mas o pod falhou porque a imagem ainda não existia na tag pedida. Por isso, a prova deve cobrir a cadeia inteira, desde a publicação da imagem até a resposta do agente.

## 9. Acompanhar no ArgoCD

**Onde:** link do ArgoCD fornecido na instância OAS ou no item **Release Status** do README do repositório de deploy, quando presente.

1. Abra o link fornecido; não monte o hostname por suposição.
2. Confira se a aplicação é do Educador e do ambiente **HML**. Se também houver DES, verifique sua aplicação separadamente.
3. Confira o estado de sincronização e a saúde da aplicação.
4. Confira se a versão implantada corresponde à imagem escolhida.
5. Observe o estado do pod e a quantidade de contêineres prontos.
6. Se houver falha, consulte os detalhes/eventos do recurso afetado e os logs disponíveis.

| Indicação | Como interpretar |
|---|---|
| `Synced` | O estado acompanhado está sincronizado com a configuração desejada. |
| `Healthy` | Os recursos estão considerados saudáveis pelos critérios da plataforma. |
| Pod `Running` e pronto | O contêiner está executando e sua prontidão foi reconhecida. |
| `ImagePullBackOff` | A plataforma está falhando ao obter a imagem. Na jornada MCP, a tag ainda não havia sido publicada. Leia o evento para identificar a causa no seu caso. |

**Resultado esperado:** aplicação sincronizada e saudável, pod pronto e imagem correta. Isso ainda precisa ser complementado pelo teste funcional do agente.

Fontes: [deploy Cloud](DOCUMENTACAO_GERAL/deploy-plataforma-cloud.md) e [evidências do MCP](plg-agent-consult-fin.wiki/MCP-Server-Oficial-Consultor-PJ.md#evidencias-de-deploy-bem-sucedido).

## 10. Validar que o agente responde

Existem três verificações diferentes:

| Verificação | O que demonstra |
|---|---|
| Health check | A aplicação responde à consulta de saúde. |
| Chamada a `/chat` | O agente consegue processar a solicitação; no teste com provedor real, exercita o acesso ao modelo. |
| Chamada pela API catalogada | O caminho completo do consumidor até a aplicação funciona, incluindo autenticação e roteamento. |

### Teste dentro do pod

O registro do Consultor comprova estas chamadas **dentro do pod**. Use-as no Educador depois de conferir que o template recebido preserva os endpoints e a porta 8080. Elas também servem para uma aplicação local nessa porta. Não execute no terminal do seu computador esperando atingir o cluster: `localhost` significa “o ambiente em que este comando está sendo executado”.

O caminho de cliques para abrir o terminal do pod na versão atual do console não está documentado no material. Use o console do OpenShift entregue para HML e a orientação do responsável pelo ambiente para acessar o pod correto. Se também testar DES, selecione o console/namespace de DES.

Consulta de saúde:

```bash
curl --max-time 10 -i http://localhost:8080/health/ready
```

Procure o código HTTP `200`, que indica sucesso na requisição.

Chamada funcional:

```bash
curl --max-time 90 -i -X POST http://localhost:8080/chat \
  -H 'Content-Type: application/json' \
  -d '{"message":"Quanto é 2 + 2?"}'
```

Procure HTTP `200` e um objeto com `reply`. O texto gerado pode variar. O registro de DES documentou resposta correta a esse teste com o modelo real.

### Teste pela API catalogada

A aplicação interna expõe `/chat`; a wiki registra `/v1/chat` no endereço catalogado. Não troque os caminhos indiscriminadamente.

Use o endereço e a autorização fornecidos no catálogo para seu ambiente. O material não comprova um procedimento completo de obtenção de autorização para essa chamada, portanto não há aqui um comando externo universal pronto para copiar.

O registro de 26/08/2026 documentou saúde interna e `/chat` funcionando, mas erro no acesso externo. Esse é um exemplo de por que “pod saudável” e “API acessível ao consumidor” precisam ser verificados separadamente. O erro daquele registro não foi retestado nesta elaboração.

Fonte: [validação documentada em DES](plg-agent-consult-fin.wiki/validacao-agente-des-e-jornada-mcp.md), usada como referência para o teste; execute novamente no namespace HML do Educador.

## 11. Se o agente não conseguir chamar o modelo

O agente usa o Gateway Outbound para acessar o LLM, o modelo que gera as respostas. No projeto verificado, esse acesso depende de configuração do ambiente e credenciais.

| Item | O que precisa estar disponível |
|---|---|
| Endereço do Gateway | URL correta do ambiente em `agent_config.yaml` |
| Modelo | Identificador autorizado para a aplicação |
| AppKey | Credencial da aplicação, fornecida à execução |
| Certificado e chave | Identificação usada na conexão mTLS |
| CA/confiança | Configuração para validar o certificado do servidor |

As variáveis do agente são `GATEWAY_OUTBOUND_GW_APP_KEY`, `KEY_STORE_CERT_PATH`, `KEY_STORE_KEY_PATH` e `TRUST_STORE_CA_PATH`.

No cluster, essas informações chegam ao contêiner por dois caminhos declarados no template de referência: a AppKey vem da Secret `env` (`envFrom`) e os arquivos IDH são montados como volume nos caminhos `/app/certs/tls.crt`, `/app/certs/tls.key` e `/app/certs/ca.crt`. O `values.yaml` traduz esses caminhos para as variáveis `KEY_STORE_CERT_PATH`, `KEY_STORE_KEY_PATH` e `TRUST_STORE_CA_PATH`. O nome real das Secrets no Educador depende do `values.yaml` entregue.

Localmente, não use a Secret do cluster como se fosse um `.env` automaticamente disponível. Você precisará de uma cópia autorizada da AppKey e de arquivos de certificado/chave entregues pelo canal aprovado, além de criar seu próprio `.env` local. A documentação disponível não define esse canal para o Educador; o próximo passo é solicitar orientação à equipe responsável por AgentOps/PKI.

**Falta um procedimento oficial completo, nas fontes locais, para obter esses materiais.** O próximo passo comprovável é pedir à equipe responsável a disponibilização autorizada e a confirmação do ambiente. Não preencha AppKey no código nem publique `.env` ou chaves no GitHub.

No deploy HML local, os arquivos de certificado são referenciados em `/app/certs` e há referências a Secrets do cluster. Isso comprova a configuração declarada, não que os arquivos/credenciais estejam presentes ou válidos no cluster agora.

Fonte: [guia de certificados e secrets](ambiente/GUIA_CERTIFICADOS_E_SECRETS_CONSULT_FIN.md#8-o-que-preciso-obter-antes-do-chat).

## 12. Homologação e produção

### Homologação — HML

**É possível seguir direto para HML se DES não existir ou não fizer parte do provisionamento do Educador**, desde que a equipe responsável confirme que o projeto/namespace, o repositório e a branch de deploy HML estão provisionados e autorizados para receber a primeira implantação. A documentação local descreve branches separadas por ambiente, mas não determina que DES seja uma dependência técnica obrigatória nem autoriza pular uma validação exigida pela equipe. Se DES existir e fizer parte do fluxo aprovado, valide-o primeiro.

Antes de disparar a primeira implantação HML:

1. Abra o repositório de deploy na branch `cloud/homologacao`.
2. Confirme que o projeto/namespace HML do Educador existe e que o ArgoCD acompanha essa aplicação.
3. Confira se a imagem do Educador foi publicada e se a tag usada em HML corresponde a essa imagem.
4. Confira os valores próprios de HML e confirme com a equipe responsável a existência/provisionamento das credenciais requeridas nesse ambiente: AppKey na Secret referenciada pelo chart e certificados mTLS provisionados/configurados para HML. A primeira implantação pode acionar operadores de certificado quando habilitados; isso não cria automaticamente a AppKey, salvo se a equipe confirmar esse mecanismo.
5. Se houver mudança necessária, envie-a pelo fluxo da branch HML; não crie Secrets com valores de DES nem reutilize certificados de DES sem autorização explícita.
6. Acompanhe a Action e a aplicação HML no ArgoCD; confirme pod pronto, sincronização e Secrets referenciadas por nome/estado, sem revelar conteúdo.
7. Faça os testes de saúde, chamada funcional e acesso pela API correspondente em HML.

Não copie integralmente o `values.yaml` de DES sobre o de HML: os arquivos contêm configurações próprias de ambiente. A falta de certificados/Secrets em DES não impede por si só o caminho HML, mas HML precisa ter suas próprias dependências satisfeitas antes de a chamada funcional funcionar.

### Produção — PRD

O README do agente informa que a configuração inicial de produção precisa ser elaborada pela equipe. A existência de um link de repositório PRD no registro original não comprova que essa configuração esteja pronta.

O procedimento documentado de **abertura de release** é:

1. Preparar as alterações de produção em uma nova branch criada a partir de `cloud/producao`.
2. Abrir um Pull Request com destino a `cloud/producao`.
3. Acompanhar a abertura automática do bilhete de release.

O material local não descreve todos os campos, aprovadores, gates e passos posteriores necessários para concluir essa liberação. Assim, ele permite orientar a abertura, mas **não comprova um passo a passo completo até a implantação em PRD**. Essa lacuna deve ser preenchida com o roteiro da release da equipe antes dessa etapa.

Fontes: [deploy Cloud](DOCUMENTACAO_GERAL/deploy-plataforma-cloud.md#4-como-abrir-uma-release) e [aviso no README](plg-agent-consult-fin-main/README.md).

## Apêndice A — Preparar uma cópia local do agente, se precisar alterar código

Você não precisa clonar o projeto para consultar o portal, solicitar migração ou acompanhar Actions. Este apêndice entra quando precisar desenvolver ou testar o código no computador.

**Ambiente dos comandos:** terminal Linux do Pengwin/WSL, com Git e Python 3.11 disponíveis. Não cole os blocos Bash no PowerShell. A instalação do Pengwin não faz parte da entrega da solicitação de agente.

> O `.env` deste apêndice é **somente para executar o agente localmente**. O deploy no cluster usa Secrets OpenShift. Nunca faça `git add .env` e não copie a chave privada para o repositório.

### A1. Verificar ferramentas e autenticação

Execute um comando por vez:

```bash
git --version
python3.11 --version
git config user.name
git config user.email
```

Depois, ainda no mesmo terminal, execute:

**EXEMPLO — CONSULTOR:** a URL de código tem este formato concreto: `https://github.com/bbvinet/plg-agent-consult-fin.git`. No procedimento abaixo, informe a URL correspondente do Educador quando disponível. Assim, os comandos posteriores de envio continuam associados ao projeto correto.

```bash
printf 'Cole a URL HTTPS do repositorio de codigo do Educador no GitHub: '
read -r repo_codigo_url
git ls-remote "$repo_codigo_url" HEAD
```

O terminal aguardará você colar a URL real e apertar Enter. Cole somente a URL do repositório, sem token ou senha. A variável `repo_codigo_url` guarda esse endereço para os comandos seguintes no mesmo terminal.

O último comando consulta o repositório sem copiar ou alterar arquivos. O resultado esperado é um identificador de commit seguido de `HEAD`. Se a autenticação falhar, conclua o acesso corporativo antes de clonar.

O material registra uso de PAT/SSO e também SSH. Use o método configurado para sua conta pela equipe; este guia não escolhe permissões de token por suposição.

### A2. Clonar

Escolha uma pasta de trabalho onde ainda não exista outra cópia com o mesmo nome. No terminal aberto nessa pasta:

```bash
git clone "$repo_codigo_url" mf-edu-fin-codigo
cd mf-edu-fin-codigo
git remote -v
git branch --show-current
git status --short
```

`clone` cria a cópia na pasta local `mf-edu-fin-codigo`; `cd` entra nela; `remote -v` mostra o endereço associado; `status --short` mostra alterações locais. Confirme que o endereço exibido é o do Educador. Se a pasta já existir, não repita o clone por cima dela: confira a cópia existente.

### A3. Preparar Python e executar testes

Dentro da pasta do código, após conferir que o template entregue mantém os requisitos e arquivos da referência (Python 3.11, `requirements.txt` e extras `unit,integration`):

```bash
python3.11 -m venv .venv
source .venv/bin/activate
python --version
python -m pip install -r requirements.txt
python -m pip install -e ".[unit,integration]"
python -m pip check
python -m pytest tests/unit
python -m pytest tests/integration
```

`venv` cria um ambiente isolado. `activate` seleciona esse ambiente para o terminal atual. `pip` instala as dependências; `pytest` executa os testes.

Use o acesso corporativo a pacotes já configurado no ambiente. Se a instalação falhar, guarde a mensagem do erro. O número de testes aprovados depende da versão do código; este guia não promete a contagem de um registro anterior.

### A3.1 Criar o `.env` local (somente para chamada real ao LLM)

Faça esta etapa depois de clonar o repositório e de receber, por meio autorizado, os arquivos e a credencial. Não é necessária para executar testes unitários que usam respostas simuladas.

1. Na pasta principal do código, copie o modelo:

   ```bash
   cp .env.example .env
   ```

2. Abra `.env` no editor. Não imprima o arquivo no terminal e não o cole em mensagens.
3. Preencha `GATEWAY_OUTBOUND_GW_APP_KEY` com a AppKey autorizada do Educador.
4. Preencha `KEY_STORE_CERT_PATH` com o caminho local absoluto do certificado de cliente IDH.
5. Preencha `KEY_STORE_KEY_PATH` com o caminho local absoluto da chave privada correspondente.
6. Preencha `TRUST_STORE_CA_PATH` com o caminho local da CA quando a equipe indicar que ela deve ser usada. O código de referência também pode usar a confiança padrão do sistema se a CA não for informada; essa opção precisa ser testada no Pengwin.
7. Salve `.env` e confirme apenas que o Git o ignora, sem mostrar conteúdo:

   ```bash
   git check-ignore -q .env && echo ".env ignorado pelo Git" || echo "PARE: .env nao esta ignorado"
   ```

8. Antes de carregar o arquivo, confirme que nenhum `<PREENCHER>` ficou nos valores obrigatórios e que o template `SERVICE_NAME={{ codebase_name }}` foi substituído por um valor válido para o Educador. Deixe vazias as opções realmente não usadas; não deixe os marcadores literais, pois o shell pode interpretá-los como comandos/redirecionamentos.

9. Carregue o `.env` nesta sessão do terminal:

   ```bash
   set -a
   source .env
   set +a
   ```

10. Use as verificações sem imprimir segredos:

   ```bash
   [ -n "$GATEWAY_OUTBOUND_GW_APP_KEY" ] && echo "AppKey presente" || echo "AppKey ausente"
   [ -r "$KEY_STORE_CERT_PATH" ] && echo "Certificado legivel" || echo "Certificado pendente"
   [ -r "$KEY_STORE_KEY_PATH" ] && echo "Chave legivel" || echo "Chave pendente"
   [ -r "$TRUST_STORE_CA_PATH" ] && echo "CA legivel" || echo "CA ausente ou caminho nao configurado"
   ```

Não compartilhe os arquivos `.crt`, `.key`, o `.env` ou a saída completa do terminal. Arquivo legível não comprova que certificado e chave correspondem ou que o Gateway autoriza a chamada.

### A4. Preparar uma mudança de código

Crie uma branch de trabalho ainda inexistente:

```bash
git switch -c feat/configuracao-inicial
```

Abra o arquivo que precisa corrigir no editor. Na referência deste template, a configuração Python documentada em `aic.json` é `"versaoPython": "3.11"`. Confira os requisitos do Educador antes de aplicar esse ajuste. Se o arquivo já estiver correto, não há mudança a fazer nesse campo.

Depois de uma alteração necessária, confira:

```bash
git diff
git status --short
```

Para uma mudança feita somente em `aic.json`, o envio é:

```bash
git add aic.json
git commit -m "fix: ajusta Python da esteira para 3.11"
git push -u origin feat/configuracao-inicial
```

Esse exemplo só se aplica se o arquivo realmente foi corrigido. Se a identificação Git estiver ausente, configure seu nome e e-mail corporativo no repositório antes do commit. Se a organização exigir assinatura de commits, siga o procedimento da equipe.

O push da branch `feat/...` pode iniciar CI. Para incorporar o código em `main`, use um PR conforme o fluxo de revisão da equipe. O merge pode iniciar publicação e autodeploy; confira os resultados nas etapas 7 a 9.

Fontes: [guia local anterior](ambiente/GUIA_FINAL_MINIMALISTA_CONSULT_FIN_HML.md), [README](plg-agent-consult-fin-main/README.md) e [workflow](plg-agent-consult-fin-main/.github/workflows/ci.yaml). A versão Python foi alinhada aos arquivos do projeto.

## Apêndice B — Enviar uma alteração de deploy DES pelo Git

Use este apêndice apenas se o deploy precisar de mudança e sua conta tiver a permissão correspondente. Os comandos enviam a configuração de DES e podem alterar a aplicação em execução.

No Pengwin, em uma pasta de trabalho, para uma nova cópia:

**EXEMPLO — CONSULTOR:** a URL de deploy é `https://github.com/bbvinet/deploy-plg-agent-consult-fin.git`. No bloco abaixo, a entrada será o link de deploy do Educador. O exemplo do Consultor serve para reconhecer o formato do endereço.

```bash
printf 'Cole a URL HTTPS do repositorio de deploy do Educador no GitHub: '
read -r repo_deploy_url
git clone --branch cloud/desenvolvimento "$repo_deploy_url" mf-edu-fin-deploy
cd mf-edu-fin-deploy
git branch --show-current
git status --short
```

No pedido de URL, cole o endereço real do deploy do Educador e aperte Enter. `mf-edu-fin-deploy` é apenas o nome da pasta local. Confirme a branch `cloud/desenvolvimento`. Se a branch não existir, não crie uma branch vazia como substituição: falta conferir a entrega do repositório.

Abra `values.yaml` no editor, faça somente a alteração necessária descrita na etapa 8 e salve. Depois:

```bash
git diff -- values.yaml
```

Confira se somente os campos planejados mudaram e se a indentação foi preservada. Com a diferença revisada:

```bash
git add values.yaml
git commit -m "chore(des): ajusta configuracao de deploy"
git push origin cloud/desenvolvimento
```

Se a branch for protegida e o push for recusado, use o fluxo de PR exigido pelo repositório; não use `--force`. Se o autodeploy já tiver atualizado o ambiente, evite enviar uma cópia local desatualizada. Em qualquer rejeição por divergência, confira a versão remota antes de prosseguir.

Após o envio, abra **Actions** no repositório de deploy para acompanhar a execução e depois confira o ArgoCD. Para HML, siga o mesmo princípio usando a branch e a configuração de HML; não reutilize os valores de DES.

Fonte do acionamento: [deploy Cloud](DOCUMENTACAO_GERAL/deploy-plataforma-cloud.md). Os comandos Git explicitam como realizar o commit/push descrito pelo roteiro.

## Checklist do ponto em que estamos

- [x] Agente identificado: Educador Financeiro (`mf-edu-fin`), projeto novo na mesma oferta do Consultor — informação fornecida por você.
- [x] Aprovação obtida — informação fornecida por você.
- [ ] Provisionamento concluído e recursos identificados.
- [ ] Repositório de código localizado e acessível.
- [ ] Situação da migração para GitHub conferida.
- [ ] Repositório de deploy e branches de ambiente identificados.
- [ ] Template e configuração Python conferidos.
- [ ] Antes do primeiro pod: confirmada a origem/autorização da AppKey do Educador e a Secret `env` com `GATEWAY_OUTBOUND_GW_APP_KEY` no namespace correto, sem expor seu valor.
- [ ] Configuração do deploy conferida: Secret IDH referenciada e montada; BBcert de ingresso revisado quando habilitado.
- [ ] Após o primeiro deploy: pod pronto e Secrets de certificado provisionadas pelos operadores confirmadas por nome/estado.
- [ ] Para chamada local, se necessária: recebidos certificados/chave por canal autorizado e `.env` local criado e ignorado pelo Git.
- [ ] Build e publicação da imagem comprovados.
- [ ] HML validado como ambiente inicial, com pod pronto e versão correta (e DES validado também se existir e fizer parte do fluxo).
- [ ] Teste de saúde e chamada funcional aprovados.
- [ ] API catalogada validada pelo caminho do consumidor.
- [ ] Procedimento e configuração PRD completados pela equipe.

**A ação imediata é abrir a solicitação aprovada, confirmar o provisionamento e localizar os links dos repositórios.** É essa verificação que define se o próximo passo será migração, liberação de acesso ou acompanhamento do build.
