# -*- coding: utf-8 -*-
"""
    resolver_services.models
    ~~~~~~~~~~~~~~~~~~~~~

    Models for the data stored by the resolver sercie
"""
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Integer, String, Column, Text

Base = declarative_base()


class Record(Base):
    __tablename__ = 'records'
    id = Column(Integer, primary_key=True)
    bibcode = Column(String(19))
    link_type = Column(String(255))
    link_subtype = Column(String(255))
    title = Column(Text)
    
    def toJSON(self):
        """Returns value formatted as python dict."""
        return {
            'id': self.id,
            'bibcode': self.bibcode,
            'link_type': self.link_type or None,
            'link_subtype': self.link_subtype or None,
            'title': self.title or None
        }