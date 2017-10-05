#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import current_app
from sqlalchemy import create_engine
import sqlalchemy.exc

from adsputils import load_config, setup_logging

logger = None
config = {}

# query for url
def getURL(bibcode, linkType, linkSubType='', db='nonbib'):
    if (len(linkSubType) == 0):
        query = current_app.config['URL_QUERY'].format(db=db, bibcode=bibcode, linkType=linkType)
        errorMsg = current_app.config['URL_QUERY_ERROR_MSG'].format(bibcode=bibcode, linkType=linkType)
    else:
        query = current_app.config['URL_WITH_SUB_TYPE_QUERY'].format(db=db, bibcode=bibcode, linkType=linkType, linkSubType=linkSubType)
        errorMsg = current_app.config['URL_WITH_SUB_TYPE_QUERY_ERROR_MSG'].format(bibcode=bibcode, linkType=linkType, linkSubType=linkSubType)
    return executeQuery(query, errorMsg)


# query for url and title
def getURLandTitle(bibcode, linkType, linkSubType='', db='nonbib'):
    if (len(linkSubType) == 0):
        query = current_app.config['URL_TITLE_QUERY'].format(db=db, bibcode=bibcode, linkType=linkType)
        errorMsg = current_app.config['URL_TITLE_QUERY_ERROR_MSG'].format(bibcode=bibcode, linkType=linkType)
    else:
        query = current_app.config['URL_TITLE_WITH_SUB_TYPE_QUERY'].format(db=db, bibcode=bibcode, linkType=linkType, linkSubType=linkSubType)
        errorMsg = current_app.config['URL_TITLE_WITH_SUB_TYPE_QUERY_ERROR_MSG'].format(bibcode=bibcode, linkType=linkType, linkSubType=linkSubType)
    return executeQuery(query, errorMsg)


def executeQuery(query,errorMsg):

    global logger
    global config

    if logger == None:
        config.update(load_config())
        logger = setup_logging('resolver_service', config.get('LOG_LEVEL', 'INFO'))

    try:
        engine = create_engine(current_app.config['SQLALCHEMY_URL'])

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
        logger.info(errorMsg + error)

    return ""
