from path_scanner import default_scanner
from logging.handlers import RotatingFileHandler
import logging
import os

def init():
    global osu_folder
    osu_folder = default_scanner()

    log_formatter = logging.Formatter('%(asctime)s %(levelname)s %(funcName)s(%(lineno)d) %(message)s')
    logFile = os.path.join(os.getcwd(), 'log')
    handler = RotatingFileHandler(logFile, mode='w', maxBytes=5*1024*1024, 
                                backupCount=2, encoding='utf-8', delay=0)
    handler.setFormatter(log_formatter)
    handler.setLevel(logging.DEBUG)

    app_log = logging.getLogger('root')
    app_log.setLevel(logging.DEBUG)
    app_log.addHandler(handler)