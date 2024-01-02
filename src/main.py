import settings
import logging
from path_scanner import path_scanner
from create_db import create_db
from scan_folder.scanner import scanner
from logging.handlers import RotatingFileHandler
from pathlib import Path
import os

log_formatter = logging.Formatter('%(asctime)s %(levelname)s %(funcName)s(%(lineno)d) %(message)s')
logFile = os.path.join(os.getcwd(), 'log')
handler = RotatingFileHandler(logFile, mode='w', maxBytes=5*1024*1024, 
                              backupCount=2, encoding='utf-8', delay=0)
handler.setFormatter(log_formatter)
handler.setLevel(logging.DEBUG)

app_log = logging.getLogger('root')
app_log.setLevel(logging.DEBUG)
app_log.addHandler(handler)

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
    main()
    logging.info("Quitting appliaction...")