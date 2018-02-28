
from sqlalchemy import Integer, String, Column
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

class DataLinks(Base):
    __tablename__ = 'datalinks'
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
