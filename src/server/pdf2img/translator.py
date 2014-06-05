"RenderPages-to-pdf2img option translator"

import sys

from errors import Error, ErrorCode
from options import Option


INVALID_OPTION_VALUE = "{} is not a valid '{}' value"

class Translator(object):
    "translates Option (not Flag) to pdf2img option and validates value"
    def __init__(self, name):
        self._name, self._option = name, None
    def __call__(self, options, *args):
        "*args contains additional values needed to validate an option"
        for key, value in options.iteritems():
            if key in type(self).OPTIONS: self.set_option(value)
        return self.validate(*args)
    def set_option(self, value):
        self._option = value
        if isinstance(value, basestring):
            self._option = value.lower()
    def validate(self, *args):
        "validation is optional, return pdf2img option(s) if valid"
        return self.options
    @property
    def option(self): return self._option
    @property
    def options(self):
        if self.option is None: return []
        return [u'-{}={}'.format(self._name, self.option)]

class ImageSize(Translator):
    "translates imageWidth/imageHeight to -pixelcount"
    OPTIONS = [Option(u'imageWidth'), Option(u'imageHeight')]
    def __init__(self):
        Translator.__init__(self, u'pixelcount')
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

class Compression(Translator):
    "translates compression to -compression, adding -bpc as needed"
    OPTIONS = [Option(u'compression')]
    def __init__(self):
        Translator.__init__(self, u'compression')
    def validate(self, *args):
        if self.option is None: self._option = u'lzw'
        algorithms = ('lzw', 'g3', 'g4', 'jpg')
        if self.option not in algorithms:
            error = u'compression must be one of ' + unicode(algorithms)
            raise Error(ErrorCode.InvalidCompression, error)
        if self.option in ('g3', 'g4'):
            return self.options + [u'-bpc=1']
        return self.options

class OutputFormat(Translator):
    "translates and validates outputFormat (default=png)"
    OPTIONS = [Option(u'outputFormat')]
    def __init__(self):
        Translator.__init__(self, u'outputFormat')
    def validate(self, *args):
        if self.option == u'jpeg': self._option = u'jpg'
        if self.option == u'tiff': self._option = u'tif'
        if self.option is None: self._option = u'png'
        output_formats = ('bmp', 'gif', 'jpg', 'png', 'tif')
        if self.option not in output_formats:
            error = u'outputFormat must be one of ' + unicode(output_formats)
            raise Error(ErrorCode.InvalidOutputFormat, error)
        return self.options

class Pages(Translator):
    "translates pages to -pages (default=1), adding -multipage as needed"
    OPTIONS = [Option(u'pages')]
    def __init__(self):
        Translator.__init__(self, u'pages')
    def validate(self, *args):
        if self.option is None: self._option = '1'
        if type(self.option) == int: self._option = unicode(self.option)
        if not isinstance(self.option, basestring):
            error = INVALID_OPTION_VALUE.format(self.option, self._name)
            raise Error(ErrorCode.InvalidPage, error)
        multipage_request = u'-' in self.option or u',' in self.option
        if not multipage_request: return self.options
        if args[0] == u'tif': return self.options + [u'-multipage']
        error = u'Use TIFF format for multi-page image requests'
        raise Error(ErrorCode.InvalidOutputFormat, error)

class Resolution(Translator):
    "translates resolution to -resolution (default=150)"
    OPTIONS = [Option(u'resolution')]
    def __init__(self):
        Translator.__init__(self, u'resolution')
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
    "translates smoothing to -smoothing (default=all)"
    OPTIONS = [Option(u'smoothing')]
    def __init__(self):
        Translator.__init__(self, u'smoothing')
    def validate(self, *args):
        if self.option is None: self._option = 'all'
        return self.options


OPTIONS =\
    Compression.OPTIONS + ImageSize.OPTIONS + OutputFormat.OPTIONS +\
    Pages.OPTIONS + Resolution.OPTIONS + Smoothing.OPTIONS
