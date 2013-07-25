'API server application class'

import api_logger
import flask

class Application(flask.Flask):
    def __init__(self, name):
        flask.Flask.__init__(self, name)
        api_logger.configure(name, self.logger)

