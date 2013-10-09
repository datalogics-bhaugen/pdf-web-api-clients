# Gunicorn configuration file.

import os
import tmpdir

BIND = '127.0.0.1:5000'
PROC_NAME = 'pdfprocess'

execfile(os.path.join(tmpdir.ROOT_DIR, 'src', 'gunicorn.py'))
