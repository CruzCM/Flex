%%spark

# ==================================================================================================
# RADAR_CODE
# AUDITORIA FINAL UNIFICADA HIVE/SPARK — ELIMINAÇÃO DE DB2/JDBC
# ==================================================================================================
#
# OBJETIVO
# --------
# Auditar as tabelas utilizadas / relacionadas ao Radar diretamente no Hive Metastore,
# verificando se existe base estrutural suficiente para abandonar completamente DB2/JDBC.
#
# FONTES BLOQUEADORAS DA V13
# --------------------------
# 1. db2gfp.tran_rlzd_inst_pct
# 2. db2gfp.ct_grdr_fnco
# 3. db2d1d.dvs_grdr_fnco_pf
# 4. hive_d1q.rdpr_pf
#
# TABELAS ADICIONAIS DE AUDITORIA
# -------------------------------
# 5. db2gfp.gr_ctgr_tran
# 6. db2gfp.ctgr_tran_opb
#
# PRINCÍPIOS DE PERFORMANCE
# -------------------------
# NÃO executa:
#   - COUNT(*)
#   - MIN / MAX sobre dados
#   - COUNT DISTINCT
#   - DISTINCT
#   - GROUP BY
#   - ORDER BY em dados
#   - inputFiles()
#   - recursive HDFS listing
#   - getContentSummary()
#   - ANALYZE TABLE
#   - CACHE TABLE
#   - collect/show/take sobre registros das tabelas
#
# Faz apenas:
#   - Hive Catalog / Metastore
#   - DESCRIBE FORMATTED
#   - SHOW TBLPROPERTIES
#   - catalog.listColumns
#   - FileStatus SOMENTE do diretório raiz HDFS
#   - SHOW PARTITIONS somente para tabelas explicitamente liberadas
#   - análise lógica SQL sem executar job
#
# IMPORTANTE
# ----------
# Uma réplica existir estruturalmente no Hive NÃO comprova sozinha equivalência/freshness
# contra DB2. Este diagnóstico separa:
#
#   1. EXISTÊNCIA
#   2. COMPATIBILIDADE ESTRUTURAL
#   3. ARMAZENAMENTO NATIVO HDFS
#   4. RESOLUÇÃO SPARK
#   5. EVIDÊNCIAS DE FRESHNESS DISPONÍVEIS VIA METADADOS
#
# ==================================================================================================

from datetime import datetime, timezone
import re
import traceback


# ==================================================================================================
# 0. CONFIGURAÇÃO
# ==================================================================================================

EXECUTAR_PROBE_FISICO = False

# Mesmo um LIMIT(1) pode provocar file listing / abertura de arquivos.
# Portanto permanece DESABILITADO.
#
# Só alterar para True deliberadamente em uma etapa posterior de benchmark.
# Nesta auditoria metadata-first, deve permanecer False.

MAX_PARTICOES_EXIBIDAS = 100

# Somente tabelas sabidamente com baixo número de partições podem ser enumeradas.
TABELAS_COM_ENUMERACAO_PARTICOES_SEGURA = {
    "hive_d1q.rdpr_pf",
}


TABELAS = {

    # ==============================================================================================
    # FONTES BLOQUEADORAS — USADAS PELA V13
    # ==============================================================================================

    "TRAN_RLZD_INST_PCT": {
        "tabela": "db2gfp.tran_rlzd_inst_pct",
        "grupo": "CORE_V13",
        "bloqueadora": True,
        "origem_logica": "DB2_REPLICADA_HIVE",
        "papel": "Público + contas elegíveis + transações do Radar",

        "colunas_necessarias": {
            "NR_PTC": "NUMERIC",
            "CD_CLI": "NUMERIC",
            "NR_MCA_PCT_OPB": "NUMERIC",
            "CD_PRD": "NUMERIC",
            "NR_AG_TITR": "NUMERIC",
            "CD_CT_TITR": "STRING",
            "TS_ATL_TRAN": "TIMESTAMP",
            "NR_CPF_CNPJ_TITR": "NUMERIC",

            "CD_EST_TRAN_INST": "NUMERIC",
            "CD_TIP_PSS": "NUMERIC",
            "DT_TRAN": "DATE_OR_TIMESTAMP",

            "VL_TRAN": "NUMERIC",
            "CD_NTZ_CTB_TRAN": "STRING",
            "CD_CTGR_TRAN_OGNL": "NUMERIC",
            "CD_TIP_MOE_CRR": "STRING",
        },

        "predicado_representativo": """
            CD_EST_TRAN_INST = 0
            AND CD_TIP_PSS = 1
            AND DT_TRAN IS NOT NULL
        """,
    },

    "CT_GRDR_FNCO": {
        "tabela": "db2gfp.ct_grdr_fnco",
        "grupo": "CORE_V13",
        "bloqueadora": True,
        "origem_logica": "DB2_REPLICADA_HIVE",
        "papel": "Conta GFP + dia do ciclo financeiro",

        "colunas_necessarias": {
            "CD_UOR_CC": "NUMERIC",
            "NR_CC": "NUMERIC",
            "DD_INC_MM_CLC_BLC": "NUMERIC",
        },

        "predicado_representativo": """
            CD_UOR_CC IS NOT NULL
            AND NR_CC IS NOT NULL
        """,
    },

    "DVS_GRDR_FNCO_PF": {
        "tabela": "db2d1d.dvs_grdr_fnco_pf",
        "grupo": "CORE_V13",
        "bloqueadora": True,
        "origem_logica": "DB2_REPLICADA_HIVE",
        "papel": "Macroperfil e microperfil financeiro",

        "colunas_necessarias": {
            "DT_REF": "DATE_OR_TIMESTAMP",
            "CD_CLI": "NUMERIC",
            "CD_MAC_PRFL_CLI": "NUMERIC",
            "CD_MIC_PRFL_CLI": "NUMERIC",
        },

        "predicado_representativo": """
            DT_REF IS NOT NULL
            AND CD_CLI BETWEEN 1 AND 999999999
        """,
    },

    "RDPR_PF": {
        "tabela": "hive_d1q.rdpr_pf",
        "grupo": "CORE_V13",
        "bloqueadora": True,
        "origem_logica": "HIVE_NATIVO",
        "papel": "Renda presumida Behaviour / Bureau",

        "colunas_necessarias": {
            "NR_CPF": "NUMERIC",
            "VL_RDPR": "NUMERIC",
            "CD_IN_UTZO": "NUMERIC",
            "DT_REF": "DATE_OR_TIMESTAMP",
            "TX_CTGR_MOD": "STRING",
        },

        "predicado_representativo": """
            TX_CTGR_MOD IN ('behaviour', 'bureau')
            AND DT_REF IS NOT NULL
            AND CD_IN_UTZO = -1
        """,
    },

    # ==============================================================================================
    # AUDITORIA ADICIONAL
    # ==============================================================================================

    "GR_CTGR_TRAN": {
        "tabela": "db2gfp.gr_ctgr_tran",
        "grupo": "REFERENCIA",
        "bloqueadora": False,
        "origem_logica": "DB2_REPLICADA_HIVE",
        "papel": "Cadastro oficial dos grupos de categorias",

        "colunas_necessarias": {
            "CD_GR_CTGR_TRAN": "NUMERIC",
            "TX_DCR_GR_CTGR": "STRING",
            "CD_COR_GR_CTGR": "STRING",
        },

        "predicado_representativo": """
            CD_GR_CTGR_TRAN IS NOT NULL
        """,
    },

    "CTGR_TRAN_OPB": {
        "tabela": "db2gfp.ctgr_tran_opb",
        "grupo": "REFERENCIA",
        "bloqueadora": False,
        "origem_logica": "DB2_REPLICADA_HIVE",
        "papel": "Cadastro oficial das categorias do sistema",

        "colunas_necessarias": {
            "CD_CTGR_TRAN": "NUMERIC",
            "CD_GR_CTGR_TRAN": "NUMERIC",
            "CD_NTZ_CTB_TRAN": "STRING",
            "IN_CTGR_PDRO_SIS": "STRING",
            "TX_DCR_CTGR_TRAN": "STRING",
            "CD_TRAN_IR": "NUMERIC",
        },

        "predicado_representativo": """
            IN_CTGR_PDRO_SIS = 'S'
        """,
    },
}


