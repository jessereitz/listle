import logging
from logging.config import dictConfig

from flask import Flask, request
from flask_cors import CORS

from listle import constants, models, utils

logging.config.dictConfig(constants.LOGGING_CONF)


def create_app():
    werkzeug_log = logging.getLogger('werkzeug')
    werkzeug_log.setLevel(logging.ERROR)

    app = Flask(__name__)
    CORS(app)

    app.before_request(utils.log_request)
    app.after_request(utils.log_response)

    @app.route('/', methods=('GET',))
    def index():
        return "success"

    @app.route('/', methods=('POST',))
    def create_record():
        record = models.Record(request)
        print(dict(record))
        response = 'success'
        return response

    return app
