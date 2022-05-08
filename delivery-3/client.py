import socket
import threading
from utils import Timer


# Client class
class Client:
    # Constructor method, that initialize the attributes
    def __init__(self, ip='127.0.0.1', port=5001):
        self.ip = ip
        self.port = port
        self.sock = socket.socket(type=socket.SOCK_DGRAM)
        self.event = threading.Event()

    # Method that starts the client, by reading the message and senting it in a thread
    def start(self):
        print("Cliente iniciado")

        while True:
            message = input(Timer.get_current_time() + ' cliente: ')

            inputted_message = message[:16]
            if inputted_message == 'chefia':
                self.send(message)
                threading.Thread(target=self._recv).start()
                break

    # Method that stops the client
    def stop(self):
        self.event.set()
        self.sock.close()

    # Method that show the message returned by the server
    def _recv(self):
        while not self.event.is_set():
            data = self.sock.recv(1024)
            print(data.decode())

            if data == b'sair':
                print('*** Client finalizado ***')

    # Method used to send the message to the server
    def send(self, message):
        message = message.encode()
        self.sock.sendto(message, (self.ip, self.port))


# Creating a Client instance and using it
client = Client()
client.start()

while True:
    recv_message = input()
    client.send(recv_message)
    

    if recv_message == 'sair':
        break
