import sys, os
project_home = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
if project_home not in sys.path:
    sys.path.insert(0, project_home)

from flask_testing import TestCase
import unittest
import testing.postgresql
import json

import resolversrv.app as app
from resolversrv.models import DataLinks, Base
from resolversrv.utils import get_records
from resolversrv.views import LinkRequest


class test_database(TestCase):
    """tests for generation of resolver"""

    current_app = None
    postgresql = None

    def create_app(self):
        '''
        Get the url from in-memory db and pass it to app to create test AlchemySQL db.
        :return:
        '''
        self.postgresql = testing.postgresql.Postgresql()
        self.assertIsNotNone(self.postgresql)

        self.current_app = app.create_app(**{'SQLALCHEMY_DATABASE_URI': self.postgresql.url()})
        return self.current_app


    def setUp(self):
        '''
        Module level set-up called once before any tests in this file are executed.
        Creates a temporary database and populates it.
        '''
        Base.metadata.create_all(bind=self.app.db.engine)

        self.addStubData()


    def tearDown(self):
        '''
        Called after all of the tests in this file have been executed to close
        the database connection and destroy the temporary database.
        '''
        self.app.db.session.remove()
        self.app.db.drop_all()


    def addStubData(self):
        '''
        Add stub data
        :return:
        '''
        stub_data = [
                        ('2013MNRAS.435.1904M', 'ESOURCE',      'EPRINT_HTML', {'http://arxiv.org/abs/1307.6556'}, {''}, 0),
                        ('2013MNRAS.435.1904M', 'ESOURCE',      'EPRINT_PDF',  {'http://arxiv.org/pdf/1307.6556'}, {''}, 0),
                        ('2013MNRAS.435.1904M', 'ESOURCE',      'PUB_HTML',    {'http://dx.doi.org/10.1093%2Fmnras%2Fstt1379'}, {''}, 0),
                        ('2013MNRAS.435.1904M', 'ESOURCE',      'PUB_PDF',     {'http://mnras.oxfordjournals.org/content/435/3/1904.full.pdf'}, {''}, 0),
                        ('2013MNRAS.435.1904M', 'DATA',         'CXO',         {'http://cda.harvard.edu/chaser?obsid=494'}, {'Chandra Data Archive ObsIds 494'}, 27),
                        ('2013MNRAS.435.1904M', 'DATA',         'ESA',         {'http://archives.esac.esa.int/ehst/#bibcode=2013MNRAS.435.1904M'}, {'European HST References (EHST)'}, 1),
                        ('2013MNRAS.435.1904M', 'DATA',         'HEASARC',     {'http://heasarc.gsfc.nasa.gov/cgi-bin/W3Browse/biblink.pl?code=2013MNRAS.435.1904M'}, {''}, 1),
                        ('2013MNRAS.435.1904M', 'DATA',         'Herschel',    {'http://herschel.esac.esa.int/hpt/publicationdetailsview.do?bibcode=2013MNRAS.435.1904M'}, {''}, 1),
                        ('2013MNRAS.435.1904M', 'DATA',         'MAST',        {'http://archive.stsci.edu/mastbibref.php?bibcode=2013MNRAS.435.1904M'}, {'MAST References (GALEX EUVE HST)'}, 3),
                        ('2013MNRAS.435.1904M', 'DATA',         'NED',         {'http://$NED$/cgi-bin/nph-objsearch?search_type=Search&refcode=2013MNRAS.435.1904M'}, {'NED Objects (1)'}, 1),
                        ('2013MNRAS.435.1904M', 'DATA',         'SIMBAD',      {'http://$SIMBAD$/simbo.pl?bibcode=2013MNRAS.435.1904M'}, {'SIMBAD Objects (30)'}, 30),
                        ('2013MNRAS.435.1904M', 'DATA',         'XMM',         {'http://nxsa.esac.esa.int/nxsa-web/#obsid=0097820101'}, {'XMM-Newton Observation Number 0097820101'}, 1),
                        ('2017MNRAS.467.3556B', 'PRESENTATION', '',            {'http://www.astro.lu.se/~alexey/animations.html'}, {''}, 0),
                        ('1971ATsir.615....4D', 'ASSOCIATED',   '',            {'1971ATsir.615....4D', '1971ATsir.621....7D', '1971ATsir.624....1D', '1973ATsir.759....6D', '1974Afz....10..315D', '1974ATsir.809....1D', '1974ATsir.809....2D', '1974ATsir.837....2D', '1976Afz....12..665D', '1983Afz....19..229D', '1983Ap.....19..134D', '1984Afz....20..525D', '1984Ap.....20..290D'}, {'Part  1', 'Part  3', 'Part  5', 'Part  8', 'Part  2', 'Part 11', 'Part 12', 'Part 13', 'Part  4', 'Part  6', 'Part  7', 'Part  9', 'Part 10'}, 0)
                    ]

        for record in stub_data:
            data_link = DataLinks(bibcode=record[0],
                                  link_type=record[1],
                                  link_sub_type=record[2],
                                  url=record[3],
                                  title=record[4],
                                  item_count=record[5])
            self.app.db.session.add(data_link)
        self.app.db.session.commit()


    # returning a link
    def test_link_presentation(self):
        results = get_records(bibcode='2017MNRAS.467.3556B', link_type='PRESENTATION')
        response = LinkRequest(bibcode='2017MNRAS.467.3556B', link_type='PRESENTATION').request_link_type_single_url(results)
        self.assertEqual(response._status_code, 200)
        self.assertEqual(response.response[0], '{"action": "redirect", "link": "http://www.astro.lu.se/~alexey/animations.html", "service": "https://ui.adsabs.harvard.edu/#abs/2017MNRAS.467.3556B/PRESENTATION"}')


    # return 404 for not finding any records
    def test_link_presentation_error_bibcode(self):
        response = LinkRequest(bibcode='errorbibcode', link_type='PRESENTATION').request_link_type_single_url('')
        self.assertEqual(response._status_code, 404)
        self.assertEqual(response.response[0], '{"error": "did not find any records"}')


    # return 400 for unrecognizable link type
    def test_link_presentation_error_link_type(self):
        response = LinkRequest(bibcode='2017MNRAS.467.3556B', link_type='errorlinktype').process_request()
        self.assertEqual(response._status_code, 400)


    # returning list of url, title pairs
    def test_link_associated(self):
        results = get_records(bibcode='1971ATsir.615....4D', link_type='ASSOCIATED')
        response = LinkRequest(bibcode='1971ATsir.615....4D', link_type='ASSOCIATED',
                    gateway_redirect_url = self.current_app.config['RESOLVER_GATEWAY_URL_TEST']).request_link_type_associated(results)
        self.assertEqual(response._status_code, 200)
        self.assertEqual(json.loads(response.response[0]),
             {
                 "action": "display",
                 "links":
                 {
                     "count": 13,
                     "records": [
                         {
                              "url": "/1984Ap.....20..290D/associated/https%3A%2F%2Fui.adsabs.harvard.edu%2F%23abs%2F1984Ap.....20..290D%2Fabstract",
                              "bibcode": "1984Ap.....20..290D",
                              "title": "Part  1"
                         }, {
                              "url": "/1984Afz....20..525D/associated/https%3A%2F%2Fui.adsabs.harvard.edu%2F%23abs%2F1984Afz....20..525D%2Fabstract",
                              "bibcode": "1984Afz....20..525D",
                              "title": "Part  2"
                         }, {
                              "url": "/1974Afz....10..315D/associated/https%3A%2F%2Fui.adsabs.harvard.edu%2F%23abs%2F1974Afz....10..315D%2Fabstract",
                              "bibcode": "1974Afz....10..315D",
                              "title": "Part  3"
                         }, {
                              "url": "/1974ATsir.809....1D/associated/https%3A%2F%2Fui.adsabs.harvard.edu%2F%23abs%2F1974ATsir.809....1D%2Fabstract",
                              "bibcode": "1974ATsir.809....1D",
                              "title": "Part  4"
                         }, {
                              "url": "/1971ATsir.621....7D/associated/https%3A%2F%2Fui.adsabs.harvard.edu%2F%23abs%2F1971ATsir.621....7D%2Fabstract",
                              "bibcode": "1971ATsir.621....7D",
                              "title": "Part  5"
                         }, {
                              "url": "/1973ATsir.759....6D/associated/https%3A%2F%2Fui.adsabs.harvard.edu%2F%23abs%2F1973ATsir.759....6D%2Fabstract",
                              "bibcode": "1973ATsir.759....6D",
                              "title": "Part  6"
                         }, {
                              "url": "/1974ATsir.837....2D/associated/https%3A%2F%2Fui.adsabs.harvard.edu%2F%23abs%2F1974ATsir.837....2D%2Fabstract",
                              "bibcode": "1974ATsir.837....2D",
                              "title": "Part  7"
                         }, {
                              "url": "/1983Afz....19..229D/associated/https%3A%2F%2Fui.adsabs.harvard.edu%2F%23abs%2F1983Afz....19..229D%2Fabstract",
                              "bibcode": "1983Afz....19..229D",
                              "title": "Part  8"
                         }, {
                              "url": "/1974ATsir.809....2D/associated/https%3A%2F%2Fui.adsabs.harvard.edu%2F%23abs%2F1974ATsir.809....2D%2Fabstract",
                              "bibcode": "1974ATsir.809....2D",
                              "title": "Part  9"
                         }, {
                              "url": "/1971ATsir.624....1D/associated/https%3A%2F%2Fui.adsabs.harvard.edu%2F%23abs%2F1971ATsir.624....1D%2Fabstract",
                              "bibcode": "1971ATsir.624....1D",
                              "title": "Part 10"
                         }, {
                              "url": "/1971ATsir.615....4D/associated/https%3A%2F%2Fui.adsabs.harvard.edu%2F%23abs%2F1971ATsir.615....4D%2Fabstract",
                              "bibcode": "1971ATsir.615....4D",
                              "title": "Part 11"
                         }, {
                              "url": "/1983Ap.....19..134D/associated/https%3A%2F%2Fui.adsabs.harvard.edu%2F%23abs%2F1983Ap.....19..134D%2Fabstract",
                              "bibcode": "1983Ap.....19..134D",
                              "title": "Part 12"
                         }, {
                              "url": "/1976Afz....12..665D/associated/https%3A%2F%2Fui.adsabs.harvard.edu%2F%23abs%2F1976Afz....12..665D%2Fabstract",
                              "bibcode": "1976Afz....12..665D",
                              "title": "Part 13"
                         }
                     ],
                     "link_type": "ASSOCIATED"
                 },
                "service": "https://ui.adsabs.harvard.edu/#abs/1971ATsir.615....4D/associated"
             }
        )


    # return 404 for not finding any records
    def test_link_associated_error_bibcode(self):
        results = get_records(bibcode='errorbibcode', link_type='ASSOCIATED')
        response = LinkRequest(bibcode='errorbibcode', link_type='ASSOCIATED').request_link_type_associated(results)
        self.assertEqual(response._status_code, 404)


    # returning list of urls
    def test_link_article(self):
        results = get_records(bibcode='2013MNRAS.435.1904M', link_type='ESOURCE')
        response = LinkRequest(bibcode='2013MNRAS.435.1904', link_type='ESOURCE').request_link_type_esource(results)
        self.assertEqual(response._status_code, 200)
        self.assertEqual(json.loads(response.response[0]),
                         {"action": "display",
                          "links": {"count": 4, "link_type": "ESOURCE", "bibcode": "2013MNRAS.435.1904", "records": [
                             {"url": "http://arxiv.org/abs/1307.6556", "title": "http://arxiv.org/abs/1307.6556"},
                             {"url": "http://arxiv.org/pdf/1307.6556", "title": "http://arxiv.org/pdf/1307.6556"},
                             {"url": "http://dx.doi.org/10.1093%2Fmnras%2Fstt1379", "title": "http://dx.doi.org/10.1093%2Fmnras%2Fstt1379"},
                             {"url": "http://mnras.oxfordjournals.org/content/435/3/1904.full.pdf", "title": "http://mnras.oxfordjournals.org/content/435/3/1904.full.pdf"}]},
                          "service": ""})


    # return 404 for not finding any records
    def test_link_article_error_bibcode(self):
        results = get_records(bibcode='errorbibcode', link_type='ESOURCE')
        response = LinkRequest(bibcode='errorbibcode', link_type='ESOURCE').request_link_type_esource(results)
        self.assertEqual(response._status_code, 404)


    # returning a url of link type ESOURCE
    def test_link_article_sub_type(self):
        results = get_records(bibcode='2013MNRAS.435.1904M', link_type='ESOURCE', link_sub_type='PUB_PDF')
        response = LinkRequest(bibcode='2013MNRAS.435.1904', link_type='PUB_PDF').request_link_type_esource(results)
        self.assertEqual(response._status_code, 200)
        self.assertEqual(response.response[0], '{"action": "redirect", "link": "http://mnras.oxfordjournals.org/content/435/3/1904.full.pdf", "service": "https://ui.adsabs.harvard.edu/#abs/2013MNRAS.435.1904/ESOURCE"}')


    # test DataLinks class
    def test_link_article_parts(self):
        results = get_records(bibcode='2013MNRAS.435.1904M', link_type='ESOURCE', link_sub_type='PUB_PDF')
        self.assertEqual(len(results), 1)
        results = results[0]
        self.assertEqual(len(results), 6)
        self.assertEqual(results['bibcode'], '2013MNRAS.435.1904M')
        self.assertEqual(results['url'][0], 'http://mnras.oxfordjournals.org/content/435/3/1904.full.pdf')
        self.assertEqual(results['title'][0], '')


    # returning list of url, title pairs
    def test_link_data(self):
        results = get_records(bibcode='2013MNRAS.435.1904M', link_type='DATA')
        response = LinkRequest(bibcode='2013MNRAS.435.1904', link_type='DATA',
                    gateway_redirect_url = self.current_app.config['RESOLVER_GATEWAY_URL_TEST']).request_link_type_data(results)
        self.assertEqual(response._status_code, 200)
        self.assertEqual(json.loads(response.response[0]),
             {
                 "action": "display",
                 "service": "",
                 "links": {
                     "count": 8,
                     "records": [
                         {
                             "url": "http://cxc.harvard.edu/cda",
                             "data": [
                                 {
                                     "url": "/2013MNRAS.435.1904/data/http%3A%2F%2Fcda.harvard.edu%2Fchaser%3Fobsid%3D494",
                                     "title": "Chandra Data Archive ObsIds 494"
                                 }
                             ],
                             "title": "Chandra X-Ray Observatory"
                         },
                         {
                             "url": "http://archives.esac.esa.int",
                             "data": [
                                 {
                                     "url": "/2013MNRAS.435.1904/data/http%3A%2F%2Farchives.esac.esa.int%2Fehst%2F%23bibcode%3D2013MNRAS.435.1904M",
                                     "title": "European HST References (EHST)"
                                 }
                             ],
                             "title": "ESAC Science Data Center"
                         },
                         {
                             "url": "https://heasarc.gsfc.nasa.gov/",
                             "data": [
                                 {
                                     "url": "/2013MNRAS.435.1904/data/http%3A%2F%2Fheasarc.gsfc.nasa.gov%2Fcgi-bin%2FW3Browse%2Fbiblink.pl%3Fcode%3D2013MNRAS.435.1904M",
                                     "title": "http://heasarc.gsfc.nasa.gov/cgi-bin/W3Browse/biblink.pl?code=2013MNRAS.435.1904M"
                                 }
                             ],
                             "title": "NASA's High Energy Astrophysics Science Archive Research Center"
                         },
                         {
                             "url": "https://www.cosmos.esa.int/web/herschel/home",
                             "data": [
                                 {
                                     "url": "/2013MNRAS.435.1904/data/http%3A%2F%2Fherschel.esac.esa.int%2Fhpt%2Fpublicationdetailsview.do%3Fbibcode%3D2013MNRAS.435.1904M",
                                     "title": "http://herschel.esac.esa.int/hpt/publicationdetailsview.do?bibcode=2013MNRAS.435.1904M"
                                 }
                             ],
                             "title": "Herschel Science Center"
                         },
                         {
                             "url": "http://archive.stsci.edu",
                             "data": [
                                 {
                                     "url": "/2013MNRAS.435.1904/data/http%3A%2F%2Farchive.stsci.edu%2Fmastbibref.php%3Fbibcode%3D2013MNRAS.435.1904M",
                                     "title": "MAST References (GALEX EUVE HST)"
                                 }
                             ],
                             "title": "Mikulski Archive for Space Telescopes"
                         },
                         {
                             "url": "https://ned.ipac.caltech.edu",
                             "data": [
                                 {
                                     "url": "/2013MNRAS.435.1904/data/http%3A%2F%2Fned.ipac.caltech.edu%2Fcgi-bin%2Fnph-objsearch%3Fsearch_type%3DSearch%26refcode%3D2013MNRAS.435.1904M",
                                     "title": "NED Objects (1)"
                                 }
                             ],
                             "title": "NASA/IPAC Extragalactic Database"
                         },
                         {
                             "url": "http://simbad.u-strasbg.fr",
                             "data": [
                                 {
                                     "url": "/2013MNRAS.435.1904/data/http%3A%2F%2Fsimbad.u-strasbg.fr%2Fsimbo.pl%3Fbibcode%3D2013MNRAS.435.1904M",
                                     "title": "SIMBAD Objects (30)"
                                 }
                             ],
                             "title": "SIMBAD Database at the CDS"
                         },
                         {
                             "url": "http://nxsa.esac.esa.int",
                             "data": [
                                 {
                                     "url": "/2013MNRAS.435.1904/data/http%3A%2F%2Fnxsa.esac.esa.int%2Fnxsa-web%2F%23obsid%3D0097820101",
                                     "title": "XMM-Newton Observation Number 0097820101"
                                 }
                             ],
                             "title": "XMM Newton Science Archive"
                         }
                     ],
                     "bibcode": "2013MNRAS.435.1904"
                 }
             }
        )


    # return 404 for not finding any records
    def test_link_data_error_bibcode(self):
        results = get_records(bibcode='errorbibcode', link_type='DATA')
        response = LinkRequest(bibcode='errorbibcode', link_type='DATA').request_link_type_data(results)
        self.assertEqual(response._status_code, 404)


    # returning a url of link type DATA
    def test_link_data_sub_type(self):
        results = get_records(bibcode='2013MNRAS.435.1904M', link_type='DATA', link_sub_type='MAST')
        response = LinkRequest(bibcode='2013MNRAS.435.1904', link_type='PUB_PDF').request_link_type_data(results)
        self.assertEqual(response._status_code, 200)
        self.assertEqual(response.response[0], '{"action": "redirect", "link": "http://archive.stsci.edu/mastbibref.php?bibcode=2013MNRAS.435.1904M", "service": "https://ui.adsabs.harvard.edu/#abs/2013MNRAS.435.1904/ESOURCE"}')


if __name__ == '__main__':
    unittest.main()