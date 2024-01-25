import os
import logging
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
        directories = [d for d in os.listdir(songs_directory) if os.path.isdir(os.path.join(songs_directory, d))]
        groupID = 0

        for directory in directories:
            groupID += 1
            directory_path = os.path.join(songs_directory, directory)

            osu_files = [f for f in os.listdir(directory_path) if f.endswith('.osu')]

            for file in osu_files:
                osu_file_path = os.path.join(directory_path, file)
                if(os.path.getsize(osu_file_path) == 0):
                    logging.info("skipping empty file " + osu_file_path)
                    continue

                with open(osu_file_path, 'r', encoding='utf-8-sig') as osu_file:
                    logging.debug("Reading " + osu_file.name)
                    data = song_parser(osu_file, directory)
                    
                    if(data.get("BeatmapID") == "0"):
                        logging.info("skipping file (potentially unsubmitted beatmap) " + file)
                        continue

                    data['groupID'] = groupID
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