# client é utilizado para publicar mensagens de Put e Get para os nós

import paho.mqtt.client as mqtt
import json, sys, os
from random import randrange
import time

# Variável utilizada para controlar quando começar e parar de publicar
canPublish = False

def on_message(client, userdata, message):
    global canPublish
    topic = message.topic

    # Put OK
    if (topic == 'ppd/put_ok'):
        payload = message.payload.decode("utf-8")
        print("Key:", payload, "armazenada com sucesso!")

    # Get OK
    elif (topic == 'ppd/get_ok'):
        payload = json.loads(message.payload.decode("utf-8"))
        print("Get realizado para key:", payload['key'], "- Valor retornado:", payload['value'])

    # Ao receber uma mensagem de Add ou Publish Leave, o client para de enviar mensagens de Put e Get
    elif (topic == 'ppd/add' or topic == 'ppd/publish_leave'):
        canPublish = False

    # Ao receber uma mensagem de Boot OK ou Leave Complete, o cliente volta a enviar mensagend de Put e Get
    elif (topic == 'ppd/boot_ok' or topic == 'ppd/leave_complete'):
        canPublish = True

try:
    clientId = randrange(0, 2**32)
    mqttBroker = "127.0.0.1" 

    # Conexão com o Broker
    client = mqtt.Client(str(clientId))
    client.connect(mqttBroker) 

    client.loop_start()

    # Client se inscreve para escutar as mensagens de Boot Ok enviadas pela DHT
    client.subscribe("ppd/boot_ok")

    # Client se inscreve para escutar as mensagens de Put Ok enviadas pelos nós
    client.subscribe("ppd/put_ok")

    # Client se inscreve para escutar as mensagens de Get Ok enviadas pelos nós
    client.subscribe("ppd/get_ok")

    # Client se inscreve para escutar as mensagens de Add enviadas pelo dhtController
    client.subscribe("ppd/add")

    # Client se inscreve para escutar as mensagens de Publish Leave enviadas pelo dhtController
    client.subscribe("ppd/publish_leave")

    # Client se inscreve para escutar as mensagens de Leave Complete enviadas pela DHT
    client.subscribe("ppd/leave_complete")
    client.on_message = on_message 

    while True:
        if (canPublish):
            # Gera uma chave aleatória
            key = randrange(0, 2**32)

            # Publica mensagem de Put com chave e valor para os nós processarem
            client.publish("ppd/put", json.dumps({'key': key, 'value': 'VALOR'}))
            time.sleep(5)

            # Publica mensagem de Get com a mesma chave para os nós processarem
            client.publish("ppd/get", key)
            time.sleep(5)

    client.loop_stop()
except KeyboardInterrupt:
    print('Interrupted')
    try:
        sys.exit(0)
    except SystemExit:
        os._exit(0)