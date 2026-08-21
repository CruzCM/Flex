# BBMAGIC 3.1.7

## 0) VERSÃO DO BBMAGIC

bbmagic versão: 3.1.7

## 1. MÓDULOS DISPONÍVEIS

Total de módulos descobertos: 26

- bbmagic.checks
- bbmagic.cluster
- bbmagic.common
- bbmagic.db2
- bbmagic.environment
- bbmagic.exceptions
- bbmagic.file_config
- bbmagic.gitlab_config
- bbmagic.hdfs
- bbmagic.http_config
- bbmagic.kinit
- bbmagic.livyapi
- bbmagic.log
- bbmagic.lookup
- bbmagic.publicador_modelo
- bbmagic.sas
- bbmagic.sas.authinfo
- bbmagic.sas.sas
- bbmagic.sas.sascfg
- bbmagic.sigla_api
- bbmagic.spark
- bbmagic.sumary
- bbmagic.teams_notify
- bbmagic.utils
- bbmagic.utils.format_python_version
- bbmagic.version

## 2) OBJETOS PÚBLICOS EXPOSTOS NA RAIZ (import bbmagic)

Total exposto na raiz: 37

- AuthInfo
- AuthKey
- Cluster
- Db2
- FileConfig
- GitLabConfig
- Hdfs
- HttpConfig
- Kinit
- MetaDataHive
- SAS
- Spark
- TeamsNotify
- checks
- cluster
- common
- db2
- environment
- exceptions
- file_config
- get_ambiente
- gitlab_config
- hdfs
- http_config
- kinit
- livyapi
- log
- log_project
- lookup
- sas
- sigla_api
- spark
- sumary
- suppress
- teams_notify
- utils
- version

## 3) INVENTÁRIO COMPLETO POR MÓDULO

### Resumo (qtd por categoria) por módulo

| Módulo | classes | funcoes | const | erros |
|---|---:|---:|---:|---:|
| bbmagic.checks | 1 | 5 | 1 | 0 |
| bbmagic.cluster | 4 | 2 | 1 | 0 |
| bbmagic.common | 4 | 7 | 3 | 0 |
| bbmagic.db2 | 5 | 3 | 7 | 0 |
| bbmagic.environment | 1 | 0 | 0 | 0 |
| bbmagic.exceptions | 2 | 0 | 0 | 0 |
| bbmagic.file_config | 2 | 0 | 2 | 0 |
| bbmagic.gitlab_config | 4 | 1 | 3 | 0 |
| bbmagic.hdfs | 7 | 2 | 1 | 0 |
| bbmagic.http_config | 4 | 0 | 3 | 0 |
| bbmagic.kinit | 3 | 0 | 3 | 0 |
| bbmagic.livyapi | 7 | 2 | 1 | 0 |
| bbmagic.log | 1 | 2 | 0 | 0 |
| bbmagic.lookup | 3 | 1 | 1 | 0 |
| bbmagic.publicador_modelo | 0 | 0 | 0 | 1 |
| bbmagic.sas | 4 | 0 | 0 | 0 |
| bbmagic.sas.authinfo | 3 | 0 | 1 | 0 |
| bbmagic.sas.sas | 7 | 1 | 6 | 0 |
| bbmagic.sas.sascfg | 0 | 0 | 3 | 0 |
| bbmagic.sigla_api | 1 | 0 | 0 | 0 |
| bbmagic.spark | 17 | 11 | 8 | 0 |
| bbmagic.sumary | 2 | 3 | 2 | 0 |
| bbmagic.teams_notify | 6 | 0 | 0 | 0 |
| bbmagic.utils | 0 | 1 | 0 | 0 |
| bbmagic.utils.format_python_version | 0 | 1 | 0 | 0 |
| bbmagic.version | 0 | 0 | 0 | 0 |

### Detalhe completo do inventário (JSON)

#### bbmagic.checks

##### classes

````json
[ { "nome": "BoasPraticasWarning", "assinatura": null } ]
````

##### funcoes

````json
[ { "nome": "check_configure_venv", "assinatura": "(info)" }, { "nome": "check_pre_run_cell", "assinatura": "(info)" }, { "nome": "check_saveastable", "assinatura": "(info)" }, { "nome": "get_ipython", "assinatura": "()" }, { "nome": "register_checks", "assinatura": "(checks: dict) -> None" } ]
````

##### constantes

````json
[ { "nome": "spark_checks", "tipo": "dict" } ]
````

##### submodulos

````json
[ "os", "sys", "warnings" ]
````

##### erros

````json
[]
````

#### bbmagic.cluster

##### classes

````json
[ { "nome": "Cluster", "assinatura": "(config: Optional[bbmagic.file_config.FileConfig] = None) -> None" }, { "nome": "FileConfig", "assinatura": "(path) -> None" }, { "nome": "HttpConfig", "assinatura": "(set_no_proxy: bool = True)" }, { "nome": "defaultdict", "assinatura": null } ]
````

##### funcoes

````json
[ { "nome": "get_cloud", "assinatura": "() -> str" }, { "nome": "get_environment", "assinatura": "() -> str" } ]
````

##### constantes

````json
[ { "nome": "Optional", "tipo": "_SpecialForm" } ]
````

##### submodulos

````json
[ "pd", "re" ]
````

##### erros

````json
[]
````

#### bbmagic.common

##### classes

````json
[ { "nome": "BoasPraticasWarning", "assinatura": null }, { "nome": "Path", "assinatura": "(*args, **kwargs)" }, { "nome": "TemporaryDirectory", "assinatura": "(suffix=None, prefix=None, dir=None)" }, { "nome": "VirtualEnvironment", "assinatura": "(path=None, python=None, cache=None, readonly=False, system_site_packages=False)" } ]
````

##### funcoes

````json
[ { "nome": "create_virtualenv", "assinatura": "(requirements: Union[Sequence[str], str, NoneType] = None, path: Optional[str] = None, create_zip: bool = False, zip_path: str = '.', zip_name: str = 'virtualenv') -> virtualenvapi.manage.VirtualEnvironment" }, { "nome": "get_ambiente", "assinatura": "() -> str" }, { "nome": "get_bbmagic_spark_cluster", "assinatura": "(default: Optional[str] = None) -> str" }, { "nome": "get_bbmagic_spark_version", "assinatura": "(default: Optional[int] = None) -> int" }, { "nome": "get_cloud", "assinatura": "() -> str" }, { "nome": "get_environment", "assinatura": "() -> str" }, { "nome": "get_project_id", "assinatura": "(raise_not_found: bool = False) -> Optional[str]" } ]
````

##### constantes

````json
[ { "nome": "Optional", "tipo": "_SpecialForm" }, { "nome": "Sequence", "tipo": "_SpecialGenericAlias" }, { "nome": "Union", "tipo": "_SpecialForm" } ]
````

##### submodulos

````json
[ "os", "shutil" ]
````

##### erros

````json
[]
````

#### bbmagic.db2

##### classes

````json
[ { "nome": "DB2Server", "assinatura": "(host, port, database)" }, { "nome": "DataFrame", "assinatura": "(data=None, index: 'Axes | None' = None, columns: 'Axes | None' = None, dtype: 'Dtype | None' = None, copy: 'bool | None' = None) -> 'None'" }, { "nome": "Db2", "assinatura": "(user: Optional[str] = None, password: Optional[str] = None, host: str = 'gwdb2.bb.com.br', port: int = 50100, database: str = 'BDB2P04', trust_env: bool = True, jars_path: Optional[str] = None, backoff_limit: int = 3600, pconnect: bool = True) -> None" }, { "nome": "HTML", "assinatura": "(data=None, url=None, filename=None, metadata=None)" }, { "nome": "Template", "assinatura": "(source: Union[str, jinja2.nodes.Template], block_start_string: str = '{%', block_end_string: str = '%}', variable_start_string: str = '{{', variable_end_string: str = '}}', comment_start_string: str = '{#', comment_end_string: str = '#}', line_statement_prefix: Optional[str] = None, line_comment_prefix: Optional[str] = None, trim_blocks: bool = False, lstrip_blocks: bool = False, newline_sequence: "te.Literal['\\n', '\\r\\n', '\\r']" = '\n', keep_trailing_newline: bool = False, extensions: Sequence[Union[str, Type[ForwardRef('Extension')]]] = (), optimized: bool = True, undefined: Type[jinja2.runtime.Undefined] = <class 'jinja2.runtime.Undefined'>, finalize: Optional[Callable[..., Any]] = None, autoescape: Union[bool, Callable[[Optional[str]], bool]] = False, enable_async: bool = False) -> Any" } ]
````

##### funcoes

````json
[ { "nome": "get_ambiente", "assinatura": "() -> str" }, { "nome": "get_project_id", "assinatura": "(raise_not_found: bool = False) -> Optional[str]" }, { "nome": "namedtuple", "assinatura": "(typename, field_names, *, rename=False, defaults=None, module=None)" } ]
````

##### constantes

````json
[ { "nome": "DB2_BACKOFF_LIMIT", "tipo": "int" }, { "nome": "Iterator", "tipo": "_SpecialGenericAlias" }, { "nome": "Optional", "tipo": "_SpecialForm" }, { "nome": "Union", "tipo": "_SpecialForm" }, { "nome": "db2_desenv", "tipo": "DB2Server" }, { "nome": "db2_homologa", "tipo": "DB2Server" }, { "nome": "db2_prod", "tipo": "DB2Server" } ]
````

##### submodulos

````json
[ "IPython", "getpass", "ibm_db", "ibm_db_dbi", "os", "pd", "requests" ]
````

##### erros

````json
[]
````

#### bbmagic.environment

##### classes

````json
[ { "nome": "Environment", "assinatura": "()" } ]
````

##### funcoes

````json
[]
````

##### constantes

````json
[]
````

##### submodulos

````json
[ "os" ]
````

##### erros

````json
[]
````

#### bbmagic.exceptions

##### classes

````json
[ { "nome": "KinitError", "assinatura": null }, { "nome": "PublicadorError", "assinatura": null } ]
````

##### funcoes

````json
[]
````

##### constantes

````json
[]
````

##### submodulos

````json
[]
````

##### erros

````json
[]
````

#### bbmagic.file_config

##### classes

````json
[ { "nome": "FileConfig", "assinatura": "(path) -> None" }, { "nome": "Path", "assinatura": "(*args, **kwargs)" } ]
````

##### funcoes

````json
[]
````

##### constantes

````json
[ { "nome": "BBMAGIC_VERSION", "tipo": "str" }, { "nome": "Optional", "tipo": "_SpecialForm" } ]
````

##### submodulos

````json
[ "configparser" ]
````

##### erros

````json
[]
````

#### bbmagic.gitlab_config

##### classes

````json
[ { "nome": "FileConfig", "assinatura": "(path) -> None" }, { "nome": "GitLabConfig", "assinatura": "()" }, { "nome": "Path", "assinatura": "(*args, **kwargs)" }, { "nome": "PathLike", "assinatura": "()" } ]
````

##### funcoes

````json
[ { "nome": "quote_plus", "assinatura": "(string, safe='', encoding=None, errors=None)" } ]
````

##### constantes

````json
[ { "nome": "BBMAGIC_VERSION", "tipo": "str" }, { "nome": "Optional", "tipo": "_SpecialForm" }, { "nome": "Union", "tipo": "_SpecialForm" } ]
````

##### submodulos

````json
[ "os", "requests", "ssl", "time", "urllib3" ]
````

##### erros

````json
[]
````

#### bbmagic.hdfs

##### classes

````json
[ { "nome": "Cluster", "assinatura": "(config: Optional[bbmagic.file_config.FileConfig] = None) -> None" }, { "nome": "FileConfig", "assinatura": "(path) -> None" }, { "nome": "Hdfs", "assinatura": "(username: Optional[str] = None, hdp: Optional[int] = None, set_no_proxy: bool = True, cluster: Optional[str] = 'CDP', config: Optional[bbmagic.file_config.FileConfig] = None, **kwargs) -> None" }, { "nome": "HttpConfig", "assinatura": "(set_no_proxy: bool = True)" }, { "nome": "KerberosClient", "assinatura": "(url, mutual_auth='OPTIONAL', max_concurrency=1, root=None, proxy=None, timeout=None, session=None, **kwargs)" }, { "nome": "Kinit", "assinatura": "(username: Optional[str] = None, conf_file: Optional[str] = None, cluster: str = 'CDP', backoff_limit: int = 3600, hdp: Optional[int] = None) -> None" }, { "nome": "Lookup", "assinatura": "()" } ]
````

##### funcoes

````json
[ { "nome": "get_cloud", "assinatura": "() -> str" }, { "nome": "get_environment", "assinatura": "() -> str" } ]
````

##### constantes

````json
[ { "nome": "Optional", "tipo": "_SpecialForm" } ]
````

##### submodulos

````json
[ "os", "warnings" ]
````

##### erros

````json
[]
````

#### bbmagic.http_config

##### classes

````json
[ { "nome": "FileConfig", "assinatura": "(path) -> None" }, { "nome": "HttpConfig", "assinatura": "(set_no_proxy: bool = True)" }, { "nome": "Path", "assinatura": "(*args, **kwargs)" }, { "nome": "PathLike", "assinatura": "()" } ]
````

##### funcoes

````json
[]
````

##### constantes

````json
[ { "nome": "BBMAGIC_VERSION", "tipo": "str" }, { "nome": "Optional", "tipo": "_SpecialForm" }, { "nome": "Union", "tipo": "_SpecialForm" } ]
````

##### submodulos

````json
[ "os", "requests", "ssl", "time", "urllib3" ]
````

##### erros

````json
[]
````

#### bbmagic.kinit

##### classes

````json
[ { "nome": "Kinit", "assinatura": "(username: Optional[str] = None, conf_file: Optional[str] = None, cluster: str = 'CDP', backoff_limit: int = 3600, hdp: Optional[int] = None) -> None" }, { "nome": "KinitError", "assinatura": null }, { "nome": "Path", "assinatura": "(*args, **kwargs)" } ]
````

##### funcoes

````json
[]
````

##### constantes

````json
[ { "nome": "ENV_KRB5_CONF", "tipo": "PosixPath" }, { "nome": "HDP31_KRB5_CONF", "tipo": "PosixPath" }, { "nome": "Optional", "tipo": "_SpecialForm" } ]
````

##### submodulos

````json
[ "backoff", "getpass", "os", "re", "sp", "warnings" ]
````

##### erros

````json
[]
````

#### bbmagic.livyapi

##### classes

````json
[ { "nome": "Cluster", "assinatura": "(config: Optional[bbmagic.file_config.FileConfig] = None) -> None" }, { "nome": "FileConfig", "assinatura": "(path) -> None" }, { "nome": "HTTPKerberosAuth", "assinatura": "(mutual_authentication=1, service='HTTP', delegate=False, force_preemptive=False, principal=None, hostname_override=None, sanitize_mutual_error_response=True, send_cbt=True)" }, { "nome": "HttpConfig", "assinatura": "(set_no_proxy: bool = True)" }, { "nome": "Kinit", "assinatura": "(username: Optional[str] = None, conf_file: Optional[str] = None, cluster: str = 'CDP', backoff_limit: int = 3600, hdp: Optional[int] = None) -> None" }, { "nome": "LivyApi", "assinatura": "(username: str, cluster: str = 'CDP', spark_version: int = 3, config: Optional[bbmagic.file_config.FileConfig] = None, python: Optional[int] = None) -> None" }, { "nome": "LivyClient", "assinatura": "(url: str, auth: Union[requests.auth.AuthBase, Tuple[str, str]] = None, verify: Union[bool, str] = True, requests_session: requests.sessions.Session = None) -> None" } ]
````

