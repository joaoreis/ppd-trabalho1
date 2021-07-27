class server:
    vetor = {}

    def put(self,k, v):
        self.vetor[k] = v

class cliente:
    server = None

    def __init__(self, server) -> None:
        self.server = server
    
    def bota(self, k , v):
        self.server.put(k,v)

def paralel(server):
     for i in range(0,2):
         c = cliente(server)
         c.bota(i,i)

def main():
    s = server()
    c = cliente(s)
    c1 = cliente(s)
    
    c.bota(1,2)
    c1.bota(3,4)
    print(s.vetor)

def update_x(x):
    x = 2
    print(x)
    return x
def main2():
    x = 5
    print(x)
    x = update_x(x)
    print(x)

if __name__ == "__main__":
    main2()