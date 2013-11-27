"WebAPI pdf2img action"

import os
import subprocess

import flask
import requests

import server
import options
import translator
from server import Error, ErrorCode, UNKNOWN, logger
from argument_parser import ArgumentParser
from output_file import OutputFile


class Action(server.Action):
    TYPE = 'RenderPages'
    OPTIONS = options.OPTIONS + translator.OPTIONS
    def __call__(self):
        self._parser = ArgumentParser()
        try:
            self._parser(self.options)
            self._set_input()
        except Error as error:
            self.raise_error(error)
        except Exception as exc:
            self.raise_error(Error(ErrorCode.InvalidSyntax, exc.message))
        self.client.authorize()
        return self._pdf2img()
    def _content_type(self):
        image_type = self.output_format.lower()
        if image_type == 'jpg': image_type = 'jpeg'
        if image_type == 'tif': image_type = 'tiff'
        return u'image/{}'.format(image_type)
    def _get_image(self, input_name, output_file):
        with server.Stdout() as stdout:
            options = Action._options() + self._parser.pdf2img_options
            if self.password:
                options += [u'-password={}'.format(self.password)]
            args = ['pdf2img'] + options + [input_name, self.output_format]
            if subprocess.call(args, stdout=stdout):
                self.raise_error(Action.get_error(stdout))
        with open(output_file.name, 'rb') as image_file:
            content_type = self._content_type()
            return flask.Response(image_file.read(), content_type=content_type)
    def _pdf2img(self):
        with server.TemporaryFile() as input_file:
            self._save_input(input_file)
            with OutputFile(input_file.name, self.output_format) as output:
                return self._get_image(input_file.name, output)
    @classmethod
    def from_request(cls, request):
        action = FromURL if request.form.get('inputURL', None) else FromFile
        return action(request)
    @classmethod
    def _options(cls):
        if not server.RESOURCE: return []
        resources = ('CMap', 'Font', 'Unicode')
        resources = [os.path.join(server.RESOURCE, r) for r in resources]
        return [u'-fontlist="{}"'.format(';'.join(resources))]
    @property
    def output_format(self): return self._parser.output_format
    @property
    def pages(self): return self._parser.pages

class FromFile(Action):
    def _save_input(self, input_file):
        self.input.save(input_file)
    def _set_input(self):
        if not self.request_files:
            error = 'no inputURL or request file'
            self.raise_error(Error(ErrorCode.InvalidInput, error))
        if len(self.request_files) > 1:
            error = u'excess input ({} files)'.format(len(self.request_files))
            self.raise_error(Error(ErrorCode.InvalidInput, error))
        self._input = self.request_files[0]

class FromURL(Action):
    def _save_input(self, input_file):
        input_file.write(self.input)
    def _set_input(self):
        if self.request_files:
            error = 'excess input (inputURL and request file)'
            self.raise_error(Error(ErrorCode.InvalidInput, error))
        try:
            self._input = requests.get(self.input_url).content
        except Exception as exception:
            self.raise_error(Error(ErrorCode.InvalidInput, unicode(exception)))
