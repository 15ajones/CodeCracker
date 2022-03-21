import boto3
from boto3.dynamodb.conditions import Key

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
    delete_user_table()

if __name__ == "__main__":
    main()




