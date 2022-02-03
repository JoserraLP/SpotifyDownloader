from music_playlist_manager.user import SpotifyUser, YoutubeUser
from music_playlist_manager.manager import PlaylistManager
from music_playlist_manager.constants import DEFAULT_OUTPUT_DIR, DEFAULT_USERNAME

import optparse


def get_options():
    """
    Define options for the executable script.
    :return: options
    :rtype: object
    """
    optParser = optparse.OptionParser()

    # Dataset generation group
    playlist_group = optparse.OptionGroup(optParser, "Playlist manager options", "Playlist tools")
    playlist_group.add_option("-s", "--spotify", action="store_true", dest="spotify",
                              help="flag to download from Youtube playlists. Default is False. "
                                   "Cannot be used with 'youtube' option.")
    playlist_group.add_option("-u", "--spotify-user", dest="spotify_user", default=DEFAULT_USERNAME,
                              help="Spotify user to download its playlists. Default user is 'joserralp'. "
                                   "Cannot be used with 'youtube' option.")
    playlist_group.add_option("-y", "--youtube", action="store_true", dest="youtube",
                              help="flag to download from Youtube playlists. Default is False. "
                                   "Cannot be used with 'spotify' option.")
    playlist_group.add_option("-o", "--output-dir", dest="output_dir", action="store", default=DEFAULT_OUTPUT_DIR,
                              help="output directory where the playlists will be downloaded")
    optParser.add_option_group(playlist_group)

    options, args = optParser.parse_args()
    return options


if __name__ == "__main__":

    # Retrieve execution options (parameters)
    exec_options = get_options()

    if exec_options.spotify and exec_options.youtube:
        print("Error, both sources can not be used together")
        exit(-1)

    if not exec_options.youtube and ((not exec_options.spotify and exec_options.spotify_user) or
                                     (exec_options.spotify and not exec_options.spotify_user)):
        print("Error, 'spotify' flag must be used with the user")
        exit(-1)

    playlists = list()

    if exec_options.spotify:
        spotify_user = SpotifyUser(username=exec_options.spotify_user)
        playlists = spotify_user.get_current_playlists()
        source = 'spotify'

    if exec_options.youtube:
        youtube_user = YoutubeUser()
        playlists = youtube_user.get_current_playlist()
        source = 'youtube'

    downloader = PlaylistManager(playlists=playlists, output_dir=exec_options.output_dir)
    downloader.download_playlists(source=source)
    downloader.store_not_downloaded_tracks()
