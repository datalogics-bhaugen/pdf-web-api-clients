"web_api pdf2img action option translator"

import simplejson as json

from web_api import logger
from errors import Error, ErrorCode
from options import Option


class Translator(object):
    def __init__(self, name):
        self._name, self._option = name, None
    def __call__(self, options, *args):
        for key, value in options.iteritems():
            if key in type(self).OPTIONS: self.set_option(value)
        return self.validate(*args)
    def set_option(self, value):
        self._option = value.lower()
    def validate(self, *args):
        return self.options
    @property
    def option(self): return self._option
    @property
    def options(self):
        if self.option is None: return []
        return ['-{}={}'.format(self._name, self.option)]

class ImageSize(Translator):
    OPTIONS = [Option('imageWidth'), Option('imageHeight')]
    def __init__(self):
        Translator.__init__(self, 'pixelcount')
        self._dimensions = [None, None]
    def __call__(self, options):
        for key, value in options.iteritems():
            if key in ImageSize.OPTIONS:
                self._dimensions[ImageSize.OPTIONS.index(key)] = value
        if self.width and self.height:
            self.set_option('{}x{}'.format(self.width, self.height))
        elif self.width:
            self.set_option('w:{}'.format(self.width))
        elif self.height:
            self.set_option('h:{}'.format(self.height))
        return self.options
    @property
    def width(self): return self._dimensions[0]
    @property
    def height(self): return self._dimensions[1]

class OutputFormat(Translator):
    OPTIONS = [Option('outputFormat')]
    def __init__(self):
        Translator.__init__(self, 'outputFormat')
    def validate(self, *args):
        if self.option == 'jpeg': self._option = 'jpg'
        if self.option == 'tiff': self._option = 'tif'
        if not self.option: self._option = 'png'
        output_formats = ('gif', 'jpg', 'png', 'tif')
        if self.option not in output_formats:
            error = 'outputFormat must be one of ' + str(output_formats)
            raise Error(ErrorCode.InvalidOutputFormat, error)
        return self.options

class Pages(Translator):
    OPTIONS = [Option('pages')]
    def __init__(self):
        Translator.__init__(self, 'pages')
    def validate(self, *args):
        if not self.option: self._option = '1'
        multipage_request = '-' in self.option or ',' in self.option
        if not multipage_request: return self.options
        if args[0] == 'tif': return self.options + ['-multipage']
        error = 'Use TIFF format for multi-page image requests'
        raise Error(ErrorCode.InvalidOutputFormat, error)

class Resolution(Translator):
    OPTIONS = [Option('resolution')]
    def __init__(self):
        Translator.__init__(self, 'resolution')
    def validate(self, *args):
        if not self.option: self._option = '150'
        if 'x' not in self.option: return self.options
        error = 'No support for non-square pixel rendering.'
        raise Error(ErrorCode.InvalidResolution, error)

class Smoothing(Translator):
    OPTIONS = [Option('smoothing')]
    def __init__(self):
        Translator.__init__(self, 'smoothing')
    def validate(self, *args):
        if not self.option: self._option = 'all'
        if self.option == 'none': self._option = None
        return self.options


OPTIONS =\
    ImageSize.OPTIONS + OutputFormat.OPTIONS + Pages.OPTIONS +\
    Resolution.OPTIONS + Smoothing.OPTIONS
