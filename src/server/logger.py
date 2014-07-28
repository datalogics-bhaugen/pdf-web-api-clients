import os
import sys
import time
import logging

import cfg
import tmpdir
from platform import system
from datetime import datetime
from logging.handlers import SysLogHandler as BaseSysLogHandler
from logging.handlers import TimedRotatingFileHandler as BaseFileHandler


LOGGER = logging.getLogger()
PYTHON3 = sys.version_info.major == 3

class BaseHandler(object):
    "Base handler class defines level-dependent log entry formats."
    def __init__(self):
        prefix = '%(asctime)s:'
        level = '[%(levelname)s]'
        message = '%(message)s'
        basic_formatter = logging.Formatter(' '.join((prefix, message)))
        level_formatter = logging.Formatter(' '.join((prefix, level, message)))
        self._formatters = {
            logging.DEBUG: basic_formatter,
            logging.INFO: basic_formatter,
            logging.WARNING: level_formatter,
            logging.ERROR: level_formatter,
            logging.CRITICAL: level_formatter}
    def emit(self, record):
        self.setFormatter(self._formatters[record.levelno])
        handler = super() if PYTHON3 else super(BaseHandler, self)
        handler.emit(record)

class FileHandler(BaseHandler, BaseFileHandler):
    "File handler rotates log files daily by default."
    def __init__(self, log_name, when='D', interval=1):
        BaseHandler.__init__(self)
        logging.Formatter.converter = time.gmtime
        log_filename = '{}.log'.format(log_name)
        log_path = os.path.join(tmpdir.VAR_DIR, 'log', log_filename)
        BaseFileHandler.__init__(self, log_path, when=when, interval=interval)

class SysLogHandler(BaseHandler, BaseSysLogHandler):
    "Syslog handler uses local0 facility, ignores debug-level entries."
    def __init__(self):
        BaseHandler.__init__(self)
        address = '/var/run/syslog' if system() == 'Darwin' else '/dev/log'
        BaseSysLogHandler.__init__(self, address, BaseSysLogHandler.LOG_LOCAL0)
    def emit(self, record):
        if logging.DEBUG < record.levelno:
            handler = super() if PYTHON3 else super(SysLogHandler, self)
            handler.emit(record)


def debug(msg, *args, **kwargs): LOGGER.debug(msg, *args, **kwargs)
def info(msg, *args, **kwargs): LOGGER.info(msg, *args, **kwargs)
def warning(msg, *args, **kwargs): LOGGER.warning(msg, *args, **kwargs)
def error(msg, *args, **kwargs): LOGGER.error(msg, *args, **kwargs)
def critical(msg, *args, **kwargs): LOGGER.critical(msg, *args, **kwargs)
def log(lvl, msg, *args, **kwargs): LOGGER.log(lvl, msg, *args, **kwargs)

def log_level():
    dlenv = cfg.Configuration.environment.dlenv
    return logging.DEBUG if dlenv == 'test' else logging.INFO

def start(app_logger, name, version=None):
    global LOGGER
    LOGGER = app_logger
    LOGGER.setLevel(log_level())
    LOGGER.addHandler(SysLogHandler())
    LOGGER.addHandler(FileHandler(name))
    if version:
        info('{} ({}) started'.format(name, version))
    else:
        info('{} started'.format(name))

def iso8601_timestamp():
    utcnow = str(datetime.utcnow())
    return utcnow.replace(' ', 'T') + 'Z'
