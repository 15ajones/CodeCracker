import socket
import subprocess
import time
import socket
import sys, platform
import ctypes, ctypes.util
import os.path

'''     OFFICIAL COMBINED GAME  
            BOARD 1  - COMPLETE   '''

def main():

    #the server name and port client wishes to access
    board_server_name = '192.168.137.200'  #ip of arduino (subject to change - CHANGES
    board_server_port = 11000
    #create a TCP client socket
    board_client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    #binding to a port and address so that the server can send information back
    board_client_socket.bind(('', 15010))

    #the server name and port client wishes to access
    server_name = '18.132.60.200'  # public ipv4 of ec2
    server_port = 12000                        
    #create a TCP client socket
    ec2_client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # Bind board 1 socket to port 11000
    ec2_client_socket.bind(('', 16190))  # change port for each board

    print("Running UDP client for board 1...")
    #user presses button to join game
    # Add user/player to database
    msg = "Rohan"
    ec2_client_socket.sendto(str.encode(msg), (server_name, server_port))

    # msg = "Am I admin?"
    # ec2_client_socket.sendto(str.encode(msg), (server_name, server_port))

    msg, cadd = ec2_client_socket.recvfrom(1024)  # recieves user or admin
    server_msg = msg.decode()
    print("received " + server_msg)    #always print

    if (server_msg=="admin"):  
        #  To Do: send "admin" to arduino
        is_admin = True
        #1 is admin, 0 is player.
        # msg = "1"
        # board_client_socket.sendto(msg.encode(), (board_server_name, board_server_port))
        # print("sent to board: " + msg)        

    else:
        is_admin = False
    

    in_the_system = True
    in_game = False             #game started / else stalling in menu screen
    # game_name = ""
    while(in_the_system):
        if not in_game:        #menu screen state
            if is_admin: #user decides which game
                
                time.sleep(1) #added to give delay before sending admin to board (for game over issue)
                # Send message to board: WAITING FOR GAME   
                msg = "1"  # tells admin arduino to select game
                board_client_socket.sendto(msg.encode(), (board_server_name, board_server_port))
                print("sent to board: " + msg)    

                # receive selected game from board
                game_select_msg = board_client_socket.recv(1024)    # left/right
                game_select_msg = game_select_msg.decode()
                print("received code: " + game_select_msg)           
                
                #send selected game to the server
                server_msg = "admin " + game_select_msg  # admin select left/right
                ec2_client_socket.sendto(str.encode(server_msg), (server_name, server_port))


                if game_select_msg == "S":
                    msg, cadd = ec2_client_socket.recvfrom(1024)      # recieves game name 
                    server_msg = msg.decode()
                    print("game received: " + server_msg) 
                    print("game selected")  

                    if server_msg == "memory" or server_msg == "mastermind":
                        in_game =  True
                        msg = server_msg  # tells admin arduino what game is selected
                        board_client_socket.sendto(msg.encode(), (board_server_name, board_server_port))
                        print("sent to board: " + msg)   

                # if not start then continue 
                # if start then in_game == true
            
            else:   
                msg, cadd = ec2_client_socket.recvfrom(1024)  #user receives game name
                server_msg = msg.decode()
                print("received: " + server_msg)    #always print

                if server_msg == "memory" or server_msg == "mastermind":
                        in_game =  True
                        msg = "start game"  # tells admin arduino what game is selected
                        board_client_socket.sendto(msg.encode(), (board_server_name, board_server_port))
                        print("sent to board: " + msg)    

    
        else: #game state (during rounds)
            print("waiting for turn...") 
            msg, cadd = ec2_client_socket.recvfrom(1024)      # your 
            server_msg = msg.decode()
            print("received: " + server_msg)    #always print

            if server_msg == "game over":    # if eliminated -> receives game over message instead
                # Send game over message to board
                # board_msg = "game over"
                # board_client_socket.sendto(board_msg.encode(), (board_server_name, board_server_port))
                # print("sent" + board_msg)
                
                in_game = False
                time.sleep(1) #added to give delay before sending admin to board (for game over issue)


            elif server_msg == "your turn":     #server_msg == "your turn"
                # Send message to board: your turn
                board_msg = "your turn"
                board_client_socket.sendto(board_msg.encode(), (board_server_name, board_server_port))
                print("sent: " + board_msg)



                # receive input passcode from board
                inputpass_msg = board_client_socket.recv(1024)
                inputpass_msg = inputpass_msg.decode()
                print("received code: " + inputpass_msg)

                # Send inputted passcode from board to server
                server_msg = inputpass_msg  
                ec2_client_socket.sendto(str.encode(server_msg), (server_name, server_port))
        





if __name__ == '__main__':
    main()

