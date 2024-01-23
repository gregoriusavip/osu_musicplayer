import settings
import os

def path_scanner(osu_path: str):
    """
    function to check if a given folder directory contains "Songs" folder

    NOTE: does not check if it is a valid osu folder or if the songs folder is invalid

    Parameters:
    `osu_path` (str): path to the folder containing `Songs` folder

    :return: `True` if path exists, `False` otherwise
    """
    songs_directory = os.path.join(osu_path, "Songs")
    return os.path.exists(songs_directory)

def database_exists():
    """
    helper function to check if a database exist in the current working directory.

    :return: `True` if the database exist, `False` otherwise.
    """

    database = os.path.join(os.getcwd(), settings.DATABASE_NAME)

    if os.path.exists(database):
        return True
    return False
    