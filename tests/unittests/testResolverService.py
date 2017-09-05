import sys
import os
PROJECT_HOME = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '../../'))
sys.path.append(PROJECT_HOME)

from flask_testing import TestCase
import unittest
import app as app
from linksData import *

class TestResolver(TestCase):
    def create_app(self):
        app_ = app.create_app()
        return app_

    def test_fetchingAbstract(self):
        assert(getURL('1987gady.book.....B','ABSTRACT') == 'http://adsabs.harvard.edu/abs/1987gady.book.....B')

    def test_fetchingCitations(self):
        assert(getURL('1987gady.book.....B', 'CITATIONS') == 'http://adsabs.harvard.edu/cgi-bin/nph-ref_query?bibcode=1987gady.book.....B&amp;refs=CITATIONS&amp;db_key=AST')

    def test_fetchingData(self):
        assert(getURL('1998AJ....115.2285M', 'DATA') == 'http://adsabs.harvard.edu/cgi-bin/nph-data_query?bibcode=1998AJ....115.2285M&db_key=AST&link_type=DATA')

    def test_fetchingEJOURNAL(self):
        assert(getURL('1998ARA&A..36..189K', 'EJOURNAL') == 'http://www.annualreviews.org/doi/full/10.1146/annurev.astro.36.1.189')

    def test_fetchingARTICLE(self):
        assert(getURL('1998ARA&A..36..189K', 'ARTICLE') == 'http://www.annualreviews.org/doi/pdf/10.1146/annurev.astro.36.1.189')

    def test_fetchingGIF(self):
        assert(getURL('1990ARA&A..28..215D', 'GIF') == 'http://articles.adsabs.harvard.edu/full/1990ARA%26A..28..215D')

    def test_fetchingSpires(self):
        assert(getURL('1998ARA&A..36..189K', 'SPIRES') == 'http://inspirehep.net/search?p=find+j+ARAAA,36,189')

    def test_fetchingComments(self):
        assert(getURL('2005A&A...440..775K', 'COMMENTS') == 'http://adsabs.harvard.edu/NOTES/2005A+A...440..775K.html')

    def test_fetchingMail(self):
        assert(getURL('1989agna.book.....O', 'MAIL') == 'http://www.uscibooks.com/oster.htm')

    def test_fetchingLibrary(self):
        assert(getURL('1987gady.book.....B', 'LIBRARY') == 'https://catalog.loc.gov/legacy.html')

    def test_fetchingMultimedia(self):
        assert(getURL('MULTIMEDIABibcode01', 'MULTIMEDIA') == 'https://ui.adsabs.harvard.edu')

    def test_fetchingNED(self):
        assert(getURL('1998ApJ...498..541K', 'NED') == 'http://ned.ipac.caltech.edu/cgi-bin/nph-objsearch?search_type=Search&refcode=1998ApJ...498..541K')

    def test_fetchingAssociated(self):
        assert(getURL('2000ApJ...539L..13G', 'ASSOCIATED') == 'http://adsabs.harvard.edu/cgi-bin/nph-ref_query?bibcode=2000ApJ...539L..13G&amp;refs=ASSOCIATED&amp;db_key=AST')

    def test_fetchingPDS(self):
        assert(getURL('1995PASP..107..156H', 'PDS') == 'http://pdsproto.jpl.nasa.gov/catalog/dataset/results.CFM?ResultsSelBox=HST-J-WFPC2-3-SL9-IMPACT-V1.0')

    def test_fetchingReferences(self):
        assert(getURL('1998ARA&A..36..189K', 'REFERENCES') == 'http://adsabs.harvard.edu/cgi-bin/nph-ref_query?bibcode=1998ARA%26A..36..189K&amp;refs=REFERENCES&amp;db_key=AST')

    def test_fetchingSIMBAD(self):
        assert(getURL('1998ARA&A..36..189K', 'SIMBAD') == 'http://simbad.harvard.edu/simbad/sim-ref?querymethod=bib&simbo=on&submit=submit+bibcode&bibcode=1998ARA%26A..36..189K')

    def test_fetchingTOC(self):
        assert(getURL('1990ARA&A..28..215D', 'TOC') == 'http://adsabs.harvard.edu/cgi-bin/nph-abs_connect?bibcode=1990ARA%26A..28&amp;db_key=ALL&amp;sort=BIBCODE&amp;nr_to_return=500&amp;data_and=YES&amp;toc_link=YES')

    def test_fetchingAR(self):
        assert(getURL('1987gady.book.....B', 'AR') == 'http://adsabs.harvard.edu/cgi-bin/nph-ref_query?bibcode=1987gady.book.....B&amp;refs=AR&amp;db_key=AST')

    def test_fetchingRepring(self):
        assert(getURL('1998ARA&A..36..189K', 'PREPRINT') == 'https://arxiv.org/abs/astro-ph/9807187')

    def test_fetchingCustom(self):
        assert(getURL('1987gady.book.....B', 'CUSTOM') == 'http://adsabs.harvard.edu/abs/1987gady.book.....B&amp;data_type=REFERENCES&amp;format=%25Q')

    def test_route(self):
        """
        Tests for the existence of a /linkURL route, and that it returns
        properly formatted JSON data
        """
        r = self.client.get('/linkURL?bibcode=1987gady.book.....B&link_type=ABSTRACT')
        self.assertEqual(r.status_code, 200)

if __name__ == '__main__':
  unittest.main()