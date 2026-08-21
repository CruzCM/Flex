# Ambiente de Produção — Documentação Estruturada

> Documento gerado a partir de `AMBIENTE_PRODUCAO.txt`, preservando integralmente todas as atribuições recebidas. A organização abaixo adiciona estrutura de navegação e decomposição de valores compostos, sem corrigir, normalizar, reordenar, deduplicar ou ocultar o conteúdo original.

> **Atenção:** o arquivo contém valores de sessão, token/secret, caminhos de keytab e outros identificadores operacionais. Eles foram mantidos exatamente porque o objetivo desta documentação é preservar 100% das informações do arquivo-fonte.

## 1. Metadados e integridade

| Campo | Valor |
|---|---|
| Arquivo-fonte | `AMBIENTE_PRODUCAO.txt` |
| Tamanho do arquivo-fonte | `64886` bytes |
| Linhas físicas | `61` |
| Linhas vazias | `1` |
| Atribuições `NOME=VALOR` | `60` |
| Variáveis únicas | `60` |
| SHA-256 do conteúdo-fonte | `9362ec7c88b9b7b759713aede5daaad1bf3d8b2f73edf30bf65e896e30f93910` |

### Regras de preservação aplicadas

- Nenhuma variável foi removida.
- Nenhum valor foi redigido, mascarado ou substituído.
- Valores vazios continuam explicitamente representados como vazios.
- A ordem interna de listas separadas por `:` foi preservada.
- Entradas repetidas em listas foram preservadas; não houve deduplicação.
- Entradas vazias produzidas por separadores consecutivos ou finais foram preservadas.
- Cada variável apresenta sua atribuição original completa em bloco `text`.
- O dump bruto integral é repetido no apêndice para conferência direta.

## 2. Sumário

