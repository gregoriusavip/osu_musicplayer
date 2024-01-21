# timer/profiler for debugging
import cProfile
import timeit
from functools import partial

# settings and logging
import settings
import logging

# database/scanner functions
from path_scanner import database_exists
from db.create_db import create_db
from db.db_operation import query_beatmap, default_select
from scan_folder.scanner import scanner

# music player functionality
from music_player.controller import test

def main():
    # initialized settings
    settings.init()
    logging.info("Starting application...\n")

    # if db does not exist, create the db
    if not database_exists():
        create_db()
        songs_directory = settings.OSU_FOLDER
        scanner(songs_directory)   # TODO: handle error
    partial_function = partial(query_beatmap, user_query="nakuru", sort_by="Title")
    execution_time = timeit.timeit(partial_function, number=1)
    print(f"Execution time: {execution_time} seconds")
    test()

if __name__ == '__main__':
    cProfile.run('main()', 'restats')
    logging.info("Quitting appliaction..." + "\n")