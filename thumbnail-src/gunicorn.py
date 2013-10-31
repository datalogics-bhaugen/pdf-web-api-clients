# Gunicorn configuration file.

import os
from thumbnail.tmpdir import ROOT_DIR, VAR_DIR

BIND = '127.0.0.1:5050'
PROC_NAME = 'thumbnail'
ERROR_LOG = os.path.join(VAR_DIR, 'log', 'server', '{}.log'.format(PROC_NAME))

execfile(os.path.join(ROOT_DIR, 'src', 'gunicorn.py'))
