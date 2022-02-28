from lib2to3.pgen2.grammar import opmap_raw
from msilib.schema import AdminExecuteSequence
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

def add_user(user,ip,socket_addr,dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table('Users')
    response = table.put_item(
        Item={
            'User': user,
            'IP' : ip,
            'info': {
                'points': 0,
                'socket_addr': socket_addr
            }
        }
    )
    print("added user")
    return response

def update_points(user, IP, point):#pass param is the new password
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
    try:
        if not dynamodb:
            dynamodb = boto3.resource('dynamodb', region_name="us-east-1")

        table = dynamodb.Table('Users')
        print("deleted table")
        table.delete()
    except:
        print("no table to delete")


def main():
    print("Server has started running")
    delete_user_table()
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

    board1 = ('0.0.0.0', 11000)
    board2 = ('0.0.0.0', 12000)
    board3 = ('0.0.0.0', 13000)
    board4 = ('0.0.0.0', 14000)
    board5 = ('0.0.0.0', 15000)
    board6 = ('0.0.0.0', 16000)
    game_started = False
    players=[]
    number_players = 0
    while True:
        if not game_started:
            cmsg, cadd = server_socket.recvfrom(2048)
            cmsg = cmsg.decode()
            if cadd





#extra for tcp socket:

#ready message

#Now the loop that actually listens from clients

        
            
# to add a new device:
#     add player1

# the first player to be added is going to be assigned admin 
#     start player1

# at each go, i receive a message asking if its my go
# i reply "y" if its your go, else "n". if the game has ended ill send game over winner: player1
# message will be: turn player1

# player whos turn it is guesses a go:
# guess LRLR player1









            
            
                


            
        
        
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