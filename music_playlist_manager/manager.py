from os import listdir

import spotdl
import os
import sys
import eyed3
import pandas as pd

from os.path import isfile, join


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

    def download_playlists(self):
        """
        Use the "spotdl" library to download each one of the playlists.

        :return: None
        """
        # Set the working directory to the output directory
        base_dir = self._output_dir + '/'
        os.chdir(base_dir)

        # Iterate over the different playlists
        for playlist in self._playlists:
            # Retrieve the playlist name
            playlist_dir = base_dir + playlist['name']
            # If the playlist folder does not exist, create it
            if not os.path.exists(playlist_dir):
                os.mkdir(playlist_dir)
            # Change current directory to the playlist folder
            os.chdir(playlist_dir)
            # Add the playlist URL to the execution of the spotdl script
            sys.argv += [playlist['url']]

            # Execute spotdl script
            spotdl.console_entry_point()

    def store_not_downloaded_tracks(self):
        """
        Process the songs that are not found and store its info into a given file.

        :return: None
        """

        # Set the working directory to the output directory
        base_dir = self._output_dir + '/'
        os.chdir(base_dir)
        # Create dict for the unprocessed tracks
        not_downloaded_tracks = dict()
        # Iterate over the playlists
        for playlist in self._playlists:
            # Initialize the list of not found tracks per playlist
            not_downloaded_tracks[playlist['name']] = list()
            # Create the playlist directory
            playlist_folder = base_dir + playlist['name']
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
                        # Append track artists and name
                        not_downloaded_tracks[playlist['name']].append(
                            {key: playlist_track.get(key) for key in ['artists', 'name']})

        # TODO process the csv file
        not_downloaded_tracks = pd.DataFrame.from_dict(not_downloaded_tracks, orient="index")
        not_downloaded_tracks.to_csv(base_dir+'not_found.csv')
