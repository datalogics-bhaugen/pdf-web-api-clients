"pdfprocess image action"

import os
import base64
import subprocess

import requests
import pdfprocess
from pdfprocess import Auth, Error, ProcessCode, UNKNOWN
from argument_parser import ArgumentParser
from output_file import OutputFile


class Action(pdfprocess.Action):
    def __init__(self, logger, request):
        pdfprocess.Action.__init__(self, logger, request)
        self._parser = ArgumentParser(self._log_request)
    def __call__(self):
        try:
            self._parser(self.options)
        except Error as error:
            self.raise_error(error)
        except Exception as exc:
            self.raise_error(Error(ProcessCode.InvalidSyntax, exc.message))
        auth = self.authorize()
        if auth != Auth.OK: self.raise_authorize_error(auth)
        return self._pdf2img()
    def _get_image(self, input_name, output_file):
        with pdfprocess.Stdout() as stdout:
            options = Action._options() + self._parser.pdf2img_options
            args = ['pdf2img'] + options + [input_name, self.output_form]
            if subprocess.call(args, stdout=stdout):
                self.raise_error(Action.get_error(stdout))
        with open(output_file.name, 'rb') as image_file:
            image = base64.b64encode(image_file.read())
            return pdfprocess.response(ProcessCode.OK, image)
    def _log_request(self, parser_options):
        options = ' '.join(parser_options)
        if options: options = ' ' + options
        output_form = self.output_form
        if output_form: output_form = ' ' + output_form
        info_args = (options, self.input_name, output_form, self.client)
        self.logger.info('pdf2img%s %s%s %s' % info_args)
    def _pdf2img(self):
        with pdfprocess.TemporaryFile() as input_file:
            self._save_input(input_file)
            input_file.flush()
            with OutputFile(input_file.name, self.output_form) as output_file:
                return self._get_image(input_file.name, output_file)
    @classmethod
    def _options(cls):
        if not pdfprocess.RESOURCE: return []
        resources = ('CMap', 'Font', 'Unicode')
        resources = [os.path.join(pdfprocess.RESOURCE, r) for r in resources]
        return ['-fontlist="%s"' % ';'.join(resources)]
    @property
    def output_form(self): return self._parser.output_form
    @property
    def pages(self): return self._parser.pages

class Get(Action):
    def _save_input(self, input_file):
        input_file.write(self.input)
    def _set_input(self, request):
        url = request.form.get('inputURL', None)
        if not url:
            self.raise_error(Error(ProcessCode.InvalidInput, 'no input'))
        try:
            self._input = requests.get(url).content
        except Exception as exception:
            self.raise_error(Error(ProcessCode.InvalidInput, str(exception)))
        Action._set_input(self, request, os.path.basename(url))

class Post(Action):
    def _save_input(self, input_file):
        self.input.save(input_file)
    def _set_input(self, request):
        request_files = request.files.values()
        if not request_files:
            self.raise_error(Error(ProcessCode.InvalidInput, 'no input'))
        if len(request_files) > 1:
            self.raise_error(Error(ProcessCode.InvalidInput, 'excess input'))
        self._input = request_files[0]
        Action._set_input(self, request)
