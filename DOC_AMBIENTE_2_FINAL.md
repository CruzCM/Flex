# BBMagic

## Introdução

A BBMagic é uma biblioteca disponível para as linguagens Python e R, projetada para facilitar a conexão com diferentes fontes de dados e ferramentas do ecossistema de Analytics do Banco do Brasil. Seu objetivo principal é aumentar a produtividade no desenvolvimento de soluções analíticas, sendo a forma recomendada para conectar-se com HDFS, DB2 e Spark.

Este guia apresenta as instruções para instalação, validação e uso da biblioteca, além de recomendações para conexões em ambientes de produção.

## 1. Instalação

A instalação da biblioteca BBMagic é simples e rápida. Siga os passos abaixo:

**Passo 1. No AnalyticsLabb, abra um terminal e execute o comando a seguir:**

```bash
python -m pip install big_bbmagic --upgrade --user
```

Nota: Este comando instala a versão mais recente da biblioteca.

**Passo 2. Caso já possua um Jupyter Notebook aberto, reinicie o kernel para que as alterações sejam aplicadas:**

Restart Kernel

## 2. Validação da Instalação

Após a instalação, valide se a biblioteca foi instalada corretamente:

**Passo 1. Execute os comandos abaixo no seu ambiente Python:**

```python
import bbmagic

print(bbmagic.__version__)
```

**Passo 2. Verifique se a versão instalada é exibida na tela. Por exemplo:**

```text
3.1.1
```

Se a versão for exibida, a instalação foi realizada com sucesso!

## 3. Conexão com Clusters em Produção

### Recomendações

Para conexões com clusters em produção, recomenda-se o uso de variáveis de ambiente VDP. Essa abordagem permite que mudanças nos clusters conectados sejam realizadas sem a necessidade de novo versionamento do projeto.

### Exemplo de Código

Utilize o código abaixo para configurar a conexão com os clusters:

```python
# Recuperando a variável de referência do cluster
import os
from bbmagic import Hdfs

if os.getenv('AMBIENTE') == 'MODELAGEM':
  user = input('Informe sua matrícula:')
  cluster = 'CDP'
else:
  user = os.getenv('USER_KEYTAB')
  cluster = os.getenv('VDP_CLUSTER')

hdfs = Hdfs(user, cluster=cluster)
```

## 4. Listagem de Clusters Disponíveis

Os clusters disponíveis podem ser consultados utilizando os comandos abaixo:

BBMagic Listagem de Clusters

## 5. Versão Recomendada

A versão recomendada para uso é a 3.1.1, devido à sua maior compatibilidade com outras bibliotecas e suporte técnico. Essa versão é compatível com as versões Python 3.9 e Python 3.11.

> Atenção: Certifique-se de utilizar a versão recomendada para evitar problemas de compatibilidade.

---

# BBMagic e HDFS

## Introdução

Este documento apresenta uma visão geral sobre o uso da biblioteca BBMagic para interações com o sistema HDFS. A BBMagic é um wrapper simples sobre a classe PyWebHdfsClient, que facilita o download e upload de arquivos no HDFS. Ela inclui o comando Kinit para autenticação via Kerberos e oferece uma função prática para upload de arquivos.

Aqui, você aprenderá como configurar e utilizar a BBMagic para acessar e manipular arquivos no HDFS.

## Visão Geral sobre a Ferramenta

A BBMagic é uma biblioteca que simplifica a interação com o HDFS. Suas principais funcionalidades incluem:

- Autenticação simplificada: Suporte para autenticação via keytab ou matrícula e senha SISBB.
- Operações no HDFS: Upload, download, listagem, renomeação e exclusão de arquivos.
- Configuração de clusters: Conexão com diferentes clusters.

## Público-alvo

Este guia é destinado a desenvolvedores e analistas que utilizam o HDFS para armazenamento e manipulação de dados na Plataforma A2B2.

## Conhecimentos Necessários

Para utilizar a BBMagic, é necessário ter conhecimentos básicos em:

- Python;
- Conceitos de HDFS;
- Autenticação via Kerberos.

## Pré-requisitos para Utilização

Antes de começar a utilizar a BBMagic, certifique-se de:

- Ter acesso ao HDFS da A2B2;
- Possuir uma keytab válida ou credenciais de matrícula e senha SISBB;
- Ter a biblioteca BBMagic instalada no ambiente Python.

## Configurações

### Instalação da Biblioteca

Certifique-se de que a biblioteca BBMagic está instalada no seu ambiente Python. Caso não esteja, siga os passos para instalação indicados na introdução à BBMagic.

## Como Usar

### Importando a Biblioteca

Para começar, importe a biblioteca BBMagic no seu código:

```python
from bbmagic import Hdfs
```

### Obtendo Informações sobre a Classe Hdfs

Para consultar a documentação da classe Hdfs, utilize o comando:

```python
help(Hdfs)
```

### Conectando ao HDFS

A conexão ao HDFS pode ser feita utilizando uma keytab ou suas credenciais de matrícula e senha SISBB. É necessário especificar o cluster que deseja acessar no parâmetro cluster ao criar a instância. Caso o parâmetro cluster seja omitido, o BBMagic se conectará ao cluster padrão (HDP_3).

