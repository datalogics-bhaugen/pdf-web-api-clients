'''
pdf2img appends a page number to the output filename, so we cannot
use tempfile to construct the output file. instead, we assume that
pdf2img successfully created the output file from the temporary
file we provided as input. this class encapsulates all this logic,
and deletes the image files created by pdf2img.
'''

import os
import glob


class OutputFile(object):
    def __init__(self, name, pages, extension):
        page_suffix = '' if '-' in pages or ',' in pages else '*'
        self._options = [] if page_suffix else ['-multipage']
        self._pattern = '%s%s.%s' % (name, page_suffix, extension)
    def __del__(self):
        try: os.remove(self.name)
        except Exception: pass
    def __enter__(self):
        return self
    def __exit__(self, type, value, traceback):
        pass
    @property
    def name(self):
        return glob.glob(self._pattern)[0]
    @property
    def options(self): return self._options

