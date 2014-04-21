"WebAPI input document"

import requests

from cfg import Configuration
from errors import Error, ErrorCode


class Input(object):
    def __init__(self, action):
        self._action, self._input = action, None
    def _raise_error(self, error):
        self._action.raise_error(Error(ErrorCode.InvalidInput, error))
    @property
    def files(self): return self._action.request_files

class FromFile(Input):
    def initialize(self):
        files = len(self.files)
        if files > 1:
            self._raise_error(u'excess input ({} files)'.format(files))
        if 'input' not in self.files:
            self._raise_error(u'request missing "input" or "inputURL" part')
        self._input = self.files['input']
    def save(self, input_file):
        self._input.save(input_file)

class FromURL(Input):
    def __del__(self):
        if self._input: self._input.close()
    def initialize(self):
        if self.files:
            self._raise_error(u'excess input (inputURL and request file)')
        try:
            self._input = requests.get(self._action.input_url, stream=True)
        except Exception as exception:
            self._raise_error(unicode(exception))
        Error.validate_input_size(self._content_length)
    def save(self, input_file):
        chunk_size = int(Configuration.limits.input_size) / 10
        for chunk in self._input.iter_content(chunk_size=chunk_size):
            if chunk:
                input_file.write(chunk)
                Error.validate_input_size(input_file.tell())
    @property
    def _content_length(self):
        try:
            return int(self._input.headers['content-length'])
        except:
            return 0
