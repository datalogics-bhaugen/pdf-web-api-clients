"pdfprocess image package"

import base64
import subprocess
import tempfile

import flask
import simplejson as json

import errors
import pdfprocess
from pdfprocess import Auth, Error, ProcessCode
from .argument_parser import ArgumentParser, Flag
from .output_file import OutputFile


class Action(pdfprocess.Action):
    def __init__(self, logger, request):
        pdfprocess.Action.__init__(self, logger, request)
        self._input_name = self.request_form.get('inputName', '<anon>')
        self._options = json.loads(self.request_form.get('options', '{}'))
        self._parser = ArgumentParser(self._log_request)
    def __call__(self):
        try:
            self._parser(self._options)
        except Exception as exc:
            return self.abort(Error(ProcessCode.InvalidSyntax, exc.message))
        if self.multipage_request and self.output_form != 'tif':
            exc_info = 'Use TIFF format for multi-page image requests'
            return self.abort(Error(ProcessCode.InvalidPage, exc_info))
        if self.output_form not in ('gif', 'jpg', 'png', 'tif'):
            error = "outputForm must be one of: 'gif', 'jpg', 'png', or 'tif'"
            return self.abort(Error(ProcessCode.InvalidOutputType, error))
        auth = self.authorize()
        if auth in (Auth.OK, Auth.Unknown): return self._pdf2img()
        return self.authorize_error(auth)
    def _get_error(self, stdout):
        no_password = not self._have_password()
        return errors.get_error(self._logger.debug, no_password, stdout)
    def _get_image(self, input_name, output_file):
        with pdfprocess.Stdout() as stdout:
            options = self._parser.pdf2img_options + output_file.options
            args = ['pdf2img'] + options + [input_name, self.output_form]
            if subprocess.call(args, stdout=stdout):
                return self.abort(self._get_error(stdout))
        with open(output_file.name, 'rb') as image_file:
            image = base64.b64encode(image_file.read())
            return self.response(ProcessCode.OK, image)
    def _have_password(self):
        for option in self._parser.pdf2img_options:
            if option.startswith('-password='):
                return True
    def _log_request(self, parser_options):
        input_name = self.input_name
        if ' ' in input_name: input_name = '"%s"' % input_name
        options = ' '.join(parser_options)
        if options: options = ' ' + options
        self._logger.info('pdf2img%s %s %s %s' %
            (options, input_name, self.output_form, self.client))
    def _pdf2img(self):
        with tempfile.NamedTemporaryFile() as input_file:
            self.input.save(input_file)
            input_file.flush()
            input_name = input_file.name
            pages, output_form = (self.pages, self.output_form)
            with OutputFile(input_name, pages, output_form) as output_file:
                return self._get_image(input_name, output_file)
    @property
    def input_name(self): return self._input_name
    @property
    def multipage_request(self): return '-' in self.pages or ',' in self.pages
    @property
    def output_form(self): return self._parser.output_form
    @property
    def pages(self): return self._parser.pages

