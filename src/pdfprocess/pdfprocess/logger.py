#!/usr/bin/env python

'logging file handler for API server'

import logging
import os
import time
from logging.handlers import TimedRotatingFileHandler

logging.Formatter.converter = time.gmtime

def get_format(level):
    level_name = '' if level < logging.WARNING else '[%(levelname)s] '
    return '%(asctime)s: ' + level_name + '%(message)s'

def get_log_directory():
    try: return os.environ['LOGPATH']
    except KeyError: return '.'

def get_log_path(log_name):
    return os.path.join(get_log_directory(), '%s.log' % log_name)

class FileHandler(TimedRotatingFileHandler):
    'rotate daily by default, display level only for errors and warnings'
    def __init__(self, log_name, level=logging.DEBUG, when='D', interval=1):
        TimedRotatingFileHandler.__init__(self,
            get_log_path(log_name), when=when, interval=interval)
        self.setFormatter(logging.Formatter(get_format(level)))
        self.setLevel(level)