# ==================================================================================================
# 1. UTILITÁRIOS GERAIS
# ==================================================================================================

def linha(char="=", tamanho=130):
    print(char * tamanho)


def texto_curto(valor, limite=500):
    if valor is None:
        return None

    valor = str(valor)

    if len(valor) <= limite:
        return valor

    return valor[:limite] + "...[TRUNCADO]"


def registrar_evento(resultado, nivel, etapa, mensagem):
    resultado["eventos"].append({
        "nivel": nivel,
        "etapa": etapa,
        "mensagem": texto_curto(mensagem, 1200),
    })


def executar_seguro(resultado, etapa, funcao, padrao=None):
    """
    Executa uma etapa isoladamente.

    Qualquer Exception é registrada e o diagnóstico continua.
    KeyboardInterrupt/SystemExit NÃO são capturados deliberadamente.
    """
    try:
        return funcao()

    except Exception as exc:
        registrar_evento(
            resultado,
            "ERRO",
            etapa,
            f"{type(exc).__name__}: {exc}"
        )
        return padrao


def normalizar_tipo(tipo):
    t = str(tipo or "").strip().lower()

    if any(x in t for x in (
        "tinyint",
        "smallint",
        "int",
        "integer",
        "bigint",
        "decimal",
        "numeric",
        "float",
        "double",
        "real",
    )):
        return "NUMERIC"

    if t.startswith("timestamp"):
        return "TIMESTAMP"

    if t.startswith("date"):
        return "DATE"

    if any(x in t for x in (
        "string",
        "char",
        "varchar",
    )):
        return "STRING"

    if t.startswith("boolean"):
        return "BOOLEAN"

    if t.startswith("binary"):
        return "BINARY"

    if t.startswith("array"):
        return "ARRAY"

    if t.startswith("map"):
        return "MAP"

    if t.startswith("struct"):
        return "STRUCT"

    return t.upper() if t else "DESCONHECIDO"


def tipo_compativel(tipo_real, tipo_esperado):

    familia = normalizar_tipo(tipo_real)

    if tipo_esperado == "DATE_OR_TIMESTAMP":
        return familia in ("DATE", "TIMESTAMP")

    return familia == tipo_esperado


def formatar_bytes(valor):

    if valor is None:
        return "N/D"

    try:
        numero = int(valor)
    except Exception:
        return str(valor)

    unidades = ["B", "KB", "MB", "GB", "TB", "PB"]

    valor_float = float(numero)

    for unidade in unidades:

        if abs(valor_float) < 1024.0 or unidade == unidades[-1]:
            return f"{valor_float:,.2f} {unidade} ({numero:,} bytes)"

        valor_float /= 1024.0


# ==================================================================================================
# 2. METADADOS HIVE
# ==================================================================================================

def obter_describe_formatted(tabela):

    linhas = spark.sql(
        f"DESCRIBE FORMATTED {tabela}"
    ).collect()

    resultado = {}

    for row in linhas:

        valores = list(row)

        chave = (
            str(valores[0]).strip()
            if len(valores) > 0 and valores[0] is not None
            else ""
        )

        valor = (
            str(valores[1]).strip()
            if len(valores) > 1 and valores[1] is not None
            else ""
        )

        if chave:
            resultado[chave] = valor

    return resultado


