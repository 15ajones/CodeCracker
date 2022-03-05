import sys
import socket
import time
print("We're in tcp client...");

server_name = str(sys.argv[1])
server_port = int(sys.argv[2])

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((server_name, server_port))

while True:
    print("pinging")
    msg = "ping"
    client_socket.send(msg.encode())
    mseg = client_socket.recv(1024)
    print(mseg.decode())

client_socket.close()
