import sqlite3
import logging
from db.error_enum import Error
from db.sql_error import sql_error_handler

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except sqlite3.Error as e:
        sql_error_handler(e, "Failed to create a connection to the file: " + db_file)
    
    return conn

def create_cursor(conn):
    """
    Helper function to create a cursor to a valid connection
    """
    try:
        cursor = conn.cursor()
        #optimization
        pragma_statements = ["PRAGMA journal_mode = WAL",
                             "PRAGMA synchronous = normal"]
        for statement in pragma_statements:
            cursor.execute(statement)
    except sqlite3.Error as e:
        sql_error_handler(e, "Failed to established a cursor to the database.")
    
    return cursor

def add_beatmap(conn, data):
    logging.debug("Current data: " + data.__str__())
    try:
        cursor = conn.cursor()
        #optimization
        pragma_statements = ["PRAGMA journal_mode = WAL",
                             "PRAGMA synchronous = normal"]
        for statement in pragma_statements:
            cursor.execute(statement)
        insert = '''
                    INSERT INTO beatmaps VALUES 
                    (null, :BeatmapSetID, :BeatmapID, :Title, :TitleUnicode, :Artist, 
                    :ArtistUnicode, :Creator, :Version, :Source, :Tags, :AudioFilename, :BackgroundFilename, 0)
                '''
        
        cursor.execute(insert, data)
        conn.commit()
    except sqlite3.Error as e:
        sql_error_handler(e, "Failed to add beatmap to the database.\nData: " + data.__str__())
        conn.close()
    finally:
        cursor.close()

    return cursor.lastrowid
