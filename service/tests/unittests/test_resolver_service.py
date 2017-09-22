# -*- coding: utf-8 -*-

import sys
import os
PROJECT_HOME = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '../../'))
sys.path.append(PROJECT_HOME)

from flask_testing import TestCase
import unittest
import app as app
from linksRequest import *

class TestResolver(TestCase):
    def create_app(self):
        #Start the wsgi application
        return app.create_app()

    def test_fetchingAbstract(self):
        self.assertEqual(processRequest('1987gady.book.....B','ABSTRACT'), ['https://ui.adsabs.harvard.edu/#abs/1987gady.book.....B/ABSTRACT', 200])

    def test_fetchingCitations(self):
        self.assertEqual(processRequest('1987gady.book.....B', 'CITATIONS'), ['https://ui.adsabs.harvard.edu/#abs/1987gady.book.....B/CITATIONS', 200])

    def test_fetchingEJOURNAL(self):
        self.assertEqual(processRequest('1668RSPT....3..863M', 'EJOURNAL'), ['http://www.jstor.org/stable/101320?origin=ads', 200])

    def test_fetchingARTICLE(self):
        self.assertEqual(processRequest('1668RSPT....3..863M', 'ARTICLE'), ['http://www.jstor.org/stable/101320?origin=ads', 200])

    def test_fetchingGIF(self):
        self.assertEqual(processRequest('1990ARA&A..28..215D', 'GIF'), ['http://articles.adsabs.harvard.edu/full/1990ARA&A..28..215D', 200])

    def test_fetchingSpires(self):
        self.assertEqual(processRequest('1968PhLB...28..223A', 'INSPIRE'), ['http://inspirehep.net/search?p=find+j+PHLTA,B28,223', 200])

    def test_fetchingComments(self):
        self.assertEqual(processRequest('2005A&A...440..775K', 'COMMENTS'), ['http://adsabs.harvard.edu/NOTES/2005A+A...440..775K.html', 200])

    def test_fetchingARI(self):
        self.assertEqual(processRequest('1885AMOW.1882..167R', 'ARI'), ['http://dc.g-vo.org/arigfh/katkat/byhdw/qp/1385', 200])

    # def test_fetchingLibrary(self):
    #     self.assertEqual(processRequest('1987gady.book.....B', 'LIBRARY'), 'https://catalog.loc.gov/legacy.html')

    def test_fetchingMultimedia(self):
        self.assertEqual(processRequest('1999bha..progE...4B', 'PRESENTATION'), ['http://online.kitp.ucsb.edu/online/bhole99/begelman/', 200])

    def test_fetchingNED(self):
        self.assertEqual(processRequest('1885AN....112..245H', 'NED'), ['http://$NED$/cgi-bin/nph-objsearch?search_type=Search&refcode=1885AN....112..245H', 200])

    # def test_fetchingAssociated(self):
    #     self.assertEqual(processRequest('2000ApJ...539L..13G', 'ASSOCIATED'), 'http://adsabs.harvard.edu/cgi-bin/nph-ref_query?bibcode=2000ApJ...539L..13G&amp;refs=ASSOCIATED&amp;db_key=AST')

    def test_fetchingReferences(self):
        self.assertEqual(processRequest('1998ARA&A..36..189K', 'REFERENCES'), ['https://ui.adsabs.harvard.edu/#abs/1998ARA&A..36..189K/REFERENCES', 200])

    def test_fetchingSIMBAD(self):
        self.assertEqual(processRequest('1861MNRAS..21...68B', 'SIMBAD'), ['http://$SIMBAD$/simbo.pl?bibcode=1861MNRAS..21...68B', 200])

    # def test_fetchingTOC(self):
    #     self.assertEqual(processRequest('1990ARA&A..28..215D', 'TOC'), 'http://adsabs.harvard.edu/cgi-bin/nph-abs_connect?bibcode=1990ARA%26A..28&amp;db_key=ALL&amp;sort=BIBCODE&amp;nr_to_return=500&amp;data_and=YES&amp;toc_link=YES')

    def test_fetchingAR(self):
        self.assertEqual(processRequest('1987gady.book.....B', 'COREADS'), ['https://ui.adsabs.harvard.edu/#abs/1987gady.book.....B/COREADS', 200])

    def test_fetchingRepring(self):
        self.assertEqual(processRequest('1991hep.th...10030D', 'PREPRINT'), ['https://arxiv.org/abs/hep-th/9110030', 200])

    def test_fetchingARXIV_HTML(self):
        self.assertEqual(processRequest('1991hep.th...10030D', 'PREPRINT'), ['https://arxiv.org/abs/hep-th/9110030', 200])

    # def test_fetchingCustom(self):
    #     self.assertEqual(processRequest('1987gady.book.....B', 'CUSTOM'), 'http://adsabs.harvard.edu/abs/1987gady.book.....B&amp;data_type=REFERENCES&amp;format=%25Q')

    def test_route(self):
        """
        Tests for the existence of a /linkURL route, and that it returns
        properly formatted JSON data
        """
        r = self.client.get('/resolver/1987gady.book.....B/ABSTRACT')
        self.assertEqual(r.status_code, 200)

if __name__ == '__main__':
  unittest.main()