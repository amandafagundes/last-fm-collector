from http_client import client
from dateutil.relativedelta import relativedelta
from datetime import datetime
import math


class TracksService:

    httpClient = client.HttpClient()

    def getInfo(self, artist, track):
        try:
            trackInfo = None
            response = self.httpClient.get(
                'track.getinfo', {'artist': artist, 'track': track, 'autocorrect': 1})

            if 'track' in response:
                rawInfo = response['track']

                trackInfo = {
                    'duration': rawInfo['duration'],
                    'listeners': rawInfo['listeners'],
                    'playcount': rawInfo['playcount'],
                }

                if len(rawInfo['toptags']['tag']) > 0:
                    trackInfo['tags'] = []
                    for tag in rawInfo['toptags']['tag']:
                        trackInfo['tags'].append(tag['name'])
            return trackInfo
        except Exception:
            return None
