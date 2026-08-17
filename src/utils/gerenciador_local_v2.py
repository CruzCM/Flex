# ============================================================
# gerenciador_local_v2.py
# Módulo Local: Criação e orquestração de sessão Spark via BBMagic 3.1.7
# ============================================================

import os
import tempfile
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Optional, Tuple, Dict, Any, List, Union

try:
    from zoneinfo import ZoneInfo
except ImportError:
    ZoneInfo = None

from bbmagic import Spark

try:
    from dotenv import load_dotenv, dotenv_values
except Exception:
    load_dotenv = None
    dotenv_values = None

try:
    from IPython import get_ipython
except Exception:
    get_ipython = None

if ZoneInfo is None:
    FUSO_SAO_PAULO = timezone(timedelta(hours=-3), "America/Sao_Paulo")
else:
    try:
        FUSO_SAO_PAULO = ZoneInfo("America/Sao_Paulo")
    except Exception:
        FUSO_SAO_PAULO = timezone(timedelta(hours=-3), "America/Sao_Paulo")


def obter_variavel_ambiente_local(nome_variavel: str, obrigatoria: bool = True, padrao: Optional[str] = None) -> Optional[str]:
    """
    Obtém o valor de uma variável de ambiente local no container Python/Jupyter.
    """
    valor = os.environ.get(nome_variavel)
    if valor is None or not str(valor).strip():
        if obrigatoria:
            raise ValueError(f"Variável de ambiente local obrigatória não informada: '{nome_variavel}'")
        return padrao
    return str(valor).strip()


