import sys, os
project_home = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../'))
if project_home not in sys.path:
    sys.path.insert(0, project_home)

import unittest
import json

from resolversrv import app
from resolversrv.tests.unittests.base import TestCaseDatabase
from resolversrv.utils import get_records, add_records
from resolversrv.views import LinkRequest, PopulateRequest

class test_database(TestCaseDatabase):

    def create_app(self):
        '''Start the wsgi application'''
        a = app.create_app(**{
            'SQLALCHEMY_DATABASE_URI': self.postgresql_url,
            'RESOLVER_GATEWAY_URL': '/{bibcode}/{link_type}/{url}',
           })
        return a

    def add_stub_data(self):
        """
        Add stub data
        :return:
        """
        stub_data = [
                        ('2013MNRAS.435.1904M', 'TOC',          '',            [''], [''], 0),
                        ('2013MNRAS.435.1904M', 'ESOURCE',      'EPRINT_HTML', ['http://arxiv.org/abs/1307.6556'], [''], 0),
                        ('2013MNRAS.435.1904M', 'ESOURCE',      'EPRINT_PDF',  ['http://arxiv.org/pdf/1307.6556'], [''], 0),
                        ('2013MNRAS.435.1904M', 'ESOURCE',      'PUB_HTML',    ['https://doi.org/10.1093%2Fmnras%2Fstt1379'], [''], 0),
                        ('2013MNRAS.435.1904M', 'ESOURCE',      'PUB_PDF',     ['http://mnras.oxfordjournals.org/content/435/3/1904.full.pdf'], [''], 0),
                        ('2013MNRAS.435.1904M', 'DATA',         'Chandra',     ['http://cda.harvard.edu/chaser?obsid=494'], ['Chandra Data Archive ObsIds 494'], 27),
                        ('2013MNRAS.435.1904M', 'DATA',         'ESA',         ['http://archives.esac.esa.int/ehst/#bibcode=2013MNRAS.435.1904M'], ['European HST References (EHST)'], 1),
                        ('2013MNRAS.435.1904M', 'DATA',         'HEASARC',     ['http://heasarc.gsfc.nasa.gov/cgi-bin/W3Browse/biblink.pl?code=2013MNRAS.435.1904M'], [], 1),
                        ('2013MNRAS.435.1904M', 'DATA',         'Herschel',    ['http://herschel.esac.esa.int/hpt/publicationdetailsview.do?bibcode=2013MNRAS.435.1904M'], [], 1),
                        ('2013MNRAS.435.1904M', 'DATA',         'MAST',        ['http://archive.stsci.edu/mastbibref.php?bibcode=2013MNRAS.435.1904M'], ['MAST References (GALEX EUVE HST)'], 3),
                        ('2013MNRAS.435.1904M', 'DATA',         'NED',         ['http://$NED$/cgi-bin/nph-objsearch?search_type=Search&refcode=2013MNRAS.435.1904M'], ['NED Objects (1)'], 1),
                        ('2013MNRAS.435.1904M', 'DATA',         'SIMBAD',      ['http://$SIMBAD$/simbo.pl?bibcode=2013MNRAS.435.1904M'], ['SIMBAD Objects (30)'], 30),
                        ('2013MNRAS.435.1904M', 'DATA',         'XMM',         ['http://nxsa.esac.esa.int/nxsa-web/#obsid=0097820101'], ['XMM-Newton Observation Number 0097820101'], 1),
                        ('2017MNRAS.467.3556B', 'PRESENTATION', '',            ['http://www.astro.lu.se/~alexey/animations.html'], [''], 0),
                        ('1943RvMP...15....1C', 'INSPIRE',      '',            ['http://inspirehep.net/search?p=find+j+RMPHA,15,1'], [''], 0),
                        ('1971ATsir.615....4D', 'ASSOCIATED',   '',            ['1971ATsir.615....4D', '1974Afz....10..315D', '1971ATsir.621....7D', '1976Afz....12..665D', '1971ATsir.624....1D', '1983Afz....19..229D', '1983Ap.....19..134D', '1973ATsir.759....6D', '1984Afz....20..525D', '1984Ap.....20..290D', '1974ATsir.809....1D', '1974ATsir.809....2D', '1974ATsir.837....2D'], ['Part  1', 'Part  2', 'Part  3', 'Part  4', 'Part  5', 'Part  6', 'Part  7', 'Part  8', 'Part  9', 'Part 10', 'Part 11', 'Part 12', 'Part 13'], 0),
                        ('2007ASPC..368...27R', 'ESOURCE',      'ADS_PDF',     ['http://articles.adsabs.harvard.edu/pdf/2007ASPC..368...27R'], [''], 0),
                        ('2007ASPC..368...27R', 'ESOURCE',      'ADS_SCAN',    ['http://articles.adsabs.harvard.edu/full/2007ASPC..368...27R'], [''], 0),
                        ('2007ASPC..368...27R', 'ESOURCE',      'EPRINT_HTML', ['https://arxiv.org/abs/astro-ph/0703637'], [''], 0),
                        ('2007ASPC..368...27R', 'ESOURCE',      'EPRINT_PDF',  ['https://arxiv.org/pdf/astro-ph/0703637'], [''], 0),
                        ('2007ASPC..368...27R', 'ESOURCE',      'PUB_HTML',    ['http://aspbooks.org/custom/publications/paper/368-0027.html'], [''], 0),
                        ('2007ASPC..368...27R', 'TOC',          '',            [''], [''], 0)
        ]

        datalinks_list = []
        for record in stub_data:
            datalinks_record = {'bibcode': record[0],
                                'data_links_rows': [{'link_type': record[1], 'link_sub_type': record[2],
                                                     'url': record[3], 'title': record[4],
                                                     'item_count': record[5]}]}
            datalinks_list.append(datalinks_record)

        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        response = self.client.put('/update', data=json.dumps(datalinks_list), headers=headers)
        self.assertEqual(response._status_code, 200)
        self.assertEqual(response.json['status'], 'updated db with new data successfully')


    def test_link_type_all(self):
        """
        return links for all types of a bibcode
        :return:
        """
        self.add_stub_data()
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        response = self.client.get('/2013MNRAS.435.1904M', headers=headers)
        self.assertEqual(response._status_code, 200)
        self.assertDictEqual(response.json, {u'action': u'display', u'links': {u'count': 17, u'records': [
                                                {u'url': u'/2013MNRAS.435.1904M/METRICS', u'count': 1, u'bibcode': u'2013MNRAS.435.1904M', u'type': u'metrics', u'title': u'METRICS (1)'},
                                                {u'url': u'/2013MNRAS.435.1904M/CITATIONS', u'count': 1, u'bibcode': u'2013MNRAS.435.1904M', u'type': u'citations', u'title': u'CITATIONS (1)'},
                                                {u'url': u'/2013MNRAS.435.1904M/REFERENCES', u'count': 1, u'bibcode': u'2013MNRAS.435.1904M', u'type': u'references', u'title': u'REFERENCES (1)'},
                                                {u'url': u'/2013MNRAS.435.1904M/SIMILAR', u'count': 1, u'bibcode': u'2013MNRAS.435.1904M', u'type': u'similar', u'title': u'SIMILAR (1)'},
                                                {u'url': u'/2013MNRAS.435.1904M/GRAPHICS', u'count': 1, u'bibcode': u'2013MNRAS.435.1904M', u'type': u'graphics', u'title': u'GRAPHICS (1)'},
                                                {u'url': u'/2013MNRAS.435.1904M/TOC', u'count': 1, u'bibcode': u'2013MNRAS.435.1904M', u'type': u'toc', u'title': u'TOC (1)'},
                                                {u'url': u'/2013MNRAS.435.1904M/ABSTRACT', u'count': 1, u'bibcode': u'2013MNRAS.435.1904M', u'type': u'abstract', u'title': u'ABSTRACT (1)'},
                                                {u'url': u'/2013MNRAS.435.1904M/OPENURL', u'count': 1, u'bibcode': u'2013MNRAS.435.1904M', u'type': u'openurl', u'title': u'OPENURL (1)'},
                                                {u'url': u'/2013MNRAS.435.1904M/COREADS', u'count': 1, u'bibcode': u'2013MNRAS.435.1904M', u'type': u'coreads', u'title': u'COREADS (1)'},
                                                {u'url': u'/2013MNRAS.435.1904M/ESOURCE', u'count': 4, u'bibcode': u'2013MNRAS.435.1904M', u'type': u'esource', u'title': u'ESOURCE (4)'},
                                                {u'url': u'/2013MNRAS.435.1904M/DATA', u'count': 65, u'bibcode': u'2013MNRAS.435.1904M', u'type': u'data', u'title': u'DATA (65)'},
                                                {u'url': u'/2013MNRAS.435.1904M/ARXIV', u'count': 1, u'bibcode': u'2013MNRAS.435.1904M', u'type': u'arxiv', u'title': u'ARXIV (1)'},
                                                {u'url': u'/2013MNRAS.435.1904M/DOI', u'count': 1, u'bibcode': u'2013MNRAS.435.1904M', u'type': u'doi', u'title': u'DOI (1)'}],
                                             u'link_type': 'all'}, u'service': u''})


    def test_link_inspire(self):
        """
        return a record of link type == inspire
        :return:
        """
        self.add_stub_data()
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        response = self.client.get('/1943RvMP...15....1C/INSPIRE', headers=headers)
        self.assertEqual(response._status_code, 200)
        self.assertDictEqual(response.json, {u'action': u'redirect',
                                             u'link': u'http://inspirehep.net/search?p=find+j+RMPHA,15,1',
                                             u'link_type': u'INSPIRE',
                                             u'service': u'http://inspirehep.net/search?p=find+j+RMPHA,15,1'})


    def test_link_presentation(self):
        """
        fetch record of a link_type presentation
        :return:
        """
        self.add_stub_data()
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        response = self.client.get('/2017MNRAS.467.3556B/PRESENTATION', headers=headers)
        self.assertEqual(response._status_code, 200)
        self.assertDictEqual(response.json, {u'action': u'redirect',
                                             u'link': u'http://www.astro.lu.se/~alexey/animations.html',
                                             u'link_type': u'PRESENTATION',
                                             u'service': u'http://www.astro.lu.se/~alexey/animations.html'})


    def test_link_associated(self):
        """
        returning list of url, title pairs
        :return:
        """
        self.add_stub_data()
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        response = self.client.get('/1971ATsir.615....4D/ASSOCIATED', headers=headers)
        self.assertEqual(response._status_code, 200)
        self.assertDictEqual(response.json, {u'action': u'display',
                                             u'links': {u'count': 13,
                                                        u'records': [{u'url': u'/1971ATsir.615....4D/associated/:%2Fabs%2F1971ATsir.615....4D%2Fabstract', u'bibcode': u'1971ATsir.615....4D', u'title': u'Part  1'},
                                                                     {u'url': u'/1974Afz....10..315D/associated/:%2Fabs%2F1974Afz....10..315D%2Fabstract', u'bibcode': u'1974Afz....10..315D', u'title': u'Part  2'},
                                                                     {u'url': u'/1971ATsir.621....7D/associated/:%2Fabs%2F1971ATsir.621....7D%2Fabstract', u'bibcode': u'1971ATsir.621....7D', u'title': u'Part  3'},
                                                                     {u'url': u'/1976Afz....12..665D/associated/:%2Fabs%2F1976Afz....12..665D%2Fabstract', u'bibcode': u'1976Afz....12..665D', u'title': u'Part  4'},
                                                                     {u'url': u'/1971ATsir.624....1D/associated/:%2Fabs%2F1971ATsir.624....1D%2Fabstract', u'bibcode': u'1971ATsir.624....1D', u'title': u'Part  5'},
                                                                     {u'url': u'/1983Afz....19..229D/associated/:%2Fabs%2F1983Afz....19..229D%2Fabstract', u'bibcode': u'1983Afz....19..229D', u'title': u'Part  6'},
                                                                     {u'url': u'/1983Ap.....19..134D/associated/:%2Fabs%2F1983Ap.....19..134D%2Fabstract', u'bibcode': u'1983Ap.....19..134D', u'title': u'Part  7'},
                                                                     {u'url': u'/1973ATsir.759....6D/associated/:%2Fabs%2F1973ATsir.759....6D%2Fabstract', u'bibcode': u'1973ATsir.759....6D', u'title': u'Part  8'},
                                                                     {u'url': u'/1984Afz....20..525D/associated/:%2Fabs%2F1984Afz....20..525D%2Fabstract', u'bibcode': u'1984Afz....20..525D', u'title': u'Part  9'},
                                                                     {u'url': u'/1984Ap.....20..290D/associated/:%2Fabs%2F1984Ap.....20..290D%2Fabstract', u'bibcode': u'1984Ap.....20..290D', u'title': u'Part 10'},
                                                                     {u'url': u'/1974ATsir.809....1D/associated/:%2Fabs%2F1974ATsir.809....1D%2Fabstract', u'bibcode': u'1974ATsir.809....1D', u'title': u'Part 11'},
                                                                     {u'url': u'/1974ATsir.809....2D/associated/:%2Fabs%2F1974ATsir.809....2D%2Fabstract', u'bibcode': u'1974ATsir.809....2D', u'title': u'Part 12'},
                                                                     {u'url': u'/1974ATsir.837....2D/associated/:%2Fabs%2F1974ATsir.837....2D%2Fabstract', u'bibcode': u'1974ATsir.837....2D', u'title': u'Part 13'}],
                                                        u'link_type': u'ASSOCIATED'},
                                             u'service': u'/abs/1971ATsir.615....4D/associated'})


    def test_link_esource_subtype(self):
        """
        check status code for calling process_request for a esource sub type link
        :return:
        """
        self.add_stub_data()
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        response = self.client.get('/2013MNRAS.435.1904M/EPRINT_HTML', headers=headers)
        self.assertEqual(response._status_code, 200)
        self.assertDictEqual(response.json, {u'action': u'redirect',
                                             u'link': u'http://arxiv.org/abs/1307.6556',
                                             u'link_type': u'ESOURCE|EPRINT_HTML',
                                             u'service': u'http://arxiv.org/abs/1307.6556'
                                             })


    def test_link_esource(self):
        """
        returning list of urls
        :return:
        """
        self.add_stub_data()
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        response = self.client.get('/2013MNRAS.435.1904M/ESOURCE', headers=headers)
        self.assertEqual(response._status_code, 200)
        self.assertDictEqual(response.json, {u'action': u'display',
                                             u'links': {u'count': 4,
                                                        u'link_type': u'ESOURCE',
                                                        u'bibcode': u'2013MNRAS.435.1904M',
                                                        u'records': [
                                                            {u'url': u'http://arxiv.org/abs/1307.6556', u'title': u'http://arxiv.org/abs/1307.6556', u'link_type': u'ESOURCE|EPRINT_HTML'},
                                                            {u'url': u'http://arxiv.org/pdf/1307.6556', u'title': u'http://arxiv.org/pdf/1307.6556', u'link_type': u'ESOURCE|EPRINT_PDF'},
                                                            {u'url': u'https://doi.org/10.1093%2Fmnras%2Fstt1379', u'title': u'https://doi.org/10.1093%2Fmnras%2Fstt1379', u'link_type': u'ESOURCE|PUB_HTML'},
                                                            {u'url': u'http://mnras.oxfordjournals.org/content/435/3/1904.full.pdf', u'title': u'http://mnras.oxfordjournals.org/content/435/3/1904.full.pdf', u'link_type': u'ESOURCE|PUB_PDF'}
                                                        ]
                                             },
                                             u'service': u''})


    def test_link_data_subtype(self):
        """
        check status code for calling process_request for a data sub type link
        :return:
        """
        self.add_stub_data()
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        response = self.client.get('/2013MNRAS.435.1904M/ESA', headers=headers)
        self.assertEqual(response._status_code, 200)
        self.assertDictEqual(response.json, {u'action': u'redirect',
                                             u'link': u'http://archives.esac.esa.int/ehst/#bibcode=2013MNRAS.435.1904M',
                                             u'link_type': u'DATA|ESA',
                                             u'service': u'http://archives.esac.esa.int/ehst/#bibcode=2013MNRAS.435.1904M'})

    def test_link_data(self):
        """
        returning list of url, title pairs
        :return:
        """
        self.add_stub_data()
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        response = self.client.get('/2013MNRAS.435.1904M/DATA', headers=headers)
        self.assertEqual(response._status_code, 200)
        self.assertDictEqual(response.json,{u'action': u'display',
                                            u'service': u'',
                                            u'links': {u'count': 8,
                                            u'records': [{u'url': u'http://cxc.harvard.edu/cda',  # Chandra
                                                          u'data': [{u'url': u'/2013MNRAS.435.1904M/DATA|Chandra/http%3A%2F%2Fcda.harvard.edu%2Fchaser%3Fobsid%3D494',
                                                                     u'title': u'Chandra Data Archive ObsIds 494',
                                                                     u'link_type': u'DATA|Chandra'}],
                                                          u'title': u'Chandra X-Ray Observatory'},
                                                         {u'url': u'http://archives.esac.esa.int', # ESA
                                                          u'data': [{u'url': u'/2013MNRAS.435.1904M/DATA|ESA/http%3A%2F%2Farchives.esac.esa.int%2Fehst%2F%23bibcode%3D2013MNRAS.435.1904M',
                                                                     u'title': u'European HST References (EHST)',
                                                                     u'link_type': u'DATA|ESA'}],
                                                          u'title': u'ESAC Science Data Center'
                                                         },
                                                         {u'url': u'https://heasarc.gsfc.nasa.gov/', # HEASARC
                                                          u'data': [{u'url': u'/2013MNRAS.435.1904M/DATA|HEASARC/http%3A%2F%2Fheasarc.gsfc.nasa.gov%2Fcgi-bin%2FW3Browse%2Fbiblink.pl%3Fcode%3D2013MNRAS.435.1904M',
                                                                     u'title': u'http://heasarc.gsfc.nasa.gov/cgi-bin/W3Browse/biblink.pl?code=2013MNRAS.435.1904M',
                                                                     u'link_type': u'DATA|HEASARC'}],
                                                          u'title': u"NASA's High Energy Astrophysics Science Archive Research Center"
                                                         },
                                                         {u'url': u'https://www.cosmos.esa.int/web/herschel/home', #Herschel
                                                          u'data': [{u'url': u'/2013MNRAS.435.1904M/DATA|Herschel/http%3A%2F%2Fherschel.esac.esa.int%2Fhpt%2Fpublicationdetailsview.do%3Fbibcode%3D2013MNRAS.435.1904M',
                                                                     u'title': u'http://herschel.esac.esa.int/hpt/publicationdetailsview.do?bibcode=2013MNRAS.435.1904M',
                                                                     u'link_type': u'DATA|Herschel'}],
                                                          u'title': u'Herschel Science Center'
                                                         },
                                                         {u'url': u'http://archive.stsci.edu', # MAST
                                                          u'data': [{u'url': u'/2013MNRAS.435.1904M/DATA|MAST/http%3A%2F%2Farchive.stsci.edu%2Fmastbibref.php%3Fbibcode%3D2013MNRAS.435.1904M',
                                                                     u'title': u'MAST References (GALEX EUVE HST)',
                                                                     u'link_type': u'DATA|MAST'}],
                                                          u'title': u'Mikulski Archive for Space Telescopes'
                                                         },
                                                         {u'url': u'https://ned.ipac.caltech.edu', # NED
                                                          u'data': [{u'url': u'/2013MNRAS.435.1904M/DATA|NED/http%3A%2F%2Fned.ipac.caltech.edu%2Fcgi-bin%2Fnph-objsearch%3Fsearch_type%3DSearch%26refcode%3D2013MNRAS.435.1904M',
                                                                     u'title': u'NED Objects (1)',
                                                                     u'link_type': u'DATA|NED'}],
                                                          u'title': u'NASA/IPAC Extragalactic Database'
                                                         },
                                                         {u'url': u'http://simbad.u-strasbg.fr', # SIMBAD
                                                          u'data': [{u'url': u'/2013MNRAS.435.1904M/DATA|SIMBAD/http%3A%2F%2Fsimbad.u-strasbg.fr%2Fsimbo.pl%3Fbibcode%3D2013MNRAS.435.1904M',
                                                                     u'title': u'SIMBAD Objects (30)',
                                                                     u'link_type': u'DATA|SIMBAD'}],
                                                          u'title': u'SIMBAD Database at the CDS'
                                                         },
                                                         {u'url': u'http://nxsa.esac.esa.int', # XMM
                                                          u'data': [{u'url': u'/2013MNRAS.435.1904M/DATA|XMM/http%3A%2F%2Fnxsa.esac.esa.int%2Fnxsa-web%2F%23obsid%3D0097820101',
                                                                     u'title': u'XMM-Newton Observation Number 0097820101',
                                                                     u'link_type': u'DATA|XMM'}],
                                                          u'title': u'XMM Newton Science Archive'
                                                         }],
                                            u'bibcode': u'2013MNRAS.435.1904M'}})


    def test_link_all_error_bibcode(self):
        """
        call get_records to fetch all the records for a none existing bibcode
        :return:
        """
        results = get_records(bibcode='errorbibcode')
        self.assertEqual(results, None)


    def test_error_with_sub_type(self):
        """
        call get_records to fetch the records for a none existing bibcode, link_type, and link_subtype
        :return:
        """
        results = get_records(bibcode='errorbibcode', link_type='errorlinktype', link_sub_type='errorlinksubtype')
        self.assertEqual(results, None)

    def test_link_associated_error_bibcode(self):
        """
        return 404 for not finding any records
        :return:
        """
        results = get_records(bibcode='errorbibcode', link_type='ASSOCIATED')
        response = LinkRequest(bibcode='').request_link_type_associated(results)
        self.assertEqual(response._status_code, 404)


    def test_link_esource_error_bibcode(self):
        """
        return 404 for not finding any records
        :return:
        """
        results = get_records(bibcode='errorbibcode', link_type='ESOURCE')
        response = LinkRequest(bibcode='').request_link_type_esource(results)
        self.assertEqual(response._status_code, 404)


    def test_link_data_error_bibcode(self):
        """
        return 404 for not finding any records
        :return:
        """
        results = get_records(bibcode='errorbibcode', link_type='DATA')
        response = LinkRequest(bibcode='').request_link_type_data(results)
        self.assertEqual(response._status_code, 404)


    def test_process_request_upsert(self):
        """
        return 200 for successful insert/update to db
        :return:
        """
        self.add_stub_data()
        datalinks_list = [{"bibcode": "1513efua.book.....S",
                           "data_links_rows": [{"link_type": "LIBRARYCATALOG", "link_sub_type": "",
                                                "url": ["http://catalog.loc.gov/cgi-bin/Pwebrecon.cgi?v3=1&DB=local&CMD=010a+unk82013020&CNT=10+records+per+page"],
                                                "title": [""],
                                                "item_count": 0}]}]
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        # insert it here
        response = self.client.put('/update', data=json.dumps(datalinks_list), headers=headers)
        self.assertEqual(response._status_code, 200)
        self.assertEqual(response.json['status'], 'updated db with new data successfully')
        # select it here
        response = self.client.get('/1513efua.book.....S/LIBRARYCATALOG', headers=headers)
        self.assertEqual(response._status_code, 200)
        self.assertDictEqual(response.json, {u'action': u'redirect',
                                             u'link': u'http://catalog.loc.gov/cgi-bin/Pwebrecon.cgi?v3=1&DB=local&CMD=010a+unk82013020&CNT=10+records+per+page',
                                             u'link_type': u'LIBRARYCATALOG',
                                             u'service': u'http://catalog.loc.gov/cgi-bin/Pwebrecon.cgi?v3=1&DB=local&CMD=010a+unk82013020&CNT=10+records+per+page'})

    def test_process_request_delete(self):
        """
        return 200 for successful deletion from db
        :return:
        """
        self.add_stub_data()
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        # delete it here
        bibcodes = {'bibcode': ['2013MNRAS.435.1904M']}
        response = self.client.delete('/delete', data=json.dumps(bibcodes), headers=headers)
        self.assertEqual(response._status_code, 200)
        self.assertEqual(response.json['status'], 'removed 13 records of 1 bibcodes')
        # select it here
        response = self.client.get('/2013MNRAS.435.1904M/ESOURCE', headers=headers)
        self.assertEqual(response._status_code, 404)
        self.assertEqual(response.json['error'], 'did not find any records')

    def test_link_toc(self):
        """
        TOC was one of the on the fly types, as of 3/27/2019 we should have bibcodes with TOC in db
        so this link should not be created if the entry does not exists in db
        :return:
        """
        self.add_stub_data()
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}

        # verify that TOC record does not exsits in db and hence return error
        response = self.client.get('/2019AIPC.2081c0032P/TOC', headers=headers)
        self.assertEqual(response._status_code, 404)
        # insert it here
        datalinks_list = [{"bibcode": "2019AIPC.2081c0032P",
                           "data_links_rows": [{"link_type": "TOC", "link_sub_type": "", "url": [""], "title": [""], "item_count": 0}]}]
        response = self.client.put('/update', data=json.dumps(datalinks_list), headers=headers)
        self.assertEqual(response._status_code, 200)
        self.assertEqual(response.json['status'], 'updated db with new data successfully')
        # select it here
        response = self.client.get('/2019AIPC.2081c0032P/TOC', headers=headers)
        self.assertEqual(response._status_code, 200)
        self.assertDictEqual(response.json, {u'action': u'redirect',
                                             u'link': u'/abs/2019AIPC.2081c0032P/toc',
                                             u'service': u'/abs/2019AIPC.2081c0032P/toc',
                                             u'link_type': u'TOC'})
        # delete it here
        bibcodes = {'bibcode': ['2019AIPC.2081c0032P']}
        response = self.client.delete('/delete', data=json.dumps(bibcodes), headers=headers)
        self.assertEqual(response._status_code, 200)
        # verify that is gone
        response = self.client.get('/2019AIPC.2081c0032P/TOC', headers=headers)
        self.assertEqual(response._status_code, 404)


    def test_link_esource_subtype_article(self):
        """
        check status code for calling process_request for a esource sub type link for legacy type article
        :return:
        """
        self.add_stub_data()
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        response = self.client.get('/2007ASPC..368...27R/ARTICLE', headers=headers)
        self.assertEqual(response._status_code, 200)
        self.assertDictEqual(response.json, {u'action': u'redirect',
                                             u'link': u'http://articles.adsabs.harvard.edu/pdf/2007ASPC..368...27R',
                                             u'service': u'http://articles.adsabs.harvard.edu/pdf/2007ASPC..368...27R',
                                             u'link_type': u'ESOURCE|ADS_PDF'})
        response = self.client.get('/2013MNRAS.435.1904M/ARTICLE', headers=headers)
        self.assertEqual(response._status_code, 200)
        self.assertDictEqual(response.json, {u'action': u'redirect',
                                             u'link': u'http://mnras.oxfordjournals.org/content/435/3/1904.full.pdf',
                                             u'service': u'http://mnras.oxfordjournals.org/content/435/3/1904.full.pdf',
                                             u'link_type': u'ESOURCE|PUB_PDF'})


if __name__ == '__main__':
    unittest.main()
