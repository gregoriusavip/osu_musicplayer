import sqlite3
import logging
import settings
from db.error_enum import Error
from error_handler import error_handler

def create_db():
    """
    function to create the database for storing beatmaps information.

    :return: enum Error flag. `Error.SUCCESS` if no error occurred, `Error.SQL_ERROR` otherwise.
    """
    message = ""
    ret = Error.SUCCESS # return flag
    logging.info("Creating database...")
    try:
        db = sqlite3.connect(settings.DATABASE_NAME)
        db_cur = db.cursor()

        logging.info("Removing and creating new beatmaps table...")
        message = "Table creation"
        db_cur.execute("DROP TABLE IF EXISTS beatmaps")
        
        table = """ CREATE TABLE beatmaps (
                    MainID INTEGER PRIMARY KEY,
                    BeatmapSetID INTEGER,
                    BeatmapID INTEGER,
                    Title TEXT,
                    TitleUnicode TEXT,
                    Artist TEXT,
                    ArtistUnicode TEXT,
                    Creator TEXT,
                    Version TEXT,
                    Source TEXT,
                    Tags TEXT,
                    AudioFilename TEXT NOT NULL,
                    BackgroundFilename TEXT,
                    HideSong BOOLEAN NOT NULL CHECK (HideSong IN (0,1))); """
        
        db_cur.execute(table)
        logging.info("Successfully created beatmapInfo table")
        logging.info("Created database.\n")
    except sqlite3.Error as e:
        error_handler(e, message)
        ret = Error.SQL_ERROR
    finally:
        db_cur.close()
        db.close()
    
    return ret