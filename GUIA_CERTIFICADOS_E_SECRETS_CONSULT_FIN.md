# Certificados e secrets do CONSULT FIN

Guia para entender os acessos do Agent sem expor informações sensíveis. **Hello World** significa receber uma resposta real do modelo pelo `/chat`. Apenas iniciar o serviço não basta.

Este guia usa o código e os documentos disponíveis no workspace. Configuração declarada e registros anteriores não comprovam o funcionamento atual de homologação (HML).

## 1. Visão geral

O Agent é o programa que recebe sua mensagem. O Gateway Outbound é a porta de saída para o LLM, o modelo de linguagem que produz a resposta.

```text
Agent local
  ↓
AppKey
  +
certificado cliente
  +
chave privada
  +
CA (confiança para validar o servidor)
  ↓
Gateway Outbound
  ↓
LLM
```

A confiança da CA pode vir de um arquivo configurado ou da confiança padrão do ambiente, se suficiente.

**AppKey e mTLS são coisas diferentes.** A AppKey é uma credencial enviada ao Gateway. O mTLS usa certificado e chave para identificar o cliente durante a conexão segura. Um não substitui o outro.

## 2. O que é cada item

Um **secret** é uma informação que deve permanecer protegida. Uma variável terminada em `PATH` guarda um caminho, não o conteúdo do arquivo.

| Item | O que é e para que serve | Contém segredo? Pode compartilhar? | Obrigatório para o Hello World? |
|---|---|---|---|
| `GATEWAY_OUTBOUND_GW_APP_KEY` | Credencial da aplicação enviada ao Gateway. | **Sim. Nunca compartilhar o valor.** O nome da variável pode ser informado. | **Sim**, válida e autorizada. |
| `KEY_STORE_CERT_PATH` | Caminho do certificado que identifica o Agent como cliente. | O caminho não é a chave privada. O certificado é público no sentido criptográfico, mas pode revelar dados internos. Compartilhar caminho ou certificado somente se autorizado. | **Sim**, para fornecer o certificado apropriado ao fluxo atual com mTLS. |
| `KEY_STORE_KEY_PATH` | Caminho da chave privada correspondente ao certificado. | O caminho não é a chave. **O conteúdo do arquivo é secreto e nunca deve ser compartilhado.** | **Sim**, junto do certificado cliente. |
| `TRUST_STORE_CA_PATH` | Caminho de um arquivo de autoridades certificadoras (CAs) para validar o servidor. Tem prioridade no provider. | Um arquivo de CAs não contém chave privada. Ainda assim, compartilhar material ou detalhes internos somente se autorizado. | **Não em todos os casos.** É uma forma de fornecer confiança. Se configurado, o arquivo precisa ser válido e legível. |
| `REQUESTS_CA_BUNDLE` | Caminho de um conjunto de CAs. É a alternativa usada pelo provider quando `TRUST_STORE_CA_PATH` está ausente ou vazia; também aparece em integrações opcionais. | Não é uma senha nem chave privada. Compartilhar detalhes internos somente se autorizado. | **Não em todos os casos.** É outra forma de fornecer confiança. Se selecionado pelo provider, precisa ser válido e legível. |

**Obrigatório é validar o servidor com sucesso.** Sem as duas variáveis de CA, o provider mantém `verify=True` e pode usar a confiança padrão do ambiente. Qual opção será necessária no seu Pengwin: **NÃO DETERMINADO**, até a execução real.

Outras credenciais previstas no projeto:

| Item | Onde entra no fluxo | Necessário no Hello World básico? |
|---|---|---|
| `RAG_CLIENT_ID` | Token de acesso para recuperação de documentos, chamada RAG, enviado em `X-Client-Id`. | Não. A função está desligada no YAML analisado. Nunca compartilhar o token. |
| `GUARDRAIL_EXTERNAL_CLIENT_ID` | Token para o serviço externo de curadoria, enviado em `X-Client-Id`. | Não. A curadoria externa está desligada no YAML analisado. Nunca compartilhar o token. |
| `APPLICATION_INSIGHTS_CONNECTION_STRING` | Configuração de conexão para envio de telemetria ao Azure Application Insights. | Não. Não compartilhar a connection string. |

O MCP, protocolo usado para acessar ferramentas externas, está configurado com autenticação `none` no YAML analisado. O código prevê token do tipo Bearer quando essa opção é habilitada; não há credencial MCP obrigatória demonstrada para essa configuração. `SSL_CERT_FILE` aparece no exemplo como configuração de confiança para bibliotecas, mas não é lida diretamente pelo provider do Gateway.

