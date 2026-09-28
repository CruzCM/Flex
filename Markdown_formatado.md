# 1. Visão geral, do começo até o app ficar montado

```
┌──────────────────────────────────────────────────────────────────────────────┐
│  FASE 0 — FORA DO PYTHON                                                    │
├──────────────────────────────────────────────────────────────────────────────┤
│  GitHub / build / imagem / deployment / pod / container                     │
│                                                                              │
│  O container já sobe com o projeto dentro dele.                             │
│  Então, dentro do container, alguém executa:                                │
│                                                                              │
│      python -m iaa_agent_mf_assist_financeir                                │
└──────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│  FASE 1 — __main__.py                                                       │
├──────────────────────────────────────────────────────────────────────────────┤
│  __main__.py é executado                                                    │
│                                                                              │
│  main() é CHAMADA                                                           │
│                                                                              │
│  Dentro de main():                                                          │
│    ├─ host = "0.0.0.0"                                                      │
│    ├─ port = 8080                                                           │
│    ├─ workers = 1                                                           │
│    ├─ log_level = "info"                                                    │
│    └─ uvicorn.run("iaa_agent_mf_assist_financeir.app:app", ...)             │
│                                                                              │
│  Aqui nasce / começa:                                                       │
│    └─ processo Uvicorn / servidor HTTP                                      │
└──────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│  FASE 2 — Uvicorn precisa do objeto "app"                                   │
├──────────────────────────────────────────────────────────────────────────────┤
│  Uvicorn lê:                                                                 │
│                                                                              │
│      "iaa_agent_mf_assist_financeir.app:app"                                │
│                                                                              │
│  Então ele:                                                                  │
│    1. importa o módulo app.py                                                │
│    2. executa app.py de cima para baixo                                      │
│    3. procura a variável global chamada "app"                                │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

# 2. O que realmente nasce durante a carga de `app.py`

Agora vamos entrar no que **de fato nasce** durante a execução do módulo.

---

## FASE 2A — `app.py` dispara o `graph.py` e outras peças

```
┌──────────────────────────────────────────────────────────────────────────────┐
│  app.py começa a ser executado                                              │
├──────────────────────────────────────────────────────────────────────────────┤
│  Importações ocorrem                                                        │
│                                                                              │
│  IMPORTANTE:                                                                 │
│  Importar um módulo pode executar o código global daquele módulo.           │
└──────────────────────────────────────────────────────────────────────────────┘
```

### Ordem crítica dentro do `app.py`

```
from iaa_agent_mf_assist_financeir.config import get_config
from iaa_agent_mf_assist_financeir.graph import graph
from iaa_agent_mf_assist_financeir.utils.guardrails_middleware import GuardrailsMiddleware
from iaa_agent_mf_assist_financeir.utils.tracing import configure_azure_monitor
```

A ordem real de “nascimento” fica assim:

---

## 2A.1 — `config.py`

```
┌──────────────────────────────────────────────────────────────────────────────┐
│  IMPORT: from ...config import get_config                                   │
├──────────────────────────────────────────────────────────────────────────────┤
│  config.py é carregado                                                       │
│                                                                              │
│  NASCEM valores globais do módulo:                                           │
│    ├─ _config = None                                                         │
│    └─ _config_lock = threading.Lock()   ← AQUI nasce o lock                 │
│                                                                              │
│  Classes dataclass são definidas, mas NÃO "nascem" objetos ainda.            │
│  get_config() e load_agent_config() são definidas, mas NÃO executam ainda.   │
└──────────────────────────────────────────────────────────────────────────────┘
```

### Aqui já nasceram:

- `_config` com valor `None`
- `_config_lock` como um objeto `threading.Lock`

### Ainda não nasceram:

- nenhum `AgentConfig`
- nenhuma configuração lida do YAML

---

## 2A.2 — `graph.py`

Agora o `app.py` faz:

```
from iaa_agent_mf_assist_financeir.graph import graph
```

Aí o `graph.py` é executado.

```
┌──────────────────────────────────────────────────────────────────────────────┐
│  IMPORT: from ...graph import graph                                         │
├──────────────────────────────────────────────────────────────────────────────┤
│  graph.py começa                                                             │
│                                                                              │
│  1) EXECUTA: config = get_config()                                           │
│                                                                              │
│     get_config() verifica _config                                            │
│       ├─ se _config is None                                                  │
│       │    ├─ entra no with _config_lock                                     │
│       │    ├─ chama load_agent_config()                                      │
│       │    ├─ lê agent_config.yaml                                           │
│       │    ├─ monta AgentConfig(...)                                         │
│       │    └─ guarda em _config                                              │
│       └─ retorna _config                                                     │
│                                                                              │
│  2) NASCE no graph.py:                                                       │
│       config = <AgentConfig>                                                 │
│                                                                              │
│  3) NASCEM os validators:                                                    │
│       _context_precision_validator = ContextPrecisionValidator()             │
│       _tool_correctness_validator = ToolCorrectnessValidator()               │
│       _toxicity_validator = ToxicityValidator()                             │
│       _non_advice_validator = NonAdviceValidator()                          │
│       _pii_validator = PIIValidator()                                       │
│                                                                              │
│  4) NASCEM valores de observabilidade do módulo:                             │
│       _appinsights_conn_str = os.environ.get(...)                           │
│       _agent_name = config.agent_name ou "dia-agent"                        │
│                                                                              │
│  5) PODE nascer azure_tracer:                                                │
│       ├─ se _appinsights_conn_str existir                                    │
│       │     azure_tracer = AzureAIOpenTelemetryTracer(...)                   │
│       └─ senão                                                               │
│             azure_tracer = None                                              │
│                                                                              │
│  6) NASCE logger do graph.py:                                                │
│       logger = logging.getLogger(__name__)                                   │
│                                                                              │
│  7) class AgentGraph, AgentFactory etc são definidas                         │
│     (ainda sem instância)                                                    │
│                                                                              │
│  8) NASCE o objeto global mais importante do módulo:                         │
│       graph = AgentGraph()                                                   │
│                                                                              │
│       Dentro de AgentGraph.__init__():                                       │
│         ├─ self._compiled = None                                             │
│         └─ self._lock = asyncio.Lock()                                       │
└──────────────────────────────────────────────────────────────────────────────┘
```

### Resultado concreto do `graph.py`

No fim do import, o que existe é:

```
graph
└── AgentGraph
    ├── _compiled = None
    └── _lock = <asyncio.Lock>
