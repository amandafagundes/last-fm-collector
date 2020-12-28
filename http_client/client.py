import requests
import os
import json

class HttpClient:

    BASE_URL = 'http://ws.audioscrobbler.com/2.0'

    def get(self, method, dicParams):

        params = ''

        for key in dicParams:
            params += key + '=' + str(dicParams[key]) + '&'

        r = requests.get(self.BASE_URL + '/?method=' + method +
                         '&' + params + 'api_key=' + os.getenv('LAST_FM_API_KEY') + '&format=json')

        return r.json()