def obter_tblproperties(tabela):

    propriedades = {}

    linhas = spark.sql(
        f"SHOW TBLPROPERTIES {tabela}"
    ).collect()

    for row in linhas:

        valores = list(row)

        if len(valores) >= 2:
            propriedades[str(valores[0])] = str(valores[1])

    return propriedades


def encontrar_metadata(meta, *nomes):

    procurados = {
        str(nome).strip().lower()
        for nome in nomes
    }

    for chave, valor in meta.items():

        if str(chave).strip().lower() in procurados:
            return valor

    return None


def detectar_formato(meta, props):

    elementos = [
        encontrar_metadata(meta, "Provider"),
        encontrar_metadata(meta, "InputFormat"),
        encontrar_metadata(meta, "OutputFormat"),
        encontrar_metadata(meta, "Serde Library"),
        props.get("spark.sql.sources.provider"),
    ]

    texto = " ".join(
        str(x or "")
        for x in elementos
    ).lower()

    if "parquet" in texto:
        return "PARQUET"

    if "orc" in texto:
        return "ORC"

    if "avro" in texto:
        return "AVRO"

    if "jdbc" in texto:
        return "JDBC"

    if "text" in texto:
        return "TEXT"

    provider = encontrar_metadata(meta, "Provider")

    return (
        str(provider).upper()
        if provider
        else "NAO_IDENTIFICADO"
    )


def detectar_jdbc_indireto(meta, props):

    textos = []

    for chave in (
        "Provider",
        "InputFormat",
        "OutputFormat",
        "Serde Library",
        "Storage Handler",
    ):
        valor = encontrar_metadata(meta, chave)

        if valor:
            textos.append(str(valor))

    for chave, valor in props.items():

        kl = str(chave).lower()

        # Não copiamos valores sensíveis para saída.
        if any(x in kl for x in (
            "provider",
            "driver",
            "jdbc",
            "url",
        )):
            textos.append(str(chave))
            textos.append(str(valor))

    agregado = " ".join(textos).lower()

    return "jdbc" in agregado


def classificar_localizacao(location):

    if not location:
        return "NAO_IDENTIFICADA"

    loc = str(location).lower()

    if "modelagemha" in loc:
        return "SANDBOX_MODELAGEM"

    if "/dados/transientes/" in loc:
        return "SANDBOX_TRANSIENTE"

    if "/sbx_" in loc:
        return "SANDBOX"

    if "/dados/corporativos/" in loc:
        return "CORPORATIVA"

    if loc.startswith("hdfs://"):
        return "HDFS_OUTRA"

    return "OUTRA"


# ==================================================================================================
# 3. SCHEMA
# ==================================================================================================

def obter_schema_catalogo(tabela):
    """
    Caminho principal: Spark Catalog.

    Se listColumns falhar, usa spark.table(...).schema como fallback.
    O fallback lê apenas definição de schema; não executa action.
    """

    try:
        colunas = spark.catalog.listColumns(tabela)

        return [
            {
                "nome": c.name,
                "tipo": c.dataType,
                "nullable": c.nullable,
                "particao": c.isPartition,
                "bucket": c.isBucket,
                "origem_schema": "CATALOG_LISTCOLUMNS",
            }
            for c in colunas
        ]

    except Exception:

        schema = spark.table(tabela).schema

        return [
            {
                "nome": campo.name,
                "tipo": campo.dataType.simpleString(),
                "nullable": campo.nullable,
                "particao": False,
                "bucket": False,
                "origem_schema": "DATAFRAME_SCHEMA_FALLBACK",
            }
            for campo in schema.fields
        ]


def validar_colunas(schema_info, esperadas):

    mapa = {
        c["nome"].upper(): c
        for c in schema_info
    }

    presentes = []
    faltantes = []
    incompativeis = []

    for nome, esperado in esperadas.items():

        coluna = mapa.get(nome.upper())

        if coluna is None:
            faltantes.append(nome)
            continue

        if tipo_compativel(
            coluna["tipo"],
            esperado
        ):
            presentes.append(nome)

        else:
            incompativeis.append(
                {
                    "coluna": nome,
                    "tipo_hive": coluna["tipo"],
                    "esperado": esperado,
                }
            )

    return presentes, faltantes, incompativeis


# ==================================================================================================
# 4. HDFS — SOMENTE FILESTATUS DO ROOT
# ==================================================================================================

def obter_status_hdfs_root(location):
    """
    NÃO lista arquivos.
    NÃO calcula tamanho recursivo.
    NÃO usa getContentSummary().

    Consulta somente FileStatus do caminho informado.
    """

    resultado = {
        "aplicavel": False,
        "existe": None,
        "diretorio": None,
        "modificacao_utc": None,
    }

    if not location:
        return resultado

    if not str(location).lower().startswith("hdfs://"):
        return resultado

    resultado["aplicavel"] = True

    jvm = spark._jvm
    hconf = spark._jsc.hadoopConfiguration()

    path = jvm.org.apache.hadoop.fs.Path(location)
    fs = path.getFileSystem(hconf)

    existe = bool(fs.exists(path))

    resultado["existe"] = existe

    if not existe:
        return resultado

    status = fs.getFileStatus(path)

    resultado["diretorio"] = bool(
        status.isDirectory()
    )

    timestamp_ms = status.getModificationTime()

    resultado["modificacao_utc"] = (
        datetime
        .fromtimestamp(
            timestamp_ms / 1000.0,
            tz=timezone.utc
        )
        .isoformat()
    )

    return resultado


# ==================================================================================================
# 5. ESTATÍSTICAS JÁ EXISTENTES — SEM ANALYZE TABLE
# ==================================================================================================

