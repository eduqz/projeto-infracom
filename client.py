import socket


server_name = '127.0.0.1'
server_port = 65000

inputted_message = str(input('Digite: '))
encoded_message = str.encode(inputted_message)

client_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

client_socket.sendto(encoded_message, (server_name, server_port))

returned_message, _ = client_socket.recvfrom(1024)

print("%s received from server" % returned_message.decode())

client_socket.close()