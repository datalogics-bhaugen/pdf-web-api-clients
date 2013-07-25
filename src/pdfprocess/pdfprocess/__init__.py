'API server'

import api_flask

import flask
import os
import subprocess
import tempfile

class OutputFile(object):
    '''
    pdf2img appends a page count to the output filename, so we cannot
    use tempfile to construct the output file. instead, we assume that
    pdf2img successfully created the output file from the temporary
    file we provided as input. this class encapsulates all this logic,
    and deletes the temporary files created by pdf2img.
    '''
    def __init__(self, name, extension, page):
        self._name = '%s%s.%s' % (name, page, extension) # no underscore!
    def __enter__(self):
        return self
    def __exit__(self, type, value, traceback):
        try: os.remove(self.name)
        except OSError as error: pass
    @property
    def name(self): return self._name
    @property
    def options(self): return ['-digits=1']

def authorize(request_form):
    # TODO: use 3scale
    api_key = request_form.get('apiKey', None)
    return api_key == 'f54ab5d8-5775-42c7-b888-f074ba892b57'

def authorize_error(request_form):
    pass # TODO: set code, etc.

def get_image(options, input_file_storage, output_form, page):
    with tempfile.NamedTemporaryFile() as input_file:
        input_file_storage.save(input_file)
        input_file.flush()
        with OutputFile(input_file.name, output_form, page) as output_file:
            options += output_file.options
            args = ['pdf2img'] + options + [input_file.name, output_form]
            exit_code = subprocess.call(args)
            if exit_code: app.logger.warning('exit_code: %d' % exit_code)
            return flask.send_file(output_file.name)

def get_options(request_form):
    options = []
    for key, value in request_form.iteritems():
        if key not in ('apiKey', 'inputFile', 'outputForm'):
            options.append(key if value == 'True' else '%s=%s' % (key, value))
    return options

def log_request(request_form, options, output_form):
    options = ' '.join(options)
    if options: options = ' ' + options
    input_file = request_form.get('inputFile', '<anon>')
    app.logger.info('pdf2img%s %s %s' % (options, input_file, output_form))

app = api_flask.Application(__name__)

@app.before_first_request
def initialize():
    app.logger.info('%s started' % app.name)

@app.route('/0/actions/image', methods=['POST'])
def image():
    request_form = flask.request.form
    options = get_options(request_form)
    output_form = request_form.get('outputForm', '')
    log_request(request_form, options, output_form)

    if not authorize(request_form):
        return authorize_error(request_form)

    input = flask.request.files['input']
    # TODO: pages option is required, no default
    page = request_form.get('-pages', '1')
    return get_image(options, input, output_form, page)