def extrair_stats_existentes(meta, props):

    stats = {}

    nomes = {
        "numrows": "numRows",
        "numfiles": "numFiles",
        "rawdatasize": "rawDataSize",
        "totalsize": "totalSize",
    }

    for fonte in (meta, props):

        for chave, valor in fonte.items():

            normalizada = (
                str(chave)
                .strip()
                .lower()
                .replace(" ", "")
            )

            if normalizada in nomes:
                stats[nomes[normalizada]] = valor

    # Alguns DESCRIBE FORMATTED trazem:
    # Statistics   123456 bytes, 789 rows
    statistics = encontrar_metadata(
        meta,
        "Statistics"
    )

    if statistics:
        stats["Statistics"] = statistics

    return stats


# ==================================================================================================
# 6. PARTIÇÕES — SOMENTE METASTORE E SOMENTE ALLOWLIST
# ==================================================================================================

def obter_particoes_seguras(tabela):

    if (
        tabela.lower()
        not in TABELAS_COM_ENUMERACAO_PARTICOES_SEGURA
    ):
        return {
            "enumerada": False,
            "motivo": "BLOQUEADA_POR_SEGURANCA",
            "particoes": [],
            "truncada": False,
        }

    linhas = spark.sql(
        f"SHOW PARTITIONS {tabela}"
    ).take(MAX_PARTICOES_EXIBIDAS + 1)

    truncada = (
        len(linhas) >
        MAX_PARTICOES_EXIBIDAS
    )

    particoes = [
        str(row[0])
        for row in linhas[:MAX_PARTICOES_EXIBIDAS]
    ]

    return {
        "enumerada": True,
        "motivo": None,
        "particoes": particoes,
        "truncada": truncada,
    }


def maior_dt_ref_em_particoes(particoes):

    datas = []

    padrao = re.compile(
        r"(?:^|/)dt_ref=([^/]+)",
        re.IGNORECASE
    )

    for p in particoes:

        match = padrao.search(p)

        if match:
            datas.append(match.group(1))

    return max(datas) if datas else None


# ==================================================================================================
# 7. ANÁLISE LÓGICA SPARK — SEM ACTION
# ==================================================================================================

def validar_consulta_logica(
    tabela,
    colunas,
    predicado
):
    """
    Cria DataFrame e solicita apenas o plano ANALYZED.

    Não executa:
      count()
      collect()
      show()
      take()
      write()

    Portanto não deve disparar job Spark de leitura dos dados.
    """

    lista = ", ".join(colunas)

    query = f"""
        SELECT
            {lista}
        FROM {tabela}
        WHERE {predicado}
    """

    df = spark.sql(query)

    plano = (
        df
        ._jdf
        .queryExecution()
        .analyzed()
        .toString()
    )

    return {
        "ok": True,
        "query": query,
        "plano": texto_curto(plano, 4000),
    }


# ==================================================================================================
# 8. PROBE FÍSICO OPCIONAL — DESABILITADO
# ==================================================================================================

def probe_fisico_opcional(
    tabela,
    colunas,
    predicado
):
    """
    NÃO será chamado enquanto EXECUTAR_PROBE_FISICO=False.

    Mesmo LIMIT(1) pode provocar file listing e I/O,
    portanto não faz parte da auditoria metadata-first.
    """

    df = (
        spark
        .table(tabela)
        .select(*colunas)
        .where(predicado)
        .limit(1)
    )

    rows = df.collect()

    return len(rows)


# ==================================================================================================
# 9. ESTRUTURA DE RESULTADO
# ==================================================================================================

def novo_resultado(chave, cfg):

    return {
        "chave": chave,
        "tabela": cfg["tabela"],
        "grupo": cfg["grupo"],
        "bloqueadora": cfg["bloqueadora"],
        "origem_logica": cfg["origem_logica"],
        "papel": cfg["papel"],

        "existe": False,

        "tipo_tabela": None,
        "temporaria": None,

        "provider": None,
        "input_format": None,
        "output_format": None,
        "serde": None,
        "location": None,

        "formato": None,
        "classe_localizacao": None,
        "jdbc_indireto": None,

        "hdfs_existe": None,
        "hdfs_modificacao_utc": None,

        "qtd_colunas": None,
        "colunas_particao": [],
        "colunas_bucket": [],

        "colunas_faltantes": [],
        "tipos_incompativeis": [],

        "stats": {},
        "particoes": [],
        "particoes_truncadas": False,
        "max_dt_ref_particao": None,

        "sql_analisavel": False,

        "estrutura_compativel": False,
        "armazenamento_nativo": False,

        "status": "NAO_PROCESSADA",
        "veredito": "NAO_AVALIADO",

        "eventos": [],
    }


# ==================================================================================================
# 10. CABEÇALHO DA AUDITORIA
# ==================================================================================================

linha()
print("RADAR_CODE — AUDITORIA FINAL HIVE/SPARK")
print("OBJETIVO: avaliar remoção completa de DB2/JDBC")
linha()

print(f"Spark version.......................: {spark.version}")
print(f"defaultParallelism..................: {spark.sparkContext.defaultParallelism}")

print(
    "spark.sql.shuffle.partitions......:",
    spark.conf.get(
        "spark.sql.shuffle.partitions",
        "N/D"
    )
)

print(
    "spark.sql.adaptive.enabled.........:",
    spark.conf.get(
        "spark.sql.adaptive.enabled",
        "N/D"
    )
)

print(
    "spark.sql.catalogImplementation....:",
    spark.conf.get(
        "spark.sql.catalogImplementation",
        "N/D"
    )
)

print()
print("Quantidade de tabelas auditadas.....:", len(TABELAS))
print("Modo.................................: METADATA-FIRST")
print("Probe físico........................:", EXECUTAR_PROBE_FISICO)

linha()


# ==================================================================================================
# 11. AUDITORIA DAS TABELAS
# ==================================================================================================

