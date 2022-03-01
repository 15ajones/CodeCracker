import socket
print("We're in udp client...");

#the server name and port client wishes to access
server_name = 'localhost'
server_port = 12000
#create a UDP client socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

#Bind UDP client 2 to port 13000
client_socket.bind((server_name, 13000))

#some work
msg = input("Enter message into client 2: ");

#send the message  to the udp server
client_socket.sendto(msg.encode(),(server_name, server_port))


client_socket.close()
