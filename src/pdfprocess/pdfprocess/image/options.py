"pdfprocess image action options"


class Option(object):
    def __init__(self, name, normalize=True):
        self._name = name
        self._normalize = normalize
        self._normalized_name = name.lower()
    def __str__(self):
        return self._normalized_name if self._normalize else self.name
    def __eq__(self, other): return self._normalized_name == other.lower()
    def __ne__(self, other): return not self == other
    @property
    def name(self): return self._name
    @property
    def action(self): return 'store'


class Flag(Option):
    @property
    def action(self): return 'store_true'

class FlagAlias(Flag):
    def __init__(self, name, pdf2img_name):
        Flag.__init__(self, name)
        self._pdf2img_name = pdf2img_name.lower()
    def __str__(self):
        return self._pdf2img_name


class ImageSize(object):
    OPTIONS = [Option('width'), Option('height')]
    def __init__(self):
        self._dimensions = {}
    def __setitem__(self, key, value):
        self._dimensions[key.lower()] = value
    def options(self):
        if len(self._dimensions) == 2:
            return ['-pixelcount=%sx%s' % (self.width, self.height)]
        elif 'width' in self._dimensions:
            return ['-pixelcount=w:%s' % self.width]
        elif self._dimensions:
            return ['-pixelcount=h:%s' % self.height]
        else:
            return []
    @property
    def width(self): return self._dimensions['width']
    @property
    def height(self): return self._dimensions['height']


OPTIONS = [
    Flag('OPP', normalize=False),
    FlagAlias('disableColorManagement', 'noCMM'),
    FlagAlias('disableThinLineEnhancement', 'noEnhanceThinLines'),
    FlagAlias('printPreview', 'asPrinted'),
    FlagAlias('suppressAnnotations', 'noAnnot'),
    Option('colorModel'),
    Option('compression'),
    Option('pages'),
    Option('password'),
    Option('pdfRegion'),
    Option('resolution'),
    Option('smoothing')]

