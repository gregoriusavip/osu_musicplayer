import settings
import logging
from path_scanner import database_exists
from db.create_db import create_db
from scan_folder.scanner import scanner
from db.db_operation import query_beatmap
import cProfile
from music_player.controller import test

def main():
    # initialized settings
    settings.init()
    logging.info("Starting application...\n")

    # if db does not exist, create the db
    if not database_exists():
        create_db()
        songs_directory = settings.OSU_FOLDER
        scanner(songs_directory)
    query_beatmap("Nakuru")
    test()

if __name__ == '__main__':
    cProfile.run('main()', 'restats')
    logging.info("Quitting appliaction..." + "\n")