##### funcoes

````json
[ { "nome": "get_cloud", "assinatura": "() -> str" }, { "nome": "get_environment", "assinatura": "() -> str" } ]
````

##### constantes

````json
[ { "nome": "Optional", "tipo": "_SpecialForm" } ]
````

##### submodulos

````json
[ "os", "warnings" ]
````

##### erros

````json
[]
````

#### bbmagic.log

##### classes

````json
[ { "nome": "datetime", "assinatura": null } ]
````

##### funcoes

````json
[ { "nome": "get_start_session", "assinatura": "(session)" }, { "nome": "log_project", "assinatura": "(spark_bbmagic=None)" } ]
````

##### constantes

````json
[]
````

##### submodulos

````json
[ "os", "sys" ]
````

##### erros

````json
[]
````

#### bbmagic.lookup

##### classes

````json
[ { "nome": "Environment", "assinatura": "()" }, { "nome": "Lookup", "assinatura": "()" }, { "nome": "SiglaAPI", "assinatura": "(timeout=10)" } ]
````

##### funcoes

````json
[ { "nome": "urlparse", "assinatura": "(url, scheme='', allow_fragments=True)" } ]
````

##### constantes

````json
[ { "nome": "Optional", "tipo": "_SpecialForm" } ]
````

##### submodulos

````json
[ "os" ]
````

##### erros

````json
[]
````

#### bbmagic.publicador_modelo

##### classes

````json
[]
````

##### funcoes

````json
[]
````

##### constantes

````json
[]
````

##### submodulos

````json
[]
````

##### erros

````json
[ "ERRO_IMPORT: No module named 'big_bblib'" ]
````

#### bbmagic.sas

##### classes

````json
[ { "nome": "AuthInfo", "assinatura": "()" }, { "nome": "AuthKey", "assinatura": "(name: str, user: str, password: Optional[str] = None) -> None" }, { "nome": "SAS", "assinatura": "(username: str = '', host: str = 'sasanl03.intranet.bb.com.br', port: int = 8591, appserver: str = 'SASApp_ANL03 - Workspace Server', authkey: str = '', libnames: Optional[List[dict]] = None, timeout: int = 30) -> None" }, { "nome": "SASProcedureError", "assinatura": null } ]
````

##### funcoes

````json
[]
````

##### constantes

````json
[]
````

##### submodulos

````json
[ "authinfo", "sas", "sascfg" ]
````

##### erros

````json
[]
````

#### bbmagic.sas.authinfo

##### classes

````json
[ { "nome": "AuthInfo", "assinatura": "()" }, { "nome": "AuthKey", "assinatura": "(name: str, user: str, password: Optional[str] = None) -> None" }, { "nome": "Path", "assinatura": "(*args, **kwargs)" } ]
````

##### funcoes

````json
[]
````

##### constantes

````json
[ { "nome": "Optional", "tipo": "_SpecialForm" } ]
````

##### submodulos

````json
[ "getpass", "os" ]
````

##### erros

````json
[]
````

#### bbmagic.sas.sas

##### classes

````json
[ { "nome": "AuthInfo", "assinatura": "()" }, { "nome": "DataFrame", "assinatura": "(data=None, index: 'Axes | None' = None, columns: 'Axes | None' = None, dtype: 'Dtype | None' = None, copy: 'bool | None' = None) -> 'None'" }, { "nome": "Path", "assinatura": "(*args, **kwargs)" }, { "nome": "SAS", "assinatura": "(username: str = '', host: str = 'sasanl03.intranet.bb.com.br', port: int = 8591, appserver: str = 'SASApp_ANL03 - Workspace Server', authkey: str = '', libnames: Optional[List[dict]] = None, timeout: int = 30) -> None" }, { "nome": "SASProcedureError", "assinatura": null }, { "nome": "SASServer", "assinatura": "(host, port, appserver)" }, { "nome": "SASsession", "assinatura": "(**kwargs)" } ]
````

##### funcoes

````json
[ { "nome": "namedtuple", "assinatura": "(typename, field_names, *, rename=False, defaults=None, module=None)" } ]
````

##### constantes

````json
[ { "nome": "Iterator", "tipo": "_SpecialGenericAlias" }, { "nome": "List", "tipo": "_SpecialGenericAlias" }, { "nome": "Optional", "tipo": "_SpecialForm" }, { "nome": "Union", "tipo": "_SpecialForm" }, { "nome": "analiticob02", "tipo": "SASServer" }, { "nome": "sasanl03", "tipo": "SASServer" } ]
````

##### submodulos

````json
[ "getpass", "pd", "re", "uuid" ]
````

##### erros

````json
[]
````

#### bbmagic.sas.sascfg

##### classes

````json
[]
````

##### funcoes

````json
[]
````

##### constantes

````json
[ { "nome": "SAS_config_names", "tipo": "list" }, { "nome": "SAS_config_options", "tipo": "dict" }, { "nome": "iomlinux", "tipo": "dict" } ]
````

##### submodulos

````json
[]
````

##### erros

````json
[]
````

#### bbmagic.sigla_api

##### classes

````json
[ { "nome": "SiglaAPI", "assinatura": "(timeout=10)" } ]
````

##### funcoes

````json
[]
````

##### constantes

````json
[]
````

##### submodulos

````json
[ "requests" ]
````

##### erros

````json
[]
````

#### bbmagic.spark

##### classes

````json
[ { "nome": "BoasPraticasWarning", "assinatura": null }, { "nome": "Cluster", "assinatura": "(config: Optional[bbmagic.file_config.FileConfig] = None) -> None" }, { "nome": "Db2", "assinatura": "(user: Optional[str] = None, password: Optional[str] = None, host: str = 'gwdb2.bb.com.br', port: int = 50100, database: str = 'BDB2P04', trust_env: bool = True, jars_path: Optional[str] = None, backoff_limit: int = 3600, pconnect: bool = True) -> None" }, { "nome": "HTML", "assinatura": "(data=None, url=None, filename=None, metadata=None)" }, { "nome": "HTTPKerberosAuth", "assinatura": "(mutual_authentication=1, service='HTTP', delegate=False, force_preemptive=False, principal=None, hostname_override=None, sanitize_mutual_error_response=True, send_cbt=True)" }, { "nome": "Hdfs", "assinatura": "(username: Optional[str] = None, hdp: Optional[int] = None, set_no_proxy: bool = True, cluster: Optional[str] = 'CDP', config: Optional[bbmagic.file_config.FileConfig] = None, **kwargs) -> None" }, { "nome": "HdfsError", "assinatura": "(message, *args, **kwargs)" }, { "nome": "Kinit", "assinatura": "(username: Optional[str] = None, conf_file: Optional[str] = None, cluster: str = 'CDP', backoff_limit: int = 3600, hdp: Optional[int] = None) -> None" }, { "nome": "LivyApi", "assinatura": "(username: str, cluster: str = 'CDP', spark_version: int = 3, config: Optional[bbmagic.file_config.FileConfig] = None, python: Optional[int] = None) -> None" }, { "nome": "Lookup", "assinatura": "()" }, { "nome": "NamespaceMagics", "assinatura": "(*args: Any, **kwargs: Any) -> Any" }, { "nome": "Path", "assinatura": "(*args, **kwargs)" }, { "nome": "PythonVersion", "assinatura": "()" }, { "nome": "Spark", "assinatura": "(session_name: str, username: Optional[str] = None, language: str = 'python', auth: str = 'Kerberos', timeout: int = 900, db2: bool = False, spark_conf: Optional[dict] = None, jars: Optional[list] = None, archives: Optional[list] = None, pyfiles: Optional[list] = None, files: Optional[list] = None, python: Optional[int] = None, env: Optional[dict] = None, debug: bool = False, driver_memory: str = '8g', driver_cores: int = 4, num_executors: int = 4, executor_memory: str = '2g', executor_cores: int = 4, virtualenv: Optional[str] = None, overwrite_virtualenv: bool = False, cluster: str = 'CDP', spark_version: int = 3)" }, { "nome": "TemporaryDirectory", "assinatura": "(suffix=None, prefix=None, dir=None)" }, { "nome": "datetime", "assinatura": null }, { "nome": "suppress", "assinatura": "(*exceptions)" } ]
````

##### funcoes

````json
[ { "nome": "create_virtualenv", "assinatura": "(requirements: Union[Sequence[str], str, NoneType] = None, path: Optional[str] = None, create_zip: bool = False, zip_path: str = '.', zip_name: str = 'virtualenv') -> virtualenvapi.manage.VirtualEnvironment" }, { "nome": "display", "assinatura": "(*objs, include=None, exclude=None, metadata=None, transient=None, display_id=None, raw=False, clear=False, **kwargs)" }, { "nome": "format_python_version", "assinatura": "(version_num: int) -> str" }, { "nome": "getLogger", "assinatura": "(name=None)" }, { "nome": "get_environment", "assinatura": "() -> str" }, { "nome": "get_ipython", "assinatura": "()" }, { "nome": "get_project_id", "assinatura": "(raise_not_found: bool = False) -> Optional[str]" }, { "nome": "get_python_version", "assinatura": "()" }, { "nome": "log_project", "assinatura": "(spark_bbmagic=None)" }, { "nome": "register_checks", "assinatura": "(checks: dict) -> None" }, { "nome": "urlparse", "assinatura": "(url, scheme='', allow_fragments=True)" } ]
````

##### constantes

````json
[ { "nome": "Dict", "tipo": "_SpecialGenericAlias" }, { "nome": "LIBS_PATHS", "tipo": "dict" }, { "nome": "LIVY_AUTH_KERBEROS", "tipo": "str" }, { "nome": "LIVY_TIMEOUT_SECONDS", "tipo": "int" }, { "nome": "Optional", "tipo": "_SpecialForm" }, { "nome": "PYSPARK_PATHS", "tipo": "dict" }, { "nome": "logger", "tipo": "Logger" }, { "nome": "spark_checks", "tipo": "dict" } ]
````

##### submodulos

````json
[ "errno", "json", "os", "pickle", "random", "requests", "string", "sys", "uuid", "warnings" ]
````

##### erros

````json
[]
````

#### bbmagic.sumary

##### classes

````json
[ { "nome": "DataFrame", "assinatura": "(data=None, index: 'Axes | None' = None, columns: 'Axes | None' = None, dtype: 'Dtype | None' = None, copy: 'bool | None' = None) -> 'None'" }, { "nome": "MetaDataHive", "assinatura": "() -> None" } ]
````

##### funcoes

````json
[ { "nome": "colored", "assinatura": "(text, color=None, on_color=None, attrs=None)" }, { "nome": "display", "assinatura": "(*objs, include=None, exclude=None, metadata=None, transient=None, display_id=None, raw=False, clear=False, **kwargs)" }, { "nome": "dumps", "assinatura": "(obj, *, skipkeys=False, ensure_ascii=True, check_circular=True, allow_nan=True, cls=None, indent=None, separators=None, default=None, sort_keys=False, **kw)" } ]
````

##### constantes

````json
[ { "nome": "Optional", "tipo": "_SpecialForm" }, { "nome": "Union", "tipo": "_SpecialForm" } ]
````

##### submodulos

````json
[ "logging", "os", "pd", "requests", "urllib3" ]
````

##### erros

````json
[]
````

#### bbmagic.teams_notify

##### classes

````json
[ { "nome": "Apprise", "assinatura": "(servers: 'Optional[Union[str, dict, NotifyBase, AppriseConfig, ConfigBase, list[Union[str, dict, NotifyBase, AppriseConfig, ConfigBase]]]]' = None, asset: 'Optional[AppriseAsset]' = None, location: 'Optional[ContentLocation]' = None, debug: 'bool' = False) -> 'None'" }, { "nome": "NotifyFormat", "assinatura": "(value, names=None, *, module=None, qualname=None, type=None, start=1)" }, { "nome": "NotifyType", "assinatura": "(value, names=None, *, module=None, qualname=None, type=None, start=1)" }, { "nome": "TeamsNotify", "assinatura": "(webhook: str)" }, { "nome": "cardsection", "assinatura": "()" }, { "nome": "connectorcard", "assinatura": "(hookurl, http_proxy=None, https_proxy=None, http_timeout=60, verify=None)" } ]
````

##### funcoes

````json
[]
````

##### constantes

````json
[]
````

##### submodulos

````json
[ "common" ]
````

##### erros

````json
[]
````

#### bbmagic.utils

##### classes

````json
[]
````

##### funcoes

````json
[ { "nome": "format_python_version", "assinatura": "(version_num: int) -> str" } ]
````

##### constantes

````json
[]
````

##### submodulos

````json
[]
````

##### erros

````json
[]
````

#### bbmagic.utils.format_python_version

##### classes

````json
[]
````

##### funcoes

````json
[ { "nome": "format_python_version", "assinatura": "(version_num: int) -> str" } ]
````

##### constantes

````json
[]
````

##### submodulos

````json
[]
````

##### erros

````json
[]
````

#### bbmagic.version

##### classes

````json
[]
````

##### funcoes

````json
[]
````

##### constantes

````json
[]
````

##### submodulos

````json
[]
````

##### erros

````json
[]
````

## 4) DEEP-DIVE NAS CLASSES DO BBMAGIC

Classes próprias do bbmagic encontradas: 53

- bbmagic.checks.BoasPraticasWarning
- bbmagic.cluster.Cluster
- bbmagic.cluster.FileConfig
- bbmagic.cluster.HttpConfig
- bbmagic.common.BoasPraticasWarning
- bbmagic.db2.DB2Server
- bbmagic.db2.Db2
- bbmagic.environment.Environment
- bbmagic.exceptions.KinitError
- bbmagic.exceptions.PublicadorError
- bbmagic.file_config.FileConfig
- bbmagic.gitlab_config.FileConfig
- bbmagic.gitlab_config.GitLabConfig
- bbmagic.hdfs.Cluster
- bbmagic.hdfs.FileConfig
- bbmagic.hdfs.Hdfs
- bbmagic.hdfs.HttpConfig
- bbmagic.hdfs.Kinit
- bbmagic.hdfs.Lookup
- bbmagic.http_config.FileConfig
- bbmagic.http_config.HttpConfig
- bbmagic.kinit.Kinit
- bbmagic.kinit.KinitError
- bbmagic.livyapi.Cluster
- bbmagic.livyapi.FileConfig
- bbmagic.livyapi.HttpConfig
- bbmagic.livyapi.Kinit
- bbmagic.livyapi.LivyApi
- bbmagic.lookup.Environment
- bbmagic.lookup.Lookup
- bbmagic.lookup.SiglaAPI
- bbmagic.sas.AuthInfo
- bbmagic.sas.AuthKey
- bbmagic.sas.SAS
- bbmagic.sas.SASProcedureError
- bbmagic.sas.authinfo.AuthInfo
- bbmagic.sas.authinfo.AuthKey
- bbmagic.sas.sas.AuthInfo
- bbmagic.sas.sas.SAS
- bbmagic.sas.sas.SASProcedureError
- bbmagic.sas.sas.SASServer
- bbmagic.sigla_api.SiglaAPI
- bbmagic.spark.BoasPraticasWarning
- bbmagic.spark.Cluster
- bbmagic.spark.Db2
- bbmagic.spark.Hdfs
- bbmagic.spark.Kinit
- bbmagic.spark.LivyApi
- bbmagic.spark.Lookup
- bbmagic.spark.PythonVersion
- bbmagic.spark.Spark
- bbmagic.sumary.MetaDataHive
- bbmagic.teams_notify.TeamsNotify

