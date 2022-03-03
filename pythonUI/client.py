import socket
import main

# set up TCP link to server
server_name = 'localhost' #insert public ipv4
server_port = 12421

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((server_name, server_port))
print('connected to server')


def connect_to_web :

    player = client_socket.recv(1024).decode()
    sequence = client_socket.recv(1024).decode()

    