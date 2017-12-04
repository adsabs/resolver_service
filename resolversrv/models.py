#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import current_app
from sqlalchemy import Integer, String, Column, and_
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.exc import NoResultFound


Base = declarative_base()

class DataLinks(Base):
    __tablename__ = 'datalinks'
    __table_args__ = ({"schema": "nonbib"})
    bibcode = Column(String, primary_key=True)
    link_type = Column(String, primary_key=True)
    link_sub_type = Column(String, primary_key=True)
    url = Column(ARRAY(String))
    title = Column(ARRAY(String))
    item_count = Column(Integer)

    def __init__(self, bibcode, link_type, link_sub_type, url, title, item_count):
        """

        :param bibcode:
        :param link_type:
        :param link_sub_type:
        :param url:
        :param title:
        :param item_count:
        :return:
        """
        self.bibcode = bibcode
        self.link_type = link_type
        self.link_sub_type = link_sub_type
        self.url = url
        self.title = title
        self.item_count = item_count

    def toJSON(self):
        """

        :return: values formatted as python dict, if no values found returns empty structure, not None
        """
        return {
            'bibcode': self.bibcode,
            'link_type': self.link_type or '',
            'link_sub_type': self.link_sub_type or '',
            'url' : self.url or [''],
            'title': self.title or [''],
            'itemCount': self.item_count or 0,
        }


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
                msg = "Fetched records for bibcode = '{bibcode}'."
            elif link_sub_type is None:
                rows = session.query(DataLinks).filter(and_(DataLinks.bibcode == bibcode, DataLinks.link_type == link_type)).all()
                msg = "Fetched records for bibcode = '{bibcode}' and link type = '{link_type}'."
            else:
                rows = session.query(DataLinks).filter(and_(DataLinks.bibcode == bibcode, DataLinks.link_type == link_type, DataLinks.link_sub_type == link_sub_type)).all()
                msg = "Fetched records for bibcode = '{bibcode}', link type = '{link_type}' and link sub type = '{link_sub_type}'."
            current_app.logger.debug(msg.format(bibcode=bibcode, link_type=link_type, link_sub_type=link_sub_type))
            results = []
            for row in rows:
                results.append(row.toJSON())
            return results
    except NoResultFound, e:
        if link_type is None:
            msg = "No records found for bibcode = '{bibcode}'."
        elif link_sub_type is None:
            msg = "No records found for bibcode = '{bibcode}' and link type = '{link_type}'."
        else:
            msg = "No records found for bibcode = '{bibcode}', link type = '{link_type}' and link sub type = '{link_sub_type}'."
        current_app.logger.error(msg.format(bibcode=bibcode, link_type=link_type, link_sub_type=link_sub_type))
        current_app.logger.error('Error: ' + e)
        return None

