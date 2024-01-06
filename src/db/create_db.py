from db.Error import Error
import sqlite3
import logging
from db.sql_error import sql_error_handler

# function to create the database for storing beatmaps information
def create_db() -> Error:
    message = ""
    logging.info("Creating database...")
    try:
        db = sqlite3.connect("beatmaps.sql")
        db.execute("PRAGMA foreign_keys = 1")
        db_cur = db.cursor()

        logging.info("Removing and creating new Beatmaps table...")
        message = "Beatmaps table creation"
        db_cur.execute("DROP TABLE IF EXISTS Beatmaps")

        """
        BeatmapID: Integer ID of the beatmap
        HideSet: boolean to hide the set from display
        """
        table = """ CREATE TABLE Beatmaps (
                    BeatmapID INTEGER PRIMARY KEY UNIQUE,
                    HideSet BOOLEAN NOT NULL CHECK (HideSet IN (0,1))
                ); """
        
        db_cur.execute(table)
        logging.info("Successfully created Beatmaps table")

        logging.info("Removing and creating new BeatmapInfo table...")
        message = "beatmapInfo table creation"
        db_cur.execute("DROP TABLE IF EXISTS BeatmapInfo")
        
        table = """ CREATE TABLE BeatmapInfo (
                    MainID INTEGER PRIMARY KEY UNIQUE,
                    BeatmapSetID INTEGER UNIQUE,
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
                    HideSong BOOLEAN NOT NULL CHECK (HideSong IN (0,1)),
                    HideSet REFERENCES beatmaps(HideSet),
                    FOREIGN KEY(BeatmapID) REFERENCES beatmaps(BeatmapID)); """
        db_cur.execute(table)
        logging.info("Successfully created beatmapInfo table")

        message = "closing database cursor"
        db_cur.close()
        logging.info("Created database.")
        return Error.SUCCESS
    except sqlite3.Error as e:
        sql_error_handler(e, message)
        return Error.SQL_ERROR
    
