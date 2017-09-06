#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import current_app
from sqlalchemy import create_engine
import sqlalchemy.exc

def getURL(bibcode, linkType):
    query = "SELECT linkURL FROM linkInfo as I INNER JOIN linkTypes as T ON I.linkTypeId = T.linkTypeID WHERE I.bibcode = '{}' AND T.linkTypeName = '{}'".format(bibcode, linkType)
    errorMsg = "Exception Error while fetching linkURL for bibcode = '{}' and link type = '{}': ".format(bibcode, linkType)
    return executeQuery(query, errorMsg)

def getLinkTag(linkTypeName):
    query = "SELECT linkTypeTag FROM linkTypes WHERE linkTypeName = '{}'".format(linkTypeName)
    errorMsg = "Exception Error while fetching the tag for link type name = '{}'".format(linkTypeName)
    return executeQuery(query, errorMsg)

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
