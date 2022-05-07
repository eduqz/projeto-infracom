import socket
import threading
from utils import get_time


class Client:
    def __init__(self,ip='127.0.0.1',port=699):
        self.ip=ip
        self.port=port
        self.sock=socket.socket(type=socket.SOCK_DGRAM)
        self.event=threading.Event()

    def start(self):
        print("Client ligado!")
        while True:
            message = input(get_time() + ' cliente: ')
            
            cmd = message[:16]
            if cmd == 'chefia':
                self.send(message)
                threading.Thread(target=self.__recv).start()
                break
    
    def stop(self):
        self.event.set()
        self.sock.close()
    
    def __recv(self):
        while not self.event.is_set():
            data=self.sock.recv(1024)
            print(data.decode())
            if data == b'bye':
                print('--- saiu ---')

    def send(self,cmd):
        cmd=cmd.encode()
        self.sock.sendto(cmd,(self.ip,self.port))

client = Client()
client.start()
while True:
    cmd=input()
    client.send(cmd)

    if cmd =='bye':
        break