# Documentação Técnica do Nosso Ambiente Analítico

## Versão final enxuta

Esta documentação descreve o **nosso ambiente analítico de trabalho**: como o projeto roda, como se conecta ao Big Data, como organiza caminhos, como usa variáveis de ambiente e como cria a sessão Spark.

O foco é exclusivamente no que usamos no projeto:

* ambiente local do projeto;
* variáveis de ambiente;
* BBMagic;
* HDFS;
* Hive;
* Spark;
* DB2;
* Hue;
* estrutura oficial de pastas;
* camada própria de criação da sessão Spark;
* regras práticas de uso.

Esta versão não traz código. O objetivo é documentar o funcionamento e as decisões do ambiente.

---

# 1. Visão geral

Nosso ambiente tem duas camadas principais:

1. **Ambiente local do projeto**
   É o container acessado pelo JupyterLab. Nele ficam os notebooks, arquivos do projeto, configurações locais, `.env` de modelagem, requirements e o código que inicia conexões.

2. **Ambiente Big Data**
   É o ambiente distribuído onde ficam HDFS, Hive, Spark, DB2 acessado via conexão, Hue e os dados em escala.

A regra central é simples:

> O notebook organiza e dispara o trabalho. O cluster armazena e processa os dados grandes.

Por isso, um arquivo local não é automaticamente um arquivo HDFS, uma variável local não existe automaticamente no Spark e uma biblioteca instalada no container não necessariamente existe nos executores Spark.

---

# 2. Componentes do nosso ambiente

## 2.1 JupyterLab

O JupyterLab é a interface de desenvolvimento do projeto.

Usamos o JupyterLab para:

* editar notebooks;
* executar validações;
* carregar configurações locais;
* iniciar sessão Spark;
* acessar HDFS, Hive e DB2;
* testar consultas;
* acompanhar resultados durante a modelagem.

O JupyterLab roda no container do projeto. Ele não é o cluster Big Data.

## 2.2 Container do projeto

O container é o ambiente local onde o projeto roda durante o desenvolvimento.

Nele ficam:

* notebooks;
* arquivos `.py`;
* arquivos `.sql`;
* arquivos de configuração;
* requirements;
* `.env` de modelagem;
* bibliotecas instaladas localmente;
* variáveis de ambiente disponíveis no container.

O container deve ser tratado como ambiente de desenvolvimento e orquestração, não como local definitivo para dados grandes.

## 2.3 GitLab

O GitLab é o repositório oficial do projeto.

Devem ser versionados:

* código do projeto;
* documentação;
* notebooks relevantes;
* arquivos SQL;
* requirements;
* configurações sem segredo.

Não devem ser versionados:

* `.env` real;
* senhas;
* tokens;
* keytabs;
* arquivos temporários;
* bases de dados;
* saídas grandes;
* credenciais de DB2 ou de qualquer outro serviço.

---

# 3. Ambientes

O projeto deve se comportar de forma diferente conforme o valor de `AMBIENTE`.

## 3.1 Modelagem

Modelagem é o ambiente de desenvolvimento, teste e exploração.

Em Modelagem:

* usamos sandbox;
* usamos caminhos em `/dados/transientes`;
* podemos carregar `.env` local;
* podemos usar matrícula ou configuração local autorizada;
* podemos recriar virtualenv Spark;
* podemos validar consultas e paths antes de publicar.

Modelagem não deve usar path produtivo como padrão.

## 3.2 Produção

Produção é o ambiente controlado.

Em Produção:

* não usamos `.env` local;
* não dependemos de matrícula pessoal;
* usamos keytab/usuário técnico;
* usamos variáveis cadastradas no ambiente;
* usamos `CTMODATE` como data de referência;
* usamos caminhos corporativos;
* evitamos qualquer dependência manual.

Produção não deve depender de arquivo local, path pessoal ou configuração criada apenas no notebook.

---

# 4. Variáveis de ambiente

Variáveis de ambiente são a base da separação entre Modelagem e Produção.

Elas evitam que o código fique preso a usuário, path, senha, data ou cluster específico.

## 4.1 Variáveis principais