```

**Muito importante:**

> o `graph` já nasceu,\
> **mas o agente/grafo compilado ainda não nasceu**.

Ou seja:

```
graph existe                  ✅
graph._compiled já pronto     ❌
```

---

## 2A.3 — `guardrails_middleware.py`

Depois o `app.py` importa:

```
from iaa_agent_mf_assist_financeir.utils.guardrails_middleware import GuardrailsMiddleware
```

Aí esse módulo executa seu código global.

```
┌──────────────────────────────────────────────────────────────────────────────┐
│  IMPORT: GuardrailsMiddleware                                               │
├──────────────────────────────────────────────────────────────────────────────┤
│  guardrails_middleware.py é executado                                        │
│                                                                              │
│  NASCEM objetos globais do módulo:                                           │
│    ├─ logger = logging.getLogger(__name__)                                   │
│    ├─ _tracer = trace.get_tracer("agent.guardrails")                         │
│    ├─ _meter = metrics.get_meter("agent.guardrails")                         │
│    ├─ _guardrail_requests = _meter.create_counter(...)                       │
│    ├─ _guardrail_blocks = _meter.create_counter(...)                         │
│    ├─ _guardrail_redactions = _meter.create_counter(...)                     │
│    └─ _guardrail_latency = _meter.create_histogram(...)                      │
│                                                                              │
│  NASCEM configurações globais vindas de env var:                             │
│    ├─ _MAX_INPUT_LEN                                                         │
│    ├─ _BLOCK_PII_INPUT                                                       │
│    ├─ _REDACT_PII_OUTPUT                                                     │
│    ├─ _SERVICE_NAME                                                          │
│    └─ _DEPLOY_ENV                                                            │
│                                                                              │
│  A classe GuardrailsMiddleware é definida                                    │
│  (mas nenhum middleware ainda foi adicionado ao app)                         │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## 2A.4 — `tracing.py`

Depois o `app.py` importa:

```
from iaa_agent_mf_assist_financeir.utils.tracing import configure_azure_monitor
```

