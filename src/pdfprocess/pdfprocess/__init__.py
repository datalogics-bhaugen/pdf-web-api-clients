'API server'

import flask
import subprocess
import tempfile

import api_flask
from api_tempfile import OutputFile, StdFile

def authorize(request_form):
    # TODO: use 3scale
    api_key = request_form.get('apiKey', None)
    return api_key == 'f54ab5d8-5775-42c7-b888-f074ba892b57'

def authorize_error(request_form):
    pass # TODO: set code, etc.

def get_image(options, input_file_storage, page, output_form):
    with tempfile.NamedTemporaryFile() as input_file:
        input_file_storage.save(input_file)
        input_file.flush()
        with OutputFile(input_file.name, page, output_form) as output_file:
            return pdf2img(options, input_file, output_file, output_form)

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

def pdf2img(options, input_file, output_file, output_form):
    options += output_file.options
    args = ['pdf2img'] + options + [input_file.name, output_form]
    with StdFile() as stdout, StdFile() as stderr:
        exit_code = subprocess.call(args, stdout=stdout, stderr=stderr)
        if exit_code: pdf2img_error(exit_code, str(stdout), str(stderr))
    return flask.send_file(output_file.name)

def pdf2img_error(exit_code, stdout, stderr):
    app.logger.warning('exit_code: %d' % exit_code)
    if stdout: app.logger.debug('stdout: %s' % stdout)
    if stderr: app.logger.debug('stderr: %s' % stderr)
    flask.g.stdout = stdout # TODO: stderr
    flask.abort(500) # TODO: return different codes, etc.

app = api_flask.Application(__name__)

@app.before_first_request
def initialize():
    app.logger.info('%s started' % app.name)

@app.errorhandler(500)
def internal_server_error(error):
    return flask.g.stdout, 500

@app.route('/0/actions/image', methods=['POST'])
def image():
    request_form = flask.request.form
    options = get_options(request_form)
    output_form = request_form.get('outputForm', '')
    log_request(request_form, options, output_form)

    if not authorize(request_form):
        return authorize_error(request_form)

    input = flask.request.files['input']
    page = request_form.get('-pages', '1') # TODO: this seems bogus
    return get_image(options, input, page, output_form)

