from socket import *
from utils import *
import random


# Function that intercepts all requests to corrupt and delay packets, to test the RDT algorithm
def intercept(pkt, sock, addr):
    rand = random.randint(1, 10)
    if rand >= 1 and rand <= 2:
        print("Pacote perdido")
        return
    if rand >= 3 and rand <= 4:
        pkt = corrupt(pkt)
        print("Pacote corrompido. Resultado: %s" % str(pkt))
    rand_sleep()
    sock.sendto(pkt, addr)



# Set the sender and receiver addresses
from_send_addr = ('localhost', 1600)
to_recv_addr = ('localhost', 1601)
from_recv_addr = ('localhost', 1602)
to_send_addr = ('localhost', 1603)


# Create the sockets
send_sock = socket(AF_INET, SOCK_DGRAM)
send_sock.bind(from_send_addr)
send_sock.setblocking(0)
recv_sock = socket(AF_INET, SOCK_DGRAM)
recv_sock.bind(from_recv_addr)
recv_sock.setblocking(0)

out_sock = socket(AF_INET, SOCK_DGRAM)


# Interceptor starting
print("Interceptor iniciado")
while True:
    # Execute the interceptor to sender actions
    try:
        pkt = str(send_sock.recv(BUFSIZE))
        print("Pacote recebido do sender: %s" % pkt)
        intercept(pkt, out_sock, to_recv_addr)
    except error:
        pass
    
    # Execute the interceptor to receiver actions
    try:
        pkt = recv_sock.recv(BUFSIZE)
        print("Pacote recebido do receiver: %s" % pkt)
        intercept(pkt, out_sock, to_send_addr)
    except error:
        pass
