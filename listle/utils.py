import datetime
import logging
from datetime import datetime

from flask import current_app, request

from listle import constants

logger = logging.getLogger(__name__)


def log_request():
    logger.info(f'============================== REQUEST {request.method} {request.path} ==============================')
    logger.info(f'Request Headers: {dict(request.headers)}')
    logger.info(f'Request JSON: {request.json}')


def log_response(resp):
    logger.info(f'============================== RESPONSE {resp.status_code} ==============================')
    logger.info(f'Response Headers: {dict(resp.headers)}')
    return resp


def request_to_record(req):
    record = {
        'charset': request.charset,
        'url': request.url,
        'datetime': datetime.now().isoformat(),
        'headers': dict(request.headers),
        'body': request.json,
    }
    ua = request.user_agent

    record['user_agent'] = {
        'string': ua.string,
        'platform': ua.platform,
        'browser': ua.browser,
        'version': ua.version,
        'language': ua.language,
    }
