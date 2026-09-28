Exemplo enviado pelo cliente:

```
{
  "message": "Quanto é 2 + 2?",
  "session_id": "sessao-123"
}
```

O caminho feliz é este:

```
CLIENTE
   │
   │ POST /chat
   │ JSON válido
   ▼
UVICORN
   │
   ▼
FASTAPI / STARLETTE
   │
   ▼
GuardrailsMiddleware
   │
   ├─ lê request
   ├─ valida entrada
   └─ deixa passar
   │
   ▼
ROTA /chat
   │
   ├─ FastAPI cria ChatRequest
   ├─ incrementa contador
   ├─ cria HumanMessage
   └─ chama graph.ainvoke(...)
   │
   ▼
AGENTE / LANGGRAPH
   │
   └─ devolve resultado
   │
   ▼
ROTA /chat
   │
   ├─ extrai resposta
   ├─ conta ToolMessages
   └─ cria ChatResponse
   │
   ▼
GuardrailsMiddleware
   │
   ├─ verifica saída
   └─ não encontra problema
   │
   ▼
FASTAPI / UVICORN
   │
   ▼
CLIENTE
```

Agora vamos devagar.

## 1. A requisição chega no Uvicorn

Imagine que alguém faça:

```
POST https://minha-api/chat
```

com:

```
{
  "message": "Quanto é 2 + 2?",
  "session_id": "sessao-123"
}
```

O Uvicorn está ouvindo a porta configurada, por exemplo `8080`.

Ele recebe a requisição HTTP e a entrega à aplicação ASGI:

```
Uvicorn
   ↓
app
```

Esse `app` é justamente:

```
app = FastAPI(...)
```

que vimos antes.

---

# 2. Antes da rota, a requisição encontra o middleware

Como anteriormente foi executado:

```
app.add_middleware(GuardrailsMiddleware)
```

a requisição não vai direto para:

```
chat()
```

Primeiro ela passa pelo middleware.

A primeira função chamada nele é:

```
GuardrailsMiddleware.dispatch(...)
```

O código verifica:

```
if request.method == "POST" and request.url.path == _CHAT_ROUTE:
```

e `_CHAT_ROUTE` vale:

```
"/chat"
```

Como nossa requisição é:

```
POST /chat
```

a condição é verdadeira.

Então ele chama:

```
return await self._guard_chat(request, call_next)
```

&#x20; guardrails_middleware

Nosso fluxo agora está aqui:

```
POST /chat
    ↓
dispatch()
    ↓
_guard_chat()
```

---

# 3. O middleware registra que recebeu um `/chat`

Ao entrar em `_guard_chat()`, ele monta atributos de observabilidade:

```
attrs_base = {
    "guardrail.route": "/chat",
    ...
}
```

e incrementa:

```
_guardrail_requests.add(1, attrs_base)
```

Então, nesse instante, uma métrica registra:

> passou mais uma requisição `/chat` pelos guardrails.

Depois nasce um span:

```
with _tracer.start_as_current_span(
    "guardrails.middleware.chat",
    ...
) as span:
```

e ele marca o tempo inicial:

```
t0 = time.perf_counter()
```

&#x20; guardrails_middleware

Então:

```
requisição chegou
     ↓
contador de guardrail +1
     ↓
span de tracing iniciado
     ↓
cronômetro iniciado
```

---

# 4. Middleware lê o JSON bruto

Aqui ainda não temos um `ChatRequest`.

Isso é importante.

O middleware está lidando com a requisição HTTP mais crua.

Ele faz:

```
body_bytes = await request.body()
```

Imagine que isso produza bytes equivalentes a:

```
{
  "message": "Quanto é 2 + 2?",
  "session_id": "sessao-123"
}
```

Depois ele faz:

```
body = json.loads(body_bytes)
```

Agora `body` é um dicionário Python:

```
{
    "message": "Quanto é 2 + 2?",
    "session_id": "sessao-123"
}
```

E pega somente:

```
message = body.get("message", "")
```

Então nasce:

```
message = "Quanto é 2 + 2?"
```

