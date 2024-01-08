from pathlib import Path
import os

def default_scanner():
    """Scans the user from home directory to locate osu folder.

    NOTE: Run `path_scanner` instead if default location is not found.

    Returns: 
    `str`: path to the songs folder if exist, `None` otherwise
    """
    songs_directory = os.path.join(Path.home(), 'Appdata', 'Local', 'osu!', "Songs")
    if not os.path.exists(songs_directory):
        return None
    return songs_directory

def path_scanner(osu_path: str):
    """function to check if a given folder directory contains "Songs" folder

    NOTE: does not check if it is a valid osu folder or if the songs folder is invalid

    Parameters:
    `osu_path` (str): path to the folder containing `Songs` folder

    Returns: 
    `str`: path to the songs folder if exist, `None` otherwise
    """
    songs_directory = os.path.join(osu_path, "Songs")
    if not os.path.exists(songs_directory):
        return None
    return songs_directory

def get_database_path():
    database = os.path.join(os.getcwd(), "beatmaps.sql")

    if os.path.exists(database):
        return database
    return None
    