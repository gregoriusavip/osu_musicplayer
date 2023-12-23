import settings
from folder.path_scanner import path_scanner

settings.init()

if not settings.osu_folder:
    print("osu songs folder cannot be located. please select the correct directory")
    path = "some_path"
    settings.osu_folder = path_scanner(path)