| Variável       | Uso no projeto                                                                  |
| -------------- | ------------------------------------------------------------------------------- |
| `AMBIENTE`     | Define se o projeto está em Modelagem, Desenvolvimento, Homologação ou Produção |
| `CTMODATE`     | Data de referência controlada pelo ambiente, principalmente em Produção         |
| `KEYTAB`       | Referência à keytab/usuário técnico quando disponível                           |
| `USER_KEYTAB`  | Nome do usuário técnico/keytab                                                  |
| `DB2_HOST`     | Host do DB2 do ambiente                                                         |
| `DB2_DATABASE` | Banco DB2 do ambiente                                                           |
| `DB2_USER`     | Usuário DB2 do ambiente                                                         |
| `DB2_PASSWORD` | Senha DB2 do ambiente                                                           |
| `VDP_*`        | Variáveis de projeto cadastradas por ambiente                                   |

## 4.2 `AMBIENTE`

`AMBIENTE` orienta as decisões do projeto.

A lógica geral é:

* se for Modelagem, carregar configurações locais controladas;
* se não for Modelagem, usar variáveis oficiais do ambiente.

Não devemos sobrescrever `AMBIENTE` manualmente para forçar comportamento.

## 4.3 `CTMODATE`

`CTMODATE` é a data de referência da execução.

Em Produção, ela deve ser usada no lugar de data calculada diretamente pelo relógio do notebook. Isso permite execução retroativa e reprocessamento.

Em Modelagem, o valor pode não representar a data real. Por isso, a camada do projeto pode definir uma data local de trabalho para desenvolvimento.

## 4.4 Variáveis `VDP_`

As variáveis `VDP_` guardam valores específicos do projeto por ambiente.

Devem ser usadas para:

* paths HDFS;
* nomes de sandbox;
* schemas;
* tabelas;
* clusters;
* parâmetros de execução;
* credenciais autorizadas;
* configurações que mudam entre ambientes.

## 4.5 `.env` em Modelagem

O `.env` é usado apenas para simular variáveis em Modelagem.

Regras:

* não versionar `.env` real;
* não usar `.env` em Produção;
* manter nomes compatíveis com as variáveis oficiais;
* não colocar segredo em arquivo versionado;
* usar apenas como apoio de desenvolvimento.

---

# 5. BBMagic

BBMagic é a biblioteca usada como camada principal de conexão com o ecossistema analítico.

No nosso ambiente, ela é usada principalmente para:

* autenticação Kerberos;
* conexão com HDFS;
* criação de sessão Spark;
* configuração SparkMagic/Livy;
* conexão com DB2;
* uso de jars e virtualenv na sessão Spark;
* integração com variáveis de ambiente.

A BBMagic facilita a conexão, mas não decide sozinha:

* qual path usar;
* qual ambiente está correto;
* qual tabela deve ser lida ou gravada;
* se um dado pode ir para Produção;
* se a sessão Spark está dimensionada corretamente;
* se a lógica do pipeline está eficiente.

Essas decisões continuam sendo responsabilidade do projeto.

---

# 6. HDFS

HDFS é o sistema de arquivos distribuído do ambiente Big Data.

Usamos HDFS para armazenar arquivos que precisam ser acessados pelo cluster, pelo Spark ou pelo Hive.

## 6.1 Tipos de caminho HDFS no nosso projeto

Devemos pensar em três tipos de caminho:

1. **Pasta pessoal do usuário/keytab**
   Usada para apoio técnico, arquivos temporários de sessão e artefatos da BBMagic.

2. **Área de sandbox/modelagem**
   Usada para dados do projeto em desenvolvimento.

3. **Área corporativa/produção**
   Usada para dados oficiais ou produtivos.

## 6.2 Pasta pessoal

A pasta pessoal segue o conceito:

* `/user/{usuario}`;
* `/user/{keytab}`.

Ela pode conter, por exemplo, artefatos da BBMagic, como ambientes virtuais em:

* `/user/{keytab}/.bbmagic/envs`.

Essa área não deve ser usada como destino oficial de dados do projeto.

## 6.3 `/tmp`

`/tmp` é área temporária.

Pode ser usada para teste ou apoio rápido, mas não deve ser usada como:

* destino definitivo;
* path de tabela Hive;
* área de produção;
* repositório oficial do projeto.

