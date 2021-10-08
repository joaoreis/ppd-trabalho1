# Trabalho T2 - Uso de Middleware Publish/Subscribe e Filas de Mensagens

###### João Ubaldo, Renan Evangelista e Úrsula Abreu

## Vídeo explicativo

[Explicação da implementação](https://drive.google.com/file/d/1P-fyngdhISarUpBm9ZqPrk1eIYfrjl1i/view?usp=sharing)

## Executando o trabalho

### Requerimentos

- python3
- mqtt

Após iniciar o broker do mqtt, utilize o comando para iniciar o client:
```
python3 client.py
```
O client é quem realiza os puts e gets, após o comando, o terminal aguarda a DHT ficar pronta. 

Para auxiliar a adição e remoção de nós, foi criado um controller ([dhtController](dhtController.py)), para iniciar a controller utilize o comando:
```
python3 dhtController.py
```
Essa controller dá a possibilidade de adicionar um nó aleatório, ou remover  um nó informando seu node ID
e, finalmente, inicia-se a DHT com o comando:
```
python3 dht.py
```
A DHT é iniciada apenas com 1 nó, que é responsável por todo o endereçamento de memória da DHT. No client, que estava aguardando o início da DHT iniciará o envio dos puts e gets.

No controller, solicitando a adição de um nó aleatório (digitando 1 no terminal do controller), será possível observar a adição do nó tanto no terminal da DHT quanto no terminal do broker e, após o boot ok, os nós recalculam seus antecessores e sucessores, independente da quantidades de nós anteriormente na DHT. O client espera todos os joins ocorrerem na DHT antes de voltar a enviar mensagens para não enviar mensagens desnecessárias enquanto a DHT estiver sendo modificada.

Solicitando a remoção de um nó (digitando 2 no terminal do controller e, em seguida, o ID de um nó), após todos os nós da DHT retornarem ok para remoção do nó especificado, será possível observar a remoção no terminal da DHT e os nós com antecessores e sucessores recalculados. O client espera todos os joins ocorreram na DHT antes de voltar a enviar mensagens, similar à adição.
