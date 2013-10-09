"pdfprocess configuration"

import os
import ConfigParser
import tmpdir


class Configuration(object):
    VERSIONS = 'versions'
    def __init__(self, server_cfg=None):
        parser = ConfigParser.ConfigParser()
        parser.read(server_cfg or os.path.join(tmpdir.ROOT_DIR, 'server.cfg'))
        self._pdf2img_version = parser.get(Configuration.VERSIONS, 'pdf2img')
        self._server_version = parser.get(Configuration.VERSIONS, 'server')
    @property
    def pdf2img_version(self): return self._pdf2img_version
    @property
    def server_version(self): return self._server_version
