import random

class Client:
    server = None
    id = 0
    quantity = 0
    keys = []
    
    def __init__(self, server, id, quantity) -> None:
        self.server = server
        self.id = id
        self.quantity = quantity

    def generate(self):
        for i in range(self.quantity):
            key = '{0}{1}-{2}'.format("c", str(self.id), str(i))
            self.keys.append(key)
            value = random.randint(0, 10* self.quantity)
            self.server.put(key, value)

    def retrieve(self):
        for key in self.keys:
            value = self.server.get(key)
