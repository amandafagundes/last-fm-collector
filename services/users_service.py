from http_client import client
from dateutil.relativedelta import relativedelta
from datetime import datetime
from services import tracks_service
import math
from db import database
from models.reproduction import Reproduction
database = database.Database()
tracksService = tracks_service.TracksService()


class UsersService:

    httpClient = client.HttpClient()

    def getReproductions(self, userId, lastRep = 0):
        reproductions = []
        try:
            print(f'Getting reproductions starting from {lastRep}')
            result = Reproduction.query(userId, Reproduction.reproduction > lastRep, limit=100)
            for rep in result:
                print('.')
                reproductions.append(rep.to_dict()) 
        except Reproduction.DoesNotExist:
            print('****DoesNotExist****')
        return reproductions

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

    def getUserTotalTracks(self, userId):
        print('Getting user last song info...')

        lastSongInfo = self.httpClient.get(
            'user.getrecenttracks',
            {'user': userId, 'page': 1, 'limit': 1, 'from': 1577836799, 'to': 1609459199})

        if('error' in lastSongInfo):
            print('*Last.fm API Error: ', lastSongInfo['error'])
            return 0

        totalTracks = int(lastSongInfo['recenttracks']['@attr']['total'])

        # if the user has listened less than 2000 tracks
        if totalTracks < 2000:
            print('~> USELESS: User didin\'t hear enough songs!')
            return 0

        if totalTracks > 10000:
            print('~> USELESS: Too many songs!')
            return 0

        print('Getting user first song info...')
        firstSongInfo = self.httpClient.get(
            'user.getrecenttracks',
            {'user': userId, 'page': totalTracks, 'limit': 1, 'from': 1577836799, 'to': 1609459199})

        firstSongDate = datetime.fromtimestamp(
            int(firstSongInfo['recenttracks']['track'][0]['date']['uts']))
        lastSongDate = datetime.fromtimestamp(
            int(lastSongInfo['recenttracks']['track'][0]['date']['uts']))

        if(lastSongDate.month - firstSongDate.month < 10):
            print('~> USELESS: Less than 10 months of music!')
            return 0

        return totalTracks

    # collect the tracks of users that listened at least 2000 songs
    def getUserReproductions(self, userId):
        reproductions = []
        tracks = []
        try:

            totalTracks = self.getUserTotalTracks(userId)

            pages = math.ceil(totalTracks/1000)

            previousTrack = {}
            print(f'Iterating over {pages} pages...')
            for page in range(pages):

                print(f'Getting tracks from page {page}...')
                songInfo = self.httpClient.get(
                    'user.getrecenttracks',
                    {'user': userId, 'page': page + 1, 'limit': 1000})

                for track in songInfo['recenttracks']['track']:
                    # print('Converting track...')
                    newTrack = {
                        'total_tracks': totalTracks,
                        'artist_id': track['artist']['mbid'],
                        'artist_name': track['artist']['#text'],
                        'album_id': track['album']['mbid'],
                        'album_name': track['album']['#text'],
                        'playback_date': datetime.fromtimestamp(int(track['date']['uts'])).strftime('%Y-%m-%d %H:%M:%S.%f'),
                        'name': track['name'],
                        'id': track['mbid'],
                    }

                    trackData = tracksService.getInfo(
                        newTrack['artist_name'], track['name'])

                    newTrack.update(trackData)

                    if not previousTrack:
                        newTrack['reproduction'] = 0
                    else:
                        previousTrackDate = datetime.fromisoformat(
                            previousTrack['playback_date'])
                        trackDate = datetime.fromisoformat(
                            newTrack['playback_date'])

                        if abs(relativedelta(previousTrackDate, trackDate).hours) >= 1:
                            newTrack['reproduction'] = previousTrack['reproduction'] + 1
                        else:
                            newTrack['reproduction'] = previousTrack['reproduction']

                        if(previousTrack['reproduction'] != newTrack['reproduction']):
                            reproductions.append({
                                'reproduction': newTrack['reproduction']-1,
                                'tracks': tracks})
                            tracks = []

                    tracks.append(newTrack)
                    previousTrack = newTrack
        except KeyError as e:
            print('*KeyError: ', e)

        except Exception as e:
            print('*Exception: ', e)

        return reproductions

    def save(self, user):
        database.save(user)
