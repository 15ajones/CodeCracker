import boto3
import socket
from decimal import Decimal
from pprint import pprint
from boto3.dynamodb.conditions import Key
from random import randrange
import time
def create_user_table(dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb',region_name='us-east-1')

    table = dynamodb.create_table(
        TableName='Users',
        KeySchema=[
            {
                'AttributeName': 'User', # the User value is the socket value of a player
                'KeyType': 'HASH'  # Partition key
            },
            {
                'AttributeName': 'Name', #the user name the user wants to send
                'KeyType': 'RANGE' # Sort key
            } 
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'User',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'Name',
                'AttributeType': 'S'
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        }
    )
    print("created table")
    return table

def add_user(user,name,dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table('Users')
    response = table.put_item(
        Item={
            'User': user,
            'Name' : name,
            'info': {
                'points': 0
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

def delete_user_table(dynamodb=None):
    try:
        if not dynamodb:
            dynamodb = boto3.resource('dynamodb', region_name="us-east-1")
        table = dynamodb.Table('Users')
        print("deleted table")
        table.delete()
    except:
        pass

def main():
    print("Server has started running")
    # delete_user_table()
    table = create_user_table()
    server_port = 12000
    #create a UDP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    #bind the server to the localhost at port server_port
    server_socket.bind(('0.0.0.0',server_port))
    #ready message
    print('Chat server running on port ', server_port)

    #Now the loop that actually listens from clients
    #The same server socket serves all clients here

    # board1 = ('0.0.0.0', 11000)
    # board2 = ('0.0.0.0', 12000)
    # board3 = ('0.0.0.0', 13000)
    # board4 = ('0.0.0.0', 14000)
    # board5 = ('0.0.0.0', 15000)
    # board6 = ('0.0.0.0', 16000)
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
    
    while True:

        if not game_started: # IN MENU SCREEN
            #---------------------------------------------------------------------------
            # RECEIVING A MESSAGE FROM A USER/ADMIN
            cmsg, cadd = server_socket.recvfrom(2048)
            player_to_add = [str(cadd[0]), int(cadd[1])]
            player_to_add += str(cmsg)
            print(str(player_to_add))
            cmsg = cmsg.decode()
            print(cmsg)
            cmsg = cmsg.split()
            #---------------------------------------------------------------------------
            # HANDLING MESSAGE IF ITS FROM ADMIN
            if len(cmsg)==2 and cmsg[0]=="admin":
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

                elif cmsg[1] == "S":
                    selection = menu_options[current_menu_select]
                    if selection == "leaderboard":
                        if UI_cadd != "none":
                            cmsg = "select"
                            server_socket.sendto(cmsg.encode(), UI_cadd)
                            time.sleep(5)
                            cmsg = "menu"
                            server_socket.sendto(cmsg.encode(), UI_cadd)

                    elif selection == "mastermind":
                        game_type = "mastermind"
                        game_started = True
                        wordle = ""
                        if UI_cadd != "none":
                            cmsg = "select"
                            server_socket.sendto(cmsg.encode(), UI_cadd)
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
                        memory_pattern = ""
                        memory_players = players
                        players_left = len(memory_players)
                        cmsg = "memory"
                        for player in players:
                            server_socket.sendto(cmsg.encode(), (player[0], int(player[1])))
                        i = -1
            #---------------------------------------------------------------------------
            # HANDLING MESSAGE IF ITS FROM UI
            elif cmsg[0]=="ui" or cmsg[0]=="UI":
                UI_cadd = cadd
            #---------------------------------------------------------------------------
            # RECEIVING MESSAGE FROM NEW USER
            else:
                
                is_admin = True if number_players == 0 else False
                players.append(player_to_add)
                add_user(str(player_to_add[0]), str(cmsg))
                # add_user(str(cadd), str(cmsg[0]), is_admin)
                number_players+=1
                if is_admin:
                    cmsg = "admin"
                else:
                    cmsg = "user"
                
                server_socket.sendto(cmsg.encode(), cadd)
            #---------------------------------------------------------------------------



        else: # IN ONGOING GAME
            
            while game_started:

                # DOING MASTERMIND GAME
                if game_type == "mastermind":

                    for player in players: 

                        if not game_started:
                            break
                        else:
                            if UI_cadd != "none":
                                cmsg = "turn " +  player[0] 
                                server_socket.sendto(cmsg.encode(), UI_cadd)
                            cmsg = "your turn"
                            server_socket.sendto(cmsg.encode(), (player[0], int(player[1])))
                            valid_reply = False
                            while not valid_reply:
                                cmsg, cadd = server_socket.recvfrom(2048)
                                guess = cmsg.decode()
                                print("guess is: ", guess)
                                valid_reply = True
                            guess_reply = ""
                            correct_guess = True
                            for i in range(5): 
                                if guess[i]==wordle[i]:
                                    guess_reply += "g"
                                elif guess[i] in wordle:
                                    guess_reply += "y"
                                    correct_guess = False
                                else:
                                    guess_reply += "r"
                                    correct_guess = False
                            if UI_cadd != "none":
                                cmsg = "outcome " +  guess_reply
                                server_socket.sendto(cmsg.encode(), UI_cadd)
                            if correct_guess: # if correct guess we send a message saying game over to everyone, and end this section
                                if UI_cadd != "none":
                                    cmsg = "winner " +  str(player[0]) 
                                    server_socket.sendto(cmsg.encode(), UI_cadd)
                                
                                game_started = False
                                cmsg = "game over"
                                for x in players:
                                    server_socket.sendto(cmsg.encode(), (x[0], int(x[1])))
                                time.sleep(5)
                                if UI_cadd != "none":
                                    cmsg = "menu"
                                    server_socket.sendto(cmsg.encode(), UI_cadd)
                                    cmsg = "leaderboard omar 0"
                                    server_socket.sendto(cmsg.encode(), UI_cadd)
                                
                
                elif game_type == "memory":
                    if players_left == 1:
                        game_started = False
                        for player in players:
                            if player!=0:
                                winner = player
                                break
                        cmsg = "game over"
                        for x in players:
                            server_socket.sendto(cmsg.encode(), (x[0], int(x[1])))
                        if UI_cadd != "none":
                            cmsg = "winner " +  winner
                            server_socket.sendto(cmsg.encode(), UI_cadd)
                            time.sleep(5)
                            cmsg = "menu " +  player[0]
                            server_socket.sendto(cmsg.encode(), UI_cadd)
                            cmsg = "leaderboard omar 0"
                            server_socket.sendto(cmsg.encode(), UI_cadd)

                    
                    for player in memory_players:
                        if UI_cadd != "none":
                            cmsg = "players"
                            for x in memory_players:
                                cmsg+=" "
                                cmsg+=memory_players[0]
                            server_socket.sendto(cmsg.encode(), UI_cadd)
                        if not game_started:#if game has ended we can end the for loop and leave this section
                            break
                        i+=1
                        if player == 0:
                            continue
                        if UI_cadd != "none":
                            cmsg = "turn " +  player[0] 
                            server_socket.sendto(cmsg.encode(), UI_cadd)
                        cmsg = "your turn"
                        server_socket.sendto(cmsg.encode(), (player[0], int(player[1])))
                        cmsg, cadd = server_socket.recvfrom(2048)
                        cmsg = cmsg.decode()
                        if memory_pattern == "": #start of new pattern
                            memory_pattern += cmsg[0]
                        else: 
                            if cmsg[0:len(memory_pattern)] == memory_pattern and len(cmsg) == len(memory_pattern)+1: # player got pattern right, extends it
                                memory_pattern = cmsg
                                if UI_cadd != "none":
                                    cmsg = "move " + cmsg[-1]
                                    server_socket.sendto(cmsg.encode(), UI_cadd)
                            else: #player got pattern wrong, is eliminated.
                                memory_players[i] = 0;
                                players_left-=1
                                if players_left == 1:
                                    game_started = False
                                    break
                                memory_pattern = ""


if __name__ == "__main__":
    main()