resultados = []

for chave, cfg in TABELAS.items():

    resultado = novo_resultado(
        chave,
        cfg
    )

    tabela = cfg["tabela"]

    linha()
    print(f"📦 {chave}")
    print(f"Tabela...............................: {tabela}")
    print(f"Grupo................................: {cfg['grupo']}")
    print(f"Bloqueadora para V13.................: {cfg['bloqueadora']}")
    print(f"Papel................................: {cfg['papel']}")
    linha("-")

    # ==============================================================================================
    # ETAPA 1 — EXISTÊNCIA
    # ==============================================================================================

    existe = executar_seguro(
        resultado,
        "TABLE_EXISTS",
        lambda: bool(
            spark.catalog.tableExists(
                tabela
            )
        ),
        False
    )

    resultado["existe"] = bool(existe)

    print(
        "Existe no Hive Catalog..............:",
        "SIM" if existe else "NAO"
    )

    if not existe:

        resultado["status"] = "ERRO"
        resultado["veredito"] = "TABELA_NAO_ENCONTRADA"

        registrar_evento(
            resultado,
            "ERRO",
            "TABLE_EXISTS",
            "Tabela canônica não encontrada no Hive Catalog."
        )

        resultados.append(resultado)

        print()
        print("❌ Tabela não encontrada.")
        print("   As demais tabelas continuarão sendo processadas.")

        continue

    # ==============================================================================================
    # ETAPA 2 — DESCRIBE FORMATTED
    # ==============================================================================================

    meta = executar_seguro(
        resultado,
        "DESCRIBE_FORMATTED",
        lambda: obter_describe_formatted(
            tabela
        ),
        {}
    )

    # ==============================================================================================
    # ETAPA 3 — TBLPROPERTIES
    # ==============================================================================================

    props = executar_seguro(
        resultado,
        "SHOW_TBLPROPERTIES",
        lambda: obter_tblproperties(
            tabela
        ),
        {}
    )

    # ==============================================================================================
    # ETAPA 4 — CATALOG GET TABLE
    # ==============================================================================================

    tabela_catalogo = executar_seguro(
        resultado,
        "CATALOG_GET_TABLE",
        lambda: spark.catalog.getTable(
            tabela
        ),
        None
    )

    if tabela_catalogo is not None:

        resultado["tipo_tabela"] = (
            tabela_catalogo.tableType
        )

        resultado["temporaria"] = (
            tabela_catalogo.isTemporary
        )

    else:

        resultado["tipo_tabela"] = encontrar_metadata(
            meta,
            "Type",
            "Table Type"
        )

    # ==============================================================================================
    # ETAPA 5 — STORAGE
    # ==============================================================================================

    resultado["provider"] = encontrar_metadata(
        meta,
        "Provider"
    )

    resultado["input_format"] = encontrar_metadata(
        meta,
        "InputFormat"
    )

    resultado["output_format"] = encontrar_metadata(
        meta,
        "OutputFormat"
    )

    resultado["serde"] = encontrar_metadata(
        meta,
        "Serde Library"
    )

    resultado["location"] = encontrar_metadata(
        meta,
        "Location"
    )

    resultado["formato"] = detectar_formato(
        meta,
        props
    )

    resultado["classe_localizacao"] = (
        classificar_localizacao(
            resultado["location"]
        )
    )

    resultado["jdbc_indireto"] = (
        detectar_jdbc_indireto(
            meta,
            props
        )
    )

    print()
    print("METADADOS DE ARMAZENAMENTO")
    print("----------------------------------------")
    print(f"Tipo tabela............................: {resultado['tipo_tabela']}")
    print(f"Provider...............................: {resultado['provider']}")
    print(f"Formato detectado......................: {resultado['formato']}")
    print(f"InputFormat............................: {resultado['input_format']}")
    print(f"OutputFormat...........................: {resultado['output_format']}")
    print(f"Serde..................................: {resultado['serde']}")
    print(f"Location...............................: {resultado['location']}")
    print(f"Classe localização.....................: {resultado['classe_localizacao']}")
    print(f"Indício de JDBC indireto...............: {resultado['jdbc_indireto']}")

    # ==============================================================================================
    # ETAPA 6 — HDFS ROOT STATUS
    # ==============================================================================================

    hdfs = executar_seguro(
        resultado,
        "HDFS_ROOT_FILESTATUS",
        lambda: obter_status_hdfs_root(
            resultado["location"]
        ),
        {
            "aplicavel": False,
            "existe": None,
            "diretorio": None,
            "modificacao_utc": None,
        }
    )

    resultado["hdfs_existe"] = (
        hdfs.get("existe")
    )

    resultado["hdfs_modificacao_utc"] = (
        hdfs.get("modificacao_utc")
    )

    print()
    print("HDFS ROOT — SEM RECURSÃO")
    print("----------------------------------------")
    print(f"Aplicável..............................: {hdfs.get('aplicavel')}")
    print(f"Path existe............................: {hdfs.get('existe')}")
    print(f"É diretório............................: {hdfs.get('diretorio')}")
    print(f"Última modificação root UTC............: {hdfs.get('modificacao_utc')}")

    # ==============================================================================================
    # ETAPA 7 — SCHEMA
    # ==============================================================================================

    schema_info = executar_seguro(
        resultado,
        "SCHEMA",
        lambda: obter_schema_catalogo(
            tabela
        ),
        []
    )

    resultado["qtd_colunas"] = len(
        schema_info
    )

    resultado["colunas_particao"] = [
        c["nome"]
        for c in schema_info
        if c.get("particao")
    ]

    resultado["colunas_bucket"] = [
        c["nome"]
        for c in schema_info
        if c.get("bucket")
    ]

    print()
    print("SCHEMA")
    print("----------------------------------------")
    print(f"Quantidade de colunas..................: {resultado['qtd_colunas']}")
    print(f"Colunas de partição....................: {resultado['colunas_particao'] or 'NENHUMA'}")
    print(f"Colunas bucket.........................: {resultado['colunas_bucket'] or 'NENHUMA'}")

    if schema_info:

        print()
        print(
            f"{'#':>3} | "
            f"{'COLUNA':<32} | "
            f"{'TIPO':<28} | "
            f"{'NULL':<5} | "
            f"{'PART':<5} | "
            f"{'BUCKET':<6}"
        )

        print("-" * 100)

        for i, coluna in enumerate(
            schema_info,
            start=1
        ):

            print(
                f"{i:>3} | "
                f"{coluna['nome']:<32} | "
                f"{coluna['tipo']:<28} | "
                f"{str(coluna['nullable']):<5} | "
                f"{str(coluna['particao']):<5} | "
                f"{str(coluna['bucket']):<6}"
            )

    # ==============================================================================================
    # ETAPA 8 — COLUNAS NECESSÁRIAS
    # ==============================================================================================

    validacao = executar_seguro(
        resultado,
        "VALIDACAO_COLUNAS",
        lambda: validar_colunas(
            schema_info,
            cfg["colunas_necessarias"]
        ),
        (
            [],
            list(
                cfg["colunas_necessarias"].keys()
            ),
            []
        )
    )

    presentes, faltantes, incompativeis = validacao

    resultado["colunas_faltantes"] = faltantes
    resultado["tipos_incompativeis"] = incompativeis

    print()
    print("COMPATIBILIDADE COM O RADAR")
    print("----------------------------------------")

    mapa_schema = {
        c["nome"].upper(): c
        for c in schema_info
    }

    print(
        f"{'COLUNA':<32} | "
        f"{'ESPERADO':<20} | "
        f"{'HIVE':<28} | "
        f"STATUS"
    )

    print("-" * 95)

    for nome, esperado in (
        cfg["colunas_necessarias"].items()
    ):

        coluna = mapa_schema.get(
            nome.upper()
        )

        if coluna is None:

            print(
                f"{nome:<32} | "
                f"{esperado:<20} | "
                f"{'AUSENTE':<28} | "
                f"❌"
            )

        else:

            compativel = tipo_compativel(
                coluna["tipo"],
                esperado
            )

            print(
                f"{nome:<32} | "
                f"{esperado:<20} | "
                f"{coluna['tipo']:<28} | "
                f"{'✅' if compativel else '⚠️'}"
            )

    print()
    print(
        "Colunas faltantes......................:",
        faltantes or "NENHUMA"
    )

    print(
        "Tipos incompatíveis....................:",
        incompativeis or "NENHUM"
    )

    # ==============================================================================================
    # ETAPA 9 — STATS EXISTENTES NO METASTORE
    # ==============================================================================================

    stats = executar_seguro(
        resultado,
        "METASTORE_STATS",
        lambda: extrair_stats_existentes(
            meta,
            props
        ),
        {}
    )

    resultado["stats"] = stats

    print()
    print("ESTATÍSTICAS JÁ EXISTENTES")
    print("----------------------------------------")

    if not stats:

        print("Nenhuma estatística reutilizável encontrada.")
        print("ANALYZE TABLE NÃO será executado.")

    else:

        for chave_stat, valor in stats.items():

            if chave_stat in (
                "totalSize",
                "rawDataSize"
            ):
                valor_exibido = (
                    formatar_bytes(valor)
                )
            else:
                valor_exibido = valor

            print(
                f"{chave_stat:<30}: "
                f"{valor_exibido}"
            )

    # ==============================================================================================
    # ETAPA 10 — PROPRIEDADES OPERACIONAIS NÃO SENSÍVEIS
    # ==============================================================================================

    print()
    print("PROPRIEDADES OPERACIONAIS")
    print("----------------------------------------")

    propriedades_permitidas = (
        "transient_lastDdlTime",
        "last_modified_by",
        "last_modified_time",
        "COLUMN_STATS_ACCURATE",
        "numRows",
        "numFiles",
        "totalSize",
        "rawDataSize",
        "external.table.purge",
        "bucketing_version",
        "spark.sql.sources.provider",
    )

    encontrou = False

    for propriedade in propriedades_permitidas:

        if propriedade in props:

            encontrou = True

            valor = props[
                propriedade
            ]

            if propriedade in (
                "totalSize",
                "rawDataSize"
            ):
                valor = formatar_bytes(
                    valor
                )

            print(
                f"{propriedade:<32}: "
                f"{valor}"
            )

    if not encontrou:
        print("Nenhuma propriedade selecionada encontrada.")

    # ==============================================================================================
    # ETAPA 11 — PARTIÇÕES
    # ==============================================================================================

    print()
    print("PARTICIONAMENTO")
    print("----------------------------------------")

    if resultado["colunas_particao"]:

        print("Tabela particionada....................: SIM")

        part_info = executar_seguro(
            resultado,
            "SHOW_PARTITIONS",
            lambda: obter_particoes_seguras(
                tabela
            ),
            {
                "enumerada": False,
                "motivo": "ERRO",
                "particoes": [],
                "truncada": False,
            }
        )

        resultado["particoes"] = (
            part_info["particoes"]
        )

        resultado["particoes_truncadas"] = (
            part_info["truncada"]
        )

        print(
            "Partições enumeradas...................:",
            part_info["enumerada"]
        )

        if not part_info["enumerada"]:

            print(
                "Motivo.................................:",
                part_info["motivo"]
            )

        else:

            print(
                "Quantidade observada...................:",
                len(part_info["particoes"])
            )

            print(
                "Resultado truncado.....................:",
                part_info["truncada"]
            )

            for particao in (
                part_info["particoes"]
            ):
                print(
                    "  ",
                    particao
                )

            maior_dt = maior_dt_ref_em_particoes(
                part_info["particoes"]
            )

            resultado[
                "max_dt_ref_particao"
            ] = maior_dt

            if maior_dt:

                print()
                print(
                    "Maior DT_REF vista no metastore.......:",
                    maior_dt
                )

    else:

        print("Tabela particionada....................: NAO")
        print("Partition pruning Hive.................: NÃO DISPONÍVEL")
        print("Column pruning........................: depende do formato colunar")
        print("Predicate/filter skipping..............: deve ser validado em benchmark posterior")

    # ==============================================================================================
    # ETAPA 12 — RESOLUÇÃO LÓGICA SPARK
    # ==============================================================================================

    analise = executar_seguro(
        resultado,
        "ANALISE_LOGICA_SQL",
        lambda: validar_consulta_logica(
            tabela,
            list(
                cfg[
                    "colunas_necessarias"
                ].keys()
            ),
            cfg[
                "predicado_representativo"
            ]
        ),
        None
    )

    if analise:

        resultado["sql_analisavel"] = True

        print()
        print("ANÁLISE LÓGICA SPARK")
        print("----------------------------------------")
        print("Consulta resolvida......................: SIM")
        print("Job de leitura disparado................: NÃO")
        print("Plano analyzed..........................: OK")

    else:

        resultado["sql_analisavel"] = False

        print()
        print("ANÁLISE LÓGICA SPARK")
        print("----------------------------------------")
        print("Consulta resolvida......................: NÃO")

    # ==============================================================================================
    # ETAPA 13 — PROBE FÍSICO OPCIONAL
    # ==============================================================================================

    if EXECUTAR_PROBE_FISICO:

        probe = executar_seguro(
            resultado,
            "PROBE_FISICO",
            lambda: probe_fisico_opcional(
                tabela,
                list(
                    cfg[
                        "colunas_necessarias"
                    ].keys()
                )[:3],
                cfg[
                    "predicado_representativo"
                ]
            ),
            None
        )

        print()
        print("PROBE FÍSICO")
        print("----------------------------------------")
        print("Resultado...............................:", probe)

    else:

        print()
        print("PROBE FÍSICO")
        print("----------------------------------------")
        print("DESABILITADO POR SEGURANÇA DE PERFORMANCE")

    # ==============================================================================================
    # ETAPA 14 — CLASSIFICAÇÃO
    # ==============================================================================================

    formato_colunar = (
        resultado["formato"]
        in ("ORC", "PARQUET")
    )

    hdfs_valido = (
        resultado["hdfs_existe"]
        is not False
    )

    estrutura_compativel = (
        resultado["existe"]
        and len(
            resultado[
                "colunas_faltantes"
            ]
        ) == 0
        and len(
            resultado[
                "tipos_incompativeis"
            ]
        ) == 0
        and resultado[
            "sql_analisavel"
        ]
    )

    armazenamento_nativo = (
        not resultado[
            "jdbc_indireto"
        ]
        and formato_colunar
        and resultado[
            "classe_localizacao"
        ] in (
            "CORPORATIVA",
            "HDFS_OUTRA",
            "SANDBOX_MODELAGEM",
            "SANDBOX_TRANSIENTE",
            "SANDBOX",
        )
        and hdfs_valido
    )

    resultado[
        "estrutura_compativel"
    ] = estrutura_compativel

    resultado[
        "armazenamento_nativo"
    ] = armazenamento_nativo

    # ----------------------------------------------------------------------------------------------
    # STATUS
    # ----------------------------------------------------------------------------------------------

    possui_erros = any(
        evento["nivel"] == "ERRO"
        for evento in resultado["eventos"]
    )

    if (
        estrutura_compativel
        and armazenamento_nativo
    ):

        if possui_erros:
            resultado["status"] = "WARN"
        else:
            resultado["status"] = "OK"

        resultado[
            "veredito"
        ] = "APTA_ESTRUTURALMENTE_SEM_JDBC"

    else:

        resultado["status"] = "ERRO"

        if resultado["jdbc_indireto"]:

            resultado[
                "veredito"
            ] = "CATALOGO_EXISTE_MAS_BACKEND_JDBC"

        elif resultado[
            "colunas_faltantes"
        ]:

            resultado[
                "veredito"
            ] = "SCHEMA_INCOMPLETO"

        elif resultado[
            "tipos_incompativeis"
        ]:

            resultado[
                "veredito"
            ] = "TIPOS_INCOMPATIVEIS"

        elif not resultado[
            "sql_analisavel"
        ]:

            resultado[
                "veredito"
            ] = "SQL_NAO_RESOLVE"

        else:

            resultado[
                "veredito"
            ] = "ARMAZENAMENTO_NAO_CONFIRMADO"

    # ==============================================================================================
    # RESULTADO INDIVIDUAL
    # ==============================================================================================

    print()
    print("RESULTADO INDIVIDUAL")
    print("----------------------------------------")

    print(
        "Estrutura compatível...................:",
        resultado["estrutura_compativel"]
    )

    print(
        "Armazenamento nativo Spark/HDFS........:",
        resultado["armazenamento_nativo"]
    )

    print(
        "Status.................................:",
        resultado["status"]
    )

    print(
        "Veredito...............................:",
        resultado["veredito"]
    )

    if resultado["eventos"]:

        print()
        print("EVENTOS / FALHAS NÃO FATAIS")
        print("----------------------------------------")

        for evento in resultado[
            "eventos"
        ]:

            print(
                f"[{evento['nivel']}] "
                f"{evento['etapa']}: "
                f"{evento['mensagem']}"
            )

    resultados.append(
        resultado
    )


