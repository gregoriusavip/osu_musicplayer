from db.error_enum import Error
import sqlite3
import logging
from db.sql_error import sql_error_handler

# function to create the database for storing beatmaps information
def create_db() -> Error:
    message = ""
    logging.info("Creating database...")
    try:
        db = sqlite3.connect("beatmaps.sql")
        db_cur = db.cursor()

        logging.info("Removing and creating new beatmaps table...")
        message = "beatmaps table creation"
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

        message = "closing database cursor"
        db_cur.close()
        logging.info("Created database.\n")
        return Error.SUCCESS
    except sqlite3.Error as e:
        sql_error_handler(e, message)
        return Error.SQL_ERROR
    
