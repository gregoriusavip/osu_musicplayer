import os
import fnmatch
import re

sub_pattern = re.compile("^[0-9]* ")

def extract_song(song):
    song = re.sub(sub_pattern, "", song)
    return song.split(" - ")

def song_parser(song_path):
    info = extract_song(os.path.basename(song_path))
    for song in os.listdir(song_path):
        if fnmatch.fnmatch(song, '*.mp3'):
            info.append(song)
    print(info)

from pathlib import Path
songs_directory = os.path.join(Path.home(), 'Appdata', 'Local', 'osu!', "Songs", "1480431 Plum - Dustwind")
song_parser(songs_directory)