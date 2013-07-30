'API server temporary file classes'

import os
import tempfile

class OutputFile(object):
    '''
    pdf2img appends a page count to the output filename, so we cannot
    use tempfile to construct the output file. instead, we assume that
    pdf2img successfully created the output file from the temporary
    file we provided as input. this class encapsulates all this logic,
    and deletes the image files created by pdf2img.
    '''
    def __init__(self, name, page, extension):
        self._name = '%s%s.%s' % (name, page, extension) # no underscore!
    def __enter__(self):
        return self
    def __exit__(self, type, value, traceback):
        try: os.remove(self.name)
        except OSError as error: pass
    @property
    def name(self): return self._name
    @property
    def options(self): return ['-digits=1']

class Stdout(object):
    'for capturing stdout'
    def __init__(self):
        self._file = tempfile.TemporaryFile()
    def __enter__(self):
        return self
    def __exit__(self, type, value, traceback):
        self._file.close()
    def __str__(self):
        self._file.seek(0)
        return ''.join((line for line in self._file))
    def __getattr__(self, name):
        return getattr(self._file, name)

