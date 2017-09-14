#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import current_app
from sqlalchemy import create_engine
import sqlalchemy.exc

def getURL(bibcode, linkType):
    query = "SELECT url FROM nonbib.datalinks WHERE bibcode = '{}' AND " \
            "(link_type = '{}' OR link_sub_type = '{}')".format(bibcode, linkType, linkType)
    errorMsg = "Exception Error while fetching url for bibcode = '{}' and link type = '{}': ".format(bibcode, linkType)
    return executeQuery(query, errorMsg)

def getURLandTitle(bibcode, linkType):
    query = "SELECT url,title FROM nonbib.datalinks WHERE bibcode = '{}' AND link_type = '{}'".format(bibcode, linkType)
    errorMsg = "Exception Error while fetching url, title for bibcode = '{}' and link type = '{}': ".format(bibcode, linkType)
    print executeQuery(query, errorMsg)

# data = {}
#         data['id'] = 'ITEM-{0}'.format(index + 1)
#         data['author'] = self.__getCSLAuthorList(aDoc)
#         data['type'] = self.__getDocType(aDoc.get('doctype', ''))
#         return data


def executeQuery(query,errorMsg):
    result = ""
    try:
        engine = create_engine(current_app.config['SQLALCHEMY_URL'])
        conn = engine.connect()

        # submit the query to get the link URL
        rows = conn.execute(query).fetchall()
        print '-------------', rows
        if len(rows) > 0:
            result = rows[0][0]

    except (Exception, sqlalchemy.exc.DatabaseError) as error:
        current_app.logger.error(errorMsg, error)

    return result
