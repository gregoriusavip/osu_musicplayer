from pathlib import Path
import os

def default_scanner():
    songs_directory = os.path.join(Path.home(), 'Appdata', 'Local', 'osu!', "Songs")
    if not os.path.exists(songs_directory):
        return None
    return songs_directory

def path_scanner(osu_path):
    songs_directory = os.path.join(osu_path, "Songs")
    if not os.path.exists(songs_directory):
        return None
    return songs_directory

