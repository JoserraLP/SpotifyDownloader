
from music_playlist_manager.user import SpotifyUser
from music_playlist_manager.manager import PlaylistManager

spotify_user = SpotifyUser()
playlists = spotify_user.get_current_playlists()

downloader = PlaylistManager(playlists=playlists, output_dir='../Test')
# downloader.download_playlists()
downloader.store_not_downloaded_tracks()







