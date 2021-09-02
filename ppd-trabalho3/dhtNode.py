import paho.mqtt.client as mqtt
from random import randrange
import json
import time

class DhtNode:
    def __init__(self):
        self.id = randrange(0, 2**32)
        self.nodes = [self.id]
        self.prev = -1
        self.next = -1
        self.data = {}
        self.client = None

    # Join do node
    def join(self):

        # Inicia conexão Broker
        mqttBroker = "127.0.0.1" 

        self.client = mqtt.Client(str(self.id))
        self.client.connect(mqttBroker) 

        # Faz subscribe 
        self.client.subscribe("ppd/join")
        self.client.subscribe("ppd/put")
        self.client.subscribe("ppd/get")
        self.client.subscribe("ppd/boot_ok")
        self.client.on_message = self.on_message 

        # Publica join no Broker
        self.client.publish("ppd/join", self.id)
        print(f"{self.id} - Fez join")

        self.client.loop_start()
        time.sleep(30000)


    # Callback para lidar com o que receber do subscribe
    def on_message(self, client, userdata, message):
        topic = message.topic

        # Join
        if (topic == 'ppd/join'):
            payload = int(message.payload.decode("utf-8"))
            if (payload == self.id): return

        # Put
        elif (topic == 'ppd/put'):
            payload = json.loads(message.payload.decode("utf-8"))
                
            if (int(payload['key']) <= self.id and int(payload['key']) > self.prev):
                self.data[int(payload['key'])] = payload['value']
                self.client.publish("ppd/put_ok", payload['key'])

                print(f"{self.id} - Executou um put com chave {payload['key']} e valor {payload['value']}")
        
        # Get
        elif (topic == 'ppd/get'):
            payload = int(message.payload.decode("utf-8"))

            if (int(payload) <= self.id and int(payload) > self.prev):
                value = self.data[payload] if payload in self.data else None
                self.client.publish("ppd/get_ok", json.dumps({'key': payload, 'value': value}))

                print(f"{self.id} - Executou um get com chave {payload}")

        # Boot OK
        elif (topic == 'ppd/boot_ok'):
            payload = list(map(int, message.payload.decode("utf-8").split()))
            self.nodes = payload
            self.order_nodes()

    # Ordena os nodes
    def order_nodes(self):
        self.nodes.sort()
        nodeId = self.nodes.index(self.id)
        self.prev = self.nodes[nodeId - 1] if nodeId > 0 else self.nodes[-1]
        self.next = self.nodes[nodeId + 1] if nodeId < len(self.nodes)-1 else self.nodes[0]

if __name__ == '__main__':
    node = DhtNode()
    node.join()