import logging
from logging.config import dictConfig

from flask import Flask, request
from flask_cors import CORS

from listle import constants, models, utils
from listle.connectors import EmailConnector, FirestoreConnector


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
        logger.info("creating")
        record = models.Record(request)
        # ec = EmailConnector(record)
        # ec.send_message()
        fsc = FirestoreConnector(record)
        fsc.dispatch()
        response = 'success'
        return response

    return app