### CLASSE: bbmagic.checks.BoasPraticasWarning

#### Construtor

````text
None
````

#### Doc

````text
Base class for warnings about dubious runtime behavior.
````

#### Métodos públicos (1)

##### with_traceback

**assinatura**

````text
null
````

**doc**

````text
"Exception.with_traceback(tb) --\nset self.traceback to tb and return self."
````

### CLASSE: bbmagic.cluster.Cluster

#### Construtor

````text
(config: Optional[bbmagic.file_config.FileConfig] = None) -> None
````

#### Métodos públicos (3)

##### exists

**assinatura**

````text
"(cluster: str, service: str)"
````

**doc**

````text
null
````

##### fix

**assinatura**

````text
"(cluster: str)"
````

**doc**

````text
null
````

##### list

**assinatura**

````text
"()"
````

**doc**

````text
null
````

### CLASSE: bbmagic.cluster.FileConfig

#### Construtor

````text
(path) -> None
````

#### Métodos públicos (2)

##### get

**assinatura**

````text
"(self, tag: str, key: str) -> Optional[str]"
````

**doc**

````text
"Retorna o valor da chave se existir; caso contrário, retorna None.\n\nEvitando usar o parâmetro fallback do ConfigParser.get porque os stubs\ndo mypy exigem str e não aceitam None como fallback."
````

##### get_instance

**assinatura**

````text
"()"
````

**doc**

````text
null
````

### CLASSE: bbmagic.cluster.HttpConfig

#### Construtor

````text
(set_no_proxy: bool = True)
````

#### Métodos públicos (3)

##### get

**assinatura**

````text
"(self, tag: str, key: str) -> Optional[str]"
````

**doc**

````text
"Retorna o valor da chave se existir; caso contrário, retorna None.\n\nEvitando usar o parâmetro fallback do ConfigParser.get porque os stubs\ndo mypy exigem str e não aceitam None como fallback."
````

##### get_instance

**assinatura**

````text
"()"
````

**doc**

````text
null
````

##### set_no_proxy

**assinatura**

````text
"(self) -> None"
````

**doc**

````text
"Garante que a variável no_proxy está configurada para ignorar o domínio\nda API web da BBMagic"
````

### CLASSE: bbmagic.common.BoasPraticasWarning

#### Construtor

````text
None
````

#### Doc

````text
Base class for warnings about dubious runtime behavior.
````

#### Métodos públicos (1)

##### with_traceback

**assinatura**

````text
null
````

**doc**

````text
"Exception.with_traceback(tb) --\nset self.traceback to tb and return self."
````

### CLASSE: bbmagic.db2.DB2Server

#### Construtor

````text
(host, port, database)
````

#### Doc

````text
DB2Server(host, port, database)
````

#### Métodos públicos (2)

##### count

**assinatura**

````text
"(self, value, /)"
````

**doc**

````text
"Return number of occurrences of value."
````

##### index

**assinatura**

````text
"(self, value, start=0, stop=9223372036854775807, /)"
````

**doc**

````text
"Return first index of value.\n\nRaises ValueError if the value is not present."
````

### CLASSE: bbmagic.db2.Db2

#### Construtor

````text
(user: Optional[str] = None, password: Optional[str] = None, host: str = 'gwdb2.bb.com.br', port: int = 50100, database: str = 'BDB2P04', trust_env: bool = True, jars_path: Optional[str] = None, backoff_limit: int = 3600, pconnect: bool = True) -> None
````

#### Doc

````text
Cria uma conexão ao DB2
````

#### Métodos públicos (9)

##### connect

**assinatura**

````text
"(self) -> ibm_db_dbi.Connection"
````

**doc**

````text
"Cria a conexão JDBC com o servidor DB2."
````

##### describe

**assinatura**

````text
"(self, schema: str, table: str) -> IPython.core.display.HTML"
````

**doc**

````text
"Gera um relatório consolidado com os metadados da tabela existentes no catálogo\ndo DB2.\n\n:param schema: nome do schema\n:param table: nome da tabela\n\n:return: Retorna um objeto HTML com o relatório para exibição no Jupyter Notebook.\n:rtype: IPython.core.display.HTML"
````

##### get_cofre_credentials

**assinatura**

````text
"(self, project_id: str) -> dict"
````

**doc**

````text
"Recupera credenciais do cofre com base no project_id do projeto"
````

##### query

**assinatura**

````text
"(self, sql: str, params: Optional[list] = None, chunksize: Optional[int] = 2500) -> Union[pandas.core.frame.DataFrame, Iterator[pandas.core.frame.DataFrame]]"
````

**doc**

````text
"Retorna um DataFrame contendo o resultado da execução da query SQL.\n\n:param sql: query SQL para execução\n:param params: lista de parâmetros para utilização na query\n:param chunksize: Se especificado, retorna um iterador onde chunksize é a quantidade\n de linhas incluídas em cada chunk\n\n:return: Daframe ou Iterator[DataFrame]\n\nExemplos de Uso::\n\n >>> for chunk in db2.query("SELEC [...]"
````

##### set_conn_param

**assinatura**

````text
"(self, param_name, param_value: Union[str, int, NoneType]) -> Union[str, int]"
````

**doc**

````text
null
````

##### show_schemas

**assinatura**

````text
"(self) -> pandas.core.frame.DataFrame"
````

**doc**

````text
"Lista todos os schemas no database\n\n:return: Retorna um Pandas DataFrame contendo uma linha para cada schema encontrado.\n:rtype: pandas.core.api.DataFrame\n\nExemplo de uso::\n\n >>> db2.show_schemas()"
````

##### show_tables

**assinatura**

````text
"(self, schema: str) -> pandas.core.frame.DataFrame"
````

**doc**

````text
"Lista todas as tabelas e views de um schema.\n\n:param schema: nome do schema\n\n:return: Retorna um Pandas DataFrame contendo uma linha para cada tabela do schema\n e as informações schema, name e type nas respectivas colunas.\n:rtype: pandas.core.api.DataFrame\n\nExemplo de uso::\n\n >>> db2.show_tables("DB2MCI")"
````

##### syscolumns

**assinatura**

````text
"(self, schema: str, table: str) -> pandas.core.frame.DataFrame"
````

**doc**

````text
"Retorna metadados das colunas de uma tabela.\n\n:param schema: nome do schema\n:param table: nome da tabela\n\n:return: Retorna um Pandas DataFrame contendo as informações sobre as colunas da\n tabela de acordo com o catálogo syscat.syscolumns\n:rtype: pandas.core.api.DataFrame"
````

##### systabstats

**assinatura**

````text
"(self, schema: str, table: str) -> pandas.core.frame.DataFrame"
````

**doc**

````text
"Retorna metadados de uma tabela.\n\n:param schema: nome do schema\n:param table: nome da tabela\n\n:return: Retorna um Pandas DataFrame contendo as informações sobre a tabela\n existentes no catálogo syscat.systabstats\n:rtype: pandas.core.api.DataFrame"
````

### CLASSE: bbmagic.environment.Environment

#### Construtor

````text
()
````

#### Métodos públicos (3)

##### get

**assinatura**

````text
"(self) -> str"
````

**doc**

````text
null
````

##### is_modeling

**assinatura**

````text
"(self) -> bool"
````

**doc**

````text
null
````

##### is_prodution

**assinatura**

````text
"(self) -> bool"
````

**doc**

````text
null
````

### CLASSE: bbmagic.exceptions.KinitError

#### Construtor

````text
None
````

#### Doc

````text
Erro exibido quando há falha na autenticação com o kinit
````

#### Métodos públicos (1)

##### with_traceback

**assinatura**

````text
null
````

**doc**

````text
"Exception.with_traceback(tb) --\nset self.traceback to tb and return self."
````

### CLASSE: bbmagic.exceptions.PublicadorError

#### Construtor

````text
None
````

#### Doc

````text
Erro exibido quando há falha ao salvar um modelo no Artifactory
````

#### Métodos públicos (1)

##### with_traceback

**assinatura**

````text
null
````

**doc**

````text
"Exception.with_traceback(tb) --\nset self.traceback to tb and return self."
````

### CLASSE: bbmagic.file_config.FileConfig

#### Construtor

````text
(path) -> None
````

#### Métodos públicos (2)

##### get

**assinatura**

````text
"(self, tag: str, key: str) -> Optional[str]"
````

**doc**

````text
"Retorna o valor da chave se existir; caso contrário, retorna None.\n\nEvitando usar o parâmetro fallback do ConfigParser.get porque os stubs\ndo mypy exigem str e não aceitam None como fallback."
````

##### get_instance

**assinatura**

````text
"()"
````

**doc**

````text
null
````

### CLASSE: bbmagic.gitlab_config.FileConfig

#### Construtor

````text
(path) -> None
````

#### Métodos públicos (2)

##### get

**assinatura**

````text
"(self, tag: str, key: str) -> Optional[str]"
````

**doc**

````text
"Retorna o valor da chave se existir; caso contrário, retorna None.\n\nEvitando usar o parâmetro fallback do ConfigParser.get porque os stubs\ndo mypy exigem str e não aceitam None como fallback."
````

##### get_instance

**assinatura**

````text
"()"
````

**doc**

````text
null
````

### CLASSE: bbmagic.gitlab_config.GitLabConfig

#### Construtor

````text
()
````

#### Métodos públicos (2)

##### get

**assinatura**

````text
"(self, tag: str, key: str) -> Optional[str]"
````

**doc**

````text
"Retorna o valor da chave se existir; caso contrário, retorna None.\n\nEvitando usar o parâmetro fallback do ConfigParser.get porque os stubs\ndo mypy exigem str e não aceitam None como fallback."
````

##### get_instance

**assinatura**

````text
"()"
````

**doc**

````text
null
````

### CLASSE: bbmagic.hdfs.Cluster

#### Construtor

````text
(config: Optional[bbmagic.file_config.FileConfig] = None) -> None
````

#### Métodos públicos (3)

##### exists

**assinatura**

````text
"(cluster: str, service: str)"
````

**doc**

````text
null
````

##### fix

**assinatura**

````text
"(cluster: str)"
````

**doc**

````text
null
````

##### list

**assinatura**

````text
"()"
````

**doc**

````text
null
````

### CLASSE: bbmagic.hdfs.FileConfig

#### Construtor

````text
(path) -> None
````

#### Métodos públicos (2)

##### get

**assinatura**

````text
"(self, tag: str, key: str) -> Optional[str]"
````

**doc**

````text
"Retorna o valor da chave se existir; caso contrário, retorna None.\n\nEvitando usar o parâmetro fallback do ConfigParser.get porque os stubs\ndo mypy exigem str e não aceitam None como fallback."
````

##### get_instance

**assinatura**

````text
"()"
````

**doc**

````text
null
````

### CLASSE: bbmagic.hdfs.Hdfs

#### Construtor

````text
(username: Optional[str] = None, hdp: Optional[int] = None, set_no_proxy: bool = True, cluster: Optional[str] = 'CDP', config: Optional[bbmagic.file_config.FileConfig] = None, **kwargs) -> None
````

#### Doc

````text
Permite acesso ao HDFS com autenticação via kerberos.
````

#### Documentação complementar

````text
:param username: matrícula ou caminho para arquivo keytab :param hdp: Cluster HDP para conexão utilizar: 3 para HDP 3.1 our 2 para HDP 2.6 :param cluster: Identifica o cluster que deve receber a conexao - hdp ou cdp :param **kwargs: Argumentos [...]
````

#### Métodos públicos (30)

##### acl_status

**assinatura**

````text
"(self, hdfs_path, strict=True)"
````

**doc**

````text
"Get AclStatus_ for a file or folder on HDFS.\n\n:param hdfs_path: Remote path.\n:param strict: If False, return None rather than raise an exception if\n the path doesn't exist.\n\n.. AclStatus: https://hadoop.apache.org/docs/stable2/hadoop-project-dist/hadoop-hdfs/WebHDFS.html#Get_ACL_Status"
````

##### allow_snapshot

**assinatura**

````text
"(self, hdfs_path)"
````

**doc**

````text
"Allow snapshots for a remote folder.\n\n:param hdfs_path: Remote path to a directory. If hdfs_path\n doesn't exist or does points to a normal file, an\n :class:HdfsError will be raised. No-op if snapshotting is\n already allowed."
````

##### checksum

**assinatura**

````text
"(self, hdfs_path)"
````

**doc**

````text
"Get a remote file's checksum.\n\n:param hdfs_path: Remote path. Must point to a file."
````

##### content

**assinatura**

````text
"(self, hdfs_path, strict=True)"
````

**doc**

````text
"Get ContentSummary for a file or folder on HDFS.\n\n:param hdfs_path: Remote path.\n:param strict: If False, return None rather than raise an exception if\n the path doesn't exist.\n\n.. ContentSummary: CS\n.. CS: http://hadoop.apache.org/docs/r1.0.4/webhdfs.html#ContentSummary"
````

##### create_snapshot

**assinatura**

````text
"(self, hdfs_path, snapshotname=None)"
````

**doc**

````text
"Create snapshot for a remote folder where it was allowed.\n\n:param hdfs_path: Remote path to a directory. If hdfs_path\n doesn't exist, doesn't allow to create snapshot or points to a\n normal file, an :class:HdfsError will be raised.\n:param snapshotname snapshot name; if absent, name is generated\n by the server.\n\nReturns a path to created snapshot."
````

##### delete

**assinatura**

````text
"(self, hdfs_path, recursive=False, skip_trash=True)"
````

**doc**

````text
"Remove a file or directory from HDFS.\n\n:param hdfs_path: HDFS path.\n:param recursive: Recursively delete files and directories. By default,\n this method will raise an :class:HdfsError if trying to delete a\n non-empty directory.\n:param skip_trash: When false, the deleted path will be moved to an\n appropriate trash folder rather than deleted. This requires Hadoop 2.9+\n and trash to be enabled [...]"
````

##### delete_snapshot

**assinatura**

````text
"(self, hdfs_path, snapshotname)"
````

**doc**

