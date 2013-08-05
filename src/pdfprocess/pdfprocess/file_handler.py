import os
import logging
from logging.handlers import TimedRotatingFileHandler as BaseFileHandler


class FileHandler(BaseFileHandler):
    "format depends on record level"
    def __init__(self, log_name, when='D', interval=1):
        "rotate daily by default"
        log_dir = os.environ['LOG_PATH'] if 'LOG_PATH' in os.environ else '.'
        path = os.path.join(log_dir, '%s.log' % log_name)
        BaseFileHandler.__init__(self, path, when=when, interval=interval)
        self._make_formatters()
    def emit(self, record):
        self.setFormatter(self._formatters[record.levelno])
        BaseFileHandler.emit(self, record)
    def _make_formatters(self):
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

