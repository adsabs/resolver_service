import sys, os
project_home = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../'))
if project_home not in sys.path:
    sys.path.insert(0, project_home)

from flask_testing import TestCase
import unittest
import testing.postgresql
import json

from adsmsg.nonbibrecord import DataLinksRecordList

import resolversrv.app as app
from resolversrv.models import DataLinks, Base
from resolversrv.utils import get_records, add_records
from resolversrv.views import LinkRequest, PopulateRequest

TestCase.maxDiff = None

class test_database(TestCase):
    """tests for generation of resolver"""

    postgresql_url_dict = {
        'port': 1234,
        'host': '127.0.0.0',
        'user': 'postgres',
        'database': 'testdb'
    }
    postgresql_url = 'postgresql://{user}:{user}@{host}:{port}/{database}' \
        .format(
        user=postgresql_url_dict['user'],
        host=postgresql_url_dict['host'],
        port=postgresql_url_dict['port'],
        database=postgresql_url_dict['database']
    )

    def create_app(self):
        '''Start the wsgi application'''
        a = app.create_app(**{
            'SQLALCHEMY_DATABASE_URI': self.postgresql_url,
            'SQLALCHEMY_ECHO': False,
            'TESTING': True,
            'PROPAGATE_EXCEPTIONS': True,
            'TRAP_BAD_REQUEST_ERRORS': True
        })
        return a

    @classmethod
    def setUpClass(cls):
        cls.postgresql = \
            testing.postgresql.Postgresql(**cls.postgresql_url_dict)

    @classmethod
    def tearDownClass(cls):
        cls.postgresql.stop()

    def setUp(self):
        Base.metadata.create_all(bind=self.app.db.engine)

    def tearDown(self):
        self.app.db.session.remove()
        Base.metadata.drop_all(bind=self.app.db.engine)

    # postgresql = None
    #
    # def create_app(self):
    #     """
    #     Get the url from in-memory db and pass it to app to create test AlchemySQL db.
    #     :return:
    #     """
    #     current_app = app.create_app(**{'SQLALCHEMY_DATABASE_URI': 'postgresql://postgres:postgres@localhost:1234/testdb'})
    #     return current_app


    # def setUp(self):
    #     """
    #     Module level set-up called once before any tests in this file are executed.
    #     Creates a temporary database and populates it.
    #     :return:
    #     """
    #     Base.metadata.create_all(bind=self.app.db.engine)
    #     self.addStubData()
    #
    #
    # def tearDown(self):
    #     """
    #     Called after once after each test in this file have been executed.
    #     Closes the database connection and destroy the temporary database.
    #     :return:
    #     """
    #     self.app.db.session.remove()
    #     self.app.db.drop_all()


    def addStubData(self):
        """
        Add stub data
        :return:
        """
        stub_data = [
                        ('2013MNRAS.435.1904M', 'ESOURCE',      'EPRINT_HTML', ['http://arxiv.org/abs/1307.6556'], [], 0),
                        ('2013MNRAS.435.1904M', 'ESOURCE',      'EPRINT_PDF',  ['http://arxiv.org/pdf/1307.6556'], [], 0),
                        ('2013MNRAS.435.1904M', 'ESOURCE',      'PUB_HTML',    ['http://dx.doi.org/10.1093%2Fmnras%2Fstt1379'], [], 0),
                        ('2013MNRAS.435.1904M', 'ESOURCE',      'PUB_PDF',     ['http://mnras.oxfordjournals.org/content/435/3/1904.full.pdf'], [], 0),
                        ('2013MNRAS.435.1904M', 'DATA',         'CXO',         ['http://cda.harvard.edu/chaser?obsid=494'], ['Chandra Data Archive ObsIds 494'], 27),
                        ('2013MNRAS.435.1904M', 'DATA',         'ESA',         ['http://archives.esac.esa.int/ehst/#bibcode=2013MNRAS.435.1904M'], ['European HST References (EHST)'], 1),
                        ('2013MNRAS.435.1904M', 'DATA',         'HEASARC',     ['http://heasarc.gsfc.nasa.gov/cgi-bin/W3Browse/biblink.pl?code=2013MNRAS.435.1904M'], [], 1),
                        ('2013MNRAS.435.1904M', 'DATA',         'Herschel',    ['http://herschel.esac.esa.int/hpt/publicationdetailsview.do?bibcode=2013MNRAS.435.1904M'], [], 1),
                        ('2013MNRAS.435.1904M', 'DATA',         'MAST',        ['http://archive.stsci.edu/mastbibref.php?bibcode=2013MNRAS.435.1904M'], ['MAST References (GALEX EUVE HST)'], 3),
                        ('2013MNRAS.435.1904M', 'DATA',         'NED',         ['http://$NED$/cgi-bin/nph-objsearch?search_type=Search&refcode=2013MNRAS.435.1904M'], ['NED Objects (1)'], 1),
                        ('2013MNRAS.435.1904M', 'DATA',         'SIMBAD',      ['http://$SIMBAD$/simbo.pl?bibcode=2013MNRAS.435.1904M'], ['SIMBAD Objects (30)'], 30),
                        ('2013MNRAS.435.1904M', 'DATA',         'XMM',         ['http://nxsa.esac.esa.int/nxsa-web/#obsid=0097820101'], ['XMM-Newton Observation Number 0097820101'], 1),
                        ('2017MNRAS.467.3556B', 'PRESENTATION', '',            ['http://www.astro.lu.se/~alexey/animations.html'], [], 0),
                        ('1943RvMP...15....1C', 'INSPIRE',      '',            ['http://inspirehep.net/search?p=find+j+RMPHA,15,1'], [], 0),
                        ('1971ATsir.615....4D', 'ASSOCIATED',   '',            ['1971ATsir.615....4D', '1974Afz....10..315D', '1971ATsir.621....7D', '1976Afz....12..665D', '1971ATsir.624....1D', '1983Afz....19..229D', '1983Ap.....19..134D', '1973ATsir.759....6D', '1984Afz....20..525D', '1984Ap.....20..290D', '1974ATsir.809....1D', '1974ATsir.809....2D', '1974ATsir.837....2D'], ['Part  1', 'Part  2', 'Part  3', 'Part  4', 'Part  5', 'Part  6', 'Part  7', 'Part  8', 'Part  9', 'Part 10', 'Part 11', 'Part 12', 'Part 13'], 0)
                    ]

        record_list_msg = DataLinksRecordList()
        for record in stub_data:
            datalinks_record = {'bibcode': record[0],
                                'data_links_rows': [{'link_type': record[1], 'link_sub_type': record[2],
                                                     'url': record[3], 'title': record[4],
                                                     'item_count': record[5]}]}
            record_list_msg.datalinks_records.add(**datalinks_record)
        status, text = add_records(record_list_msg)
        self.assertEqual(status, True)
        self.assertEqual(text, 'updated db with new data successfully')


    def test_add_stub_data(self):
        """
        Add stub data
        :return:
        """
        stub_data = [
                        ('2013MNRAS.435.1904M', 'ESOURCE',      'EPRINT_HTML', ['http://arxiv.org/abs/1307.6556'], [], 0),
                        ('2013MNRAS.435.1904M', 'ESOURCE',      'EPRINT_PDF',  ['http://arxiv.org/pdf/1307.6556'], [], 0),
                        ('2013MNRAS.435.1904M', 'ESOURCE',      'PUB_HTML',    ['http://dx.doi.org/10.1093%2Fmnras%2Fstt1379'], [], 0),
                        ('2013MNRAS.435.1904M', 'ESOURCE',      'PUB_PDF',     ['http://mnras.oxfordjournals.org/content/435/3/1904.full.pdf'], [], 0),
                        ('2013MNRAS.435.1904M', 'DATA',         'CXO',         ['http://cda.harvard.edu/chaser?obsid=494'], ['Chandra Data Archive ObsIds 494'], 27),
                        ('2013MNRAS.435.1904M', 'DATA',         'ESA',         ['http://archives.esac.esa.int/ehst/#bibcode=2013MNRAS.435.1904M'], ['European HST References (EHST)'], 1),
                        ('2013MNRAS.435.1904M', 'DATA',         'HEASARC',     ['http://heasarc.gsfc.nasa.gov/cgi-bin/W3Browse/biblink.pl?code=2013MNRAS.435.1904M'], [], 1),
                        ('2013MNRAS.435.1904M', 'DATA',         'Herschel',    ['http://herschel.esac.esa.int/hpt/publicationdetailsview.do?bibcode=2013MNRAS.435.1904M'], [], 1),
                        ('2013MNRAS.435.1904M', 'DATA',         'MAST',        ['http://archive.stsci.edu/mastbibref.php?bibcode=2013MNRAS.435.1904M'], ['MAST References (GALEX EUVE HST)'], 3),
                        ('2013MNRAS.435.1904M', 'DATA',         'NED',         ['http://$NED$/cgi-bin/nph-objsearch?search_type=Search&refcode=2013MNRAS.435.1904M'], ['NED Objects (1)'], 1),
                        ('2013MNRAS.435.1904M', 'DATA',         'SIMBAD',      ['http://$SIMBAD$/simbo.pl?bibcode=2013MNRAS.435.1904M'], ['SIMBAD Objects (30)'], 30),
                        ('2013MNRAS.435.1904M', 'DATA',         'XMM',         ['http://nxsa.esac.esa.int/nxsa-web/#obsid=0097820101'], ['XMM-Newton Observation Number 0097820101'], 1),
                        ('2017MNRAS.467.3556B', 'PRESENTATION', '',            ['http://www.astro.lu.se/~alexey/animations.html'], [], 0),
                        ('1943RvMP...15....1C', 'INSPIRE',      '',            ['http://inspirehep.net/search?p=find+j+RMPHA,15,1'], [], 0),
                        ('1971ATsir.615....4D', 'ASSOCIATED',   '',            ['1971ATsir.615....4D', '1974Afz....10..315D', '1971ATsir.621....7D', '1976Afz....12..665D', '1971ATsir.624....1D', '1983Afz....19..229D', '1983Ap.....19..134D', '1973ATsir.759....6D', '1984Afz....20..525D', '1984Ap.....20..290D', '1974ATsir.809....1D', '1974ATsir.809....2D', '1974ATsir.837....2D'], ['Part  1', 'Part  2', 'Part  3', 'Part  4', 'Part  5', 'Part  6', 'Part  7', 'Part  8', 'Part  9', 'Part 10', 'Part 11', 'Part 12', 'Part 13'], 0)
                    ]

        record_list_msg = DataLinksRecordList()
        for record in stub_data:
            datalinks_record = {'bibcode': record[0],
                                'data_links_rows': [{'link_type': record[1], 'link_sub_type': record[2],
                                                     'url': record[3], 'title': record[4],
                                                     'item_count': record[5]}]}
            record_list_msg.datalinks_records.add(**datalinks_record)
        status, text = add_records(record_list_msg)
        self.assertEqual(status, True)
        self.assertEqual(text, 'updated db with new data successfully')


    # def test_process_request_link_type_all(self):
    #     """
    #     return links for all types of a bibcode
    #     :return:
    #     """
    #     response = LinkRequest(bibcode='2013MNRAS.435.1904M').process_request()
    #     self.assertEqual(response._status_code, 200)
    #     self.assertEqual(response.response[0], '{"action": "display", "links": {"count": 16, '
    #                                            '"records": ['
    #                                            '{"url": "", "count": 1, "bibcode": "2013MNRAS.435.1904M", "type": "metrics", "title": "METRICS (1)"}, '
    #                                            '{"url": "", "count": 1, "bibcode": "2013MNRAS.435.1904M", "type": "citations", "title": "CITATIONS (1)"}, '
    #                                            '{"url": "", "count": 1, "bibcode": "2013MNRAS.435.1904M", "type": "references", "title": "REFERENCES (1)"}, '
    #                                            '{"url": "", "count": 1, "bibcode": "2013MNRAS.435.1904M", "type": "graphics", "title": "GRAPHICS (1)"}, '
    #                                            '{"url": "", "count": 1, "bibcode": "2013MNRAS.435.1904M", "type": "toc", "title": "TOC (1)"}, '
    #                                            '{"url": "", "count": 1, "bibcode": "2013MNRAS.435.1904M", "type": "abstract", "title": "ABSTRACT (1)"}, '
    #                                            '{"url": "", "count": 1, "bibcode": "2013MNRAS.435.1904M", "type": "openurl", "title": "OPENURL (1)"}, '
    #                                            '{"url": "", "count": 1, "bibcode": "2013MNRAS.435.1904M", "type": "coreads", "title": "COREADS (1)"}, '
    #                                            '{"url": "", "count": 4, "bibcode": "2013MNRAS.435.1904M", "type": "esource", "title": "ESOURCE (4)"}, '
    #                                            '{"url": "", "count": 65, "bibcode": "2013MNRAS.435.1904M", "type": "data", "title": "DATA (65)"}, '
    #                                            '{"url": "", "count": 1, "bibcode": "2013MNRAS.435.1904M", "type": "arxiv", "title": "ARXIV (1)"}, '
    #                                            '{"url": "", "count": 1, "bibcode": "2013MNRAS.435.1904M", "type": "doi", "title": "DOI (1)"}], '
    #                                            '"link_type": "all"}, "service": ""}')
    #
    #
    # def test_process_request_link_inspire(self):
    #     """
    #     return a record of link type == inspire
    #     :return:
    #     """
    #     response = LinkRequest(bibcode='1943RvMP...15....1C', link_type='INSPIRE').process_request()
    #     self.assertEqual(response._status_code, 200)
    #     self.assertEqual(response.response[0], '{"action": "redirect", "link": "http://inspirehep.net/search?p=find+j+RMPHA,15,1", "service": "https://ui.adsabs.harvard.edu/#abs/1943RvMP...15....1C/INSPIRE"}')
    #
    #
    # def test_process_request_link_associated(self):
    #     """
    #     check status code for calling process_request for link associated
    #     :return:
    #     """
    #     response = LinkRequest(bibcode='1971ATsir.615....4D', link_type='ASSOCIATED').process_request()
    #     self.assertEqual(response._status_code, 200)
    #
    #
    # def test_process_request_link_esource(self):
    #     """
    #     check status code for calling process_request for a esource sub type link
    #     :return:
    #     """
    #     response = LinkRequest(bibcode='2013MNRAS.435.1904M', link_type='EPRINT_HTML').process_request()
    #     self.assertEqual(response._status_code, 200)
    #
    #
    # def test_process_request_link_data(self):
    #     """
    #     check status code for calling process_request for a data sub type link
    #     :return:
    #     """
    #     response = LinkRequest(bibcode='2013MNRAS.435.1904M', link_type='ESA').process_request()
    #     self.assertEqual(response._status_code, 200)
    #
    #
    # def test_link_all(self):
    #     """
    #     call get_records to fetch all the records for a bibcode
    #     :return:
    #     """
    #     results = get_records(bibcode='2013MNRAS.435.1904M')
    #     self.assertEqual(len(results), 12)
    #
    #
    # def test_link_presentation(self):
    #     """
    #     fetch record of a link_type presentation
    #     :return:
    #     """
    #     results = get_records(bibcode='2017MNRAS.467.3556B', link_type='PRESENTATION')
    #     response = LinkRequest(bibcode='2017MNRAS.467.3556B', link_type='PRESENTATION').request_link_type_single_url(results)
    #     self.assertEqual(response._status_code, 200)
    #     self.assertEqual(response.response[0], '{"action": "redirect", "link": "http://www.astro.lu.se/~alexey/animations.html", "service": "https://ui.adsabs.harvard.edu/#abs/2017MNRAS.467.3556B/PRESENTATION"}')
    #
    #
    # def test_link_all_error_bibcode(self):
    #     """
    #     call get_records to fetch all the records for a none existing bibcode
    #     :return:
    #     """
    #     results = get_records(bibcode='errorbibcode')
    #     self.assertEqual(results, None)
    #
    #
    # def test_error_with_sub_type(self):
    #     """
    #     call get_records to fetch the records for a none existing bibcode, link_type, and link_subtype
    #     :return:
    #     """
    #     results = get_records(bibcode='errorbibcode', link_type='errorlinktype', link_sub_type='errorlinksubtype')
    #     self.assertEqual(results, None)
    #
    # def test_link_associated(self):
    #     """
    #     returning list of url, title pairs
    #     :return:
    #     """
    #     results = get_records(bibcode='1971ATsir.615....4D', link_type='ASSOCIATED')
    #     response = LinkRequest(bibcode='1971ATsir.615....4D', link_type='ASSOCIATED',
    #                 gateway_redirect_url = self.app.config['RESOLVER_GATEWAY_URL_TEST']).request_link_type_associated(results)
    #     self.assertEqual(response._status_code, 200)
    #     self.assertEqual(json.loads(response.response[0]),
    #                      {u'action': u'display',
    #                       u'service': u'https://ui.adsabs.harvard.edu/#abs/1971ATsir.615....4D/associated',
    #                       u'links': {u'count': 13,
    #                                  u'records': [{
    #                                                     u'url': u'/1971ATsir.615....4D/associated/https:,,ui.adsabs.harvard.edu,#abs,1971ATsir.615....4D,abstract',
    #                                                     u'bibcode': u'1971ATsir.615....4D',
    #                                                     u'title': u'Part  1'
    #                                               }, {
    #                                                     u'url': u'/1974Afz....10..315D/associated/https:,,ui.adsabs.harvard.edu,#abs,1974Afz....10..315D,abstract',
    #                                                     u'bibcode': u'1974Afz....10..315D',
    #                                                     u'title': u'Part  2'
    #                                               }, {
    #                                                     u'url': u'/1971ATsir.621....7D/associated/https:,,ui.adsabs.harvard.edu,#abs,1971ATsir.621....7D,abstract',
    #                                                     u'bibcode': u'1971ATsir.621....7D',
    #                                                     u'title': u'Part  3'
    #                                               }, {
    #                                                     u'url': u'/1976Afz....12..665D/associated/https:,,ui.adsabs.harvard.edu,#abs,1976Afz....12..665D,abstract',
    #                                                     u'bibcode': u'1976Afz....12..665D',
    #                                                     u'title': u'Part  4'
    #                                               }, {
    #                                                     u'url': u'/1971ATsir.624....1D/associated/https:,,ui.adsabs.harvard.edu,#abs,1971ATsir.624....1D,abstract',
    #                                                     u'bibcode': u'1971ATsir.624....1D',
    #                                                     u'title': u'Part  5'
    #                                               }, {
    #                                                     u'url': u'/1983Afz....19..229D/associated/https:,,ui.adsabs.harvard.edu,#abs,1983Afz....19..229D,abstract',
    #                                                     u'bibcode': u'1983Afz....19..229D',
    #                                                     u'title': u'Part  6'
    #                                               }, {
    #                                                     u'url': u'/1983Ap.....19..134D/associated/https:,,ui.adsabs.harvard.edu,#abs,1983Ap.....19..134D,abstract',
    #                                                     u'bibcode': u'1983Ap.....19..134D',
    #                                                     u'title': u'Part  7'
    #                                               }, {
    #                                                     u'url': u'/1973ATsir.759....6D/associated/https:,,ui.adsabs.harvard.edu,#abs,1973ATsir.759....6D,abstract',
    #                                                     u'bibcode': u'1973ATsir.759....6D',
    #                                                     u'title': u'Part  8'
    #                                               }, {
    #                                                     u'url': u'/1984Afz....20..525D/associated/https:,,ui.adsabs.harvard.edu,#abs,1984Afz....20..525D,abstract',
    #                                                     u'bibcode': u'1984Afz....20..525D',
    #                                                     u'title': u'Part  9'
    #                                               }, {
    #                                                     u'url': u'/1984Ap.....20..290D/associated/https:,,ui.adsabs.harvard.edu,#abs,1984Ap.....20..290D,abstract',
    #                                                     u'bibcode': u'1984Ap.....20..290D',
    #                                                     u'title': u'Part 10'
    #                                               }, {
    #                                                     u'url': u'/1974ATsir.809....1D/associated/https:,,ui.adsabs.harvard.edu,#abs,1974ATsir.809....1D,abstract',
    #                                                     u'bibcode': u'1974ATsir.809....1D',
    #                                                     u'title': u'Part 11'
    #                                               }, {
    #                                                     u'url': u'/1974ATsir.809....2D/associated/https:,,ui.adsabs.harvard.edu,#abs,1974ATsir.809....2D,abstract',
    #                                                     u'bibcode': u'1974ATsir.809....2D',
    #                                                     u'title': u'Part 12'
    #                                               }, {
    #                                                     u'url': u'/1974ATsir.837....2D/associated/https:,,ui.adsabs.harvard.edu,#abs,1974ATsir.837....2D,abstract',
    #                                                     u'bibcode': u'1974ATsir.837....2D',
    #                                                     u'title': u'Part 13'
    #                                               }],
    #                                  u'link_type': u'ASSOCIATED'}}
    #                      )
    #
    #
    # def test_link_associated_error_bibcode(self):
    #     """
    #     return 404 for not finding any records
    #     :return:
    #     """
    #     results = get_records(bibcode='errorbibcode', link_type='ASSOCIATED')
    #     response = LinkRequest(bibcode='').request_link_type_associated(results)
    #     self.assertEqual(response._status_code, 404)
    #
    #
    # def test_link_esource(self):
    #     """
    #     returning list of urls
    #     :return:
    #     """
    #     results = get_records(bibcode='2013MNRAS.435.1904M', link_type='ESOURCE')
    #     response = LinkRequest(bibcode='2013MNRAS.435.1904', link_type='ESOURCE').request_link_type_esource(results)
    #     self.assertEqual(response._status_code, 200)
    #     self.assertEqual(json.loads(response.response[0]),
    #                      {"action": "display",
    #                       "links": {"count": 4, "link_type": "ESOURCE", "bibcode": "2013MNRAS.435.1904", "records": [
    #                          {"url": "http://arxiv.org/abs/1307.6556", "title": "http://arxiv.org/abs/1307.6556"},
    #                          {"url": "http://arxiv.org/pdf/1307.6556", "title": "http://arxiv.org/pdf/1307.6556"},
    #                          {"url": "http://dx.doi.org/10.1093%2Fmnras%2Fstt1379", "title": "http://dx.doi.org/10.1093%2Fmnras%2Fstt1379"},
    #                          {"url": "http://mnras.oxfordjournals.org/content/435/3/1904.full.pdf", "title": "http://mnras.oxfordjournals.org/content/435/3/1904.full.pdf"}]},
    #                       "service": ""})
    #
    #
    # def test_link_esource_error_bibcode(self):
    #     """
    #     return 404 for not finding any records
    #     :return:
    #     """
    #     results = get_records(bibcode='errorbibcode', link_type='ESOURCE')
    #     response = LinkRequest(bibcode='').request_link_type_esource(results)
    #     self.assertEqual(response._status_code, 404)
    #
    #
    # def test_link_esource_sub_type(self):
    #     """
    #     returning a url of link type ESOURCE
    #     :return:
    #     """
    #     results = get_records(bibcode='2013MNRAS.435.1904M', link_type='ESOURCE', link_sub_type='PUB_PDF')
    #     response = LinkRequest(bibcode='2013MNRAS.435.1904', link_type='PUB_PDF').request_link_type_esource(results)
    #     self.assertEqual(response._status_code, 200)
    #     self.assertEqual(response.response[0], '{"action": "redirect", "link": "http://mnras.oxfordjournals.org/content/435/3/1904.full.pdf", "service": "https://ui.adsabs.harvard.edu/#abs/2013MNRAS.435.1904/ESOURCE"}')
    #
    #
    # def test_link_esource_parts(self):
    #     """
    #     test DataLinks class
    #     :return:
    #     """
    #     results = get_records(bibcode='2013MNRAS.435.1904M', link_type='ESOURCE', link_sub_type='PUB_PDF')
    #     self.assertEqual(len(results), 1)
    #     results = results[0]
    #     self.assertEqual(len(results), 6)
    #     self.assertEqual(results['bibcode'], '2013MNRAS.435.1904M')
    #     self.assertEqual(results['url'][0], 'http://mnras.oxfordjournals.org/content/435/3/1904.full.pdf')
    #     self.assertEqual(results['title'][0], '')
    #
    #
    # def test_link_data(self):
    #     """
    #     returning list of url, title pairs
    #     :return:
    #     """
    #     results = get_records(bibcode='2013MNRAS.435.1904M', link_type='DATA')
    #     response = LinkRequest(bibcode='2013MNRAS.435.1904', link_type='DATA',
    #                 gateway_redirect_url = self.app.config['RESOLVER_GATEWAY_URL_TEST']).request_link_type_data(results)
    #     self.assertEqual(response._status_code, 200)
    #     self.assertEqual(json.loads(response.response[0]),
    #          {
    #              "action": "display",
    #              "service": "",
    #              "links": {
    #                  "count": 8,
    #                  "records": [
    #                      {
    #                          "url": "http://cxc.harvard.edu/cda",
    #                          "data": [
    #                              {
    #                                  "url": "/2013MNRAS.435.1904/data/http%3A%2F%2Fcda.harvard.edu%2Fchaser%3Fobsid%3D494",
    #                                  "title": "Chandra Data Archive ObsIds 494"
    #                              }
    #                          ],
    #                          "title": "Chandra X-Ray Observatory"
    #                      },
    #                      {
    #                          "url": "http://archives.esac.esa.int",
    #                          "data": [
    #                              {
    #                                  "url": "/2013MNRAS.435.1904/data/http%3A%2F%2Farchives.esac.esa.int%2Fehst%2F%23bibcode%3D2013MNRAS.435.1904M",
    #                                  "title": "European HST References (EHST)"
    #                              }
    #                          ],
    #                          "title": "ESAC Science Data Center"
    #                      },
    #                      {
    #                          "url": "https://heasarc.gsfc.nasa.gov/",
    #                          "data": [
    #                              {
    #                                  "url": "/2013MNRAS.435.1904/data/http%3A%2F%2Fheasarc.gsfc.nasa.gov%2Fcgi-bin%2FW3Browse%2Fbiblink.pl%3Fcode%3D2013MNRAS.435.1904M",
    #                                  "title": "http://heasarc.gsfc.nasa.gov/cgi-bin/W3Browse/biblink.pl?code=2013MNRAS.435.1904M"
    #                              }
    #                          ],
    #                          "title": "NASA's High Energy Astrophysics Science Archive Research Center"
    #                      },
    #                      {
    #                          "url": "https://www.cosmos.esa.int/web/herschel/home",
    #                          "data": [
    #                              {
    #                                  "url": "/2013MNRAS.435.1904/data/http%3A%2F%2Fherschel.esac.esa.int%2Fhpt%2Fpublicationdetailsview.do%3Fbibcode%3D2013MNRAS.435.1904M",
    #                                  "title": "http://herschel.esac.esa.int/hpt/publicationdetailsview.do?bibcode=2013MNRAS.435.1904M"
    #                              }
    #                          ],
    #                          "title": "Herschel Science Center"
    #                      },
    #                      {
    #                          "url": "http://archive.stsci.edu",
    #                          "data": [
    #                              {
    #                                  "url": "/2013MNRAS.435.1904/data/http%3A%2F%2Farchive.stsci.edu%2Fmastbibref.php%3Fbibcode%3D2013MNRAS.435.1904M",
    #                                  "title": "MAST References (GALEX EUVE HST)"
    #                              }
    #                          ],
    #                          "title": "Mikulski Archive for Space Telescopes"
    #                      },
    #                      {
    #                          "url": "https://ned.ipac.caltech.edu",
    #                          "data": [
    #                              {
    #                                  "url": "/2013MNRAS.435.1904/data/http%3A%2F%2Fned.ipac.caltech.edu%2Fcgi-bin%2Fnph-objsearch%3Fsearch_type%3DSearch%26refcode%3D2013MNRAS.435.1904M",
    #                                  "title": "NED Objects (1)"
    #                              }
    #                          ],
    #                          "title": "NASA/IPAC Extragalactic Database"
    #                      },
    #                      {
    #                          "url": "http://simbad.u-strasbg.fr",
    #                          "data": [
    #                              {
    #                                  "url": "/2013MNRAS.435.1904/data/http%3A%2F%2Fsimbad.u-strasbg.fr%2Fsimbo.pl%3Fbibcode%3D2013MNRAS.435.1904M",
    #                                  "title": "SIMBAD Objects (30)"
    #                              }
    #                          ],
    #                          "title": "SIMBAD Database at the CDS"
    #                      },
    #                      {
    #                          "url": "http://nxsa.esac.esa.int",
    #                          "data": [
    #                              {
    #                                  "url": "/2013MNRAS.435.1904/data/http%3A%2F%2Fnxsa.esac.esa.int%2Fnxsa-web%2F%23obsid%3D0097820101",
    #                                  "title": "XMM-Newton Observation Number 0097820101"
    #                              }
    #                          ],
    #                          "title": "XMM Newton Science Archive"
    #                      }
    #                  ],
    #                  "bibcode": "2013MNRAS.435.1904"
    #              }
    #          }
    #     )
    #
    #
    # def test_link_data_error_bibcode(self):
    #     """
    #     return 404 for not finding any records
    #     :return:
    #     """
    #     results = get_records(bibcode='errorbibcode', link_type='DATA')
    #     response = LinkRequest(bibcode='').request_link_type_data(results)
    #     self.assertEqual(response._status_code, 404)
    #
    #
    # def test_link_data_sub_type(self):
    #     """
    #     returning a url of link type DATA
    #     :return:
    #     """
    #     results = get_records(bibcode='2013MNRAS.435.1904M', link_type='DATA', link_sub_type='MAST')
    #     response = LinkRequest(bibcode='2013MNRAS.435.1904', link_type='PUB_PDF').request_link_type_data(results)
    #     self.assertEqual(response._status_code, 200)
    #     self.assertEqual(response.response[0], '{"action": "redirect", "link": "http://archive.stsci.edu/mastbibref.php?bibcode=2013MNRAS.435.1904M", "service": "https://ui.adsabs.harvard.edu/#abs/2013MNRAS.435.1904/ESOURCE"}')
    #
    #
    # def test_process_request_upsert(self):
    #     """
    #     return 200 for successful insert/update to db
    #     :return:
    #     """
    #     datalinks_record = [{"bibcode": "1513efua.book.....S",
    #                         "data_links_rows": [{"link_type": "LIBRARYCATALOG", "link_sub_type": "",
    #                                              "url": ["{http://catalog.loc.gov/cgi-bin/Pwebrecon.cgi?v3=1&DB=local&CMD=010a+unk82013020&CNT=10+records+per+page}"],
    #                                              "title": [""],
    #                                              "item_count": 0}]}]
    #     response = PopulateRequest().process_request(datalinks_record)
    #     #self.assertEqual(response._status_code, 200)
    #     self.assertEqual(response.response[0], '{"status": "updated db with new data successfully"}')


if __name__ == '__main__':
    unittest.main()
