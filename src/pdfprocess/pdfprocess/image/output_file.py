'''
pdf2img appends a page number to the output filename, so we cannot
use tempfile to construct the output file. instead, we assume that
pdf2img successfully created the output file from the temporary
file we provided as input. this class encapsulates all this logic,
and deletes the image files created by pdf2img.
'''

import os


class OutputFile(object):
    def __init__(self, name, page, extension):
        self._options = ['-digits=1']
        if not page or '-' in page or ',' in page:
            self._options.append('-multipage')
            page = ''
        self._name = '%s%s.%s' % (name, page, extension) # no underscore!
    def __enter__(self):
        return self
    def __exit__(self, type, value, traceback):
        try: os.remove(self.name)
        except OSError as error: pass
    @property
    def name(self): return self._name
    @property
    def options(self): return self._options

