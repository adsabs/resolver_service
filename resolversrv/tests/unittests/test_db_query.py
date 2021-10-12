import sys, os
project_home = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../'))
if project_home not in sys.path:
    sys.path.insert(0, project_home)

import unittest
import json

from resolversrv import app
from resolversrv.tests.unittests.base import TestCaseDatabase
from resolversrv.utils import get_records, add_records, get_records_new, add_records_new, del_records_new, get_ids
from resolversrv.views import LinkRequest, PopulateRequest

from adsmsg import DocumentRecords

class TestDatabase(TestCaseDatabase):

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
                        ('1514temg.book.....V', 'ASSOCIATED',   '',            ['1514temg.book.....V', 'https://www.si.edu/object/siris_sil_154413'], ['Main Paper', 'Supplementary Material'], 0),
                        ('2007ASPC..368...27R', 'ESOURCE',      'ADS_PDF',     ['http://articles.adsabs.harvard.edu/pdf/2007ASPC..368...27R'], [''], 0),
                        ('2007ASPC..368...27R', 'ESOURCE',      'ADS_SCAN',    ['http://articles.adsabs.harvard.edu/full/2007ASPC..368...27R'], [''], 0),
                        ('2007ASPC..368...27R', 'ESOURCE',      'EPRINT_HTML', ['https://arxiv.org/abs/astro-ph/0703637'], [''], 0),
                        ('2007ASPC..368...27R', 'ESOURCE',      'EPRINT_PDF',  ['https://arxiv.org/pdf/astro-ph/0703637'], [''], 0),
                        ('2007ASPC..368...27R', 'ESOURCE',      'PUB_HTML',    ['http://aspbooks.org/custom/publications/paper/368-0027.html'], [''], 0),
                        ('2007ASPC..368...27R', 'TOC',          '',            [''], [''], 0),
                        ('2004astro.ph..1427R', 'DATA',         'MAST',        ['http://archive.stsci.edu/prepds/gems','https://archive.stsci.edu/mastbibref.php?bibcode=2004ApJS..152..163R'],['GEMS: Galaxy Evolution from Morphologies and SEDs (Hans-Walter Rix)','MAST References (HST)'], 2),
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
                                                {u'url': u'/2013MNRAS.435.1904M/ABSTRACT', u'count': 1, u'bibcode': u'2013MNRAS.435.1904M', u'type': u'abstract', u'title': u'ABSTRACT (1)'},
                                                {u'url': u'/2013MNRAS.435.1904M/CITATIONS', u'count': 1, u'bibcode': u'2013MNRAS.435.1904M', u'type': u'citations', u'title': u'CITATIONS (1)'},
                                                {u'url': u'/2013MNRAS.435.1904M/REFERENCES', u'count': 1, u'bibcode': u'2013MNRAS.435.1904M', u'type': u'references', u'title': u'REFERENCES (1)'},
                                                {u'url': u'/2013MNRAS.435.1904M/COREADS', u'count': 1, u'bibcode': u'2013MNRAS.435.1904M', u'type': u'coreads', u'title': u'COREADS (1)'},
                                                {u'url': u'/2013MNRAS.435.1904M/TOC', u'count': 1, u'bibcode': u'2013MNRAS.435.1904M', u'type': u'toc', u'title': u'TOC (1)'},
                                                {u'url': u'/2013MNRAS.435.1904M/OPENURL', u'count': 1, u'bibcode': u'2013MNRAS.435.1904M', u'type': u'openurl', u'title': u'OPENURL (1)'},
                                                {u'url': u'/2013MNRAS.435.1904M/GRAPHICS', u'count': 1, u'bibcode': u'2013MNRAS.435.1904M', u'type': u'graphics', u'title': u'GRAPHICS (1)'},
                                                {u'url': u'/2013MNRAS.435.1904M/METRICS', u'count': 1, u'bibcode': u'2013MNRAS.435.1904M', u'type': u'metrics', u'title': u'METRICS (1)'},
                                                {u'url': u'/2013MNRAS.435.1904M/SIMILAR', u'count': 1, u'bibcode': u'2013MNRAS.435.1904M', u'type': u'similar', u'title': u'SIMILAR (1)'},
                                                {u'url': u'/2013MNRAS.435.1904M/ESOURCE', u'count': 4, u'bibcode': u'2013MNRAS.435.1904M', u'type': u'esource', u'title': u'ESOURCE (4)'},
                                                {u'url': u'/2013MNRAS.435.1904M/DATA', u'count': 65, u'bibcode': u'2013MNRAS.435.1904M', u'type': u'data', u'title': u'DATA (65)'},
                                                {u'url': u'/2013MNRAS.435.1904M/DOI', u'count': 1, u'bibcode': u'2013MNRAS.435.1904M', u'type': u'doi', u'title': u'DOI (1)'},
                                                {u'url': u'/2013MNRAS.435.1904M/ARXIV', u'count': 1, u'bibcode': u'2013MNRAS.435.1904M', u'type': u'arxiv', u'title': u'ARXIV (1)'}],
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
                                                                     {u'url': u'/1971ATsir.615....4D/associated/:%2Fabs%2F1974Afz....10..315D%2Fabstract', u'bibcode': u'1974Afz....10..315D', u'title': u'Part  2'},
                                                                     {u'url': u'/1971ATsir.615....4D/associated/:%2Fabs%2F1971ATsir.621....7D%2Fabstract', u'bibcode': u'1971ATsir.621....7D', u'title': u'Part  3'},
                                                                     {u'url': u'/1971ATsir.615....4D/associated/:%2Fabs%2F1976Afz....12..665D%2Fabstract', u'bibcode': u'1976Afz....12..665D', u'title': u'Part  4'},
                                                                     {u'url': u'/1971ATsir.615....4D/associated/:%2Fabs%2F1971ATsir.624....1D%2Fabstract', u'bibcode': u'1971ATsir.624....1D', u'title': u'Part  5'},
                                                                     {u'url': u'/1971ATsir.615....4D/associated/:%2Fabs%2F1983Afz....19..229D%2Fabstract', u'bibcode': u'1983Afz....19..229D', u'title': u'Part  6'},
                                                                     {u'url': u'/1971ATsir.615....4D/associated/:%2Fabs%2F1983Ap.....19..134D%2Fabstract', u'bibcode': u'1983Ap.....19..134D', u'title': u'Part  7'},
                                                                     {u'url': u'/1971ATsir.615....4D/associated/:%2Fabs%2F1973ATsir.759....6D%2Fabstract', u'bibcode': u'1973ATsir.759....6D', u'title': u'Part  8'},
                                                                     {u'url': u'/1971ATsir.615....4D/associated/:%2Fabs%2F1984Afz....20..525D%2Fabstract', u'bibcode': u'1984Afz....20..525D', u'title': u'Part  9'},
                                                                     {u'url': u'/1971ATsir.615....4D/associated/:%2Fabs%2F1984Ap.....20..290D%2Fabstract', u'bibcode': u'1984Ap.....20..290D', u'title': u'Part 10'},
                                                                     {u'url': u'/1971ATsir.615....4D/associated/:%2Fabs%2F1974ATsir.809....1D%2Fabstract', u'bibcode': u'1974ATsir.809....1D', u'title': u'Part 11'},
                                                                     {u'url': u'/1971ATsir.615....4D/associated/:%2Fabs%2F1974ATsir.809....2D%2Fabstract', u'bibcode': u'1974ATsir.809....2D', u'title': u'Part 12'},
                                                                     {u'url': u'/1971ATsir.615....4D/associated/:%2Fabs%2F1974ATsir.837....2D%2Fabstract', u'bibcode': u'1974ATsir.837....2D', u'title': u'Part 13'}],
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


    def test_data_subtype_multiple_links(self):
        """

        :return:
        """
        self.add_stub_data()
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        response = self.client.get('/2004astro.ph..1427R/MAST', headers=headers)
        self.assertEqual(response._status_code, 200)
        self.assertDictEqual(response.json, {u'action': u'display',
                                             u'links': {u'bibcode': u'2004astro.ph..1427R',
                                             u'count': 1,
                                             u'records': [{u'data': [{u'link_type': u'DATA|MAST',
                                                                      u'title': u'GEMS: Galaxy Evolution from Morphologies and SEDs (Hans-Walter Rix)',
                                                                      u'url': u'/2004astro.ph..1427R/DATA|MAST/http%3A%2F%2Farchive.stsci.edu%2Fprepds%2Fgems'}],
                                                           u'title': u'Mikulski Archive for Space Telescopes',
                                                           u'url': u'http://archive.stsci.edu'},
                                                          {u'data': [{u'link_type': u'DATA|MAST',
                                                                      u'title': u'MAST References (HST)',
                                                                      u'url': u'/2004astro.ph..1427R/DATA|MAST/https%3A%2F%2Farchive.stsci.edu%2Fmastbibref.php%3Fbibcode%3D2004ApJS..152..163R'}],
                                                           u'title': u'Mikulski Archive for Space Telescopes',
                                                           u'url': u'http://archive.stsci.edu'}]},
                                             u'service': u''})


    def test_verify_url(self):
        """

        :return:
        """
        self.add_stub_data()
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        response = self.client.get('/1514temg.book.....V/verify_url:https%3A%2F%2Fwww.si.edu%2Fobject%2Fsiris_sil_154413', headers=headers)
        self.assertEqual(response.json, {'link': 'verified'})
        response = self.client.get('/1514temg.book.....V/verify_url:http%3A%2F%2Fwww.google.com', headers=headers)
        self.assertEqual(response.json, {'link': 'not found'})


