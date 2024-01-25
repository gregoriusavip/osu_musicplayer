from typing import IO
import logging
import settings
import re
import os

pattern = re.compile("^[0-9]* ")

def _warning_default_message(file_name: str) -> None:
    logging.warning("From file: " + file_name + "\n")

def _extract_beatmap_id(beatmap_folder_name: str) -> str:
    """extract the beatmapID from the folder name

    Parameters:
    `beatmap_folder_name` (str): base folder path that contains the beatmapID

    Returns:
    `str`: the ID of this beatmap if exist, `None` otherwise
    """

    logging.debug("Extracting beatmap ID from folder " + beatmap_folder_name)
    beatmapID = re.match(pattern, beatmap_folder_name)
    if beatmapID:
        beatmapID = beatmapID.group(0)[:-1]
        logging.debug("Extracted ID " + beatmapID)
        return beatmapID
    logging.warning("ID could not be extracted")
    return beatmapID

def _osu_file_read_until(osu_file: IO[str], target: str) -> None:
    logging.debug("Parsing file until it reaches the string: " + target)
    # read file until it reaches the target
    for line in (l[:-1] for l in osu_file):
        logging.debug("Reading line: " + line)
        if line == target:
            logging.debug("target string " + target + " is found")
            return
        
    logging.warning("WARNING: target string " + target + " could not be found.\n")
    _warning_default_message(osu_file.name)
    

def _osu_file_general_parse(osu_file: IO[str], beatmap_info: dict) -> None:
    logging.debug("Parsing [General] to find the Audio Filename")
    # read until it gets AudioFilename, Content format is `key: value`
    for line in (l[:-1] for l in osu_file):
        logging.debug("Reading line: " + line)
        data = line.split(":")
        if(data[0] == "AudioFilename"):
            logging.debug("Found the audio filename: " + data[1][1:])
            beatmap_info[data[0]] = data[1][1:]
            break
    
    if beatmap_info[settings.GENERAL_KEYS] is None:
        logging.warning("WARNING: " + settings.GENERAL_KEYS + " is missing from parsing [General].\n")
        _warning_default_message(osu_file.name)
    else:
        logging.debug("Key:" + settings.GENERAL_KEYS + ", Value:" + beatmap_info[settings.GENERAL_KEYS])
        logging.debug("Finished parsing through [General]")

def _osu_file_metadata_parse(osu_file: IO[str], beatmap_info: dict) -> None:
    logging.debug("Parsing [Metadata] for beatmap information")
    # read metadata until it reaches an empty line
    for line in (l[:-1] for l in osu_file):
        logging.debug("Reading line: " + line)
        if not re.match(r'^\s*$', line):
            data = line.split(":")
            logging.debug("Found the data: " + data[0])
            if(len(data) > 1):
                beatmap_info[data[0]] = data[1]
            else:
                logging.warning("line: " + line + " is not formatted as a key:value pairs. This line will be ignored")
                _warning_default_message(osu_file.name)
                continue
            logging.debug("Key:" + data[0] + ", Value:" + beatmap_info[data[0]])
        else:
            break
    
    empty_keys = [key for key in settings.METADATA_KEYS if beatmap_info.get(key) is None]
    if len(empty_keys) != 0:
        logging.warning("The following key(s) " + str(empty_keys) + " has an empty value")
        _warning_default_message(osu_file.name)
    logging.debug("Finished parsing through [Metadata]")

def _osu_file_events_parse(osu_file: IO[str], beatmap_info: dict) -> None:
    logging.debug("Parsing [Events] for background and or video filename")
    # read events until it reaches an empty line
    for line in (l[:-1] for l in osu_file):
        logging.debug("Reading line: " + line)
        if not re.match(r'^\s*$', line):
            if line[:2] == "//":
                pass
            data = line.split(",")
            if (data[0] == "0") and (data[1] == "0") :
                beatmap_info[settings.EVENTS_KEYS] = data[2][1:-1]
                break
        else:
            break
    
    if beatmap_info[settings.EVENTS_KEYS] == None:
        logging.warning("WARNING: " + settings.EVENTS_KEYS + " is missing from parsing [Events].")
        _warning_default_message(osu_file.name)
    logging.debug("Finished parsing through [Events]")

# osu_file format is based of https://osu.ppy.sh/wiki/en/Client/File_formats/osu_%28file_format%29
def _osu_file_parser(osu_file: IO[str]) -> dict:
    beatmap_info = dict()
    beatmap_info[settings.GENERAL_KEYS] = None
    for key in settings.METADATA_KEYS:
        beatmap_info[key] = None
    beatmap_info[settings.EVENTS_KEYS] = None

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
    
    # parse through [Events] to get and insert to beatmap_info
    _osu_file_events_parse(osu_file, beatmap_info)

    return beatmap_info

def song_parser(osu_file: IO[str], base_song_folder_path: str) -> dict:
    version = None
    for line in osu_file:
        logging.debug("Reading line: " + line)
        if not re.match(r'^\s*$', line.strip('\n')):
            version = int(line.split()[3][1:])
            break
    res = _osu_file_parser(osu_file)
    if(version is not None and version < 10):
        res["BeatmapSetID"] = _extract_beatmap_id(base_song_folder_path)
    res[settings.GENERAL_KEYS] = os.path.join(base_song_folder_path, res[settings.GENERAL_KEYS])
    if(res[settings.EVENTS_KEYS] is not None):
        res[settings.EVENTS_KEYS] = os.path.join(base_song_folder_path, res[settings.EVENTS_KEYS])
    return res