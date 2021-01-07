import json
import boto3
import os
from datetime import datetime
from services import users_service, tracks_service
from boto3.dynamodb.conditions import Key

usersService = users_service.UsersService()
tracksService = tracks_service.TracksService()


def users(event, context):
    usersService.getUsers(1)


def reproductions(event, context):
    userId = event['pathParameters']['userId']
    lastRep = 0

    if bool(event['queryStringParameters']) and 'last' in event['queryStringParameters']:
        lastRep = int(event['queryStringParameters']['last'])

    reproductions = usersService.getReproductions(userId, lastRep)

    print('*****')

    return {
        "statusCode": 200,
        "body": json.dumps({
            'count': len(reproductions),
            'reproductions': reproductions
        })
    }


def populate(event, context):
    friends = []
    discoveredUsers = 0

    # try:
    # for each friend, get the user info and last listened songs

    while discoveredUsers < 5:
        users = usersService.getBrazilianUsers()

        for user in users:
            userId = user['id']
            print(f'Getting {userId} data...')
            userData = usersService.getInfo(userId)
            print(f'Getting {userId} tracks...')
            days = usersService.getYearReproductions(userId)
            if(userData != None and days != None):
                print(f'Getting track tags...')
                for day in days:
                    data = {
                        'user_id': userData['id'],
                        'user': userData,
                        'date': day['day'],
                        'reproductions': day['reproductions'],
                        'created_at': datetime.today().strftime(
                            '%Y-%m-%d %H:%M:%S.%f')
                    }
                    usersService.save(data)
                discoveredUsers += 1
    # except:
    #     print('**Error**')

    response = {
        "statusCode": 200,
        "body": json.dumps(friends)
    }

    return response
