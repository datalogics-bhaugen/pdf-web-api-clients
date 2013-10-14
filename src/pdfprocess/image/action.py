"pdfprocess image action"

import os
import base64
import subprocess

import requests
import pdfprocess
from pdfprocess import Auth, Error, ProcessCode, UNKNOWN, logger
from argument_parser import ArgumentParser
from output_file import OutputFile


class Action(pdfprocess.Action):
    def __init__(self, request):
        pdfprocess.Action.__init__(self, request)
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
        logger.info('pdf2img%s %s%s %s' % info_args)
    def _pdf2img(self):
        with pdfprocess.TemporaryFile() as input_file:
            self._save_input(input_file)
            with OutputFile(input_file.name, self.output_form) as output_file:
                return self._get_image(input_file.name, output_file)
    @classmethod
    def from_request(cls, request):
        action = FromURL if request.form.get('inputURL', None) else FromFile
        return action(request)
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

class FromFile(Action):
    def _save_input(self, input_file):
        self.input.save(input_file)
    def _set_input(self, request):
        request_files = request.files.values()
        if not request_files:
            error = 'no inputURL or request file'
            self.raise_error(Error(ProcessCode.InvalidInput, error))
        if len(request_files) > 1:
            error = 'excess input: %d files' % len(request_files)
            self.raise_error(Error(ProcessCode.InvalidInput, error))
        self._input = request_files[0]
        Action._set_input(self, request)

class FromURL(Action):
    def _save_input(self, input_file):
        input_file.write(self.input)
    def _set_input(self, request):
        if request.files.values():
            error = 'excess input: inputURL and request file'
            self.raise_error(Error(ProcessCode.InvalidInput, error))
        input_url = request.form.get('inputURL')
        try:
            self._input = requests.get(input_url).content
        except Exception as exception:
            self.raise_error(Error(ProcessCode.InvalidInput, str(exception)))
        Action._set_input(self, request, os.path.basename(input_url))
