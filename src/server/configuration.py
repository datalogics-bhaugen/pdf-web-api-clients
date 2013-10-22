"WebAPI configuration"

import os
import ConfigParser
from tmpdir import ROOT_DIR


class Configuration(object):
    VERSIONS = 'versions'
    def __init__(self, server_cfg=None):
        self._filename = server_cfg or os.path.join(ROOT_DIR, 'server.cfg')
        parser = ConfigParser.ConfigParser()
        parser.read(self._filename)
        self._pdf2img_version = parser.get(Configuration.VERSIONS, 'pdf2img')
        self._server_version = parser.get(Configuration.VERSIONS, 'server')
    @property
    def filename(self): return self._filename
    @property
    def pdf2img_version(self): return self._pdf2img_version
    @property
    def server_version(self): return self._server_version
