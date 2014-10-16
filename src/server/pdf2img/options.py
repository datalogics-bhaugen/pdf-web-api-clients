'''
This module defines the classes used by
:py:class:`server.pdf2img.argument_parser.ArgumentParser`.
'''

class Option(object):
    "RenderPages option, e.g. password."
    FORMAT = u'-{}={}'
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
        "Return printed representation, translated for PDF2IMG if specified."
        return Option.FORMAT.format(self.option_name(pdf2img_option), value)
    def option_name(self, pdf2img_option=False):
        "The name of this option, translated for PDF2IMG if specified."
        return str(self) if pdf2img_option else self.name
    @property
    def name(self):
        "The WebAPI name of this option, e.g. password."
        return self._name
    @property
    def action(self):
        ":py:meth:`argparse.ArgumentParser.add_argument` *action* value."
        return 'store'

class Flag(Option):
    "RenderPages flag (boolean option), e.g. printPreview."
    FORMAT = u'-{}'
    def format(self, value, pdf2img_flag=False):
        "Return printed representation, translated for PDF2IMG if specified."
        if not value: return u''
        if value is True:
            return Flag.FORMAT.format(self.option_name(pdf2img_flag))
        raise Exception(u'invalid {} value: {}'.format(self.name, value))
    @property
    def action(self):
        ":py:meth:`argparse.ArgumentParser.add_argument` *action* value."
        return 'store_true'


OPTIONS = [
    Flag(u'OPP'),
    Flag(u'disableColorManagement', u'nocmm'),
    Flag(u'disableThinLineEnhancement', u'noenhancethinlines'),
    Flag(u'printPreview', u'asprinted'),
    Flag(u'suppressAnnotations', u'noannot'),
    Option(u'colorModel', u'colormodel'),
    Option(u'password'),
    Option(u'pdfRegion', u'pdfregion'),
    Option(u'resampler')]
