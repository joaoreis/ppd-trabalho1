
from contextlib import contextmanager
from multiprocessing import Pool, Process
import sys
from server import Server
from client import Client
from time import time
from xmlrpc.client import ServerProxy

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
    client = Client(server, id, quantity)
    client.generate()
    client.retrieve()
    

###############################################################################
def parallel_generate_retrieve(process_count, size, server: Server):

    procs = []

    for i in range(process_count):
        p = Process(target=execute, args=(process_count, i, size, server))
        print("Iniciando processo %d" %i)
        p.start()
        procs.append(p)

    for p in procs:
        p.join()

###############################################################################
def main():
    size = 1_000_000
    process_count = get_total_processes()
    
    server = ServerProxy("http://localhost:8000/")
    
    start = time()
    parallel_generate_retrieve(process_count, size, server)
    print("Time Elapsed: %4.6f" % (time() - start))

if __name__ == "__main__":
    main()