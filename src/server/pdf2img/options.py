"WebAPI pdf2img action options"


class Option(object):
    FORMAT = '-{}={}'
    def __init__(self, name, pdf2img_name=None):
        self._name = name
        self._pdf2img_name = pdf2img_name or name
    def __str__(self):
        return self._pdf2img_name
    def __eq__(self, other):
        return self.name.lower() == other.lower()
    def __ne__(self, other):
        return not self == other
    def format(self, value, pdf2img_option=False):
        return Option.FORMAT.format(self.option_name(pdf2img_option), value)
    def option_name(self, pdf2img_option=False):
        return str(self) if pdf2img_option else self.name
    @property
    def name(self): return self._name
    @property
    def action(self): return 'store'

class Flag(Option):
    FORMAT = '-{}'
    def format(self, value, pdf2img_flag=False):
        if not value: return ''
        if value is True:
            return Flag.FORMAT.format(self.option_name(pdf2img_flag))
        raise Exception('invalid {} value: {}'.format(self.name, value))
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
