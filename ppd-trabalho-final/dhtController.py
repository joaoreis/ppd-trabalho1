# dhtController é utilizado para publicar mensagens de adição e remoção dos nós, possibilitando o teste dos nós dinâmicos na DHT

import paho.mqtt.client as mqtt
import json, sys, os
from random import randrange
import time

try:
    clientId = randrange(0, 2**32)
    mqttBroker = "127.0.0.1" 

    # Conexão com o Broker  
    client = mqtt.Client(str(clientId))
    client.connect(mqttBroker) 

    client.loop_start()
    print("Digite 1 para adicionar um novo nó aleatório ou 2 para remover um nó específico:")

    while True:
        action = input()
        if (action == '1'):
            # Publica uma mensagem de Add para a DHT adicionar um novo nó
            client.publish("ppd/add")
        elif (action == '2'):
            print("Digite o NodeID que deixará a rede:")
            nodeId = input()

            # Publica uma mensagem de Publish Leave indicando o NodeId que deve publicar um Leave
            client.publish("ppd/publish_leave", nodeId)

    client.loop_stop()
except KeyboardInterrupt:
    print('Interrupted')
    try:
        sys.exit(0)
    except SystemExit:
        os._exit(0)