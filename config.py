#!/usr/bin/python
# -*- coding: utf-8 -*-

import os

# In what environment are we?
ENVIRONMENT = os.getenv('ENVIRONMENT', 'staging').lower()
# Configure logging
RESOLVER_SERVICE_LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            'format': '%(levelname)s\t%(process)d '
                      '[%(asctime)s]:\t%(message)s',
            'datefmt': '%m/%d/%Y %H:%M:%S',
        }
    },
    'handlers': {
        'file': {
            'formatter': 'default',
            'level': 'INFO',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': '/tmp/resolver_service_app.{}.log'.format(ENVIRONMENT),
        },
        'console': {
            'formatter': 'default',
            'level': 'INFO',
            'class': 'logging.StreamHandler'
        },
    },
    'loggers': {
        '': {
            'handlers': ['file','console'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}

SQLALCHEMY_URL = 'postgresql://dbo:gs@localhost/mydb'
