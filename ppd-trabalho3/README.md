# Trabalho T1.3 - Uso de Middleware Publish/Subscribe e Filas de Mensagens

###### João Ubaldo, Renan Evangelista e Úrsula Abreu

## Estrutura

O arquivo dhtNode.py implementa a classe `DhtNode` e é responsável por fazer a criação do node e executar todos os publish/subscribes necessários.

O arquivo dht.py é o arquivo que gera a DHT de 8 nós e utiliza a classe `DhtNode`.

O arquivo client.py faz o papel do node que publica put e get e escuta put_ok e get_ok da DHT.

## Executando o trabalho

### Requerimentos

- python3
- mqtt

Para a criação da DHT com os 8 nós, utilize o comando: 

```
python3 dht.py
```

Após os 8 nós serem criadas e publicarem a mensagem de join, a DHT publica uma mensagem de boot_ok.
Após essa mensagem, podemos executar o arquivo client.py, ele é responsável por gerar chaves aleatórias e publicar put e get com essas chaves geradas.

```
python3 client.py
```