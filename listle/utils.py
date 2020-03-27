import logging

from flask import request

logger = logging.getLogger(__name__)


def log_request():
    logger.info(f'============================== REQUEST {request.method} {request.path} ==============================')
    logger.info(f'Request Headers: {dict(request.headers)}')
    logger.info(f'Request JSON: {request.json}')


def log_response(resp):
    logger.info(f'============================== RESPONSE {resp.status_code} ==============================')
    logger.info(f'Response Headers: {dict(resp.headers)}')
    return resp
