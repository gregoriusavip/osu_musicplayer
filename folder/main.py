import settings
import logging
from path_scanner import path_scanner
from create_db import create_db

settings.init()

if not settings.osu_folder:
    print("osu songs folder cannot be located. please select the correct directory")
    path = "some_path"
    settings.osu_folder = path_scanner(path)

def main():
    logging.basicConfig(format='%(asctime)s %(message)s', filename="debug.log", level=logging.DEBUG)
    logging.info("Starting application...")
    create_db()
    logging.info("Quitting appliaction...")

if __name__ == '__main__':
    main()