```
┌──────────────────────────────────────────────────────────────────────────────┐
│  IMPORT: configure_azure_monitor                                            │
├──────────────────────────────────────────────────────────────────────────────┤
│  tracing.py é executado                                                      │
│                                                                              │
│  NASCEM objetos/valores globais do módulo:                                   │
│    ├─ logger = logging.getLogger(__name__)                                   │
│    └─ _APPINSIGHTS_CS = os.getenv("APPLICATION_INSIGHTS_CONNECTION_STRING")  │
│                                                                              │
│  configure_azure_monitor(), get_tracer(), get_meter() são definidas          │
│  mas ainda NÃO executam.                                                     │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

# 3. Agora sim: execução direta do `app.py`

Terminados os imports, o Python continua no próprio `app.py`.

---

## 3.1 — Nasce o logger do `app.py`

```
logger = logging.getLogger(__name__)
```

```
┌──────────────────────────────────────────────────────────────────────────────┐
│  app.py                                                                      │
├──────────────────────────────────────────────────────────────────────────────┤
│  NASCE:                                                                      │
│    logger = logging.getLogger(__name__)                                      │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## 3.2 — Nasce `config` dentro do `app.py`

```
config = get_config()
```

```
┌──────────────────────────────────────────────────────────────────────────────┐
│  app.py                                                                      │
├──────────────────────────────────────────────────────────────────────────────┤
│  EXECUTA: get_config()                                                       │
│                                                                              │
│  Como _config provavelmente já foi montado pelo graph.py:                    │
│    ├─ get_config() vê que _config já existe                                  │
│    └─ retorna o mesmo AgentConfig                                            │
│                                                                              │
│  NASCE no app.py:                                                            │
│    config = <AgentConfig>                                                    │
└──────────────────────────────────────────────────────────────────────────────┘
```

Agora o `app.py` tem:

```
config
└── AgentConfig
    ├── agent_id
    ├── agent_name
    ├── deployment
    ├── instructions
    ├── agent_description
    ├── temperature
    ├── top_p
    ├── mcp = MCPConfig(...)
    ├── metadata = Metadata(...)
    ├── llm = LLMConfig(...)
    ├── guardrails = GuardrailsConfig(...)
    └── rag = RAGConfig(...)
```

---

## 3.3 — Executa `configure_azure_monitor()`

```
configure_azure_monitor()
```

```
┌──────────────────────────────────────────────────────────────────────────────┐
│  app.py                                                                      │
├──────────────────────────────────────────────────────────────────────────────┤
│  EXECUTA: configure_azure_monitor()                                          │
│                                                                              │
│  Dentro da função:                                                           │
│    ├─ se _APPINSIGHTS_CS estiver vazio                                       │
│    │     ├─ logger.info(...)                                                 │
│    │     └─ return                                                           │
│    │                                                                          │
│    └─ se _APPINSIGHTS_CS existir                                             │
│          ├─ tracer_provider = trace.get_tracer_provider()                    │
│          ├─ az_trace_exporter = AzureMonitorTraceExporter(...)               │
│          ├─ batch_processor = BatchSpanProcessor(az_trace_exporter)          │
│          └─ tracer_provider.add_span_processor(batch_processor)              │
│                                                                              │
│  O efeito é:                                                                  │
│    "o OpenTelemetry da aplicação passa a ter caminho para exportar            │
│     traces para Azure Monitor / Application Insights"                        │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

# 4. Definição do `lifespan` e nascimento do `app`

## 4.1 — `lifespan` é definido

```
@asynccontextmanager
async def lifespan(app_instance: FastAPI):
    await graph.compile()
    yield
