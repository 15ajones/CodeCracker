import socket
import subprocess
import time
import socket
import sys, platform
import ctypes, ctypes.util
import os.path

print("We're in tcp client...");

#the server name and port client wishes to access
server_name = '192.168.59.153'  #ipv4 of ec2
server_port = 11000
#create a TCP client socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Set up a TCP connection
#connection_socket will be assigned to this client on the server side
client_socket.connect((server_name, server_port))

msg = "admin"
client_socket.send(msg.encode())
print("sent" + msg)

game_over = input("Game Over? ") #y is go

while(game_over == "y"):

    msg = "your turn"
    client_socket.send(msg.encode())
    print("sent" + msg)

    # receive input passcode
    msg = client_socket.recv(1024)
    print(msg.decode())

    # send passchecker to arduino
    msg = "ggyrr"
    client_socket.send(msg.encode())
    print("sent" + msg)

    game_over = input("Game Over? ") #y is go



msg = "game over"
client_socket.send(msg.encode())
print("sent" + msg)

  
msg = "first place!"
client_socket.send(msg.encode())
print("sent" + msg)


# enabled commands:

# msg = "add user1 192.168.6.87 mypassword"
# msg = "getpass user1"
# msg = "guesspass user1 mypassword"
# msg = "updatepass user1 192.168.6.87 newpassword"
# msg = "getpass user1"
# msg = "add player1"



# #send the message  to the udp server
# client_socket.send(msg.encode())
# print("sent message")

# #return values from the server
# msg = client_socket.recv(1024)
# print(msg.decode())
client_socket.close()


