"pdfprocess image action option translator"

from errors import Error, ProcessCode
from options import Option


class Translator(object):
    def __init__(self, name, default_value=''):
        self._name, self._option = (name, default_value)
    def __call__(self, options):
        for key, value in options.iteritems():
            if key in type(self).OPTIONS: self.set_option(value)
        return self.validate()
    def set_option(self, value):
        self._option = value.lower()
    def validate(self):
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
        return self.validate()
    @property
    def width(self): return self._dimensions[0]
    @property
    def height(self): return self._dimensions[1]

class OutputForm(Translator):
    OPTIONS = [Option('outputForm')]
    def __init__(self):
        Translator.__init__(self, 'outputForm', 'tif')
    def validate(self):
        if self.option == 'jpeg': self._option = 'jpg'
        if self.option == 'tiff': self._option = 'tif'
        output_forms = ('gif', 'jpg', 'png', 'tif')
        if self.option not in output_forms:
            message = 'outputForm must be one of ' + str(output_forms)
            raise Error(ProcessCode.InvalidOutputType, message)
        return Translator.validate(self)

class Resolution(Translator):
    OPTIONS = [Option('resolution')]
    def __init__(self):
        Translator.__init__(self, 'resolution')
    def validate(self):
        if 'x' in self.option:
            message = 'No support for non-square pixel rendering.'
            raise Error(ProcessCode.InvalidResolution, message)
        return Translator.validate(self)

class Smoothing(Translator):
    OPTIONS = [Option('smoothing')]
    def __init__(self):
        Translator.__init__(self, 'smoothing', 'all')
    def validate(self):
        if self.option == 'none': self._option = None
        return Translator.validate(self)


OPTIONS =\
    ImageSize.OPTIONS + OutputForm.OPTIONS +\
    Resolution.OPTIONS + Smoothing.OPTIONS

