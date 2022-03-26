import socket


server_name = "127.0.0.1"
server_port = 65000

server_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

server_socket.bind((server_name, server_port))

print("UDP server up and listening")


while(True):
    encoded_message, address = server_socket.recvfrom(1024)

    message = encoded_message.decode()

    print("%s received from client" % message)

    uppercase_message = message.upper()

    send_message = str.encode(uppercase_message)
    server_socket.sendto(send_message, address)
    
    print("%s sent to client" % send_message.decode())

