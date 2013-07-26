'API server logger configuration'

import logging
import logging.handlers
import os

def configure(app_name, logger):
    logger.setLevel(logging.DEBUG) # TODO: get level from configuration
    logger.addHandler(FileHandler(app_name))

class FileHandler(logging.handlers.TimedRotatingFileHandler):
    def __init__(self, log_name, when='D', interval=1):
        'rotate daily by default'
        prefix = '%(asctime)s:'
        message = '%(message)s'
        level = '[%(levelname)s]'
        info_formatter = logging.Formatter(' '.join((prefix, message)))
        error_formatter = logging.Formatter(' '.join((prefix, level, message)))
        self.formatters = {
            logging.DEBUG: info_formatter,
            logging.INFO: info_formatter,
            logging.WARNING: error_formatter,
            logging.ERROR: error_formatter,
            logging.CRITICAL: error_formatter}
        log_path = os.path.join(_get_log_directory(), '%s.log' % log_name)
        super(FileHandler, self).__init__(
            log_path, when=when, interval=interval)
    def emit(self, record):
        self.setFormatter(self.formatters[record.levelno])
        super(FileHandler, self).emit(record)

def _get_log_directory():
    'log in current working directory by default'
    try: return os.environ['LOGPATH']
    except KeyError: return '.'