Fontes: [.env.example](../plg-agent-consult-fin-main/.env.example), [configuração do Agent](../plg-agent-consult-fin-main/agent_config.yaml), [configuração em código](../plg-agent-consult-fin-main/plg_agent_consult_fin/config.py) e [README](../plg-agent-consult-fin-main/README.md).

## 3. Certificado, chave e CA

```text
tls.crt → certificado público: identifica o cliente
tls.key → chave privada: prova a identidade do cliente
ca.crt  → CA: ajuda a validar o certificado/cadeia do servidor
```

- Certificado e chave precisam corresponder: formar o mesmo par.
- A CA é uma autoridade certificadora em que o cliente confia para verificar o servidor e sua cadeia de certificados.
- A CA não substitui o certificado cliente.
- Certificado cliente sem a chave privada não resolve a autenticação mTLS.
- **A chave privada nunca deve ser compartilhada em chats, documentação ou prints.**

Esses são os nomes usados na montagem HML. Arquivos locais podem ter outros nomes; as variáveis devem apontar para os arquivos corretos. Não é necessário configurar um arquivo separado de CA se a confiança padrão já for suficiente.

## 4. mTLS

TLS é a proteção da conexão usada pelo HTTPS. **mTLS** significa TLS mútuo: o cliente verifica o servidor, e o servidor também exige que o cliente apresente seu certificado e prove possuir a chave correspondente.

Receber `certificate required` pode indicar que:

- o DNS, que transforma o nome do servidor em endereço, funcionou;
- a comunicação pela rede funcionou até um servidor TLS;
- o servidor foi alcançado e exige certificado cliente.

O alerta, sozinho, não confirma toda a rota nem a identidade do servidor final, especialmente se houver intermediários. **Não significa autenticação concluída, AppKey aceita ou acesso ao modelo autorizado.**

O [registro de continuação do Hello World](CONTINUACAO_HELLO_WORLD_CONSULT_FIN.md) documenta uma tentativa anterior sem certificado cliente que recebeu esse erro. Isso não comprova o estado atual do ambiente.

## 5. O que acontece no código

O provider, componente que prepara a conexão com o modelo:

1. Lê `GATEWAY_OUTBOUND_GW_APP_KEY` do ambiente do processo. Sua ausência provoca erro.
2. Lê os caminhos em `KEY_STORE_CERT_PATH` e `KEY_STORE_KEY_PATH`. Só configura o par cliente quando ambos estão preenchidos.
3. Escolhe a confiança do servidor: primeiro `TRUST_STORE_CA_PATH`; se ausente ou vazia, `REQUESTS_CA_BUNDLE`.
4. Se houver caminho de CA selecionado, carrega esse arquivo em um contexto TLS. Sem esses caminhos, mantém `verify=True`.
5. Prepara o cliente HTTPS assíncrono com a validação do servidor e, quando fornecidos, certificado e chave do cliente. A conexão real acontece ao fazer a requisição.
6. Envia a AppKey no header `x-application-key`, um campo da requisição HTTP. Remove o header `Authorization` nesse transporte.

O `api_key="dummy"` do código é apenas um preenchimento exigido pela biblioteca; não é uma credencial real do modelo.

**Atenção à leitura do fonte:** o comentário que menciona “sem verificação” não descreve o comportamento executado. A validação continua ativa. Uma CA prioritária inválida causa erro; não há tentativa automática da alternativa nesse caso.

As variáveis precisam estar disponíveis no processo do Agent. Só criar um `.env` não garante seu carregamento. O exemplo do projeto documenta a exportação na sessão do terminal; nunca exiba seu conteúdo para pedir ajuda.

Fonte: [provider do Gateway](../plg-agent-consult-fin-main/plg_agent_consult_fin/llm/gateway_outbound.py).

## 6. HML

Nos manifests disponíveis, homologação declara o Secret Kubernetes `idh-mtls`. Um Secret é um recurso do cluster usado para fornecer material protegido à aplicação.

| Arquivo do Secret | Caminho no container | Variável que aponta para ele |
|---|---|---|
| `tls.crt` | `/app/certs/tls.crt` | `KEY_STORE_CERT_PATH` |
| `tls.key` | `/app/certs/tls.key` | `KEY_STORE_KEY_PATH` |
| `ca.crt` | `/app/certs/ca.crt` | `TRUST_STORE_CA_PATH` |

