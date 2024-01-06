import settings
import logging
from path_scanner import path_scanner
from db.create_db import create_db
from scan_folder.scanner import scanner
from pathlib import Path
import os
import cProfile

def main():
    settings.init()
    logging.info("Starting application...")
    logging.info("Settings initialized\n")
    if not settings.osu_folder:
        logging.info("osu songs folder cannot be located.")
        path = "some_path"
        settings.osu_folder = path_scanner(path)
        
    create_db()
    songs_directory = os.path.join(Path.home(), 'Appdata', 'Local', 'osu!', "Songs")
    scanner(songs_directory)

if __name__ == '__main__':
    cProfile.run('main()', 'restats')
    logging.info("Quitting appliaction..." + "\n")