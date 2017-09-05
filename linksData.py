#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import current_app
import psycopg2
from config import config

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
    conn = None
    try:
        # read the connection parameters
        params = config()
        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        # submit the query to get the link URL
        cur.execute(query)
        rows = cur.fetchall()
        if len(rows) > 0:
            result = rows[0][0]
        # close communication with the PostgreSQL database server
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        current_app.logger.error(errorMsg, error)
    finally:
        if conn is not None:
            conn.close()
    return result