A montagem de `/app/certs` está declarada como somente leitura. `idhmtls` está habilitado com o nome de Secret `idh-mtls`.

> **`idh-mtls` ≠ certificado de ingress `bbcert`**

- **`idh-mtls`:** material que o Agent usa na conexão de saída para o Gateway, incluindo identidade do cliente e confiança no servidor.
- **`bbcert`:** gerenciamento declarado do certificado do ingress, a entrada HTTPS pela qual outros clientes acessam o Agent. Está habilitado e exporta para o Secret `plg-agent-consult-fin-tls`, referenciado pelo ingress.

O certificado de entrada do Agent não deve ser confundido com seu certificado de cliente para sair ao Gateway.

Há também importação de variáveis do Secret `env`. Seu conteúdo, inclusive a presença de AppKey válida, é **NÃO DETERMINADO**. Não foram acessados Secrets nem consultado o cluster. Os registros disponíveis não comprovam validade atual dos certificados nem sucesso do `/chat`.

Fontes: [values de homologação](../deploy-plg-agent-consult-fin-cloud-homologacao/values.yaml) e [baseline](../BASELINE_V0_CONSULT_FIN.md), especialmente seções 10, 17 e 26.

## 7. Local x HML

| Item | Local | HML |
|---|---|---|
| AppKey | Variável de ambiente do Agent. | Importação do Secret `env` declarada; presença efetiva da AppKey: **NÃO DETERMINADO**. |
| Certificado cliente | Arquivo local apontado pela variável. | Secret `idh-mtls` montado, conforme manifests. |
| Chave privada | Arquivo local correspondente ao certificado. | Secret `idh-mtls` montado, conforme manifests. |
| CA / confiança | Arquivo/bundle configurado ou confiança padrão, se suficiente. Opção necessária no Pengwin: **NÃO DETERMINADO**. | `ca.crt` do Secret montado, apontado por `TRUST_STORE_CA_PATH`. |
| Ingress TLS | Não necessário para acessar o Agent por HTTP em localhost. A saída HTTPS para o Gateway continua validada. | `bbcert`/ingress declarados para HTTPS de entrada. |

## 8. O que preciso obter antes do `/chat`

- [ ] AppKey válida e autorizada.
- [ ] Certificado cliente apropriado para esse acesso.
- [ ] Chave privada correspondente ao certificado.
- [ ] Confiança correta para validar o servidor: CA configurada ou confiança padrão suficiente.
- [ ] Acesso de rede ao Gateway e autorização/disponibilidade do modelo.
- [ ] Caminhos locais de cert/key legíveis; caminho de CA legível se configurado.

**O que pedir à equipe:** disponibilização autorizada da AppKey, do certificado e da chave correspondente; confirmação das permissões para o Gateway/modelo; orientação sobre a confiança de CA adequada ao ambiente. Não peça que enviem os valores em chats ou documentação.

O `.env.example` menciona AppKey recebida por e-mail e material de certificados associado às secrets da aplicação provisionada. Isso não define um procedimento completo de solicitação e entrega autorizada. **Processo exato, canal aprovado e responsáveis: NÃO DETERMINADO.** Este guia não orienta extrair Secrets Kubernetes.

## 9. O que eu posso verificar sem expor secrets

Estes comandos são para **Bash no Pengwin/WSL**, o ambiente Linux no Windows. Execute sem rastreamento de comandos (`set -x`), pois ele pode expor valores mesmo em verificações simples.

```bash
[ -n "$GATEWAY_OUTBOUND_GW_APP_KEY" ] && echo "AppKey presente" || echo "AppKey ausente"

[ -r "$KEY_STORE_CERT_PATH" ] && echo "Certificado legível" || echo "Certificado pendente"

[ -r "$KEY_STORE_KEY_PATH" ] && echo "Chave legível" || echo "Chave pendente"

if [ -n "$TRUST_STORE_CA_PATH" ]; then
  [ -r "$TRUST_STORE_CA_PATH" ] && echo "CA legível" || echo "CA pendente"
elif [ -n "$REQUESTS_CA_BUNDLE" ]; then
  [ -r "$REQUESTS_CA_BUNDLE" ] && echo "Bundle CA legível" || echo "Bundle CA pendente"
else
  echo "Confiança padrão selecionada; suficiência ainda não verificada"
fi
```