# ==================================================================================================
# 12. RESUMO FINAL — SEM DEPENDER DE SPARK DATAFRAME
# ==================================================================================================

linha()
print("RESUMO FINAL DA AUDITORIA")
linha()

cabecalho = (
    f"{'TABELA':<35} | "
    f"{'GRUPO':<12} | "
    f"{'EXISTE':<7} | "
    f"{'FORMATO':<12} | "
    f"{'LOCAL':<20} | "
    f"{'SCHEMA':<7} | "
    f"{'NATIVO':<7} | "
    f"{'STATUS':<7} | "
    f"VEREDITO"
)

print(cabecalho)
print("-" * len(cabecalho))

for r in resultados:

    print(
        f"{r['tabela']:<35} | "
        f"{r['grupo']:<12} | "
        f"{('SIM' if r['existe'] else 'NAO'):<7} | "
        f"{str(r['formato'] or 'N/D'):<12} | "
        f"{str(r['classe_localizacao'] or 'N/D'):<20} | "
        f"{('SIM' if r['estrutura_compativel'] else 'NAO'):<7} | "
        f"{('SIM' if r['armazenamento_nativo'] else 'NAO'):<7} | "
        f"{r['status']:<7} | "
        f"{r['veredito']}"
    )


# ==================================================================================================
# 13. RESUMO DE ERROS / WARNINGS
# ==================================================================================================

