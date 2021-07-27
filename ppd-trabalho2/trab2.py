
from contextlib import contextmanager
from multiprocessing import Pool, Process
import sys
from server import Server
from client import Client
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
    print(client.timeElapsed)

###############################################################################
def parallel_generate_retrieve(process_count, size, server: Server):

    procs = []

    for i in range(process_count):
        p = Process(target=execute, args=(process_count, i, size, server))
        print("Starting for process %d" %i)
        p.start()
        procs.append(p)

    for p in procs:
        p.join()


###############################################################################
def main():
    #size = 1_000_000
    size = 8
    process_count = get_total_processes()
    
    server = ServerProxy("http://localhost:8000/")
    
    parallel_generate_retrieve(process_count, size, server)
    server.print()


if __name__ == "__main__":
    main()