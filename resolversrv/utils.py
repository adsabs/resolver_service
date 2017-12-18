#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask import current_app
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import and_

from resolversrv.models import DataLinks

def get_records(bibcode, link_type=None, link_sub_type=None):
    """
    Queries nonbib.datalinks table and returns results.

    :param bibcode:
    :param link_type:
    :param link_sub_type:
    :return: list of json records or None
    """
    try:
        with current_app.session_scope() as session:
            if link_type is None:
                rows = session.query(DataLinks).filter(and_(DataLinks.bibcode == bibcode)).all()
                msg = "Fetched records for bibcode = %s."
            elif link_sub_type is None:
                rows = session.query(DataLinks).filter(and_(DataLinks.bibcode == bibcode, DataLinks.link_type == link_type)).all()
                msg = "Fetched records for bibcode = %s and link type = %s."
            else:
                rows = session.query(DataLinks).filter(
                    and_(DataLinks.bibcode == bibcode, DataLinks.link_type == link_type,
                         DataLinks.link_sub_type == link_sub_type)).all()
                msg = "Fetched records for bibcode = %s, link type = %s and link sub type = %s."
            current_app.logger.debug(msg.format(bibcode, link_type, link_sub_type))
            results = []
            for row in rows:
                results.append(row.toJSON())
            return results
    except NoResultFound, e:
        if link_type is None:
            msg = "No records found for bibcode = %s."
        elif link_sub_type is None:
            msg = "No records found for bibcode = %s and link type = %s."
        else:
            msg = "No records found for bibcode = %s, link type = %s and link sub type = %s."
        current_app.logger.error(msg.format(bibcode, link_type, link_sub_type))
        current_app.logger.error('Error: ' + e)
        return None