linha("-")
print("ERROS E WARNINGS CAPTURADOS")
linha("-")

total_eventos = 0

for r in resultados:

    for evento in r["eventos"]:

        total_eventos += 1

        print(
            f"{r['tabela']} | "
            f"{evento['nivel']} | "
            f"{evento['etapa']} | "
            f"{evento['mensagem']}"
        )

if total_eventos == 0:
    print("Nenhum erro/warning capturado.")


# ==================================================================================================
# 14. DECISÃO SOBRE AS 4 FONTES BLOQUEADORAS DA V13
# ==================================================================================================

core = [
    r
    for r in resultados
    if r["bloqueadora"]
]

core_esperado = sum(
    1
    for cfg in TABELAS.values()
    if cfg["bloqueadora"]
)

core_completo = (
    len(core)
    == core_esperado
)

core_estrutural_ok = (
    core_completo
    and all(
        r[
            "estrutura_compativel"
        ]
        for r in core
    )
)

core_nativo_ok = (
    core_completo
    and all(
        r[
            "armazenamento_nativo"
        ]
        for r in core
    )
)

core_sem_jdbc_indireto = (
    core_completo
    and all(
        not r[
            "jdbc_indireto"
        ]
        for r in core
    )
)


linha()
print("DECISÃO — REMOÇÃO DO DB2/JDBC DA V13")
linha()