````text
"Remove snapshot for a remote folder where it was allowed.\n\n:param hdfs_path: Remote path to a directory. If hdfs_path doesn't exist\n or points to a normal file, an :class:HdfsError will be raised.\n:param snapshotname snapshot name; if it does not exist, an\n :class:HdfsError will be raised."
````

##### disallow_snapshot

**assinatura**

````text
"(self, hdfs_path)"
````

**doc**

````text
"Disallow snapshots for a remote folder.\n\n:param hdfs_path: Remote path to a directory. If hdfs_path\n doesn't exist, points to a normal file or there are some\n snapshots, an :class:HdfsError will be raised.\n\nNo-op if snapshotting is disallowed/never allowed."
````

##### download

**assinatura**

````text
"(self, hdfs_path, local_path, overwrite=False, n_threads=1, temp_dir=None, **kwargs)"
````

**doc**

````text
"Download a file or folder from HDFS and save it locally.\n\n:param hdfs_path: Path on HDFS of the file or folder to download. If a\n folder, all the files under it will be downloaded.\n:param local_path: Local path. If it already exists and is a directory,\n the files will be downloaded inside of it.\n:param overwrite: Overwrite any existing file or directory.\n:param n_threads: Number of threads to us [...]"
````

##### from_options

**assinatura**

````text
"(options, class_name='Client')"
````

**doc**

````text
"Load client from options.\n\n:param options: Options dictionary.\n:param class_name: Client class name. Defaults to the base :class:Client\n class.\n\nThis method provides a single entry point to instantiate any registered\n:class:Client subclass. To register a subclass, simply load its\ncontaining module. If using the CLI, you can use the autoload.modules and\nautoload.paths options."
````

##### list

**assinatura**

````text
"(self, hdfs_path, status=False)"
````

**doc**

````text
"Return names of files contained in a remote folder.\n\n:param hdfs_path: Remote path to a directory. If hdfs_path doesn't exist\n or points to a normal file, an :class:HdfsError will be raised.\n:param status: Also return each file's corresponding FileStatus."
````

##### makedirs

**assinatura**

````text
"(self, hdfs_path, permission=None)"
````

**doc**

````text
"Create a remote directory, recursively if necessary.\n\n:param hdfs_path: Remote path. Intermediate directories will be created\n appropriately.\n:param permission: Octal permission to set on the newly created directory.\n These permissions will only be set on directories that do not already\n exist.\n\nThis function currently has no return value as WebHDFS doesn't return a\nmeaningful flag."
````

##### parts

**assinatura**

````text
"(self, hdfs_path, parts=None, status=False)"
````

**doc**

````text
"Returns a dictionary of part-files corresponding to a path.\n\n:param hdfs_path: Remote path. This directory should contain at most one\n part file per partition (otherwise one will be picked arbitrarily).\n:param parts: List of part-files numbers or total number of part-files to\n select. If a number, that many partitions will be chosen at random. By\n default all part-files are returned. If parts [...]"
````

##### read

**assinatura**

````text
"(self, hdfs_path, offset=0, length=None, buffer_size=None, encoding=None, chunk_size=0, delimiter=None, progress=None)"
````

**doc**

````text
"Read a file from HDFS.\n\n:param hdfs_path: HDFS path.\n:param offset: Starting byte position.\n:param length: Number of bytes to be processed. None will read the entire\n file.\n:param buffer_size: Size of the buffer in bytes used for transferring the\n data. Defaults the the value set in the HDFS configuration.\n:param encoding: Encoding used to decode the request. By default the raw\n data is retur [...]"
````

##### remove_acl

**assinatura**

````text
"(self, hdfs_path)"
````

**doc**

````text
"RemoveAcl_ for a file or folder on HDFS.\n\n:param hdfs_path: Path to an existing remote file or directory. An\n :class:HdfsError will be raised if the path doesn't exist.\n\n.. RemoveAcl: https://hadoop.apache.org/docs/stable2/hadoop-project-dist/hadoop-hdfs/WebHDFS.html#Remove_ACL"
````

##### remove_acl_entries

**assinatura**

````text
"(self, hdfs_path, acl_spec)"
````

**doc**

````text
"RemoveAclEntries for a file or folder on HDFS.\n\n:param hdfs_path: Path to an existing remote file or directory. An\n :class:HdfsError will be raised if the path doesn't exist.\n:param acl_spec: String representation of an ACL spec. Must be a valid\n string with entries for user, group and other. For example:\n \"user::rwx,user:foo:rw-,group::r--,other::---\".\n\n.. RemoveAclEntries: https://hadoo [...]"
````

##### remove_default_acl

**assinatura**

````text
"(self, hdfs_path)"
````

**doc**

````text
"RemoveDefaultAcl for a file or folder on HDFS.\n\n:param hdfs_path: Path to an existing remote file or directory. An\n :class:HdfsError will be raised if the path doesn't exist.\n\n.. RemoveDefaultAcl: https://hadoop.apache.org/docs/stable2/hadoop-project-dist/hadoop-hdfs/WebHDFS.html#Remove_Default_ACL"
````

##### rename

**assinatura**

````text
"(self, hdfs_src_path, hdfs_dst_path)"
````

**doc**

````text
"Move a file or folder.\n\n:param hdfs_src_path: Source path.\n:param hdfs_dst_path: Destination path. If the path already exists and is\n a directory, the source will be moved into it. If the path exists and is\n a file, or if a parent destination directory is missing, this method will\n raise an :class:HdfsError."
````

##### rename_snapshot

**assinatura**

````text
"(self, hdfs_path, oldsnapshotname, snapshotname)"
````

**doc**

````text
"Rename snapshot for a remote folder.\n\n:param hdfs_path: Remote path to a directory. If hdfs_path doesn't exist\n or points to a normal file, an :class:HdfsError will be raised.\n:param oldsnapshotname snapshot name; if it does not exist,\n an :class:HdfsError will be raised.\n:param snapshotname new snapshot name; if it does already exist,\n an :class:HdfsError will be raised."
````

##### resolve

**assinatura**

````text
"(self, hdfs_path)"
````

**doc**

````text
"Return absolute, normalized path, with special markers expanded.\n\n:param hdfs_path: Remote path.\n\nCurrently supported markers:\n\n* '#LATEST': this marker gets expanded to the most recently updated file\n or folder. They can be combined using the '{N}' suffix. For example,\n 'foo/#LATEST{2}' is equivalent to 'foo/#LATEST/#LATEST'."
````

##### set_acl

**assinatura**

````text
"(self, hdfs_path, acl_spec, clear=True)"
````

**doc**

````text
"SetAcl or ModifyAcl_ for a file or folder on HDFS.\n\n:param hdfs_path: Path to an existing remote file or directory. An\n :class:HdfsError will be raised if the path doesn't exist.\n:param acl_spec: String representation of an ACL spec. Must be a valid\n string with entries for user, group and other. For example:\n \"user::rwx,user:foo:rw-,group::r--,other::---\".\n:param clear: Clear existing ACL [...]"
````

##### set_no_proxy

**assinatura**

````text
"(self) -> None"
````

**doc**

````text
"Garante que a variável no_proxy está configurada para ignorar o domínio\nda API web da BBMagic"
````

##### set_owner

**assinatura**

````text
"(self, hdfs_path, owner=None, group=None)"
````

**doc**

````text
"Change the owner of file.\n\n:param hdfs_path: HDFS path.\n:param owner: Optional, new owner for file.\n:param group: Optional, new group for file.\n\nAt least one of owner and group must be specified."
````

##### set_permission

**assinatura**

````text
"(self, hdfs_path, permission)"
````

**doc**

````text
"Change the permissions of file.\n\n:param hdfs_path: HDFS path.\n:param permission: New octal permissions string of file."
````

##### set_replication

**assinatura**

````text
"(self, hdfs_path, replication)"
````

**doc**

````text
"Set file replication.\n\n:param hdfs_path: Path to an existing remote file. An :class:HdfsError\n will be raised if the path doesn't exist or points to a directory.\n:param replication: Replication factor."
````

##### set_times

**assinatura**

````text
"(self, hdfs_path, access_time=None, modification_time=None)"
````

**doc**

````text
"Change remote timestamps.\n\n:param hdfs_path: HDFS path.\n:param access_time: Timestamp of last file access.\n:param modification_time: Timestamps of last file access."
````

##### status

**assinatura**

````text
"(self, hdfs_path, strict=True)"
````

**doc**

````text
"Get FileStatus_ for a file or folder on HDFS.\n\n:param hdfs_path: Remote path.\n:param strict: If False, return None rather than raise an exception if\n the path doesn't exist.\n\n.. FileStatus: FS\n.. FS: http://hadoop.apache.org/docs/r1.0.4/webhdfs.html#FileStatus"
````

##### upload

**assinatura**

````text
"(self, hdfs_path, local_path, n_threads=1, temp_dir=None, chunk_size=65536, progress=None, cleanup=True, **kwargs)"
````

**doc**

````text
"Upload a file or directory to HDFS.\n\n:param hdfs_path: Target HDFS path. If it already exists and is a\n directory, files will be uploaded inside.\n:param local_path: Local path to file or folder. If a folder, all the files\n inside of it will be uploaded (note that this implies that folders empty\n of files will not be created remotely).\n:param n_threads: Number of threads to use for parallelizati [...]"
````

##### walk

**assinatura**

````text
"(self, hdfs_path, depth=0, status=False, ignore_missing=False, allow_dir_changes=False)"
````

**doc**

````text
"Depth-first walk of remote filesystem.\n\n:param hdfs_path: Starting path. If the path doesn't exist, an\n :class:HdfsError will be raised. If it points to a file, the returned\n generator will be empty.\n:param depth: Maximum depth to explore. 0 for no limit.\n:param status: Also return each file or folder's corresponding FileStatus.\n:param ignore_missing: Ignore missing nested folders rather th [...]"
````

##### write

**assinatura**

````text
"(self, hdfs_path, data=None, overwrite=False, permission=None, blocksize=None, replication=None, buffersize=None, append=False, encoding=None)"
````

**doc**

````text
"Create a file on HDFS.\n\n:param hdfs_path: Path where to create file. The necessary directories will\n be created appropriately.\n:param data: Contents of file to write. Can be a string, a generator or a\n file object. The last two options will allow streaming upload (i.e.\n without having to load the entire contents into memory). If None, this\n method will return a file-like object and should be [...]"
````

### CLASSE: bbmagic.hdfs.HttpConfig

#### Construtor

````text
(set_no_proxy: bool = True)
````

#### Métodos públicos (3)

##### get

**assinatura**

````text
"(self, tag: str, key: str) -> Optional[str]"
````

**doc**

````text
"Retorna o valor da chave se existir; caso contrário, retorna None.\n\nEvitando usar o parâmetro fallback do ConfigParser.get porque os stubs\ndo mypy exigem str e não aceitam None como fallback."
````

##### get_instance

**assinatura**

````text
"()"
````

**doc**

````text
null
````

##### set_no_proxy

**assinatura**

````text
"(self) -> None"
````

**doc**

````text
"Garante que a variável no_proxy está configurada para ignorar o domínio\nda API web da BBMagic"
````

### CLASSE: bbmagic.hdfs.Kinit

#### Construtor

````text
(username: Optional[str] = None, conf_file: Optional[str] = None, cluster: str = 'CDP', backoff_limit: int = 3600, hdp: Optional[int] = None) -> None
````

#### Doc

````text
Autentica o usuário no Kerberos utilizando kinit.
````

#### Documentação complementar

````text
:param username: matrícula ou caminho para arquivo keytab :param conf_file: caminho para o arquivo krb5.conf. Caso não seja informado será utilizada configuração do arquivo temporátio gerado pelo pacote :param hdp: Parâmetro depr [...]
````

#### Métodos públicos (6)

##### get_ticket

**assinatura**

````text
"(self) -> str"
````

**doc**

````text
"Autentica no Kerberos utilizando Kinit.\n\nVerifica se o usuário já possui um ticket kerberos válido. Caso não encontre\nrealiza a autenticação com kinit. O parâmetro informado pode ser a matrícula\ndo usuário ou uma keytab.\n\nCaso a matrícula seja informada, um prompt será exibido para que a senha SISBB\nseja informada.\n\nCaso o caminho para uma keytab seja informada, utiliza o arquivo. Caso seja inform [...]"
````

##### get_username

**assinatura**

````text
"(self, username: Optional[str]) -> str"
````

**doc**

````text
null
````

##### is_matricula

**assinatura**

````text
"(self, string: str) -> bool"
````

**doc**

````text
null
````

##### raise_keytab_on_modelagem

**assinatura**

````text
"(self) -> None"
````

**doc**

````text
null
````

##### run_kinit_cmd

**assinatura**

````text
"(self, kinit_cmd: list, password: Optional[str]) -> int"
````

**doc**

````text
null
````

##### user_has_ticket

**assinatura**

````text
"(self) -> bool"
````

**doc**

````text
"Verifica se há um ticket válido no cache de credenciais do Kerberos.\n\nVerifica as credenciais no cache padrão ou no caminho indicado na\nvariável de ambiente KRB5CCNAME."
````

### CLASSE: bbmagic.hdfs.Lookup

#### Construtor

````text
()
````

#### Métodos públicos (2)

##### migration_cluster

**assinatura**

````text
"(self, cluster: str = 'CDP') -> str"
````

**doc**

````text
null
````

##### sigla

**assinatura**

````text
"(self) -> str"
````

**doc**

````text
null
````

### CLASSE: bbmagic.http_config.FileConfig

#### Construtor

````text
(path) -> None
````

#### Métodos públicos (2)

##### get

**assinatura**

````text
"(self, tag: str, key: str) -> Optional[str]"
````

**doc**

````text
"Retorna o valor da chave se existir; caso contrário, retorna None.\n\nEvitando usar o parâmetro fallback do ConfigParser.get porque os stubs\ndo mypy exigem str e não aceitam None como fallback."
````

##### get_instance

**assinatura**

````text
"()"
````

**doc**

````text
null
````

### CLASSE: bbmagic.http_config.HttpConfig

#### Construtor

````text
(set_no_proxy: bool = True)
````

#### Métodos públicos (3)

##### get

**assinatura**

````text
"(self, tag: str, key: str) -> Optional[str]"
````

**doc**

````text
"Retorna o valor da chave se existir; caso contrário, retorna None.\n\nEvitando usar o parâmetro fallback do ConfigParser.get porque os stubs\ndo mypy exigem str e não aceitam None como fallback."
````

##### get_instance

**assinatura**

````text
"()"
````

**doc**

````text
null
````

##### set_no_proxy

**assinatura**

````text
"(self) -> None"
````

**doc**

````text
"Garante que a variável no_proxy está configurada para ignorar o domínio\nda API web da BBMagic"
````

### CLASSE: bbmagic.kinit.Kinit

#### Construtor

````text
(username: Optional[str] = None, conf_file: Optional[str] = None, cluster: str = 'CDP', backoff_limit: int = 3600, hdp: Optional[int] = None) -> None
````

#### Doc

````text
Autentica o usuário no Kerberos utilizando kinit.
````

#### Documentação complementar

