import settings
import logging
from path_scanner import path_scanner, database_exists
from db.create_db import create_db
from scan_folder.scanner import scanner
from pathlib import Path
import os
import cProfile

def main():
    # initialized settings
    settings.init()
    logging.info("Starting application...\n")

    # default osu path, handle path creation if default path is not valid
    settings.osu_folder = os.path.join(Path.home(), 'Appdata', 'Local', 'osu!')
    if not path_scanner(settings.osu_folder): #NOTE change to loop until valid path
        logging.info("osu songs folder cannot be located.")
        path = "some_path"  #NOTE ask user for the path
        settings.osu_folder = path
        # repeat

    # if db does not exist, create the db
    ## if not database_exists():
    create_db()
    songs_directory = os.path.join(settings.osu_folder, "Songs")
    scanner(songs_directory)

if __name__ == '__main__':
    cProfile.run('main()', 'restats')
    logging.info("Quitting appliaction..." + "\n")