class TestDatabaseNew(TestCaseDatabase):

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
            {
                "bibcode": "2013MNRAS.435.1904M",
                "identifier": ["2013MNRAS.435.1904M", "2013arXiv1307.6556M", "2013MNRAS.tmp.2206M", "10.1093/mnras/stt1379", "arXiv:1307.6556"],
                "links": {
                    "DOI": ["10.1093/mnras/stt1379"],
                    "ARXIV": ["arXiv:1307.6556"],
                    "DATA": {
                        "Chandra": {
                            "url": ["https://cda.harvard.edu/chaser?obsid=494,493,5290,5289,5286,5288,5287,3666,6162,6159,6163,6160,6161,13413,12028,10900,10898,13416,13414,12029,12027,13417,10899,13412,10901,13415,12026"],
                            "title": ["Chandra Data Archive ObsIds 494, 493, 5290, 5289, 5286, 5288, 5287, 3666, 6162, 6159, 6163, 6160, 6161, 13413, 12028, 10900, 10898, 13416, 13414, 12029, 12027, 13417, 10899, 13412, 10901, 13415, 12026"],
                            "count": 1
                        },
                        "ESA": {
                            "url": ["http://archives.esac.esa.int/ehst/#bibcode=2013MNRAS.435.1904M"],
                            "title": ["European HST References (EHST)"],
                            "count": 1
                        },
                        "HEASARC": {
                            "url": ["http://heasarc.gsfc.nasa.gov/cgi-bin/W3Browse/biblink.pl?code=2013MNRAS.435.1904M"],
                            "title": ["http://heasarc.gsfc.nasa.gov/cgi-bin/W3Browse/biblink.pl?code=2013MNRAS.435.1904M"],
                            "count": 1
                        },
                        "Herschel": {
                            "url": ["http://archives.esac.esa.int/hsa/whsa/?ACTION=PUBLICATION&ID=2013MNRAS.435.1904M"],
                            "title": ["http://archives.esac.esa.int/hsa/whsa/?ACTION=PUBLICATION&ID=2013MNRAS.435.1904M"],
                            "count": 1
                        },
                        "MAST": {
                            "url": ["https://archive.stsci.edu/mastbibref.php?bibcode=2013MNRAS.435.1904M"],
                            "title": ["MAST References (HST, EUVE, GALEX)"],
                            "count": 3
                        },
                        "NED": {
                            "url": ["https://$NED$/uri/NED::InRefcode/2013MNRAS.435.1904M"],
                            "title": ["NED Objects (1)"],
                            "count": 1
                        },
                        "SIMBAD": {
                            "url": ["http://$SIMBAD$/simbo.pl?bibcode=2013MNRAS.435.1904M"],
                            "title": ["SIMBAD Objects (30)"],
                            "count": 30
                        },
                        "XMM": {
                            "url": ["https://nxsa.esac.esa.int/nxsa-web/#bibcode=2013MNRAS.435.1904M"],
                            "title": ["XMM data (1 observations)"],
                            "count": 1
                        }
                    },
                    "ESOURCE": {
                        "EPRINT_HTML": {
                            "url": ["https://arxiv.org/abs/1307.6556"],
                            "title": ['']
                        },
                        "EPRINT_PDF": {
                            "url": ["https://arxiv.org/pdf/1307.6556"],
                            "title": ['']
                        },
                        "PUB_HTML": {
                            "url": ["https://doi.org/10.1093%2Fmnras%2Fstt1379"],
                            "title": ['']
                        },
                        "PUB_PDF": {
                            "url": ["https://academic.oup.com/mnras/pdf-lookup/doi/10.1093/mnras/stt1379"],
                            "title": ['']
                        }
                    },
                    "CITATIONS": True,
                    "REFERENCES": True
                }
            },
            {
                "bibcode": "2017MNRAS.467.3556B",
                "identifier": ["2017MNRAS.467.3556B", "2017arXiv170202377B", "10.1093/mnras/stx312", "arXiv:1702.02377"],
                "links": {
                    "DOI": ["10.1093/mnras/stx312"],
                    "ARXIV": ["arXiv:1702.02377"],
                    "DATA": {
                        "SIMBAD": {
                            "url": ["http://$SIMBAD$/simbo.pl?bibcode=2017MNRAS.467.3556B"],
                            "title": ["SIMBAD Objects (5)"],
                            "count": 5
                        }
                    },
                    "ESOURCE": {
                        "EPRINT_HTML": {
                            "url": ["https://arxiv.org/abs/1702.02377"],
                            "title": ['']
                        },
                        "EPRINT_PDF": {
                            "url": ["https://arxiv.org/pdf/1702.02377"],
                            "title": ['']
                        },
                        "PUB_HTML": {
                            "url": ["https://doi.org/10.1093%2Fmnras%2Fstx312"],
                            "title": ['']},
                        "PUB_PDF": {
                            "url": ["https://academic.oup.com/mnras/pdf-lookup/doi/10.1093/mnras/stx312"],
                            "title": ['']
                        }
                    },
                    "ASSOCIATED": {
                        "url": ["http://www.astro.lu.se/~alexey/animations.html"],
                        "title": ["Supporting Media"]
                    },
                    "PRESENTATION": {
                        "url": ["http://www.astro.lu.se/~alexey/animations.html"],
                        "title": ['']
                    },
                    "CITATIONS": True,
                    "REFERENCES": True
                }
            },
            {
                "bibcode": "1943RvMP...15....1C",
                "identifier": ["1943RvMP...15....1C", "10.1103/RevModPhys.15.1"],
                "links": {
                    "DOI": ["10.1103/RevModPhys.15.1"],
                    "ESOURCE": {
                        "PUB_HTML": {
                            "url": ["http://link.aps.org/doi/10.1103/RevModPhys.15.1"],
                            "title": ['']
                        }
                    },
                    "INSPIRE": {
                        "url": ["http://inspirehep.net/search?p=find+j+RMPHA,15,1"],
                        "title": ['']
                    },
                    "CITATIONS": True,
                    "REFERENCES": True
                }
            },
            {
                "bibcode": "1971ATsir.615....4D",
                "identifier": ["1971ATsir.615....4D"],
                "links": {
                    "ASSOCIATED": {
                        "url": ["1971ATsir.615....4D", "1971ATsir.621....7D", "1971ATsir.624....1D", "1973ATsir.759....6D", "1974Afz....10..315D", "1974ATsir.809....1D", "1974ATsir.809....2D", "1974ATsir.837....2D", "1976Afz....12..665D", "1983Afz....19..229D", "1983Ap.....19..134D", "1984Afz....20..525D", "1984Ap.....20..290D"],
                        "title": ["Part  1","Part  3","Part  5","Part  8","Part  2","Part 11","Part 12","Part 13","Part  4","Part  6","Part  7","Part  9","Part 10"],
                        "count": 10
                    },
                    "CITATIONS": True,
                    "REFERENCES": False
                }
            },
            {
                "bibcode": "1514temg.book.....V",
                "identifier": ["1514temg.book.....V", "10.3931/e-rara-426"],
                "links": {
                    "DOI": ["10.3931/e-rara-426"],
                    "ESOURCE": {
                        "PUB_HTML": {
                            "url": ["https://doi.org/10.3931%2Fe-rara-426"],
                            "title": ['']
                        }
                    },
                    "ASSOCIATED": {
                        "url": ["1514temg.book.....V", "https://www.si.edu/object/siris_sil_154413"],
                        "title": ["Main Paper", "Supplementary Material"],
                        "count": 2
                    },
                    "CITATIONS": False,
                    "REFERENCES": False
                }
            },
            {
                "bibcode": "2007ASPC..368...27R",
                "identifier": ["2007ASPC..368...27R", "2007astro.ph..3637R", "arXiv:astro-ph/0703637"],
                "links": {
                    "ARXIV": ["arXiv:astro-ph/0703637"],
                    "TOC": True,
                    "ESOURCE": {
                        "ADS_PDF": {
                            "url": ["http://articles.adsabs.harvard.edu/pdf/2007ASPC..368...27R"],
                            "title": ['']
                        },
                        "ADS_SCAN": {
                            "url": ["http://articles.adsabs.harvard.edu/full/2007ASPC..368...27R"],
                            "title": ['']},
                        "EPRINT_HTML": {
                            "url": ["http://arxiv.org/abs/astro-ph/0703637"],
                            "title": ['']
                        },
                        "EPRINT_PDF": {
                            "url": ["http://arxiv.org/pdf/astro-ph/0703637"],
                            "title": ['']
                        },
                        "PUB_HTML": {
                            "url": ["http://aspbooks.org/custom/publications/paper/368-0027.html"],
                            "title": ['']
                        }
                    },
                    "REFERENCES": True
                }
            },
            {
                "bibcode": "2004ApJS..152..163R",
                "identifier": ["2004ApJS..152..163R", "2004astro.ph..1427R", "10.1086/420885", "arXiv:astro-ph/0401427"],
                "links": {
                    "DOI": ["10.1086/420885"],
                    "ARXIV": ["arXiv:astro-ph/0401427"],
                    "DATA": {
                        "ESA": {
                            "url": ["http://archives.esac.esa.int/ehst/#bibcode=2004ApJS..152..163R"],
                            "title": ["European HST References (EHST)"],
                            "count": 1
                        },
                        "MAST": {
                            "url": ["http://archive.stsci.edu/mastbibref.php?bibcode=2004ApJS..152..163R", "http://archive.stsci.edu/prepds/gems"],
                            "title": ["MAST References (HST)", "GEMS: Galaxy Evolution from Morphologies and SEDs (Hans-Walter Rix)"],
                            "count": 2
                        },
                        "SIMBAD": {
                            "url": ["http://$SIMBAD$/simbo.pl?bibcode=2004ApJS..152..163R"],
                            "title": ["SIMBAD Objects (3)"],
                            "count": 3
                        }
                    },
                    "ESOURCE": {
                        "EPRINT_HTML": {
                            "url": ["http://arxiv.org/abs/astro-ph/0401427"],
                            "title": ['']
                        },
                        "EPRINT_PDF": {
                            "url": ["http://arxiv.org/pdf/astro-ph/0401427"],
                            "title": ['']
                        },
                        "PUB_HTML": {
                            "url": ["https://doi.org/10.1086%2F420885"],
                            "title": ['']
                        },
                        "PUB_PDF": {
                            "url": ["http://stacks.iop.org/0067-0049/152/163/pdf"],
                             "title": ['']
                        }
                    },
                    "CITATIONS": True,
                    "REFERENCES": True
                }
            },
            {
                 "bibcode": "2021JOSS....6.2807C",
                 "identifier": ["2021JOSS....6.2807C", "10.21105/joss.02807"],
                 "links": {
                     "DOI": ["10.21105/joss.02807"],
                     "CITATIONS": False,
                     "REFERENCES": False
                 }
             },
            {
                "bibcode": "2021zndo...4441439K",
                "identifier": ["2021zndo...4441439K", "10.5281/zenodo.4441439"],
                "links": {
                    "DOI": ["10.5281/zenodo.4441439"],
                    "ESOURCE": {
                        "PUB_HTML": {
                            "url": ["https://doi.org/10.5281/zenodo.4441439"],
                            "title": ["https://doi.org/10.5281/zenodo.4441439"]
                        }
                    },
                    "CITATIONS": True,
                    "REFERENCES": False
                }
            }
        ]
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        response = self.client.put('/update_new', data=json.dumps(stub_data), headers=headers)
        self.assertEqual(response._status_code, 200)
        self.assertEqual(response.json['status'], 'updated db with new data successfully')


    def test_link_type_all(self):
        """
        return links for all types of a bibcode
        :return:
        """
        self.add_stub_data()
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        response = self.client.get('/2013MNRAS.435.1904M/new', headers=headers)
        self.assertEqual(response._status_code, 200)
        self.assertDictEqual(response.json, {u'action': u'display', u'links': {u'count': 17, u'records': [
                                                {u'url': u'/2013MNRAS.435.1904M/ABSTRACT', u'count': 1, u'bibcode': u'2013MNRAS.435.1904M', u'type': u'abstract', u'title': u'ABSTRACT (1)'},
                                                {u'url': u'/2013MNRAS.435.1904M/CITATIONS', u'count': 1, u'bibcode': u'2013MNRAS.435.1904M', u'type': u'citations', u'title': u'CITATIONS (1)'},
                                                {u'url': u'/2013MNRAS.435.1904M/REFERENCES', u'count': 1, u'bibcode': u'2013MNRAS.435.1904M', u'type': u'references', u'title': u'REFERENCES (1)'},
                                                {u'url': u'/2013MNRAS.435.1904M/COREADS', u'count': 1, u'bibcode': u'2013MNRAS.435.1904M', u'type': u'coreads', u'title': u'COREADS (1)'},
                                                {u'url': u'/2013MNRAS.435.1904M/OPENURL', u'count': 1, u'bibcode': u'2013MNRAS.435.1904M', u'type': u'openurl', u'title': u'OPENURL (1)'},
                                                {u'url': u'/2013MNRAS.435.1904M/GRAPHICS', u'count': 1, u'bibcode': u'2013MNRAS.435.1904M', u'type': u'graphics', u'title': u'GRAPHICS (1)'},
                                                {u'url': u'/2013MNRAS.435.1904M/METRICS', u'count': 1, u'bibcode': u'2013MNRAS.435.1904M', u'type': u'metrics', u'title': u'METRICS (1)'},
                                                {u'url': u'/2013MNRAS.435.1904M/SIMILAR', u'count': 1, u'bibcode': u'2013MNRAS.435.1904M', u'type': u'similar', u'title': u'SIMILAR (1)'},
                                                {u'url': u'/2013MNRAS.435.1904M/ESOURCE', u'count': 4, u'bibcode': u'2013MNRAS.435.1904M', u'type': u'esource', u'title': u'ESOURCE (4)'},
                                                {u'url': u'/2013MNRAS.435.1904M/DATA', u'count': 39, u'bibcode': u'2013MNRAS.435.1904M', u'type': u'data', u'title': u'DATA (39)'},
                                                {u'url': u'/2013MNRAS.435.1904M/DOI', u'count': 1, u'bibcode': u'2013MNRAS.435.1904M', u'type': u'doi', u'title': u'DOI (1)'},
                                                {u'url': u'/2013MNRAS.435.1904M/ARXIV', u'count': 1, u'bibcode': u'2013MNRAS.435.1904M', u'type': u'arxiv', u'title': u'ARXIV (1)'}],
                                             u'link_type': 'all'}, u'service': u''})


    def test_link_inspire(self):
        """
        return a record of link type == inspire
        :return:
        """
        self.add_stub_data()
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        response = self.client.get('/1943RvMP...15....1C/INSPIRE/new', headers=headers)
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
        response = self.client.get('/2017MNRAS.467.3556B/PRESENTATION/new', headers=headers)
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
        response = self.client.get('/1971ATsir.615....4D/ASSOCIATED/new', headers=headers)
        self.assertEqual(response._status_code, 200)
        self.assertDictEqual(response.json, {u'action': u'display',
                                             u'links': {u'count': 13,
                                                        u'records': [{u'url': u'/1971ATsir.615....4D/associated/:%2Fabs%2F1971ATsir.615....4D%2Fabstract', u'bibcode': u'1971ATsir.615....4D', u'title': u'Part  1'},
                                                                     {u'url': u'/1971ATsir.615....4D/associated/:%2Fabs%2F1974Afz....10..315D%2Fabstract', u'bibcode': u'1974Afz....10..315D', u'title': u'Part  2'},
                                                                     {u'url': u'/1971ATsir.615....4D/associated/:%2Fabs%2F1971ATsir.621....7D%2Fabstract', u'bibcode': u'1971ATsir.621....7D', u'title': u'Part  3'},
                                                                     {u'url': u'/1971ATsir.615....4D/associated/:%2Fabs%2F1976Afz....12..665D%2Fabstract', u'bibcode': u'1976Afz....12..665D', u'title': u'Part  4'},
                                                                     {u'url': u'/1971ATsir.615....4D/associated/:%2Fabs%2F1971ATsir.624....1D%2Fabstract', u'bibcode': u'1971ATsir.624....1D', u'title': u'Part  5'},
                                                                     {u'url': u'/1971ATsir.615....4D/associated/:%2Fabs%2F1983Afz....19..229D%2Fabstract', u'bibcode': u'1983Afz....19..229D', u'title': u'Part  6'},
                                                                     {u'url': u'/1971ATsir.615....4D/associated/:%2Fabs%2F1983Ap.....19..134D%2Fabstract', u'bibcode': u'1983Ap.....19..134D', u'title': u'Part  7'},
                                                                     {u'url': u'/1971ATsir.615....4D/associated/:%2Fabs%2F1973ATsir.759....6D%2Fabstract', u'bibcode': u'1973ATsir.759....6D', u'title': u'Part  8'},
                                                                     {u'url': u'/1971ATsir.615....4D/associated/:%2Fabs%2F1984Afz....20..525D%2Fabstract', u'bibcode': u'1984Afz....20..525D', u'title': u'Part  9'},
                                                                     {u'url': u'/1971ATsir.615....4D/associated/:%2Fabs%2F1984Ap.....20..290D%2Fabstract', u'bibcode': u'1984Ap.....20..290D', u'title': u'Part 10'},
                                                                     {u'url': u'/1971ATsir.615....4D/associated/:%2Fabs%2F1974ATsir.809....1D%2Fabstract', u'bibcode': u'1974ATsir.809....1D', u'title': u'Part 11'},
                                                                     {u'url': u'/1971ATsir.615....4D/associated/:%2Fabs%2F1974ATsir.809....2D%2Fabstract', u'bibcode': u'1974ATsir.809....2D', u'title': u'Part 12'},
                                                                     {u'url': u'/1971ATsir.615....4D/associated/:%2Fabs%2F1974ATsir.837....2D%2Fabstract', u'bibcode': u'1974ATsir.837....2D', u'title': u'Part 13'}],
                                                        u'link_type': u'ASSOCIATED'},
                                             u'service': u'/abs/1971ATsir.615....4D/associated'})


    def test_link_esource_subtype(self):
        """
        check status code for calling process_request for a esource sub type link
        :return:
        """
        self.add_stub_data()
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        response = self.client.get('/2013MNRAS.435.1904M/EPRINT_HTML/new', headers=headers)
        self.assertEqual(response._status_code, 200)
        self.assertDictEqual(response.json, {u'action': u'redirect',
                                             u'link': u'https://arxiv.org/abs/1307.6556',
                                             u'link_type': u'ESOURCE|EPRINT_HTML',
                                             u'service': u'https://arxiv.org/abs/1307.6556'
                                             })


    def test_link_esource(self):
        """
        returning list of urls
        :return:
        """
        self.add_stub_data()
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        response = self.client.get('/2013MNRAS.435.1904M/ESOURCE/new', headers=headers)
        self.assertEqual(response._status_code, 200)
        self.assertDictEqual(response.json, {u'action': u'display',
                                             u'links': {u'count': 4,
                                                        u'link_type': u'ESOURCE',
                                                        u'bibcode': u'2013MNRAS.435.1904M',
                                                        u'records': [
                                                            {u'url': u'https://academic.oup.com/mnras/pdf-lookup/doi/10.1093/mnras/stt1379', u'title': u'https://academic.oup.com/mnras/pdf-lookup/doi/10.1093/mnras/stt1379', u'link_type': u'ESOURCE|PUB_PDF'},
                                                            {u'url': u'https://doi.org/10.1093%2Fmnras%2Fstt1379', u'title': u'https://doi.org/10.1093%2Fmnras%2Fstt1379', u'link_type': u'ESOURCE|PUB_HTML'},
                                                            {u'url': u'https://arxiv.org/pdf/1307.6556', u'title': u'https://arxiv.org/pdf/1307.6556', u'link_type': u'ESOURCE|EPRINT_PDF'},
                                                            {u'url': u'https://arxiv.org/abs/1307.6556', u'title': u'https://arxiv.org/abs/1307.6556', u'link_type': u'ESOURCE|EPRINT_HTML'},
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
        response = self.client.get('/2013MNRAS.435.1904M/ESA/new', headers=headers)
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
        response = self.client.get('/2013MNRAS.435.1904M/DATA/new', headers=headers)
        self.assertEqual(response._status_code, 200)
        self.assertDictEqual(response.json,{u'action': u'display',
                                            u'service': u'',
                                            u'links': {u'count': 8,
                                            u'records': [{u'url': u'http://archives.esac.esa.int', # ESA
                                                          u'data': [{u'url': u'/2013MNRAS.435.1904M/DATA|ESA/http%3A%2F%2Farchives.esac.esa.int%2Fehst%2F%23bibcode%3D2013MNRAS.435.1904M',
                                                                     u'title': u'European HST References (EHST)',
                                                                     u'link_type': u'DATA|ESA'}],
                                                          u'title': u'ESAC Science Data Center'
                                                         },
                                                         {u'url': u'https://ned.ipac.caltech.edu',  # NED
                                                          u'data': [{u'url': u'/2013MNRAS.435.1904M/DATA|NED/https%3A%2F%2Fned.ipac.caltech.edu%2Furi%2FNED%3A%3AInRefcode%2F2013MNRAS.435.1904M',
                                                                     u'title': u'NED Objects (1)',
                                                                     u'link_type': u'DATA|NED'}],
                                                          u'title': u'NASA/IPAC Extragalactic Database'
                                                         },
                                                         {u'url': u'http://nxsa.esac.esa.int',  # XMM
                                                          u'data': [{u'url': u'/2013MNRAS.435.1904M/DATA|XMM/https%3A%2F%2Fnxsa.esac.esa.int%2Fnxsa-web%2F%23bibcode%3D2013MNRAS.435.1904M',
                                                                     u'title': u'XMM data (1 observations)',
                                                                     u'link_type': u'DATA|XMM'}],
                                                          u'title': u'XMM Newton Science Archive'
                                                         },
                                                         {u'url': u'http://archive.stsci.edu',  # MAST
                                                          u'data': [{u'url': u'/2013MNRAS.435.1904M/DATA|MAST/https%3A%2F%2Farchive.stsci.edu%2Fmastbibref.php%3Fbibcode%3D2013MNRAS.435.1904M',
                                                                     u'title': u'MAST References (HST, EUVE, GALEX)',
                                                                     u'link_type': u'DATA|MAST'}],
                                                          u'title': u'Mikulski Archive for Space Telescopes'
                                                         },
                                                         {u'url': u'http://simbad.u-strasbg.fr', # SIMBAD
                                                          u'data': [{u'url': u'/2013MNRAS.435.1904M/DATA|SIMBAD/http%3A%2F%2Fsimbad.u-strasbg.fr%2Fsimbo.pl%3Fbibcode%3D2013MNRAS.435.1904M',
                                                                     u'title': u'SIMBAD Objects (30)',
                                                                     u'link_type': u'DATA|SIMBAD'}],
                                                          u'title': u'SIMBAD Database at the CDS'
                                                         },
                                                         {u'url': u'http://cxc.harvard.edu/cda',  # Chandra
                                                          u'data': [{u'url': u'/2013MNRAS.435.1904M/DATA|Chandra/https%3A%2F%2Fcda.harvard.edu%2Fchaser%3Fobsid%3D494%2C493%2C5290%2C5289%2C5286%2C5288%2C5287%2C3666%2C6162%2C6159%2C6163%2C6160%2C6161%2C13413%2C12028%2C10900%2C10898%2C13416%2C13414%2C12029%2C12027%2C13417%2C10899%2C13412%2C10901%2C13415%2C12026',
                                                                     u'title': u'Chandra Data Archive ObsIds 494, 493, 5290, 5289, 5286, 5288, 5287, 3666, 6162, 6159, 6163, 6160, 6161, 13413, 12028, 10900, 10898, 13416, 13414, 12029, 12027, 13417, 10899, 13412, 10901, 13415, 12026',
                                                                      u'link_type': u'DATA|Chandra'}],
                                                          u'title': u'Chandra X-Ray Observatory'
                                                         },
                                                         {u'url': u'https://heasarc.gsfc.nasa.gov/', # HEASARC
                                                          u'data': [{u'url': u'/2013MNRAS.435.1904M/DATA|HEASARC/http%3A%2F%2Fheasarc.gsfc.nasa.gov%2Fcgi-bin%2FW3Browse%2Fbiblink.pl%3Fcode%3D2013MNRAS.435.1904M',
                                                                     u'title': u'http://heasarc.gsfc.nasa.gov/cgi-bin/W3Browse/biblink.pl?code=2013MNRAS.435.1904M',
                                                                     u'link_type': u'DATA|HEASARC'}],
                                                          u'title': u"NASA's High Energy Astrophysics Science Archive Research Center"
                                                         },
                                                         {u'url': u'https://www.cosmos.esa.int/web/herschel/home', #Herschel
                                                          u'data': [{u'url': u'/2013MNRAS.435.1904M/DATA|Herschel/http%3A%2F%2Farchives.esac.esa.int%2Fhsa%2Fwhsa%2F%3FACTION%3DPUBLICATION%26ID%3D2013MNRAS.435.1904M',
                                                                     u'title': u'http://archives.esac.esa.int/hsa/whsa/?ACTION=PUBLICATION&ID=2013MNRAS.435.1904M',
                                                                     u'link_type': u'DATA|Herschel'}],
                                                          u'title': u'Herschel Science Center'
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
        results = get_records_new(bibcode='errorbibcode', link_type='ASSOCIATED')
        response = LinkRequest(bibcode='').request_link_type_associated(results)
        self.assertEqual(response._status_code, 404)


    def test_link_esource_error_bibcode(self):
        """
        return 404 for not finding any records
        :return:
        """
        results = get_records_new(bibcode='errorbibcode', link_type='ESOURCE')
        response = LinkRequest(bibcode='').request_link_type_esource(results)
        self.assertEqual(response._status_code, 404)


    def test_link_data_error_bibcode(self):
        """
        return 404 for not finding any records
        :return:
        """
        results = get_records_new(bibcode='errorbibcode', link_type='DATA')
        response = LinkRequest(bibcode='').request_link_type_data(results)
        self.assertEqual(response._status_code, 404)


    def test_process_request_upsert(self):
        """
        return 200 for successful insert/update to db
        :return:
        """
        self.add_stub_data()
        document_record = {
            "bibcode": "1513efua.book.....S",
            "identifier": [],
            "links": {
                "LIBRARYCATALOG": {
                    "url": ["http://catalog.loc.gov/cgi-bin/Pwebrecon.cgi?v3=1&DB=local&CMD=010a+unk82013020&CNT=10+records+per+page"],
                    "title": ['']
                }
            }
        }
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        # insert it here
        response = self.client.put('/update_new', data=json.dumps([document_record]), headers=headers)
        self.assertEqual(response._status_code, 200)
        self.assertEqual(response.json['status'], 'updated db with new data successfully')
        # select it here
        response = self.client.get('/1513efua.book.....S/LIBRARYCATALOG/new', headers=headers)
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
        response = self.client.delete('/delete_new', data=json.dumps(bibcodes), headers=headers)
        self.assertEqual(response._status_code, 200)
        self.assertEqual(response.json['status'], 'removed 1 records of 1 bibcodes')
        # select it here
        response = self.client.get('/2013MNRAS.435.1904M/ESOURCE/new', headers=headers)
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
        response = self.client.get('/2019AIPC.2081c0032P/TOC/new', headers=headers)
        self.assertEqual(response._status_code, 404)
        # insert it here
        document_record = {"bibcode": "2019AIPC.2081c0032P",
                           "identifier": [],
                           "links": {"TOC": True}}
        response = self.client.put('/update_new', data=json.dumps([document_record]), headers=headers)
        self.assertEqual(response._status_code, 200)
        self.assertEqual(response.json['status'], 'updated db with new data successfully')
        # select it here
        response = self.client.get('/2019AIPC.2081c0032P/TOC/new', headers=headers)
        self.assertEqual(response._status_code, 200)
        self.assertDictEqual(response.json, {u'action': u'redirect',
                                             u'link': u'/abs/2019AIPC.2081c0032P/toc',
                                             u'service': u'/abs/2019AIPC.2081c0032P/toc',
                                             u'link_type': u'TOC'})
        # delete it here
        bibcodes = {'bibcode': ['2019AIPC.2081c0032P']}
        response = self.client.delete('/delete_new', data=json.dumps(bibcodes), headers=headers)
        self.assertEqual(response._status_code, 200)
        # verify that is gone
        response = self.client.get('/2019AIPC.2081c0032P/TOC/new', headers=headers)
        self.assertEqual(response._status_code, 404)


    def test_link_esource_subtype_article(self):
        """
        check status code for calling process_request for a esource sub type link for legacy type article
        :return:
        """
        self.add_stub_data()
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        response = self.client.get('/2007ASPC..368...27R/ARTICLE/new', headers=headers)
        self.assertEqual(response._status_code, 200)
        self.assertDictEqual(response.json, {u'action': u'redirect',
                                             u'link': u'http://articles.adsabs.harvard.edu/pdf/2007ASPC..368...27R',
                                             u'service': u'http://articles.adsabs.harvard.edu/pdf/2007ASPC..368...27R',
                                             u'link_type': u'ESOURCE|ADS_PDF'})
        response = self.client.get('/2013MNRAS.435.1904M/ARTICLE/new', headers=headers)
        self.assertEqual(response._status_code, 200)
        self.assertDictEqual(response.json, {u'action': u'redirect',
                                             u'link': u'https://academic.oup.com/mnras/pdf-lookup/doi/10.1093/mnras/stt1379',
                                             u'service': u'https://academic.oup.com/mnras/pdf-lookup/doi/10.1093/mnras/stt1379',
                                             u'link_type': u'ESOURCE|PUB_PDF'})


    def test_data_subtype_multiple_links(self):
        """

        :return:
        """
        self.add_stub_data()
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        response = self.client.get('/2004ApJS..152..163R/MAST/new', headers=headers)
        self.assertEqual(response._status_code, 200)
        self.assertDictEqual(response.json, {u'action': u'display',
                                             u'links': {u'bibcode': u'2004ApJS..152..163R',
                                             u'count': 1,
                                             u'records': [{u'data': [{u'link_type': u'DATA|MAST',
                                                                      u'title': u'MAST References (HST)',
                                                                      u'url': u'/2004ApJS..152..163R/DATA|MAST/http%3A%2F%2Farchive.stsci.edu%2Fmastbibref.php%3Fbibcode%3D2004ApJS..152..163R'}],
                                                           u'title': u'Mikulski Archive for Space Telescopes',
                                                           u'url': u'http://archive.stsci.edu'},
                                                          {u'data': [{u'link_type': u'DATA|MAST',
                                                                      u'title': u'GEMS: Galaxy Evolution from Morphologies and SEDs (Hans-Walter Rix)',
                                                                      u'url': u'/2004ApJS..152..163R/DATA|MAST/http%3A%2F%2Farchive.stsci.edu%2Fprepds%2Fgems'}],
                                                           u'title': u'Mikulski Archive for Space Telescopes',
                                                           u'url': u'http://archive.stsci.edu'}]},
                                             u'service': u''})


    def test_verify_url(self):
        """

        :return:
        """
        self.add_stub_data()
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        response = self.client.get('/1514temg.book.....V/verify_url:https%3A%2F%2Fwww.si.edu%2Fobject%2Fsiris_sil_154413/new', headers=headers)
        self.assertEqual(response.json, {'link': 'verified'})
        response = self.client.get('/1514temg.book.....V/verify_url:http%3A%2F%2Fwww.google.com/new', headers=headers)
        self.assertEqual(response.json, {'link': 'not found'})


    def test_link_esource_subtype_article_no_record(self):
        """
        check status code for calling process_request for a esource sub type link for legacy type article where there is no esource
        :return:
        """
        self.add_stub_data()
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        # no esource record
        response = self.client.get('/2021JOSS....6.2807C/ARTICLE/new', headers=headers)
        self.assertEqual(response._status_code, 404)
        self.assertDictEqual(response.json, {'error': 'did not find any records'})
        # no %_PDF record
        response = self.client.get('/2021zndo...4441439K/ARTICLE/new', headers=headers)
        self.assertEqual(response._status_code, 404)
        self.assertDictEqual(response.json, {'error': 'did not find any records'})


    def test_get_records_failure(self):
        """

        :return:
        """
        with self.assertRaises(Exception) as context:
            get_records_new({'bibcode':'is single value'})
            self.assertTrue("can't adapt type 'dict'" in str(context))
        with self.assertRaises(Exception) as context:
            document_records = {
                'status': 2,  # name='new', index=2, number=2,
                'document_records': [
                    {
                         'bibcode': '2021JOSS....6.2807C',
                         'identifier': ['2021JOSS....6.2807C'],
                         'links': {
                             'DOI': ['10.21105/joss.02807'],
                             'CITATIONS': False,
                             'REFERENCES': False
                         }
                    }, {
                         'bibcode': '2021JOSS....6.2807C',
                         'identifier': ['2021JOSS....6.2807C'],
                         'links': {
                             'DOI': ['10.21105/joss.02807'],
                             'CITATIONS': False,
                             'REFERENCES': False
                         }
                    },
                ]
            }
            # duplicate records
            add_records_new(DocumentRecords(**document_records))
            self.assertTrue("ON CONFLICT DO UPDATE command cannot affect row a second time" in str(context))
        with self.assertRaises(Exception) as context:
            del_records_new([12, 14])
            self.assertTrue("operator does not exist: character varying = integer" in str(context))
        with self.assertRaises(Exception) as context:
            get_ids({'id': ['is a list']})
            self.assertTrue("no matches found in database" in str(context))

    def test_reconciliation(self):
        """

        :return:
        """
        self.add_stub_data()
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        identifiers = ['doi:10.1093/mnras/stt1379', 'arXiv:1702.02377', 'https://doi.org/10.5281/zenodo.4441439', '10.1086/420885', 'astro-ph/0703637']
        response = self.client.post('/reconciliation', data=json.dumps({'identifier':identifiers}), headers=headers)
        self.assertEqual(response._status_code, 200)
        self.assertDictEqual(response.json, {'ids': [
            ['10.1093/mnras/stt1379', '2013MNRAS.435.1904M'],
            ['arXiv:1702.02377', '2017MNRAS.467.3556B'],
            ['10.5281/zenodo.4441439', '2021zndo...4441439K'],
            ['10.1086/420885', '2004ApJS..152..163R'],
            ['astro-ph/0703637', 'not in database']
        ]})


if __name__ == '__main__':
    unittest.main()
