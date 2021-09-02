
from sqlalchemy import Integer, String, Column
from sqlalchemy.dialects.postgresql import ARRAY, JSONB
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

# DataLinks is db v1.0
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


# Documents is db v2.0
class Documents(Base):
    __tablename__ = 'documents'
    bibcode = Column(String, primary_key=True)
    identifier = Column(ARRAY(String), default=list)
    links = Column(JSONB, default=dict)

    def __init__(self, bibcode, identifier, links):
        """

        :param bibcode:
        :param identifier:
        :param links:
        """
        self.bibcode = bibcode
        self.identifier = identifier
        self.links = links

    def toJSON(self):
        """

        :return: values formatted as python dict, if no values found returns empty structure, not None
        """
        docs = []
        for link_type, unknown in self.links.items():
            if isinstance(unknown, bool):
                docs.append({
                    'bibcode': self.bibcode,
                    'link_type': link_type,
                    'link_sub_type': '',
                    'url': [''],
                    'title': [''],
                })
            # is doi or arxiv, so save the ids in url
            elif isinstance(unknown, list):
                docs.append({
                    'bibcode': self.bibcode,
                    'link_type': link_type,
                    'link_sub_type': '',
                    'url' : unknown,
                    'title': [''],
                })
            elif isinstance(unknown, dict):
                if 'url' in list(unknown.keys()):
                    # url and title, and possibly count, but does not have sub_type
                    docs.append({
                        'bibcode': self.bibcode,
                        'link_type': link_type,
                        'link_sub_type': None,
                        'url': unknown.get('url', []),
                        'title': unknown.get('title', []),
                        'itemCount': int(unknown.get('count', len(unknown.get('url', [])))),
                    })
                else:
                    # having link_sub_type
                    for link_sub_type, value in unknown.items():
                        if isinstance(value, dict):
                            docs.append({
                                'bibcode': self.bibcode,
                                'link_type': link_type,
                                'link_sub_type': link_sub_type,
                                'url': value.get('url',[]),
                                'title': value.get('title',[]),
                                'itemCount': int(value.get('count', len(value.get('url',[])))),
                            })
        return docs