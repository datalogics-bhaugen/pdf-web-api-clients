# Gunicorn configuration file.

import os
from server import cfg
from server.tmpdir import ROOT_DIR, VAR_DIR

PORT = cfg.Configuration.service.port
PROC_NAME = 'pdfprocess'
ERROR_LOG = os.path.join(VAR_DIR, 'log', 'server', '{}.log'.format(PROC_NAME))

execfile(os.path.join(ROOT_DIR, 'src', 'gunicorn.py'))
