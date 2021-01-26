from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
from datetime import datetime


class SpotipyService:

    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=os.getenv('SPOTIFY_CLIENT'),
                                                               client_secret=os.getenv('SPOTIFY_SECRET')))

os.getenv('LAST_FM_API_KEY')
    def getArtistGenres(self, artist):
        print(f'Getting {artist} genres from Spotify...')
        genres = []
        results = self.sp.search(artist, type='artist', limit=1)

        for genre in results['artists']['items'][0]['genres']:
            genres.append(genre)

        return genres

    def getTrackReleaseDate(self, track):
        print('Getting track release date from Spotify...')
        result = self.sp.search(track, type='track', limit=1)

        album = result['tracks']['items'][0]['album']
        release_date = {
            'date': album['release_date'],
            'precision': album['release_date_precision']
        }

        return release_date
