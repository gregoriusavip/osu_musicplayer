import os
import logging
import glob
from scan_folder.song_parser import song_parser

def scanner(songs_directory):
    logging.info("----------------------------SCANNING START----------------------------")
    if os.path.exists(songs_directory):
        for root, _, _ in os.walk(os.path.abspath(songs_directory)):
            files = glob.glob(os.path.join(root,"*.osu"))
            for file in files:
                with open(os.path.join(root, file), "r", encoding='utf-8-sig') as osu_file:
                    logging.debug("Reading " + file)
                    song_parser(osu_file, os.path.basename(root))
    logging.info("----------------------------SCANNING FINISHED----------------------------\n")