## 6.4 Área de modelagem

A área de modelagem fica em `/dados/transientes`.

Ela deve ser usada para dados da sandbox e desenvolvimento.

## 6.5 Área de produção

A área de produção fica em `/dados/corporativos`.

Ela deve ser usada para dados corporativos, controlados e produtivos.

---

# 7. Estrutura oficial de pastas

## 7.1 Modelagem

Estrutura oficial de modelagem:

```text
hdfs://modelagemha/dados/transientes/{sigla}/{sandbox}/dados_analiticos
hdfs://modelagemha/dados/transientes/{sigla}/{sandbox}/dados_brutos
hdfs://modelagemha/dados/transientes/{sigla}/{sandbox}/dados_trabalhados
hdfs://modelagemha/dados/transientes/{sigla}/{sandbox}/hve
hdfs://modelagemha/dados/transientes/{sigla}/{sandbox}/hve/external
```

## 7.2 Produção

Estrutura oficial de produção:

```text
hdfs://cdpprodescorha/dados/corporativos/{sigla}/dados_analiticos
hdfs://cdpprodescorha/dados/corporativos/{sigla}/dados_brutos
hdfs://cdpprodescorha/dados/corporativos/{sigla}/dados_trabalhados
hdfs://cdpprodescorha/dados/corporativos/{sigla}/hve
hdfs://cdpprodescorha/dados/corporativos/{sigla}/hve/external
```

## 7.3 Finalidade das pastas

| Pasta               | Uso                                                             |
| ------------------- | --------------------------------------------------------------- |
| `dados_brutos`      | Dados recebidos ou extraídos com pouca ou nenhuma transformação |
| `dados_trabalhados` | Dados tratados, padronizados ou intermediários                  |
| `dados_analiticos`  | Dados finais para análise, modelagem ou consumo analítico       |
| `hve`               | Área associada à organização Hive                               |
| `hve/external`      | Local físico esperado para tabelas externas Hive                |

## 7.4 Regra prática

Use:

* `/dados/transientes/{sigla}/{sandbox}` em Modelagem;
* `/dados/corporativos/{sigla}` em Produção;
* `/user/{usuario}` apenas como apoio pessoal/técnico;
* `/tmp` apenas para temporários.

Não misture esses papéis.

---

# 8. Hive

Hive é a camada de tabelas sobre dados armazenados no HDFS.

A tabela Hive possui metadados. O dado físico fica em um path HDFS.

Por isso, sempre separe mentalmente:

* database Hive;
* nome da tabela;
* schema;
* path físico;
* formato dos arquivos;
* partições;
* ambiente.

## 8.1 Tabelas externas

Tabelas externas devem apontar para o path físico correto.

No nosso padrão, a localização física de tabelas externas deve ficar dentro de `hve/external`, respeitando Modelagem ou Produção.

## 8.2 Cuidados

Antes de criar ou alterar tabela Hive, valide:

* ambiente correto;
* database correto;
* path correto;
* schema correto;
* permissões;
* risco de sobrescrita;
* impacto em consumidores.

---

# 9. Spark

Spark é o motor distribuído usado para processar dados no cluster.

No nosso projeto, a sessão Spark é criada por uma camada própria sobre a BBMagic.

## 9.1 Papel da sessão Spark

A sessão Spark conecta o notebook ao cluster.

Ela possui:

* nome de sessão;
* usuário/keytab;
* cluster;
* variáveis de ambiente;
* jars;
* virtualenv;
* configurações Spark;
* driver;
* executores.

## 9.2 Driver e executores

O driver coordena a execução. Os executores processam os dados.

Evite trazer dados grandes para o driver. Isso acontece quando o fluxo coleta dados distribuídos para o ambiente local ou tenta converter grandes volumes para pandas.

## 9.3 `spark_conf`

`spark_conf` é a configuração da sessão Spark.

Ele pode conter parâmetros de:

* timezone;
* Hive;
* shuffle;
* alocação dinâmica;
* Parquet;
* compatibilidade de datas;
* timeout;
* comportamento de escrita.

`spark_conf` deve ser extensível, mas controlado. Não deve virar uma lista de ajustes aleatórios.

## 9.4 Virtualenv Spark

