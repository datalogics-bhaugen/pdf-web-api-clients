"WebAPI pdf2img action option translator"

import sys

from errors import Error, ErrorCode
from options import Option


INVALID_OPTION_VALUE = "{} is not a valid '{}' value"
STRING_TYPES = (str, unicode) if sys.version_info.major < 3 else (str,)


class Translator(object):
    def __init__(self, name):
        self._name, self._option = name, None
    def __call__(self, options, *args):
        for key, value in options.iteritems():
            if key in type(self).OPTIONS: self.set_option(value)
        return self.validate(*args)
    def set_option(self, value):
        self._option = value.lower() if type(value) in STRING_TYPES else value
    def validate(self, *args):
        return self.options
    @property
    def option(self): return self._option
    @property
    def options(self):
        if self.option is None: return []
        return [u'-{}={}'.format(self._name, self.option)]

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
            self.set_option(u'{}x{}'.format(self.width, self.height))
        elif self.width:
            self.set_option(u'w:{}'.format(self.width))
        elif self.height:
            self.set_option(u'h:{}'.format(self.height))
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
        if self.option == u'jpeg': self._option = u'jpg'
        if self.option == u'tiff': self._option = u'tif'
        if self.option is None: self._option = u'png'
        output_formats = (u'gif', u'jpg', u'png', u'tif')
        if self.option not in output_formats:
            error = u'outputFormat must be one of ' + unicode(output_formats)
            raise Error(ErrorCode.InvalidOutputFormat, error)
        return self.options

class Pages(Translator):
    OPTIONS = [Option('pages')]
    def __init__(self):
        Translator.__init__(self, 'pages')
    def validate(self, *args):
        if self.option is None: self._option = '1'
        if type(self.option) == int: self._option = unicode(self.option)
        if type(self.option) not in STRING_TYPES:
            error = INVALID_OPTION_VALUE.format(self.option, self._name)
            raise Error(ErrorCode.InvalidPage, error)
        multipage_request = u'-' in self.option or u',' in self.option
        if not multipage_request: return self.options
        if args[0] == u'tif': return self.options + [u'-multipage']
        error = u'Use TIFF format for multi-page image requests'
        raise Error(ErrorCode.InvalidOutputFormat, error)

class Resolution(Translator):
    OPTIONS = [Option('resolution')]
    def __init__(self):
        Translator.__init__(self, 'resolution')
    def validate(self, *args):
        if self.option is None: self._option = 150
        try:
            if int(self.option) and not isinstance(self.option, bool):
                return self.options
        except ValueError:
            pass
        error = INVALID_OPTION_VALUE.format(self.option, self._name)
        raise Error(ErrorCode.InvalidResolution, error)

class Smoothing(Translator):
    OPTIONS = [Option('smoothing')]
    def __init__(self):
        Translator.__init__(self, 'smoothing')
    def validate(self, *args):
        if self.option is None: self._option = 'all'
        if self.option == 'none': self._option = None
        return self.options


OPTIONS =\
    ImageSize.OPTIONS + OutputFormat.OPTIONS + Pages.OPTIONS +\
    Resolution.OPTIONS + Smoothing.OPTIONS
