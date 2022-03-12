import socket
import subprocess
import time
import socket
import sys, platform
import ctypes, ctypes.util
import os.path

print("We're in udp client...");

#the server name and port client wishes to access
server_name = '192.168.73.153'  #ipv4 of ec2
server_port = 11000
#create a TCP client socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#binding to a port and address so that the server can send information back
client_socket.bind(("", 15000))


#1 is admin, 0 is player.
msg = "1"
client_socket.sendto(msg.encode(), (server_name, server_port))
print("sent: " + msg)

# #return values from the server
# msg, sadd= client_socket.recvfrom(2048)
# print(msg.decode())

game_over = input("Game Over? ") #y is go

while(game_over == "n"):

    msg = "your turn"
    client_socket.sendto(msg.encode(), (server_name, server_port))
    print("sent: " + msg)

    # receive input passcode
    msg = client_socket.recv(1024)
    print("received code: " + msg.decode())

    # # send passchecker to arduino
    # msg = "ggyrr"
    # client_socket.sendto(msg.encode(), (server_name, server_port))
    # print("sent: " + msg)

    game_over = input("Game Over? ") #y is go



# msg = "game over"
# client_socket.send(msg.encode()) fix this line for udp
# print("sent" + msg)

  
# msg = "first place!"
# client_socket.send(msg.encode())
# print("sent" + msg)


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