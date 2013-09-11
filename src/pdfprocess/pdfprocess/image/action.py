"pdfprocess image action"

import base64
import subprocess
import tempfile

import pdfprocess
from pdfprocess import Auth, Error, ProcessCode
from .argument_parser import ArgumentParser
from .options import Flag
from .output_file import OutputFile


class Action(pdfprocess.Action):
    def __init__(self, logger, request):
        pdfprocess.Action.__init__(self, logger, request)
        self._input_name = self.request_form.get('inputName', '<anon>')
        self._parser = ArgumentParser(self._log_request)
    def __call__(self):
        try:
            self._parser(self.options)
        except Error as error:
            self.raise_error(error)
        except Exception as exc:
            self.raise_error(Error(ProcessCode.InvalidSyntax, exc.message))
        auth = self.authorize()
        if auth != Auth.OK: self.authorize_error(auth)
        return self._pdf2img()
    def _get_image(self, input_name, output_file):
        with pdfprocess.Stdout() as stdout:
            options = self._parser.pdf2img_options
            args = ['pdf2img'] + options + [input_name, self.output_form]
            if subprocess.call(args, stdout=stdout):
                self.raise_error(Action.get_error(stdout))
        with open(output_file.name, 'rb') as image_file:
            image = base64.b64encode(image_file.read())
            return pdfprocess.response(ProcessCode.OK, image)
    def _log_request(self, parser_options):
        options = ' '.join(parser_options)
        if options: options = ' ' + options
        input_name = self.input_name
        if ' ' in input_name: input_name = '"%s"' % input_name
        output_form = self.output_form
        if output_form: output_form = ' ' + output_form
        info_args = (options, input_name, output_form, self.client)
        self.logger.info('pdf2img%s %s%s %s' % info_args)
    def _pdf2img(self):
        with tempfile.NamedTemporaryFile() as input_file:
            self.input.save(input_file)
            input_file.flush()
            with OutputFile(input_file.name, self.output_form) as output_file:
                return self._get_image(input_file.name, output_file)
    @property
    def input_name(self): return self._input_name
    @property
    def output_form(self): return self._parser.output_form
    @property
    def pages(self): return self._parser.pages