- [1. Metadados e integridade](#1-metadados-e-integridade)
- [2. Sumário](#2-sumário)
- [3. Visão geral](#3-visão-geral)
- [4. Identificação do ambiente e projeto](#4-identificação-do-ambiente-e-projeto)
- [5. Aplicação e sessão](#5-aplicação-e-sessão)
- [6. Hadoop](#6-hadoop)
- [7. YARN, container e NodeManager](#7-yarn-container-e-nodemanager)
- [8. Spark e Livy](#8-spark-e-livy)
- [9. Java e JVM](#9-java-e-jvm)
- [10. Python e PySpark](#10-python-e-pyspark)
- [11. Autenticação, tokens e credenciais](#11-autenticação-tokens-e-credenciais)
- [12. Sistema operacional e runtime](#12-sistema-operacional-e-runtime)
- [13. Performance e paralelismo](#13-performance-e-paralelismo)
- [14. Paths e dependências gerais](#14-paths-e-dependências-gerais)
- [15. Inventário consolidado](#15-inventário-consolidado)
- [16. Apêndice — dump bruto integral](#16-apêndice--dump-bruto-integral)

## 3. Visão geral

O arquivo registra **60 variáveis de ambiente**. A documentação as distribui em **11 categorias técnicas** apenas para facilitar navegação; a categorização não altera os valores originais.

| Categoria | Quantidade de variáveis |
|---|---:|
| Identificação do ambiente e projeto | 5 |
| Aplicação e sessão | 4 |
| Hadoop | 6 |
| YARN, container e NodeManager | 13 |
| Spark e Livy | 7 |
| Java e JVM | 3 |
| Python e PySpark | 6 |
| Autenticação, tokens e credenciais | 3 |
| Sistema operacional e runtime | 7 |
| Performance e paralelismo | 3 |
| Paths e dependências gerais | 3 |
| **Total** | **60** |

### Valores compostos detectados

| Variável | Estrutura | Itens | Vazios | Duplicados adicionais |
|---|---|---:|---:|---:|
| `CLASSPATH` | separada por `:` | 242 | 1 | 1 |
| `SPARK_DIST_CLASSPATH` | separada por `:` | 226 | 0 | 0 |
| `PYTHONPATH` | separada por `:` | 8 | 0 | 2 |
| `PATH` | separada por `:` | 2 | 0 | 0 |
| `LD_LIBRARY_PATH` | separada por `:` | 2 | 1 | 0 |
| `JDK_JAVA_OPTIONS` | opções separadas por espaço | 3 | 0 | 0 |

## 4. Identificação do ambiente e projeto

Variáveis classificadas nesta seção: **5**.

### `AMBIENTE`

| Propriedade | Valor |
|---|---|
| Linha no arquivo-fonte | `2` |
| Categoria documental | Identificação do ambiente e projeto |
| Representação | atribuição simples |
| Comprimento do valor | `8` caracteres |

#### Valor

```text
PRODUCAO
```

#### Atribuição original exata

```text
AMBIENTE=PRODUCAO
```

### `DOMINIO`

| Propriedade | Valor |
|---|---|
| Linha no arquivo-fonte | `8` |
| Categoria documental | Identificação do ambiente e projeto |
| Representação | atribuição simples |
| Comprimento do valor | `3` caracteres |

#### Valor

```text
t2i
```

#### Atribuição original exata

```text
DOMINIO=t2i
```

### `HOJE`

| Propriedade | Valor |
|---|---|
| Linha no arquivo-fonte | `16` |
| Categoria documental | Identificação do ambiente e projeto |
| Representação | atribuição simples |
| Comprimento do valor | `10` caracteres |

#### Valor

```text
2026-07-01
```

#### Atribuição original exata

```text
HOJE=2026-07-01
```

### `MODEL_NAME`

| Propriedade | Valor |
|---|---|
| Linha no arquivo-fonte | `31` |
| Categoria documental | Identificação do ambiente e projeto |
| Representação | atribuição simples |
| Comprimento do valor | `35` caracteres |

#### Valor

```text
t2i_mf_etl_vinculacao_meus_insights
```

#### Atribuição original exata

```text
MODEL_NAME=t2i_mf_etl_vinculacao_meus_insights
```

### `PROJECT_ID`

| Propriedade | Valor |
|---|---|
| Linha no arquivo-fonte | `42` |
| Categoria documental | Identificação do ambiente e projeto |
| Representação | atribuição simples |
| Comprimento do valor | `36` caracteres |

#### Valor

```text
663d3236-46ba-4ea8-bc96-51c694d548c3
```

#### Atribuição original exata

```text
PROJECT_ID=663d3236-46ba-4ea8-bc96-51c694d548c3
```

## 5. Aplicação e sessão

Variáveis classificadas nesta seção: **4**.

### `APPLICATION_WEB_PROXY_BASE`

| Propriedade | Valor |
|---|---|
| Linha no arquivo-fonte | `3` |
| Categoria documental | Aplicação e sessão |
| Representação | atribuição simples |
| Comprimento do valor | `39` caracteres |

#### Valor

```text
/proxy/application_1779574059803_412553
```

#### Atribuição original exata

```text
APPLICATION_WEB_PROXY_BASE=/proxy/application_1779574059803_412553
```

### `APP_SUBMIT_TIME_ENV`

| Propriedade | Valor |
|---|---|
| Linha no arquivo-fonte | `4` |
| Categoria documental | Aplicação e sessão |
| Representação | atribuição simples |
| Comprimento do valor | `13` caracteres |

#### Valor

```text
1782917390993
```

#### Atribuição original exata

```text
APP_SUBMIT_TIME_ENV=1782917390993
```

### `BBMAGIC_SESSION_ID`

| Propriedade | Valor |
|---|---|
| Linha no arquivo-fonte | `5` |
| Categoria documental | Aplicação e sessão |
| Representação | atribuição simples |
| Comprimento do valor | `36` caracteres |

#### Valor

```text
2eaf3761-b6a4-46cd-aeba-752d5677f0f4
```

#### Atribuição original exata

```text
BBMAGIC_SESSION_ID=2eaf3761-b6a4-46cd-aeba-752d5677f0f4
```

### `SESSION_NAME`

| Propriedade | Valor |
|---|---|
| Linha no arquivo-fonte | `51` |
| Categoria documental | Aplicação e sessão |
| Representação | atribuição simples |
| Comprimento do valor | `60` caracteres |

#### Valor

```text
spark_/projeto/hdpt2i.keytab_mf_etl_vinculacao_meus_insights
```

#### Atribuição original exata

```text
SESSION_NAME=spark_/projeto/hdpt2i.keytab_mf_etl_vinculacao_meus_insights
```

## 6. Hadoop

Variáveis classificadas nesta seção: **6**.

### `HADOOP_CLIENT_CONF_DIR`

| Propriedade | Valor |
|---|---|
| Linha no arquivo-fonte | `9` |
| Categoria documental | Hadoop |
| Representação | atribuição simples |
| Comprimento do valor | `31` caracteres |

#### Valor

```text
/etc/hadoop/conf.cloudera.yarn2
```

#### Atribuição original exata

```text
HADOOP_CLIENT_CONF_DIR=/etc/hadoop/conf.cloudera.yarn2
```

### `HADOOP_COMMON_HOME`

| Propriedade | Valor |
|---|---|
| Linha no arquivo-fonte | `10` |
| Categoria documental | Hadoop |
| Representação | atribuição simples |
| Comprimento do valor | `68` caracteres |

#### Valor

```text
/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop
```

#### Atribuição original exata

```text
HADOOP_COMMON_HOME=/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop
```

### `HADOOP_HDFS_HOME`

| Propriedade | Valor |
|---|---|
| Linha no arquivo-fonte | `11` |
| Categoria documental | Hadoop |
| Representação | atribuição simples |
| Comprimento do valor | `73` caracteres |

#### Valor

```text
/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop-hdfs
```

#### Atribuição original exata

```text
HADOOP_HDFS_HOME=/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop-hdfs
```

### `HADOOP_HOME`

| Propriedade | Valor |
|---|---|
| Linha no arquivo-fonte | `12` |
| Categoria documental | Hadoop |
| Representação | atribuição simples |
| Comprimento do valor | `68` caracteres |

#### Valor

```text
/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop
```

#### Atribuição original exata

```text
HADOOP_HOME=/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop
```

### `HADOOP_MAPRED_HOME`

| Propriedade | Valor |
|---|---|
| Linha no arquivo-fonte | `13` |
| Categoria documental | Hadoop |
| Representação | atribuição simples |
| Comprimento do valor | `78` caracteres |

#### Valor

```text
/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop-mapreduce
```

#### Atribuição original exata

```text
HADOOP_MAPRED_HOME=/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop-mapreduce
```

### `HADOOP_YARN_HOME`

| Propriedade | Valor |
|---|---|
| Linha no arquivo-fonte | `15` |
| Categoria documental | Hadoop |
| Representação | atribuição simples |
| Comprimento do valor | `73` caracteres |

#### Valor

```text
/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop-yarn
```

#### Atribuição original exata

```text
HADOOP_YARN_HOME=/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop-yarn
```

## 7. YARN, container e NodeManager

Variáveis classificadas nesta seção: **13**.

### `CONTAINER_ID`

| Propriedade | Valor |
|---|---|
| Linha no arquivo-fonte | `7` |
| Categoria documental | YARN, container e NodeManager |
| Representação | atribuição simples |
| Comprimento do valor | `45` caracteres |

#### Valor

```text
container_e396_1779574059803_412553_01_000001
```

#### Atribuição original exata

```text
CONTAINER_ID=container_e396_1779574059803_412553_01_000001
```

### `LOCAL_DIRS`

| Propriedade | Valor |
|---|---|
| Linha no arquivo-fonte | `25` |
| Categoria documental | YARN, container e NodeManager |
| Representação | atribuição simples |
| Comprimento do valor | `74` caracteres |

#### Valor

```text
/data22/yarn/nm/usercache/hdpt2i/appcache/application_1779574059803_412553
```

#### Atribuição original exata

```text
LOCAL_DIRS=/data22/yarn/nm/usercache/hdpt2i/appcache/application_1779574059803_412553
```

### `LOCAL_USER_DIRS`

| Propriedade | Valor |
|---|---|
| Linha no arquivo-fonte | `26` |
| Categoria documental | YARN, container e NodeManager |
| Representação | atribuição simples |
| Comprimento do valor | `33` caracteres |

#### Valor

```text
/data22/yarn/nm/usercache/hdpt2i/
```

#### Atribuição original exata

```text
LOCAL_USER_DIRS=/data22/yarn/nm/usercache/hdpt2i/
```

### `LOG_DIRS`

| Propriedade | Valor |
|---|---|
| Linha no arquivo-fonte | `28` |
| Categoria documental | YARN, container e NodeManager |
| Representação | atribuição simples |
| Comprimento do valor | `106` caracteres |

#### Valor

```text
/data22/yarn/container-logs/application_1779574059803_412553/container_e396_1779574059803_412553_01_000001
```

#### Atribuição original exata

```text
LOG_DIRS=/data22/yarn/container-logs/application_1779574059803_412553/container_e396_1779574059803_412553_01_000001
```

### `NM_AUX_SERVICE_mapreduce_shuffle`

| Propriedade | Valor |
|---|---|
| Linha no arquivo-fonte | `32` |
| Categoria documental | YARN, container e NodeManager |
| Representação | atribuição simples |
| Comprimento do valor | `44` caracteres |

#### Valor

```text
AAA0+gAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA=
```

#### Atribuição original exata

```text
NM_AUX_SERVICE_mapreduce_shuffle=AAA0+gAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA=
```

### `NM_AUX_SERVICE_spark3_shuffle`

| Propriedade | Valor |
|---|---|
| Linha no arquivo-fonte | `33` |
| Categoria documental | YARN, container e NodeManager |
| Representação | valor vazio |
| Estado do valor | **Vazio (`NOME=`)** |

#### Valor

O valor está definido como **vazio** no arquivo-fonte.

#### Atribuição original exata

```text
NM_AUX_SERVICE_spark3_shuffle=
```

### `NM_AUX_SERVICE_spark_shuffle`

| Propriedade | Valor |
|---|---|
| Linha no arquivo-fonte | `34` |
| Categoria documental | YARN, container e NodeManager |
| Representação | valor vazio |
| Estado do valor | **Vazio (`NOME=`)** |

#### Valor

O valor está definido como **vazio** no arquivo-fonte.

#### Atribuição original exata

```text
NM_AUX_SERVICE_spark_shuffle=
```

### `NM_HOST`

| Propriedade | Valor |
|---|---|
| Linha no arquivo-fonte | `35` |
| Categoria documental | YARN, container e NodeManager |
| Representação | atribuição simples |
| Comprimento do valor | `29` caracteres |

#### Valor

```text
xfd691.dispositivos.bb.com.br
```

#### Atribuição original exata

```text
NM_HOST=xfd691.dispositivos.bb.com.br
```

### `NM_HTTP_PORT`

| Propriedade | Valor |
|---|---|
| Linha no arquivo-fonte | `36` |
| Categoria documental | YARN, container e NodeManager |
| Representação | atribuição simples |
| Comprimento do valor | `4` caracteres |

#### Valor

```text
8042
```

#### Atribuição original exata

```text
NM_HTTP_PORT=8042
```

### `NM_PORT`

| Propriedade | Valor |
|---|---|
| Linha no arquivo-fonte | `37` |
| Categoria documental | YARN, container e NodeManager |
| Representação | atribuição simples |
| Comprimento do valor | `4` caracteres |

#### Valor

```text
8041
```

#### Atribuição original exata

```text
NM_PORT=8041
```

### `PRELAUNCH_ERR`

| Propriedade | Valor |
|---|---|
| Linha no arquivo-fonte | `40` |
| Categoria documental | YARN, container e NodeManager |
| Representação | atribuição simples |
| Comprimento do valor | `120` caracteres |

#### Valor

```text
/data22/yarn/container-logs/application_1779574059803_412553/container_e396_1779574059803_412553_01_000001/prelaunch.err
```

#### Atribuição original exata

```text
PRELAUNCH_ERR=/data22/yarn/container-logs/application_1779574059803_412553/container_e396_1779574059803_412553_01_000001/prelaunch.err
```

### `PRELAUNCH_OUT`

| Propriedade | Valor |
|---|---|
| Linha no arquivo-fonte | `41` |
| Categoria documental | YARN, container e NodeManager |
| Representação | atribuição simples |
| Comprimento do valor | `120` caracteres |

#### Valor

```text
/data22/yarn/container-logs/application_1779574059803_412553/container_e396_1779574059803_412553_01_000001/prelaunch.out
```

#### Atribuição original exata

```text
PRELAUNCH_OUT=/data22/yarn/container-logs/application_1779574059803_412553/container_e396_1779574059803_412553_01_000001/prelaunch.out
```

### `PWD`

| Propriedade | Valor |
|---|---|
| Linha no arquivo-fonte | `43` |
| Categoria documental | YARN, container e NodeManager |
| Representação | atribuição simples |
| Comprimento do valor | `120` caracteres |

#### Valor

```text
/data22/yarn/nm/usercache/hdpt2i/appcache/application_1779574059803_412553/container_e396_1779574059803_412553_01_000001
```

#### Atribuição original exata

```text
PWD=/data22/yarn/nm/usercache/hdpt2i/appcache/application_1779574059803_412553/container_e396_1779574059803_412553_01_000001
```

## 8. Spark e Livy

Variáveis classificadas nesta seção: **7**.

### `LIVY_SPARK_MAJOR_VERSION`

| Propriedade | Valor |
|---|---|
| Linha no arquivo-fonte | `24` |
| Categoria documental | Spark e Livy |
| Representação | atribuição simples |
| Comprimento do valor | `1` caracteres |

#### Valor

```text
3
```

#### Atribuição original exata

```text
LIVY_SPARK_MAJOR_VERSION=3
```

### `SPARK_AUTH_SOCKET_TIMEOUT`

| Propriedade | Valor |
|---|---|
| Linha no arquivo-fonte | `53` |
| Categoria documental | Spark e Livy |
| Representação | atribuição simples |
| Comprimento do valor | `2` caracteres |

#### Valor

```text
15
```

#### Atribuição original exata

```text
SPARK_AUTH_SOCKET_TIMEOUT=15
```

### `SPARK_BUFFER_SIZE`

| Propriedade | Valor |
|---|---|
| Linha no arquivo-fonte | `54` |
| Categoria documental | Spark e Livy |
| Representação | atribuição simples |
| Comprimento do valor | `5` caracteres |

#### Valor

```text
65536
```

#### Atribuição original exata

```text
SPARK_BUFFER_SIZE=65536
```

### `SPARK_DIST_CLASSPATH`

| Propriedade | Valor |
|---|---|
| Linha no arquivo-fonte | `55` |
| Categoria documental | Spark e Livy |
| Representação | lista separada por `:` |
| Comprimento do valor | `23412` caracteres |

#### Estrutura interna

O valor original foi decomposto **somente para visualização** usando `:` como separador. Foram encontradas **226 posições**.

| # | Entrada | Observação |
|---:|---|---|
| 1 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/avro.jar` |  |
| 2 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/aws-java-sdk-bundle-1.12.599.jar` |  |
| 3 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/aws-java-sdk-bundle.jar` |  |
| 4 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/azure-data-lake-store-sdk-2.3.6.jar` |  |
| 5 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/azure-data-lake-store-sdk.jar` |  |
| 6 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/checker-qual-3.33.0.jar` |  |
| 7 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/checker-qual.jar` |  |
| 8 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/commons-beanutils-1.9.4.jar` |  |
| 9 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/commons-beanutils.jar` |  |
| 10 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/commons-cli-1.2.jar` |  |
| 11 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/commons-cli.jar` |  |
| 12 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/commons-codec-1.14.jar` |  |
| 13 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/commons-codec.jar` |  |
| 14 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/commons-collections-3.2.2.jar` |  |
| 15 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/commons-collections.jar` |  |
| 16 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/commons-compress-1.23.0.jar` |  |
| 17 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/commons-compress.jar` |  |
| 18 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/commons-configuration2-2.10.1.jar` |  |
| 19 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/commons-configuration2.jar` |  |
| 20 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/commons-io-2.11.0.jar` |  |
| 21 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/commons-io.jar` |  |
| 22 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/commons-lang-2.6.jar` |  |
| 23 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/commons-lang3-3.8.1.jar` |  |
| 24 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/commons-lang3.jar` |  |
| 25 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/commons-lang.jar` |  |
| 26 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/commons-logging-1.1.3.jar` |  |
| 27 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/commons-logging.jar` |  |
| 28 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/commons-math3-3.1.1.jar` |  |
| 29 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/commons-math3.jar` |  |
| 30 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/commons-net-3.9.0.jar` |  |
| 31 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/commons-net.jar` |  |
| 32 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/commons-text-1.10.0.jar` |  |
| 33 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/commons-text.jar` |  |
| 34 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/curator-client-5.4.0.7.1.9.1000-103.jar` |  |
| 35 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/curator-client.jar` |  |
| 36 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/curator-framework-5.4.0.7.1.9.1000-103.jar` |  |
| 37 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/curator-framework.jar` |  |
| 38 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/curator-recipes-5.4.0.7.1.9.1000-103.jar` |  |
| 39 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/curator-recipes.jar` |  |
| 40 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/failureaccess-1.0.1.jar` |  |
| 41 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/failureaccess.jar` |  |
| 42 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/gson-2.9.0.jar` |  |
| 43 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/gson.jar` |  |
| 44 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/guava-32.0.1-jre.jar` |  |
| 45 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/guava.jar` |  |
| 46 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/hadoop-annotations-3.1.1.7.1.9.1000-103.jar` |  |
| 47 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/hadoop-annotations.jar` |  |
| 48 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/hadoop-auth-3.1.1.7.1.9.1000-103.jar` |  |
| 49 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/hadoop-auth.jar` |  |
| 50 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/hadoop-aws-3.1.1.7.1.9.1000-103.jar` |  |
| 51 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/hadoop-aws.jar` |  |
| 52 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/hadoop-azure-3.1.1.7.1.9.1000-103.jar` |  |
| 53 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/hadoop-azure-datalake-3.1.1.7.1.9.1000-103.jar` |  |
| 54 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/hadoop-azure-datalake.jar` |  |
| 55 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/hadoop-azure.jar` |  |
| 56 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/hadoop-common-3.1.1.7.1.9.1000-103.jar` |  |
| 57 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/hadoop-common.jar` |  |
| 58 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/hadoop-hdfs-client-3.1.1.7.1.9.1000-103.jar` |  |
| 59 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/hadoop-hdfs-client.jar` |  |
| 60 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/hadoop-mapreduce-client-common-3.1.1.7.1.9.1000-103.jar` |  |
| 61 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/hadoop-mapreduce-client-common.jar` |  |
| 62 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/hadoop-mapreduce-client-core-3.1.1.7.1.9.1000-103.jar` |  |
| 63 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/hadoop-mapreduce-client-core.jar` |  |
| 64 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/hadoop-mapreduce-client-jobclient-3.1.1.7.1.9.1000-103.jar` |  |
| 65 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/hadoop-mapreduce-client-jobclient.jar` |  |
| 66 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/hadoop-yarn-api-3.1.1.7.1.9.1000-103.jar` |  |
| 67 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/hadoop-yarn-api.jar` |  |
| 68 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/hadoop-yarn-client-3.1.1.7.1.9.1000-103.jar` |  |
| 69 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/hadoop-yarn-client.jar` |  |
| 70 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/hadoop-yarn-common-3.1.1.7.1.9.1000-103.jar` |  |
| 71 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/hadoop-yarn-common.jar` |  |
| 72 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/httpclient-4.5.13.jar` |  |
| 73 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/httpclient.jar` |  |
| 74 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/httpcore-4.4.13.jar` |  |
| 75 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/httpcore.jar` |  |
| 76 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/j2objc-annotations-2.8.jar` |  |
| 77 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/j2objc-annotations.jar` |  |
| 78 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/jakarta.activation-api-1.2.1.jar` |  |
| 79 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/jakarta.activation-api.jar` |  |
| 80 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/jakarta.xml.bind-api-2.3.2.jar` |  |
| 81 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/jakarta.xml.bind-api.jar` |  |
| 82 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/javax.activation-api-1.2.0.jar` |  |
| 83 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/javax.activation-api.jar` |  |
| 84 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/jaxb-api-2.2.11.jar` |  |
| 85 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/jaxb-api.jar` |  |
| 86 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/jcip-annotations-1.0-1.jar` |  |
| 87 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/jcip-annotations.jar` |  |
| 88 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/jline-3.22.0.jar` |  |
| 89 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/jline.jar` |  |
| 90 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/jsp-api-2.1.jar` |  |
| 91 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/jsp-api.jar` |  |
| 92 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/jsr305-3.0.0.jar` |  |
| 93 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/jsr305.jar` |  |
| 94 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/jsr311-api-1.1.1.jar` |  |
| 95 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/jsr311-api.jar` |  |
| 96 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/kerb-admin-2.0.3.jar` |  |
| 97 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/kerb-admin.jar` |  |
| 98 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/kerb-client-2.0.3.jar` |  |
| 99 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/kerb-client.jar` |  |
| 100 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/kerb-common-2.0.3.jar` |  |
| 101 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/kerb-common.jar` |  |
| 102 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/kerb-core-2.0.3.jar` |  |
| 103 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/kerb-core.jar` |  |
| 104 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/kerb-crypto-2.0.3.jar` |  |
| 105 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/kerb-crypto.jar` |  |
| 106 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/kerb-identity-2.0.3.jar` |  |
| 107 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/kerb-identity.jar` |  |
| 108 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/kerb-server-2.0.3.jar` |  |
| 109 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/kerb-server.jar` |  |
| 110 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/kerb-simplekdc-2.0.3.jar` |  |
| 111 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/kerb-simplekdc.jar` |  |
| 112 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/kerb-util-2.0.3.jar` |  |
| 113 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/kerb-util.jar` |  |
| 114 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/kerby-asn1-2.0.3.jar` |  |
| 115 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/kerby-asn1.jar` |  |
| 116 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/kerby-config-2.0.3.jar` |  |
| 117 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/kerby-config.jar` |  |
| 118 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/kerby-pkix-2.0.3.jar` |  |
| 119 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/kerby-pkix.jar` |  |
| 120 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/kerby-util-2.0.3.jar` |  |
| 121 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/kerby-util.jar` |  |
| 122 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/kerby-xdr-2.0.3.jar` |  |
| 123 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/kerby-xdr.jar` |  |
| 124 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/kotlin-stdlib-jdk7-1.8.0.jar` |  |
| 125 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/kotlin-stdlib-jdk7.jar` |  |
| 126 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/kotlin-stdlib-jdk8-1.8.0.jar` |  |
| 127 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/kotlin-stdlib-jdk8.jar` |  |
| 128 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/listenablefuture-9999.0-empty-to-avoid-conflict-with-guava.jar` |  |
| 129 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/listenablefuture.jar` |  |
| 130 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/lz4-java-1.7.1.jar` |  |
| 131 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/lz4-java.jar` |  |
| 132 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/metrics-core-3.2.4.jar` |  |
| 133 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/metrics-core.jar` |  |
| 134 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-all-4.1.100.Final.jar` |  |
| 135 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-all.jar` |  |
| 136 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-buffer-4.1.100.Final.jar` |  |
| 137 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-buffer.jar` |  |
| 138 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-codec-4.1.100.Final.jar` |  |
| 139 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-codec-dns-4.1.100.Final.jar` |  |
| 140 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-codec-dns.jar` |  |
| 141 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-codec-haproxy-4.1.100.Final.jar` |  |
| 142 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-codec-haproxy.jar` |  |
| 143 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-codec-http2-4.1.100.Final.jar` |  |
| 144 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-codec-http2.jar` |  |
| 145 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-codec-http-4.1.100.Final.jar` |  |
| 146 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-codec-http.jar` |  |
| 147 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-codec.jar` |  |
| 148 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-codec-memcache-4.1.100.Final.jar` |  |
| 149 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-codec-memcache.jar` |  |
| 150 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-codec-mqtt-4.1.100.Final.jar` |  |
| 151 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-codec-mqtt.jar` |  |
| 152 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-codec-redis-4.1.100.Final.jar` |  |
| 153 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-codec-redis.jar` |  |
| 154 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-codec-smtp-4.1.100.Final.jar` |  |
| 155 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-codec-smtp.jar` |  |
| 156 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-codec-socks-4.1.100.Final.jar` |  |
| 157 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-codec-socks.jar` |  |
| 158 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-codec-stomp-4.1.100.Final.jar` |  |
| 159 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-codec-stomp.jar` |  |
| 160 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-codec-xml-4.1.100.Final.jar` |  |
| 161 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-codec-xml.jar` |  |
| 162 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-common-4.1.100.Final.jar` |  |
| 163 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-common.jar` |  |
| 164 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-handler-4.1.100.Final.jar` |  |
| 165 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-handler.jar` |  |
| 166 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-handler-proxy-4.1.100.Final.jar` |  |
| 167 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-handler-proxy.jar` |  |
| 168 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-handler-ssl-ocsp-4.1.100.Final.jar` |  |
| 169 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-handler-ssl-ocsp.jar` |  |
| 170 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-resolver-4.1.100.Final.jar` |  |
| 171 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-resolver-dns-4.1.100.Final.jar` |  |
| 172 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-resolver-dns-classes-macos-4.1.100.Final.jar` |  |
| 173 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-resolver-dns-classes-macos.jar` |  |
| 174 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-resolver-dns.jar` |  |
| 175 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-resolver-dns-native-macos-4.1.100.Final-osx-aarch_64.jar` |  |
| 176 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-resolver-dns-native-macos-4.1.100.Final-osx-x86_64.jar` |  |
| 177 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-resolver-dns-native-macos.jar` |  |
| 178 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-resolver.jar` |  |
| 179 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-transport-4.1.100.Final.jar` |  |
| 180 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-transport-classes-epoll-4.1.100.Final.jar` |  |
| 181 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-transport-classes-epoll.jar` |  |
| 182 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-transport-classes-kqueue-4.1.100.Final.jar` |  |
| 183 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-transport-classes-kqueue.jar` |  |
| 184 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-transport.jar` |  |
| 185 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-transport-native-epoll-4.1.100.Final-linux-aarch_64.jar` |  |
| 186 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-transport-native-epoll-4.1.100.Final-linux-x86_64.jar` |  |
| 187 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-transport-native-epoll.jar` |  |
| 188 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-transport-native-kqueue-4.1.100.Final-osx-aarch_64.jar` |  |
| 189 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-transport-native-kqueue-4.1.100.Final-osx-x86_64.jar` |  |
| 190 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-transport-native-kqueue.jar` |  |
| 191 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-transport-native-unix-common-4.1.100.Final.jar` |  |
| 192 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-transport-native-unix-common.jar` |  |
| 193 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-transport-rxtx-4.1.100.Final.jar` |  |
| 194 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-transport-rxtx.jar` |  |
| 195 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-transport-sctp-4.1.100.Final.jar` |  |
| 196 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-transport-sctp.jar` |  |
| 197 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-transport-udt-4.1.100.Final.jar` |  |
| 198 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-transport-udt.jar` |  |
| 199 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/nimbus-jose-jwt-9.37.2.jar` |  |
| 200 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/nimbus-jose-jwt.jar` |  |
| 201 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/okio-jvm-3.4.0.jar` |  |
| 202 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/okio-jvm.jar` |  |
| 203 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/protobuf-java-2.5.0.jar` |  |
| 204 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/protobuf-java.jar` |  |
| 205 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/re2j-1.2.jar` |  |
| 206 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/re2j.jar` |  |
| 207 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/reload4j-1.2.22.jar` |  |
| 208 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/reload4j.jar` |  |
| 209 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/snappy-java-1.1.10.5.jar` |  |
| 210 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/snappy-java.jar` |  |
| 211 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/stax2-api-4.2.1.jar` |  |
| 212 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/stax2-api.jar` |  |
| 213 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/token-provider-2.0.3.jar` |  |
| 214 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/token-provider.jar` |  |
| 215 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/wildfly-openssl-1.1.3.Final.jar` |  |
| 216 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/wildfly-openssl.jar` |  |
| 217 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/woodstox-core-5.4.0.jar` |  |
| 218 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/woodstox-core.jar` |  |
| 219 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop-ozone/share/ozone/lib/ozone-filesystem-hadoop3-1.4.0.7.1.9.1000-103.jar` |  |
| 220 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hbase/bin/../lib/client-facing-thirdparty/audience-annotations-0.12.0.jar` |  |
| 221 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hbase/bin/../lib/client-facing-thirdparty/commons-logging-1.2.jar` |  |
| 222 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hbase/bin/../lib/client-facing-thirdparty/opentelemetry-api-0.12.0.jar` |  |
| 223 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hbase/bin/../lib/client-facing-thirdparty/opentelemetry-context-0.12.0.jar` |  |
| 224 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hbase/bin/../lib/shaded-clients/hbase-shaded-mapreduce-2.4.17.7.1.9.1000-103.jar` |  |
| 225 | `/opt/cloudera/parcels/SPARK3-3.3.2.3.3.7190.0-91-1.p0.45265883/lib/spark3/../iceberg/iceberg-hive-runtime-1.3.0.3.3.7190.0-91.jar` |  |
| 226 | `/opt/cloudera/parcels/SPARK3-3.3.2.3.3.7190.0-91-1.p0.45265883/lib/spark3/../iceberg/iceberg-spark-runtime-3.3_2.12-1.3.0.3.3.7190.0-91.jar` |  |

#### Atribuição original exata

```text
SPARK_DIST_CLASSPATH=/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/avro.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/aws-java-sdk-bundle-1.12.599.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/aws-java-sdk-bundle.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/azure-data-lake-store-sdk-2.3.6.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/azure-data-lake-store-sdk.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/checker-qual-3.33.0.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/checker-qual.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/commons-beanutils-1.9.4.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/commons-beanutils.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/commons-cli-1.2.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/commons-cli.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/commons-codec-1.14.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/commons-codec.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/commons-collections-3.2.2.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/commons-collections.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/commons-compress-1.23.0.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/commons-compress.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/commons-configuration2-2.10.1.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/commons-configuration2.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/commons-io-2.11.0.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/commons-io.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/commons-lang-2.6.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/commons-lang3-3.8.1.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/commons-lang3.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/commons-lang.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/commons-logging-1.1.3.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/commons-logging.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/commons-math3-3.1.1.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/commons-math3.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/commons-net-3.9.0.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/commons-net.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/commons-text-1.10.0.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/commons-text.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/curator-client-5.4.0.7.1.9.1000-103.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/curator-client.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/curator-framework-5.4.0.7.1.9.1000-103.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/curator-framework.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/curator-recipes-5.4.0.7.1.9.1000-103.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/curator-recipes.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/failureaccess-1.0.1.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/failureaccess.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/gson-2.9.0.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/gson.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/guava-32.0.1-jre.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/guava.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/hadoop-annotations-3.1.1.7.1.9.1000-103.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/hadoop-annotations.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/hadoop-auth-3.1.1.7.1.9.1000-103.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/hadoop-auth.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/hadoop-aws-3.1.1.7.1.9.1000-103.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/hadoop-aws.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/hadoop-azure-3.1.1.7.1.9.1000-103.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/hadoop-azure-datalake-3.1.1.7.1.9.1000-103.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/hadoop-azure-datalake.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/hadoop-azure.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/hadoop-common-3.1.1.7.1.9.1000-103.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/hadoop-common.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/hadoop-hdfs-client-3.1.1.7.1.9.1000-103.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/hadoop-hdfs-client.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/hadoop-mapreduce-client-common-3.1.1.7.1.9.1000-103.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/hadoop-mapreduce-client-common.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/hadoop-mapreduce-client-core-3.1.1.7.1.9.1000-103.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/hadoop-mapreduce-client-core.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/hadoop-mapreduce-client-jobclient-3.1.1.7.1.9.1000-103.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/hadoop-mapreduce-client-jobclient.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/hadoop-yarn-api-3.1.1.7.1.9.1000-103.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/hadoop-yarn-api.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/hadoop-yarn-client-3.1.1.7.1.9.1000-103.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/hadoop-yarn-client.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/hadoop-yarn-common-3.1.1.7.1.9.1000-103.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/hadoop-yarn-common.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/httpclient-4.5.13.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/httpclient.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/httpcore-4.4.13.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/httpcore.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/j2objc-annotations-2.8.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/j2objc-annotations.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/jakarta.activation-api-1.2.1.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/jakarta.activation-api.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/jakarta.xml.bind-api-2.3.2.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/jakarta.xml.bind-api.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/javax.activation-api-1.2.0.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/javax.activation-api.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/jaxb-api-2.2.11.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/jaxb-api.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/jcip-annotations-1.0-1.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/jcip-annotations.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/jline-3.22.0.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/jline.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/jsp-api-2.1.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/jsp-api.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/jsr305-3.0.0.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/jsr305.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/jsr311-api-1.1.1.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/jsr311-api.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/kerb-admin-2.0.3.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/kerb-admin.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/kerb-client-2.0.3.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/kerb-client.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/kerb-common-2.0.3.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/kerb-common.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/kerb-core-2.0.3.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/kerb-core.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/kerb-crypto-2.0.3.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/kerb-crypto.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/kerb-identity-2.0.3.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/kerb-identity.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/kerb-server-2.0.3.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/kerb-server.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/kerb-simplekdc-2.0.3.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/kerb-simplekdc.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/kerb-util-2.0.3.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/kerb-util.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/kerby-asn1-2.0.3.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/kerby-asn1.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/kerby-config-2.0.3.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/kerby-config.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/kerby-pkix-2.0.3.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/kerby-pkix.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/kerby-util-2.0.3.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/kerby-util.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/kerby-xdr-2.0.3.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/kerby-xdr.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/kotlin-stdlib-jdk7-1.8.0.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/kotlin-stdlib-jdk7.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/kotlin-stdlib-jdk8-1.8.0.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/kotlin-stdlib-jdk8.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/listenablefuture-9999.0-empty-to-avoid-conflict-with-guava.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/listenablefuture.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/lz4-java-1.7.1.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/lz4-java.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/metrics-core-3.2.4.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/metrics-core.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-all-4.1.100.Final.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-all.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-buffer-4.1.100.Final.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-buffer.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-codec-4.1.100.Final.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-codec-dns-4.1.100.Final.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-codec-dns.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-codec-haproxy-4.1.100.Final.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-codec-haproxy.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-codec-http2-4.1.100.Final.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-codec-http2.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-codec-http-4.1.100.Final.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-codec-http.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-codec.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-codec-memcache-4.1.100.Final.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-codec-memcache.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-codec-mqtt-4.1.100.Final.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-codec-mqtt.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-codec-redis-4.1.100.Final.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-codec-redis.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-codec-smtp-4.1.100.Final.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-codec-smtp.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-codec-socks-4.1.100.Final.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-codec-socks.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-codec-stomp-4.1.100.Final.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-codec-stomp.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-codec-xml-4.1.100.Final.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-codec-xml.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-common-4.1.100.Final.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-common.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-handler-4.1.100.Final.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-handler.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-handler-proxy-4.1.100.Final.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-handler-proxy.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-handler-ssl-ocsp-4.1.100.Final.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-handler-ssl-ocsp.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-resolver-4.1.100.Final.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-resolver-dns-4.1.100.Final.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-resolver-dns-classes-macos-4.1.100.Final.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-resolver-dns-classes-macos.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-resolver-dns.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-resolver-dns-native-macos-4.1.100.Final-osx-aarch_64.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-resolver-dns-native-macos-4.1.100.Final-osx-x86_64.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-resolver-dns-native-macos.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-resolver.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-transport-4.1.100.Final.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-transport-classes-epoll-4.1.100.Final.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-transport-classes-epoll.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-transport-classes-kqueue-4.1.100.Final.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-transport-classes-kqueue.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-transport.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-transport-native-epoll-4.1.100.Final-linux-aarch_64.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-transport-native-epoll-4.1.100.Final-linux-x86_64.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-transport-native-epoll.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-transport-native-kqueue-4.1.100.Final-osx-aarch_64.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-transport-native-kqueue-4.1.100.Final-osx-x86_64.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-transport-native-kqueue.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-transport-native-unix-common-4.1.100.Final.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-transport-native-unix-common.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-transport-rxtx-4.1.100.Final.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-transport-rxtx.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-transport-sctp-4.1.100.Final.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-transport-sctp.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-transport-udt-4.1.100.Final.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-transport-udt.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/nimbus-jose-jwt-9.37.2.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/nimbus-jose-jwt.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/okio-jvm-3.4.0.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/okio-jvm.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/protobuf-java-2.5.0.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/protobuf-java.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/re2j-1.2.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/re2j.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/reload4j-1.2.22.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/reload4j.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/snappy-java-1.1.10.5.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/snappy-java.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/stax2-api-4.2.1.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/stax2-api.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/token-provider-2.0.3.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/token-provider.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/wildfly-openssl-1.1.3.Final.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/wildfly-openssl.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/woodstox-core-5.4.0.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/woodstox-core.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop-ozone/share/ozone/lib/ozone-filesystem-hadoop3-1.4.0.7.1.9.1000-103.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hbase/bin/../lib/client-facing-thirdparty/audience-annotations-0.12.0.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hbase/bin/../lib/client-facing-thirdparty/commons-logging-1.2.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hbase/bin/../lib/client-facing-thirdparty/opentelemetry-api-0.12.0.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hbase/bin/../lib/client-facing-thirdparty/opentelemetry-context-0.12.0.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hbase/bin/../lib/shaded-clients/hbase-shaded-mapreduce-2.4.17.7.1.9.1000-103.jar:/opt/cloudera/parcels/SPARK3-3.3.2.3.3.7190.0-91-1.p0.45265883/lib/spark3/../iceberg/iceberg-hive-runtime-1.3.0.3.3.7190.0-91.jar:/opt/cloudera/parcels/SPARK3-3.3.2.3.3.7190.0-91-1.p0.45265883/lib/spark3/../iceberg/iceberg-spark-runtime-3.3_2.12-1.3.0.3.3.7190.0-91.jar
```

### `SPARK_HOME`

| Propriedade | Valor |
|---|---|
| Linha no arquivo-fonte | `56` |
| Categoria documental | Spark e Livy |
| Representação | atribuição simples |
| Comprimento do valor | `1` caracteres |

#### Valor

```text
.
```

#### Atribuição original exata

```text
SPARK_HOME=.
```

### `SPARK_USER`

| Propriedade | Valor |
|---|---|
| Linha no arquivo-fonte | `57` |
| Categoria documental | Spark e Livy |
| Representação | atribuição simples |
| Comprimento do valor | `6` caracteres |

#### Valor

```text
hdpt2i
```

#### Atribuição original exata

```text
SPARK_USER=hdpt2i
```

### `SPARK_YARN_STAGING_DIR`

| Propriedade | Valor |
|---|---|
| Linha no arquivo-fonte | `58` |
| Categoria documental | Spark e Livy |
| Representação | atribuição simples |
| Comprimento do valor | `88` caracteres |

#### Valor

```text
hdfs:/tmp/spark/yarn/.sparkStaging/hdpt2i/.sparkStaging/application_1779574059803_412553
```

#### Atribuição original exata

```text
SPARK_YARN_STAGING_DIR=hdfs:/tmp/spark/yarn/.sparkStaging/hdpt2i/.sparkStaging/application_1779574059803_412553
```

## 9. Java e JVM

Variáveis classificadas nesta seção: **3**.

### `JAVA_HOME`

| Propriedade | Valor |
|---|---|
| Linha no arquivo-fonte | `18` |
| Categoria documental | Java e JVM |
| Representação | atribuição simples |
| Comprimento do valor | `24` caracteres |

#### Valor

```text
/usr/lib/jvm/jre-openjdk
```

#### Atribuição original exata

```text
JAVA_HOME=/usr/lib/jvm/jre-openjdk
```

### `JDK_JAVA_OPTIONS`

| Propriedade | Valor |
|---|---|
| Linha no arquivo-fonte | `19` |
| Categoria documental | Java e JVM |
| Representação | opções JVM separadas por espaço |
| Comprimento do valor | `140` caracteres |

#### Opções JVM

A decomposição abaixo usa espaço como separador apenas para leitura. A atribuição original completa permanece preservada logo depois.

1. `--add-opens=java.base/java.lang=ALL-UNNAMED`
2. `--add-exports=java.base/sun.net.dns=ALL-UNNAMED`
3. `--add-exports=java.base/sun.net.util=ALL-UNNAMED`

#### Atribuição original exata

```text
JDK_JAVA_OPTIONS=--add-opens=java.base/java.lang=ALL-UNNAMED --add-exports=java.base/sun.net.dns=ALL-UNNAMED --add-exports=java.base/sun.net.util=ALL-UNNAMED
```

### `JVM_PID`

| Propriedade | Valor |
|---|---|
| Linha no arquivo-fonte | `20` |
| Categoria documental | Java e JVM |
| Representação | atribuição simples |
| Comprimento do valor | `7` caracteres |

#### Valor

```text
3900365
```

#### Atribuição original exata

```text
JVM_PID=3900365
```

## 10. Python e PySpark

Variáveis classificadas nesta seção: **6**.

### `PYSPARK_DRIVER_PYTHON`

| Propriedade | Valor |
|---|---|
| Linha no arquivo-fonte | `44` |
| Categoria documental | Python e PySpark |
| Representação | atribuição simples |
| Comprimento do valor | `16` caracteres |

#### Valor

```text
/usr/bin/python3
```

#### Atribuição original exata

```text
PYSPARK_DRIVER_PYTHON=/usr/bin/python3
```

### `PYSPARK_GATEWAY_PORT`

| Propriedade | Valor |
|---|---|
| Linha no arquivo-fonte | `45` |
| Categoria documental | Python e PySpark |
| Representação | atribuição simples |
| Comprimento do valor | `4` caracteres |

#### Valor

```text
7589
```

#### Atribuição original exata

```text
PYSPARK_GATEWAY_PORT=7589
```

### `PYSPARK_PYTHON`

| Propriedade | Valor |
|---|---|
| Linha no arquivo-fonte | `47` |
| Categoria documental | Python e PySpark |
| Representação | atribuição simples |
| Comprimento do valor | `18` caracteres |

#### Valor

```text
/usr/bin/python3.9
```

#### Atribuição original exata

```text
PYSPARK_PYTHON=/usr/bin/python3.9
```

### `PYTHONHASHSEED`

| Propriedade | Valor |
|---|---|
| Linha no arquivo-fonte | `48` |
| Categoria documental | Python e PySpark |
| Representação | atribuição simples |
| Comprimento do valor | `1` caracteres |

#### Valor

```text
0
```

#### Atribuição original exata

```text
PYTHONHASHSEED=0
```

### `PYTHONPATH`

| Propriedade | Valor |
|---|---|
| Linha no arquivo-fonte | `49` |
| Categoria documental | Python e PySpark |
| Representação | lista separada por `:` |
| Comprimento do valor | `841` caracteres |

#### Estrutura interna

O valor original foi decomposto **somente para visualização** usando `:` como separador. Foram encontradas **8 posições**.

| # | Entrada | Observação |
|---:|---|---|
| 1 | `/opt/cloudera/cm-agent/lib/python3.11/site-packages` |  |
| 2 | `/opt/cloudera/cm-agent/thirdparty` |  |
| 3 | `/opt/cloudera/parcels/SPARK3-3.3.2.3.3.7190.0-91-1.p0.45265883/lib/spark3/python/lib/py4j-0.10.9.5-src.zip` |  |
| 4 | `/opt/cloudera/parcels/SPARK3-3.3.2.3.3.7190.0-91-1.p0.45265883/lib/spark3/python/lib/pyspark.zip` |  |
| 5 | `/data22/yarn/nm/usercache/hdpt2i/appcache/application_1779574059803_412553/container_e396_1779574059803_412553_01_000001/pyspark.zip` | repetida 2x no valor; ocorrência 1/2 |
| 6 | `/data22/yarn/nm/usercache/hdpt2i/appcache/application_1779574059803_412553/container_e396_1779574059803_412553_01_000001/py4j-0.10.9.5-src.zip` | repetida 2x no valor; ocorrência 1/2 |
| 7 | `/data22/yarn/nm/usercache/hdpt2i/appcache/application_1779574059803_412553/container_e396_1779574059803_412553_01_000001/pyspark.zip` | repetida 2x no valor; ocorrência 2/2 |
| 8 | `/data22/yarn/nm/usercache/hdpt2i/appcache/application_1779574059803_412553/container_e396_1779574059803_412553_01_000001/py4j-0.10.9.5-src.zip` | repetida 2x no valor; ocorrência 2/2 |

#### Atribuição original exata

```text
PYTHONPATH=/opt/cloudera/cm-agent/lib/python3.11/site-packages:/opt/cloudera/cm-agent/thirdparty:/opt/cloudera/parcels/SPARK3-3.3.2.3.3.7190.0-91-1.p0.45265883/lib/spark3/python/lib/py4j-0.10.9.5-src.zip:/opt/cloudera/parcels/SPARK3-3.3.2.3.3.7190.0-91-1.p0.45265883/lib/spark3/python/lib/pyspark.zip:/data22/yarn/nm/usercache/hdpt2i/appcache/application_1779574059803_412553/container_e396_1779574059803_412553_01_000001/pyspark.zip:/data22/yarn/nm/usercache/hdpt2i/appcache/application_1779574059803_412553/container_e396_1779574059803_412553_01_000001/py4j-0.10.9.5-src.zip:/data22/yarn/nm/usercache/hdpt2i/appcache/application_1779574059803_412553/container_e396_1779574059803_412553_01_000001/pyspark.zip:/data22/yarn/nm/usercache/hdpt2i/appcache/application_1779574059803_412553/container_e396_1779574059803_412553_01_000001/py4j-0.10.9.5-src.zip
```

### `PYTHONUNBUFFERED`

| Propriedade | Valor |
|---|---|
| Linha no arquivo-fonte | `50` |
| Categoria documental | Python e PySpark |
| Representação | atribuição simples |
| Comprimento do valor | `3` caracteres |

#### Valor

```text
YES
```

#### Atribuição original exata

```text
PYTHONUNBUFFERED=YES
```

## 11. Autenticação, tokens e credenciais

Variáveis classificadas nesta seção: **3**.

### `KEYTAB`

| Propriedade | Valor |
|---|---|
| Linha no arquivo-fonte | `21` |
| Categoria documental | Autenticação, tokens e credenciais |
| Representação | atribuição simples |
| Comprimento do valor | `22` caracteres |

#### Valor

```text
/projeto/hdpt2i.keytab
```

#### Atribuição original exata

```text
KEYTAB=/projeto/hdpt2i.keytab
```

### `HADOOP_TOKEN_FILE_LOCATION`

| Propriedade | Valor |
|---|---|
| Linha no arquivo-fonte | `14` |
| Categoria documental | Autenticação, tokens e credenciais |
| Representação | atribuição simples |
| Comprimento do valor | `137` caracteres |

#### Valor

```text
/data22/yarn/nm/usercache/hdpt2i/appcache/application_1779574059803_412553/container_e396_1779574059803_412553_01_000001/container_tokens
```

#### Atribuição original exata

```text
HADOOP_TOKEN_FILE_LOCATION=/data22/yarn/nm/usercache/hdpt2i/appcache/application_1779574059803_412553/container_e396_1779574059803_412553_01_000001/container_tokens
```

### `PYSPARK_GATEWAY_SECRET`

| Propriedade | Valor |
|---|---|
| Linha no arquivo-fonte | `46` |
| Categoria documental | Autenticação, tokens e credenciais |
| Representação | atribuição simples |
| Comprimento do valor | `44` caracteres |

#### Valor

```text
1oEeFz2vRdzvcMSJdOhzjLfs95kpTMntEiYpssIhBd0=
```

#### Atribuição original exata

```text
PYSPARK_GATEWAY_SECRET=1oEeFz2vRdzvcMSJdOhzjLfs95kpTMntEiYpssIhBd0=
```

## 12. Sistema operacional e runtime

Variáveis classificadas nesta seção: **7**.

### `HOME`

| Propriedade | Valor |
|---|---|
| Linha no arquivo-fonte | `17` |
| Categoria documental | Sistema operacional e runtime |
| Representação | atribuição simples |
| Comprimento do valor | `6` caracteres |

#### Valor

```text
/home/
```

#### Atribuição original exata

```text
HOME=/home/
```

### `LANG`

| Propriedade | Valor |
|---|---|
| Linha no arquivo-fonte | `22` |
| Categoria documental | Sistema operacional e runtime |
| Representação | atribuição simples |
| Comprimento do valor | `11` caracteres |

#### Valor

```text
en_US.UTF-8
```

#### Atribuição original exata

```text
LANG=en_US.UTF-8
```

### `LOGNAME`

| Propriedade | Valor |
|---|---|
| Linha no arquivo-fonte | `27` |
| Categoria documental | Sistema operacional e runtime |
| Representação | atribuição simples |
| Comprimento do valor | `6` caracteres |

#### Valor

```text
hdpt2i
```

#### Atribuição original exata

```text
LOGNAME=hdpt2i
```

### `SHLVL`

| Propriedade | Valor |
|---|---|
| Linha no arquivo-fonte | `52` |
| Categoria documental | Sistema operacional e runtime |
| Representação | atribuição simples |
| Comprimento do valor | `1` caracteres |

#### Valor

```text
1
```

#### Atribuição original exata

```text
SHLVL=1
```

### `USER`

| Propriedade | Valor |
|---|---|
| Linha no arquivo-fonte | `59` |
| Categoria documental | Sistema operacional e runtime |
| Representação | atribuição simples |
| Comprimento do valor | `6` caracteres |

#### Valor

```text
hdpt2i
```

#### Atribuição original exata

```text
USER=hdpt2i
```

### `USE_LOGS`

| Propriedade | Valor |
|---|---|
| Linha no arquivo-fonte | `60` |
| Categoria documental | Sistema operacional e runtime |
| Representação | atribuição simples |
| Comprimento do valor | `4` caracteres |

#### Valor

```text
True
```

#### Atribuição original exata

```text
USE_LOGS=True
```

### `_`

| Propriedade | Valor |
|---|---|
| Linha no arquivo-fonte | `61` |
| Categoria documental | Sistema operacional e runtime |
| Representação | atribuição simples |
| Comprimento do valor | `33` caracteres |

#### Valor

```text
/usr/lib/jvm/jre-openjdk/bin/java
```

#### Atribuição original exata

```text
_=/usr/lib/jvm/jre-openjdk/bin/java
```

## 13. Performance e paralelismo

Variáveis classificadas nesta seção: **3**.

### `MALLOC_ARENA_MAX`

| Propriedade | Valor |
|---|---|
| Linha no arquivo-fonte | `29` |
| Categoria documental | Performance e paralelismo |
| Representação | atribuição simples |
| Comprimento do valor | `1` caracteres |

#### Valor

```text
4
```

#### Atribuição original exata

```text
MALLOC_ARENA_MAX=4
```

### `MKL_NUM_THREADS`

| Propriedade | Valor |
|---|---|
| Linha no arquivo-fonte | `30` |
| Categoria documental | Performance e paralelismo |
| Representação | atribuição simples |
| Comprimento do valor | `1` caracteres |

#### Valor

```text
1
```

#### Atribuição original exata

```text
MKL_NUM_THREADS=1
```

### `OPENBLAS_NUM_THREADS`

| Propriedade | Valor |
|---|---|
| Linha no arquivo-fonte | `38` |
| Categoria documental | Performance e paralelismo |
| Representação | atribuição simples |
| Comprimento do valor | `1` caracteres |

#### Valor

```text
1
```

#### Atribuição original exata

```text
OPENBLAS_NUM_THREADS=1
```

## 14. Paths e dependências gerais

Variáveis classificadas nesta seção: **3**.

### `CLASSPATH`

| Propriedade | Valor |
|---|---|
| Linha no arquivo-fonte | `6` |
| Categoria documental | Paths e dependências gerais |
| Representação | lista separada por `:` |
| Comprimento do valor | `37548` caracteres |

#### Estrutura interna

O valor original foi decomposto **somente para visualização** usando `:` como separador. Foram encontradas **242 posições**.

| # | Entrada | Observação |
|---:|---|---|
| 1 | `/data22/yarn/nm/usercache/hdpt2i/appcache/application_1779574059803_412553/container_e396_1779574059803_412553_01_000001` |  |
| 2 | `/data22/yarn/nm/usercache/hdpt2i/appcache/application_1779574059803_412553/container_e396_1779574059803_412553_01_000001/__spark_conf__` |  |
| 3 | `/data22/yarn/nm/usercache/hdpt2i/appcache/application_1779574059803_412553/container_e396_1779574059803_412553_01_000001/__spark_libs__/*` |  |
| 4 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../SPARK3-3.3.2.3.3.7190.0-91-1.p0.45265883/lib/spark3/jars/*` |  |
| 5 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../SPARK3-3.3.2.3.3.7190.0-91-1.p0.45265883/lib/spark3/hive/*` |  |
| 6 | `/etc/hadoop/conf.cloudera.yarn2` | repetida 2x no valor; ocorrência 1/2 |
| 7 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/*` |  |
| 8 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/lib/*` |  |
| 9 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop-hdfs/*` |  |
| 10 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop-hdfs/lib/*` |  |
| 11 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop-yarn/*` |  |
| 12 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop-yarn/lib/*` |  |
| 13 | `/etc/hadoop/conf.cloudera.yarn2` | repetida 2x no valor; ocorrência 2/2 |
| 14 | `/data22/yarn/nm/usercache/hdpt2i/appcache/application_1779574059803_412553/container_e396_1779574059803_412553_01_000001/mr-framework/*` |  |
| 15 | *(vazio)* | entrada vazia preservada |
| 16 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/avro.jar` |  |
| 17 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/aws-java-sdk-bundle-1.12.599.jar` |  |
| 18 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/aws-java-sdk-bundle.jar` |  |
| 19 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/azure-data-lake-store-sdk-2.3.6.jar` |  |
| 20 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/azure-data-lake-store-sdk.jar` |  |
| 21 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/checker-qual-3.33.0.jar` |  |
| 22 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/checker-qual.jar` |  |
| 23 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/commons-beanutils-1.9.4.jar` |  |
| 24 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/commons-beanutils.jar` |  |
| 25 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/commons-cli-1.2.jar` |  |
| 26 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/commons-cli.jar` |  |
| 27 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/commons-codec-1.14.jar` |  |
| 28 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/commons-codec.jar` |  |
| 29 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/commons-collections-3.2.2.jar` |  |
| 30 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/commons-collections.jar` |  |
| 31 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/commons-compress-1.23.0.jar` |  |
| 32 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/commons-compress.jar` |  |
| 33 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/commons-configuration2-2.10.1.jar` |  |
| 34 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/commons-configuration2.jar` |  |
| 35 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/commons-io-2.11.0.jar` |  |
| 36 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/commons-io.jar` |  |
| 37 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/commons-lang-2.6.jar` |  |
| 38 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/commons-lang3-3.8.1.jar` |  |
| 39 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/commons-lang3.jar` |  |
| 40 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/commons-lang.jar` |  |
| 41 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/commons-logging-1.1.3.jar` |  |
| 42 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/commons-logging.jar` |  |
| 43 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/commons-math3-3.1.1.jar` |  |
| 44 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/commons-math3.jar` |  |
| 45 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/commons-net-3.9.0.jar` |  |
| 46 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/commons-net.jar` |  |
| 47 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/commons-text-1.10.0.jar` |  |
| 48 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/commons-text.jar` |  |
| 49 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/curator-client-5.4.0.7.1.9.1000-103.jar` |  |
| 50 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/curator-client.jar` |  |
| 51 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/curator-framework-5.4.0.7.1.9.1000-103.jar` |  |
| 52 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/curator-framework.jar` |  |
| 53 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/curator-recipes-5.4.0.7.1.9.1000-103.jar` |  |
| 54 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/curator-recipes.jar` |  |
| 55 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/failureaccess-1.0.1.jar` |  |
| 56 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/failureaccess.jar` |  |
| 57 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/gson-2.9.0.jar` |  |
| 58 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/gson.jar` |  |
| 59 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/guava-32.0.1-jre.jar` |  |
| 60 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/guava.jar` |  |
| 61 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/hadoop-annotations-3.1.1.7.1.9.1000-103.jar` |  |
| 62 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/hadoop-annotations.jar` |  |
| 63 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/hadoop-auth-3.1.1.7.1.9.1000-103.jar` |  |
| 64 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/hadoop-auth.jar` |  |
| 65 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/hadoop-aws-3.1.1.7.1.9.1000-103.jar` |  |
| 66 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/hadoop-aws.jar` |  |
| 67 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/hadoop-azure-3.1.1.7.1.9.1000-103.jar` |  |
| 68 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/hadoop-azure-datalake-3.1.1.7.1.9.1000-103.jar` |  |
| 69 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/hadoop-azure-datalake.jar` |  |
| 70 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/hadoop-azure.jar` |  |
| 71 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/hadoop-common-3.1.1.7.1.9.1000-103.jar` |  |
| 72 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/hadoop-common.jar` |  |
| 73 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/hadoop-hdfs-client-3.1.1.7.1.9.1000-103.jar` |  |
| 74 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/hadoop-hdfs-client.jar` |  |
| 75 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/hadoop-mapreduce-client-common-3.1.1.7.1.9.1000-103.jar` |  |
| 76 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/hadoop-mapreduce-client-common.jar` |  |
| 77 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/hadoop-mapreduce-client-core-3.1.1.7.1.9.1000-103.jar` |  |
| 78 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/hadoop-mapreduce-client-core.jar` |  |
| 79 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/hadoop-mapreduce-client-jobclient-3.1.1.7.1.9.1000-103.jar` |  |
| 80 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/hadoop-mapreduce-client-jobclient.jar` |  |
| 81 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/hadoop-yarn-api-3.1.1.7.1.9.1000-103.jar` |  |
| 82 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/hadoop-yarn-api.jar` |  |
| 83 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/hadoop-yarn-client-3.1.1.7.1.9.1000-103.jar` |  |
| 84 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/hadoop-yarn-client.jar` |  |
| 85 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/hadoop-yarn-common-3.1.1.7.1.9.1000-103.jar` |  |
| 86 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/hadoop-yarn-common.jar` |  |
| 87 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/httpclient-4.5.13.jar` |  |
| 88 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/httpclient.jar` |  |
| 89 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/httpcore-4.4.13.jar` |  |
| 90 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/httpcore.jar` |  |
| 91 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/j2objc-annotations-2.8.jar` |  |
| 92 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/j2objc-annotations.jar` |  |
| 93 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/jakarta.activation-api-1.2.1.jar` |  |
| 94 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/jakarta.activation-api.jar` |  |
| 95 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/jakarta.xml.bind-api-2.3.2.jar` |  |
| 96 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/jakarta.xml.bind-api.jar` |  |
| 97 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/javax.activation-api-1.2.0.jar` |  |
| 98 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/javax.activation-api.jar` |  |
| 99 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/jaxb-api-2.2.11.jar` |  |
| 100 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/jaxb-api.jar` |  |
| 101 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/jcip-annotations-1.0-1.jar` |  |
| 102 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/jcip-annotations.jar` |  |
| 103 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/jline-3.22.0.jar` |  |
| 104 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/jline.jar` |  |
| 105 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/jsp-api-2.1.jar` |  |
| 106 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/jsp-api.jar` |  |
| 107 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/jsr305-3.0.0.jar` |  |
| 108 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/jsr305.jar` |  |
| 109 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/jsr311-api-1.1.1.jar` |  |
| 110 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/jsr311-api.jar` |  |
| 111 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/kerb-admin-2.0.3.jar` |  |
| 112 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/kerb-admin.jar` |  |
| 113 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/kerb-client-2.0.3.jar` |  |
| 114 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/kerb-client.jar` |  |
| 115 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/kerb-common-2.0.3.jar` |  |
| 116 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/kerb-common.jar` |  |
| 117 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/kerb-core-2.0.3.jar` |  |
| 118 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/kerb-core.jar` |  |
| 119 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/kerb-crypto-2.0.3.jar` |  |
| 120 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/kerb-crypto.jar` |  |
| 121 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/kerb-identity-2.0.3.jar` |  |
| 122 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/kerb-identity.jar` |  |
| 123 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/kerb-server-2.0.3.jar` |  |
| 124 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/kerb-server.jar` |  |
| 125 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/kerb-simplekdc-2.0.3.jar` |  |
| 126 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/kerb-simplekdc.jar` |  |
| 127 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/kerb-util-2.0.3.jar` |  |
| 128 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/kerb-util.jar` |  |
| 129 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/kerby-asn1-2.0.3.jar` |  |
| 130 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/kerby-asn1.jar` |  |
| 131 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/kerby-config-2.0.3.jar` |  |
| 132 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/kerby-config.jar` |  |
| 133 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/kerby-pkix-2.0.3.jar` |  |
| 134 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/kerby-pkix.jar` |  |
| 135 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/kerby-util-2.0.3.jar` |  |
| 136 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/kerby-util.jar` |  |
| 137 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/kerby-xdr-2.0.3.jar` |  |
| 138 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/kerby-xdr.jar` |  |
| 139 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/kotlin-stdlib-jdk7-1.8.0.jar` |  |
| 140 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/kotlin-stdlib-jdk7.jar` |  |
| 141 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/kotlin-stdlib-jdk8-1.8.0.jar` |  |
| 142 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/kotlin-stdlib-jdk8.jar` |  |
| 143 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/listenablefuture-9999.0-empty-to-avoid-conflict-with-guava.jar` |  |
| 144 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/listenablefuture.jar` |  |
| 145 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/lz4-java-1.7.1.jar` |  |
| 146 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/lz4-java.jar` |  |
| 147 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/metrics-core-3.2.4.jar` |  |
| 148 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/metrics-core.jar` |  |
| 149 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-all-4.1.100.Final.jar` |  |
| 150 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-all.jar` |  |
| 151 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-buffer-4.1.100.Final.jar` |  |
| 152 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-buffer.jar` |  |
| 153 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-codec-4.1.100.Final.jar` |  |
| 154 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-codec-dns-4.1.100.Final.jar` |  |
| 155 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-codec-dns.jar` |  |
| 156 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-codec-haproxy-4.1.100.Final.jar` |  |
| 157 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-codec-haproxy.jar` |  |
| 158 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-codec-http2-4.1.100.Final.jar` |  |
| 159 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-codec-http2.jar` |  |
| 160 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-codec-http-4.1.100.Final.jar` |  |
| 161 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-codec-http.jar` |  |
| 162 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-codec.jar` |  |
| 163 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-codec-memcache-4.1.100.Final.jar` |  |
| 164 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-codec-memcache.jar` |  |
| 165 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-codec-mqtt-4.1.100.Final.jar` |  |
| 166 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-codec-mqtt.jar` |  |
| 167 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-codec-redis-4.1.100.Final.jar` |  |
| 168 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-codec-redis.jar` |  |
| 169 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-codec-smtp-4.1.100.Final.jar` |  |
| 170 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-codec-smtp.jar` |  |
| 171 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-codec-socks-4.1.100.Final.jar` |  |
| 172 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-codec-socks.jar` |  |
| 173 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-codec-stomp-4.1.100.Final.jar` |  |
| 174 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-codec-stomp.jar` |  |
| 175 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-codec-xml-4.1.100.Final.jar` |  |
| 176 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-codec-xml.jar` |  |
| 177 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-common-4.1.100.Final.jar` |  |
| 178 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-common.jar` |  |
| 179 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-handler-4.1.100.Final.jar` |  |
| 180 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-handler.jar` |  |
| 181 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-handler-proxy-4.1.100.Final.jar` |  |
| 182 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-handler-proxy.jar` |  |
| 183 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-handler-ssl-ocsp-4.1.100.Final.jar` |  |
| 184 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-handler-ssl-ocsp.jar` |  |
| 185 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-resolver-4.1.100.Final.jar` |  |
| 186 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-resolver-dns-4.1.100.Final.jar` |  |
| 187 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-resolver-dns-classes-macos-4.1.100.Final.jar` |  |
| 188 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-resolver-dns-classes-macos.jar` |  |
| 189 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-resolver-dns.jar` |  |
| 190 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-resolver-dns-native-macos-4.1.100.Final-osx-aarch_64.jar` |  |
| 191 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-resolver-dns-native-macos-4.1.100.Final-osx-x86_64.jar` |  |
| 192 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-resolver-dns-native-macos.jar` |  |
| 193 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-resolver.jar` |  |
| 194 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-transport-4.1.100.Final.jar` |  |
| 195 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-transport-classes-epoll-4.1.100.Final.jar` |  |
| 196 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-transport-classes-epoll.jar` |  |
| 197 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-transport-classes-kqueue-4.1.100.Final.jar` |  |
| 198 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-transport-classes-kqueue.jar` |  |
| 199 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-transport.jar` |  |
| 200 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-transport-native-epoll-4.1.100.Final-linux-aarch_64.jar` |  |
| 201 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-transport-native-epoll-4.1.100.Final-linux-x86_64.jar` |  |
| 202 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-transport-native-epoll.jar` |  |
| 203 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-transport-native-kqueue-4.1.100.Final-osx-aarch_64.jar` |  |
| 204 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-transport-native-kqueue-4.1.100.Final-osx-x86_64.jar` |  |
| 205 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-transport-native-kqueue.jar` |  |
| 206 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-transport-native-unix-common-4.1.100.Final.jar` |  |
| 207 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-transport-native-unix-common.jar` |  |
| 208 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-transport-rxtx-4.1.100.Final.jar` |  |
| 209 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-transport-rxtx.jar` |  |
| 210 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-transport-sctp-4.1.100.Final.jar` |  |
| 211 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-transport-sctp.jar` |  |
| 212 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-transport-udt-4.1.100.Final.jar` |  |
| 213 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-transport-udt.jar` |  |
| 214 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/nimbus-jose-jwt-9.37.2.jar` |  |
| 215 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/nimbus-jose-jwt.jar` |  |
| 216 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/okio-jvm-3.4.0.jar` |  |
| 217 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/okio-jvm.jar` |  |
| 218 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/protobuf-java-2.5.0.jar` |  |
| 219 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/protobuf-java.jar` |  |
| 220 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/re2j-1.2.jar` |  |
| 221 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/re2j.jar` |  |
| 222 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/reload4j-1.2.22.jar` |  |
| 223 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/reload4j.jar` |  |
| 224 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/snappy-java-1.1.10.5.jar` |  |
| 225 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/snappy-java.jar` |  |
| 226 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/stax2-api-4.2.1.jar` |  |
| 227 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/stax2-api.jar` |  |
| 228 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/token-provider-2.0.3.jar` |  |
| 229 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/token-provider.jar` |  |
| 230 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/wildfly-openssl-1.1.3.Final.jar` |  |
| 231 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/wildfly-openssl.jar` |  |
| 232 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/woodstox-core-5.4.0.jar` |  |
| 233 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/woodstox-core.jar` |  |
| 234 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop-ozone/share/ozone/lib/ozone-filesystem-hadoop3-1.4.0.7.1.9.1000-103.jar` |  |
| 235 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hbase/bin/../lib/client-facing-thirdparty/audience-annotations-0.12.0.jar` |  |
| 236 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hbase/bin/../lib/client-facing-thirdparty/commons-logging-1.2.jar` |  |
| 237 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hbase/bin/../lib/client-facing-thirdparty/opentelemetry-api-0.12.0.jar` |  |
| 238 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hbase/bin/../lib/client-facing-thirdparty/opentelemetry-context-0.12.0.jar` |  |
| 239 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hbase/bin/../lib/shaded-clients/hbase-shaded-mapreduce-2.4.17.7.1.9.1000-103.jar` |  |
| 240 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../SPARK3-3.3.2.3.3.7190.0-91-1.p0.45265883/lib/spark3/../iceberg/iceberg-hive-runtime-1.3.0.3.3.7190.0-91.jar` |  |
| 241 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../SPARK3-3.3.2.3.3.7190.0-91-1.p0.45265883/lib/spark3/../iceberg/iceberg-spark-runtime-3.3_2.12-1.3.0.3.3.7190.0-91.jar` |  |
| 242 | `/data22/yarn/nm/usercache/hdpt2i/appcache/application_1779574059803_412553/container_e396_1779574059803_412553_01_000001/__spark_conf__/__hadoop_conf__` |  |

#### Atribuição original exata

```text
CLASSPATH=/data22/yarn/nm/usercache/hdpt2i/appcache/application_1779574059803_412553/container_e396_1779574059803_412553_01_000001:/data22/yarn/nm/usercache/hdpt2i/appcache/application_1779574059803_412553/container_e396_1779574059803_412553_01_000001/__spark_conf__:/data22/yarn/nm/usercache/hdpt2i/appcache/application_1779574059803_412553/container_e396_1779574059803_412553_01_000001/__spark_libs__/*:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../SPARK3-3.3.2.3.3.7190.0-91-1.p0.45265883/lib/spark3/jars/*:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../SPARK3-3.3.2.3.3.7190.0-91-1.p0.45265883/lib/spark3/hive/*:/etc/hadoop/conf.cloudera.yarn2:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/*:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/lib/*:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop-hdfs/*:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop-hdfs/lib/*:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop-yarn/*:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop-yarn/lib/*:/etc/hadoop/conf.cloudera.yarn2:/data22/yarn/nm/usercache/hdpt2i/appcache/application_1779574059803_412553/container_e396_1779574059803_412553_01_000001/mr-framework/*::/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/avro.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/aws-java-sdk-bundle-1.12.599.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/aws-java-sdk-bundle.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/azure-data-lake-store-sdk-2.3.6.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/azure-data-lake-store-sdk.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/checker-qual-3.33.0.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/checker-qual.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/commons-beanutils-1.9.4.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/commons-beanutils.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/commons-cli-1.2.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/commons-cli.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/commons-codec-1.14.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/commons-codec.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/commons-collections-3.2.2.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/commons-collections.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/commons-compress-1.23.0.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/commons-compress.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/commons-configuration2-2.10.1.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/commons-configuration2.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/commons-io-2.11.0.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/commons-io.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/commons-lang-2.6.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/commons-lang3-3.8.1.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/commons-lang3.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/commons-lang.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/commons-logging-1.1.3.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/commons-logging.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/commons-math3-3.1.1.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/commons-math3.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/commons-net-3.9.0.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/commons-net.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/commons-text-1.10.0.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/commons-text.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/curator-client-5.4.0.7.1.9.1000-103.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/curator-client.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/curator-framework-5.4.0.7.1.9.1000-103.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/curator-framework.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/curator-recipes-5.4.0.7.1.9.1000-103.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/curator-recipes.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/failureaccess-1.0.1.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/failureaccess.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/gson-2.9.0.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/gson.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/guava-32.0.1-jre.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/guava.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/hadoop-annotations-3.1.1.7.1.9.1000-103.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/hadoop-annotations.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/hadoop-auth-3.1.1.7.1.9.1000-103.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/hadoop-auth.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/hadoop-aws-3.1.1.7.1.9.1000-103.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/hadoop-aws.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/hadoop-azure-3.1.1.7.1.9.1000-103.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/hadoop-azure-datalake-3.1.1.7.1.9.1000-103.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/hadoop-azure-datalake.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/hadoop-azure.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/hadoop-common-3.1.1.7.1.9.1000-103.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/hadoop-common.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/hadoop-hdfs-client-3.1.1.7.1.9.1000-103.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/hadoop-hdfs-client.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/hadoop-mapreduce-client-common-3.1.1.7.1.9.1000-103.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/hadoop-mapreduce-client-common.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/hadoop-mapreduce-client-core-3.1.1.7.1.9.1000-103.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/hadoop-mapreduce-client-core.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/hadoop-mapreduce-client-jobclient-3.1.1.7.1.9.1000-103.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/hadoop-mapreduce-client-jobclient.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/hadoop-yarn-api-3.1.1.7.1.9.1000-103.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/hadoop-yarn-api.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/hadoop-yarn-client-3.1.1.7.1.9.1000-103.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/hadoop-yarn-client.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/hadoop-yarn-common-3.1.1.7.1.9.1000-103.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/hadoop-yarn-common.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/httpclient-4.5.13.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/httpclient.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/httpcore-4.4.13.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/httpcore.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/j2objc-annotations-2.8.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/j2objc-annotations.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/jakarta.activation-api-1.2.1.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/jakarta.activation-api.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/jakarta.xml.bind-api-2.3.2.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/jakarta.xml.bind-api.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/javax.activation-api-1.2.0.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/javax.activation-api.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/jaxb-api-2.2.11.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/jaxb-api.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/jcip-annotations-1.0-1.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/jcip-annotations.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/jline-3.22.0.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/jline.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/jsp-api-2.1.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/jsp-api.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/jsr305-3.0.0.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/jsr305.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/jsr311-api-1.1.1.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/jsr311-api.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/kerb-admin-2.0.3.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/kerb-admin.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/kerb-client-2.0.3.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/kerb-client.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/kerb-common-2.0.3.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/kerb-common.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/kerb-core-2.0.3.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/kerb-core.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/kerb-crypto-2.0.3.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/kerb-crypto.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/kerb-identity-2.0.3.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/kerb-identity.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/kerb-server-2.0.3.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/kerb-server.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/kerb-simplekdc-2.0.3.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/kerb-simplekdc.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/kerb-util-2.0.3.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/kerb-util.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/kerby-asn1-2.0.3.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/kerby-asn1.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/kerby-config-2.0.3.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/kerby-config.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/kerby-pkix-2.0.3.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/kerby-pkix.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/kerby-util-2.0.3.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/kerby-util.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/kerby-xdr-2.0.3.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/kerby-xdr.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/kotlin-stdlib-jdk7-1.8.0.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/kotlin-stdlib-jdk7.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/kotlin-stdlib-jdk8-1.8.0.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/kotlin-stdlib-jdk8.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/listenablefuture-9999.0-empty-to-avoid-conflict-with-guava.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/listenablefuture.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/lz4-java-1.7.1.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/lz4-java.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/metrics-core-3.2.4.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/metrics-core.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-all-4.1.100.Final.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-all.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-buffer-4.1.100.Final.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-buffer.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-codec-4.1.100.Final.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-codec-dns-4.1.100.Final.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-codec-dns.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-codec-haproxy-4.1.100.Final.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-codec-haproxy.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-codec-http2-4.1.100.Final.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-codec-http2.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-codec-http-4.1.100.Final.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-codec-http.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-codec.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-codec-memcache-4.1.100.Final.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-codec-memcache.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-codec-mqtt-4.1.100.Final.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-codec-mqtt.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-codec-redis-4.1.100.Final.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-codec-redis.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-codec-smtp-4.1.100.Final.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-codec-smtp.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-codec-socks-4.1.100.Final.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-codec-socks.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-codec-stomp-4.1.100.Final.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-codec-stomp.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-codec-xml-4.1.100.Final.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-codec-xml.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-common-4.1.100.Final.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-common.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-handler-4.1.100.Final.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-handler.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-handler-proxy-4.1.100.Final.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-handler-proxy.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-handler-ssl-ocsp-4.1.100.Final.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-handler-ssl-ocsp.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-resolver-4.1.100.Final.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-resolver-dns-4.1.100.Final.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-resolver-dns-classes-macos-4.1.100.Final.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-resolver-dns-classes-macos.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-resolver-dns.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-resolver-dns-native-macos-4.1.100.Final-osx-aarch_64.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-resolver-dns-native-macos-4.1.100.Final-osx-x86_64.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-resolver-dns-native-macos.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-resolver.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-transport-4.1.100.Final.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-transport-classes-epoll-4.1.100.Final.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-transport-classes-epoll.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-transport-classes-kqueue-4.1.100.Final.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-transport-classes-kqueue.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-transport.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-transport-native-epoll-4.1.100.Final-linux-aarch_64.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-transport-native-epoll-4.1.100.Final-linux-x86_64.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-transport-native-epoll.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-transport-native-kqueue-4.1.100.Final-osx-aarch_64.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-transport-native-kqueue-4.1.100.Final-osx-x86_64.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-transport-native-kqueue.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-transport-native-unix-common-4.1.100.Final.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-transport-native-unix-common.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-transport-rxtx-4.1.100.Final.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-transport-rxtx.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-transport-sctp-4.1.100.Final.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-transport-sctp.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-transport-udt-4.1.100.Final.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-transport-udt.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/nimbus-jose-jwt-9.37.2.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/nimbus-jose-jwt.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/okio-jvm-3.4.0.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/okio-jvm.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/protobuf-java-2.5.0.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/protobuf-java.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/re2j-1.2.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/re2j.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/reload4j-1.2.22.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/reload4j.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/snappy-java-1.1.10.5.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/snappy-java.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/stax2-api-4.2.1.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/stax2-api.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/token-provider-2.0.3.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/token-provider.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/wildfly-openssl-1.1.3.Final.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/wildfly-openssl.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/woodstox-core-5.4.0.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/woodstox-core.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop-ozone/share/ozone/lib/ozone-filesystem-hadoop3-1.4.0.7.1.9.1000-103.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hbase/bin/../lib/client-facing-thirdparty/audience-annotations-0.12.0.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hbase/bin/../lib/client-facing-thirdparty/commons-logging-1.2.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hbase/bin/../lib/client-facing-thirdparty/opentelemetry-api-0.12.0.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hbase/bin/../lib/client-facing-thirdparty/opentelemetry-context-0.12.0.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hbase/bin/../lib/shaded-clients/hbase-shaded-mapreduce-2.4.17.7.1.9.1000-103.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../SPARK3-3.3.2.3.3.7190.0-91-1.p0.45265883/lib/spark3/../iceberg/iceberg-hive-runtime-1.3.0.3.3.7190.0-91.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../SPARK3-3.3.2.3.3.7190.0-91-1.p0.45265883/lib/spark3/../iceberg/iceberg-spark-runtime-3.3_2.12-1.3.0.3.3.7190.0-91.jar:/data22/yarn/nm/usercache/hdpt2i/appcache/application_1779574059803_412553/container_e396_1779574059803_412553_01_000001/__spark_conf__/__hadoop_conf__
```

### `PATH`

| Propriedade | Valor |
|---|---|
| Linha no arquivo-fonte | `39` |
| Categoria documental | Paths e dependências gerais |
| Representação | lista separada por `:` |
| Comprimento do valor | `23` caracteres |

#### Estrutura interna

O valor original foi decomposto **somente para visualização** usando `:` como separador. Foram encontradas **2 posições**.

| # | Entrada | Observação |
|---:|---|---|
| 1 | `/usr/local/bin` |  |
| 2 | `/usr/bin` |  |

#### Atribuição original exata

```text
PATH=/usr/local/bin:/usr/bin
```

### `LD_LIBRARY_PATH`

| Propriedade | Valor |
|---|---|
| Linha no arquivo-fonte | `23` |
| Categoria documental | Paths e dependências gerais |
| Representação | lista separada por `:` |
| Comprimento do valor | `136` caracteres |

#### Estrutura interna

O valor original foi decomposto **somente para visualização** usando `:` como separador. Foram encontradas **2 posições**.

| # | Entrada | Observação |
|---:|---|---|
| 1 | `/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/lib/native` |  |
| 2 | *(vazio)* | entrada vazia preservada |

#### Atribuição original exata

```text
LD_LIBRARY_PATH=/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/lib/native:
```

## 15. Inventário consolidado

A tabela abaixo funciona como índice de conferência. Os valores completos permanecem nas respectivas subseções e no apêndice bruto.

| # | Linha-fonte | Variável | Categoria | Representação |
|---:|---:|---|---|---|
| 1 | 2 | `AMBIENTE` | Identificação do ambiente e projeto | atribuição simples |
| 2 | 3 | `APPLICATION_WEB_PROXY_BASE` | Aplicação e sessão | atribuição simples |
| 3 | 4 | `APP_SUBMIT_TIME_ENV` | Aplicação e sessão | atribuição simples |
| 4 | 5 | `BBMAGIC_SESSION_ID` | Aplicação e sessão | atribuição simples |
| 5 | 6 | `CLASSPATH` | Paths e dependências gerais | lista separada por `:` |
| 6 | 7 | `CONTAINER_ID` | YARN, container e NodeManager | atribuição simples |
| 7 | 8 | `DOMINIO` | Identificação do ambiente e projeto | atribuição simples |
| 8 | 9 | `HADOOP_CLIENT_CONF_DIR` | Hadoop | atribuição simples |
| 9 | 10 | `HADOOP_COMMON_HOME` | Hadoop | atribuição simples |
| 10 | 11 | `HADOOP_HDFS_HOME` | Hadoop | atribuição simples |
| 11 | 12 | `HADOOP_HOME` | Hadoop | atribuição simples |
| 12 | 13 | `HADOOP_MAPRED_HOME` | Hadoop | atribuição simples |
| 13 | 14 | `HADOOP_TOKEN_FILE_LOCATION` | Autenticação, tokens e credenciais | atribuição simples |
| 14 | 15 | `HADOOP_YARN_HOME` | Hadoop | atribuição simples |
| 15 | 16 | `HOJE` | Identificação do ambiente e projeto | atribuição simples |
| 16 | 17 | `HOME` | Sistema operacional e runtime | atribuição simples |
| 17 | 18 | `JAVA_HOME` | Java e JVM | atribuição simples |
| 18 | 19 | `JDK_JAVA_OPTIONS` | Java e JVM | opções JVM separadas por espaço |
| 19 | 20 | `JVM_PID` | Java e JVM | atribuição simples |
| 20 | 21 | `KEYTAB` | Autenticação, tokens e credenciais | atribuição simples |
| 21 | 22 | `LANG` | Sistema operacional e runtime | atribuição simples |
| 22 | 23 | `LD_LIBRARY_PATH` | Paths e dependências gerais | lista separada por `:` |
| 23 | 24 | `LIVY_SPARK_MAJOR_VERSION` | Spark e Livy | atribuição simples |
| 24 | 25 | `LOCAL_DIRS` | YARN, container e NodeManager | atribuição simples |
| 25 | 26 | `LOCAL_USER_DIRS` | YARN, container e NodeManager | atribuição simples |
| 26 | 27 | `LOGNAME` | Sistema operacional e runtime | atribuição simples |
| 27 | 28 | `LOG_DIRS` | YARN, container e NodeManager | atribuição simples |
| 28 | 29 | `MALLOC_ARENA_MAX` | Performance e paralelismo | atribuição simples |
| 29 | 30 | `MKL_NUM_THREADS` | Performance e paralelismo | atribuição simples |
| 30 | 31 | `MODEL_NAME` | Identificação do ambiente e projeto | atribuição simples |
| 31 | 32 | `NM_AUX_SERVICE_mapreduce_shuffle` | YARN, container e NodeManager | atribuição simples |
| 32 | 33 | `NM_AUX_SERVICE_spark3_shuffle` | YARN, container e NodeManager | valor vazio |
| 33 | 34 | `NM_AUX_SERVICE_spark_shuffle` | YARN, container e NodeManager | valor vazio |
| 34 | 35 | `NM_HOST` | YARN, container e NodeManager | atribuição simples |
| 35 | 36 | `NM_HTTP_PORT` | YARN, container e NodeManager | atribuição simples |
| 36 | 37 | `NM_PORT` | YARN, container e NodeManager | atribuição simples |
| 37 | 38 | `OPENBLAS_NUM_THREADS` | Performance e paralelismo | atribuição simples |
| 38 | 39 | `PATH` | Paths e dependências gerais | lista separada por `:` |
| 39 | 40 | `PRELAUNCH_ERR` | YARN, container e NodeManager | atribuição simples |
| 40 | 41 | `PRELAUNCH_OUT` | YARN, container e NodeManager | atribuição simples |
| 41 | 42 | `PROJECT_ID` | Identificação do ambiente e projeto | atribuição simples |
| 42 | 43 | `PWD` | YARN, container e NodeManager | atribuição simples |
| 43 | 44 | `PYSPARK_DRIVER_PYTHON` | Python e PySpark | atribuição simples |
| 44 | 45 | `PYSPARK_GATEWAY_PORT` | Python e PySpark | atribuição simples |
| 45 | 46 | `PYSPARK_GATEWAY_SECRET` | Autenticação, tokens e credenciais | atribuição simples |
| 46 | 47 | `PYSPARK_PYTHON` | Python e PySpark | atribuição simples |
| 47 | 48 | `PYTHONHASHSEED` | Python e PySpark | atribuição simples |
| 48 | 49 | `PYTHONPATH` | Python e PySpark | lista separada por `:` |
| 49 | 50 | `PYTHONUNBUFFERED` | Python e PySpark | atribuição simples |
| 50 | 51 | `SESSION_NAME` | Aplicação e sessão | atribuição simples |
| 51 | 52 | `SHLVL` | Sistema operacional e runtime | atribuição simples |
| 52 | 53 | `SPARK_AUTH_SOCKET_TIMEOUT` | Spark e Livy | atribuição simples |
| 53 | 54 | `SPARK_BUFFER_SIZE` | Spark e Livy | atribuição simples |
| 54 | 55 | `SPARK_DIST_CLASSPATH` | Spark e Livy | lista separada por `:` |
| 55 | 56 | `SPARK_HOME` | Spark e Livy | atribuição simples |
| 56 | 57 | `SPARK_USER` | Spark e Livy | atribuição simples |
| 57 | 58 | `SPARK_YARN_STAGING_DIR` | Spark e Livy | atribuição simples |
| 58 | 59 | `USER` | Sistema operacional e runtime | atribuição simples |
| 59 | 60 | `USE_LOGS` | Sistema operacional e runtime | atribuição simples |
| 60 | 61 | `_` | Sistema operacional e runtime | atribuição simples |

## 16. Apêndice — dump bruto integral

O conteúdo abaixo reproduz o arquivo-fonte completo, na ordem original, sem reorganização. A primeira linha do arquivo-fonte é vazia e permanece vazia imediatamente após a abertura do bloco.

```text

AMBIENTE=PRODUCAO
APPLICATION_WEB_PROXY_BASE=/proxy/application_1779574059803_412553
APP_SUBMIT_TIME_ENV=1782917390993
BBMAGIC_SESSION_ID=2eaf3761-b6a4-46cd-aeba-752d5677f0f4
CLASSPATH=/data22/yarn/nm/usercache/hdpt2i/appcache/application_1779574059803_412553/container_e396_1779574059803_412553_01_000001:/data22/yarn/nm/usercache/hdpt2i/appcache/application_1779574059803_412553/container_e396_1779574059803_412553_01_000001/__spark_conf__:/data22/yarn/nm/usercache/hdpt2i/appcache/application_1779574059803_412553/container_e396_1779574059803_412553_01_000001/__spark_libs__/*:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../SPARK3-3.3.2.3.3.7190.0-91-1.p0.45265883/lib/spark3/jars/*:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../SPARK3-3.3.2.3.3.7190.0-91-1.p0.45265883/lib/spark3/hive/*:/etc/hadoop/conf.cloudera.yarn2:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/*:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/lib/*:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop-hdfs/*:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop-hdfs/lib/*:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop-yarn/*:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop-yarn/lib/*:/etc/hadoop/conf.cloudera.yarn2:/data22/yarn/nm/usercache/hdpt2i/appcache/application_1779574059803_412553/container_e396_1779574059803_412553_01_000001/mr-framework/*::/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/avro.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/aws-java-sdk-bundle-1.12.599.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/aws-java-sdk-bundle.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/azure-data-lake-store-sdk-2.3.6.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/azure-data-lake-store-sdk.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/checker-qual-3.33.0.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/checker-qual.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/commons-beanutils-1.9.4.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/commons-beanutils.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/commons-cli-1.2.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/commons-cli.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/commons-codec-1.14.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/commons-codec.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/commons-collections-3.2.2.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/commons-collections.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/commons-compress-1.23.0.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/commons-compress.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/commons-configuration2-2.10.1.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/commons-configuration2.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/commons-io-2.11.0.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/commons-io.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/commons-lang-2.6.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/commons-lang3-3.8.1.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/commons-lang3.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/commons-lang.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/commons-logging-1.1.3.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/commons-logging.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/commons-math3-3.1.1.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/commons-math3.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/commons-net-3.9.0.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/commons-net.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/commons-text-1.10.0.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/commons-text.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/curator-client-5.4.0.7.1.9.1000-103.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/curator-client.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/curator-framework-5.4.0.7.1.9.1000-103.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/curator-framework.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/curator-recipes-5.4.0.7.1.9.1000-103.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/curator-recipes.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/failureaccess-1.0.1.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/failureaccess.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/gson-2.9.0.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/gson.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/guava-32.0.1-jre.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/guava.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/hadoop-annotations-3.1.1.7.1.9.1000-103.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/hadoop-annotations.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/hadoop-auth-3.1.1.7.1.9.1000-103.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/hadoop-auth.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/hadoop-aws-3.1.1.7.1.9.1000-103.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/hadoop-aws.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/hadoop-azure-3.1.1.7.1.9.1000-103.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/hadoop-azure-datalake-3.1.1.7.1.9.1000-103.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/hadoop-azure-datalake.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/hadoop-azure.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/hadoop-common-3.1.1.7.1.9.1000-103.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/hadoop-common.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/hadoop-hdfs-client-3.1.1.7.1.9.1000-103.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/hadoop-hdfs-client.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/hadoop-mapreduce-client-common-3.1.1.7.1.9.1000-103.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/hadoop-mapreduce-client-common.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/hadoop-mapreduce-client-core-3.1.1.7.1.9.1000-103.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/hadoop-mapreduce-client-core.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/hadoop-mapreduce-client-jobclient-3.1.1.7.1.9.1000-103.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/hadoop-mapreduce-client-jobclient.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/hadoop-yarn-api-3.1.1.7.1.9.1000-103.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/hadoop-yarn-api.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/hadoop-yarn-client-3.1.1.7.1.9.1000-103.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/hadoop-yarn-client.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/hadoop-yarn-common-3.1.1.7.1.9.1000-103.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/hadoop-yarn-common.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/httpclient-4.5.13.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/httpclient.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/httpcore-4.4.13.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/httpcore.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/j2objc-annotations-2.8.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/j2objc-annotations.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/jakarta.activation-api-1.2.1.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/jakarta.activation-api.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/jakarta.xml.bind-api-2.3.2.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/jakarta.xml.bind-api.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/javax.activation-api-1.2.0.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/javax.activation-api.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/jaxb-api-2.2.11.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/jaxb-api.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/jcip-annotations-1.0-1.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/jcip-annotations.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/jline-3.22.0.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/jline.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/jsp-api-2.1.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/jsp-api.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/jsr305-3.0.0.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/jsr305.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/jsr311-api-1.1.1.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/jsr311-api.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/kerb-admin-2.0.3.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/kerb-admin.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/kerb-client-2.0.3.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/kerb-client.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/kerb-common-2.0.3.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/kerb-common.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/kerb-core-2.0.3.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/kerb-core.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/kerb-crypto-2.0.3.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/kerb-crypto.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/kerb-identity-2.0.3.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/kerb-identity.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/kerb-server-2.0.3.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/kerb-server.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/kerb-simplekdc-2.0.3.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/kerb-simplekdc.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/kerb-util-2.0.3.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/kerb-util.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/kerby-asn1-2.0.3.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/kerby-asn1.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/kerby-config-2.0.3.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/kerby-config.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/kerby-pkix-2.0.3.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/kerby-pkix.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/kerby-util-2.0.3.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/kerby-util.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/kerby-xdr-2.0.3.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/kerby-xdr.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/kotlin-stdlib-jdk7-1.8.0.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/kotlin-stdlib-jdk7.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/kotlin-stdlib-jdk8-1.8.0.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/kotlin-stdlib-jdk8.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/listenablefuture-9999.0-empty-to-avoid-conflict-with-guava.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/listenablefuture.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/lz4-java-1.7.1.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/lz4-java.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/metrics-core-3.2.4.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/metrics-core.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-all-4.1.100.Final.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-all.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-buffer-4.1.100.Final.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-buffer.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-codec-4.1.100.Final.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-codec-dns-4.1.100.Final.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-codec-dns.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-codec-haproxy-4.1.100.Final.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-codec-haproxy.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-codec-http2-4.1.100.Final.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-codec-http2.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-codec-http-4.1.100.Final.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-codec-http.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-codec.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-codec-memcache-4.1.100.Final.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-codec-memcache.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-codec-mqtt-4.1.100.Final.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-codec-mqtt.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-codec-redis-4.1.100.Final.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-codec-redis.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-codec-smtp-4.1.100.Final.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-codec-smtp.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-codec-socks-4.1.100.Final.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-codec-socks.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-codec-stomp-4.1.100.Final.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-codec-stomp.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-codec-xml-4.1.100.Final.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-codec-xml.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-common-4.1.100.Final.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-common.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-handler-4.1.100.Final.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-handler.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-handler-proxy-4.1.100.Final.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-handler-proxy.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-handler-ssl-ocsp-4.1.100.Final.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-handler-ssl-ocsp.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-resolver-4.1.100.Final.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-resolver-dns-4.1.100.Final.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-resolver-dns-classes-macos-4.1.100.Final.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-resolver-dns-classes-macos.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-resolver-dns.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-resolver-dns-native-macos-4.1.100.Final-osx-aarch_64.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-resolver-dns-native-macos-4.1.100.Final-osx-x86_64.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-resolver-dns-native-macos.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-resolver.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-transport-4.1.100.Final.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-transport-classes-epoll-4.1.100.Final.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-transport-classes-epoll.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-transport-classes-kqueue-4.1.100.Final.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-transport-classes-kqueue.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-transport.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-transport-native-epoll-4.1.100.Final-linux-aarch_64.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-transport-native-epoll-4.1.100.Final-linux-x86_64.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-transport-native-epoll.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-transport-native-kqueue-4.1.100.Final-osx-aarch_64.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-transport-native-kqueue-4.1.100.Final-osx-x86_64.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-transport-native-kqueue.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-transport-native-unix-common-4.1.100.Final.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-transport-native-unix-common.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-transport-rxtx-4.1.100.Final.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-transport-rxtx.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-transport-sctp-4.1.100.Final.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-transport-sctp.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-transport-udt-4.1.100.Final.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-transport-udt.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/nimbus-jose-jwt-9.37.2.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/nimbus-jose-jwt.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/okio-jvm-3.4.0.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/okio-jvm.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/protobuf-java-2.5.0.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/protobuf-java.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/re2j-1.2.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/re2j.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/reload4j-1.2.22.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/reload4j.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/snappy-java-1.1.10.5.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/snappy-java.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/stax2-api-4.2.1.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/stax2-api.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/token-provider-2.0.3.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/token-provider.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/wildfly-openssl-1.1.3.Final.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/wildfly-openssl.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/woodstox-core-5.4.0.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/woodstox-core.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop-ozone/share/ozone/lib/ozone-filesystem-hadoop3-1.4.0.7.1.9.1000-103.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hbase/bin/../lib/client-facing-thirdparty/audience-annotations-0.12.0.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hbase/bin/../lib/client-facing-thirdparty/commons-logging-1.2.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hbase/bin/../lib/client-facing-thirdparty/opentelemetry-api-0.12.0.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hbase/bin/../lib/client-facing-thirdparty/opentelemetry-context-0.12.0.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hbase/bin/../lib/shaded-clients/hbase-shaded-mapreduce-2.4.17.7.1.9.1000-103.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../SPARK3-3.3.2.3.3.7190.0-91-1.p0.45265883/lib/spark3/../iceberg/iceberg-hive-runtime-1.3.0.3.3.7190.0-91.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../SPARK3-3.3.2.3.3.7190.0-91-1.p0.45265883/lib/spark3/../iceberg/iceberg-spark-runtime-3.3_2.12-1.3.0.3.3.7190.0-91.jar:/data22/yarn/nm/usercache/hdpt2i/appcache/application_1779574059803_412553/container_e396_1779574059803_412553_01_000001/__spark_conf__/__hadoop_conf__
CONTAINER_ID=container_e396_1779574059803_412553_01_000001
DOMINIO=t2i
HADOOP_CLIENT_CONF_DIR=/etc/hadoop/conf.cloudera.yarn2
HADOOP_COMMON_HOME=/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop
HADOOP_HDFS_HOME=/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop-hdfs
HADOOP_HOME=/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop
HADOOP_MAPRED_HOME=/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop-mapreduce
HADOOP_TOKEN_FILE_LOCATION=/data22/yarn/nm/usercache/hdpt2i/appcache/application_1779574059803_412553/container_e396_1779574059803_412553_01_000001/container_tokens
HADOOP_YARN_HOME=/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop-yarn
HOJE=2026-07-01
HOME=/home/
JAVA_HOME=/usr/lib/jvm/jre-openjdk
JDK_JAVA_OPTIONS=--add-opens=java.base/java.lang=ALL-UNNAMED --add-exports=java.base/sun.net.dns=ALL-UNNAMED --add-exports=java.base/sun.net.util=ALL-UNNAMED
JVM_PID=3900365
KEYTAB=/projeto/hdpt2i.keytab
LANG=en_US.UTF-8
LD_LIBRARY_PATH=/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/../../../CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/lib/native:
LIVY_SPARK_MAJOR_VERSION=3
LOCAL_DIRS=/data22/yarn/nm/usercache/hdpt2i/appcache/application_1779574059803_412553
LOCAL_USER_DIRS=/data22/yarn/nm/usercache/hdpt2i/
LOGNAME=hdpt2i
LOG_DIRS=/data22/yarn/container-logs/application_1779574059803_412553/container_e396_1779574059803_412553_01_000001
MALLOC_ARENA_MAX=4
MKL_NUM_THREADS=1
MODEL_NAME=t2i_mf_etl_vinculacao_meus_insights
NM_AUX_SERVICE_mapreduce_shuffle=AAA0+gAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA=
NM_AUX_SERVICE_spark3_shuffle=
NM_AUX_SERVICE_spark_shuffle=
NM_HOST=xfd691.dispositivos.bb.com.br
NM_HTTP_PORT=8042
NM_PORT=8041
OPENBLAS_NUM_THREADS=1
PATH=/usr/local/bin:/usr/bin
PRELAUNCH_ERR=/data22/yarn/container-logs/application_1779574059803_412553/container_e396_1779574059803_412553_01_000001/prelaunch.err
PRELAUNCH_OUT=/data22/yarn/container-logs/application_1779574059803_412553/container_e396_1779574059803_412553_01_000001/prelaunch.out
PROJECT_ID=663d3236-46ba-4ea8-bc96-51c694d548c3
PWD=/data22/yarn/nm/usercache/hdpt2i/appcache/application_1779574059803_412553/container_e396_1779574059803_412553_01_000001
PYSPARK_DRIVER_PYTHON=/usr/bin/python3
PYSPARK_GATEWAY_PORT=7589
PYSPARK_GATEWAY_SECRET=1oEeFz2vRdzvcMSJdOhzjLfs95kpTMntEiYpssIhBd0=
PYSPARK_PYTHON=/usr/bin/python3.9
PYTHONHASHSEED=0
PYTHONPATH=/opt/cloudera/cm-agent/lib/python3.11/site-packages:/opt/cloudera/cm-agent/thirdparty:/opt/cloudera/parcels/SPARK3-3.3.2.3.3.7190.0-91-1.p0.45265883/lib/spark3/python/lib/py4j-0.10.9.5-src.zip:/opt/cloudera/parcels/SPARK3-3.3.2.3.3.7190.0-91-1.p0.45265883/lib/spark3/python/lib/pyspark.zip:/data22/yarn/nm/usercache/hdpt2i/appcache/application_1779574059803_412553/container_e396_1779574059803_412553_01_000001/pyspark.zip:/data22/yarn/nm/usercache/hdpt2i/appcache/application_1779574059803_412553/container_e396_1779574059803_412553_01_000001/py4j-0.10.9.5-src.zip:/data22/yarn/nm/usercache/hdpt2i/appcache/application_1779574059803_412553/container_e396_1779574059803_412553_01_000001/pyspark.zip:/data22/yarn/nm/usercache/hdpt2i/appcache/application_1779574059803_412553/container_e396_1779574059803_412553_01_000001/py4j-0.10.9.5-src.zip
PYTHONUNBUFFERED=YES
SESSION_NAME=spark_/projeto/hdpt2i.keytab_mf_etl_vinculacao_meus_insights
SHLVL=1
SPARK_AUTH_SOCKET_TIMEOUT=15
SPARK_BUFFER_SIZE=65536
SPARK_DIST_CLASSPATH=/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/avro.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/aws-java-sdk-bundle-1.12.599.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/aws-java-sdk-bundle.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/azure-data-lake-store-sdk-2.3.6.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/azure-data-lake-store-sdk.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/checker-qual-3.33.0.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/checker-qual.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/commons-beanutils-1.9.4.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/commons-beanutils.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/commons-cli-1.2.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/commons-cli.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/commons-codec-1.14.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/commons-codec.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/commons-collections-3.2.2.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/commons-collections.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/commons-compress-1.23.0.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/commons-compress.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/commons-configuration2-2.10.1.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/commons-configuration2.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/commons-io-2.11.0.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/commons-io.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/commons-lang-2.6.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/commons-lang3-3.8.1.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/commons-lang3.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/commons-lang.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/commons-logging-1.1.3.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/commons-logging.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/commons-math3-3.1.1.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/commons-math3.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/commons-net-3.9.0.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/commons-net.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/commons-text-1.10.0.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/commons-text.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/curator-client-5.4.0.7.1.9.1000-103.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/curator-client.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/curator-framework-5.4.0.7.1.9.1000-103.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/curator-framework.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/curator-recipes-5.4.0.7.1.9.1000-103.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/curator-recipes.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/failureaccess-1.0.1.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/failureaccess.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/gson-2.9.0.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/gson.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/guava-32.0.1-jre.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/guava.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/hadoop-annotations-3.1.1.7.1.9.1000-103.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/hadoop-annotations.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/hadoop-auth-3.1.1.7.1.9.1000-103.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/hadoop-auth.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/hadoop-aws-3.1.1.7.1.9.1000-103.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/hadoop-aws.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/hadoop-azure-3.1.1.7.1.9.1000-103.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/hadoop-azure-datalake-3.1.1.7.1.9.1000-103.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/hadoop-azure-datalake.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/hadoop-azure.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/hadoop-common-3.1.1.7.1.9.1000-103.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/hadoop-common.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/hadoop-hdfs-client-3.1.1.7.1.9.1000-103.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/hadoop-hdfs-client.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/hadoop-mapreduce-client-common-3.1.1.7.1.9.1000-103.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/hadoop-mapreduce-client-common.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/hadoop-mapreduce-client-core-3.1.1.7.1.9.1000-103.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/hadoop-mapreduce-client-core.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/hadoop-mapreduce-client-jobclient-3.1.1.7.1.9.1000-103.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/hadoop-mapreduce-client-jobclient.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/hadoop-yarn-api-3.1.1.7.1.9.1000-103.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/hadoop-yarn-api.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/hadoop-yarn-client-3.1.1.7.1.9.1000-103.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/hadoop-yarn-client.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/hadoop-yarn-common-3.1.1.7.1.9.1000-103.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/hadoop-yarn-common.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/httpclient-4.5.13.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/httpclient.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/httpcore-4.4.13.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/httpcore.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/j2objc-annotations-2.8.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/j2objc-annotations.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/jakarta.activation-api-1.2.1.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/jakarta.activation-api.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/jakarta.xml.bind-api-2.3.2.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/jakarta.xml.bind-api.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/javax.activation-api-1.2.0.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/javax.activation-api.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/jaxb-api-2.2.11.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/jaxb-api.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/jcip-annotations-1.0-1.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/jcip-annotations.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/jline-3.22.0.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/jline.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/jsp-api-2.1.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/jsp-api.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/jsr305-3.0.0.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/jsr305.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/jsr311-api-1.1.1.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/jsr311-api.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/kerb-admin-2.0.3.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/kerb-admin.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/kerb-client-2.0.3.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/kerb-client.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/kerb-common-2.0.3.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/kerb-common.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/kerb-core-2.0.3.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/kerb-core.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/kerb-crypto-2.0.3.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/kerb-crypto.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/kerb-identity-2.0.3.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/kerb-identity.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/kerb-server-2.0.3.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/kerb-server.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/kerb-simplekdc-2.0.3.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/kerb-simplekdc.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/kerb-util-2.0.3.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/kerb-util.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/kerby-asn1-2.0.3.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/kerby-asn1.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/kerby-config-2.0.3.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/kerby-config.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/kerby-pkix-2.0.3.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/kerby-pkix.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/kerby-util-2.0.3.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/kerby-util.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/kerby-xdr-2.0.3.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/kerby-xdr.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/kotlin-stdlib-jdk7-1.8.0.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/kotlin-stdlib-jdk7.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/kotlin-stdlib-jdk8-1.8.0.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/kotlin-stdlib-jdk8.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/listenablefuture-9999.0-empty-to-avoid-conflict-with-guava.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/listenablefuture.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/lz4-java-1.7.1.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/lz4-java.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/metrics-core-3.2.4.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/metrics-core.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-all-4.1.100.Final.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-all.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-buffer-4.1.100.Final.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-buffer.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-codec-4.1.100.Final.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-codec-dns-4.1.100.Final.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-codec-dns.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-codec-haproxy-4.1.100.Final.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-codec-haproxy.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-codec-http2-4.1.100.Final.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-codec-http2.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-codec-http-4.1.100.Final.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-codec-http.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-codec.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-codec-memcache-4.1.100.Final.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-codec-memcache.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-codec-mqtt-4.1.100.Final.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-codec-mqtt.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-codec-redis-4.1.100.Final.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-codec-redis.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-codec-smtp-4.1.100.Final.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-codec-smtp.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-codec-socks-4.1.100.Final.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-codec-socks.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-codec-stomp-4.1.100.Final.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-codec-stomp.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-codec-xml-4.1.100.Final.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-codec-xml.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-common-4.1.100.Final.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-common.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-handler-4.1.100.Final.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-handler.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-handler-proxy-4.1.100.Final.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-handler-proxy.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-handler-ssl-ocsp-4.1.100.Final.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-handler-ssl-ocsp.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-resolver-4.1.100.Final.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-resolver-dns-4.1.100.Final.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-resolver-dns-classes-macos-4.1.100.Final.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-resolver-dns-classes-macos.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-resolver-dns.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-resolver-dns-native-macos-4.1.100.Final-osx-aarch_64.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-resolver-dns-native-macos-4.1.100.Final-osx-x86_64.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-resolver-dns-native-macos.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-resolver.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-transport-4.1.100.Final.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-transport-classes-epoll-4.1.100.Final.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-transport-classes-epoll.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-transport-classes-kqueue-4.1.100.Final.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-transport-classes-kqueue.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-transport.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-transport-native-epoll-4.1.100.Final-linux-aarch_64.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-transport-native-epoll-4.1.100.Final-linux-x86_64.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-transport-native-epoll.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-transport-native-kqueue-4.1.100.Final-osx-aarch_64.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-transport-native-kqueue-4.1.100.Final-osx-x86_64.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-transport-native-kqueue.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-transport-native-unix-common-4.1.100.Final.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-transport-native-unix-common.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-transport-rxtx-4.1.100.Final.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-transport-rxtx.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-transport-sctp-4.1.100.Final.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-transport-sctp.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-transport-udt-4.1.100.Final.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/netty-transport-udt.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/nimbus-jose-jwt-9.37.2.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/nimbus-jose-jwt.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/okio-jvm-3.4.0.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/okio-jvm.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/protobuf-java-2.5.0.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/protobuf-java.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/re2j-1.2.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/re2j.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/reload4j-1.2.22.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/reload4j.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/snappy-java-1.1.10.5.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/snappy-java.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/stax2-api-4.2.1.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/stax2-api.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/token-provider-2.0.3.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/token-provider.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/wildfly-openssl-1.1.3.Final.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/wildfly-openssl.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/woodstox-core-5.4.0.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop/client/woodstox-core.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hadoop-ozone/share/ozone/lib/ozone-filesystem-hadoop3-1.4.0.7.1.9.1000-103.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hbase/bin/../lib/client-facing-thirdparty/audience-annotations-0.12.0.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hbase/bin/../lib/client-facing-thirdparty/commons-logging-1.2.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hbase/bin/../lib/client-facing-thirdparty/opentelemetry-api-0.12.0.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hbase/bin/../lib/client-facing-thirdparty/opentelemetry-context-0.12.0.jar:/opt/cloudera/parcels/CDH-7.1.9-1.cdh7.1.9.p1000.55406660/lib/hbase/bin/../lib/shaded-clients/hbase-shaded-mapreduce-2.4.17.7.1.9.1000-103.jar:/opt/cloudera/parcels/SPARK3-3.3.2.3.3.7190.0-91-1.p0.45265883/lib/spark3/../iceberg/iceberg-hive-runtime-1.3.0.3.3.7190.0-91.jar:/opt/cloudera/parcels/SPARK3-3.3.2.3.3.7190.0-91-1.p0.45265883/lib/spark3/../iceberg/iceberg-spark-runtime-3.3_2.12-1.3.0.3.3.7190.0-91.jar
SPARK_HOME=.
SPARK_USER=hdpt2i
SPARK_YARN_STAGING_DIR=hdfs:/tmp/spark/yarn/.sparkStaging/hdpt2i/.sparkStaging/application_1779574059803_412553
USER=hdpt2i
USE_LOGS=True
_=/usr/lib/jvm/jre-openjdk/bin/java
```

---

### Validação de integridade da transformação

- Variáveis esperadas: **60**
- Variáveis documentadas: **60**
- Variáveis não classificadas: **0**
- Variáveis classificadas mais de uma vez: **0**
- SHA-256 do arquivo-fonte usado na geração: `9362ec7c88b9b7b759713aede5daaad1bf3d8b2f73edf30bf65e896e30f93910`

A validação automatizada complementar do arquivo gerado verifica que todas as atribuições originais aparecem no Markdown e que o apêndice contém o dump-fonte integral.