```python
# Substitua 'f0000000' pela sua matrícula
hdfs = Hdfs('f0000000', cluster="HDP_3")

# A linha abaixo também conectaria ao cluster HDP_3
# hdfs = Hdfs('f0000000')
```

Para mais informações sobre a conexão com clusters em produção, consulte na introdução à BBMagic.

A sessão HDFS será iniciada na pasta /user/<nome-do-usuario>/ ou /user/<keytab>/.

## Operações Básicas no HDFS

### Upload de Arquivos

Para realizar o upload de um arquivo para o HDFS, utilize o seguinte comando:

```python
# Defina o nome que deseja para o arquivo no HDFS
hdfs_file = 'arquivo.csv'

# Substitua pelo caminho do arquivo local
local_file = 'cogsley_sales.csv'

# Realize o upload do arquivo
hdfs_file_path = hdfs.upload(hdfs_file, local_file, overwrite=True)
```

### Verificando o Status do Arquivo

Após o upload, confirme se o arquivo foi enviado com sucesso:

```python
hdfs.status(hdfs_file_path)
```

### Listando Arquivos e Diretórios

Para listar os arquivos e diretórios na sua pasta pessoal no HDFS:

```python
# Listando arquivos e diretórios na pasta pessoal
hdfs.list(hdfs_file_path[:15])

# Para listar arquivos em outra pasta
# hdfs.list('/pasta/')
```

### Download de Arquivos

Para fazer o download de um arquivo do HDFS para o disco local:

```python
# Substitua 'nome_do_arquivo.csv' pelo nome e extensão do arquivo
# que deseja salvar localmente
download_file = hdfs.download(hdfs_file, 'nome_do_arquivo.csv', overwrite=True)
```

### Renomeando Arquivos

Para renomear um arquivo no HDFS:

```python
# Renomeando o arquivo enviado
hdfs.rename(hdfs_file_path, 'arquivo_renomeado.csv')

# Renomeando outros arquivos
# hdfs.rename('/pasta/arquivo.csv', '/pasta/arquivo_renomeado.csv')
```

### Deletando Arquivos

Para deletar um arquivo no HDFS:

```python
# Deletando o arquivo enviado e renomeado
hdfs.delete(hdfs_file_path[:15]+'arquivo_renomeado.csv')

# Deletando outros arquivos
# hdfs.delete('/pasta/arquivo.csv')
```

```python
# Listando os arquivos e diretórios da sua pasta pessoal após deletar
hdfs.list(hdfs_file_path[:15])

# Listando arquivos e diretórios de outras pastas
# hdfs.list('/pasta/')
```

### Utilizando Constantes para Paths

Para otimizar o código, você pode declarar constantes com o path padrão que deseja usar no HDFS. Isso facilita operações como upload, download e acesso a arquivos.

```python
# Definindo um path padrão e concatenando
HDFS_PATH = '/tmp/'
hdfs.upload(HDFS_PATH+'arquivo_remoto.txt', 'pasta_local/arquivo_local.txt', overwrite=True)

# Definindo um path padrão com URI completa
HDFS_PATH2 = '/tmp/arquivo_remoto.txt'
hdfs.upload(HDFS_PATH2, local_file, overwrite=True)
```

### Deletando Arquivos Criados

```python
# Deletando os arquivos criados acima
hdfs.delete(HDFS_PATH+'arquivo_remoto.csv')
hdfs.delete(HDFS_PATH2)
```

---

# BBMagic e Spark

## Introdução

Este documento apresenta as funcionalidades e instruções para utilização do BBMagic com o módulo Spark, que permite:

- Configurar automaticamente o sparkmagic;
- Conectar ao HDP2 ou HDP3;
- Criar sessões Spark com dimensionamento de recursos dinâmicos;
- Configurar automaticamente os drivers para conexão com o DB2, realizando o upload para o HDFS caso não sejam encontrados em /user/<nome-do-usuario>/.bbmagic/.

## Criando uma sessão Spark

Para criar uma sessão Spark utilizando o BBMagic, siga os passos abaixo:

**Passo 1. Importe o módulo Spark da biblioteca BBMagic:**

```python
from bbmagic import Spark
```

**Passo 2. Valide a instalação imprimindo a ajuda da classe Spark, que fornece a descrição de parâmetros avançados para a criação da sessão:**

```python
help(Spark)
```

**Passo 3. Inicie uma sessão Spark com o seguinte comando:**

```python
spark = Spark('', username='', cluster=<"nome_do_cluster">, db2=)
```

### Parâmetros:

- nome_da_sessão: Nome da sessão Spark.
- username: Matrícula ou keytab para autenticação.
- cluster: Nome do cluster ao qual deseja se conectar (ex.: "HDP_3").
- db2: Define se a conexão JDBC ao DB2 será configurada automaticamente (True ou False).

### Exemplo de uso:

```python
# Substitua a chave fictícia abaixo pela sua chave
spark = Spark('testebbmagic', username='f0000000', cluster="HDP_3", db2=True)
```

Para mais informações sobre a conexão com clusters em produção, consulte a introdução da BBMagic.

## Sessão Spark ativa

