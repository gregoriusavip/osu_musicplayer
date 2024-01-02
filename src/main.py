import settings
import logging
from path_scanner import path_scanner
from create_db import create_db
from scan_folder.scanner import scanner
from pathlib import Path
import os
import cProfile

def main():
    settings.init()
    if not settings.osu_folder:
        logging.info("osu songs folder cannot be located.")
        path = "some_path"
        settings.osu_folder = path_scanner(path)
        
    create_db()
    songs_directory = os.path.join(Path.home(), 'Appdata', 'Local', 'osu!', "Songs")
    scanner(songs_directory)

if __name__ == '__main__':
    logging.info("Starting application...")
    cProfile.run('main()', 'restats', sort='tottime')
    logging.info("Quitting appliaction...")