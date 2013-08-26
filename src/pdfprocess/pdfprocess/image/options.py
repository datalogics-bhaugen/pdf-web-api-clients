"pdfprocess image action options"


class Option(object):
    def __init__(self, name, pdf2img_name=None):
        self._name = name
        self._pdf2img_name = pdf2img_name if pdf2img_name else name
    def __str__(self):
        return self._pdf2img_name
    def __eq__(self, other):
        return self.name.lower() == other.lower()
    def __ne__(self, other):
        return not self == other
    @property
    def name(self): return self._name
    @property
    def action(self): return 'store'

class Flag(Option):
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

