#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os

PROJECT_HOME = os.path.abspath(os.path.join(os.path.dirname(__file__), '.'))
sys.path.append(PROJECT_HOME)

from sqlalchemy import create_engine
import sqlalchemy.exc

from adsputils import load_config, setup_logging

logger = None
config = {}

# query for url
def getURL(bibcode, linkType, linkSubType='', db='nonbib'):
    global logger
    global config

    if logger == None:
        config.update(load_config())
        logger = setup_logging('resolver_service', config.get('LOG_LEVEL', 'INFO'))

    if (len(linkSubType) == 0):
        query = config['URL_QUERY'].format(db=db, bibcode=bibcode, linkType=linkType)
        errorMsg = config['URL_QUERY_ERROR_MSG'].format(bibcode=bibcode, linkType=linkType)
    else:
        query = config['URL_WITH_SUB_TYPE_QUERY'].format(db=db, bibcode=bibcode, linkType=linkType, linkSubType=linkSubType)
        errorMsg = config['URL_WITH_SUB_TYPE_QUERY_ERROR_MSG'].format(bibcode=bibcode, linkType=linkType, linkSubType=linkSubType)
    return executeQuery(query, errorMsg)


# query for url and title
def getURLandTitle(bibcode, linkType, linkSubType='', db='nonbib'):
    global logger
    global config

    if logger == None:
        config.update(load_config(proj_home=PROJECT_HOME))
        logger = setup_logging('resolver_service', config.get('LOG_LEVEL', 'INFO'))

    if (len(linkSubType) == 0):
        query = config['URL_TITLE_QUERY'].format(db=db, bibcode=bibcode, linkType=linkType)
        errorMsg = config['URL_TITLE_QUERY_ERROR_MSG'].format(bibcode=bibcode, linkType=linkType)
    else:
        query = config['URL_TITLE_WITH_SUB_TYPE_QUERY'].format(db=db, bibcode=bibcode, linkType=linkType, linkSubType=linkSubType)
        errorMsg = config['URL_TITLE_WITH_SUB_TYPE_QUERY_ERROR_MSG'].format(bibcode=bibcode, linkType=linkType, linkSubType=linkSubType)
    return executeQuery(query, errorMsg)


def executeQuery(query,errorMsg):

    try:
        engine = create_engine(config['SQLALCHEMY_URL'])

        conn = engine.connect()
        rows = conn.execute(query).fetchall()
        results = []
        for row in rows:
            if (len(row) == 1):
                results.append(''.join(row[0]))
            else:
                for item in zip(*row):
                    results.append(item)
        conn.close()
        engine.dispose()

        return results

    except (Exception, sqlalchemy.exc.DatabaseError) as error:
        logger.info(errorMsg + str(error))

    return ""