## Enviando comandos para a sessão Spark

Após abrir uma sessão Spark, você pode enviar comandos ao cluster adicionando %%spark no início da célula de código.

### Exemplo:

```python
%%spark
import sys
sys.version
```

Caso haja mais de uma sessão Spark aberta, especifique a sessão desejada utilizando a flag -s seguida do nome da sessão:

```python
%%spark -s 
```

### Exemplo:

```python
%%spark -s testebbmagic
import sys
sys.version
```

## Leitura de arquivos no HDFS

Para ler um arquivo no HDFS via Spark, é necessário realizar o upload do arquivo para o HDFS. Caso ainda não tenha feito isso, execute as células da seção anterior sobre HDFS.

> ⚠️ Atenção: Se você não executou as células do HDFS da seção anterior, será necessário executá-las para que a leitura do arquivo no HDFS funcione corretamente. Caso contrário, ocorrerá um erro de variáveis não definidas.

### Exemplo de upload de arquivo para o HDFS:

```python
# Fazendo upload de um arquivo local para o HDFS
# conforme as variáveis previamente configuradas
hdfs_file_path = hdfs.upload(hdfs_file, local_file, overwrite=True)
```

### Exemplo de leitura de arquivo no HDFS via Spark:

```python
%%time
%%spark

df = spark.read.csv('arquivo.csv', header=True)
df.head()
```

Utilize a opção %%time (sempre acima do %%spark) para obter o tempo de execução da célula.

## Leitura de tabelas no DB2

Para realizar a leitura de uma tabela no DB2, utilize os comandos abaixo:

### Exemplo 1: Listar tabelas no DB2

```python
%%time
%%spark

spark.sql("SHOW TABLES in db2opr").select('tableName').collect()
```

### Exemplo 2: Consultar dados em uma tabela do DB2

```python
%%time
%%spark

df = spark.sql("SELECT cod FROM db2mci.cliente LIMIT 100")
type(df.toPandas())
```

---

# Fonte de Dados - DB2

Este documento fornece instruções detalhadas sobre como utilizar o pacote BBMagic para interagir com a base de dados DB2 em notebooks. O objetivo é facilitar a conexão, consulta e manipulação de dados no DB2 utilizando o módulo Db2.

## 1. Introdução

O pacote Db2 do BBMagic oferece uma série de recursos para abstrair e facilitar o uso da base de dados DB2 diretamente em notebooks. Este guia apresenta as principais funcionalidades do pacote e como utilizá-las de forma eficiente.

Para importar o módulo, execute a célula abaixo:

```python
from bbmagic import Db2
```

## 2. Criando uma Conexão

Para criar uma instância de conexão ao DB2, utilize o comando abaixo:

```python
db2 = Db2()
```

O URL padrão de conexão é gwdb2.bb.com.br:50100/BDB2P04.

### Utilizando Variáveis de Ambiente

Se as variáveis de ambiente DB2_USER, DB2_PASSWORD e DB2_DATABASE estiverem configuradas, o módulo utilizará essas credenciais automaticamente.

### Solicitando Credenciais via Prompt

Caso as variáveis de ambiente não estejam configuradas, o sistema solicitará o usuário e a senha impessoais via prompt.

### Passando o Usuário como Parâmetro

Você também pode passar o usuário impessoal diretamente como parâmetro. Nesse caso, apenas a senha será solicitada via prompt.

```python
# Substitua 'seu_usuario' pelo seu usuário impessoal
db2 = Db2('seu_usuario')
```

### ⚠️ Atenção!

> Para acessar o DB2, é necessário um usuário impessoal. Caso você não possua um, verifique com o seu coordenador como requisitá-lo.

Para obter mais informações sobre o módulo Db2, execute o comando:

```python
help(Db2)
```

## 3. Exibindo Schemas e Tabelas

### Exibindo Schemas

Para listar todos os schemas disponíveis no banco de dados, utilize:

```python
db2.show_schemas()
```

### Filtrando Schemas

Você pode filtrar os schemas utilizando palavras-chave. Por exemplo:

```python
df = db2.show_schemas()
df[df.SCHEMA.str.contains('MCI')]
```

### Exibindo Tabelas de um Schema

Para listar todas as tabelas de um schema específico, utilize:

```python
db2.show_tables('DB2MCI')
```

## 4. Executando Consultas SQL

Para realizar consultas SQL no DB2, utilize o método query() do objeto Db2. Veja um exemplo:

```python
sql = "SELECT cod, cod_cpf_cgc, cod_tipo FROM db2mci.cliente ORDER BY cod LIMIT 250000"
resultado = db2.query(sql)
resultado
```

## 5. Trabalhando com Resultados em Blocos

Por padrão, o BBMagic retorna os resultados das consultas em blocos de 2500 linhas, utilizando pandas.DataFrame. Isso evita problemas de memória ao lidar com grandes volumes de dados.

### Exemplo de Processamento em Blocos

```python
%%time

total_pj = 0

for num, blocos in enumerate(resultado):
  clientes_pj = blocos.query('COD_TIPO == 2')
  print(f'Encontrados {len(clientes_pj)} clientes PJ no bloco #{num}.')
  total_pj += len(clientes_pj)

print(f'Encontrados {total_pj} clientes PJ.')
```

