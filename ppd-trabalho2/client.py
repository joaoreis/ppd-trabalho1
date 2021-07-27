import random
from time import time

class Client:
    server = None
    id = 0
    quantity = 0
    keys = []
    timeElapsed = 0
    
    def __init__(self, server, id, quantity) -> None:
        self.server = server
        self.id = id
        self.quantity = quantity

    def generate(self):
        start = time()
        
        for i in range(self.quantity):
            key = '{0}{1}-{2}'.format("c", str(self.id), str(i))
            self.keys.append(key)
            value = random.randint(0, 10* self.quantity)
            self.server.put(key, value)
        
        self.timeElapsed = time() - start

    def retrieve(self):
        start = time()
        for key in self.keys:
            value = self.server.get(key)
        self.timeElapsed += (time() - start)