print(
    "Fontes core esperadas................:",
    core_esperado
)

print(
    "Fontes core processadas..............:",
    len(core)
)

print(
    "Todas existem/estrutura compatível...:",
    core_estrutural_ok
)

print(
    "Todas possuem armazenamento nativo...:",
    core_nativo_ok
)

print(
    "Nenhuma possui JDBC indireto..........:",
    core_sem_jdbc_indireto
)

print()


if (
    core_estrutural_ok
    and core_nativo_ok
    and core_sem_jdbc_indireto
):

    print("✅ CONCLUSÃO ESTRUTURAL")
    print()
    print("As 4 fontes físicas bloqueadoras da V13 estão disponíveis")
    print("ao Spark através do Hive com estrutura compatível e sem")
    print("evidência de backend JDBC.")
    print()
    print("Portanto, do ponto de vista de ARQUITETURA DE ACESSO,")
    print("é possível construir a próxima versão sem DB2/JDBC.")
    print()
    print("AINDA NÃO SIGNIFICA equivalência temporal comprovada.")
    print("Antes da migração definitiva falta validar:")
    print()
    print("  1. freshness das réplicas;")
    print("  2. equivalência dos recortes usados pelo Radar;")
    print("  3. desempenho real das leituras ORC/Parquet;")
    print("  4. eficiência do predicate/column pruning;")
    print("  5. impacto do novo desenho sem acumuladores mensais JDBC.")

else:

    print("❌ CONCLUSÃO ESTRUTURAL")
    print()
    print("Ainda existe pelo menos uma fonte bloqueadora da V13")
    print("que não está comprovadamente apta para substituir DB2/JDBC.")
    print()
    print("Verifique o resumo individual para localizar a pendência.")


# ==================================================================================================
# 15. AUDITORIA DAS DUAS TABELAS DE REFERÊNCIA
# ==================================================================================================

referencias = [
    r
    for r in resultados
    if not r["bloqueadora"]
]

linha()
print("AUDITORIA ADICIONAL — TABELAS DE REFERÊNCIA")
linha()

for r in referencias:

    print(
        f"{r['tabela']}: "
        f"{r['veredito']}"
    )


# ==================================================================================================
# 16. GARANTIAS DE PERFORMANCE DO PRÓPRIO DIAGNÓSTICO
# ==================================================================================================

linha()
print("GARANTIAS DE SEGURANÇA DE PERFORMANCE")
linha()

print("COUNT(*) executado..................: NÃO")
print("MIN/MAX em dados executado..........: NÃO")
print("DISTINCT executado..................: NÃO")
print("GROUP BY executado..................: NÃO")
print("ANALYZE TABLE executado.............: NÃO")
print("inputFiles() executado..............: NÃO")
print("Listagem HDFS recursiva.............: NÃO")
print("ContentSummary HDFS.................: NÃO")
print("Leitura de registros................:", "SIM" if EXECUTAR_PROBE_FISICO else "NÃO")
print("SHOW PARTITIONS irrestrito..........: NÃO")
print("Falha individual aborta auditoria...: NÃO")

linha()
print("FIM DA AUDITORIA RADAR_CODE")
linha()
