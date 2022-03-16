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
    board_server_name = '192.168.73.153'  #ip of arduino (subject to change - fetch from serial monitor)
    board_server_port = 11000
    #create a TCP client socket
    board_client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    #binding to a port and address so that the server can send information back
    board_client_socket.bind(('', 15000))

    #the server name and port client wishes to access
    server_name = '35.176.178.191'  # public ipv4 of ec2
    server_port = 12000                        
    #create a TCP client socket
    ec2_client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Bind board 1 socket to port 11000
    ec2_client_socket.bind(('', 11000))  # change port for each board

    print("Running UDP client for board 1...")
    #user presses button to join game
    # Add user/player to database
    msg = "board1"
    ec2_client_socket.sendto(str.encode(msg), (server_name, server_port))

    # msg = "Am I admin?"
    # ec2_client_socket.sendto(str.encode(msg), (server_name, server_port))

    msg = ec2_client_socket.recvfrom(1024)  # recieves user or admin
    server_msg = msg.decode()

    if (server_msg=="admin"):  
        #  To Do: send "admin" to arduino
        is_admin = True
        #1 is admin, 0 is player.
        msg = "1"
        board_client_socket.sendto(msg.encode(), (board_server_name, board_server_port))
        print("sent to board: " + msg)        

    else:
        is_admin = False
    

    in_the_system = True
    in_game = False             #game started / else stalling in menu screen
    game_name = ""
    while(in_the_system):
        if not in_game:        #menu screen state
            if is_admin: #user decides which game
                # Send message to board: WAITING FOR GAME   
                board_msg = "game select"
                board_client_socket.sendto(board_msg.encode(), (board_server_name, board_server_port))
                print("sent: " + board_msg)

                # receive selected game from board
                game_select_msg = board_client_socket.recv(1024)
                game_select_msg = game_select_msg.decode()
                print("received code: " + game_select_msg)           

                #send selected game to the server
                server_msg = "admin start " + game_select_msg 
                ec2_client_socket.sendto(str.encode(server_msg), (server_name, server_port))
               
            else:   
                msg = ec2_client_socket.recvfrom(1024)  #user receives game name
                server_msg = msg.decode()
                if server_msg == "memory":
                    in_game = True
                    game_name = "memory"
                else:
                    in_game = True
                    game_name = "mastermind"
    
        else: #game state (during rounds)
            msg = ec2_client_socket.recvfrom(1024)  # recieves game name 
            server_msg = msg.decode()
            if server_msg == "game over":    # if eliminated -> receives game over message instead
                # # Send game over message to board
                # board_msg = "game over"
                # board_client_socket.sendto(board_msg.encode(), (board_server_name, board_server_port))
                # print("sent" + board_msg)

                # # Recieves leaderboard position from server 
                # server_msg = ec2_client_socket.recv(1024)
                # server_leaderboard_msg = server_msg.decode()                      

                # # Send leaderboard position to board    
                # board_msg = server_leaderboard_msg
                # board_client_socket.sendto(board_msg.encode(), (board_server_name, board_server_port))
                # print("sent" + board_msg)
                in_game = False
                game_name = ""
                continue 
            else: #server_msg == "your turn"
                # Send message to board: your turn
                board_msg = "your turn"
                board_client_socket.sendto(board_msg.encode(), (board_server_name, board_server_port))
                print("sent: " + board_msg)

                # receive input passcode from board
                inputpass_msg = board_client_socket.recv(1024)
                print("received code: " + inputpass_msg.decode())

                # Send inputted passcode from board to server
                server_msg = inputpass_msg  
                ec2_client_socket.sendto(str.encode(server_msg), (server_name, server_port))
        





                                    
    
            







# #if mastermind then do below 


#     r = 0 # keeps track of round number during game

#     while(gameover_status != "game over"):

#         # Increment round number at start of round
#         r += 1
#         print("Round " + r)

#         # Send message to server asking if it is player's turn: 
#         # msg = "Is it my turn?"
#         # ec2_client_socket.sendto(str.encode(msg), (server_name, server_port))
        
#         # Receive reply from server if your turn 
#         server_msg = ec2_client_socket.recvfrom(1024)
#         confirm_turn_msg = server_msg.decode()
        
#         if ( confirm_turn_msg == "Your turn" ):

#             # Send message to board: your turn
#             board_msg = "your turn"
#             board_client_socket.sendto(board_msg.encode(), (board_server_name, board_server_port))
#             print("sent: " + board_msg)

#             # receive input passcode from board
#             inputpass_msg = board_client_socket.recv(1024)
#             print("received code: " + inputpass_msg.decode())

#             # Send inputted passcode from board to server
#             server_msg = inputpass_msg  
#             ec2_client_socket.sendto(str.encode(server_msg), (server_name, server_port))

#         # Check for game over status
#         gameover_msg = ec2_client_socket.recvfrom(1024)
#         gameover_status = gameover_msg.decode()




# #else -> memory ...





#     # In stop state -> send game over to board + leaderboard retrieval

#     # Send game over message to board
#     board_msg = "game over"
#     board_client_socket.sendto(board_msg.encode(), (board_server_name, board_server_port))
#     print("sent" + board_msg)

#     # Recieves leaderboard position from server 
#     server_msg = ec2_client_socket.recv(1024)
#     server_leaderboard_msg = server_msg.decode()                      

#     # Send leaderboard position to board    
#     board_msg = server_leaderboard_msg
#     board_client_socket.sendto(board_msg.encode(), (board_server_name, board_server_port))
#     print("sent" + board_msg)


#     # Remove board1 from database
#     msg = "remove board1"                           # need to implement in udp server
#     ec2_client_socket.sendto(str.encode(server_msg), (server_name, server_port))

#     # Close UDP socket
#     ec2_client_socket.close()
#     board_client_socket.close()




if __name__ == '__main__':
    main()

