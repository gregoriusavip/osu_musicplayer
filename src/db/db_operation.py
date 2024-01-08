import sqlite3
import logging
from db.sql_error import sql_error_handler

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except sqlite3.Error as e:
        sql_error_handler(e, "Failed to create a connection to the file: " + db_file)
    
    return conn

def add_beatmap(conn, data):
    logging.debug("Current data: " + data.__str__())
    try:
        cursor = conn.cursor()
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