```

Aqui **a função é definida**, mas ainda **não executa**.

Então:

```
lifespan existe como função          ✅
graph.compile() já executou          ❌
```

---

## 4.2 — Agora nasce o objeto principal da API

```
app = FastAPI(
    title=config.agent_name,
    description=config.agent_description,
    version=config.metadata.version or "0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)
```

```
┌──────────────────────────────────────────────────────────────────────────────┐
│  app.py                                                                      │
├──────────────────────────────────────────────────────────────────────────────┤
│  NASCE o objeto principal da aplicação:                                      │
│                                                                              │
│      app = FastAPI(...)                                                      │
│                                                                              │
│  app nasce com estas configurações iniciais:                                 │
│    ├─ title = config.agent_name                                              │
│    ├─ description = config.agent_description                                 │
│    ├─ version = config.metadata.version ou "0.1.0"                           │
│    ├─ docs_url = "/docs"                                                     │
│    ├─ redoc_url = "/redoc"                                                   │
│    └─ lifespan = lifespan                                                    │
│                                                                              │
│  IMPORTANTE:                                                                 │
│    ├─ o objeto app já existe                                                 │
│    ├─ mas o lifespan ainda não rodou                                         │
│    ├─ o graph ainda não foi compilado por aqui                               │
│    └─ as rotas ainda não foram registradas abaixo                            │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

# 5. Estado global do `app.py` logo depois do `app = FastAPI(...)`

## 5.1 — Nasce `_START_TIME`

```
_START_TIME = time.time()
```

```
_START_TIME = instante em que esse trecho do módulo foi executado
```

Serve para depois calcular uptime.

---

## 5.2 — Nasce `_request_count`

```
_request_count: int = 0
```

Contador inicial de chamadas.

---

## 5.3 — Nasce `_request_count_lock`

```
_request_count_lock = threading.Lock()
```

Lock para proteger incremento do contador.

---

## 5.4 — Middleware é acoplado ao app

```
app.add_middleware(GuardrailsMiddleware)
```

```
┌──────────────────────────────────────────────────────────────────────────────┐
│  app.py                                                                      │
├──────────────────────────────────────────────────────────────────────────────┤
│  EXECUTA: app.add_middleware(GuardrailsMiddleware)                           │
│                                                                              │
│  Efeito:                                                                     │
│    o objeto app passa a ter o middleware GuardrailsMiddleware                │
│    no pipeline de requisições                                                │
│                                                                              │
│  Ainda não significa que uma requisição foi interceptada.                    │
│  Significa apenas que o app ficou configurado para usar esse middleware.     │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

# 6. O que ainda é só definição (não “nascimento” de objeto)

Depois disso aparecem classes Pydantic e funções de rota.

Essas partes são **definidas**, não executadas ainda.

## Classes Pydantic definidas

```
class ChatRequest(BaseModel): ...
class ChatResponse(BaseModel): ...
class MetricsResponse(BaseModel): ...
```

Nesse momento:

- a classe existe
- **mas nenhum `ChatRequest` ainda foi instanciado**

## Rotas definidas

```
@app.post("/chat", response_model=ChatResponse)
async def chat(...): ...

@app.get("/metrics", response_model=MetricsResponse)
async def metrics(): ...

@app.get("/health/live")
async def live(): ...

@app.get("/health/ready")
async def ready(): ...
```

O efeito do decorator aqui é:

```
a função é registrada no app como rota
```

Então, durante a carga do módulo:

```
app ganha a rota POST /chat
app ganha a rota GET /metrics
app ganha a rota GET /health/live
app ganha a rota GET /health/ready
```

Mas:

```
chat() ainda não executou
metrics() ainda não executou
live() ainda não executou
ready() ainda não executou
```

---

# 7. Foto final da aplicação montada (antes do startup real)

Quando o `app.py` termina de ser executado, temos isso:

```
┌──────────────────────────────────────────────────────────────────────────────┐
│  ESTADO FINAL DO MÓDULO app.py APÓS CARREGAMENTO                            │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  logger                      = logging.getLogger(...)                        │
│  config                      = AgentConfig(...)                              │
│  _START_TIME                 = <timestamp>                                   │
│  _request_count              = 0                                             │
│  _request_count_lock         = <threading.Lock>                              │
│                                                                              │
│  graph                       = AgentGraph(...)                               │
│    ├─ _compiled              = None                                          │
│    └─ _lock                  = <asyncio.Lock>                                │
│                                                                              │
│  app                         = FastAPI(...)                                  │
│    ├─ title                  = config.agent_name                             │
│    ├─ description            = config.agent_description                      │
│    ├─ version                = config.metadata.version                       │
│    ├─ docs_url               = "/docs"                                       │
│    ├─ redoc_url              = "/redoc"                                      │
│    ├─ lifespan               = lifespan                                      │
│    ├─ middleware             = [GuardrailsMiddleware]                        │
│    └─ rotas registradas:                                                     │
│         ├─ POST /chat                                                       │
│         ├─ GET /metrics                                                     │
│         ├─ GET /health/live                                                 │
│         └─ GET /health/ready                                                │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

# 8. Próximo nascimento importante: startup real do FastAPI

Depois que o `app.py` termina, o Uvicorn já conseguiu o objeto `app`.

Aí começa o startup real da aplicação.

```
┌──────────────────────────────────────────────────────────────────────────────┐
│  STARTUP REAL                                                                │
├──────────────────────────────────────────────────────────────────────────────┤
│  Uvicorn já tem o objeto app                                                 │
│  FastAPI inicia                                                              │
│  FastAPI executa o lifespan                                                  │
│                                                                              │
│      await graph.compile()                                                   │
│                                                                              │
│  AQUI acontece o próximo nascimento importante:                              │
│                                                                              │
│      graph._compiled deixa de ser None                                       │
│                                                                              │
│  Ou seja:                                                                    │
│    nasce o grafo compilado / pronto para uso                                 │
│                                                                              │
│  Depois:                                                                     │
│      yield                                                                   │
│                                                                              │
│  A aplicação é considerada pronta para receber requisições.                  │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

# 9. Fluxo de uma requisição `/chat` já com tudo montado

Agora sim, depois de startup concluído:

```
┌──────────────────────────────────────────────────────────────────────────────┐
│  REQUISIÇÃO POST /chat                                                      │
├──────────────────────────────────────────────────────────────────────────────┤
│  Cliente                                                                     │
│    ↓                                                                         │
│  Uvicorn                                                                     │
│    ↓                                                                         │
│  app (FastAPI)                                                               │
│    ↓                                                                         │
│  GuardrailsMiddleware.dispatch(request, call_next)                           │
│    │                                                                         │
│    ├─ se não for POST /chat                                                  │
│    │     └─ call_next(request)                                               │
│    │                                                                         │
│    └─ se for POST /chat                                                      │
│          ├─ lê body                                                          │
│          ├─ extrai message                                                   │
│          ├─ valida tamanho                                                   │
│          ├─ valida injection                                                 │
│          ├─ valida PII de entrada                                            │
│          ├─ valida guardrail externo                                         │
│          │                                                                   │
│          ├─ se falhar                                                        │
│          │     └─ retorna HTTP 400                                           │
│          │                                                                   │
│          └─ se passar                                                        │
│                └─ response = await call_next(request)                        │
│                              │                                               │
│                              ▼                                               │
│                        rota POST /chat                                       │
│                        função: chat(request: ChatRequest)                    │
│                              │                                               │
│                              ├─ with _request_count_lock                     │
│                              │    └─ _request_count += 1                     │
│                              │                                               │
│                              ├─ t0 = time.perf_counter()                     │
│                              ├─ initial_state = {                            │
│                              │      "messages": [HumanMessage(...)]          │
│                              │  }                                            │
│                              ├─ result = await graph.ainvoke(...)            │
│                              ├─ extrai messages                              │
│                              ├─ conta ToolMessage                            │
│                              ├─ mede elapsed_ms                              │
│                              └─ retorna ChatResponse(...)                    │
│                                                                              │
│  resposta volta ao middleware                                                │
│    ├─ se status != 200 ou não JSON                                           │
│    │     └─ devolve como veio                                                │
│    └─ senão                                                                  │
│          ├─ pega payload["reply"]                                            │
│          ├─ check_output_blocklist(reply)                                    │
│          ├─ talvez substitui resposta                                        │
│          ├─ talvez redact_pii(reply)                                         │
│          └─ devolve resposta final                                           │
│                                                                              │
│  Cliente recebe                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

# 10. Resumo em linguagem muito simples

Se eu resumisse tudo numa visão “leiga, mas correta”, seria assim:

```
1. O container sobe com o projeto dentro.

2. O Python executa __main__.py.

3. O __main__.py chama uvicorn.run(...).

4. O Uvicorn carrega app.py.

5. Durante esse carregamento:
   - a configuração YAML é lida e vira AgentConfig
   - nasce o objeto graph = AgentGraph()
   - nascem os validators
   - nascem objetos de tracing/metrics
   - nasce o objeto app = FastAPI(...)
   - o middleware é acoplado
   - as rotas são registradas

6. Depois que o app está montado, o FastAPI executa o lifespan.

7. No lifespan:
   - graph.compile() roda
   - nasce o grafo compilado/pronto

8. A aplicação fica pronta.

9. Quando chega um POST /chat:
   - o middleware verifica entrada
   - se passar, chama a rota /chat
   - a rota /chat chama o graph
   - a resposta volta
   - o middleware ainda pode ajustar a saída
   - a resposta final é enviada ao cliente
```

---

Se você quiser, no próximo passo eu posso fazer uma **versão 2 desse diagrama**, ainda mais visual, em formato de:

1. **árvore hierárquica**
2. **linha do tempo**
3. **“quem chama quem”**
4. **“o que nasce em cada arquivo”**

Eu acho que a próxima melhor seria justamente essa: **“quem chama quem” + “o que nasce em cada momento”**.