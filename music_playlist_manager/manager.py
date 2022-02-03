import os
import subprocess
from os import listdir
from os.path import isfile, join

import eyed3
import pandas as pd


class PlaylistManager:
    """
    Playlist manager class
    """

    def __init__(self, playlists: list, output_dir: str):
        """
        PlaylistManager initializer.

        :param playlists: list with the playlists and its related information.
        :type playlists: list
        :param output_dir: output directory where the songs will be stored
        :type output_dir: str
        """
        self._output_dir = output_dir
        self._playlists = playlists

    def download_playlists(self, source: str):
        """
        Use the "spotdl" o "yt-dlp" library to download each one of the playlists.

        :param source: Source of the playlists. Can be 'spotify' or 'youtube'.
        :type source: str

        :return: None
        """
        # Set the working directory to the output directory
        base_dir = os.path.join(os.getcwd(), self._output_dir, "")
        os.chdir(base_dir)

        # Iterate over the different playlists
        for playlist in self._playlists:
            # Retrieve the playlist name
            playlist_dir = base_dir + playlist['name']
            # If the playlist folder does not exist, create it
            if not os.path.isdir(playlist_dir):
                os.makedirs(playlist_dir)
            # Change current directory to the playlist folder
            os.chdir(playlist_dir)

            if source == 'spotify':
                # Execute spotdl script
                subprocess.call(["spotdl", playlist['url']])
            elif source == 'youtube':
                # Execute yt-dlp script
                subprocess.call(["yt-dlp", "-x", "--audio-format", "mp3", "-o", playlist_dir+"/%(title)s.%(ext)s",
                                 "--no-part", "--embed-metadata", playlist['url']])

    def store_not_downloaded_tracks(self):
        """
        Process the songs that are not found and store its info into a given file.

        :return: None
        """

        # Set the working directory to the output directory
        base_dir = self._output_dir + '/'
        os.chdir(base_dir)
        # Create list for the unprocessed tracks
        not_downloaded_tracks = list()
        # Iterate over the playlists
        for playlist in self._playlists:
            # Create the playlist directory
            playlist_folder = './' + playlist['name']
            # If the folder exists
            if os.path.exists(playlist_folder):
                # Iterate over the playlist tracks
                for playlist_track in playlist['tracks']:
                    # Flag to check if the value exists
                    existing = False
                    # Iterate over those files that are .mp3
                    for file in [f for f in listdir(playlist_folder) if
                                 isfile(join(playlist_folder, f)) and f.endswith('.mp3')]:
                        # Load metadata from the mp3 file
                        track = eyed3.load(join(playlist_folder, file))
                        # If the track name is in the playlist tracks
                        if track.tag.title in playlist_track['name']:
                            existing = True
                    # If the track is not found on the folder
                    if not existing:
                        # Store its artist, name and playlist it belongs to
                        not_found_track = {key: playlist_track.get(key) for key in ['artists', 'name']}
                        not_found_track['playlist'] = playlist['name']

                        # Append track artists and name
                        not_downloaded_tracks.append(not_found_track)

        # Create a DataFrame with the info
        not_downloaded_tracks = pd.DataFrame(not_downloaded_tracks)

        # Reverse the order columns
        not_downloaded_tracks = not_downloaded_tracks[not_downloaded_tracks.columns.tolist()[::-1]]

        # Store the DataFrame
        not_downloaded_tracks.to_csv('./not_found.csv')
