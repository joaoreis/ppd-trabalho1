#trab3.py

import random

###############################################################################
def startNode(addressSpace):
        node = DhtNode(addressSpace)
        return node.nodeId

###############################################################################
def main():
    n_bytes = 32
    addressSpace = 2**n_bytes
    nodes = 8
   
    ids = []
    for n in range(nodes):
        id = startNode(addressSpace)
        ids.append(id)
    ids.sort()
    print(ids)
    # Iniciar a rede dos nós
    # Iniciar outro processo que fica publicando valores para o broker (msg put), e tambem msgs de get ( ou outro proceso)
        # sub msgs de confirmacao de put
        # pub msg get
        # sub mgs de confirmacao de get 
    
class DhtNode: # É pra ser um Processo
    nodeId = 0
    
    def __init__(self, addressSpace) -> None:
        self.nodeId =  random.randint(0, addressSpace)
        # sortear um numero de 32b e atribuir ao seu id e PID
        # publicar no broker o seu node ID (msg Join)
        # subscribe as mensagens de join ( espera receber 7 joins, msg confirmacao boot?)
    # saber quem é o seu sucessor
    # saber quem é o seu antecessor
    # Armazena em uma hashtable valores dentro da sua faixa
    # Retorna valores dentro da sua faixa (msg get, sub)
    # pub mensagens de confirmacao de put 
    # pub msg de confirmacao de get



        


if __name__ == "__main__":
    main()