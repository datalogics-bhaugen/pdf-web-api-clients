# Gunicorn configuration file.

import os

BIND = '127.0.0.1:5050'
PROC_NAME = 'thumbnail'

root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
execfile(os.path.join(root_dir, 'src', 'gunicorn.py'))
