import json
import boto3
import os
from datetime import datetime
from services import users_service, tracks_service
from boto3.dynamodb.conditions import Key

usersService = users_service.UsersService()
tracksService = tracks_service.TracksService()


def friends(event, context):
    friends = []

    userId = event['pathParameters']['userId']

    friendsIds = usersService.getFriendsIds(userId)

    for idMap in friendsIds:
        friendData = usersService.getInfo(idMap['name'])
        if friendData != None:
            friends.append(friendData)

    response = {
        "statusCode": 200,
        "body": json.dumps({
            'count': len(friends),
            'friends': friends
        })
    }

    return response


def populate(event, context):
    friends = []
    discoveredUsers = 0

    # try:
    # for each friend, get the user info and last listened songs

    while discoveredUsers < 5:
        users = usersService.getBrazilianUsers()

        for user in users:
            userId = user['user_id']
            print(f'Getting {userId} data...')
            userData = usersService.getInfo(userId)
            print(f'Getting {userId} tracks...')
            reproductions = usersService.getUserReproductions(userId)
            if(userData != None and reproductions != None):
                print(f'Getting track tags...')
                for reproduction in reproductions:
                        data = {
                            'user_id': userData['user_id'],
                            'reproduction': reproduction['reproduction'],
                            'tracks': reproduction['tracks'],
                            'created_at': datetime.today().strftime('%Y-%m-%d %H:%M:%S.%f')
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
