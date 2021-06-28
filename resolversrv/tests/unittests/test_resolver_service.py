# -*- coding: utf-8 -*-

import sys
import os
PROJECT_HOME = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../'))
sys.path.append(PROJECT_HOME)

from flask_testing import TestCase
import unittest

import resolversrv.app as app
from resolversrv.views import LinkRequest

TestCase.maxDiff = None

class test_resolver(TestCase):
    def create_app(self):
        self.current_app = app.create_app()
        return self.current_app

    # the following four types' links are created on the fly
    def test_fetchingAbstract(self):
        response = LinkRequest('1987gady.book.....B', 'ABSTRACT').process_request()
        self.assertEqual(response._status_code, 200)
        self.assertDictEqual(eval(response.response[0]), {"action": "redirect", "link": "/abs/1987gady.book.....B/abstract", "link_type": "ABSTRACT", "service": "/abs/1987gady.book.....B/abstract"})
    def test_fetchingCitations(self):
        response = LinkRequest('1987gady.book.....B', 'CITATIONS').process_request()
        self.assertEqual(response._status_code, 200)
        self.assertDictEqual(eval(response.response[0]), {"action": "redirect", "link": "/abs/1987gady.book.....B/citations", "link_type": "CITATIONS", "service": "/abs/1987gady.book.....B/citations"})
    def test_fetchingCoRead(self):
        response = LinkRequest('1987gady.book.....B', 'COREADS').process_request()
        self.assertEqual(response._status_code, 200)
        self.assertDictEqual(eval(response.response[0]), {"action": "redirect", "link": "/abs/1987gady.book.....B/coreads", "link_type": "COREADS", "service": "/abs/1987gady.book.....B/coreads"})
    def test_fetchingReferences(self):
        response = LinkRequest('1998ARA&A..36..189K', 'REFERENCES').process_request()
        self.assertEqual(response._status_code, 200)
        self.assertDictEqual(eval(response.response[0]), {"action": "redirect", "link": "/abs/1998ARA&A..36..189K/references", "link_type": "REFERENCES", "service": "/abs/1998ARA&A..36..189K/references"})


    # the following three tests support of legacy type EJOURNAL
    def test_fetchingEJOURNAL(self):
        link_request = LinkRequest('1668RSPT....3..863M', 'EJOURNAL', self.current_app.config['RESOLVER_GATEWAY_URL'])
        self.assertEqual(link_request.link_type, 'ESOURCE')
        self.assertEqual(link_request.link_sub_type, 'PUB_HTML')
    def test_fetchingPreprint(self):
        link_request = LinkRequest('1991hep.th...10030D', 'PREPRINT', self.current_app.config['RESOLVER_GATEWAY_URL'])
        self.assertEqual(link_request.link_type, 'ESOURCE')
        self.assertEqual(link_request.link_sub_type, 'EPRINT_HTML')
    def test_fetchingGIF(self):
        link_request = LinkRequest('1990ARA&A..28..215D', 'GIF', self.current_app.config['RESOLVER_GATEWAY_URL'])
        self.assertEqual(link_request.link_type, 'ESOURCE')
        self.assertEqual(link_request.link_sub_type, 'ADS_SCAN')


    # the following four tests verifies minor/major link type init
    def test_linkTypeData(self):
        link_request = LinkRequest('2013MNRAS.435.1904M', 'DATA', self.current_app.config['RESOLVER_GATEWAY_URL'])
        self.assertEqual(link_request.link_type, 'DATA')
        self.assertEqual(link_request.link_sub_type, None)
    def test_linkSubTypeData(self):
        link_request = LinkRequest('2013MNRAS.435.1904M', 'Chandra', self.current_app.config['RESOLVER_GATEWAY_URL'])
        self.assertEqual(link_request.link_type, 'DATA')
        self.assertEqual(link_request.link_sub_type, 'Chandra')
    def test_linkSubTypeESOURCE(self):
        link_request = LinkRequest('1668RSPT....3..863M', 'PUB_HTML', self.current_app.config['RESOLVER_GATEWAY_URL'])
        self.assertEqual(link_request.link_type, 'ESOURCE')
        self.assertEqual(link_request.link_sub_type, 'PUB_HTML')
    def test_linkTypeEmpty(self):
        link_request = LinkRequest('1668RSPT....3..863M', '', self.current_app.config['RESOLVER_GATEWAY_URL'])
        self.assertEqual(link_request.link_type, None)
        self.assertEqual(link_request.link_sub_type, None)
    def test_linkTypeError(self):
        link_request = LinkRequest('1668RSPT....3..863M', 'ERROR', self.current_app.config['RESOLVER_GATEWAY_URL'])
        self.assertEqual(link_request.link_type, '?')
        self.assertEqual(link_request.link_sub_type, '?')


    # the following tests verify that private methods from class LinkRequest function properly
    def test_privateMethodLinkRequest1(self):
        link_request = LinkRequest('2013MNRAS.435.1904M', 'DATA', self.current_app.config['RESOLVER_GATEWAY_URL'])
        self.assertEqual(link_request._LinkRequest__get_url_hostname_with_protocol('http://cda.harvard.edu/chaser?obsid=494'),
                         'http://cda.harvard.edu/')
    def test_privateMethodLinkRequest2(self):
        link_request = LinkRequest('2013MNRAS.435.1904M', 'DATA', self.current_app.config['RESOLVER_GATEWAY_URL'])
        self.assertEqual(link_request._LinkRequest__get_url_hostname('http://cda.harvard.edu/chaser?obsid=494'),
                         'cda.harvard.edu')
    def test_privateMethodLinkRequest3(self):
        link_request = LinkRequest('2013MNRAS.435.1904M', 'DATA', self.current_app.config['RESOLVER_GATEWAY_URL'])
        title,url = link_request._LinkRequest__get_data_source_title_url('SIMBAD', '')
        self.assertEqual(title, 'SIMBAD Database at the CDS')
        self.assertEqual(url, 'http://simbad.u-strasbg.fr')
    def test_privateMethodLinkRequest4(self):
        link_request = LinkRequest('2013MNRAS.435.1904M', 'DATA', self.current_app.config['RESOLVER_GATEWAY_URL'])
        title,url = link_request._LinkRequest__get_data_source_title_url('Author', 'http://author.does-not.have.url')
        self.assertEqual(title, 'Author Hosted Dataset')
        self.assertEqual(url, 'http://author.does-not.have.url')
    def test_privateMethodLinkRequest5(self):
        link_request = LinkRequest('2013MNRAS.435.1904M', 'DATA', self.current_app.config['RESOLVER_GATEWAY_URL'])
        title,url = link_request._LinkRequest__get_data_source_title_url('newSubType', 'http://newSubType.does-not.have.url')
        self.assertEqual(title, 'Resource at http://newSubType.does-not.have.url')
        self.assertEqual(url, 'http://newSubType.does-not.have.url')
    def test_privateMethodLinkRequest6(self):
        link_request = LinkRequest('2013MNRAS.435.1904M', 'DATA', self.current_app.config['RESOLVER_GATEWAY_URL'])
        self.assertEqual(link_request._LinkRequest__update_data_type_hostname('https://ned.ipac.caltech.edu', 'NED',
                                                                              'http://$NED$/cgi-bin/nph-objsearch?search_type=Search&refcode=2013MNRAS.435.1904M'),
                                                                              'http://ned.ipac.caltech.edu/cgi-bin/nph-objsearch?search_type=Search&refcode=2013MNRAS.435.1904M')
    def test_privateMethodLinkRequest7(self):
        link_request = LinkRequest('2013MNRAS.435.1904M', 'DATA', self.current_app.config['RESOLVER_GATEWAY_URL'])
        self.assertEqual(link_request._LinkRequest__update_data_type_hostname('http://simbad.u-strasbg.fr', 'SIMBAD',
                                                                              'http://$SIMBAD$/simbo.pl?bibcode=2013MNRAS.435.1904M'),
                                                                              'http://simbad.u-strasbg.fr/simbo.pl?bibcode=2013MNRAS.435.1904M')
    def test_privateMethodLinkRequest8(self):
        link_request = LinkRequest('1948TrPul..61....5Z', 'DATA', self.current_app.config['RESOLVER_GATEWAY_URL'])
        self.assertEqual(link_request._LinkRequest__update_data_type_hostname('http://vizier.u-strasbg.fr', 'Vizier',
                                                                              'http://$VIZIER$/viz-bin/VizieR?-source=I/45'),
                                                                              'http://vizier.u-strasbg.fr/viz-bin/VizieR?-source=I/45')
    def test_privateMethodLinkRequest9(self):
        link_request = LinkRequest('1905POPot..50....1L', 'DATA', self.current_app.config['RESOLVER_GATEWAY_URL'])
        self.assertEqual(link_request._LinkRequest__update_data_type_hostname('http://vizier.u-strasbg.fr/', 'CDS',
                                                                              'http://$VIZIER$/viz-bin/VizieR?-source=IV/26'),
                                                                              'http://vizier.u-strasbg.fr/viz-bin/VizieR?-source=IV/26')
    def test_privateMethodLinkRequest10(self):
        link_request = LinkRequest('2013MNRAS.435.1904M', 'DATA', self.current_app.config['RESOLVER_GATEWAY_URL'])
        self.assertEqual(link_request._LinkRequest__update_data_type_hostname('http://cxc.harvard.edu/cda', 'Chandra',
                                                                              'http://cda.harvard.edu/chaser?obsid=494'),
                                                                              'http://cda.harvard.edu/chaser?obsid=494')
    def test_privateMethodLinkRequest11(self):
        link_request = LinkRequest('1979A&AS...38..423G', 'DATA', self.current_app.config['RESOLVER_GATEWAY_URL'])
        self.assertEqual(link_request._LinkRequest__update_data_type_hostname('http://vizier.u-strasbg.fr/', 'CDS',
                                                                              'http://cdsweb.u-strasbg.fr/cgi-bin/qcat?V/35'),
                                                                              'http://cdsweb.u-strasbg.fr/cgi-bin/qcat?V/35')

    # the following tests verify that public methods from class LinkRequest function properly
    def test_publicMethodLinkRequest1(self):
        response = LinkRequest('1987gady.book.....B', 'ABSTRACT').request_link_type_deterministic_single_url_toJSON('')
        self.assertEqual(response._status_code, 404)
        self.assertEqual(response.response[0], b'{"error": "did not find any records"}')
    def test_publicMethodLinkRequest2(self):
        response = LinkRequest('2003MNRAS.342.1117M', 'CD').verify_url('http%3A%2F%2Fvizier.u-strasbg.fr%2Fviz-bin%2FVizieR%3F-source%3DIV%2F26')
        self.assertEqual(response._status_code, 200)
        self.assertEqual(response.response[0], b'{"link": "verified"}')

    def test_route(self):
        """
        Tests for the existence of a the endpoint route
        """
        r = self.client.get('/1987gady.book.....B/ABSTRACT')
        self.assertEqual(r.status_code, 200)

    def test_check_link_type(self):
        r = self.client.get('/check_link_type/ABSTRACT')
        self.assertEqual(r.status_code, 200)
        r = self.client.get('/check_link_type/DATA|ISO')
        self.assertEqual(r.status_code, 200)
        r = self.client.get('/check_link_type/DATA|ISO2')
        self.assertEqual(r.status_code, 400)
        r = self.client.get('/check_link_type/ABSTRACT|ISO')
        self.assertEqual(r.status_code, 400)
        r = self.client.get('/check_link_type/DATA|ACA')
        self.assertEqual(r.status_code, 200)

    def test_case_insensetive_link_sub_type_data(self):
        """
        Test case insensitvity of data link subtypes
        """
        lowercase_data_sub_type = ['aca', 'alma', 'ari', 'astroverse', 'atnf', 'author', 'bavj', 'bicep2', 'cadc', 'cds', 'chandra', 'dryad', 'esa', 'eso', 'figshare', 'gcpd', 'gemini', 'github', 'gtc', 'heasarc', 'herschel', 'ibvs', 'ines', 'irsa', 'iso', 'jwst', 'koa', 'lpl', 'mast', 'ned', 'nexsci', 'noao', 'pangaea', 'pasa', 'pdg', 'pds', 'protocols', 'simbad', 'spitzer', 'tns', 'vizier', 'xmm', 'zenodo']
        uppercase_data_sub_type = ['ACA', 'ALMA', 'ARI', 'ASTROVERSE', 'ATNF', 'AUTHOR', 'BAVJ', 'BICEP2', 'CADC', 'CDS', 'CHANDRA', 'DRYAD', 'ESA', 'ESO', 'FIGSHARE', 'GCPD', 'GEMINI', 'GITHUB', 'GTC', 'HEASARC', 'HERSCHEL', 'IBVS', 'INES', 'IRSA', 'ISO', 'JWST', 'KOA', 'LPL', 'MAST', 'NED', 'NEXSCI', 'NOAO', 'PANGAEA', 'PASA', 'PDG', 'PDS', 'PROTOCOLS', 'SIMBAD', 'SPITZER', 'TNS', 'VIZIER', 'XMM', 'ZENODO']
        mixedcase_data_sub_type = ['AcA', 'ALMA', 'ARI', 'Astroverse', 'ATNF', 'Author', 'BAVJ', 'BICEP2', 'CADC', 'CDS', 'Chandra', 'Dryad', 'ESA', 'ESO', 'Figshare', 'GCPD', 'Gemini', 'Github', 'GTC', 'HEASARC', 'Herschel', 'IBVS', 'INES', 'IRSA', 'ISO', 'JWST', 'KOA', 'LPL', 'MAST', 'NED', 'NExScI', 'NOAO', 'PANGAEA', 'PASA', 'PDG', 'PDS', 'protocols', 'SIMBAD', 'Spitzer', 'TNS', 'Vizier', 'XMM', 'Zenodo']
        for lower,db in zip(lowercase_data_sub_type, mixedcase_data_sub_type):
            link_request = LinkRequest('anybibcode', lower, self.current_app.config['RESOLVER_GATEWAY_URL'])
            self.assertEqual(link_request.link_type, 'DATA')
            self.assertEqual(link_request.link_sub_type, db)
        for upper,db in zip(uppercase_data_sub_type, mixedcase_data_sub_type):
            link_request = LinkRequest('anybibcode', upper, self.current_app.config['RESOLVER_GATEWAY_URL'])
            self.assertEqual(link_request.link_type, 'DATA')
            self.assertEqual(link_request.link_sub_type, db)


    def test_associated_redirect_url(self):
        """

        """
        link_request = LinkRequest('1990A&AS...83...71D', 'ASSOCIATED')
        bibcode, redirectURL = link_request._LinkRequest__get_associated_redirect_url(url='1987A&A...179...60C')
        self.assertEqual(bibcode, '1987A&A...179...60C')
        self.assertEqual(redirectURL, 'http://localhost:5050/link_gateway/1990A&AS...83...71D/associated/:%2Fabs%2F1987A%26A...179...60C%2Fabstract')


if __name__ == '__main__':
  unittest.main()