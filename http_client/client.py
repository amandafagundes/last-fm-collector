import urllib3
import os
import json


class HttpClient:

    http = urllib3.PoolManager()

    BASE_URL = 'http://ws.audioscrobbler.com/2.0'

    def get(self, method, dicParams):

        params = ''

        for key in dicParams:
            params += key + '=' + str(dicParams[key]) + '&'

        r = self.http.request('GET', self.BASE_URL + '/?method=' + method +
                              '&' + params + 'api_key=' + os.getenv('LAST_FM_API_KEY') + '&format=json')

        if r == None:
            raise Exception('Last.fm empty response')

        return json.loads(r.data.decode('utf8'))
