#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import inspect

from sqlalchemy import create_engine, Integer, String, Column, and_
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.orm.exc import NoResultFound

from adsmutils import load_config, setup_logging

import resolversrv

config = {}
config.update(load_config(proj_home = os.path.dirname(inspect.getsourcefile(resolversrv))))
logger = setup_logging('resolver_service')

engine = create_engine(config['SQLALCHEMY_DATABASE_URI'])
Base = declarative_base(engine)

db_session = scoped_session(sessionmaker())
db_session.configure(bind=engine)
db_session.execute('set search_path to nonbib')


class DataLinks(Base):
    __tablename__ = 'datalinks'
    bibcode = Column(String, primary_key=True)
    link_type = Column(String, primary_key=True)
    link_sub_type = Column(String, primary_key=True)
    url = Column(ARRAY(String))
    title = Column(ARRAY(String))
    item_count = Column(Integer)

    def __init__(self, bibcode, link_type, link_sub_type, url, title, item_count):
        self.bibcode = bibcode
        self.link_type = link_type
        self.link_sub_type = link_sub_type
        self.url = url
        self.title = title
        self.item_count = item_count

    def toJSON(self):
        """Returns value formatted as python dict."""
        return {
            'bibcode': self.bibcode,
            'link_type': self.link_type or None,
            'link_sub_type': self.link_sub_type or None,
            'url' : self.url or None,
            'title': self.title or None,
            'itemCount': self.item_count or None,
        }

    def get_bibcode(self):
        if (self.bibcode):
            return ''.join(self.bibcode)
        return None

    def get_count(self):
        if (self.url):
            return len(self.url)
        return 0

    def get_url(self):
        if (self.url):
            return ''.join(self.url)
        return None

    def get_url_elem(self, idx):
        if (self.url):
            return self.url[idx]
        return None

    def get_title(self):
        if (self.title):
            return ''.join(self.title)
        return None

    def get_title_elem(self, idx):
        if (self.title):
            return self.title[idx]
        return None

def get_records(bibcode, link_type, link_sub_type=None):
    """
    Queries nonbib.datalinks table and returns results.
    
    :param bibcode: 
    :param link_type: 
    :param link_sub_type: 
    """
    try:
        if not link_sub_type:
            rows = db_session.query(DataLinks).filter(and_(DataLinks.bibcode == bibcode, DataLinks.link_type == link_type)).all()
            msg = "Fetched records for bibcode = '{bibcode}' and link type = '{link_type}'."
        else:
            rows = db_session.query(DataLinks).filter(DataLinks.link_type == link_type, DataLinks.link_sub_type == link_sub_type).all()
            msg = "Fetched records for bibcode = '{bibcode}', link type = '{link_type}' and link sub type = '{link_sub_type}'."
        logger.debug(msg.format(bibcode=bibcode, link_type=link_type, link_sub_type=link_sub_type))
        return rows
    except NoResultFound:
        if not link_sub_type:
            msg = "No records found for bibcode = '{bibcode}' and link type = '{link_type}'."
        else:
            msg = "No records found for bibcode = '{bibcode}', link type = '{link_type}' and link sub type = '{link_sub_type}'."
        logger.error(msg.format(bibcode=bibcode, link_type=link_type, link_sub_type=link_sub_type))
        return None
