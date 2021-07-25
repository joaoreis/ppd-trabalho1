
from numpy.random.mtrand import randint


class Server:
    dict = {}

    def get(self, key):
        return self.dict[key]

    def put(self, key, value):
        self.dict[key] = value

class Client:
    quantity = 0
    
    def __init__(self, quantity, server) -> None:
        self.quantity = quantity

    def generate(self, server):
        for i in range(self.quantity):
            key = randint(10* self.quantity)
            value = randint(10* self.quantity)
            server.put(key,value)


def main():
    size = 8 #1_000_000
    number_of_clients = 4
    server = Server()
    clients = []

    for i in range(number_of_clients):
        client = Client(int(size/number_of_clients), server)
        clients.append(client)
        client.generate(server)

    print (server.dict)

    

if __name__ == "__main__":
    main()