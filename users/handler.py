import json
from services import users_service

usersService = users_service.UsersService()

def friends(event, context):
    friends = []

    userId = event['pathParameters']['userId']

    friendsIds = usersService.getFriendsIds(userId)

    for idMap in friendsIds:
        friendData = usersService.getInfo(idMap['name'])
        friends.append(friendData)

    response = {
        "statusCode": 200,
        "body": json.dumps({
            'count': len(friends),
            'friends': friends
        })
    }
    
    return response

def info(event, context):

    userId = event['pathParameters']['userId']

    response = usersService.getInfo(userId)

    response = {
        "statusCode": 200,
        "body": json.dumps(response)
    }

    return response
