# profiler for debugging
import cProfile

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

def display_songs(song_list):
    index = 0
    print("Title\t TitleUnicode\t Artist\t ArtistUnicode\t Mapper\t BeatmapSetID")
    for row in song_list:
        print(f"{row[0]}\t {row[1]}\t {row[2]}\t {row[3]}\t {row[4]}\t {row[5]}")
        index += 1
        if index == 50:
            break

def main():
    # initialized settings
    settings.init()
    logging.info("Starting application...\n")

    # if db does not exist, create the db
    if not database_exists():
        create_db()
        songs_directory = settings.OSU_FOLDER
        scanner(songs_directory)   # TODO: handle error
    data = query_beatmap("nakuru", "Title")
    display_songs(data)
    test()

if __name__ == '__main__':
    cProfile.run('main()', 'restats')
    logging.info("Quitting appliaction..." + "\n")