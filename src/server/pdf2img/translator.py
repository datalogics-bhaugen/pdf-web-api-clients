"RenderPages-to-PDF2IMG option translator."

import sys

from errors import Error, ErrorCode
from options import Option


INVALID_VALUE = "{} is not a valid '{}' value"

class Translator(object):
    "Translates Option (not Flag) to PDF2IMG option and validates value."
    def __init__(self, pdf2img_name):
        self._pdf2img_name = pdf2img_name
        self.option_value = None
    def __call__(self, options, *args):
        "*args contains the additional values needed to validate an option."
        for key, value in options.iteritems():
            if key in type(self).OPTIONS:
                self.option_value = value
        return self.validate(*args)
    def validate(self, *args):
        "Validation is optional, return PDF2IMG option(s) if valid."
        return self.pdf2img_options
    @property
    def option_value(self):
        "The normalized option value (strings are lowercase)."
        return self._option_value
    @option_value.setter
    def option_value(self, value):
        self._option_value = value
        if isinstance(value, basestring):
            self._option_value = value.lower()
    @property
    def pdf2img_options(self):
        "The PDF2IMG options (a translator may add an option, e.g. -bpc=1)."
        if self.option_value is None: return []
        return [u'-{}={}'.format(self.pdf2img_name, self.option_value)]
    @property
    def pdf2img_name(self):
        "The PDF2IMG option supported by this translator."
        return self._pdf2img_name

class ImageSize(Translator):
    "Translates the imageWidth and imageHeight options to -pixelcount."
    OPTIONS = [Option(u'imageWidth'), Option(u'imageHeight')]
    def __init__(self):
        Translator.__init__(self, u'pixelcount')
        self._dimensions = [None, None]
    def __call__(self, options):
        for key, value in options.iteritems():
            if key in ImageSize.OPTIONS:
                self._dimensions[ImageSize.OPTIONS.index(key)] = value
        if self.width and self.height:
            self.option_value = u'{}x{}'.format(self.width, self.height)
        elif self.width:
            self.option_value = u'w:{}'.format(self.width)
        elif self.height:
            self.option_value = u'h:{}'.format(self.height)
        return self.pdf2img_options
    @property
    def width(self):
        "The specified image width."
        return self._dimensions[0]
    @property
    def height(self):
        "The specified image height."
        return self._dimensions[1]

class Compression(Translator):
    "Validates the compression option."
    OPTIONS = [Option(u'compression')]
    def __init__(self):
        Translator.__init__(self, u'compression')
    def validate(self, *args):
        "Must be one of (lzw, g3, g4, jpg), default=lzw, add -bpc=1 as needed."
        if self.option_value is None: self.option_value = u'lzw'
        algorithms = ('lzw', 'g3', 'g4', 'jpg')
        if self.option_value not in algorithms:
            error = u'compression must be one of ' + unicode(algorithms)
            raise Error(ErrorCode.InvalidCompression, error)
        if self.option_value in ('g3', 'g4'):
            return self.pdf2img_options + [u'-bpc=1']
        return self.pdf2img_options

class OutputFormat(Translator):
    "Validates the outputFormat option."
    OPTIONS = [Option(u'outputFormat')]
    def __init__(self):
        Translator.__init__(self, u'outputFormat')
    def validate(self, *args):
        "Must be one of (bmp, gif, jpg, png, tif), default=png."
        if self.option_value == u'jpeg': self.option_value = u'jpg'
        if self.option_value == u'tiff': self.option_value = u'tif'
        if self.option_value is None: self.option_value = u'png'
        output_formats = ('bmp', 'gif', 'jpg', 'png', 'tif')
        if self.option_value not in output_formats:
            error = u'outputFormat must be one of ' + unicode(output_formats)
            raise Error(ErrorCode.InvalidOutputFormat, error)
        return self.pdf2img_options

class Pages(Translator):
    "Validates the pages option."
    OPTIONS = [Option(u'pages')]
    def __init__(self):
        Translator.__init__(self, u'pages')
    def validate(self, *args):
        "Default=1, add -multipage as needed."
        if self.option_value is None: self.option_value = '1'
        if type(self.option_value) == int:
            self.option_value = unicode(self.option_value)
        if not isinstance(self.option_value, basestring):
            error = INVALID_VALUE.format(self.option_value, self.pdf2img_name)
            raise Error(ErrorCode.InvalidPage, error)
        if u'-' not in self.option_value and u',' not in self.option_value:
            return self.pdf2img_options
        if args[0] == u'tif': return self.pdf2img_options + [u'-multipage']
        error = u'Use TIFF format for multi-page image requests'
        raise Error(ErrorCode.InvalidOutputFormat, error)

class Resolution(Translator):
    "Validates the resolution option."
    OPTIONS = [Option(u'resolution')]
    def __init__(self):
        Translator.__init__(self, u'resolution')
    def validate(self, *args):
        "Must be an integer, default=150."
        if self.option_value is None: self.option_value = 150
        try:
            boolean_value = isinstance(self.option_value, bool)
            if int(self.option_value) and not boolean_value:
                return self.pdf2img_options
        except ValueError:
            pass
        error = INVALID_VALUE.format(self.option_value, self.pdf2img_name)
        raise Error(ErrorCode.InvalidResolution, error)

class Smoothing(Translator):
    "Validates the smoothing option."
    OPTIONS = [Option(u'smoothing')]
    def __init__(self):
        Translator.__init__(self, u'smoothing')
    def validate(self, *args):
        "Default=all."
        if self.option_value is None: self.option_value = 'all'
        return self.pdf2img_options


OPTIONS =\
    Compression.OPTIONS + ImageSize.OPTIONS + OutputFormat.OPTIONS +\
    Pages.OPTIONS + Resolution.OPTIONS + Smoothing.OPTIONS
