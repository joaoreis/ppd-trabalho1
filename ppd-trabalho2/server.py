from multiprocessing import Manager
from xmlrpc.server import SimpleXMLRPCServer

class Server(SimpleXMLRPCServer):

    hashtable = {} #Manager().dict()

    def get(self, key):
        return self.hashtable[key]

    def put(self, key:str, value:int):
        self.hashtable[key] = value

    def print(self):
        print (self.hashtable)


def main():
    myServer = Server(("localhost", 8000))
    print("Listening on port 8000")
    myServer.register_function(myServer.put, "put")
    myServer.register_function(myServer.get, "get")
    myServer.register_function(myServer.print, "print")
    myServer.serve_forever()

if __name__ == "__main__":
    main()