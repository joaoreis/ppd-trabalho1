import paho.mqtt.client as mqtt
from dhtNode import DhtNode
from multiprocessing import Process
import time
from random import randrange

processos = []
nodeIds = []

def run_node():
    node = DhtNode()
    node.join()

def kill_nodes():
    for p in processos:
        p.terminate()

def main():
    for _ in range(8):
        p = Process(target=run_node)
        processos.append(p)
        p.start()
    for p in processos:
        p.join()
        
def on_message(client, userdata, message):
    nodeId = int(message.payload.decode("utf-8"))
    nodeIds.append(nodeId)

    if(len(nodeIds) == 8):
        print("Boot OK - Todos os nós fizeram join")
        client.publish("ppd/boot_ok", " ".join(str(x) for x in nodeIds))

if __name__ == '__main__':
    clientId = randrange(0, 2**32)
    mqttBroker = "127.0.0.1" 

    client = mqtt.Client(str(clientId))
    client.connect(mqttBroker) 

    client.loop_start()

    client.subscribe("ppd/join")
    client.on_message = on_message 

    main()