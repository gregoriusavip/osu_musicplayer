from Error import Error
import sqlite3
import logging

# function to create the database for storing beatmaps information
def create_db():
    message = ""
    logging.info("Creating database...")
    try:
        db = sqlite3.connect("beatmaps.sql")
        db.execute("PRAGMA foreign_keys = 1")
        db_cur = db.cursor()

        logging.info("Removing and creating new beatmaps table...")
        message = "beatmaps table creation"
        db_cur.execute("DROP TABLE IF EXISTS beatmaps")

        """
        beatmapID: based of the id of the beatmap
        metadataVersion: the version of this beatmap metadata for parsing function
        HideSet: boolean to hide the set from display
        """
        table = """ CREATE TABLE beatmaps (
                    beatmapID INTEGER PRIMARY KEY UNIQUE,
                    metadataVersion INTEGER NOT NULL,
                    HideSet BOOLEAN NOT NULL CHECK (HideSet IN (0,1))
                ); """
        db_cur.execute(table)
        logging.info("Successfully created beatmaps table")

        logging.info("Removing and creating new beatmapInfo table...")
        message = "beatmapInfo table creation"
        db_cur.execute("DROP TABLE IF EXISTS beatmapInfo")
        
        table = """ CREATE TABLE beatmapInfo (
                    mainSetID INTEGER PRIMARY KEY UNIQUE,
                    beatmapSetID INTEGER UNIQUE,
                    beatmapID INTEGER,
                    Title TEXT NOT NULL,
                    Artist TEXT NOT NULL,
                    Creator TEXT NOT NULL,
                    Version TEXT NOT NULL,
                    Source TEXT,
                    Tags TEXT,
                    songLoc TEXT NOT NULL,
                    backgroundLoc TEXT,
                    HideSong BOOLEAN NOT NULL CHECK (HideSong IN (0,1)),
                    HideSet REFERENCES beatmaps(HideSet),
                    FOREIGN KEY(beatmapID) REFERENCES beatmaps(beatmapID)); """
        db_cur.execute(table)
        logging.info("Successfully created beatmapInfo table")

        message = "closing database cursor"
        db_cur.close()
        logging.info("Created database.")
        return Error.SUCCESS
    except sqlite3.Error as e:
        sql_error_handler(e, message)
        return Error.SQL_ERROR
    
def sql_error_handler(e, message):
    reason = "Task " + message + " could not be completed."
    logging.critical(reason)
    logging.error('Sql error: %s' % (' '.join(e.args)))
    logging.error("Exception class is: ", e.__class__)