# monopoli%

Programa que eu fiz para baixar todas as monografias de um determinado ano e curso da Escola Politécnica da Ufrj (http://monografias.poli.ufrj.br/) e depois acrescentar num banco de dados Sqlite.

## Pré-requisitos

As duas bibliotecas a seguir foram usadas:

* requests
* textract

para instalar basta os comandos
```
pip install requests
pip install textract
```

### Execução

Para executar basta rodar o comando no diretório do arquivo e mágica acontecerá

```
python main.py
```
#### Tabelas Sql

A arquitetura SQL escolhida foi a de duas tabelas: Uma tabela chamada teses com um id e o título e outra chamada chaves que possui a id referente a de um título da tabela teses e as palavras-chaves na coluna chave. Como no esquema mostrado abaixo:

table teses
+--------+--------------------------+
| id     | título                   |
+--------+--------------------------+
|   1    | ALIMENTADOR DE AN...     |

table chaves
+--------+-------------------------+
| id     | chave                   |
+--------+-------------------------+
|   1    | sistemas embarcados     |
|   1    | alimentação automática  |