Dependências Python usadas pelo Spark precisam estar disponíveis para a sessão Spark.

Instalar biblioteca no notebook não garante que ela estará disponível nos executores.

Por isso, o projeto pode usar um virtualenv empacotado e armazenado no HDFS, normalmente associado à área `.bbmagic/envs` da keytab ou usuário.

## 9.5 Jars

Jars são usados para drivers e integrações, como acesso a bancos.

Eles precisam estar acessíveis ao cluster, não apenas ao container local.

## 9.6 Regra sobre recurso

Não aumente memória, executores ou cores sem diagnóstico.

Antes, verifique:

* volume lido;
* filtros aplicados;
* joins;
* reparticionamento;
* `collect`;
* conversão para pandas;
* contagens repetidas;
* plano de execução;
* shuffle;
* dados enviesados;
* escrita final.

Problema de Spark deve ser tratado primeiro como problema de lógica ou volume. Ajuste de recurso vem depois.

---

# 10. DB2

DB2 é uma fonte corporativa acessada pelo projeto.

O acesso pode acontecer de duas formas:

1. **Localmente**, pelo container, usando BBMagic.
2. **Distribuído**, pela sessão Spark, quando o volume e o fluxo exigirem processamento no cluster.

## 10.1 Uso local

Use acesso local para:

* consultas pequenas;
* validações;
* amostras;
* metadados;
* inspeção de schemas e tabelas.

Consultas locais devem evitar trazer grandes volumes para o container.

## 10.2 Uso via Spark

Use Spark quando:

* o volume for grande;
* o resultado será cruzado com dados no HDFS/Hive;
* o processamento precisa ser distribuído;
* a consulta faz parte do pipeline.

## 10.3 Credenciais

Credenciais DB2 devem vir de variáveis de ambiente ou mecanismo autorizado.

Não registrar usuário e senha no código, notebook ou documentação.

---

# 11. Hue

Hue é a interface gráfica usada para explorar e consultar recursos do ambiente Big Data.

No nosso contexto, ele serve para apoio e validação.

Use Hue para:

* conferir paths HDFS;
* consultar Hive;
* consultar Impala, quando aplicável;
* validar existência de tabela;
* inspecionar dados;
* apoiar diagnóstico de permissão ou localização.

Não use Hue como substituto do pipeline do projeto.

## 11.1 CDP Modelagem

CDP Modelagem é o cluster voltado a áreas de trabalho de usuários e sandboxes.

## 11.2 CDP Escoragem

CDP Escoragem é o cluster voltado a áreas corporativas.

A escolha do cluster deve respeitar o ambiente e o tipo de dado acessado.

---

# 12. Camada própria do projeto

Nosso projeto possui uma camada própria para padronizar a criação do ambiente e da sessão Spark.

Essa camada existe para não espalhar lógica de ambiente, sessão, paths e dependências pelos notebooks.

## 12.1 Responsabilidades

A camada própria deve cuidar de:

* carregar variáveis de ambiente;
* diferenciar Modelagem e Produção;
* carregar `.env` apenas em Modelagem;
* definir a data de referência;
* definir o nome da sessão Spark;
* identificar sandbox;
* localizar requirements;
* decidir se recria ou reaproveita virtualenv Spark;
* limpar sessão Spark anterior quando apropriado;
* montar `spark_conf`;
* informar jars necessários;
* criar sessão Spark via BBMagic;
* aplicar retry controlado;
* disponibilizar clientes de acesso.

## 12.2 SparkSessionManager

A camada de sessão Spark deve ser o ponto central para criar a sessão.

Ela não deve ser apenas um atalho. Ela representa a regra oficial de conexão do projeto.

Deve concentrar:

* usuário/keytab;
* cluster;
* nome de sessão;
* env enviado para o Spark;
* virtualenv;
* jars;
* `spark_conf`;
* política de retry;
* limpeza de sessão anterior.

## 12.3 Clientes de acesso

Depois que a sessão Spark existe, os clientes de acesso organizam o uso das fontes.

Clientes esperados:

* cliente Hive;
* cliente DB2;
* cliente Oracle, se usado no fluxo;
* utilitário de montagem de queries;
* cliente central para agrupar esses acessos.

