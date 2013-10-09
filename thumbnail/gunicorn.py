# Gunicorn configuration file.

import os
import thumbnail.tmpdir

BIND = '127.0.0.1:5050'
PROC_NAME = 'thumbnail'

execfile(os.path.join(thumbnail.tmpdir.ROOT_DIR, 'src', 'gunicorn.py'))
