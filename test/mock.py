"classes that emulate other classes"

import os
import sys
import subprocess


class Client(object):
    def __init__(self, mock, pdf2img='pdf2img'):
        self._pdf2img = self._pdf2img_path(pdf2img)
        if not self.pdf2img: sys.exit('no {} in PATH'.format(pdf2img))
        self._temporary_name = self._temporary_pdf2img_name(pdf2img)
        subprocess.call(['mv', self.pdf2img, self.temporary_name])
        subprocess.call(['ln', '-s', os.path.abspath(mock), self.pdf2img])
    def __del__(self):
        subprocess.call(['mv', self.temporary_name, self.pdf2img])
    def __enter__(self):
        return self
    def __exit__(self, type, value, traceback):
        pass
    def _pdf2img_path(self, pdf2img):
        for dir in os.environ['PATH'].split(os.pathsep):
            filename = os.path.join(dir, pdf2img)
            if os.path.isfile(filename) and os.access(filename, os.X_OK):
                return filename
    def _temporary_pdf2img_name(self, pdf2img):
        root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        return os.path.join(root_dir, 'bin', os.path.basename(pdf2img))
    @property
    def pdf2img(self): return self._pdf2img
    @property
    def temporary_name(self): return self._temporary_name

class Request(object):
    def __init__(self, options):
        self._options = options
    @property
    def files(self): return {'spam': 0}
    @property
    def form(self): return {'options': self._options}
    @property
    def remote_addr(self): return 'localhost'
