'''
pdf2img appends a page number to the output filename, so we cannot
use tempfile to construct the output file. instead, we assume that
pdf2img successfully created the output file from the temporary
file we provided as input. this class encapsulates all this logic,
and deletes the image files created by pdf2img.
'''

import os
import glob
from pdfprocess import UNKNOWN


class OutputFile(object):
    def __init__(self, name, extension):
        self._pattern = '%s*.%s' % (name, extension)
    def __del__(self):
        for filename in self.glob():
            try: os.remove(filename)
            except Exception: pass
    def __enter__(self):
        return self
    def __exit__(self, type, value, traceback):
        pass
    def glob(self):
        return glob.glob(self._pattern)
    @property
    def name(self):
        names = self.glob()
        if len(names) == 1: return names[0]
        message = 'unsupported multi-page image request' if names else None
        raise UNKNOWN.copy(message)
