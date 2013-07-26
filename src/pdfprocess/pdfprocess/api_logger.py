'API server logger configuration'

import logging
import logging.handlers
import os

def configure(app_name, logger):
    logger.setLevel(logging.DEBUG) # TODO: get level from configuration
    logger.addHandler(FileHandler(app_name))

def get_log_directory():
    'log in current working directory by default'
    try: return os.environ['LOGPATH']
    except KeyError: return '.'

class FileHandler(logging.handlers.TimedRotatingFileHandler):
    def __init__(self, log_name, when='D', interval=1):
        'rotate daily by default'
        log_path = os.path.join(get_log_directory(), '%s.log' % log_name)
        super(FileHandler, self).__init__(
            log_path, when=when, interval=interval)
        debug_format = '%(asctime)s: %(message)s'
        debug_formatter = logging.Formatter(debug_format)
        error_format = '%(asctime)s: [%(levelname)s] %(message)s'
        error_formatter = logging.Formatter(error_format)
        self.formatters = {
            logging.DEBUG: debug_formatter,
            logging.INFO: debug_formatter,
            logging.WARNING: error_formatter,
            logging.ERROR: error_formatter,
            logging.CRITICAL: error_formatter}
    def emit(self, record):
        self.setFormatter(self.formatters[record.levelno])
        super(FileHandler, self).emit(record)

