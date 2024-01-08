from path_scanner import default_scanner, get_database_path
from logging.handlers import RotatingFileHandler
import logging
import os

def init():
    global osu_folder, database, GENERAL_KEYS, METADATA_KEYS, EVENTS_KEYS
    GENERAL_KEYS = "AudioFilename"
    METADATA_KEYS = ["Title", "TitleUnicode", "Artist", "ArtistUnicode", 
                    "Creator", "Version", "Source", "Tags", "BeatmapID", "BeatmapSetID"]
    EVENTS_KEYS = "BackgroundFilename"
    osu_folder = default_scanner()
    database = get_database_path()

    log_formatter = logging.Formatter('%(asctime)s %(levelname)s %(funcName)s(%(lineno)d) %(message)s')
    logFile = os.path.join(os.getcwd(), 'log')
    handler = RotatingFileHandler(logFile, mode='w', maxBytes=50*1024, 
                                  encoding='utf-8', delay=0)
    handler.setFormatter(log_formatter)
    handler.setLevel(logging.INFO)

    app_log = logging.getLogger('root')
    app_log.setLevel(logging.INFO)
    app_log.addHandler(handler)