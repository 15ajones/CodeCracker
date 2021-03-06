import boto3
import socket
from decimal import Decimal
from pprint import pprint
from boto3.dynamodb.conditions import Key
from random import randrange
import time

def add_user(user,name,is_admin,dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table('Users')
    response = table.put_item(
        Item={
            'User': user,
            'Name' : name,
            'info': {
                'points': 0,
                'is_admin' : is_admin
            }
        }
    )
    print("added user")
    return response

def update_points(user, name, point):#pass param is the new password
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table('Users')
    response = table.update_item(
        Key={
            'User':user,
            'Name':name
        },
        UpdateExpression = "set info.points=:r",
        ExpressionAttributeValues={
            ':r': point
        },
        ReturnValues = "UPDATED_NEW"
    )
    return response

def query_user(user, dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', region_name="us-east-1")
    table = dynamodb.Table('Users')
    response = table.query(
        KeyConditionExpression=Key('User').eq(user)
    )
    results = response['Items']
    for result in results:
        return(result)
    print("finished query")

#{'info': {'is_admin': True, 'points': Decimal('0')}, 'User': '62125', 'Name': 'board1'}
def main():

    server_port = 12000
    #create a UDP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    #bind the server to the localhost at port server_port
    server_socket.bind(('0.0.0.0',server_port))
    #ready message
    print('Chat server running on port ', server_port)

    #Now the loop that actually listens from clients
    #The same server socket serves all clients here

    wordle_characters = ["L","R","1","2","3"]
    wordle_length = 5
    game_started = False
    number_players = 0
    players = []
    UI_cadd = "none"
    game_type = ""
    memory_pattern = ""
    memory_players = []
    menu_options = ["mastermind", "memory", "leaderboard"]
    current_menu_select = 0
    msgs_to_receive = 0
    while True:
        if not game_started:
            
            cmsg, cadd = server_socket.recvfrom(2048)
            player_to_add = [str(cadd[0]), int(cadd[1])]
            print(str(player_to_add))
            cmsg = cmsg.decode()
            print(cmsg)
            cmsg = cmsg.split()
            if msgs_to_receive > 0:
                msgs_to_receive = 0
                print("ignored message")
                cmsg = "game over"
                server_socket.sendto(cmsg.encode(), (cadd[0], int(cadd[1])))
            elif len(cmsg)==2 and cmsg[0]=="admin":
                if cmsg[1] == "L":
                    if UI_cadd != "none" and current_menu_select > 0:
                        cmsg = "left"
                        server_socket.sendto(cmsg.encode(), UI_cadd)
                        current_menu_select-=1
                elif cmsg[1] == "R":
                    if UI_cadd != "none" and current_menu_select < 2:
                        cmsg = "right"
                        server_socket.sendto(cmsg.encode(), UI_cadd)
                        current_menu_select+=1
                        print("sent")

                elif cmsg[1] == "S":
                    selection = menu_options[current_menu_select]
                    if selection == "leaderboard":
                        if UI_cadd != "none":
                            cmsg = "select"
                            server_socket.sendto(cmsg.encode(), UI_cadd)
                            time.sleep(5)
                            cmsg = "menu"
                            server_socket.sendto(cmsg.encode(), UI_cadd)
                            print("sent")
                        cmsg = "leaderboard"
                        server_socket.sendto(cmsg.encode(), cadd)
                        

                    elif selection == "mastermind":
                        game_type = "mastermind"
                        game_started = True
                        wordle = ""
                        if UI_cadd != "none":
                            cmsg = "select"
                            server_socket.sendto(cmsg.encode(), UI_cadd)
                            print("sent")
                        for i in range(5):
                            x = int(randrange(4))
                            wordle+=wordle_characters[x]
                        print(wordle)
                        cmsg = "mastermind"
                        for player in players:
                            server_socket.sendto(cmsg.encode(), (player[0], int(player[1])))

                    elif selection == "memory":
                        game_type = "memory"
                        game_started = True
                        wordle = ""
                        if UI_cadd != "none":
                            cmsg = "select"
                            server_socket.sendto(cmsg.encode(), UI_cadd)
                        for i in range(5):
                            x = int(randrange(4))
                            wordle+=wordle_characters[x]
                        print(wordle)
                        cmsg = "memory"
                        for player in players:
                            server_socket.sendto(cmsg.encode(), (player[0], int(player[1])))

            elif cmsg[0]=="ui" or cmsg[0]=="UI":
                UI_cadd = cadd
        
            else:
                is_admin = True if number_players == 0 else False
                players.append(player_to_add)
                add_user(str(player_to_add[1]), str(cmsg[0]), is_admin)
                print(query_user(str(player_to_add[1])))
                number_players+=1
                if UI_cadd != "none":
                    cmsg = "leaderboard " + str(cmsg[0]) + " 0"
                    print("sending", cmsg)
                    server_socket.sendto(cmsg.encode(), UI_cadd)
                    print("sent")
                    time.sleep(4)
                if is_admin:
                    cmsg = "admin"
                else:
                    cmsg = "user"
                server_socket.sendto(cmsg.encode(), cadd)
        else:
            #game has started
            #client waits until they receive the message "Your turn"
            # Once client receives this message, they enter their move and it is sent to the server.
            # client then sends ggrgy for example to all clients (g means right character, right place, y means right character, wrong place, r means wrong character)
            # When game ends, the server sends all clients the message: "Game over! x wins"
            while game_started:
                if game_type == "mastermind":
                    for player in players: #go through each player's turn
                        if not game_started:#if game has ended we can end the for loop and leave this section
                            break
                        else:
                            if UI_cadd != "none":
                                # cmsg = "turn " +  player[0] 
                                cmsg = "turn " + str(query_user(str(player[1]))['Name'])
                                print("sending", cmsg)
                                server_socket.sendto(cmsg.encode(), UI_cadd)
                                print("sent")
                                time.sleep(4)
                            cmsg = "your turn"
                            # print(cmsg)
                            # print(player[0])
                            # print(player[1])
                            server_socket.sendto(cmsg.encode(), (player[0], int(player[1])))
                            valid_reply = False
                            while not valid_reply: #keep searching for replies until we get a 5 bit word from the player who's go it is.
                                cmsg, cadd = server_socket.recvfrom(2048)
                                guess = cmsg.decode()
                                print("guess is: ", guess)
                                # if len(guess) == 5: #need to add code to make sure its the current player and the guess length is 5)
                                valid_reply = True
                            guess_reply = ""
                            correct_guess = True
                            for i in range(5): # in this loop we derive the wordle reply to a guess
                                if guess[i]==wordle[i]:
                                    guess_reply += "g"
                                elif guess[i] in wordle:
                                    guess_reply += "y"
                                    correct_guess = False
                                else:
                                    guess_reply += "r"
                                    correct_guess = False
                            print("correct guess: ", correct_guess)
                            if UI_cadd != "none":
                                cmsg = "outcome " +  guess_reply
                                server_socket.sendto(cmsg.encode(), UI_cadd)
                                print("sent outcome")
                                time.sleep(5)
                            if correct_guess: # if correct guess we send a message saying game over to everyone, and end this section
                                point = int(query_user(str(player[1]))['info']['points'])
                                name = str(query_user(str(player[1]))['Name'])
                                point+=1
                                update_points(str(player[1]),name,point)
                                if UI_cadd != "none":
                                    cmsg = "winner " +  str(query_user(str(player[1]))['Name'])
                                    server_socket.sendto(cmsg.encode(), UI_cadd)
                                    time.sleep(5)
                                game_started = False
                                cmsg = "game over"
                                for x in players:
                                    server_socket.sendto(cmsg.encode(), (x[0], int(x[1])))
                                time.sleep(5)
                                if UI_cadd != "none":
                                    cmsg = "menu"
                                    server_socket.sendto(cmsg.encode(), UI_cadd)
                                    cmsg = "leaderboard"
                                    for n in players:
                                        cmsg+=" " +str(query_user(str(n[1]))['Name'])+ " "+ str(int(query_user(str(n[1]))['info']['points']))
                                    server_socket.sendto(cmsg.encode(), UI_cadd)
                                    time.sleep(5)
                                
                
                elif game_type == "memory":
                    msgs_to_receive = len(players)
                    t = int(randrange(15))
                    time.sleep(t)
                    if UI_cadd != "none":
                        cmsg = "start " + wordle
                        print("sending", cmsg)
                        server_socket.sendto(cmsg.encode(), UI_cadd)
                        print("sent")
                        cmsg = "your turn"
                        for player in players:
                            cmsg = "your turn"
                            server_socket.sendto(cmsg.encode(), (player[0], int(player[1])))
                            print("sent to client")

                    replies = 0
                    while replies<2:
                        cmsg, cadd = server_socket.recvfrom(2048)
                        guess = cmsg.decode()
                        msgs_to_receive = msgs_to_receive - 1
                        print("guess is: ", guess)
                        if guess == wordle:
                            game_started = False
                            game_has_ended = True
                            # for player in players:
                            #     cmsg = "game over"
                            #     server_socket.sendto(cmsg.encode(), (player[0], int(player[1])))
                            cmsg = "game over"
                            server_socket.sendto(cmsg.encode(), (cadd[0], int(cadd[1])))
                            point = int(query_user(str(cadd[1]))['info']['points'])
                            name = str(query_user(str(cadd[1]))['Name'])
                            point+=1
                            update_points(str(cadd[1]),name,point)
                            if UI_cadd:
                                cmsg = "winner " + str(query_user(str(cadd[1]))['Name'])
                                server_socket.sendto(cmsg.encode(), UI_cadd)
                                time.sleep(2)
                                cmsg = "menu"
                                server_socket.sendto(cmsg.encode(), UI_cadd)
                                time.sleep(1)
                                for n in players:
                                    cmsg = "leaderboard " + str(query_user(str(n[1]))['Name'])+ " "+ str(int(query_user(str(n[1]))['info']['points']))
                                    server_socket.sendto(cmsg.encode(), UI_cadd)
                                    time.sleep(1)
                            break
                        else:
                            cmsg = "game over"
                            server_socket.sendto(cmsg.encode(), (cadd[0], int(cadd[1])))
                            replies+=1


                    if replies>1:
                        game_started = False
                        for player in players:
                            cmsg = "game over"
                            server_socket.sendto(cmsg.encode(), (player[0], int(player[1])))
                        if UI_cadd:
                            server_socket.sendto(cmsg.encode(), UI_cadd)
                            time.sleep(2)
                            cmsg = "menu"
                            server_socket.sendto(cmsg.encode(), UI_cadd)
                            time.sleep(1)
                            for n in players:
                                    cmsg = "leaderboard " + str(query_user(str(n[1]))['Name'])+ " "+ str(int(query_user(str(n[1]))['info']['points']))
                                    server_socket.sendto(cmsg.encode(), UI_cadd)
                                    time.sleep(1)
                            break







                    
                    

                        




                        
#ASK IF ADMIN/ BOARDS NEED TO BE TOLD WHEN THE GAME ENDS

#  if len(cmsg)==2 and cmsg[0]=="admin" and cmsg[1]=="start":
#                 if cmsg[2] == "mastermind":
#                     game_type = "mastermind"
#                     game_started = True
#                     wordle = ""
#                     if UI_cadd != "none":
#                         cmsg = "select"
#                         server_socket.sendto(cmsg.encode(), UI_cadd)
#                     for i in range(5):
#                         x = int(randrange(4))
#                         wordle+=wordle_characters[x]
#                     cmsg = "mastermind"
#                     for player in players:
#                         server_socket.sendto(cmsg.encode(), (player[0], int(player[1])))

#                 elif cmsg[2] == "memory":
#                     game_type = "memory"
#                     game_started = True
#                     cmsg = "game memory started"
#                     print(cmsg)
#                     server_socket.sendto(cmsg.encode(), cadd)
#                     wordle = ""
#                     if UI_cadd != "none":
#                         cmsg = "right"
#                         server_socket.sendto(cmsg.encode(), UI_cadd)
#                         cmsg = "select"
#                         server_socket.sendto(cmsg.encode(), UI_cadd)
#                     memory_pattern = ""
#                     memory_players = players
#                     players_left = len(memory_players)
#                     cmsg = "memory"
#                     for player in players:
#                         server_socket.sendto(cmsg.encode(), (player[0], int(player[1])))
#                     i = -1                           


                        

#turn user1
#move L
#eliminated user1
#winner user2  
                     
#to do: update points after a winner - do it when working with Omar

if __name__ == "__main__":
    main()




