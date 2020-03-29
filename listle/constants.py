import os

LOGGING_CONF = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'basic': {
            'format': '[%(asctime)s|%(levelname)s|%(module)s|%(lineno)d] %(message)s'
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'basic',
        },
    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'propagate': True,
            'level': 'INFO'
        },
    },
}

EMAIL_CONNECTOR_CONFIG = {
    'from_email': os.getenv('FROM_EMAIL'),
    'to_email': os.getenv('TO_EMAIL'),
    'host': os.getenv('EMAIL_HOST'),
    'port': os.getenv('EMAIL_PORT'),
    'user': os.getenv('EMAIL_USER'),
    'password': os.getenv('EMAIL_PASSWORD'),
}

ENABLED_CONNECTORS = os.getenv('ENABLED_CONNECTORS', '').split(',')
