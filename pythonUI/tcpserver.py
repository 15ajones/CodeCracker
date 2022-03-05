import socket
import time
print("We're in tcp server...");

server_port = 12000
welcome_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
welcome_socket.bind(('localhost', server_port))
welcome_socket.listen(1)

print('Server running on port ', server_port)

connection_socket, caddr = welcome_socket.accept()

while True:
    client_msg = connection_socket.recv(1024)
    client_msg = client_msg.decode()
    if client_msg == "ping":
        server_msg = "Player Data"
        connection_socket.send(server_msg.encode())
    else:
        pass
    print("cycle")