### 💡 Dica!

Utilize o comando mágico %%time no início da célula para medir o tempo de execução.

## 6. Processando Resultados com map()

A função map() pode ser utilizada para aplicar uma função sobre os blocos de resultados. Veja o exemplo:

```python
# Refazemos a consulta pois o resultado foi consumido no exemplo anterior
sql = 'SELECT cod, cod_cpf_cgc, cod_tipo FROM db2mci.cliente ORDER BY cod LIMIT 250000'
resultado = db2.query(sql)
resultado
```

```python
%%time

def conta_pj(df) -> int:
  return df.query('COD_TIPO == 2').shape[0]

total_pj = sum(map(conta_pj, resultado))

print(f'Encontrados {total_pj} clientes PJ.')
```

## 7. Carregando Resultados Inteiros na Memória

Se você tiver certeza de que o resultado da consulta cabe na memória da máquina, utilize o parâmetro chunksize=None no método db2.query().

### Exemplo

A tabela DB2MCI.TAB_OCUPACAO possui apenas 295 linhas. Veja como carregar o resultado completo:

```python
db2.describe("DB2MCI", "TAB_OCUPACAO")
```

```python
%%time

tab_ocupacao = db2.query("SELECT * FROM db2mci.tab_ocupacao", chunksize=None)

print(f"Tabela db2mci.tab_ocupacao {tab_ocupacao.shape[0]} linhas e {tab_ocupacao.shape[1]} colunas.")

tab_ocupacao.head()
```

---

# Introdução – O que é o pacote Python PLTBBSIA?

O PLTBBSIA é um pacote Python desenvolvido para o AnalyticsLabb com o objetivo de simplificar o envio de arquivos gerados por projetos analíticos para o ambiente Mainframe do Banco do Brasil, por meio da API REST do BB SIA (Sistema de Integração via Arquivos).

Para reduzir a complexidade da integração direta com o BB SIA, o time do AnalyticsLabb desenvolveu uma API intermediária que abstrai aspectos técnicos como autenticação, formatação de requisições e regras específicas do sistema. Dessa forma, o envio de arquivos pode ser realizado de forma padronizada, segura e com poucas linhas de código, sem necessidade de configurações adicionais por parte dos projetos consumidores.

### ⚠️ Atenção

> Em caso da ocorrência de algum problema na execução ou utilização da biblioteca do BBSIA, por gentileza entrar em contato com a UOR Responsável: UOR - 459594.

## Diagrama do fluxo BBSIA

## Glossário

- BBSIA: Interface para gerenciamento de FTAs no envio de arquivos ao Mainframe.
- FTA (File Transfer Agreement): Acordo de transferência de arquivos.
- GMTEDI: Sistema corporativo para gerenciamento de transferências.
- AnalyticsLabb: Plataforma analítica do Banco do Brasil.

## Instalação do PLTBBSIA

**Passo 1. Execute o comando abaixo em um terminal para instalar o pacote:**

```bash
pip install big_pltbbsia --user
```

O processo de instalação deve levar alguns segundos. Após a instalação, reinicie o kernel do Jupyter Notebook.

**Passo 2. Verifique a instalação utilizando um Jupyter Notebook. Execute os comandos abaixo:**

```python
import pltbbsia
print(pltbbsia.__version__)
```

A versão do PLTBBSIA deverá ser exibida. Exemplo: 2.0.9.

**Passo 3. Verifique se ao menos uma das seguintes variáveis de ambiente está configurada com o ID do seu projeto:**

```python
import os
print(os.environ.get("PROJETO_ID"))
print(os.environ.get("PROJECT_ID"))
```

> ⚠️ Atenção
> Se ambas as variáveis estiverem configuradas com valores diferentes, corrija para que apenas uma tenha o valor correto. O PROJECT_ID pode ser obtido no detalhamento do projeto no AnalyticsLabb na Plataforma BB:

```python
os.environ["PROJECT_ID"] = "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
os.environ["PROJETO_ID"] = None
```

## Interface BBSIA

A interface BBSIA foi criada para facilitar o gerenciamento de FTAs (File Transfer Agreements) utilizados no envio de arquivos ao Mainframe do Banco do Brasil, permitindo o acompanhamento e a administração dessas configurações de forma centralizada.

As principais funcionalidades disponíveis incluem:

- Consulta de protocolos GMTEDI, possibilitando o acompanhamento do status de envio de arquivos;
- Consulta de FTAs cadastrados no GMTEDI;
- Cadastro de FTAs no BBSIA para habilitar o envio de arquivos;
- Consulta de FTAs previamente cadastrados no BBSIA.

## Acesso à interface

Para acessar a interface na Plataforma BB, navegue pelo menu:

Analytics | IA → Serviços → Solicitações → BBSIA

## Variáveis de Ambiente Utilizadas

| Variável | Descrição |
| --- | --- |
| PROJECT_ID | Identificador do projeto no AnalyticsLabb |
| PROJETO_ID | Variante legada do PROJECT_ID |
| MODO_FTA | Define o FTA ativo para envio |
| TOKEN_FUNCOES_AJUDA | Token de autenticação corporativa |