&#x20; guardrails_middleware

Observe:

```
HTTP body
   ↓
bytes
   ↓
json.loads()
   ↓
dict Python
   ↓
body["message"]
   ↓
"Quanto é 2 + 2?"
```

---

# 5. Guardrail de tamanho

Agora:

```
if len(message) > _MAX_INPUT_LEN:
```

Suponhamos que o limite seja `4096`.

Nossa pergunta é pequena.

Então:

```
"Quanto é 2 + 2?"

tamanho <= 4096
        ↓
PASSOU
```

Nenhuma resposta é criada aqui.

O código simplesmente continua.

---

# 6. Guardrail de prompt injection

Depois:

```
matched = check_injection(message)
```

No nosso cenário feliz:

```
matched = nada relevante
```

Então:

```
if matched:
```

é falso.

Continua.

---

# 7. Guardrail de PII

Depois:

```
if _BLOCK_PII_INPUT and contains_pii(message):
```

Nossa mensagem:

```
Quanto é 2 + 2?
```

não possui CPF, telefone, email etc.

Então:

```
PII detectada? NÃO
```

Continua.

---

# 8. Guardrail externo

Depois:

```
ext_reason = await check_external_guardrail(message, None)
```

No caminho feliz imaginamos que a verificação externa aceita a mensagem:

```
ext_reason = None
```

Então:

```
if ext_reason:
```

também não entra.

Até agora:

```
POST /chat
   ↓
tamanho       ✅
injection     ✅
PII           ✅
guard externo ✅
```

Essas verificações aparecem em sequência no middleware.   guardrails_middleware

---

# 9. O momento exato em que o middleware deixa a requisição seguir

Agora chegamos nesta linha:

```
response = await call_next(request)
```

&#x20; guardrails_middleware

Essa linha é muito importante.

Até aqui estávamos:

```
middleware
```

Agora ele basicamente diz:

> "Para mim essa requisição está aprovada. Continue a execução normal do FastAPI."

Então:

```
GuardrailsMiddleware
       ↓
call_next(request)
       ↓
FastAPI continua procurando a rota
```

Note que o middleware **não terminou**.

Ele está parado no:

```
await
```

esperando uma resposta voltar.

Mentalmente:

```
MIDDLEWARE
   │
   │ envia request para frente
   ▼
 restante da aplicação
   │
   │ ...
   │
   ▼
 resposta
   │
   └──────────────→ volta para o middleware
```

---

# 10. FastAPI encontra a rota `/chat`

O FastAPI já tinha registrado:

```
@app.post("/chat", ...)
async def chat(request: ChatRequest) -> ChatResponse:
```

&#x20; app

Então ele combina:

```
método: POST
path:   /chat
```

com:

```
POST /chat → função chat()
```

Agora estamos chegando à função:

```
chat()
```

Mas antes de chamar a função existe uma etapa muito importante.

---

# 11. FastAPI/Pydantic cria o `ChatRequest`

A função espera:

```
request: ChatRequest
```

E `ChatRequest` é:

```
class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None
```

&#x20; app

O FastAPI pega o JSON e pede ao Pydantic para validá-lo.

Temos:

```
{
  "message": "Quanto é 2 + 2?",
  "session_id": "sessao-123"
}
```

Está correto.

Então **agora nasce uma instância real de `ChatRequest`**:

```
ChatRequest(
    message="Quanto é 2 + 2?",
    session_id="sessao-123"
)
```

Esse detalhe é importante para aquela nossa distinção:

Antes:

```
class ChatRequest(...)
```

só existia a **classe**.

Agora, com uma requisição real:

```
ChatRequest(...)
```

nasceu um **objeto daquela classe**.

---

# 12. Agora `chat()` realmente executa

Finalmente:

```
async def chat(request: ChatRequest) -> ChatResponse:
```

é chamada.

`request` aponta para aquele objeto:

```
request
   ↓
ChatRequest
   ├── message = "Quanto é 2 + 2?"
   └── session_id = "sessao-123"
```

---

# 13. Incrementa contador

Primeiro:

```
global _request_count
```