````text
:param username: matrícula ou caminho para arquivo keytab :param conf_file: caminho para o arquivo krb5.conf. Caso não seja informado será utilizada configuração do arquivo temporátio gerado pelo pacote :param hdp: Parâmetro depr [...]
````

#### Métodos públicos (6)

##### get_ticket

**assinatura**

````text
"(self) -> str"
````

**doc**

````text
"Autentica no Kerberos utilizando Kinit.\n\nVerifica se o usuário já possui um ticket kerberos válido. Caso não encontre\nrealiza a autenticação com kinit. O parâmetro informado pode ser a matrícula\ndo usuário ou uma keytab.\n\nCaso a matrícula seja informada, um prompt será exibido para que a senha SISBB\nseja informada.\n\nCaso o caminho para uma keytab seja informada, utiliza o arquivo. Caso seja inform [...]"
````

##### get_username

**assinatura**

````text
"(self, username: Optional[str]) -> str"
````

**doc**

````text
null
````

##### is_matricula

**assinatura**

````text
"(self, string: str) -> bool"
````

**doc**

````text
null
````

##### raise_keytab_on_modelagem

**assinatura**

````text
"(self) -> None"
````

**doc**

````text
null
````

##### run_kinit_cmd

**assinatura**

````text
"(self, kinit_cmd: list, password: Optional[str]) -> int"
````

**doc**

````text
null
````

##### user_has_ticket

**assinatura**

````text
"(self) -> bool"
````

**doc**

````text
"Verifica se há um ticket válido no cache de credenciais do Kerberos.\n\nVerifica as credenciais no cache padrão ou no caminho indicado na\nvariável de ambiente KRB5CCNAME."
````

### CLASSE: bbmagic.kinit.KinitError

#### Construtor

````text
None
````

#### Doc

````text
Erro exibido quando há falha na autenticação com o kinit
````

#### Métodos públicos (1)

##### with_traceback

**assinatura**

````text
null
````

**doc**

````text
"Exception.with_traceback(tb) --\nset self.traceback to tb and return self."
````

### CLASSE: bbmagic.livyapi.Cluster

#### Construtor

````text
(config: Optional[bbmagic.file_config.FileConfig] = None) -> None
````

#### Métodos públicos (3)

##### exists

**assinatura**

````text
"(cluster: str, service: str)"
````

**doc**

````text
null
````

##### fix

**assinatura**

````text
"(cluster: str)"
````

**doc**

````text
null
````

##### list

**assinatura**

````text
"()"
````

**doc**

````text
null
````

### CLASSE: bbmagic.livyapi.FileConfig

#### Construtor

````text
(path) -> None
````

#### Métodos públicos (2)

##### get

**assinatura**

````text
"(self, tag: str, key: str) -> Optional[str]"
````

**doc**

````text
"Retorna o valor da chave se existir; caso contrário, retorna None.\n\nEvitando usar o parâmetro fallback do ConfigParser.get porque os stubs\ndo mypy exigem str e não aceitam None como fallback."
````

##### get_instance

**assinatura**

````text
"()"
````

**doc**

````text
null
````

### CLASSE: bbmagic.livyapi.HttpConfig

#### Construtor

````text
(set_no_proxy: bool = True)
````

#### Métodos públicos (3)

##### get

**assinatura**

````text
"(self, tag: str, key: str) -> Optional[str]"
````

**doc**

````text
"Retorna o valor da chave se existir; caso contrário, retorna None.\n\nEvitando usar o parâmetro fallback do ConfigParser.get porque os stubs\ndo mypy exigem str e não aceitam None como fallback."
````

##### get_instance

**assinatura**

````text
"()"
````

**doc**

````text
null
````

##### set_no_proxy

**assinatura**

````text
"(self) -> None"
````

**doc**

````text
"Garante que a variável no_proxy está configurada para ignorar o domínio\nda API web da BBMagic"
````

### CLASSE: bbmagic.livyapi.Kinit

#### Construtor

````text
(username: Optional[str] = None, conf_file: Optional[str] = None, cluster: str = 'CDP', backoff_limit: int = 3600, hdp: Optional[int] = None) -> None
````

#### Doc

````text
Autentica o usuário no Kerberos utilizando kinit.
````

#### Documentação complementar

````text
:param username: matrícula ou caminho para arquivo keytab :param conf_file: caminho para o arquivo krb5.conf. Caso não seja informado será utilizada configuração do arquivo temporátio gerado pelo pacote :param hdp: Parâmetro depr [...]
````

#### Métodos públicos (6)

##### get_ticket

**assinatura**

````text
"(self) -> str"
````

**doc**

````text
"Autentica no Kerberos utilizando Kinit.\n\nVerifica se o usuário já possui um ticket kerberos válido. Caso não encontre\nrealiza a autenticação com kinit. O parâmetro informado pode ser a matrícula\ndo usuário ou uma keytab.\n\nCaso a matrícula seja informada, um prompt será exibido para que a senha SISBB\nseja informada.\n\nCaso o caminho para uma keytab seja informada, utiliza o arquivo. Caso seja inform [...]"
````

##### get_username

**assinatura**

````text
"(self, username: Optional[str]) -> str"
````

**doc**

````text
null
````

##### is_matricula

**assinatura**

````text
"(self, string: str) -> bool"
````

**doc**

````text
null
````

##### raise_keytab_on_modelagem

**assinatura**

````text
"(self) -> None"
````

**doc**

````text
null
````

##### run_kinit_cmd

**assinatura**

````text
"(self, kinit_cmd: list, password: Optional[str]) -> int"
````

**doc**

````text
null
````

##### user_has_ticket

**assinatura**

````text
"(self) -> bool"
````

**doc**

````text
"Verifica se há um ticket válido no cache de credenciais do Kerberos.\n\nVerifica as credenciais no cache padrão ou no caminho indicado na\nvariável de ambiente KRB5CCNAME."
````

### CLASSE: bbmagic.livyapi.LivyApi

#### Construtor

````text
(username: str, cluster: str = 'CDP', spark_version: int = 3, config: Optional[bbmagic.file_config.FileConfig] = None, python: Optional[int] = None) -> None
````

#### Doc

````text
A client for sending requests to a Livy server.
````

#### Documentação complementar

````text
:param url: The URL of the Livy server. :param auth: A requests-compatible auth object to use when making requests. :param verify: Either a boolean, in which case it controls whether we verify the server’s TLS certificate, or a string, in which ca [...]
````

#### Métodos públicos (15)

##### close

**assinatura**

````text
"(self) -> None"
````

**doc**

````text
"Close the underlying requests session, if managed by this class."
````

##### create_batch

**assinatura**

````text
"(self, file: str, class_name: str = None, args: List[str] = None, proxy_user: str = None, jars: List[str] = None, py_files: List[str] = None, files: List[str] = None, driver_memory: str = None, driver_cores: int = None, executor_memory: str = None, executor_cores: int = None, num_executors: int = None, archives: List[str] = None, queue: str = None, name: str = None, spark_conf: Dict[str, Any] = None) -> livy.models.Batch"
````

**doc**

````text
"Create a new batch in Livy.\n\nThe py_files, files, jars and archives arguments are lists of URLs,\ne.g. ["s3://bucket/object", "hdfs://path/to/file", ...] and must be\nreachable by the Spark driver process. If the provided URL has no\nscheme, it's considered to be relative to the default file system\nconfigured in the Livy server.\n\nURLs in the py_files argument are copied to a temporary staging area\na [...]"
````

##### create_session

**assinatura**

````text
"(self, kind: livy.models.SessionKind, proxy_user: str = None, jars: List[str] = None, py_files: List[str] = None, files: List[str] = None, driver_memory: str = None, driver_cores: int = None, executor_memory: str = None, executor_cores: int = None, num_executors: int = None, archives: List[str] = None, queue: str = None, name: str = None, spark_conf: Dict[str, Any] = None, heartbeat_timeout: int = None) -> livy.models.Session"
````

**doc**

````text
"Create a new session in Livy.\n\nThe py_files, files, jars and archives arguments are lists of URLs,\ne.g. ["s3://bucket/object", "hdfs://path/to/file", ...] and must be\nreachable by the Spark driver process. If the provided URL has no\nscheme, it's considered to be relative to the default file system\nconfigured in the Livy server.\n\nURLs in the py_files argument are copied to a temporary staging area [...]"
````

##### create_statement

**assinatura**

````text
"(self, session_id: int, code: str, kind: livy.models.StatementKind = None) -> livy.models.Statement"
````

**doc**

````text
"Run a statement in a session.\n\n:param session_id: The ID of the session.\n:param code: The code to execute.\n:param kind: The kind of code to execute."
````

##### delete_batch

**assinatura**

````text
"(self, batch_id: int) -> None"
````

**doc**

````text
"Kill a batch session.\n\n:param batch_id: The ID of the session."
````

##### delete_session

**assinatura**

````text
"(self, session_id: int) -> None"
````

**doc**

````text
"Kill a session.\n\n:param session_id: The ID of the session."
````

##### get_batch

**assinatura**

````text
"(self, batch_id: int) -> Optional[livy.models.Batch]"
````

**doc**

````text
"Get information about a batch.\n\n:param batch_id: The ID of the batch."
````

##### get_batch_log

**assinatura**

````text
"(self, batch_id: int, from_: int = None, size: int = None) -> Optional[livy.models.BatchLog]"
````

**doc**

````text
"Get logs for a batch.\n\n:param batch_id: The ID of the batch.\n:param from_: The line number to start getting logs from.\n:param size: The number of lines of logs to get."
````

##### get_session

**assinatura**

````text
"(self, session_id: int) -> Optional[livy.models.Session]"
````

**doc**

````text
"Get information about a session.\n\n:param session_id: The ID of the session."
````

##### get_statement

**assinatura**

````text
"(self, session_id: int, statement_id: int) -> livy.models.Statement"
````

**doc**

````text
"Get information about a statement in a session.\n\n:param session_id: The ID of the session.\n:param statement_id: The ID of the statement."
````

##### legacy_server

**assinatura**

````text
"(self) -> bool"
````

**doc**

````text
"Determine if the server is running a legacy version.\n\nLegacy versions support different session kinds than newer versions of\nLivy."
````

##### list_batches

**assinatura**

````text
"(self) -> List[livy.models.Batch]"
````

**doc**

````text
"List all the active batches in Livy."
````

##### list_sessions

**assinatura**

````text
"(self) -> List[livy.models.Session]"
````

**doc**

````text
"List all the active sessions in Livy."
````

##### list_statements

**assinatura**

````text
"(self, session_id: int) -> List[livy.models.Statement]"
````

**doc**

````text
"Get all the statements in a session.\n\n:param session_id: The ID of the session."
````

##### server_version

**assinatura**

````text
"(self) -> livy.models.Version"
````

**doc**

````text
"Get the version of Livy running on the server."
````

### CLASSE: bbmagic.lookup.Environment

#### Construtor

````text
()
````

#### Métodos públicos (3)

##### get

**assinatura**

````text
"(self) -> str"
````

**doc**

````text
null
````

##### is_modeling

**assinatura**

````text
"(self) -> bool"
````

**doc**

````text
null
````

##### is_prodution

**assinatura**

````text
"(self) -> bool"
````

**doc**

````text
null
````

### CLASSE: bbmagic.lookup.Lookup

#### Construtor

````text
()
````

#### Métodos públicos (2)

##### migration_cluster

**assinatura**

````text
"(self, cluster: str = 'CDP') -> str"
````

**doc**

````text
null
````

##### sigla

**assinatura**

````text
"(self) -> str"
````

**doc**

````text
null
````

### CLASSE: bbmagic.lookup.SiglaAPI

#### Construtor

````text
(timeout=10)
````

#### Métodos públicos (1)

##### get

**assinatura**

````text
"(self, sigla: str) -> dict"
````

**doc**

````text
"Faz uma requisição GET à API passando a sigla como parâmetro.\nRetorna os dados em JSON ou None se houver erro."
````

### CLASSE: bbmagic.sas.AuthInfo

#### Construtor

````text
()
````

#### Métodos públicos (4)

##### add_key

**assinatura**

````text
"(self, name: str, user: str, password: Optional[str] = None) -> None"
````

**doc**

````text
null
````

##### parse

**assinatura**

````text
"(self) -> list"
````

**doc**

````text
null
````

##### remove_key

**assinatura**

````text
"(self, name: str) -> None"
````

**doc**

````text
null
````

##### write

**assinatura**

````text
"(self) -> None"
````

**doc**

````text
null
````

### CLASSE: bbmagic.sas.AuthKey

#### Construtor

````text
(name: str, user: str, password: Optional[str] = None) -> None
````

#### Métodos públicos (0)

````json
{}
````

### CLASSE: bbmagic.sas.SAS

#### Construtor

````text
(username: str = '', host: str = 'sasanl03.intranet.bb.com.br', port: int = 8591, appserver: str = 'SASApp_ANL03 - Workspace Server', authkey: str = '', libnames: Optional[List[dict]] = None, timeout: int = 30) -> None
````

#### Métodos públicos (3)

##### config_authinfo

**assinatura**

````text
"(self, name: str = 'bbmagic') -> None"
````

**doc**

````text
null
````

##### create_libnames

**assinatura**

````text
"(self) -> None"
````

**doc**

````text
null
````

##### query

**assinatura**

````text
"(self, sql: str, chunksize: Optional[int] = 2500, verbose: bool = False) -> Union[pandas.core.frame.DataFrame, Iterator[pandas.core.frame.DataFrame]]"
````

**doc**

````text
null
````

### CLASSE: bbmagic.sas.SASProcedureError

#### Construtor

````text
None
````

#### Doc

````text
Common base class for all non-exit exceptions.
````

#### Métodos públicos (1)

##### with_traceback

**assinatura**

````text
null
````

**doc**

````text
"Exception.with_traceback(tb) --\nset self.traceback to tb and return self."
````

### CLASSE: bbmagic.sas.authinfo.AuthInfo

#### Construtor

````text
()
````

#### Métodos públicos (4)

##### add_key

**assinatura**

````text
"(self, name: str, user: str, password: Optional[str] = None) -> None"
````

**doc**

````text
null
````

##### parse

**assinatura**

````text
"(self) -> list"
````

**doc**

````text
null
````

##### remove_key

**assinatura**

````text
"(self, name: str) -> None"
````

**doc**

````text
null
````

##### write

**assinatura**

````text
"(self) -> None"
````

**doc**

````text
null
````

### CLASSE: bbmagic.sas.authinfo.AuthKey

#### Construtor

````text
(name: str, user: str, password: Optional[str] = None) -> None
````

#### Métodos públicos (0)

````json
{}
````

### CLASSE: bbmagic.sas.sas.AuthInfo

#### Construtor

````text
()
````

#### Métodos públicos (4)

##### add_key

**assinatura**

````text
"(self, name: str, user: str, password: Optional[str] = None) -> None"
````

**doc**

````text
null
````

##### parse

**assinatura**

````text
"(self) -> list"
````

**doc**

````text
null
````

##### remove_key

**assinatura**

````text
"(self, name: str) -> None"
````

**doc**

````text
null
````

##### write

**assinatura**

````text
"(self) -> None"
````

**doc**

