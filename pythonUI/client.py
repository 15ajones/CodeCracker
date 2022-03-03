import socket
import main

client_socket = main.client_socket

answer = client_socket.recv(1024).decode()
while True : 
    if client_socket.recv(1024).decode == 'end' :
        break
    player = client_socket.recv(1024).decode()
    sequence = client_socket.recv(1024).decode()
client_socket.close()
    
    

    

    