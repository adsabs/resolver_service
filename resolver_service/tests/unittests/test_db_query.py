import sys
import os

PROJECT_HOME = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
sys.path.append(PROJECT_HOME)

import unittest
import psycopg2
import testing.postgresql
import json

from linksRequest import LinkRequest
from linksData import *
import app

class test_resolver(unittest.TestCase):
    """tests for generation of resolver"""


    # Reference to testing.postgresql database instance
    db = None

    # Connection to the database used to set the database state before running each
    # test
    db_con = None

    # Map of database connection parameters passed to the functions we're testing
    db_conf = None

    current_app = None

    def setUp(self):
        global current_app
        current_app = app.create_app()

        """ Module level set-up called once before any tests in this file are
        executed.  Creates a temporary database and sets it up """
        global db, db_con, db_conf
        db = testing.postgresql.Postgresql()
        # Get a map of connection parameters for the database which can be passed
        # to the functions being tested so that they connect to the correct
        # database
        db_conf = db.dsn()
        # Create a connection which can be used by our test functions to set and
        # query the state of the database
        db_con = psycopg2.connect(**db_conf)
        # Commit changes immediately to the database
        db_con.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
        with db_con.cursor() as cur:
            # Create the initial database structure (roles, schemas, tables etc.)
            # basically anything that doesn't change
            cur.execute(self.slurp('service/tests/data/datalinks.sql'))

    def tearDown(self):
        """ Called after all of the tests in this file have been executed to close
        the database connecton and destroy the temporary database """
        db_con.close()
        db.stop()


    def slurp(self, path):
        """ Reads and returns the entire contents of a file """
        with open(path, 'r') as f:
            return f.read()

    def executeQuery(self, query):
        with db_con.cursor() as cur:
            cur.execute(query)
            rows = cur.fetchall()
            results = []
            for row in rows:
                if (len(row) == 1):
                    results.append(row[0].lstrip('{').rstrip('}'))
                else:
                    attach = []
                    for i in range(len(row)):
                        convert = []
                        for parts in row[i].lstrip('{').rstrip('}').replace('"', '').split(','):
                            convert.append(parts)
                        attach.append(convert)
                    results += zip(*attach)
            return results

        return ""


    # returning a link
    def test_link_presentation(self):
        self.assertEqual(self.executeQuery(current_app.config['URL_QUERY'].format(db='public', bibcode='2017MNRAS.467.3556B', linkType='PRESENTATION')),
                         ['http://www.astro.lu.se/~alexey/animations.html'])


    # returning list of url, title pairs
    def test_link_associated(self):
        result = self.executeQuery(current_app.config['URL_TITLE_QUERY'].format(db='public', bibcode='1971ATsir.615....4D', linkType='ASSOCIATED'))
        response = LinkRequest(bibcode='1971ATsir.615....4D', linkType='ASSOCIATED').returnResponseLinkTypeAssociated(result, current_app.config['RESOLVER_GATEWAY_URL_TEST'])
        self.assertEqual(response._status_code, 200)
        self.assertEqual(json.loads(response.response[0]),
                         {'action': 'display',
                          'service': 'https://ui.adsabs.harvard.edu/#abs/1971ATsir.615....4D/associated',
                          'links': {'count': 13, 'linkType': 'ASSOCIATED', 'records': [
                                {"url": "/resolver/1971ATsir.615....4D/associated/https%3A%2F%2Fui.adsabs.harvard.edu%2F%23abs%2F1971ATsir.615....4D%2Fabstract", "bibcode": "1971ATsir.615....4D", "title": "Part  1"},
                                {"url": "/resolver/1974Afz....10..315D/associated/https%3A%2F%2Fui.adsabs.harvard.edu%2F%23abs%2F1974Afz....10..315D%2Fabstract", "bibcode": "1974Afz....10..315D", "title": "Part  2"},
                                {"url": "/resolver/1971ATsir.621....7D/associated/https%3A%2F%2Fui.adsabs.harvard.edu%2F%23abs%2F1971ATsir.621....7D%2Fabstract", "bibcode": "1971ATsir.621....7D", "title": "Part  3"},
                                {"url": "/resolver/1976Afz....12..665D/associated/https%3A%2F%2Fui.adsabs.harvard.edu%2F%23abs%2F1976Afz....12..665D%2Fabstract", "bibcode": "1976Afz....12..665D", "title": "Part  4"},
                                {"url": "/resolver/1971ATsir.624....1D/associated/https%3A%2F%2Fui.adsabs.harvard.edu%2F%23abs%2F1971ATsir.624....1D%2Fabstract", "bibcode": "1971ATsir.624....1D", "title": "Part  5"},
                                {"url": "/resolver/1983Afz....19..229D/associated/https%3A%2F%2Fui.adsabs.harvard.edu%2F%23abs%2F1983Afz....19..229D%2Fabstract", "bibcode": "1983Afz....19..229D", "title": "Part  6"},
                                {"url": "/resolver/1983Ap.....19..134D/associated/https%3A%2F%2Fui.adsabs.harvard.edu%2F%23abs%2F1983Ap.....19..134D%2Fabstract", "bibcode": "1983Ap.....19..134D", "title": "Part  7"},
                                {"url": "/resolver/1973ATsir.759....6D/associated/https%3A%2F%2Fui.adsabs.harvard.edu%2F%23abs%2F1973ATsir.759....6D%2Fabstract", "bibcode": "1973ATsir.759....6D", "title": "Part  8"},
                                {"url": "/resolver/1984Afz....20..525D/associated/https%3A%2F%2Fui.adsabs.harvard.edu%2F%23abs%2F1984Afz....20..525D%2Fabstract", "bibcode": "1984Afz....20..525D", "title": "Part  9"},
                                {"url": "/resolver/1984Ap.....20..290D/associated/https%3A%2F%2Fui.adsabs.harvard.edu%2F%23abs%2F1984Ap.....20..290D%2Fabstract", "bibcode": "1984Ap.....20..290D", "title": "Part 10"},
                                {"url": "/resolver/1974ATsir.809....1D/associated/https%3A%2F%2Fui.adsabs.harvard.edu%2F%23abs%2F1974ATsir.809....1D%2Fabstract", "bibcode": "1974ATsir.809....1D", "title": "Part 11"},
                                {"url": "/resolver/1974ATsir.809....2D/associated/https%3A%2F%2Fui.adsabs.harvard.edu%2F%23abs%2F1974ATsir.809....2D%2Fabstract", "bibcode": "1974ATsir.809....2D", "title": "Part 12"},
                                {"url": "/resolver/1974ATsir.837....2D/associated/https%3A%2F%2Fui.adsabs.harvard.edu%2F%23abs%2F1974ATsir.837....2D%2Fabstract", "bibcode": "1974ATsir.837....2D", "title": "Part 13"}
                          ]}})


    # returning list of urls
    def test_link_article(self):
        result = self.executeQuery(current_app.config['URL_QUERY'].format(db='public', bibcode='2013MNRAS.435.1904M', linkType='ARTICLE'))
        response = LinkRequest(bibcode='2013MNRAS.435.1904', linkType='ARTICLE').returnResponseLinkTypeArticle(result)
        self.assertEqual(response._status_code, 200)
        self.assertEqual(json.loads(response.response[0]),
                         {"action": "display",
                          "links": {"count": 4, "linkType": "ARTICLE", "bibcode": "2013MNRAS.435.1904", "records": [
                             {"url": "http://arxiv.org/abs/1307.6556", "title": "http://arxiv.org/abs/1307.6556"},
                             {"url": "http://arxiv.org/pdf/1307.6556", "title": "http://arxiv.org/pdf/1307.6556"},
                             {"url": "http://dx.doi.org/10.1093%2Fmnras%2Fstt1379", "title": "http://dx.doi.org/10.1093%2Fmnras%2Fstt1379"},
                             {"url": "http://mnras.oxfordjournals.org/content/435/3/1904.full.pdf", "title": "http://mnras.oxfordjournals.org/content/435/3/1904.full.pdf"}]},
                          "service": ""})


    #returning a url of link type ARTICLE
    def test_link_article_sub_type(self):
        result = self.executeQuery(current_app.config['URL_WITH_SUB_TYPE_QUERY'].format(db='public', bibcode='2013MNRAS.435.1904M', linkType='ARTICLE', linkSubType='PUB_PDF'))
        response = LinkRequest(bibcode='2013MNRAS.435.1904', linkType='PUB_PDF').returnResponseLinkTypeArticle(result)
        self.assertEqual(response._status_code, 200)
        self.assertEqual(response.response[0], 'http://mnras.oxfordjournals.org/content/435/3/1904.full.pdf')


    # returning list of url, title pairs
    def test_link_data(self):
        result = self.executeQuery(current_app.config['URL_TITLE_QUERY'].format(db='public', bibcode='2013MNRAS.435.1904M', linkType='DATA'))
        response = LinkRequest(bibcode='2013MNRAS.435.1904', linkType='DATA').returnResponseLinkTypeData(result, current_app.config['RESOLVER_GATEWAY_URL_TEST'])
        self.assertEqual(response._status_code, 200)
        self.assertEqual(json.loads(response.response[0]),
                         {"action": "display",
                          "links": {
                              "count": 8, "records": [
                                  {
                                     "url": "http://cda.harvard.edu/",
                                     "data": [{"url": "/resolver/2013MNRAS.435.1904/data/http%3A%2F%2Fcda.harvard.edu%2Fchaser%3Fobsid%3D494", "title": "Chandra Data Archive ObsIds 494"}],
                                     "title": "Resource at http://cda.harvard.edu/"
                                  },
                                  {
                                     "url": "http://$NED$/",
                                     "data": [{"url": "/resolver/2013MNRAS.435.1904/data/http%3A%2F%2F%24NED%24%2Fcgi-bin%2Fnph-objsearch%3Fsearch_type%3DSearch%26refcode%3D2013MNRAS.435.1904M", "title": "NED Objects (1)"}],
                                     "title": "Resource at http://$NED$/"
                                  },
                                  {
                                      "url": "http://$SIMBAD$/",
                                      "data": [{"url": "/resolver/2013MNRAS.435.1904/data/http%3A%2F%2F%24SIMBAD%24%2Fsimbo.pl%3Fbibcode%3D2013MNRAS.435.1904M", "title": "SIMBAD Objects (30)"}],
                                      "title": "Resource at http://$SIMBAD$/"
                                  },
                                  {
                                      "url": "http://archive.stsci.edu/",
                                      "data": [{"url": "/resolver/2013MNRAS.435.1904/data/http%3A%2F%2Farchive.stsci.edu%2Fmastbibref.php%3Fbibcode%3D2013MNRAS.435.1904M", "title": "MAST References (GALEX EUVE HST)"}],
                                      "title": "Resource at http://archive.stsci.edu/"
                                  },
                                  {
                                      "url": "http://archives.esac.esa.int/",
                                      "data": [{"url": "/resolver/2013MNRAS.435.1904/data/http%3A%2F%2Farchives.esac.esa.int%2Fehst%2F%23bibcode%3D2013MNRAS.435.1904M", "title": "European HST References (EHST)"}],
                                      "title": "Resource at http://archives.esac.esa.int/"
                                  },
                                  {
                                      "url": "http://heasarc.gsfc.nasa.gov/",
                                      "data": [{"url": "/resolver/2013MNRAS.435.1904/data/http%3A%2F%2Fheasarc.gsfc.nasa.gov%2Fcgi-bin%2FW3Browse%2Fbiblink.pl%3Fcode%3D2013MNRAS.435.1904M", "title": "http://heasarc.gsfc.nasa.gov/cgi-bin/W3Browse/biblink.pl?code=2013MNRAS.435.1904M"}],
                                      "title": "Resource at http://heasarc.gsfc.nasa.gov/"
                                  },
                                  {
                                      "url": "http://herschel.esac.esa.int/",
                                      "data": [{"url": "/resolver/2013MNRAS.435.1904/data/http%3A%2F%2Fherschel.esac.esa.int%2Fhpt%2Fpublicationdetailsview.do%3Fbibcode%3D2013MNRAS.435.1904M", "title": "http://herschel.esac.esa.int/hpt/publicationdetailsview.do?bibcode=2013MNRAS.435.1904M"}],
                                      "title": "Resource at http://herschel.esac.esa.int/"
                                  },
                                  {
                                      "url": "http://nxsa.esac.esa.int/",
                                      "data": [{"url": "/resolver/2013MNRAS.435.1904/data/http%3A%2F%2Fnxsa.esac.esa.int%2Fnxsa-web%2F%23obsid%3D0097820101", "title": "XMM-Newton Observation Number 0097820101"}],
                                      "title": "Resource at http://nxsa.esac.esa.int/"
                                  }
                              ],
                              "bibcode": "2013MNRAS.435.1904"},
                          "service": ""})


    # returning a url of link type DATA
    def test_link_data_sub_type(self):
        result = self.executeQuery(current_app.config['URL_WITH_SUB_TYPE_QUERY'].format(db='public', bibcode='2013MNRAS.435.1904M', linkType='DATA', linkSubType='MAST'))
        response = LinkRequest(bibcode='2013MNRAS.435.1904', linkType='PUB_PDF').returnResponseLinkTypeData(result, current_app.config['RESOLVER_GATEWAY_URL_TEST'])
        self.assertEqual(response._status_code, 200)
        self.assertEqual(response.response[0], 'http://archive.stsci.edu/mastbibref.php?bibcode=2013MNRAS.435.1904M')


if __name__ == '__main__':
    unittest.main(verbosity=2)