````text
null
````

### CLASSE: bbmagic.sas.sas.SAS

#### Construtor

````text
(username: str = '', host: str = 'sasanl03.intranet.bb.com.br', port: int = 8591, appserver: str = 'SASApp_ANL03 - Workspace Server', authkey: str = '', libnames: Optional[List[dict]] = None, timeout: int = 30) -> None
````

#### Métodos públicos (3)

##### config_authinfo

**assinatura**

````text
"(self, name: str = 'bbmagic') -> None"
````

**doc**

````text
null
````

##### create_libnames

**assinatura**

````text
"(self) -> None"
````

**doc**

````text
null
````

##### query

**assinatura**

````text
"(self, sql: str, chunksize: Optional[int] = 2500, verbose: bool = False) -> Union[pandas.core.frame.DataFrame, Iterator[pandas.core.frame.DataFrame]]"
````

**doc**

````text
null
````

### CLASSE: bbmagic.sas.sas.SASProcedureError

#### Construtor

````text
None
````

#### Doc

````text
Common base class for all non-exit exceptions.
````

#### Métodos públicos (1)

##### with_traceback

**assinatura**

````text
null
````

**doc**

````text
"Exception.with_traceback(tb) --\nset self.traceback to tb and return self."
````

### CLASSE: bbmagic.sas.sas.SASServer

#### Construtor

````text
(host, port, appserver)
````

#### Doc

````text
SASServer(host, port, appserver)
````

#### Métodos públicos (2)

##### count

**assinatura**

````text
"(self, value, /)"
````

**doc**

````text
"Return number of occurrences of value."
````

##### index

**assinatura**

````text
"(self, value, start=0, stop=9223372036854775807, /)"
````

**doc**

````text
"Return first index of value.\n\nRaises ValueError if the value is not present."
````

### CLASSE: bbmagic.sigla_api.SiglaAPI

#### Construtor

````text
(timeout=10)
````

#### Métodos públicos (1)

##### get

**assinatura**

````text
"(self, sigla: str) -> dict"
````

**doc**

````text
"Faz uma requisição GET à API passando a sigla como parâmetro.\nRetorna os dados em JSON ou None se houver erro."
````

### CLASSE: bbmagic.spark.BoasPraticasWarning

#### Construtor

````text
None
````

#### Doc

````text
Base class for warnings about dubious runtime behavior.
````

#### Métodos públicos (1)

##### with_traceback

**assinatura**

````text
null
````

**doc**

````text
"Exception.with_traceback(tb) --\nset self.traceback to tb and return self."
````

### CLASSE: bbmagic.spark.Cluster

#### Construtor

````text
(config: Optional[bbmagic.file_config.FileConfig] = None) -> None
````

#### Métodos públicos (3)

##### exists

**assinatura**

````text
"(cluster: str, service: str)"
````

**doc**

````text
null
````

##### fix

**assinatura**

````text
"(cluster: str)"
````

**doc**

````text
null
````

##### list

**assinatura**

````text
"()"
````

**doc**

````text
null
````

### CLASSE: bbmagic.spark.Db2

#### Construtor

````text
(user: Optional[str] = None, password: Optional[str] = None, host: str = 'gwdb2.bb.com.br', port: int = 50100, database: str = 'BDB2P04', trust_env: bool = True, jars_path: Optional[str] = None, backoff_limit: int = 3600, pconnect: bool = True) -> None
````

#### Doc

````text
Cria uma conexão ao DB2
````

#### Métodos públicos (9)

##### connect

**assinatura**

````text
"(self) -> ibm_db_dbi.Connection"
````

**doc**

````text
"Cria a conexão JDBC com o servidor DB2."
````

##### describe

**assinatura**

````text
"(self, schema: str, table: str) -> IPython.core.display.HTML"
````

**doc**

````text
"Gera um relatório consolidado com os metadados da tabela existentes no catálogo\ndo DB2.\n\n:param schema: nome do schema\n:param table: nome da tabela\n\n:return: Retorna um objeto HTML com o relatório para exibição no Jupyter Notebook.\n:rtype: IPython.core.display.HTML"
````

##### get_cofre_credentials

**assinatura**

````text
"(self, project_id: str) -> dict"
````

**doc**

````text
"Recupera credenciais do cofre com base no project_id do projeto"
````

##### query

**assinatura**

````text
"(self, sql: str, params: Optional[list] = None, chunksize: Optional[int] = 2500) -> Union[pandas.core.frame.DataFrame, Iterator[pandas.core.frame.DataFrame]]"
````

**doc**

````text
"Retorna um DataFrame contendo o resultado da execução da query SQL.\n\n:param sql: query SQL para execução\n:param params: lista de parâmetros para utilização na query\n:param chunksize: Se especificado, retorna um iterador onde chunksize é a quantidade\n de linhas incluídas em cada chunk\n\n:return: Daframe ou Iterator[DataFrame]\n\nExemplos de Uso::\n\n >>> for chunk in db2.query("SELEC [...]"
````

##### set_conn_param

**assinatura**

````text
"(self, param_name, param_value: Union[str, int, NoneType]) -> Union[str, int]"
````

**doc**

````text
null
````

##### show_schemas

**assinatura**

````text
"(self) -> pandas.core.frame.DataFrame"
````

**doc**

````text
"Lista todos os schemas no database\n\n:return: Retorna um Pandas DataFrame contendo uma linha para cada schema encontrado.\n:rtype: pandas.core.api.DataFrame\n\nExemplo de uso::\n\n >>> db2.show_schemas()"
````

##### show_tables

**assinatura**

````text
"(self, schema: str) -> pandas.core.frame.DataFrame"
````

**doc**

````text
"Lista todas as tabelas e views de um schema.\n\n:param schema: nome do schema\n\n:return: Retorna um Pandas DataFrame contendo uma linha para cada tabela do schema\n e as informações schema, name e type nas respectivas colunas.\n:rtype: pandas.core.api.DataFrame\n\nExemplo de uso::\n\n >>> db2.show_tables("DB2MCI")"
````

##### syscolumns

**assinatura**

````text
"(self, schema: str, table: str) -> pandas.core.frame.DataFrame"
````

**doc**

````text
"Retorna metadados das colunas de uma tabela.\n\n:param schema: nome do schema\n:param table: nome da tabela\n\n:return: Retorna um Pandas DataFrame contendo as informações sobre as colunas da\n tabela de acordo com o catálogo syscat.syscolumns\n:rtype: pandas.core.api.DataFrame"
````

##### systabstats

**assinatura**

````text
"(self, schema: str, table: str) -> pandas.core.frame.DataFrame"
````

**doc**

````text
"Retorna metadados de uma tabela.\n\n:param schema: nome do schema\n:param table: nome da tabela\n\n:return: Retorna um Pandas DataFrame contendo as informações sobre a tabela\n existentes no catálogo syscat.systabstats\n:rtype: pandas.core.api.DataFrame"
````

### CLASSE: bbmagic.spark.Hdfs

#### Construtor

````text
(username: Optional[str] = None, hdp: Optional[int] = None, set_no_proxy: bool = True, cluster: Optional[str] = 'CDP', config: Optional[bbmagic.file_config.FileConfig] = None, **kwargs) -> None
````

#### Doc

````text
Permite acesso ao HDFS com autenticação via kerberos.
````

#### Documentação complementar

````text
:param username: matrícula ou caminho para arquivo keytab :param hdp: Cluster HDP para conexão utilizar: 3 para HDP 3.1 our 2 para HDP 2.6 :param cluster: Identifica o cluster que deve receber a conexao - hdp ou cdp :param **kwargs: Argumentos [...]
````

#### Métodos públicos (30)

##### acl_status

**assinatura**

````text
"(self, hdfs_path, strict=True)"
````

**doc**

````text
"Get AclStatus_ for a file or folder on HDFS.\n\n:param hdfs_path: Remote path.\n:param strict: If False, return None rather than raise an exception if\n the path doesn't exist.\n\n.. AclStatus: https://hadoop.apache.org/docs/stable2/hadoop-project-dist/hadoop-hdfs/WebHDFS.html#Get_ACL_Status"
````

##### allow_snapshot

**assinatura**

````text
"(self, hdfs_path)"
````

**doc**

````text
"Allow snapshots for a remote folder.\n\n:param hdfs_path: Remote path to a directory. If hdfs_path\n doesn't exist or does points to a normal file, an\n :class:HdfsError will be raised. No-op if snapshotting is\n already allowed."
````

##### checksum

**assinatura**

````text
"(self, hdfs_path)"
````

**doc**

````text
"Get a remote file's checksum.\n\n:param hdfs_path: Remote path. Must point to a file."
````

##### content

**assinatura**

````text
"(self, hdfs_path, strict=True)"
````

**doc**

````text
"Get ContentSummary for a file or folder on HDFS.\n\n:param hdfs_path: Remote path.\n:param strict: If False, return None rather than raise an exception if\n the path doesn't exist.\n\n.. ContentSummary: CS\n.. CS: http://hadoop.apache.org/docs/r1.0.4/webhdfs.html#ContentSummary"
````

##### create_snapshot

**assinatura**

````text
"(self, hdfs_path, snapshotname=None)"
````

**doc**

````text
"Create snapshot for a remote folder where it was allowed.\n\n:param hdfs_path: Remote path to a directory. If hdfs_path\n doesn't exist, doesn't allow to create snapshot or points to a\n normal file, an :class:HdfsError will be raised.\n:param snapshotname snapshot name; if absent, name is generated\n by the server.\n\nReturns a path to created snapshot."
````

##### delete

**assinatura**

````text
"(self, hdfs_path, recursive=False, skip_trash=True)"
````

**doc**

````text
"Remove a file or directory from HDFS.\n\n:param hdfs_path: HDFS path.\n:param recursive: Recursively delete files and directories. By default,\n this method will raise an :class:HdfsError if trying to delete a\n non-empty directory.\n:param skip_trash: When false, the deleted path will be moved to an\n appropriate trash folder rather than deleted. This requires Hadoop 2.9+\n and trash to be enabled [...]"
````

##### delete_snapshot

**assinatura**

````text
"(self, hdfs_path, snapshotname)"
````

**doc**

````text
"Remove snapshot for a remote folder where it was allowed.\n\n:param hdfs_path: Remote path to a directory. If hdfs_path doesn't exist\n or points to a normal file, an :class:HdfsError will be raised.\n:param snapshotname snapshot name; if it does not exist, an\n :class:HdfsError will be raised."
````

##### disallow_snapshot

**assinatura**

````text
"(self, hdfs_path)"
````

**doc**

````text
"Disallow snapshots for a remote folder.\n\n:param hdfs_path: Remote path to a directory. If hdfs_path\n doesn't exist, points to a normal file or there are some\n snapshots, an :class:HdfsError will be raised.\n\nNo-op if snapshotting is disallowed/never allowed."
````

##### download

**assinatura**

````text
"(self, hdfs_path, local_path, overwrite=False, n_threads=1, temp_dir=None, **kwargs)"
````

**doc**

````text
"Download a file or folder from HDFS and save it locally.\n\n:param hdfs_path: Path on HDFS of the file or folder to download. If a\n folder, all the files under it will be downloaded.\n:param local_path: Local path. If it already exists and is a directory,\n the files will be downloaded inside of it.\n:param overwrite: Overwrite any existing file or directory.\n:param n_threads: Number of threads to us [...]"
````

##### from_options

**assinatura**

````text
"(options, class_name='Client')"
````

**doc**

````text
"Load client from options.\n\n:param options: Options dictionary.\n:param class_name: Client class name. Defaults to the base :class:Client\n class.\n\nThis method provides a single entry point to instantiate any registered\n:class:Client subclass. To register a subclass, simply load its\ncontaining module. If using the CLI, you can use the autoload.modules and\nautoload.paths options."
````

##### list

**assinatura**

````text
"(self, hdfs_path, status=False)"
````

**doc**

````text
"Return names of files contained in a remote folder.\n\n:param hdfs_path: Remote path to a directory. If hdfs_path doesn't exist\n or points to a normal file, an :class:HdfsError will be raised.\n:param status: Also return each file's corresponding FileStatus."
````

##### makedirs

**assinatura**

````text
"(self, hdfs_path, permission=None)"
````

**doc**

````text
"Create a remote directory, recursively if necessary.\n\n:param hdfs_path: Remote path. Intermediate directories will be created\n appropriately.\n:param permission: Octal permission to set on the newly created directory.\n These permissions will only be set on directories that do not already\n exist.\n\nThis function currently has no return value as WebHDFS doesn't return a\nmeaningful flag."
````

##### parts

**assinatura**

````text
"(self, hdfs_path, parts=None, status=False)"
````

**doc**

````text
"Returns a dictionary of part-files corresponding to a path.\n\n:param hdfs_path: Remote path. This directory should contain at most one\n part file per partition (otherwise one will be picked arbitrarily).\n:param parts: List of part-files numbers or total number of part-files to\n select. If a number, that many partitions will be chosen at random. By\n default all part-files are returned. If parts [...]"
````

##### read

**assinatura**

````text
"(self, hdfs_path, offset=0, length=None, buffer_size=None, encoding=None, chunk_size=0, delimiter=None, progress=None)"
````

**doc**

````text
"Read a file from HDFS.\n\n:param hdfs_path: HDFS path.\n:param offset: Starting byte position.\n:param length: Number of bytes to be processed. None will read the entire\n file.\n:param buffer_size: Size of the buffer in bytes used for transferring the\n data. Defaults the the value set in the HDFS configuration.\n:param encoding: Encoding used to decode the request. By default the raw\n data is retur [...]"
````

##### remove_acl

**assinatura**

````text
"(self, hdfs_path)"
````

**doc**

````text
"RemoveAcl_ for a file or folder on HDFS.\n\n:param hdfs_path: Path to an existing remote file or directory. An\n :class:HdfsError will be raised if the path doesn't exist.\n\n.. RemoveAcl: https://hadoop.apache.org/docs/stable2/hadoop-project-dist/hadoop-hdfs/WebHDFS.html#Remove_ACL"
````

##### remove_acl_entries

**assinatura**

````text
"(self, hdfs_path, acl_spec)"
````

**doc**

````text
"RemoveAclEntries for a file or folder on HDFS.\n\n:param hdfs_path: Path to an existing remote file or directory. An\n :class:HdfsError will be raised if the path doesn't exist.\n:param acl_spec: String representation of an ACL spec. Must be a valid\n string with entries for user, group and other. For example:\n \"user::rwx,user:foo:rw-,group::r--,other::---\".\n\n.. RemoveAclEntries: https://hadoo [...]"
````

##### remove_default_acl

**assinatura**

````text
"(self, hdfs_path)"
````

**doc**

````text
"RemoveDefaultAcl for a file or folder on HDFS.\n\n:param hdfs_path: Path to an existing remote file or directory. An\n :class:HdfsError will be raised if the path doesn't exist.\n\n.. RemoveDefaultAcl: https://hadoop.apache.org/docs/stable2/hadoop-project-dist/hadoop-hdfs/WebHDFS.html#Remove_Default_ACL"
````

##### rename

**assinatura**

