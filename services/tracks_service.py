from http_client import client
from dateutil.relativedelta import relativedelta
from datetime import datetime
from services.spotipy_service import SpotipyService
import traceback
import math
class TracksService:

    httpClient = client.HttpClient()

    spotipyService = SpotipyService()

    def getInfo(self, artist, track):
        print('Getting track info...')
        try:
            trackInfo = None
            response = self.httpClient.get(
                'track.getinfo', {'artist': artist, 'track': track, 'autocorrect': 1})

            if 'track' in response:
                rawInfo = response['track']

                trackInfo = {
                    'duration': int(rawInfo['duration']),
                    'listeners': int(rawInfo['listeners']),
                    'playcount': int(rawInfo['playcount']),
                }

                if len(rawInfo['toptags']['tag']) > 0:
                    trackInfo['tags'] = []
                    for tag in rawInfo['toptags']['tag']:
                        trackInfo['tags'].append(tag['name'])
                
            genres = self.spotipyService.getArtistGenres(artist)
            release_date = self.spotipyService.getTrackReleaseDate(track)
            print('****** ', release_date)
            trackInfo['genres'] = genres
            trackInfo['release_date'] = release_date
            
            return trackInfo
        except Exception:
            traceback.print_exc()
            return None