## Ambiente de Execução

Ao instanciar a classe BBSIA, o ambiente de execução do projeto será identificado automaticamente:

```python
from pltbbsia import BBSIA

bbsia = BBSIA()

print(bbsia.ambiente)
# $> DESENVOLVIMENTO
```

Projetos no modo criativo serão configurados para o ambiente de DESENVOLVIMENTO.
Projetos publicados na área corporativa serão configurados para o ambiente de PRODUÇÃO.
Se necessário, é possível configurar manualmente o ambiente ao instanciar a classe:

```python
from pltbbsia import BBSIA

bbsia = BBSIA(ambiente='HOMOLOGACAO')

print(bbsia.ambiente)
# $> HOMOLOGACAO
```

> ⚠️ Atenção
> Não é possível acessar o ambiente de PRODUÇÃO fora da área corporativa. A biblioteca retornará um erro nesse caso.

#### Exemplo de erro ao tentar acessar o ambiente de PRODUÇÃO fora da área corporativa:

```python
from pltbbsia import BBSIA

bbsia = BBSIA(ambiente='PRODUCAO')
# $> Traceback (most recent call last):
# $>   File "", line 1, in 
# $> VariavelAmbienteNaoEncontradaException: (90, 'Variável de ambiente TOKEN_FUNCOES_AJUDA não encontrada.')
# -- OU --
# $> Traceback (most recent call last):
# $>   File "", line 1, in 
# $> TokenInvalidoException: (160, '403 Token não reconhecido. Contate o suporte.')
```

## Cadastro de FTA

Para cadastrar um FTA para envio de arquivos:

**Passo 1. Crie um FTA no GMTEDI. Certifique-se de que ele está ativo e configurado com o cliente de origem como o usuário impessoal BB_BIG_Big_Data_Analytics.**

**Passo 2. Use o método bbsia.cadastrar_fta() para registrar o FTA na base de dados. Informe o número do FTA (int) e o nome do FTA (string):**

```python
from pltbbsia import BBSIA

bbsia = BBSIA()

os.environ["MODO_FTA"] = bbsia.cadastrar_fta(, )
```

> ⚠️ Atenção
>
> Cada FTA deve ser criado e cadastrado no mesmo ambiente em que será utilizado.
> Caso utilize um FTA customizado, teste o projeto com um FTA criado em DESENVOLVIMENTO ou HOMOLOGAÇÃO antes de enviá-lo para PRODUÇÃO.
> Por padrão, o BBSIA utiliza um FTA já configurado para o envio ao Mainframe, não sendo necessário cadastro prévio.

## Enviando Arquivos para o Mainframe

### Tamanho Máximo do Arquivo

> ⚠️ Atenção
> O tamanho máximo permitido para envio é de 1GB. Caso necessite enviar arquivos maiores, abra uma issue solicitando a customização do seu projeto.

### Definindo o Layout do Arquivo

Os arquivos enviados ao Mainframe geralmente possuem dados em formato de largura fixa. Exemplo:

```text
0000010002021061212515 ANA MARIA MARIANA99
0000010002021071212515    JOAO DA SILVA99
0000010002021081213515 MARIO DE ANDRADE89
```

O formato do arquivo (tamanho dos campos, tipo dos dados) deve ser definido em conjunto com o time do Mainframe responsável pela aplicação que irá consumir os dados.

### Gerando o Nome do Arquivo

Os nomes dos arquivos enviados seguem o padrão:

```text
.BIG..D[.P].
```

Exemplo de nomes de arquivo:

BRP.BIG.M5AAAAAA.D200601.SS000125
HMH.BIG.T2UW1234.D200610.SS000125
BRT.BIG.M3JC9F2T.D200525.P007.SS000125
Para gerar um nome de arquivo, utilize o método BBSIA.sugerir_nomes_arquivos():

```python
from pltbbsia import BBSIA

bbsia = BBSIA()

sugestoes = bbsia.sugerir_nomes_arquivos("D")
print(sugestoes)
```

### Enviando o Arquivo

```python
# Criamos o arquivo de texto e escrevemos conforme o layout
nome_arquivo = "M1AD0001"
with open(nome_arquivo, "w") as f:
  f.write("0000010002020061203515ANA MARIA MARIANA")

bbsia = BBSIA()
bbsia.enviar_arquivo(nome_arquivo)
# $> Enviando arquivo M1AD0001  Tentativa  1 ... pronto
```

Por padrão, o arquivo será enviado para o ambiente Mainframe correspondente ao ambiente do projeto.

---

# Introdução

Este documento descreve o funcionamento de um projeto analítico no AnalyticsLabb, abordando:

- Os diferentes modos de desenvolvimento;
- Recursos disponíveis;
- Ambiente de desenvolvimento;
- Variáveis de ambiente e boas práticas para gerenciá-las.
O objetivo é fornecer um guia claro e objetivo para desenvolvedores que utilizam a plataforma.

## Cadastro

Ao criar um modelo no AnalyticsLabb, uma instância do Ansible é responsável por:

- Criar automaticamente um repositório no GitLab;
- Disponibilizar uma instância de Ambiente de Desenvolvimento (JupyterLab ou VS Code).
Existem dois modos de desenvolvimento disponíveis para a criação do Ambiente de Desenvolvimento:

### Projeto Criativo

- Permite criar projetos sem integração com os sistemas corporativos do BB.
- O código-fonte será registrado como Open Source.
- Ideal para provas de conceito, análises ad-hoc, testes e aprendizado de novas ferramentas.

### Projeto Corporativo

- Permite criar projetos com integração aos sistemas corporativos do BB.
- Requer acesso a uma Sandbox de um Domínio de Informação.
- Deve ser utilizado para implementação de modelos em produção e obrigatoriamente cadastrado no GAIA.

## Recursos

Os recursos disponíveis variam de acordo com o tipo de projeto:

| Tipo de Projeto | CPU/MAX | MEM/MAX | Storage |
| --- | --- | --- | --- |
| Projeto Criativo | 4 | 8Gb | 16Gb |
| Projeto Corporativo | 6 | 16Gb | 16Gb |

## Ambiente de Desenvolvimento

### Onde está rodando?

A instância do Ambiente de Desenvolvimento é um container Docker que roda na nuvem do cluster Kubernetes k8s-bigdata, com sistema operacional CentOS 7.6.1. As versões de linguagem disponíveis são:

- JupyterLab: Python (3.9 ou 3.11), R (4.2.1), SAS;
- VS Code: Python (3.6.8).
> ⚠️ Atenção: O suporte ao Python 3.6.8 no AnalyticsLabb foi descontinuado a partir de 03/02/2025. Após a disponibilização do Python 3.9 para o ambiente VS Code, a opção será reativada.

## Bot de Desligamento

Para otimizar recursos, um bot desliga automaticamente os projetos inativos:

- Projetos Criativos: 1 dia de inatividade;
- Projetos Corporativos: 2 dias de inatividade.
> 💡Dica: Salve e atualize seus arquivos no GitLab regularmente. Para reativar um projeto, acesse-o diretamente em Analytics | IA > AnalyticsLabb.

## Pacotes

Ao iniciar um projeto, o ambiente de desenvolvimento já possui o Python selecionado e alguns pacotes pré-instalados. Para verificar os pacotes disponíveis, utilize o comando:

```bash
pip freeze
```

Para instalar novos pacotes, utilize o comando:

```bash
pip install  --user
```

Por exemplo:

```bash
pip install pandas --user
```

> ⚠️ Atenção: Consulte as compatibilidades de bibliotecas na documentação oficial em caso de falhas na instalação.

## Acesso a Sites Externos

Os sites externos liberados para uso no AnalyticsLabb estão nesta lista.

> ⚠️Solicitação de Inclusão: Para incluir novos sites, abra uma issue.

## Variáveis de Ambiente

O uso de variáveis de ambiente é uma prática essencial para manter a segurança e confiabilidade de dados sensíveis, como:

- credenciais de login;
- senhas;
- tokens de acesso;
- configurações específicas do ambiente.
Variáveis de ambiente são valores dinâmicos armazenados no ambiente (container) onde o projeto está executando.

Isso permite que o código acesse essas informações sem precisar armazená-las diretamente no código-fonte, aumentando a segurança e a flexibilidade da aplicação.

### Uso de variáveis de ambiente para paths

Outro uso comum de variáveis de ambiente é para definir paths (caminhos de arquivos ou diretórios) que podem variar entre ambientes.

Por exemplo:

Em Windows, um caminho pode ser:
```text
C:\Users\Usuario\My Documents\arquivo.txt
```

Em Unix/Linux, o mesmo arquivo poderia estar em:
```text
/home/Usuario/Documents/arquivo.txt
```

Se esse caminho estiver fixado diretamente no código, podem ocorrer problemas devido a:

- diferenças entre sistemas operacionais;
- diferentes usuários;
- mudanças de ambiente.
Uma solução é cada ambiente manter uma variável de ambiente com o caminho base, enquanto o desenvolvedor apenas complementa o caminho no código.

Essa mesma lógica pode ser aplicada aos diretórios de tabelas do Hive no contexto de Big Data.

### Exemplo: variável de ambiente AMBIENTE

Nos projetos existe uma variável padrão chamada:

```text
AMBIENTE
```

Ela indica em qual ambiente o código está sendo executado:

- "MODELAGEM"
- "DESENVOLVIMENTO"
- "HOMOLOGACAO"
- "PRODUCAO"
Um exemplo de uso dessa variável no código:

```python
if os.environ["AMBIENTE"] == 'MODELAGEM':
  print('Código rodando em Modelagem.')

elif os.environ["AMBIENTE"] == 'DESENVOLVIMENTO':
  print('Código rodando em Desenvolvimento.')

elif os.environ["AMBIENTE"] == 'HOMOLOGACAO':
  print('Código rodando em Homologação.')

else:
  print('Código rodando em Produção.')
```

### Exemplo prático com USERNAME e USER_KEYTAB

Outra variável importante é:

```text
USERNAME
```

Em produção, ela aponta para a Keytab do usuário corporativo.

Podemos combinar AMBIENTE e USER_KEYTAB para controlar automaticamente qual usuário será utilizado:

```python
# Se em Modelagem
if os.environ["AMBIENTE"] == 'MODELAGEM':
  usuario = 'c1325226' # sua chave

# Se em Produção (modelos Batch)
# Se em Desenv, Homolog ou Produção (modelos Online)
else:
  usuario = os.environ.get('USER_KEYTAB') # variável de ambiente

spark = Spark(session_name='teste_var_env',
            username=usuario)
```

Nesse caso:

- em Modelagem, a sessão Spark usa sua matrícula (chave C ou F);
- em Produção, a sessão usa o usuário corporativo da Keytab.
Tudo ocorre automaticamente, sem necessidade de intervenção manual.

### Como listar variáveis de ambiente

Para listar todas as variáveis disponíveis no ambiente do projeto, execute:

```python
import os
os.environ
```

### Variáveis de Ambiente Padrão

Os sistemas do AnalyticsLabb possuem diversas variáveis de ambiente padrão que não devem ser alteradas.

Essas variáveis garantem o funcionamento correto do sistema e estão disponíveis em todos os projetos.

!!! error "Alteração de Variáveis de Ambiente Padrão" Alterar variáveis de ambiente padrão pode comprometer o funcionamento do projeto e causar falhas que, em alguns casos, não podem ser recuperadas. Não altere os valores dessas variáveis.

A seguir estão algumas das principais variáveis.

### PROJECT_ID

Variável que contém o ID do projeto, utilizado como identificador único.

Em projetos mais antigos também pode aparecer como:

```text
PROJETO_ID
```

### CTMODATE

Variável de data no formato:

```text
YYYY-MM-DD
```

É altamente recomendável que modelos em produção utilizem CTMODATE como referência de data atual, em vez de usar:

```python
datetime.now()
```

### Vantagens

- Permite execuções com datas retroativas.
- Em execuções agendadas, o valor é atualizado automaticamente.
- Em execuções eventuais solicitadas via issue, é possível definir uma data específica.
Exemplo de solicitação de execução:

https://fontes.intranet.bb.com.br/big/publico/atendimento/-/issues

### Atenção em ambiente de Modelagem

Em Modelagem, o valor padrão da variável é:

```text
CTMODATE=2020-01-01
```

Por isso é necessário usar uma condicional no código:

```python
if os.environ["AMBIENTE"] == 'MODELAGEM':
  hoje = datetime.now().strftime('%Y-%m-%d')

else: # em Produção
  hoje = os.environ['CTMODATE']
```

Assim:

- em Modelagem, o código usa a data atual;
- em Produção, usa a variável controlada pelo sistema.

### Variáveis disponíveis apenas em Produção

Algumas variáveis não existem em Modelagem e estão disponíveis apenas em:

- Produção
- Homologação
- Desenvolvimento
Entre elas:

- KEYTAB → aponta para a Keytab do usuário corporativo
- USER_KEYTAB → retorna o nome do usuário corporativo
- DB2_DATABASE → banco de dados DB2 do ambiente
- DB2_HOST → host do banco DB2
- DB2_USER → usuário corporativo DB2
- DB2_PASSWORD → senha do usuário DB2

### Abstração de credenciais com BBMagic

A BBMagic abstrai o uso das credenciais do DB2.

A classe Db2:

- utiliza automaticamente as variáveis de ambiente disponíveis;
- solicita credenciais de usuário impessoal apenas se não encontrar essas variáveis.

### Variáveis de Projeto (VDP)

Também é possível criar variáveis de ambiente personalizadas para o projeto, chamadas de:

Variáveis de Projeto (VDP).

Essas variáveis podem armazenar:

- tokens
- logins
- senhas
- acessos a APIs
- conexões com outros bancos de dados
- diretórios no HDFS
- caminhos de tabelas Hive

### Regra de nomenclatura

Todas as variáveis de projeto devem iniciar com o prefixo:

```text
VDP_
```

**Exemplo:**

```text
VDP_SENHA_API
```

### Onde cadastrar as VDP

Variáveis de projeto podem ser cadastradas durante:

- implantação de modelos Batch
- implantação de modelos Online

### Exemplo de uso para paths do Hive

Os diretórios no Big Data costumam variar entre ambientes.

#### Modelagem / Sandbox

```text
/dados/transientes///hve/external/
```

#### Produção

```text
/dados/corporativos//hve/external/
```

Exemplo de implementação:

```python
if os.environ["AMBIENTE"] == 'MODELAGEM':
  tabela_hive = "/dados/transientes///hve/external/"

else:
  tabela_hive = os.environ['VDP_TABELA_HIVE']
```

Esse tipo de configuração aumenta a flexibilidade e produtividade dos modelos em produção.

As variáveis VDP_ ficam disponíveis nos ambientes em que foram cadastradas:

- Produção
- Homologação
- Desenvolvimento

### Uso de variáveis de ambiente em Modelagem (.env)

Para utilizar variáveis de ambiente também em Modelagem, é possível usar a biblioteca:

python-dotenv

https://pypi.org/project/python-dotenv/

### Instalação

Execute no terminal:

```bash
pip install python-dotenv --user
```

### Criando o arquivo .env

Crie um arquivo chamado:

```text
.env
```

Exemplo de criação via terminal:

```bash
echo 'VARIAVEL="valor"' >> .env
```

Exemplo para cadastrar a variável VDP_TABELA_HIVE:

```bash
echo 'VDP_TABELA_HIVE="/dados/transientes///hve/external/"' >> .env
```

### Carregando variáveis no notebook

No início do notebook (geralmente na célula de imports), adicione:

```python
%load_ext dotenv
%dotenv
```

Isso carregará automaticamente todas as variáveis do .env.

Depois disso, elas podem ser utilizadas normalmente:

```python
tabela_hive = os.environ['VDP_TABELA_HIVE']
```

Com esse comportamento:

- em Modelagem, o valor vem do .env
- em Produção, o valor vem da configuração de implantação

### Boas práticas de segurança

Evite armazenar senhas ou credenciais diretamente no código.

Sempre:

- armazene dados sensíveis em variáveis de ambiente;
- registre essas variáveis no arquivo .env;
- adicione o .env ao .gitignore.
Isso evita que credenciais sejam expostas no GitLab.

---

# Implantando um Projeto

## Visão Geral

Este documento apresenta uma visão detalhada sobre o processo de implantação de modelos na plataforma AnalyticsLabb da A2B2. Ele abrange as etapas de implantação de modelos online e batch, descreve os recursos necessários para o ambiente de produção e orienta sobre como acompanhar a execução dos projetos.

## Modelos Online

Os sistemas corporativos do BB utilizam a linguagem de programação Cobol. Para facilitar a comunicação entre esses sistemas e aplicações desenvolvidas em linguagens mais recentes, como Python, foi criado o barramento IIB, que funciona como uma interface de comunicação baseada em Java.

Quando utilizamos Python para comunicação com o IIB, como ocorre na maioria dos modelos desenvolvidos no AnalyticsLabb, utilizamos o Curió. O Curió é uma aplicação Java sidecar que opera no mesmo Pod do modelo implantado. Ele recebe chamadas via REST e se comunica com o IIB, permitindo a integração dos modelos analíticos desenvolvidos em Python com os sistemas corporativos do BB.

## Processo de Implantação

### Criação da Imagem Docker:

Durante a implantação de um projeto no AnalyticsLabb, utilizamos o S2I (Source-to-Image) para construir uma imagem Docker a partir de uma imagem base.
As variáveis específicas do projeto, como o operation_id, são configuradas para criar uma API pronta para consumo.

### Deploy no ARQ 3.0:

A implantação do microsserviço é realizada no ARQ 3.0 por meio do portal OAAS.

### Diagrama de Funcionamento Online

O diagrama abaixo ilustra o fluxo de funcionamento dos modelos online:

diagrama-online

## Modelos Batch

Na modalidade batch, o modelo é encapsulado em uma imagem Docker, garantindo um ambiente isolado e completo para sua execução. O processo pode ser dividido em três grandes blocos:

### Construção e Implantação no AnalyticsLabb:

Os modelos são desenvolvidos e implantados no AnalyticsLabb. Durante a implantação, eles são cadastrados no Control-M, que atua como um job scheduler.

### Agendamento pelo Control-M:

O Control-M é responsável por iniciar a execução do modelo, utilizando as informações fornecidas pelo AnalyticsLabb.

### Execução no Kubernetes (K8S):

O agente Batch recebe as informações do Control-M e executa o modelo no Kubernetes (K8S).
O isolamento é garantido por namespaces no K8S.
O agente Batch monitora a execução do job por meio de HealthChecks e retorna o status ao Control-M após a finalização.

### Diagrama de Funcionamento Batch

O diagrama abaixo apresenta o fluxo de funcionamento dos modelos batch:

diagrama-batch

## Como acompanhar a execução?

O acompanhamento dos projetos em execução pode ser realizado por meio dos seguintes painéis:

### Projetos Online:

Monitoramento Online
monitoracao-online

### Projetos Batch:

Monitoramento Batch
monitoracao-batch

!!! error "Acesso à monitoração" Caso não seja possível acessar os endereços de monitoração ou caso deseje maiores informações sobre erros em projetos em execução, abra uma issue.

## Recursos em ambiente de produção

Após o refinamento e a aplicação de boas práticas para otimização de desempenho, os recursos alocados em ambiente de produção são menores do que os utilizados no ambiente de desenvolvimento/modelagem.

### Recursos para Modelos Online

Na modalidade online, os recursos são calculados por réplica (instâncias paralelas do projeto).

| Recurso | Valor | Observações |
| --- | --- | --- |
| CPU | 1 |  |
| Memória | 500MB |  |
| Storage | - | Não há persistência do filesystem |
| Réplicas | 3 |  |

### Recursos para Modelos Batch

Na modalidade batch, os recursos são calculados por job (execução do projeto).

| Recurso | Valor | Observações |
| --- | --- | --- |
| CPU | 2 |  |
| Memória | 4GB |  |
| Storage | - | Não há persistência do filesystem |

!!! info "Aumento de recursos" Devem ser envidados todos os esforços para que o projeto seja executado dentro do padrão de recursos acima. Em situações excepcionais, a solicitação de análise para aumento de recursos em produção poderá ser feita por meio de uma issue.
