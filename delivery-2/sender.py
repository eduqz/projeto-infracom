from socket import socket, AF_INET, SOCK_DGRAM, timeout
from utils import *


# Set the sender and receiver addresses
dest_addr = 'localhost'
dest_port = 1600
dest = (dest_addr, dest_port)
listen_addr = 'localhost'
listen_port = 1603
listen = (listen_addr, listen_port)

# Get the content from file
with open('content.txt') as f:
    content = f.read()

# Create the sockets
send_sock = socket(AF_INET, SOCK_DGRAM)
recv_sock = socket(AF_INET, SOCK_DGRAM)

recv_sock.bind(listen)
recv_sock.settimeout(1)

# Init variables
offset = 0
seq = 0


# Sender starting
print("Sender iniciado")

# Loop to send the whole content
while offset < len(content):
    # Get the actual segment
    if offset + SEGMENT_SIZE > len(content):
        segment = content[offset:]
    else:
        segment = content[offset:offset + SEGMENT_SIZE]
    offset += SEGMENT_SIZE

    # Wait for the ACK
    ack_received = False
    while not ack_received:
        # Send the segment
        send_sock.sendto(checksum_calculator(segment) + str(seq) + segment, dest)

        # Try to receive the response, if it take much time, log a timeout error; else, get the message and check if ack and checksum are right, if so, proceed to the next segment
        try:
            message, address = recv_sock.recvfrom(BUFSIZE)
        except timeout:
            print("Erro: timeout")
        else:
            print("Mensagem enviada: %s" % str(message))
            checksum = message[:2]
            ack_seq = message[5]

            if checksum_calculator(message[2:]) == checksum and ack_seq == str(seq):
                print("Segmento %s validado" % str(seq))
                ack_received = True

    seq = 1 - seq
