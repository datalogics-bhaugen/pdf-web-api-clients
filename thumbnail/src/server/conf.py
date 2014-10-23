# Sphinx configuration file.

import os
import sys
import glob

server_dir = os.path.abspath('.')
sys.path.insert(0, server_dir)

import cfg

SERVER_NAME = u'Thumbnail'
VERSION = cfg.Configuration.versions.server

thumbnail_dir = os.path.dirname(os.path.dirname(server_dir))
doc_dir = os.path.join(os.path.dirname(thumbnail_dir), 'doc')
for egg_dir in glob.glob(os.path.join(doc_dir, 'eggs', '*')):
    sys.path.insert(0, egg_dir)

execfile(os.path.join(doc_dir, 'conf.py'))
