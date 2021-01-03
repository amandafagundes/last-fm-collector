from http_client import client
from dateutil.relativedelta import relativedelta
from datetime import datetime
import math
from db import database

database = database.Database()


class UsersService:

    httpClient = client.HttpClient()

    def getFriendsIds(self, userId):
        try:
            friends = []
            response = self.httpClient.get(
                'user.getfriends', {'user': userId, 'limit': 20})

            rawFriends = response['friends']['user']

            for rawFriend in rawFriends:
                friends.append({'user_id': rawFriend['name']})

            return friends
        except Exception as e:
            print('****** 1', e)
            return []

    def getInfo(self, userId):
        try:
            response = self.httpClient.get('user.getinfo', {'user': userId})

            userInfo = response['user']

            return {
                'user_id': userInfo['name'],
                'user_playlists': userInfo['playlists'],
                'user_playcount': userInfo['playcount'],
                'user_gender': userInfo['gender'],
                'user_country': userInfo['country'],
                'user_type': userInfo['type'],
                'user_age': userInfo['age'],
            }

        except Exception:
            return None

    def getBrazilianUsers(self):
        brazilianUsers = []
        exploredFriendsIds = []
        # get last created user ID
        createdUsers = database.getUsersId()

        if(len(createdUsers) == 0):
            lastUserId = 'peedroohee'
        else:
            lastUserId = sorted(createdUsers, key=lambda k: k['created_at'])[
                len(createdUsers)-1]['user_id']

        index = 0
        while len(brazilianUsers) < 20:

            print(f'Getting {lastUserId} friends...')
            lastUserFriendsIds = self.getFriendsIds(lastUserId)

            for idMap in lastUserFriendsIds:

                # print('Checking if user was already explored...')
                if idMap['user_id'] not in exploredFriendsIds:

                    # print('Getting user data...')
                    friendData = self.getInfo(idMap['user_id'])
                    if(friendData != None and friendData['user_country'] == 'Brazil'):
                        print('YAY! It\'s brazilian')
                        brazilianUsers.append(friendData)

            lastUserId = brazilianUsers[index]['user_id']
            index += 1

        return brazilianUsers

    # collect the tracks of users that listened at least 2000 songs
    def getLastTracks(self, userId):
        tracks = []
        try:
            tracksLimit = 2000

            # print('Getting user last song info...')
            lastSongInfo = self.httpClient.get(
                'user.getrecenttracks',
                {'user': userId, 'page': 1, 'limit': 1})

            if('error' in lastSongInfo):
                print('*Last.fm API Error: ', lastSongInfo['error'])
                return None

            totalTracks = int(lastSongInfo['recenttracks']['@attr']['total'])

            # if the user has listened less than 2000 tracks
            if totalTracks < 2000:
                print('~> USELESS: User didin\'t hear enough songs!')
                return None

            while tracksLimit < 12000 and tracksLimit <= totalTracks:
                # print(f'Getting {tracksLimit} listened track info...')
                firstSongInfo = self.httpClient.get(
                    'user.getrecenttracks',
                    {'user': userId, 'page': tracksLimit, 'limit': 1})

                firstSongDate = datetime.fromtimestamp(
                    int(firstSongInfo['recenttracks']['track'][0]['date']['uts']))
                lastSongDate = datetime.fromtimestamp(
                    int(lastSongInfo['recenttracks']['track'][0]['date']['uts']))

                if relativedelta(lastSongDate, firstSongDate).years >= 1:
                    break

                tracksLimit += 2000

            if relativedelta(lastSongDate, firstSongDate).years > 0:
                tracksPerDay = tracksLimit / \
                    (relativedelta(lastSongDate, firstSongDate).years*365)
            else:
                print('~> USELESS: Less than one year!')
                return None

            if(tracksLimit >= 12000 or relativedelta(lastSongDate, firstSongDate).years < 1 or tracksPerDay < 5):
                print('~> USELESS: The user heard over 10000 tracks in a year or didn\'t hear tracks enough!')
                return None

            pages = math.ceil(tracksLimit/1000)

            # print(f'Iterating over {pages} pages...')
            for page in range(pages):

                print(f'Getting tracks from page {page}...')
                songInfo = self.httpClient.get(
                    'user.getrecenttracks',
                    {'user': userId, 'page': page + 1, 'limit': 1000})
                for track in songInfo['recenttracks']['track']:
                    # print('Converting track...')
                    newTrack = {
                        'track_artist_id': track['artist']['mbid'],
                        'track_artist_name': track['artist']['#text'],
                        'track_album_id': track['album']['mbid'],
                        'track_album_name': track['album']['#text'],
                        'track_playback_date': datetime.fromtimestamp(int(track['date']['uts'])).strftime('%Y-%m-%d %H:%M:%S.%f'),
                        'track_name': track['name'],
                        'track_id': track['mbid'],
                    }
                    tracks.append(newTrack)
        except KeyError as e:
            print('*KeyError: ', e)

        except Exception as e:
            print('*Exception: ', e)

        return tracks

    def save(self, user):
        database.save(user)
