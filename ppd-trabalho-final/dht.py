import paho.mqtt.client as mqtt
from dhtNode import DhtNode
from multiprocessing import Process
import time
from random import randrange

# Variável que armazena os processos
processos = []
# Variável que armazena os NodeIds atuais da DHT
nodeIds = []
# Variável que armazena a quantidade de nós atuais da DHT. A DHT é iniciada com um nó, por isso a variável é iniciada com valor 1
amount = 1

def run_node():
    node = DhtNode()
    node.join()

def join_process():
    for p in processos:
        p.join()

# Função que cria um novo processo para o novo nó 
def add_node():
    p = Process(target=run_node)
    processos.append(p)
    p.start()
    
# Função que verifica se ao criar a DHT com um nó ou se adicionar um nó, todos os nós receberam o Join
def boot_ok():
    if(len(nodeIds) == amount):
        print("Boot OK! NodeIds:", nodeIds)
        client.publish("ppd/boot_ok", " ".join(str(x) for x in nodeIds))

# Função de callback para lidar com as mensagens recebidas
def on_message(client, userdata, message):
    topic = message.topic
    global amount
    global nodeIds

    # Ao receber uma mensagem de Join, adiciona o novo NodeId e verifica se já recebeu de todos os nós
    if (topic == 'ppd/join'):
        nodeId = int(message.payload.decode("utf-8"))
        nodeIds.append(nodeId)
        boot_ok()

    # Ao receber uma mensagem de Add, aumenta a quantidade de nós da DHT e chama a função que realmente cria um novo nó
    elif (topic == 'ppd/add'):
        amount += 1
        print("Adicionando um novo nó na DHT...")
        add_node()
    
    # Ao receber uma mensagem de Publish Leave, diminui a quantidade de nós da DHT e reseta a variável de nodeIds para ser
    # populada apenas depois da mensagem de Leave Ok da cada nó 
    elif (topic == 'ppd/publish_leave'):
        amount -= 1
        nodeIds = []
        payload = int(message.payload.decode("utf-8"))
        print("Deletando NodeID:", payload, "da DHT...")

    # Ao receber uma mensagem de Leave Ok, adiciona o NodeId e verifica se já recebeu de todos os nós
    # (similar ao funcionamento do Join, mas para o Leave de um nó)
    elif (topic == 'ppd/leave_ok'):
        nodeId = int(message.payload.decode("utf-8"))
        nodeIds.append(nodeId)

        # Verifica se todos os nós confirmaram o recebimento do leave
        if(len(nodeIds) == amount):
            print("Nó deletado da DHT! Novos NodeIds:", nodeIds)

            # Publica a mensagem de Leave Complete, realmente fazendo a remoção do nó da DHT
            client.publish("ppd/leave_complete", " ".join(str(x) for x in nodeIds))

# Função main que inicia a DHT com apenas um nó
def main():
    add_node()

if __name__ == '__main__':
    clientId = randrange(0, 2**32)
    mqttBroker = "127.0.0.1" 

    # Conexão com o Broker
    client = mqtt.Client(str(clientId))
    client.connect(mqttBroker) 

    client.loop_start()

    # A DHT se inscreve para escutar as mensagens de Join enviadas pelos nós
    client.subscribe("ppd/join")

    # A DHT se inscreve para escutar as mensagens de Add enviadas pelo dhtController, para saber quando adicionar um novo nó
    client.subscribe("ppd/add")

    # A DHT se inscreve para escutar as mensagens de Publish Leave enviadas pelo dhtController, para saber quando o processo de remover um nó começou
    client.subscribe("ppd/publish_leave")

    # A DHT se inscreve para escutar as mensagens de Leave Ok enviadas pelos nós, após receberem uma mensagem de leave de um dos nós
    client.subscribe("ppd/leave_ok")
    client.on_message = on_message 

    main()
    join_process()