import logging

from listle import constants
from listle.connectors import EmailConnector, FirestoreConnector


logger = logging.getLogger(__name__)


def get_connectors():
    connectors = []
    enabled = constants.ENABLED_CONNECTORS
    if 'email' in enabled:
        connectors.append(EmailConnector)

    if 'firestore' in enabled:
        connectors.append(FirestoreConnector)

    yield from connectors


def dispatch(record):
    success = True
    message = None
    for connector_class in get_connectors():
        c = connector_class(record)
        try:
            c.dispatch()
        except Exception as e:
            logger.exception(e)
            success = False
            message = str(e)
    return success, message