````text
"(self, hdfs_src_path, hdfs_dst_path)"
````

**doc**

````text
"Move a file or folder.\n\n:param hdfs_src_path: Source path.\n:param hdfs_dst_path: Destination path. If the path already exists and is\n a directory, the source will be moved into it. If the path exists and is\n a file, or if a parent destination directory is missing, this method will\n raise an :class:HdfsError."
````

##### rename_snapshot

**assinatura**

````text
"(self, hdfs_path, oldsnapshotname, snapshotname)"
````

**doc**

````text
"Rename snapshot for a remote folder.\n\n:param hdfs_path: Remote path to a directory. If hdfs_path doesn't exist\n or points to a normal file, an :class:HdfsError will be raised.\n:param oldsnapshotname snapshot name; if it does not exist,\n an :class:HdfsError will be raised.\n:param snapshotname new snapshot name; if it does already exist,\n an :class:HdfsError will be raised."
````

##### resolve

**assinatura**

````text
"(self, hdfs_path)"
````

**doc**

````text
"Return absolute, normalized path, with special markers expanded.\n\n:param hdfs_path: Remote path.\n\nCurrently supported markers:\n\n* '#LATEST': this marker gets expanded to the most recently updated file\n or folder. They can be combined using the '{N}' suffix. For example,\n 'foo/#LATEST{2}' is equivalent to 'foo/#LATEST/#LATEST'."
````

##### set_acl

**assinatura**

````text
"(self, hdfs_path, acl_spec, clear=True)"
````

**doc**

````text
"SetAcl or ModifyAcl_ for a file or folder on HDFS.\n\n:param hdfs_path: Path to an existing remote file or directory. An\n :class:HdfsError will be raised if the path doesn't exist.\n:param acl_spec: String representation of an ACL spec. Must be a valid\n string with entries for user, group and other. For example:\n \"user::rwx,user:foo:rw-,group::r--,other::---\".\n:param clear: Clear existing ACL [...]"
````

##### set_no_proxy

**assinatura**

````text
"(self) -> None"
````

**doc**

````text
"Garante que a variável no_proxy está configurada para ignorar o domínio\nda API web da BBMagic"
````

##### set_owner

**assinatura**

````text
"(self, hdfs_path, owner=None, group=None)"
````

**doc**

````text
"Change the owner of file.\n\n:param hdfs_path: HDFS path.\n:param owner: Optional, new owner for file.\n:param group: Optional, new group for file.\n\nAt least one of owner and group must be specified."
````

##### set_permission

**assinatura**

````text
"(self, hdfs_path, permission)"
````

**doc**

````text
"Change the permissions of file.\n\n:param hdfs_path: HDFS path.\n:param permission: New octal permissions string of file."
````

##### set_replication

**assinatura**

````text
"(self, hdfs_path, replication)"
````

**doc**

````text
"Set file replication.\n\n:param hdfs_path: Path to an existing remote file. An :class:HdfsError\n will be raised if the path doesn't exist or points to a directory.\n:param replication: Replication factor."
````

##### set_times

**assinatura**

````text
"(self, hdfs_path, access_time=None, modification_time=None)"
````

**doc**

````text
"Change remote timestamps.\n\n:param hdfs_path: HDFS path.\n:param access_time: Timestamp of last file access.\n:param modification_time: Timestamps of last file access."
````

##### status

**assinatura**

````text
"(self, hdfs_path, strict=True)"
````

**doc**

````text
"Get FileStatus_ for a file or folder on HDFS.\n\n:param hdfs_path: Remote path.\n:param strict: If False, return None rather than raise an exception if\n the path doesn't exist.\n\n.. FileStatus: FS\n.. FS: http://hadoop.apache.org/docs/r1.0.4/webhdfs.html#FileStatus"
````

##### upload

**assinatura**

````text
"(self, hdfs_path, local_path, n_threads=1, temp_dir=None, chunk_size=65536, progress=None, cleanup=True, **kwargs)"
````

**doc**

````text
"Upload a file or directory to HDFS.\n\n:param hdfs_path: Target HDFS path. If it already exists and is a\n directory, files will be uploaded inside.\n:param local_path: Local path to file or folder. If a folder, all the files\n inside of it will be uploaded (note that this implies that folders empty\n of files will not be created remotely).\n:param n_threads: Number of threads to use for parallelizati [...]"
````

##### walk

**assinatura**

````text
"(self, hdfs_path, depth=0, status=False, ignore_missing=False, allow_dir_changes=False)"
````

**doc**

````text
"Depth-first walk of remote filesystem.\n\n:param hdfs_path: Starting path. If the path doesn't exist, an\n :class:HdfsError will be raised. If it points to a file, the returned\n generator will be empty.\n:param depth: Maximum depth to explore. 0 for no limit.\n:param status: Also return each file or folder's corresponding FileStatus.\n:param ignore_missing: Ignore missing nested folders rather th [...]"
````

##### write

**assinatura**

````text
"(self, hdfs_path, data=None, overwrite=False, permission=None, blocksize=None, replication=None, buffersize=None, append=False, encoding=None)"
````

**doc**

````text
"Create a file on HDFS.\n\n:param hdfs_path: Path where to create file. The necessary directories will\n be created appropriately.\n:param data: Contents of file to write. Can be a string, a generator or a\n file object. The last two options will allow streaming upload (i.e.\n without having to load the entire contents into memory). If None, this\n method will return a file-like object and should be [...]"
````

### CLASSE: bbmagic.spark.Kinit

#### Construtor

````text
(username: Optional[str] = None, conf_file: Optional[str] = None, cluster: str = 'CDP', backoff_limit: int = 3600, hdp: Optional[int] = None) -> None
````

#### Doc

````text
Autentica o usuário no Kerberos utilizando kinit.
````

#### Documentação complementar

````text
:param username: matrícula ou caminho para arquivo keytab :param conf_file: caminho para o arquivo krb5.conf. Caso não seja informado será utilizada configuração do arquivo temporátio gerado pelo pacote :param hdp: Parâmetro depr [...]
````

#### Métodos públicos (6)

##### get_ticket

**assinatura**

````text
"(self) -> str"
````

**doc**

````text
"Autentica no Kerberos utilizando Kinit.\n\nVerifica se o usuário já possui um ticket kerberos válido. Caso não encontre\nrealiza a autenticação com kinit. O parâmetro informado pode ser a matrícula\ndo usuário ou uma keytab.\n\nCaso a matrícula seja informada, um prompt será exibido para que a senha SISBB\nseja informada.\n\nCaso o caminho para uma keytab seja informada, utiliza o arquivo. Caso seja inform [...]"
````

##### get_username

**assinatura**

````text
"(self, username: Optional[str]) -> str"
````

**doc**

````text
null
````

##### is_matricula

**assinatura**

````text
"(self, string: str) -> bool"
````

**doc**

````text
null
````

##### raise_keytab_on_modelagem

**assinatura**

````text
"(self) -> None"
````

**doc**

````text
null
````

##### run_kinit_cmd

**assinatura**

````text
"(self, kinit_cmd: list, password: Optional[str]) -> int"
````

**doc**

````text
null
````

##### user_has_ticket

**assinatura**

````text
"(self) -> bool"
````

**doc**

````text
"Verifica se há um ticket válido no cache de credenciais do Kerberos.\n\nVerifica as credenciais no cache padrão ou no caminho indicado na\nvariável de ambiente KRB5CCNAME."
````

### CLASSE: bbmagic.spark.LivyApi

#### Construtor

````text
(username: str, cluster: str = 'CDP', spark_version: int = 3, config: Optional[bbmagic.file_config.FileConfig] = None, python: Optional[int] = None) -> None
````

#### Doc

````text
A client for sending requests to a Livy server.
````

#### Documentação complementar

````text
:param url: The URL of the Livy server. :param auth: A requests-compatible auth object to use when making requests. :param verify: Either a boolean, in which case it controls whether we verify the server’s TLS certificate, or a string, in which ca [...]
````

#### Métodos públicos (15)

##### close

**assinatura**

````text
"(self) -> None"
````

**doc**

````text
"Close the underlying requests session, if managed by this class."
````

##### create_batch

**assinatura**

````text
"(self, file: str, class_name: str = None, args: List[str] = None, proxy_user: str = None, jars: List[str] = None, py_files: List[str] = None, files: List[str] = None, driver_memory: str = None, driver_cores: int = None, executor_memory: str = None, executor_cores: int = None, num_executors: int = None, archives: List[str] = None, queue: str = None, name: str = None, spark_conf: Dict[str, Any] = None) -> livy.models.Batch"
````

**doc**

````text
"Create a new batch in Livy.\n\nThe py_files, files, jars and archives arguments are lists of URLs,\ne.g. ["s3://bucket/object", "hdfs://path/to/file", ...] and must be\nreachable by the Spark driver process. If the provided URL has no\nscheme, it's considered to be relative to the default file system\nconfigured in the Livy server.\n\nURLs in the py_files argument are copied to a temporary staging area\na [...]"
````

##### create_session

**assinatura**

````text
"(self, kind: livy.models.SessionKind, proxy_user: str = None, jars: List[str] = None, py_files: List[str] = None, files: List[str] = None, driver_memory: str = None, driver_cores: int = None, executor_memory: str = None, executor_cores: int = None, num_executors: int = None, archives: List[str] = None, queue: str = None, name: str = None, spark_conf: Dict[str, Any] = None, heartbeat_timeout: int = None) -> livy.models.Session"
````

**doc**

````text
"Create a new session in Livy.\n\nThe py_files, files, jars and archives arguments are lists of URLs,\ne.g. ["s3://bucket/object", "hdfs://path/to/file", ...] and must be\nreachable by the Spark driver process. If the provided URL has no\nscheme, it's considered to be relative to the default file system\nconfigured in the Livy server.\n\nURLs in the py_files argument are copied to a temporary staging area [...]"
````

##### create_statement

**assinatura**

````text
"(self, session_id: int, code: str, kind: livy.models.StatementKind = None) -> livy.models.Statement"
````

**doc**

````text
"Run a statement in a session.\n\n:param session_id: The ID of the session.\n:param code: The code to execute.\n:param kind: The kind of code to execute."
````

##### delete_batch

**assinatura**

````text
"(self, batch_id: int) -> None"
````

**doc**

````text
"Kill a batch session.\n\n:param batch_id: The ID of the session."
````

##### delete_session

**assinatura**

````text
"(self, session_id: int) -> None"
````

**doc**

````text
"Kill a session.\n\n:param session_id: The ID of the session."
````

##### get_batch

**assinatura**

````text
"(self, batch_id: int) -> Optional[livy.models.Batch]"
````

**doc**

````text
"Get information about a batch.\n\n:param batch_id: The ID of the batch."
````

##### get_batch_log

**assinatura**

````text
"(self, batch_id: int, from_: int = None, size: int = None) -> Optional[livy.models.BatchLog]"
````

**doc**

````text
"Get logs for a batch.\n\n:param batch_id: The ID of the batch.\n:param from_: The line number to start getting logs from.\n:param size: The number of lines of logs to get."
````

##### get_session

**assinatura**

````text
"(self, session_id: int) -> Optional[livy.models.Session]"
````

**doc**

````text
"Get information about a session.\n\n:param session_id: The ID of the session."
````

##### get_statement

**assinatura**

````text
"(self, session_id: int, statement_id: int) -> livy.models.Statement"
````

**doc**

````text
"Get information about a statement in a session.\n\n:param session_id: The ID of the session.\n:param statement_id: The ID of the statement."
````

##### legacy_server

**assinatura**

````text
"(self) -> bool"
````

**doc**

````text
"Determine if the server is running a legacy version.\n\nLegacy versions support different session kinds than newer versions of\nLivy."
````

##### list_batches

**assinatura**

````text
"(self) -> List[livy.models.Batch]"
````

**doc**

````text
"List all the active batches in Livy."
````

##### list_sessions

**assinatura**

````text
"(self) -> List[livy.models.Session]"
````

**doc**

````text
"List all the active sessions in Livy."
````

##### list_statements

**assinatura**

````text
"(self, session_id: int) -> List[livy.models.Statement]"
````

**doc**

````text
"Get all the statements in a session.\n\n:param session_id: The ID of the session."
````

##### server_version

**assinatura**

````text
"(self) -> livy.models.Version"
````

**doc**

````text
"Get the version of Livy running on the server."
````

### CLASSE: bbmagic.spark.Lookup

#### Construtor

````text
()
````

#### Métodos públicos (2)

##### migration_cluster

**assinatura**

````text
"(self, cluster: str = 'CDP') -> str"
````

**doc**

````text
null
````

##### sigla

**assinatura**

````text
"(self) -> str"
````

**doc**

````text
null
````

### CLASSE: bbmagic.spark.PythonVersion

#### Construtor

````text
()
````

#### Métodos públicos (0)

````json
{}
````

### CLASSE: bbmagic.spark.Spark

#### Construtor

````text
(session_name: str, username: Optional[str] = None, language: str = 'python', auth: str = 'Kerberos', timeout: int = 900, db2: bool = False, spark_conf: Optional[dict] = None, jars: Optional[list] = None, archives: Optional[list] = None, pyfiles: Optional[list] = None, files: Optional[list] = None, python: Optional[int] = None, env: Optional[dict] = None, debug: bool = False, driver_memory: str = '8g', driver_cores: int = 4, num_executors: int = 4, executor_memory: str = '2g', executor_cores: int = 4, virtualenv: Optional[str] = None, overwrite_virtualenv: bool = False, cluster: str = 'CDP', spark_version: int = 3)
````

#### Doc

````text
Cria uma sessão Spark.
````

#### Documentação complementar

