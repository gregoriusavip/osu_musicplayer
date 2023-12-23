from pathlib import Path
import os

"""
scans the user from home directory to locate osu folder
default scanner to locate the osu folder. 
run path_scanner instead if default location is not found

@return: path to the songs folder if exist, None otherwise
"""
def default_scanner():
    songs_directory = os.path.join(Path.home(), 'Appdata', 'Local', 'osu!', "Songs")
    if not os.path.exists(songs_directory):
        return None
    return songs_directory

"""
function to check if a given folder directory contains "Songs" folder
NOTE: does not check if it is a valid osu folder or if the songs folder is invalid

@return: path to the songs folder if exist, None otherwise
"""
def path_scanner(osu_path):
    songs_directory = os.path.join(osu_path, "Songs")
    if not os.path.exists(songs_directory):
        return None
    return songs_directory