class GerenciadorLocal:
    """
    Gerenciador local corporativo para inicialização e parametrização de sessões Spark via BBMagic.
    
    Responsabilidades:
    - Carregar variáveis de arquivos .env (em ambiente MODELAGEM) e propagá-las ao cluster.
    - Resolver matrícula / KEYTAB e identificar dinamicamente a data de competência (CTMODATE).
    - Preparar e empacotar virtualenvs Python no HDFS para distribuição aos executores Spark.
    - Iniciar a sessão Livy/Spark com retries resilientes e configurações otimizadas.
    """

    def __init__(
        self,
        nome_sessao: str,
        adicionar_variaveis: Optional[Dict[str, Any]] = None,
        nome_arquivo_env_modelagem: Optional[str] = "desenv.env",
        exibir_configuracao: bool = False,
        ativar_logs: bool = True,
    ) -> None:
        self.nome_sessao = nome_sessao
        self.adicionar_variaveis = adicionar_variaveis or {}
        self.nome_arquivo_env_modelagem = nome_arquivo_env_modelagem
        self.exibir_configuracao = exibir_configuracao
        self.ativar_logs = ativar_logs
        self.spark = None

        self.ambiente: Optional[str] = None
        self.keytab: Optional[str] = None
        self.nome_sessao_final: Optional[str] = None
        self.variaveis_env_modelagem: Dict[str, str] = {}

    def _log(self, mensagem: str) -> None:
        if self.exibir_configuracao:
            print(f"[GERENCIADOR-LOCAL] {mensagem}")

    def _localizar_arquivo(self, nome_arquivo: str) -> Optional[str]:
        """
        Busca recursivamente um arquivo a partir do diretório atual até a raiz do workspace.
        """
        caminho_atual = Path.cwd()
        while True:
            caminho_encontrado = next(caminho_atual.rglob(nome_arquivo), None)
            if caminho_encontrado:
                return str(caminho_encontrado)
            if caminho_atual.parent == caminho_atual:
                return None
            caminho_atual = caminho_atual.parent

    def _carregar_env_modelagem(self) -> None:
        """
        Carrega as variáveis do arquivo .env quando executado em ambiente MODELAGEM.
        """
        ambiente = os.environ.get("AMBIENTE", "").strip().upper()
        if ambiente != "MODELAGEM" or not self.nome_arquivo_env_modelagem:
            return

        if load_dotenv is None or dotenv_values is None:
            raise ImportError("A biblioteca python-dotenv é necessária para carregar arquivos .env em MODELAGEM.")

        caminho_env = self._localizar_arquivo(self.nome_arquivo_env_modelagem)
        if not caminho_env:
            raise FileNotFoundError(f"Arquivo de ambiente de modelagem não encontrado: '{self.nome_arquivo_env_modelagem}'")

        load_dotenv(dotenv_path=caminho_env, override=True)
        self.variaveis_env_modelagem = {
            str(k): str(v)
            for k, v in dotenv_values(caminho_env).items()
            if v is not None and str(v).strip()
        }
        self._log(f"Arquivo de modelagem carregado: {caminho_env}")

    def _preparar_contexto_local(self) -> None:
        self._carregar_env_modelagem()
        self.ambiente = obter_variavel_ambiente_local("AMBIENTE").upper()
        self.keytab = obter_variavel_ambiente_local("KEYTAB")
        self.nome_sessao_final = f"spark_{self.keytab}_{self.nome_sessao}"

    def _garantir_contexto_local(self) -> None:
        if not self.ambiente or not self.keytab or not self.nome_sessao_final:
            self._preparar_contexto_local()

    def _limpar_sessao_spark_anterior(self) -> None:
        if get_ipython is None:
            return
        ipython = get_ipython()
        if ipython is not None:
            try:
                ipython.run_line_magic("spark", "cleanup")
            except Exception:
                pass

    def _obter_hoje(self) -> str:
        self._garantir_contexto_local()
        if self.ambiente == "MODELAGEM":
            return datetime.now(tz=FUSO_SAO_PAULO).strftime("%Y-%m-%d")
        
        valor = os.environ.get("ctmodate") or os.environ.get("CTMODATE")
        if valor is None or not str(valor).strip():
            raise ValueError("Variável de ambiente de data 'CTMODATE'/'ctmodate' não informada.")
        return str(valor).strip()

    def _montar_variaveis_spark(self) -> Dict[str, str]:
        self._garantir_contexto_local()
        variaveis_spark = {}

        for chave, valor in self.variaveis_env_modelagem.items():
            if valor is not None:
                variaveis_spark[str(chave)] = str(valor)

        variaveis_spark.update({
            "AMBIENTE": self.ambiente,
            "KEYTAB": self.keytab,
            "SESSION_NAME": self.nome_sessao_final,
            "USE_LOGS": str(self.ativar_logs),
            "HOJE": self._obter_hoje(),
        })

        for chave, valor in self.adicionar_variaveis.items():
            if valor is not None:
                variaveis_spark[str(chave)] = str(valor)

        return variaveis_spark

    def _montar_spark_conf(self, spark_conf: Optional[Dict[str, Any]]) -> Dict[str, str]:
        configuracao_spark = {
            "spark.sql.session.timeZone": "America/Sao_Paulo",
        }
        if not spark_conf:
            return configuracao_spark

        for chave, valor in spark_conf.items():
            if valor is None:
                continue
            if isinstance(valor, bool):
                configuracao_spark[str(chave)] = str(valor).lower()
            else:
                configuracao_spark[str(chave)] = str(valor)

        return configuracao_spark

    def _mascarar_sensivel(self, chave: str, valor: Any) -> str:
        chave_up = str(chave).upper()
        if any(p in chave_up for p in ["PASSWORD", "SENHA", "SECRET", "TOKEN", "KEY"]):
            return "***"
        return str(valor)

    def _exibir_argumentos_spark(self, argumentos: Dict[str, Any]) -> None:
        if not self.exibir_configuracao:
            return
        print("[CONFIGURAÇÃO DA SESSÃO SPARK]")
        for k, v in argumentos.items():
            if k == "env" and isinstance(v, dict):
                print("  env:")
                for env_k, env_v in sorted(v.items()):
                    print(f"    {env_k}: {self._mascarar_sensivel(env_k, env_v)}")
            else:
                print(f"  {k}: {v}")

    def _criar_com_retry(self, argumentos_spark: Dict[str, Any]) -> Spark:
        esperas = [0, 60, 120, 180]
        for tentativa, espera in enumerate(esperas, start=1):
            try:
                if espera > 0:
                    time.sleep(espera)
                self._log(f"Iniciando sessão Spark (Tentativa {tentativa}/{len(esperas)})...")
                return Spark(**argumentos_spark)
            except KeyboardInterrupt:
                raise
            except (ValueError, TypeError, EnvironmentError, ImportError, FileNotFoundError):
                raise
            except Exception as exc:
                if tentativa == len(esperas):
                    raise RuntimeError(f"Falha definitiva ao criar sessão Spark após {len(esperas)} tentativas: {exc}") from exc
                self._log(f"Falha na tentativa {tentativa} ({exc}). Nova tentativa em {esperas[tentativa]}s...")
        raise RuntimeError("Falha inesperada ao criar sessão Spark.")

    def preparar_virtualenv_modelagem(
        self,
        nome_arquivo_requirements: str = "requirements-spark.txt",
        recriar_zip: bool = False,
    ) -> Tuple[Optional[str], bool]:
        """
        Cria e publica o arquivo zip de virtualenv no HDFS para uso no cluster Spark (apenas MODELAGEM).
        """
        self._preparar_contexto_local()
        if self.ambiente != "MODELAGEM":
            raise EnvironmentError("A preparação de virtualenv só é permitida no ambiente MODELAGEM.")

        try:
            from bbmagic import Hdfs
            from bbmagic.common import create_virtualenv
        except Exception as exc:
            raise ImportError(f"BBMagic não está disponível para preparar o virtualenv Spark: {exc}") from exc

        env_dir = f"/user/{self.keytab}/.bbmagic/envs"
        zip_name = f"{self.nome_sessao_final}.zip"
        hdfs_virtualenv_path = f"hdfs://{env_dir}/{zip_name}"

        hdfs = Hdfs(self.keytab)
        try:
            hdfs.makedirs(env_dir)
        except Exception:
            pass

        arquivos_hdfs = hdfs.list(env_dir)
        zip_existe = zip_name in arquivos_hdfs

        if zip_existe and not recriar_zip:
            print(f"[VIRTUALENV] Utilizando pacote existente no HDFS: {hdfs_virtualenv_path}")
            return hdfs_virtualenv_path, False

        caminho_requirements = self._localizar_arquivo(nome_arquivo_requirements)
        if not caminho_requirements:
            raise FileNotFoundError(f"Arquivo de requirements não localizado: '{nome_arquivo_requirements}'")

        with tempfile.TemporaryDirectory() as pasta_temp:
            create_virtualenv(
                requirements=caminho_requirements,
                create_zip=True,
                zip_path=pasta_temp,
                zip_name=self.nome_sessao_final,
            )
            caminho_zip_local = Path(pasta_temp) / zip_name
            if not caminho_zip_local.exists():
                zips = list(Path(pasta_temp).glob("*.zip"))
                if not zips:
                    raise FileNotFoundError("O arquivo .zip do virtualenv não foi gerado pelo BBMagic.")
                caminho_zip_local = zips[0]

            hdfs.upload(
                hdfs_path=hdfs_virtualenv_path,
                local_path=str(caminho_zip_local),
                overwrite=True,
            )

        print(f"[VIRTUALENV] Pacote gerado e publicado no HDFS com sucesso: {hdfs_virtualenv_path}")
        return hdfs_virtualenv_path, False

    def criar_sessao_spark(
        self,
        db2: bool = False,
        driver_memory: Optional[str] = None,
        driver_cores: Optional[int] = None,
        num_executors: Optional[int] = None,
        executor_memory: Optional[str] = None,
        executor_cores: Optional[int] = None,
        jars: Optional[List[str]] = None,
        pyfiles: Optional[List[str]] = None,
        files: Optional[List[str]] = None,
        archives: Optional[List[str]] = None,
        virtualenv: Optional[str] = None,
        overwrite_virtualenv: bool = False,
        spark_conf: Optional[Dict[str, Any]] = None,
        cluster: str = "CDP",
    ) -> Spark:
        """
        Instancia a sessão Spark no cluster com todos os recursos e parâmetros configurados.
        """
        self._preparar_contexto_local()

        argumentos_spark: Dict[str, Any] = {
            "session_name": self.nome_sessao_final,
            "username": self.keytab,
            "spark_version": 3,
            "cluster": cluster,
            "env": self._montar_variaveis_spark(),
            "spark_conf": self._montar_spark_conf(spark_conf),
        }

        if db2:
            argumentos_spark["db2"] = True
        if driver_memory:
            argumentos_spark["driver_memory"] = driver_memory
        if driver_cores:
            argumentos_spark["driver_cores"] = driver_cores
        if num_executors:
            argumentos_spark["num_executors"] = num_executors
        if executor_memory:
            argumentos_spark["executor_memory"] = executor_memory
        if executor_cores:
            argumentos_spark["executor_cores"] = executor_cores
        if jars:
            argumentos_spark["jars"] = jars
        if pyfiles:
            argumentos_spark["pyfiles"] = pyfiles
        if files:
            argumentos_spark["files"] = files
        if archives:
            argumentos_spark["archives"] = archives
        if virtualenv:
            argumentos_spark["virtualenv"] = virtualenv
            argumentos_spark["overwrite_virtualenv"] = overwrite_virtualenv

        self._limpar_sessao_spark_anterior()
        self._exibir_argumentos_spark(argumentos_spark)

        self.spark = self._criar_com_retry(argumentos_spark)
        return self.spark