significa que a função usará a variável global:

```
_request_count
```

Depois:

```
with _request_count_lock:
    _request_count += 1
```

Supondo que fosse:

```
_request_count = 15
```

ela pega o lock:

```
LOCK adquirido
```

faz:

```
15 → 16
```

e libera o lock.

Então:

```
_request_count = 16
```

&#x20; app

---

# 14. Registra log e inicia cronômetro

Depois:

```
logger.info(
    "chat iniciado: session_id=%s",
    request.session_id
)
```

Produz conceitualmente algo como:

```
chat iniciado: session_id=sessao-123
```

Depois:

```
t0 = time.perf_counter()
```

guarda o instante inicial da execução daquele chat.

---

# 15. Nasce `initial_state`

Aqui começamos a encostar no agente.

A rota faz:

```
initial_state = {
    "messages": [
        HumanMessage(content=request.message)
    ],
}
```

&#x20; app

Primeiro nasce:

```
HumanMessage(
    content="Quanto é 2 + 2?"
)
```

Depois esse objeto entra numa lista:

```
[    HumanMessage(...)]
```

Depois nasce o dicionário:

```
initial_state = {
    "messages": [
        HumanMessage(content="Quanto é 2 + 2?")
    ]
}
```

Então transformamos:

```
ChatRequest
message = "Quanto é 2 + 2?"
```

em:

```
estado que o LangGraph entende

{
   "messages": [
       HumanMessage(...)
   ]
}
```

---

# 16. A fronteira com o agente

A linha é:

```
result = await graph.ainvoke(initial_state)
```

&#x20; app

Aqui podemos colocar uma placa:

```
══════════════════════════════════
       FIM DA CAMADA API

       INÍCIO DO AGENTE
══════════════════════════════════
```

A rota fala:

> "`graph`, execute utilizando este estado inicial."

---

# 17. O objeto `graph` recebe a chamada

Lembra que `graph` é uma instância de:

```
AgentGraph
```

Então é chamado:

```
AgentGraph.ainvoke(...)
```

O método real é:

```
async def ainvoke(self, state):
    await self.compile()
    callbacks = [azure_tracer] if azure_tracer else []
    return await self._compiled.ainvoke(
        state,
        config={"callbacks": callbacks},
    )
```

&#x20; graph

Primeiro:

```
await self.compile()
```

No cenário normal, como o startup já executou:

```
await graph.compile()
```

temos:

```
self._compiled != None
```

Logo `compile()` verifica e praticamente não reconstrói nada.

É uma proteção extra.

Depois monta:

```
callbacks = [azure_tracer]
```

se o tracer existir, ou:

```
callbacks = []
```

caso contrário.

Finalmente:

```
self._compiled.ainvoke(...)
```

é chamado.

**Aqui efetivamente estamos dentro do grafo compilado.**

Podemos parar a caixa-preta do agente aí por enquanto:

```
initial_state
     ↓
AgentGraph.ainvoke()
     ↓
grafo compilado
     ↓
[ lógica do agente ]
     ↓
result
```

---

# 18. O agente devolve `result`

Imagine que o resultado volte aproximadamente assim:

```
result = {
    "messages": [
        HumanMessage(content="Quanto é 2 + 2?"),
        AIMessage(content="2 + 2 é igual a 4.")
    ]
}
```

Não estou dizendo que esse é necessariamente o objeto exato produzido em todos os casos; estou usando a estrutura compatível com o que o `app.py` espera.

A rota faz:

```
messages = result.get("messages", [])
```

Então:

```
messages
   ↓
lista de mensagens produzidas durante a execução
```

---

# 19. Pega a última mensagem

Depois:

```
raw_content = messages[-1].content if messages else ""
```

Se houver mensagens, pega:

```
messages[-1]
```

que significa:

> último item da lista.

Então, no nosso exemplo:

```
última mensagem
      ↓
AIMessage
      ↓
.content
      ↓
"2 + 2 é igual a 4."
```

---

# 20. Converte a resposta para texto

O código aceita duas possibilidades.

Se:

