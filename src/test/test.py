import os
import fnmatch
import re

def ver3_function(version):
    print(version)

ver_dict = {
    "v3": ver3_function,
}

def main_function(ver, version):
    ver_dict.get(ver, lambda version: print("Invalid: " + version + " not found"))(version)

from pathlib import Path
songs_directory = os.path.join(Path.home(), 'Appdata', 'Local', 'osu!', "Songs", "1 Kenji Ninuma - DISCO PRINCE")

if os.path.exists(songs_directory):
    for file in os.listdir(songs_directory):
        if fnmatch.fnmatch(file, "*.osu"):
            with open(os.path.join(songs_directory, file), "r", encoding='utf-8') as metadata:
                version = metadata.readline().strip('\n')
                main_function(version[2:], version)
