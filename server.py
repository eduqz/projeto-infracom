import socket
import struct
from utils import checksum_calculator


# Define the socket params and create it
server_name = "127.0.0.1"
server_port = 65000

server_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
server_socket.bind((server_name, server_port))
print("UDP server up and listening")


while(True):
    # Receive the message from client
    full_packet, address = server_socket.recvfrom(1024)

    # Split the packet, to get the header and the message
    header = full_packet[:16]
    encoded_message = full_packet[16:]
    header = struct.unpack("!IIII", header)
    correct_checksum = header[3]

    # Confirm if the checksum return is equal to header checksum
    checksum = checksum_calculator(encoded_message)
    is_data_corrupted = correct_checksum != checksum
    print("%s packet received from client" % ("Invalid" if is_data_corrupted else "Valid"))

    # Decode the received message
    message = encoded_message.decode()
    print("%s received from client" % message)

    # Transform the message
    uppercase_message = message.upper()

    # Return the transformed message to the client
    send_message = str.encode(uppercase_message)
    server_socket.sendto(send_message, address)
    print("%s sent to client" % send_message.decode())

