import socket
import subprocess
import time
import socket
import sys, platform
import ctypes, ctypes.util
import os.path
import urllib.request
from urllib.request import urlopen
import ssl
import json


ssl._create_default_https_context = ssl._create_unverified_context # uses unverified to bypass certificate error

READ_API_KEY = "AALOIQGCNR869UZ5"
CHANNEL_ID = "1662430"


def main():

    print("Running UDP client for board 1...");

    #the server name and port client wishes to access
    server_name = "localhost"  # public ipv4 of ec2
    server_port = 10000                         # change for each board
    #create a TCP client socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Bind board 1 socket to port 11000
    client_socket.bind((server_name, 11000))

    #Set up a UDP read_conection
    #read_conection_socket will be assigned to this client on the server side
    #client_socket.read_conect((server_name, server_port))


    # Add user/player to database
    msg = "add player1"
    client_socket.sendto(str.encode(msg), (server_name, server_port))
    msg = client_socket.recvfrom(1024)
    server_msg = msg.decode()
    print(server_msg)
    client_socket.close()


    # msg = "Am I admin?"
    # client_socket.sendto(str.encode(msg), (server_name, server_port))

    # msg = client_socket.recvfrom(1024)
    # server_msg = msg.decode()

    # if (server_msg=="y"):
    #     msg = "admin start"
    #     client_socket.sendto(str.encode(msg), (server_name, server_port))


    # while(gameover_status != "game over"):

    #     # Read Thingspeak channel for board 1  
    #     read_con = urlopen("http://api.thingspeak.com/channels/%s/feeds/last.json?api_key=%s" \
    #                         % (CHANNEL_ID,READ_API_KEY))
        
    #     response = read_con.read()
    #     http_status_code = read_con.getcode()

    #     if (http_status_code == 200):
    #         print("HTTP read_conection Successfull!")
    #     else:
    #         print("HTTP read_conection Failed!")
    #         break       # check

    #     # Send message to server asking if it is player's turn:
    #     msg = "Is it my turn?"
    #     client_socket.sendto(str.encode(msg), (server_name, server_port))
        
    #     # Receive reply from server  
    #     msg = client_socket.recvfrom(1024)
    #     confirm_turn_msg = msg.decode()
        
    #     if ( confirm_turn_msg == "Your turn" ):

    #         # Load field 1 (inputpass) data from ThingSpeak channel
    #         data=json.loads(response)
    #         input_pass = data['field1']                         # read field 1 - inputted password from board

    #         # Send inputted passcode from board to server
    #         msg = input_pass  
    #         client_socket.sendto(str.encode(msg), (server_name, server_port))

    #         msg = client_socket.recvfrom(1024)                  # receive g/y/r sequence (passchecker) for inputted pass
    #         pass_checker = msg.decode()
            
    #         # Send passchecker sequence to thingspeak channel to be read by board:
    #         write_msg = pass_checker
    #         write_msg = write_msg.replace('\n', "%0A")
    #         field_num = "2"                                     # field2: passchecker
    #         write_con=urlopen('https://api.thingspeak.com/update?api_key=LKDF3RROONZUUTAS&field'+field_num+'='+write_msg)
    #         print("\nMessage has successfully been sent to ThingSpeak channel. Field number = " + field_num + " Message: " + write_msg)


    #     # Check for game over status
    #     msg = client_socket.recvfrom(1024)
    #     gameover_status = msg.decode()



    # # In stop state -> leaderboard retrieval

    # msg = client_socket.recv(1024)
    # server_msg = msg.decode()                       # recieves leaderboard score from server 

    # write_msg = server_msg                          # assumes server sends leaderboard number e.g 1/2/3/4
    # write_msg = write_msg.replace('\n', "%0A")
    # field_num = "4"                                 # field4: leaderboard

    # write_con=urlopen('https://api.thingspeak.com/update?api_key=LKDF3RROONZUUTAS&field'+field_num+'='+write_msg)
    # print("\nMessage has successfully been sent to ThingSpeak channel. Field number = " + field_num + " Message: " + write_msg)

        

    # # Remove board1 from database
    # msg = "remove board1"                           # need to implement in udp server
    # client_socket.send(msg.encode())

    # # Close UDP socket
    # client_socket.close()
    # # Close ThingSpeak channel
    # read_con.close() 
    # write_con.close()








    # while(1):

    #     # Read Thingspeak channel for board 1  
    #     read_con = urlopen("http://api.thingspeak.com/channels/%s/feeds/last.json?api_key=%s" \
    #                         % (CHANNEL_ID,READ_API_KEY))

    #     response = read_con.read()
    #     http_status_code = read_con.getcode()

    #     if (http_status_code == 200):
    #         print("HTTP read_conection Successfull!")
    #     else:
    #         print("HTTP read_conection Failed!")
    #         break       # check

    #     data=json.loads(response)

    #     input_pass = data['field1']   
    #     start = data['field3']   # start/stop: 1=start, 0=stop


    #     # Send commands to server here: (msg)


    #     while(start):   # In start state

    #         # Receive message from udp server
    #         msg = client_socket.recvfrom(1024)
    #         server_msg = msg.decode()

    #         if (server_msg == "y"):   # inputted pass matches database pass -> passchecker = y
    #             write_msg = "y"
    #             write_msg = write_msg.replace('\n', "%0A")
    #             field_num = "2"         # field2: passchecker

    #             write_con=urlopen('https://api.thingspeak.com/update?api_key=LKDF3RROONZUUTAS&field'+field_num+'='+write_msg)
    #             print("\nMessage has successfully been sent to ThingSpeak channel. Field number = " + field_num + " Message: " + write_msg)

    #         elif (server_msg == "m"):   # inputted pass matches database pass BUT in wrong order -> passchecker = m
    #             write_msg = "m"
    #             write_msg = write_msg.replace('\n', "%0A")
    #             field_num = "2"         # field2: passchecker

    #             write_con=urlopen('https://api.thingspeak.com/update?api_key=LKDF3RROONZUUTAS&field'+field_num+'='+write_msg)
    #             print("\nMessage has successfully been sent to ThingSpeak channel. Field number = " + field_num + " Message: " + write_msg)
            
    #         elif (server_msg == "n"):   # inputted pass does NOT match database pass -> passchecker = n
    #             write_msg = "n"
    #             write_msg = write_msg.replace('\n', "%0A")
    #             field_num = "2"         # field2: passchecker

    #             write_con=urlopen('https://api.thingspeak.com/update?api_key=LKDF3RROONZUUTAS&field'+field_num+'='+write_msg)
    #             print("\nMessage has successfully been sent to ThingSpeak channel. Field number = " + field_num + " Message: " + write_msg)


        










if __name__ == '__main__':
    main()