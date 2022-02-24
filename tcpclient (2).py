import socket
import subprocess
import time
import socket
import sys, platform
import ctypes, ctypes.util
import os.path

print("We're in tcp client...");

#the server name and port client wishes to access
server_name = '35.176.178.191'  #ipv4 of ec2
server_port = 12000
#create a TCP client socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Set up a TCP connection
#connection_socket will be assigned to this client on the server side
client_socket.connect((server_name, server_port))

# enabled commands:

# msg = "add user1 192.168.6.87 mypassword"
# msg = "getpass user1"
# msg = "guesspass user1 mypassword"
# msg = "updatepass user1 192.168.6.87 newpassword"
msg = "getpass user1"


#send the message  to the udp server
client_socket.send(msg.encode())

#return values from the server
msg = client_socket.recv(1024)
print(msg.decode())
client_socket.close()




