import settings
import logging
from path_scanner import path_scanner
from create_db import create_db
import song_parser

logging.basicConfig(format='%(asctime)s %(message)s', filename="debug.log", level=logging.DEBUG)

def main():
    settings.init()
    if not settings.osu_folder:
        logging.info("osu songs folder cannot be located.")
        path = "some_path"
        settings.osu_folder = path_scanner(path)
        
    create_db()

    from pathlib import Path
    import os
    songs_directory = os.path.join(Path.home(), 'Appdata', 'Local', 'osu!', "Songs", "210 Taiko no Tatsujin - Saitama2000")
    song_parser.extract_beatmap_id(os.path.basename(songs_directory))

if __name__ == '__main__':
    logging.info("Starting application...")
    main()
    logging.info("Quitting appliaction...\n")