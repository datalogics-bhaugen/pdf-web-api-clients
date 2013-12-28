# Gunicorn configuration file.

import os

import sys  # for configuring gunicorn after moving build directory
sys.path[0:0] = [os.path.dirname(os.path.abspath(__file__))]

from thumbnail.tmpdir import ROOT_DIR, VAR_DIR

PORT = 5050
PROC_NAME = 'thumbnail'
ERROR_LOG = os.path.join(VAR_DIR, 'log', 'server', '{}.log'.format(PROC_NAME))

execfile(os.path.join(ROOT_DIR, 'src', 'gunicorn.py'))
