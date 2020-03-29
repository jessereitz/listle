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
    'from_email': 'jesse@notifyless.com',
    'host': 'smtp.mailgun.org',
    'port': 465,
    'user': 'temp@mg.notifyless.com',
    'password': '386171e0ac3a1b2080dd34289a4718b3-ed4dc7c4-9472290f',
}