“AppKey presente” não significa válida ou autorizada. “Arquivo legível” não comprova formato, validade, correspondência cert/key ou aceitação pelo servidor. A ausência de uma CA explicitamente configurada não é, por si só, erro.

Também é possível conferir os nomes das variáveis e os caminhos apenas no seu ambiente, sem copiá-los para chats. O funcionamento real da validação TLS no Pengwin permanece **NÃO DETERMINADO** até um teste real autorizado; este guia não executa esse teste.

## 10. O que NÃO compartilhar comigo ou com qualquer IA/chat

> **NUNCA compartilhar:**
>
> - AppKey;
> - senha;
> - token;
> - conteúdo de `.env`;
> - `tls.key`;
> - chave privada em qualquer formato;
> - conteúdo de Secret Kubernetes;
> - connection strings, que são configurações de conexão;
> - credenciais GitHub;
> - headers autenticados;
> - prints com valores sensíveis.

**Até logs podem conter informações sensíveis.** O provider registra caminhos de cert/key/CA e sua existência. Outros registros podem conter credenciais ou dados internos. Revise e remova essas informações antes de compartilhar; não envie logs completos sem revisão.

## 11. O que pode ser compartilhado com segurança

Prefira informações mínimas, sem valores sensíveis:

- Nome da variável, por exemplo `KEY_STORE_KEY_PATH`.
- `PRESENTE` / `AUSENTE`.
- `arquivo legível` / `arquivo não encontrado`.
- Tipo de erro ou código HTTP.
- Mensagem sanitizada: com credenciais, dados pessoais e detalhes internos removidos.
- Nome do arquivo sem conteúdo, se autorizado.

Um certificado ser público no sentido criptográfico não é autorização para publicar seu conteúdo ou informações internas.

## 12. Erros comuns

Os significados abaixo são pistas, não diagnósticos definitivos.

| Erro | Significado provável |
|---|---|
| `certificate required` | Certificado cliente não apresentado; o servidor exige mTLS. Não comprova AppKey aceita. |
| Arquivo não encontrado | Caminho de cert/key/CA incorreto ou arquivo indisponível. |
| Erro PEM | Formato textual do certificado/chave inválido ou arquivo inadequado. |
| Erro de chave/cert | Chave pode não corresponder ao certificado. |
| Falha ao verificar certificado do servidor | Confiança de CA insuficiente, cadeia incompleta ou outro problema de validade/identidade do servidor. |
| 401/403 no Gateway | Problema provável de AppKey ou autorização; verificar a origem e a mensagem sanitizada. |
| DNS falha | Problema de resolução de nome ou rede. |
| Timeout | Tempo de espera excedido; pode envolver rota, proxy, rede ou demora do serviço. |
| `/health/ready` OK mas `/chat` falha | Configuração carregada e grafo compilado não comprovam integração real com o modelo. |

O endpoint de prontidão não chama o LLM para validar o acesso. Fonte: [código da aplicação](../plg-agent-consult-fin-main/plg_agent_consult_fin/app.py).

## 13. Checklist final

- [ ] Tenho ambiente e dependências preparados conforme o [guia local](GUIA_PENGWIN_AO_HELLO_WORLD_CONSULT_FIN.md).
- [ ] A AppKey autorizada está disponível no ambiente do processo, sem ser exibida.
- [ ] Tenho certificado cliente apropriado e chave privada correspondente, em arquivos legíveis.
- [ ] Sei qual confiança será usada: `TRUST_STORE_CA_PATH`, fallback `REQUESTS_CA_BUNDLE` ou confiança padrão.
- [ ] Se configurei um arquivo de CA, ele é válido e legível.
- [ ] Tenho acesso ao Gateway e autorização para o modelo.
- [ ] Não confundi o material `idh-mtls` com o certificado de ingress `bbcert`.
- [ ] Mantive segredos fora de documentação, chats, prints e arquivos compartilhados.
- [ ] Sei que a validação TLS precisa funcionar e que não devo desativá-la para contornar erros.
- [ ] Após iniciar e testar com autorização, confirmarei uma resposta real pelo `/chat`; só então o Hello World estará concluído.

**Ainda NÃO DETERMINADO:** procedimento completo e responsáveis pela entrega autorizada; presença e validade efetivas da AppKey em HML; validade, correspondência e aceitação dos certificados reais do usuário; permissões e disponibilidade efetivas do Gateway/modelo; opção de confiança necessária no Pengwin; sucesso operacional atual do `/chat` local e em HML.
