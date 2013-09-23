"pdfprocess image action options"


class Option(object):
    FORMAT = '-%s=%s'
    def __init__(self, name, pdf2img_name=None):
        self._name = name
        self._pdf2img_name = pdf2img_name if pdf2img_name else name
    def __str__(self):
        return self._pdf2img_name
    def __eq__(self, other):
        return self.name.lower() == other.lower()
    def __ne__(self, other):
        return not self == other
    def format(self, value, pdf2img_option=False):
        option_name = str(self) if pdf2img_option else self.name
        return Option.FORMAT % (option_name, value)
    @property
    def name(self): return self._name
    @property
    def action(self): return 'store'

class Flag(Option):
    FORMAT = '-%s'
    def format(self, value, pdf2img_flag=False):
        if not value: return ''
        if value is True:
            return Flag.FORMAT % (str(self) if pdf2img_flag else self.name)
        raise Exception("invalid %s value: %s" % (self.name, value))
    @property
    def action(self): return 'store_true'


OPTIONS = [
    Flag('OPP'),
    Flag('disableColorManagement', 'nocmm'),
    Flag('disableThinLineEnhancement', 'noenhancethinlines'),
    Flag('printPreview', 'asprinted'),
    Flag('suppressAnnotations', 'noannot'),
    Option('colorModel', 'colormodel'),
    Option('compression'),
    Option('password'),
    Option('pdfRegion', 'pdfregion')]

