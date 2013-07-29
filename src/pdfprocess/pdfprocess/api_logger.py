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
        self._make_formatters()
        log_dir = os.environ['LOG_PATH'] if 'LOG_PATH' in os.environ else '.'
        path = os.path.join(log_dir, '%s.log' % log_name)
        super(FileHandler, self).__init__(path, when=when, interval=interval)
    def emit(self, record):
        self.setFormatter(self._formatters[record.levelno])
        super(FileHandler, self).emit(record)
    def _make_formatters(self):
        prefix = '%(asctime)s:'
        message = '%(message)s'
        level = '[%(levelname)s]'
        info_formatter = logging.Formatter(' '.join((prefix, message)))
        error_formatter = logging.Formatter(' '.join((prefix, level, message)))
        self._formatters = {
            logging.DEBUG: info_formatter,
            logging.INFO: info_formatter,
            logging.WARNING: error_formatter,
            logging.ERROR: error_formatter,
            logging.CRITICAL: error_formatter}

