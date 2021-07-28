# Trabalho T1.2 - Uso de Middleware RPC/RMI

###### João Ubaldo, Renan Evangelista e Úrsula Abreu

## Executando o trabalho

### Requerimentos

- python3

Para execução do projeto, basta executar os comandos: 

```
python3 server.py
python3 trab2.py {numProcessos}
```


Onde ``numProcessos`` é o número de processos, caso não seja definido, o projeto considera a execução com 1 processo.

## Resultados

Consideramos uma tabela hash de inteiros com tamanho 1000000, o tempo requerido para inserção e recuperação dos valores na tabela hash com 2, 4 e 8 instâncias cliente é:

|Processos|Tempo|
|---|---|
|2 processos|746.500257|
|4 processos|548.837419|
|8 processos|546.565700|

## Pergunta

É necessário implementar algum controle de concorrência no acesso aos métodos e à tabela hash por parte dos diferentes clientes?

Sim, achamos que é necessário principalmente por causa do método put(). A implementação foi desenvolvida para gerar chaves únicas, o que permite não existir conflitos entre as chaves, mas ainda há concorrência entre os recursos do server. Um cliente pode conseguir inserir mais chaves que outros e o controle de concorrência também pode ajudar nisso. 

Analisando os resultado obtidos, temos a hipótese de um dos motivos para a diferença de tempo de execução não ser tão grande entre 4 e 8 processos é que não existe esse controle de concorrência.
