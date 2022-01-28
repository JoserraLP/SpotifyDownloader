from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.client import Spotify

from music_playlist_manager.secrets import SPOTIPY_CLIENT_SECRET, SPOTIPY_CLIENT_ID
from music_playlist_manager.constants import DEFAULT_USERNAME


class SpotifyUser:
    """
    Spotify user class
    """

    def __init__(self, username: str = DEFAULT_USERNAME):
        """
        SpotifyUser initializer. Connect to Spotify API.

        :param username: Spotify username. Default to 'joserralp'
        :type username: str
        """
        # Store username
        self._username = username
        # Auth with Spotipy
        auth_manager = SpotifyClientCredentials(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET)
        # Create Spotify instance
        self._sp = Spotify(auth_manager=auth_manager)

    def get_current_playlists(self):
        """
        Get playlists from the current Spotify user.

        :return: list with playlist info
        """
        # Intilialize playlists list
        playlists = list()

        # Retrieve user playlists
        user_playlists = self._sp.user_playlists(self._username)
        # Iterate over the playlists
        for user_playlist in user_playlists['items']:
            playlist_tracks = []
            # Get playlist tracks
            tracks_info = self._sp.playlist(user_playlist['id'], fields=('tracks',))['tracks']
            # Iterate over the tracks in order to store its artists, name, release date and duration
            for _, item in enumerate(tracks_info['items']):
                # Get current track
                track = item['track']
                # Append data
                playlist_tracks.append({
                    'artists': [artist['name'] for artist in track['artists']],
                    'name': track['name'],
                    'release_date': track['album']['release_date'],
                    'duration': track['duration_ms'] / 1000
                })

            # Store the playlist info such as the name, url and its tracks
            playlists.append({
                'url': user_playlist['external_urls']['spotify'],
                'name': user_playlist['name'],
                'tracks': playlist_tracks
            })

        return playlists
