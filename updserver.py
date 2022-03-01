
import socket
print("We're in udp server...");
#select a server port
server_port = 12000
#create a UDP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#bind the server to the localhost at port server_port
server_socket.bind(('0.0.0.0',server_port))
#ready message

print('Server running on port ', server_port)


#Now the loop that actually listens from clients
#The same server socket serves all clients here
while True:
    cmsg, cadd = server_socket.recvfrom(2048)
    cmsg = cmsg.decode()

    # print(cmsg)
    # if(server_socket.sin_port()==11000):
    #     print("client1")
    # elif(server_socket.sin_port()==13000):
    #     print("client2")
    # else:
    print("success client")


