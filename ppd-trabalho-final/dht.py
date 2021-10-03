import paho.mqtt.client as mqtt
from dhtNode import DhtNode
from multiprocessing import Process
import time
from random import randrange

processos = []
nodeIds = []
amount = 1

def run_node():
    node = DhtNode()
    node.join()

def join_process():
    for p in processos:
        p.join()

def add_node():
    p = Process(target=run_node)
    processos.append(p)
    p.start()

def main():
    add_node()
    
def boot_ok():
    if(len(nodeIds) == amount):
        print("Boot OK! NodeIds:", nodeIds)
        client.publish("ppd/boot_ok", " ".join(str(x) for x in nodeIds))

def on_message(client, userdata, message):
    topic = message.topic
    global amount
    global nodeIds

    if (topic == 'ppd/join'):
        nodeId = int(message.payload.decode("utf-8"))
        nodeIds.append(nodeId)
        boot_ok()

    elif (topic == 'ppd/add'):
        amount += 1
        print("Adicionando um novo nó na DHT...")
        add_node()
    
    elif (topic == 'ppd/publish_leave'):
        amount -= 1
        nodeIds = []
        payload = int(message.payload.decode("utf-8"))
        print("Deletando NodeID:", payload, "da DHT...")

    elif (topic == 'ppd/leave_ok'):
        nodeId = int(message.payload.decode("utf-8"))
        nodeIds.append(nodeId)

        if(len(nodeIds) == amount):
            print("Nó deletado da DHT! Novos NodeIds:", nodeIds)
            client.publish("ppd/leave_complete", " ".join(str(x) for x in nodeIds))

if __name__ == '__main__':
    clientId = randrange(0, 2**32)
    mqttBroker = "127.0.0.1" 

    client = mqtt.Client(str(clientId))
    client.connect(mqttBroker) 

    client.loop_start()

    client.subscribe("ppd/join")
    client.subscribe("ppd/add")
    client.subscribe("ppd/publish_leave")
    client.subscribe("ppd/leave_ok")
    client.on_message = on_message 

    main()
    join_process()