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

SQLALCHEMY_URL = 'postgresql://postgres:postgres@localhost:15432/data_pipeline'

URL_QUERY = "SELECT url FROM {db}.datalinks WHERE bibcode = '{bibcode}' AND (link_type = '{linkType}')"
URL_QUERY_ERROR_MSG = "Exception Error while fetching url for bibcode = '{bibcode}' and link type = '{linkType}': "
URL_WITH_SUB_TYPE_QUERY = "SELECT url FROM {db}.datalinks WHERE bibcode = '{bibcode}' AND (link_type = '{linkType}' AND link_sub_type = '{linkSubType}')"
URL_WITH_SUB_TYPE_QUERY_ERROR_MSG = "Exception Error while fetching url for bibcode = '{bibcode}' and link type = '{linkType}' and link sub type = '{linkSubType}': "
URL_TITLE_QUERY = "SELECT url,title FROM {db}.datalinks WHERE bibcode = '{bibcode}' AND link_type = '{linkType}' ORDER BY url"
URL_TITLE_QUERY_ERROR_MSG = "Exception Error while fetching url, title for bibcode = '{bibcode}' and link type = '{linkType}': "
URL_TITLE_WITH_SUB_TYPE_QUERY = "SELECT url,title FROM {db}.datalinks WHERE bibcode = '{bibcode}' AND link_type = '{linkType}' AND link_sub_type = '{linkSubType}' ORDER BY url"
URL_TITLE_WITH_SUB_TYPE_QUERY_ERROR_MSG = "Exception Error while fetching url, title for bibcode = '{bibcode}' and link type = '{linkType}' with link sub type = '{linkSubType}': "

# This is the URL to communicate with resolver_gateway api
RESOLVER_GATEWAY_URL = 'http://localhost:5000/resolver/{bibcode}/{linkType}/{URL}'
RESOLVER_GATEWAY_URL_TEST = '/resolver/{bibcode}/{linkType}/{URL}'
