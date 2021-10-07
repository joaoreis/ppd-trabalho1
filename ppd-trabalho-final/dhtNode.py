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

        # Conexão com o Broker
        mqttBroker = "127.0.0.1" 

        self.client = mqtt.Client(str(self.id))
        self.client.connect(mqttBroker) 

        # Nó se inscreve para escutar as mensagens de Join enviadas pelos nós
        self.client.subscribe("ppd/join")

        # Nó se inscreve para escutar as mensagens de Put enviadas pelo client
        self.client.subscribe("ppd/put")

        # Nó se inscreve para escutar as mensagens de Get enviadas pelo client.py
        self.client.subscribe("ppd/get")

        # Nó se inscreve para escutar as mensagens de Boot Ok enviadas pela DHT
        self.client.subscribe("ppd/boot_ok")

        # Nó se inscreve para escutar as mensagens de Publish Leave enviadas pelo dhtController
        self.client.subscribe("ppd/publish_leave")

        # Nó se inscreve para escutar as mensagens de Leave enviadas pelos nós
        self.client.subscribe("ppd/leave")

        # Nó se inscreve para escutar as mensagens de Leave Complete enviadas pela DHT
        self.client.subscribe("ppd/leave_complete")
        self.client.on_message = self.on_message 

        # Nó publica join no Broker informando seu NodeId
        self.client.publish("ppd/join", self.id)
        print(f"NodeId: {self.id} fez Join")

        self.client.loop_start()
        time.sleep(30000)

    # Função de callback para lidar com as mensagens recebidas
    def on_message(self, client, userdata, message):
        topic = message.topic

        # Join
        if (topic == 'ppd/join'):
            payload = int(message.payload.decode("utf-8"))
            if (payload == self.id): return

        # Ao receber uma mensagem de Publish Leave, signifca que no dhtController foi indicado que queremos remover um NodeId
        # Se o id enviado for o id do nó, ele publica a mensagem de Leave
        if (topic == 'ppd/publish_leave'):
            payload = int(message.payload.decode("utf-8"))
            if (payload == self.id): 
                self.client.publish("ppd/leave", self.id)
                
        # Ao receber uma mensagem de Leave, se não for o nó que enviou, o nó envia uma mensagem de Leave Ok, indicando que recebeu o leave
        if (topic == 'ppd/leave'):     
            payload = int(message.payload.decode("utf-8"))
            if (payload != self.id): 
                self.client.publish("ppd/leave_ok", self.id)
                
        # Ao receber uma mensagem de Put, o nó verifica se a chave está dentro do endereço de responsabilidade do nó, se tiver, adiciona a chave e valor enviadas
        # e publica uma mensagem de Put Ok indicando ao client que a adição ocorreu
        elif (topic == 'ppd/put'):
            payload = json.loads(message.payload.decode("utf-8"))

            if ((len(self.nodes) == 1) or (int(payload['key']) <= self.id and int(payload['key']) > self.prev)):
                self.data[int(payload['key'])] = payload['value']
                self.client.publish("ppd/put_ok", payload['key'])

                print("NodeId:", self.id, "- Executou um put com chave", payload['key'], "e valor:", payload['value'])
        
        # Ao receber uma mensagem de Get, o nó verifica se a chave está dentro do endereço de responsabilidade do nó, se tiver, o nó publica
        # uma mensagem de Get Ok informando o valor para a chave
        elif (topic == 'ppd/get'):
            payload = int(message.payload.decode("utf-8"))

            if ((len(self.nodes) == 1) or (int(payload) <= self.id and int(payload) > self.prev)):
                value = self.data[payload] if payload in self.data else None
                self.client.publish("ppd/get_ok", json.dumps({'key': payload, 'value': value}))

                print("NodeId:", self.id, "- Executou um get com chave", payload)

        # Ao receber uma mensagem de Boot Ok, o nó armazena todos os NodeIds da DHT e calcula seu antecessor e sucessor 
        elif (topic == 'ppd/boot_ok'):
            payload = list(map(int, message.payload.decode("utf-8").split()))
            self.nodes = payload
            self.order_nodes()

        # Ao receber uma mensagem de Leave Complete, o nó armazena todos os NodeIds da DHT e calcula seu antecessor e sucessor 
        elif (topic == 'ppd/leave_complete'):
            payload = list(map(int, message.payload.decode("utf-8").split()))

            # A DHT envia os NodeIds já sem o NodeId que publicou a mensagem de Leave
            if (self.id in payload): 
                self.nodes = payload
                self.order_nodes()
            else:
                # Se o id não for encontrado, quer dizer que é o nó que publicou a mensagem de leave e ele para de escutar as mensagens do broker
                self.client.loop_stop()

    # Função que ordena os nodes e define seu sucessor e antecessor 
    def order_nodes(self):
        self.nodes.sort()
        nodeId = self.nodes.index(self.id)
        self.prev = self.nodes[nodeId - 1] if nodeId > 0 else self.nodes[-1]
        self.next = self.nodes[nodeId + 1] if nodeId < len(self.nodes)-1 else self.nodes[0]

if __name__ == '__main__':
    node = DhtNode()
    node.join()