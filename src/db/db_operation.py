import sqlite3
import logging
import settings
from error_handler import error_handler
from db.error_enum import Error

def isclosed(conn) -> bool:
    """
    A private helper function to check if a connection is closed.

    :param `conn`: a valid connection to an sqlite3 database
    :return: `True` if try block catched an error when establishing cursor to database, `False` otherwise
    """
    try:
        conn.cursor()
        return False
    except Exception as _:
        return True

def create_connection():
    """
    Helper function to establish a connection to an sqlite3 db.
    The name of the database is established on settings.

    :return: a valid `sqlite3.connect()` if file is successfully connected, `None` otherwise.
    """
    conn = None
    try:
        conn = sqlite3.connect(settings.DATABASE_NAME)
    except sqlite3.Error as e:
        error_handler(e, "Connect to an sqlite3 db named " + settings.DATABASE_NAME)
    
    return conn

def create_cursor(conn):
    """
    Helper function to create a cursor to a valid connection 
    with a preconfig settings for optimization.

    :param `conn`: Valid connection to a database
    :return: an sqlite3 `cursor()` on a valid database, `None` otherwise
    """
    cursor = None
    try:
        cursor = conn.cursor()
        #optimization
        pragma_statements = ["PRAGMA journal_mode = WAL",
                             "PRAGMA synchronous = normal"]
        for statement in pragma_statements:
            cursor.execute(statement)
    except sqlite3.Error as e:
        # Close the connection if an error occurred
        error_handler(e, "Establish a cursor for the database.")
        conn.close()
    
    return cursor

def add_beatmap(conn, beatmapInfo) -> Error:
    """
    function to add a beatmap info to the database.
    Cursor to the database will be closed after the operation.
    Connection will ONLY be closed if an error occured during data insertion.
    Therefore, connection should be closed if there is no longer operation
    outside of this function.

    :param1 `conn`: connection to a valid database
    :param2 `beatmapInfo`: a dictionary generated from `song_parser.song_parser()`

    :return: enum Error flag. `Error.SUCCESS` if no error occurred, `Error.SQL_ERROR` otherwise.

    """
    ret = Error.SUCCESS # return flag
    logging.debug("Current data: " + beatmapInfo.__str__())
    cursor = create_cursor(conn)
    try:        
        insert = '''
                    INSERT INTO beatmaps VALUES 
                    (null, :BeatmapSetID, :BeatmapID, :Title, :TitleUnicode, :Artist, 
                    :ArtistUnicode, :Creator, :Version, :Source, :Tags, :AudioFilename, :BackgroundFilename, 0)
                '''
        cursor.execute(insert, beatmapInfo)
        conn.commit()
    except sqlite3.Error as e:
        #Close the connection if an error occured
        error_handler(e, "Failed to add beatmap to the database.\nData: " + beatmapInfo.__str__())
        ret = Error.SQL_ERROR
        conn.close()
    finally:
        #Always close the cursor
        cursor.close()

    return ret
