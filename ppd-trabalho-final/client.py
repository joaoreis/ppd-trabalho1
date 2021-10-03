import paho.mqtt.client as mqtt
import json, sys, os
from random import randrange
import time

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

    # Boot OK e Leave Complete
    if (topic == 'ppd/boot_ok' or topic == 'ppd/leave_complete'):
        canPublish = True

    # Add e Publish Leave
    elif (topic == 'ppd/add' or topic == 'ppd/publish_leave'):
        canPublish = False

try:
    clientId = randrange(0, 2**32)
    mqttBroker = "127.0.0.1" 

    client = mqtt.Client(str(clientId))
    client.connect(mqttBroker) 

    client.loop_start()

    client.subscribe("ppd/boot_ok")
    client.subscribe("ppd/put_ok")
    client.subscribe("ppd/get_ok")
    client.subscribe("ppd/add")
    client.subscribe("ppd/publish_leave")
    client.subscribe("ppd/leave_complete")
    client.on_message = on_message 

    while True:
        if (canPublish):
            key = randrange(0, 2**32)
            client.publish("ppd/put", json.dumps({'key': key, 'value': 'VALOR'}))
            time.sleep(5)
            client.publish("ppd/get", key)
            time.sleep(5)

    client.loop_stop()
except KeyboardInterrupt:
    print('Interrupted')
    try:
        sys.exit(0)
    except SystemExit:
        os._exit(0)