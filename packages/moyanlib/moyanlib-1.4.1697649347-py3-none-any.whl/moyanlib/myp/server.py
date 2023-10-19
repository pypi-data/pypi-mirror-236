import socketserver as ss
from moyanlib import myp

class Server(ss.BaseRequestHandler):
    @classmethod
    def route(cls,pattern):
        def decorator(func):
            cls.routes[pattern] = func
            return func
        return decorator

    def run(self,hosts:str="0.0.0.0",port:int=8000):
        server = ss.TCPServer((hosts,port),self)
        server.serve_forever()

    def __init__(self):
        self.routes = {}

    def handle(self):
        while True:
            data = self.request.recv(1024)
            if not data:
                break
            request = myp.loadClientData(data)
            func = self.routes.get(request["path"], None)
            if func:
                retData = func(request)
                self.request.sendall(myp.dumpServerData(retData["header"], retData["data"].encode("utf-8"), retData["code"]))
            else:
                self.request.sendall(myp.dumpServerData(data=b"404",code=4))

    def finish(self):
        self.request.close


if __name__ == "__main__":
    HOST, PORT = "localhost", 9999
    with ss.TCPServer((HOST, PORT), Server) as server:
        server.serve_forever()