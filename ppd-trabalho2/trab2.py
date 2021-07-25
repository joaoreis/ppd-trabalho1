
from contextlib import contextmanager
from multiprocessing import Manager, Pool, Process
from random import seed
import random
from time import time
import sys

class Server:
    dict = {}

    def get(self, key):
        return self.dict[key]

    def put(self, key, value):
        self.dict[key] = value

###############################################################################
class Client:
    id = 0
    server = None
    quantity = 0
    keys = []
    timeElapsed = 0
    
    def __init__(self, id, quantity, server) -> None:
        self.id = id
        self.quantity = quantity
        self.server = server

    def generate(self):
        start = time()
        
        for i in range(self.quantity):
            key = '{0}{1}-{2}'.format("c", str(self.id), str(i))
            self.keys.append(key)
            value = random.randint(0, 10* self.quantity)
            self.server.put(key,value)
        
        print(self.server.dict)
        self.timeElapsed = time() - start

    def retrieve(self):
        start = time()
        for key in self.keys:
            value = self.server.get(key)
        self.timeElapsed += (time() - start)
        #print(self.timeElapsed)

###############################################################################
@contextmanager
def process_pool(size):
    # Cria um pool de processos e bloqueia ate que todos os processos sejam concluidos
    pool = Pool(size)
    yield pool
    pool.close()
    pool.join()

###############################################################################
def get_total_processes():
    # Verifica se foi passado o numero de processos
    # Se nao passar o numero de processos, consideramos 1 processo
    total_processes = int(sys.argv[1]) if (len(sys.argv) > 1) else 1

    print('Usando {} processos'.format(total_processes))

    return total_processes

###############################################################################
def execute(process_count, id, size, server):
    quantity = int(size/process_count)
    client = Client(id, quantity, server)
    client.generate()
    client.retrieve()
    
###############################################################################
def parallel_generate_retrieve(process_count, size, server):

    procs = []

    # with process_pool(process_count) as pool:
    #     pool.apply_async(execute, (process_count, size, server, results))
    # return results
    for i in range(process_count):
        p = Process(target=execute, args=(process_count, i, size, server))
        p.start()
        print("Starting for process %d" %i)
        procs.append(p)

    for p in procs:
        p.join()


###############################################################################
def main():
    size = 12 #1_000_000
    process_count = get_total_processes()
    
    server = Server()
    
    parallel_generate_retrieve(process_count, size, server)
    print (server.dict)
    

if __name__ == "__main__":
    main()