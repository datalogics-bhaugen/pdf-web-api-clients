"pdfprocess image action option translator"

from errors import Error, ProcessCode
from options import Option


class Translator(object):
    def __init__(self, name):
        self._name, self._option = (name, '')
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
        return ['-%s=%s' % (self._name, self.option)] if self.option else []

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
            self.set_option('%sx%s' % (self.width, self.height))
        elif self.width:
            self.set_option('w:%s' % self.width)
        elif self.height:
            self.set_option('h:%s' % self.height)
        return self.options
    @property
    def width(self): return self._dimensions[0]
    @property
    def height(self): return self._dimensions[1]

class OutputForm(Translator):
    OPTIONS = [Option('outputForm')]
    def __init__(self):
        Translator.__init__(self, 'outputForm')
    def validate(self, *args):
        if self.option == 'jpeg': self._option = 'jpg'
        if self.option == 'tiff' or not self.option: self._option = 'tif'
        output_forms = ('gif', 'jpg', 'png', 'tif')
        if self.option not in output_forms:
            message = 'outputForm must be one of ' + str(output_forms)
            raise Error(ProcessCode.InvalidOutputType, message)
        return self.options

class Pages(Translator):
    OPTIONS = [Option('pages')]
    def __init__(self):
        Translator.__init__(self, 'pages')
    def validate(self, *args):
        output_form = args[0]
        if output_form != 'tif':
            if '-' in self.option or ',' in self.option:
                message = 'Use TIFF format for multi-page image requests'
                raise Error(ProcessCode.InvalidOutputType, message)
            if not self.option: self._option = '1'
        return self.options

class Resolution(Translator):
    OPTIONS = [Option('resolution')]
    def __init__(self):
        Translator.__init__(self, 'resolution')
    def validate(self, *args):
        if 'x' in self.option:
            message = 'No support for non-square pixel rendering.'
            raise Error(ProcessCode.InvalidResolution, message)
        return self.options

class Smoothing(Translator):
    OPTIONS = [Option('smoothing')]
    def __init__(self):
        Translator.__init__(self, 'smoothing')
    def validate(self, *args):
        if not self.option: self._option = 'all'
        if self.option == 'none': self._option = None
        return self.options


OPTIONS =\
    ImageSize.OPTIONS + OutputForm.OPTIONS + Pages.OPTIONS +\
    Resolution.OPTIONS + Smoothing.OPTIONS

