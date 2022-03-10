import socket

print("We're in udp client...");

#the server name and port client wishes to access
server_host_name = '35.176.178.191'
server_port = 12000
#create a UDP client socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

#Bind UDP client 2 to port 13000
client_socket.bind(('', 11000))  

contin = True

while contin:
    msg = input("Enter message into client: ");
    if msg == "x":
        contin = False
        break

    #send msg to server
    client_socket.sendto(msg.encode(),(server_host_name, server_port))
    print("msg sent to server")
    #recieve and print a reply
    server_msg = client_socket.recv(1024)
    print(server_msg.decode())

    # if (server_msg != "player added"):
    #     # msg = "my turn?"
    #     # client_socket.sendto(msg.encode(),(server_host_name, server_port))
    #     # print("msg sent to server")

    #     server_msg = client_socket.recv(1024)
    #     print(server_msg.decode())

    server_msg = client_socket.recv(1024)
    print(server_msg.decode())

client_socket.close()
