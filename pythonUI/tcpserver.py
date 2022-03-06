from cgi import test
import socket
import time
print("We're in tcp server...");

server_port = 12000
welcome_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
welcome_socket.bind(('localhost', server_port))
welcome_socket.listen(1)

print('Server running on port ', server_port)

connection_socket, caddr = welcome_socket.accept()

count = 0
while True:
    client_msg = connection_socket.recv(1024)
    client_msg = client_msg.decode()
    if client_msg == "ping":
        test_input = str(count)
        connection_socket.send(test_input.encode())
    count += 1
    time.sleep(0.5)

