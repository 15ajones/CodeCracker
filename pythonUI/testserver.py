import socket
print("We're in tcp server...");

#select a server port
server_port = 12721
#create a UDP socket
welcome_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#bind the server to the localhost at port server_port
welcome_socket.bind(('localhost',server_port))

#extra for tcp socket:
welcome_socket.listen(1)

#ready message
print('Server running on port ', server_port)

#Now the loop that actually listens from clients
while True:
    connection_socket, caddr = welcome_socket.accept()
    #notice recv and send instead of recvto and sendto
    cmsg = "play,seq"
    connection_socket.send(cmsg.encode())
    

    

