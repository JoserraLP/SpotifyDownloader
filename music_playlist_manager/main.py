
from music_playlist_manager.user import SpotifyUser, YoutubeUser
from music_playlist_manager.manager import PlaylistManager
from music_playlist_manager.constants import DEFAULT_OUTPUT_DIR

spotify_user = SpotifyUser()
playlists = spotify_user.get_current_playlists()

youtube_user = YoutubeUser()
playlists = youtube_user.get_current_playlist()

downloader = PlaylistManager(playlists=playlists, output_dir=DEFAULT_OUTPUT_DIR)
downloader.download_playlists(source='youtube')
downloader.store_not_downloaded_tracks()
