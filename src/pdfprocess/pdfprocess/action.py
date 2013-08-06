"pdfprocess action"

import ThreeScalePY
import flask


class Action(object):
    def __init__(self, logger, request):
        self._input = request.files['input']
        self._logger = logger
        self._request_form = request.form
    def abort(self, process_code, text, status_code=500):
        self.logger.error('%s: %s' % (process_code, text))
        return self.response(status_code, process_code, text)
    def authorize(self): # TODO: use 3scale
        api_key = self.request_form.get('apiKey', None)
        return api_key == 'f54ab5d8-5775-42c7-b888-f074ba892b57'
    def authorize_error(self):
        # TODO: also used for bad/missing document password error?
        return self.abort(1013, 'TODO: bad apiKey or rate limit', 423)
    @classmethod
    def response(cls, status_code, process_code, output):
        json = flask.jsonify(processCode=process_code, output=output)
        return json, status_code
    @property
    def input(self): return self._input
    @property
    def logger(self): return self._logger
    @property
    def request_form(self): return self._request_form

