import os
import logging
import glob
from db.error_enum import Error
from scan_folder.song_parser import song_parser
from db.db_operation import add_beatmap, create_connection

def scanner(songs_directory) -> Error:
    logging.info("----------------------------SCANNING START----------------------------")
    
    conn = create_connection() # open connection
    if not conn:
        logging.warning("connection to the database could not be established.")
        return Error.PATH_ERROR
    
    if os.path.exists(songs_directory):
        for root, _, _ in os.walk(os.path.abspath(songs_directory)):
            files = glob.glob(os.path.join(root,"*.osu"))
            for file in files:
                with open(os.path.join(root, file), "r", encoding='utf-8-sig') as osu_file:   
                    logging.debug("Reading " + file)
                    data = song_parser(osu_file, os.path.basename(root))
                    ret = add_beatmap(conn, data)
                    if(ret == Error.SQL_EXECUTE_ERROR):
                        # connection is closed, handled by add_beatmap
                        logging.critical("An error occured during sql operation. Stopping scan process.")
                        return Error.SQL_EXECUTE_ERROR
    else:
        logging.warning("path to osu songs folder does not exist.")
        logging.warning("path: " + songs_directory + "\n")
        return Error.PATH_ERROR
    conn.cursor().execute("PRAGMA optimize")
    conn.close() # close connection
    logging.info("----------------------------SCANNING FINISHED----------------------------\n")
    return Error.SUCCESS