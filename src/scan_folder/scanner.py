import os
import logging
import glob
import settings
from db.error_enum import Error
from scan_folder.song_parser import song_parser
from db.db_operation import add_beatmap, create_connection

def _isclosed(conn) -> bool:
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

def scanner(songs_directory) -> Error:
    logging.info("----------------------------SCANNING START----------------------------")
    conn = create_connection(settings.database)
    if os.path.exists(songs_directory):
        for root, _, _ in os.walk(os.path.abspath(songs_directory)):
            files = glob.glob(os.path.join(root,"*.osu"))
            for file in files:
                with open(os.path.join(root, file), "r", encoding='utf-8-sig') as osu_file:
                    if _isclosed(conn):
                        logging.critical("An error occured during sql operation. Stopping scan process.")
                        return Error.SQL_ERROR
                    logging.debug("Reading " + file)
                    data = song_parser(osu_file, os.path.basename(root))
                    add_beatmap(conn, data)
    conn.cursor().execute("PRAGMA optimize")
    conn.close()
    logging.info("----------------------------SCANNING FINISHED----------------------------\n")
    return Error.SUCCESS