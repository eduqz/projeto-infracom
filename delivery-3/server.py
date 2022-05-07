
import json
import socket
import threading
from utils import get_time


class Server:
    def __init__(self,ip='127.0.0.1',port=699):
        self.ip=ip
        self.port=port
        self.sock=socket.socket(type=socket.SOCK_DGRAM)
        self.sock.bind((self.ip,self.port))
        self.client=set()
        self.event=threading.Event()
        self.dic={}
        self.history=[]

    def start(self):
        print('Server Ligado!')
        threading.Thread(target=self.__recv,daemon=True).start()

    def stop(self):
        self.event.set()
        self.sock.close()

    def get_str(self,t):
        if t < 10:
            return '0' + str(t)
        
        return str(t)
    
    def __recv(self):
        while not self.event.is_set():
            data,ipinfo=self.sock.recvfrom(1024)
            self.client.add(ipinfo)
            
            ip,port = ipinfo
            info = str(ip) + ':' + str(port)

            message = get_time() + ' CINtofome: '
            
            cmd = data[:16]
            if cmd == b'chefia':
                message = data = message + 'Digite sua mesa'
                self.history.append('mesa')
                self.send(message.encode())
            
            elif self.history[-1] == 'mesa':
                self.dic['mesa'] = data.decode()
                print(data.decode())
                message = data = message + 'Digite seu nome'
                self.history.append('nome')
                self.send(message.encode())
            
            elif self.history[-1] == 'nome':
                self.dic['nome'] = data.decode()
                print(data.decode())
                message = data = message + 'Digite uma das opções a seguir (o número ou por extenso)\n1 - cardapio\n2 - pedido\n3 - conta individual\n4 - não fecho com robô, chame seu gerente\n5 - nada não, tava só testando\n6 - conta da mesa'
                self.history.append('opcoes')
                self.send(message.encode())
            
            elif self.history[-1] == 'opcoes' and cmd == b'1':
                message = data = message + '(apresenta o cardápio)'
                self.history.append('cardapio')
                self.send(message.encode())
            
            elif cmd==b'sair':
                message = data = message + self.dic['nome'] + 'saiu'
                self.send(message.encode())
                self.client.remove(ipinfo)
                self.dic.pop(info)
        

    def send(self,data):
        for client in self.client:
            self.sock.sendto(data,client)

server = Server()
server.start()

while True:
    cmd=input()
    cmd = cmd.encode()
    server.send(cmd)
    
    if cmd =='bye':
        break