import json
import os
import boto3
from datetime import datetime
from services import users_service, tracks_service
from boto3.dynamodb.conditions import Key

usersService = users_service.UsersService()
tracksService = tracks_service.TracksService()


def users(event, context):
    users = usersService.getUsers(1)
    
    return {
        "statusCode": 200,
        "body": json.dumps({
            'count': len(users),
            'users': users
        })
    }


def reproductions(event, context):
    userId = event['pathParameters']['userId']
    lastRep = 0

    if bool(event['queryStringParameters']) and 'last' in event['queryStringParameters']:
        lastRep = int(event['queryStringParameters']['last'])

    reproductions = usersService.getReproductions(userId, lastRep)

    return {
        "statusCode": 200,
        "body": json.dumps({
            'count': len(reproductions),
            'reproductions': reproductions
        })
    }


def populate(event, context):
    discoveredUsers = 0

    while discoveredUsers < 5:
        users = usersService.getBrazilianUsers()

        for user in users:
            userId = user['id']
            print(f'Getting {userId} data...')
            userData = usersService.getInfo(userId)
            print(f'Getting {userId} total tracks...')
            totalTracks = usersService.getUserTotalTracks(userId)
            print(f'Getting {userId} tracks...')
            days = usersService.getYearReproductions(userId,totalTracks)
            if(userData != None and days != None):
                userData['total_tracks'] = totalTracks
                print(f'Getting track tags...')
                date_count = 0
                for day in days:
                    data = {
                        'user_id': userData['id'],
                        'user': userData,
                        'date': day['day'],
                        'date_count': date_count,
                        'reproductions': day['reproductions'],
                        'created_at': datetime.today().strftime(
                            '%Y-%m-%d %H:%M:%S.%f')
                    }
                    usersService.save(data)
                    date_count += 1
                discoveredUsers += 1
                
    response = {
        "statusCode": 200,
        "body": json.dumps(days)
    }

    return response
