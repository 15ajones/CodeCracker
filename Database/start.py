import boto3
import socket
from decimal import Decimal
from pprint import pprint
from boto3.dynamodb.conditions import Key

def create_user_table(dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb',region_name='us-east-1')

    table = dynamodb.create_table(
        TableName='Users',
        KeySchema=[
            {
                'AttributeName': 'User',
                'KeyType': 'HASH'  # Partition key
            },
            {
                'AttributeName': 'IP',
                'KeyType': 'RANGE' # Sort key
            } 
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'User',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'IP',
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

def add_user(user,ip,dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table('Users')
    response = table.put_item(
        Item={
            'User': user,
            'IP' : ip,
            'info': {
                'points': 0
            }
        }
    )
    print("added user")
    return response

def update_password(user, IP, point):#pass param is the new password
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table('Users')
    response = table.update_item(
        Key={
            'User':user,
            'IP':IP
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
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', region_name="us-east-1")

    table = dynamodb.Table('Users')
    print("deleted table")
    table.delete()
#add_user("omar","192...","qwerty")
# query_user("omar")
# delete_user_table()
print("We're in tcp server...");

#select a server port
server_port = 12000
#create a UDP socket
welcome_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#bind the server to the localhost at port server_port
welcome_socket.bind(('0.0.0.0',server_port))

#extra for tcp socket:
welcome_socket.listen(1)

#ready message
print('Server running on port ', server_port)

#Now the loop that actually listens from clients
game_started = False
number_players = 0
while True:
    if not game_started:
        if number_players == 1: #numbers of players for game to start
            game_started = True
            wordle = 
        else:
            connection_socket, caddr = welcome_socket.accept()
            # notice recv and send instead of recvto and sendto
            cmsg = connection_socket.recv(1024)  	
            cmsg = cmsg.decode()
            x = cmsg.split()
            if x[0] == "add": # adds a user : example input : add omar 112.334.5                                                                                                                                                                                                                                                                                                                               
                add_user(x[1],x[2])
                cmsg = "added user"
                connection_socket.send(cmsg.encode())
                number_players+=1
    else:
        
            
            
            
                


            
        
        
    #     cmsg = x[1] + " added"
    #     connection_socket.send(cmsg.encode())
    # elif x[0] == "getpass":
    #     cmsg = str(query_user(x[1])['info']['password'])
    #     connection_socket.send(cmsg.encode())
    # elif x[0] == "guesspass":
    #     actual_password = str(query_user(x[1])['info']['password'])
    #     if x[2] == actual_password:
    #         cmsg = "Correct!"
    #     else:
    #         cmsg = "Wrong!"
    #     connection_socket.send(cmsg.encode())
    # elif x[0] == "updatepass":
    #     update_password(x[1], x[2], x[3])
    #     cmsg = "updated password!"
    #     connection_socket.send(cmsg.encode())