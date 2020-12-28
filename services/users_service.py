from http_client import client


class UsersService:

    httpClient = client.HttpClient()

    def getFriendsIds(self, userId):
        response = self.httpClient.get(
            'user.getfriends', {'user': userId, 'limit': 10})

        rawFriends = response['friends']['user']

        friends = []

        for rawFriend in rawFriends:
            friends.append(
                {key: value for key, value in rawFriend.items() if key in ['name']})

        return friends

    def getInfo(self, userId):
        response = self.httpClient.get('user.getinfo', {'user': userId})

        userInfo = response['user']

        return {key: value for key, value in userInfo.items() if key in ['name', 'playlists', 'playcount', 'gender', 'country', 'type', 'age']}
