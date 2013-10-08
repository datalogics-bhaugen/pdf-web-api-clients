import os
import sys
import time
import logging
from platform import system
from logging.handlers import SysLogHandler as BaseSysLogHandler
from logging.handlers import TimedRotatingFileHandler as BaseFileHandler


class BaseHandler(object):
    "format depends on level"
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
        major_version = sys.version_info.major
        handler = super(BaseHandler, self) if major_version < 3 else super()
        handler.emit(record)

class FileHandler(BaseHandler, BaseFileHandler):
    def __init__(self, log_name, when='D', interval=1):
        "rotate daily by default"
        BaseHandler.__init__(self)
        logging.Formatter.converter = time.gmtime
        src_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        log_dir = os.path.join(os.path.dirname(src_dir), 'var', 'log')
        log_path = os.path.join(log_dir, '%s.log' % log_name)
        BaseFileHandler.__init__(self, log_path, when=when, interval=interval)

class SysLogHandler(BaseHandler, BaseSysLogHandler):
    def __init__(self):
        BaseHandler.__init__(self)
        address = '/var/run/syslog' if system() == 'Darwin' else '/dev/log'
        BaseSysLogHandler.__init__(self, address)

def start(logger, logger_name, log_level=logging.DEBUG):
    logger.setLevel(log_level)
    logger.addHandler(SysLogHandler())
    logger.addHandler(FileHandler(logger_name))
    logger.info('%s started' % logger_name)