````text
:param session_name: nome da sessão que será exibido na Web UI do Spark :param username: caminho para arquivo .keytab ou matrícula sem o dígito do usuário :param python: versão do Python da sessão Spark (2 ou 3) :param language: linguagem utilizada na sessão Spark ('python' o [...]
````

#### Métodos públicos (10)

##### close

**assinatura**

````text
"(self) -> None"
````

**doc**

````text
"Encerra a sessão Spark"
````

##### config_db2

**assinatura**

````text
"(self) -> None"
````

**doc**

````text
null
````

##### config_jars

**assinatura**

````text
"(self) -> None"
````

**doc**

````text
"Adiciona os jars para utilização de bibliotecas de machine learning distribuidas nas sessões spark 3"
````

##### config_sparkmagic

**assinatura**

````text
"(self) -> None"
````

**doc**

````text
null
````

##### config_virtualenv

**assinatura**

````text
"(self, virtualenv: Optional[str], overwrite: bool = False) -> Optional[str]"
````

**doc**

````text
null
````

##### connect

**assinatura**

````text
"(self) -> None"
````

**doc**

````text
null
````

##### enforce_dynamic_allocation

**assinatura**

````text
"(self, config: Optional[Dict[str, str]]) -> Optional[dict]"
````

**doc**

````text
null
````

##### get_from_spark

**assinatura**

````text
"(self, var_name: str)"
````

**doc**

````text
"Importa o conteúdo de uma variável da sessão Spark para a sessão local.\n\n\n:param var_name: nome da variável que será importada.\n\n:return: Retorna o valor da variável"
````

##### list_livy_sessions

**assinatura**

````text
"(cluster: str, spark_version: int, username: Optional[str] = None, python: int = 39) -> list"
````

**doc**

````text
null
````

##### send_to_spark

**assinatura**

````text
"(self, var) -> None"
````

**doc**

````text
"Envia uma variável local para a sessão Spark.\n\nA variável será definida com mesmo nome na sessão Spark e o valor\nserá transmitido utilizando pickle.\n\n:param var: variável que será enviada para a sessão Spark.\n\n:return: None"
````

### CLASSE: bbmagic.sumary.MetaDataHive

#### Construtor

````text
() -> None
````

#### Métodos públicos (4)

##### get_token

**assinatura**

````text
"(self) -> Optional[str]"
````

**doc**

````text
null
````

##### get_url

**assinatura**

````text
"(self) -> Optional[str]"
````

**doc**

````text
null
````

##### status_db

**assinatura**

````text
"(self, db: str, list: Optional[bool] = False) -> Optional[pandas.core.frame.DataFrame]"
````

**doc**

````text
null
````

##### status_table

**assinatura**

````text
"(self, nome_db: Optional[str] = None, nome_tabela: Optional[str] = None) -> Optional[pandas.core.frame.DataFrame]"
````

**doc**

````text
null
````

### CLASSE: bbmagic.teams_notify.TeamsNotify

#### Construtor

````text
(webhook: str)
````

#### Métodos públicos (5)

##### error

**assinatura**

````text
"(self, title, text, model='', situation='', other_details='', color='E81123')"
````

**doc**

````text
null
````

##### info

**assinatura**

````text
"(self, title, text, model='', situation='', other_details='', color='008000')"
````

**doc**

````text
null
````

##### post_msg

**assinatura**

````text
"(self, title, text, model, situation, other_details, color=None)"
````

**doc**

````text
null
````

##### post_msg_workflows

**assinatura**

````text
"(self, title: str, text: str, model: str = '', situation: str = '', other_details: str = '', type: str = '') -> dict"
````

**doc**

````text
"Função que envia mensagens por meio dos fluxos Workflows no Microsoft Teams"
````

##### warning

**assinatura**

````text
"(self, title, text, model='', situation='', other_details='', color='FFFF00')"
````

**doc**

````text
null
````

## 5) RECURSOS DE CATÁLOGO / METADADOS (foco DB2)

Métodos de metadados/catálogo detectados automaticamente:

### bbmagic.db2.Db2

#### describe

**assinatura**

````text
"(self, schema: str, table: str) -> IPython.core.display.HTML"
````

**doc**

````text
"Gera um relatório consolidado com os metadados da tabela existentes no catálogo\ndo DB2.\n\n:param schema: nome do schema\n:param table: nome da tabela\n\n:return: Retorna um objeto HTML com o relatório para exibição no Jupyter Notebook.\n:rtype: IPython.core.display.HTML"
````

#### show_schemas

**assinatura**

````text
"(self) -> pandas.core.frame.DataFrame"
````

**doc**

````text
"Lista todos os schemas no database\n\n:return: Retorna um Pandas DataFrame contendo uma linha para cada schema encontrado.\n:rtype: pandas.core.api.DataFrame\n\nExemplo de uso::\n\n >>> db2.show_schemas()"
````

#### show_tables

**assinatura**

````text
"(self, schema: str) -> pandas.core.frame.DataFrame"
````

**doc**

````text
"Lista todas as tabelas e views de um schema.\n\n:param schema: nome do schema\n\n:return: Retorna um Pandas DataFrame contendo uma linha para cada tabela do schema\n e as informações schema, name e type nas respectivas colunas.\n:rtype: pandas.core.api.DataFrame\n\nExemplo de uso::\n\n >>> db2.show_tables("DB2MCI")"
````

#### syscolumns

**assinatura**

````text
"(self, schema: str, table: str) -> pandas.core.frame.DataFrame"
````

**doc**

````text
"Retorna metadados das colunas de uma tabela.\n\n:param schema: nome do schema\n:param table: nome da tabela\n\n:return: Retorna um Pandas DataFrame contendo as informações sobre as colunas da\n tabela de acordo com o catálogo syscat.syscolumns\n:rtype: pandas.core.api.DataFrame"
````

#### systabstats

**assinatura**

````text
"(self, schema: str, table: str) -> pandas.core.frame.DataFrame"
````

**doc**

````text
"Retorna metadados de uma tabela.\n\n:param schema: nome do schema\n:param table: nome da tabela\n\n:return: Retorna um Pandas DataFrame contendo as informações sobre a tabela\n existentes no catálogo syscat.systabstats\n:rtype: pandas.core.api.DataFrame"
````

### bbmagic.hdfs.Hdfs

#### acl_status

**assinatura**

````text
"(self, hdfs_path, strict=True)"
````

**doc**

````text
"Get AclStatus_ for a file or folder on HDFS.\n\n:param hdfs_path: Remote path.\n:param strict: If False, return None rather than raise an exception if\n the path doesn't exist.\n\n.. AclStatus: https://hadoop.apache.org/docs/stable2/hadoop-project-dist/hadoop-hdfs/WebHDFS.html#Get_ACL_Status"
````

#### status

**assinatura**

````text
"(self, hdfs_path, strict=True)"
````

**doc**

````text
"Get FileStatus for a file or folder on HDFS.\n\n:param hdfs_path: Remote path.\n:param strict: If False, return None rather than raise an exception if\n the path doesn't exist.\n\n.. FileStatus: FS\n.. FS: http://hadoop.apache.org/docs/r1.0.4/webhdfs.html#FileStatus"
````

### bbmagic.livyapi.LivyApi

#### create_statement

**assinatura**

````text
"(self, session_id: int, code: str, kind: livy.models.StatementKind = None) -> livy.models.Statement"
````

**doc**

````text
"Run a statement in a session.\n\n:param session_id: The ID of the session.\n:param code: The code to execute.\n:param kind: The kind of code to execute."
````

#### get_statement

**assinatura**

````text
"(self, session_id: int, statement_id: int) -> livy.models.Statement"
````

**doc**

````text
"Get information about a statement in a session.\n\n:param session_id: The ID of the session.\n:param statement_id: The ID of the statement."
````

#### list_statements

**assinatura**

````text
"(self, session_id: int) -> List[livy.models.Statement]"
````

**doc**

````text
"Get all the statements in a session.\n\n:param session_id: The ID of the session."
````

### bbmagic.spark.Db2

#### describe

**assinatura**

````text
"(self, schema: str, table: str) -> IPython.core.display.HTML"
````

**doc**

````text
"Gera um relatório consolidado com os metadados da tabela existentes no catálogo\ndo DB2.\n\n:param schema: nome do schema\n:param table: nome da tabela\n\n:return: Retorna um objeto HTML com o relatório para exibição no Jupyter Notebook.\n:rtype: IPython.core.display.HTML"
````

#### show_schemas

**assinatura**

````text
"(self) -> pandas.core.frame.DataFrame"
````

**doc**

````text
"Lista todos os schemas no database\n\n:return: Retorna um Pandas DataFrame contendo uma linha para cada schema encontrado.\n:rtype: pandas.core.api.DataFrame\n\nExemplo de uso::\n\n >>> db2.show_schemas()"
````

#### show_tables

**assinatura**

````text
"(self, schema: str) -> pandas.core.frame.DataFrame"
````

**doc**

````text
"Lista todas as tabelas e views de um schema.\n\n:param schema: nome do schema\n\n:return: Retorna um Pandas DataFrame contendo uma linha para cada tabela do schema\n e as informações schema, name e type nas respectivas colunas.\n:rtype: pandas.core.api.DataFrame\n\nExemplo de uso::\n\n >>> db2.show_tables("DB2MCI")"
````

#### syscolumns

**assinatura**

````text
"(self, schema: str, table: str) -> pandas.core.frame.DataFrame"
````

**doc**

````text
"Retorna metadados das colunas de uma tabela.\n\n:param schema: nome do schema\n:param table: nome da tabela\n\n:return: Retorna um Pandas DataFrame contendo as informações sobre as colunas da\n tabela de acordo com o catálogo syscat.syscolumns\n:rtype: pandas.core.api.DataFrame"
````

#### systabstats

**assinatura**

````text
"(self, schema: str, table: str) -> pandas.core.frame.DataFrame"
````

**doc**

````text
"Retorna metadados de uma tabela.\n\n:param schema: nome do schema\n:param table: nome da tabela\n\n:return: Retorna um Pandas DataFrame contendo as informações sobre a tabela\n existentes no catálogo syscat.systabstats\n:rtype: pandas.core.api.DataFrame"
````

### bbmagic.spark.Hdfs

#### acl_status

**assinatura**

````text
"(self, hdfs_path, strict=True)"
````

**doc**

````text
"Get AclStatus for a file or folder on HDFS.\n\n:param hdfs_path: Remote path.\n:param strict: If False, return None rather than raise an exception if\n the path doesn't exist.\n\n.. AclStatus: https://hadoop.apache.org/docs/stable2/hadoop-project-dist/hadoop-hdfs/WebHDFS.html#Get_ACL_Status"
````

#### status

**assinatura**

````text
"(self, hdfs_path, strict=True)"
````

**doc**

````text
"Get FileStatus for a file or folder on HDFS.\n\n:param hdfs_path: Remote path.\n:param strict: If False, return None rather than raise an exception if\n the path doesn't exist.\n\n.. FileStatus: FS\n.. _FS: http://hadoop.apache.org/docs/r1.0.4/webhdfs.html#FileStatus"
````

### bbmagic.spark.LivyApi

#### create_statement

**assinatura**

````text
"(self, session_id: int, code: str, kind: livy.models.StatementKind = None) -> livy.models.Statement"
````

**doc**

````text
"Run a statement in a session.\n\n:param session_id: The ID of the session.\n:param code: The code to execute.\n:param kind: The kind of code to execute."
````

#### get_statement

**assinatura**

````text
"(self, session_id: int, statement_id: int) -> livy.models.Statement"
````

**doc**

````text
"Get information about a statement in a session.\n\n:param session_id: The ID of the session.\n:param statement_id: The ID of the statement."
````

#### list_statements

**assinatura**

````text
"(self, session_id: int) -> List[livy.models.Statement]"
````

**doc**

````text
"Get all the statements in a session.\n\n:param session_id: The ID of the session."
````

### bbmagic.sumary.MetaDataHive

#### status_db

**assinatura**

````text
"(self, db: str, list: Optional[bool] = False) -> Optional[pandas.core.frame.DataFrame]"
````

**doc**

````text
null
````

#### status_table

**assinatura**

````text
"(self, nome_db: Optional[str] = None, nome_tabela: Optional[str] = None) -> Optional[pandas.core.frame.DataFrame]"
````

**doc**

````text
null
````

### Sugestão de uso (usuário impessoal + cofre) para o schema DB2GFP:

````python
from bbmagic.db2 import Db2 from bbmagic.common import get_project_id
cred = Db2().get_cofre_credentials(get_project_id(raise_not_found=True)) print("chaves do cofre:", list(cred.keys())) # confirmar nomes reais
db2 = Db2(user=cred["user"], password=cred["password"]) df = db2.show_tables("DB2GFP") print(df.to_json(orient="records", force_ascii=False, indent=2)) print("Total de objetos em DB2GFP:", len(df))
````

## 6) RESUMO FINAL CONSOLIDADO

````json
{
  "versao": "3.1.7",
  "qtd_modulos": 26,
  "qtd_objetos_raiz": 37,
  "qtd_classes_bbmagic": 53,
  "classes": {
    "bbmagic.checks.BoasPraticasWarning": 1,
    "bbmagic.cluster.Cluster": 3,
    "bbmagic.cluster.FileConfig": 2,
    "bbmagic.cluster.HttpConfig": 3,
    "bbmagic.common.BoasPraticasWarning": 1,
    "bbmagic.db2.DB2Server": 2,
    "bbmagic.db2.Db2": 9,
    "bbmagic.environment.Environment": 3,
    "bbmagic.exceptions.KinitError": 1,
    "bbmagic.exceptions.PublicadorError": 1,
    "bbmagic.file_config.FileConfig": 2,
    "bbmagic.gitlab_config.FileConfig": 2,
    "bbmagic.gitlab_config.GitLabConfig": 2,
    "bbmagic.hdfs.Cluster": 3,
    "bbmagic.hdfs.FileConfig": 2,
    "bbmagic.hdfs.Hdfs": 30,
    "bbmagic.hdfs.HttpConfig": 3,
    "bbmagic.hdfs.Kinit": 6,
    "bbmagic.hdfs.Lookup": 2,
    "bbmagic.http_config.FileConfig": 2,
    "bbmagic.http_config.HttpConfig": 3,
    "bbmagic.kinit.Kinit": 6,
    "bbmagic.kinit.KinitError": 1,
    "bbmagic.livyapi.Cluster": 3,
    "bbmagic.livyapi.FileConfig": 2,
    "bbmagic.livyapi.HttpConfig": 3,
    "bbmagic.livyapi.Kinit": 6,
    "bbmagic.livyapi.LivyApi": 15,
    "bbmagic.lookup.Environment": 3,
    "bbmagic.lookup.Lookup": 2,
    "bbmagic.lookup.SiglaAPI": 1,
    "bbmagic.sas.AuthInfo": 4,
    "bbmagic.sas.AuthKey": 0,
    "bbmagic.sas.SAS": 3,
    "bbmagic.sas.SASProcedureError": 1,
    "bbmagic.sas.authinfo.AuthInfo": 4,
    "bbmagic.sas.authinfo.AuthKey": 0,
    "bbmagic.sas.sas.AuthInfo": 4,
    "bbmagic.sas.sas.SAS": 3,
    "bbmagic.sas.sas.SASProcedureError": 1,
    "bbmagic.sas.sas.SASServer": 2,
    "bbmagic.sigla_api.SiglaAPI": 1,
    "bbmagic.spark.BoasPraticasWarning": 1,
    "bbmagic.spark.Cluster": 3,
    "bbmagic.spark.Db2": 9,
    "bbmagic.spark.Hdfs": 30,
    "bbmagic.spark.Kinit": 6,
    "bbmagic.spark.LivyApi": 15,
    "bbmagic.spark.Lookup": 2,
    "bbmagic.spark.PythonVersion": 0,
    "bbmagic.spark.Spark": 10,
    "bbmagic.sumary.MetaDataHive": 4,
    "bbmagic.teams_notify.TeamsNotify": 5
  },
  "modulos_com_erro_import": [
    "bbmagic.publicador_modelo"
  ],
  "classes_com_recursos_catalogo": [
    "bbmagic.db2.Db2",
    "bbmagic.hdfs.Hdfs",
    "bbmagic.livyapi.LivyApi",
    "bbmagic.spark.Db2",
    "bbmagic.spark.Hdfs",
    "bbmagic.spark.LivyApi",
    "bbmagic.sumary.MetaDataHive"
  ]
}
````

✅ Estudo exploratório do BBMAGIC concluído.
