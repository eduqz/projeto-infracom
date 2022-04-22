import socket
import struct
from utils import checksum_calculator


# Define socket params
server_name = '127.0.0.1'
server_port = 65000

port = 65001

# Get user message
inputted_message = str(input('Digite: '))
encoded_message = str.encode(inputted_message)

# Calculate checksum
checksum = checksum_calculator(encoded_message)

# Create header and put it on the packet
header = struct.pack('!IIII', port, server_port, len(encoded_message), checksum)
packet_with_header = header + encoded_message

# Create the socket
client_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Send the message
client_socket.sendto(packet_with_header, (server_name, server_port))

# Get the returned message
returned_message, _ = client_socket.recvfrom(1024)
print("%s received from server" % returned_message.decode())

# Close the connection
client_socket.close()