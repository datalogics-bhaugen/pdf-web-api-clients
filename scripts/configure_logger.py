"set LOG_PATH and use UTC timestamps"

import os
import logging
import time

root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.environ['LOG_PATH'] = os.path.join(root_dir, 'var/log')
logging.Formatter.converter = time.gmtime
