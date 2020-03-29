import logging
from logging.config import dictConfig

from flask import Flask, request
from flask_cors import CORS

from listle import constants, models, utils
from listle.dispatch import dispatch

logger = logging.getLogger(__name__)


def create_app():
    dictConfig(constants.LOGGING_CONF)
    werkzeug_log = logging.getLogger('werkzeug')
    werkzeug_log.setLevel(logging.ERROR)

    app = Flask(__name__)
    CORS(app)

    app.before_request(utils.log_request)
    app.after_request(utils.log_response)

    @app.route('/', methods=('POST',))
    def create_record():
        record = models.Record(request)
        success, message = dispatch(record)

        response = {
            'success': success,
            'message': message
        }
        return response

    @app.route('/health', methods=('GET',))
    def health_check():
        return 'healthy'

    return app
