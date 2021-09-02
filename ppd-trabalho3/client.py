import paho.mqtt.client as mqtt
import json
from random import randrange
import time

def on_message(client, userdata, message):
    topic = message.topic

    # Put OK
    if (topic == 'ppd/put_ok'):
        payload = message.payload.decode("utf-8")
        print(f"Key {payload} armazenada.")

    # Get OK
    elif (topic == 'ppd/get_ok'):
        payload = json.loads(message.payload.decode("utf-8"))
        print(f"Key {payload['key']} = {payload['value']}")


clientId = randrange(0, 2**32)
mqttBroker = "127.0.0.1" 

client = mqtt.Client(str(clientId))
client.connect(mqttBroker) 

client.loop_start()

client.subscribe("ppd/put_ok")
client.subscribe("ppd/get_ok")
client.on_message = on_message 

while True:
    key = randrange(0, 2**32)
    client.publish("ppd/put", json.dumps({'key': key, 'value': 'VALOR'}))
    time.sleep(1)
    client.publish("ppd/get", key)
    time.sleep(1)

client.loop_stop()