Esses clientes não devem esconder decisões críticas. Ambiente, path, schema, tabela e fonte precisam continuar claros.

---

# 13. Fluxo padrão do nosso ambiente

## 13.1 Em Modelagem

Fluxo esperado:

1. abrir o projeto no JupyterLab;
2. carregar variáveis locais controladas;
3. identificar `AMBIENTE = MODELAGEM`;
4. definir data local de trabalho;
5. definir sandbox;
6. validar paths em `/dados/transientes`;
7. preparar ou reaproveitar virtualenv Spark;
8. criar sessão Spark;
9. validar acesso a HDFS, Hive e DB2;
10. executar testes em volume controlado;
11. ajustar lógica antes de pensar em recurso.

## 13.2 Em Produção

Fluxo esperado:

1. usar variáveis oficiais do ambiente;
2. usar `CTMODATE`;
3. usar keytab/usuário técnico;
4. usar VDPs cadastradas;
5. usar paths em `/dados/corporativos`;
6. criar sessão Spark sem depender de `.env` local;
7. executar pipeline sem intervenção manual;
8. registrar logs e falhas;
9. não depender de path pessoal ou arquivo local.

---

# 14. Regras obrigatórias

## 14.1 Caminhos

* Use path de Modelagem somente em Modelagem.
* Use path de Produção somente em Produção.
* Não use `/user/{usuario}` como destino oficial.
* Não use `/tmp` como destino definitivo.
* Não crie tabela Hive apontando para path pessoal.

## 14.2 Variáveis

* Não sobrescreva variáveis padrão do sistema.
* Não versione `.env` real.
* Use `VDP_` para valores que mudam por ambiente.
* Use `CTMODATE` em Produção.
* Não coloque senha no notebook.

## 14.3 Spark

* Não traga volume grande para o driver.
* Não use pandas para volume distribuído grande.
* Não aumente recurso sem diagnóstico.
* Não esconda configuração crítica dentro de função obscura.
* Não mantenha sessão antiga consumindo recurso.

## 14.4 Hive

* Valide database, tabela e path físico.
* Valide schema antes de gravar.
* Valide risco de sobrescrita.
* Não misture sandbox com produção.

## 14.5 DB2

* Use consulta local apenas para volume controlado.
* Use Spark quando o volume exigir processamento distribuído.
* Não exponha credenciais.

---

# 15. Diagnóstico rápido

## 15.1 Erro de path

Verifique:

* ambiente;
* cluster;
* path completo;
* permissão;
* existência do diretório;
* se o path é de Modelagem ou Produção.

## 15.2 Erro de variável

Verifique:

* nome exato da variável;
* se ela existe no ambiente atual;
* se deveria vir de `.env` ou VDP;
* se está disponível em Modelagem ou apenas em Produção.

## 15.3 Erro de Spark

Verifique:

* sessão antiga;
* keytab/usuário;
* cluster;
* virtualenv;
* jars;
* `spark_conf`;
* Livy;
* logs de criação da sessão.

## 15.4 Erro de memória Spark

Verifique antes de aumentar recurso:

* `collect`;
* conversão para pandas;
* volume lido;
* filtros;
* joins;
* shuffle;
* particionamento;
* cache;
* escrita;
* plano de execução.

## 15.5 Erro de DB2

Verifique:

* variáveis DB2;
* usuário impessoal ou técnico;
* schema;
* tabela;
* volume da consulta;
* driver/jar quando for via Spark.

---

# 16. Resumo final

Nosso ambiente deve ser entendido assim:

* **JupyterLab/container**: desenvolvimento e orquestração.
* **Variáveis de ambiente**: separação entre Modelagem e Produção.
* **BBMagic**: conexão com HDFS, Spark e DB2.
* **HDFS**: armazenamento distribuído.
* **Hive**: metadados e tabelas sobre HDFS.
* **Spark**: processamento distribuído.
* **DB2**: fonte corporativa.
* **Hue**: inspeção e validação visual.
* **Camada própria do projeto**: padronização da sessão Spark e dos acessos.

A regra principal é:

> O projeto deve funcionar por ambiente, por variável e por path oficial — nunca por improviso, usuário pessoal ou configuração manual escondida.
