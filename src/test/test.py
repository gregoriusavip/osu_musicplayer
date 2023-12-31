import os
import fnmatch
from typing import IO
import logging

GENERAL_KEYS = "AudioFilename"
METADATA_KEYS = ["Title", "TitleUnicode", "Artist", "ArtistUnicode", 
                 "Creator", "Version", "Source", "Tags", "BeatmapID", "BeatmapIDSet"]
EVENTS_KEYS = ["BackgroundFilename", "VideoFilename"]

def _osu_file_read_until(osu_file: IO[str], target: str) -> None:
    logging.info("Parsing file until it reaches the string: " + target)
    # read file until it reaches the target
    for line in (l[:-1] for l in osu_file):
        logging.debug("Reading line: " + line) 
        if line == target:
            logging.info("target string " + target + " is found")
            return
        
    logging.warning("WARNING: target string " + target + " could not be found.\n"
                    + "The file might be corrupted or an Error occured during the parsing process."
                    )

def _osu_file_general_parse(osu_file: IO[str], beatmap_info: dict) -> None:
    logging.info("Parsing [General] to find the Audio Filename")
    # read until it gets AudioFilename, Content format is `key: value`
    for line in (l[:-1] for l in osu_file):
        logging.debug("Reading line: " + line)
        data = line.split(":")
        if(data[0] == "AudioFilename"):
            logging.debug("Found the audio filename: " + data[1][1:])
            beatmap_info[data[0]] = data[1][1:]
            break
    
    if beatmap_info[GENERAL_KEYS] is None:
        logging.warning("WARNING: " + GENERAL_KEYS + " is missing from parsing [General].\n"
                        + "The file might be corrupted or an Error occured during the parsing process.")
    else:
        logging.debug("Key:" + GENERAL_KEYS + ", Value:" + beatmap_info[GENERAL_KEYS])
        logging.info("Finished parsing through [General]")

def _osu_file_metadata_parse(osu_file: IO[str], beatmap_info: dict) -> None:
    logging.info("Parsing [Metadata] for beatmap information")
    # read metadata until it reaches an empty line
    for line in (l[:-1] for l in osu_file):
        logging.debug("Reading line: " + line)
        if line is not "":
            data = line.split(":")
            logging.debug("Found the datatype" + data[0])
            beatmap_info[data[0]] = data[1]
            logging.debug("Key:" + data[0] + ", Value:" + beatmap_info[data[0]])
        else:
            break
    
    empty_keys = [key for key in METADATA_KEYS if beatmap_info.get(key) is None]
    logging.warning("The following key(s) " + str(empty_keys) + " has an empty value")
    logging.info("Finished parsing through [Metadata]")

# osu_file format is based of https://osu.ppy.sh/wiki/en/Client/File_formats/osu_%28file_format%29
def ver3_function(osu_file: IO[str], beatmap_info: dict) -> None:
    # read until reaches "[General]"
    _osu_file_read_until(osu_file, "[General]")

    # parse [General] to get AudioFilename, Inserting to beatmap_info
    _osu_file_general_parse(osu_file, beatmap_info)

    # read until reaches "[Metadata]"
    _osu_file_read_until(osu_file, "[Metadata]")

    # parse through [Metadata] to get and insert to beatmap_info
    _osu_file_metadata_parse(osu_file, beatmap_info)

    # read until reaches "[Events]"
    _osu_file_read_until(osu_file, "[Events]")
    
    for line in (l[:-1] for l in osu_file):
        lines = line.split(",")
        if "\"katamari2.jpg\"" in lines:
            print(lines)


ver_dict = {
    "v3": ver3_function,
}

def main_function(version, osu_file):
    beatmap_info = dict()
    beatmap_info[GENERAL_KEYS] = None
    for key in METADATA_KEYS + EVENTS_KEYS:
        beatmap_info[key] = None

    ver_dict.get(version[-2:], lambda metadata: print("Invalid: " + version + " not found"))(osu_file, beatmap_info)
    print(beatmap_info)

from pathlib import Path
songs_directory = os.path.join(Path.home(), 'Appdata', 'Local', 'osu!', "Songs", "1 Kenji Ninuma - DISCO PRINCE")

if os.path.exists(songs_directory):
    for file in os.listdir(songs_directory):
        if fnmatch.fnmatch(file, "*.osu"):
            with open(os.path.join(songs_directory, file), "r", encoding='utf-8') as osu_file:
                logging.info("--------------------------------------------")
                logging.info("Reading " + file)
                version = osu_file.readline().strip('\n')
                main_function(version, osu_file)
