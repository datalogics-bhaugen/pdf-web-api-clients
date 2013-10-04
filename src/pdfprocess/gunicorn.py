# Gunicorn configuration file.

import os

BIND = '127.0.0.1:5000'
PROC_NAME = 'pdfprocess'

src_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
execfile(os.path.join(src_dir, 'gunicorn.py'))