```
raw_content
```

for lista, ele percorre os blocos e junta os textos.

Caso contrário:

```
reply = str(raw_content)
```

No nosso caso simples:

```
reply = "2 + 2 é igual a 4."
```

---

# 21. Conta quantas tools foram utilizadas

Depois:

```
tool_calls_made = sum(
    1 for m in messages
    if isinstance(m, ToolMessage)
)
```

&#x20; app

No nosso exemplo, suponha que o agente respondeu diretamente, sem chamar nenhuma tool.

Então:

```
ToolMessage encontrados = 0
```

Logo:

```
tool_calls_made = 0
```

Se tivesse usado duas tools e houvesse dois `ToolMessage`, seria:

```
tool_calls_made = 2
```

---

# 22. Calcula duração

Agora:

```
elapsed_ms = (time.perf_counter() - t0) * 1000
```

Por exemplo:

```
t0        = início
agora     = fim
diferença = 1,35 segundo

elapsed_ms = 1350
```

Então registra:

```
chat concluído:
session_id=sessao-123
tool_calls=0
elapsed_ms=1350
```

---

# 23. Nasce `ChatResponse`

A rota retorna:

```
return ChatResponse(
    reply=reply,
    session_id=request.session_id,
    tool_calls_made=tool_calls_made,
)
```

&#x20; app

**Agora nasce uma instância de `ChatResponse`:**

```
ChatResponse(
    reply="2 + 2 é igual a 4.",
    session_id="sessao-123",
    tool_calls_made=0
)
```

FastAPI/Pydantic transforma isso numa resposta JSON equivalente a:

```
{
  "reply": "2 + 2 é igual a 4.",
  "session_id": "sessao-123",
  "tool_calls_made": 0
}
```

---

# 24. Só que a resposta ainda não chegou ao cliente

Lembra desta linha no middleware?

```
response = await call_next(request)
```

O middleware estava esperando.

Agora o:

```
await call_next(request)
```

terminou.

E `response` recebe a resposta criada pela aplicação.

Então voltamos fisicamente para dentro de:

```
_guard_chat()
```

Fluxo:

```
middleware
    │
    ├──────── call_next ────────→ chat()
    │                              │
    │                              ▼
    │                            agente
    │                              │
    │                              ▼
    │                         ChatResponse
    │                              │
    ◀──────────────────────────────┘
    
response = ...
```

---

# 25. Middleware verifica a resposta

Ele olha:

```
if response.status_code == 200
```

No caminho feliz:

```
200 ✅
```

E verifica:

```
"application/json" in response.headers["content-type"]
```

Também:

```
JSON ✅
```

Então ele lê o corpo da resposta.

&#x20; guardrails_middleware

---

# 26. Extrai `reply`

Ele transforma o JSON novamente em objeto Python:

```
payload = json.loads(raw)
```

Teremos algo semelhante a:

```
payload = {
    "reply": "2 + 2 é igual a 4.",
    "session_id": "sessao-123",
    "tool_calls_made": 0
}
```

Depois:

```
reply = payload.get("reply", "")
```

Então:

```
reply = "2 + 2 é igual a 4."
```

---

# 27. Verifica blocklist de saída

```
matched_out = check_output_blocklist(reply)
```

No caminho feliz:

```
nenhuma expressão proibida
```

Logo:

```
if matched_out:
```

é falso.

Continua.

---

# 28. Verifica PII na saída

Se estiver habilitado:

```
_REDACT_PII_OUTPUT
```

ele executa:

```
redacted = redact_pii(reply)
```

Nossa resposta:

```
2 + 2 é igual a 4.
```

não contém informação pessoal.

Então:

```
redacted == reply
```

Nada é alterado.

&#x20; guardrails_middleware

---

# 29. Middleware reconstrói a resposta HTTP

Depois:

```
raw = json.dumps(payload).encode()
```

Ou seja:

```
dict Python
   ↓
JSON
   ↓
bytes
```

Ele atualiza:

```
headers["content-length"]
```

e cria:

```
Response(
    content=raw,
    status_code=200,
    ...
)
```

