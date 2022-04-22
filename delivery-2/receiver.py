from socket import socket, AF_INET, SOCK_DGRAM
from sys import stdout
from utils import *


# *** Functions
# Sender method
def send(content, dest):
    checksum = checksum_calculator(content)
    send_sock.sendto(checksum + content, dest)


# *** Main
# Set the sender and receiver addresses
dest_addr = 'localhost'
dest_port = 1602
dest = (dest_addr, dest_port)
listen_addr = 'localhost'
listen_port = 1601
listen = (listen_addr, listen_port)

# Create the sockets
send_sock = socket(AF_INET, SOCK_DGRAM)
recv_sock = socket(AF_INET, SOCK_DGRAM)

recv_sock.bind(listen)

# Define the seq expected
expecting_seq = 0


# Receiver starting
print("Receiver iniciado")

# Start the receiver loop
while True:
    message, address = recv_sock.recvfrom(BUFSIZE)

    # Get the data from message
    checksum = message[:2]
    seq = message[2]
    content = message[3:]

    # Based on the checksum calculated, send the right ACK
    if checksum_calculator(content) == checksum:
        send("ACK" + seq, dest)
        if seq == str(expecting_seq):
            stdout.write(content)
            expecting_seq = 1 - expecting_seq
    else:
        negative_seq = str(1 - expecting_seq)
        send("ACK" + negative_seq, dest)
