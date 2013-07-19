#!/usr/bin/env python

'mock pdf2img server'

import flask
import logging
from logging.handlers import TimedRotatingFileHandler
import subprocess

def make_file_handler():
    rotate_daily = 'D'
    return TimedRotatingFileHandler('%s.log' % app.name, rotate_daily)

app = flask.Flask(__name__)
app.logger.addHandler(make_file_handler())
app.logger.setLevel(logging.INFO)
app.logger.info('%s started' % __doc__)

def get_options(request_form):
    result = ''
    for arg, value in request_form.iteritems():
        if arg not in ('apiKey', 'inputFile', 'outputForm'):
            result += ' ' + arg
            if value != 'True': result += ' ' + value
    return result

def log_request(request_form):
    app.logger.debug('request.form: %s' % request_form)
    input_file = request_form.get('inputFile', None)
    output_form = request_form.get('outputForm', None)
    options = get_options(request_form)
    app.logger.info('pdf2img%s %s %s' % (options, input_file, output_form))

def authenticate(request_form):
    api_key = request_form.get('apiKey', None)
    return api_key == 'f54ab5d8-5775-42c7-b888-f074ba892b57'

@app.route('/0/actions/pdf2img', methods=['POST'])
def pdf2img():
    log_request(flask.request.form)
    if authenticate(flask.request.form):
        #TODO: condense with log_request to do this once
        input_file = flask.request.form.get('inputFile', None)
        output_form = flask.request.form.get('outputForm', None)
        options = get_options(flask.request.form)
        subprocess.call(["pdf2img", input_file, output_form])
        if input_file.endswith(".pdf"):
            input_file = input_file[:-len(".pdf")]
        output_file = (input_file + "_1." + output_form)
        return flask.send_file(output_file)
    # TODO: Deal with multipage output
    # TODO: Delete returned files from server
    # TODO: return error

if __name__ == '__main__':
    app.run(host='0.0.0.0')

