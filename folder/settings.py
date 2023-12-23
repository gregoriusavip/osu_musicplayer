import folder.path_scanner as path_scanner

def init():
    global osu_folder
    osu_folder = path_scanner.default_scanner()