&#x20; guardrails_middleware

Essa é a resposta final que sai do middleware.

---

# 30. Finaliza métricas e tracing do middleware

Antes de sair completamente, entra o:

```
finally:
```

e executa:

```
elapsed_ms = ...
_guardrail_latency.record(...)
span.set_attribute(...)
```

&#x20; guardrails_middleware

Então fica registrado:

```
quanto tempo toda a passagem pelo middleware levou
```

Isso inclui o período em que ele ficou aguardando:

```
await call_next(request)
```

e, portanto, inclui o tempo gasto no restante da aplicação durante essa chamada.

---

# 31. Resposta volta para o Uvicorn

O fluxo agora está terminando:

```
GuardrailsMiddleware
        ↓
FastAPI / Starlette
        ↓
Uvicorn
```

O Uvicorn transforma aquela resposta ASGI em HTTP e envia pela rede.

---

# 32. Cliente recebe

Finalmente:

```
HTTP/1.1 200 OK
Content-Type: application/json
```

com algo semelhante a:

```
{
  "reply": "2 + 2 é igual a 4.",
  "session_id": "sessao-123",
  "tool_calls_made": 0
}
```

---

# O fluxo inteiro em uma única imagem mental

```
┌──────────────── CLIENTE ────────────────┐
│                                         │
│ POST /chat                              │
│ {                                       │
│   message: "Quanto é 2 + 2?",           │
│   session_id: "sessao-123"              │
│ }                                       │
└───────────────────┬─────────────────────┘
                    │
                    ▼
                UVICORN
                    │
                    ▼
             app = FastAPI(...)
                    │
                    ▼
      GuardrailsMiddleware.dispatch()
                    │
                    ▼
             _guard_chat()
                    │
             inicia métricas
             inicia tracing
             lê body
                    │
                    ▼
             extrai message
                    │
          ┌─────────┴─────────┐
          │ tamanho OK        │
          │ injection OK      │
          │ PII OK            │
          │ externo OK        │
          └─────────┬─────────┘
                    │
                    ▼
        await call_next(request)
                    │
                    ▼
               FastAPI
                    │
          procura POST /chat
                    │
                    ▼
        Pydantic valida o JSON
                    │
                    ▼
         NASCE ChatRequest
                    │
                    ▼
                chat()
                    │
         _request_count += 1
                    │
              inicia timer
                    │
                    ▼
       NASCE HumanMessage(...)
                    │
                    ▼
       NASCE initial_state
                    │
                    ▼
      graph.ainvoke(initial_state)
                    │
          ═════════════════
             AGENTE
          ═════════════════
                    │
                    ▼
                 result
                    │
                    ▼
        pega result["messages"]
                    │
                    ▼
        pega última mensagem
                    │
                    ▼
             monta reply
                    │
                    ▼
        conta ToolMessage(s)
                    │
                    ▼
          NASCE ChatResponse
                    │
                    ▼
          FastAPI gera resposta
                    │
                    ▼
        call_next() TERMINA
                    │
                    ▼
       middleware recebe response
                    │
            status 200?
                 SIM
                    │
               é JSON?
                 SIM
                    │
                    ▼
            extrai "reply"
                    │
                    ▼
           blocklist saída
                 OK
                    │
                    ▼
             PII saída
                 OK
                    │
                    ▼
        reconstrói Response
                    │
        registra latência
        finaliza span
                    │
                    ▼
                 UVICORN
                    │
                    ▼
┌──────────────── CLIENTE ────────────────┐
│                                         │
│ HTTP 200                                │
│                                         │
│ {                                       │
│   reply: "2 + 2 é igual a 4.",          │
│   session_id: "sessao-123",             │
│   tool_calls_made: 0                    │
│ }                                       │
└─────────────────────────────────────────┘
```

A **fronteira exata para o próximo estudo** é esta:

```
result = await graph.ainvoke(initial_state)
```

Até essa linha, nós já conseguimos explicar praticamente todo o caminho da **API**. A partir dela, começamos efetivamente a abrir a caixa do **agente/LangGraph**.