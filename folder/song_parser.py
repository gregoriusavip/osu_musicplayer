import os
import fnmatch
import re
import logging

pattern = re.compile("^[0-9]* ")

def extract_song_name(song):
    song = re.sub(pattern, "", song)
    return song.split(" - ")


def extract_beatmap_id(beatmap_folder_name: str) -> str:
    """extract the beatmapID from the folder name

    Parameters:
    `beatmap_folder_name` (str): base folder path that contains the beatmapID

    Returns:
    `str`: the ID of this beatmap if exist, `None` otherwise
    """

    logging.info("Extracting beatmap ID from folder " + beatmap_folder_name)
    beatmapID = re.match(pattern, beatmap_folder_name)
    if beatmapID:
        beatmapID = beatmapID.group(0)[:-1]
        logging.info("Extracted ID " + beatmapID)
        return beatmapID
    logging.warning("ID could not be extracted")
    return beatmapID

def song_parser(song_path):
    info = extract_song_name(os.path.basename(song_path))
    for song in os.listdir(song_path):
        if fnmatch.fnmatch(song, '*.mp3'):
            info.append(song)
    print(info)