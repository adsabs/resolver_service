# -*- coding: utf-8 -*-

import sys
import os
PROJECT_HOME = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../'))
sys.path.append(PROJECT_HOME)

from flask_testing import TestCase
import unittest

from google.protobuf.json_format import MessageToDict

from adsmsg import DataLinksRecordList, DocumentRecords

import resolversrv.app as app
from resolversrv.models import DataLinks
from resolversrv.utils import add_records, add_records_new
from resolversrv.views import LinkRequest, PopulateRequest

TestCase.maxDiff = None

class test_with_no_database_required(TestCase):

    def create_app(self):
        self.current_app = app.create_app()
        return self.current_app

    def test_add_records_no_data(self):
        """
        return False and text explanation when an empty DataLinksRecordList is passed to add_records
        :return:
        """
        status, text = add_records(DataLinksRecordList())
        self.assertEqual(status, False)
        self.assertEqual(text, 'unable to add records to the database')

    def test_process_request_no_bibcode_error(self):
        """
        return 400 for bibcode of length 0
        :return:
        """
        response = LinkRequest(bibcode='', link_type='PRESENTATION').process_request()
        self.assertEqual(response._status_code, 400)
        self.assertEqual(eval(response.response[0]), {"error": "no bibcode received"})

    def test_link_no_url(self):
        """
        return 404 for not finding any records
        :return:
        """
        response = LinkRequest(bibcode='2017MNRAS.467.3556B', link_type='PRESENTATION').request_link_type_single_url(None)
        self.assertEqual(response._status_code, 404)
        self.assertEqual(eval(response.response[0]), {"error": "did not find any records"})


    def test_link_url_KeyError(self):
        """
        return 400 from request_link_type_single_url where there is KeyError
        :return:
        """
        results = [{'bibcode': u'2017MNRAS.467.3556B',
                    'link_type': u'PRESENTATION',
                    'link_sub_type': '',
                    'title': [u''],
                    'url_KeyError': ['http://www.astro.lu.se/~alexey/animations.html'],
                    'itemCount': 0,
                    }]
        response = LinkRequest(bibcode='2017MNRAS.467.3556B', link_type='PRESENTATION').request_link_type_single_url(results)
        self.assertEqual(response._status_code, 400)
        self.assertEqual(eval(response.response[0]), {"error": "requested information for bibcode=2017MNRAS.467.3556B and link_type=PRESENTATION is missing"})


    def test_link_url_IndexError(self):
        """
        return 400 from request_link_type_single_url when there is IndexError
        :return:
        """
        results = [{'bibcode': u'2017MNRAS.467.3556B',
                    'link_type': u'PRESENTATION',
                    'link_sub_type': '',
                    'title': [u''],
                    'url': [],
                    'itemCount': 0,
                    }]
        response = LinkRequest(bibcode='2017MNRAS.467.3556B', link_type='PRESENTATION').request_link_type_single_url(results)
        self.assertEqual(response._status_code, 400)
        self.assertEqual(eval(response.response[0]), {"error": "requested information for bibcode=2017MNRAS.467.3556B and link_type=PRESENTATION is missing"})


    def test_link_type_single_url(self):
        """
        return a url from request_link_type_single_url when results passed in is correct and complete
        :return:
        """
        results = [{'bibcode': u'2017MNRAS.467.3556B',
                    'link_type': u'PRESENTATION',
                    'link_sub_type': '',
                    'title': [u''],
                    'url': ['http://www.astro.lu.se/~alexey/animations.html'],
                    'itemCount': 0,
                    }]
        response = LinkRequest(bibcode='2017MNRAS.467.3556B', link_type='PRESENTATION').request_link_type_single_url(results)
        self.assertEqual(response._status_code, 200)
        self.assertDictEqual(eval(response.response[0]), {"action": "redirect", "link": "http://www.astro.lu.se/~alexey/animations.html", "link_type": "PRESENTATION", "service": "http://www.astro.lu.se/~alexey/animations.html"})


    def test_link_presentation_error_link_type(self):
        """
        return 400 for unrecognizable link type
        :return:
        """
        response = LinkRequest(bibcode='2017MNRAS.467.3556B', link_type='errorlinktype').process_request()
        self.assertEqual(response._status_code, 400)

    def test_link_associated_KeyError(self):
        """
        return 400 from request_link_type_associated where there is KeyError
        :return:
        """
        results = [{'bibcode': u'1971ATsir.615....4D',
                    'link_type': u'ASSOCIATED',
                    'link_sub_type': '',
                    'title': [u'Part 11', u'Part 10', u'Part 13', u'Part 12', u'Part  8', u'Part  9', u'Part  2', u'Part  3', u'Part  1', u'Part  6', u'Part  7', u'Part  4', u'Part  5'],
                    'url_KeyError': [u'1971ATsir.615....4D', u'1971ATsir.624....1D', u'1976Afz....12..665D', u'1983Ap.....19..134D', u'1983Afz....19..229D', u'1974ATsir.809....2D', u'1984Afz....20..525D', u'1974Afz....10..315D', u'1984Ap.....20..290D', u'1973ATsir.759....6D', u'1974ATsir.837....2D', u'1974ATsir.809....1D', u'1971ATsir.621....7D'],
                    'itemCount': 0,
                    }]
        response = LinkRequest(bibcode='1971ATsir.615....4D', link_type='ASSOCIATED').request_link_type_associated(results)
        self.assertEqual(response._status_code, 400)
        self.assertEqual(eval(response.response[0]), {"error": "requested information for bibcode=1971ATsir.615....4D and link_type=ASSOCIATED is missing"})


    def test_link_associated_IndexError(self):
        """
        return 400 from request_link_type_associated when there is IndexError
        :return:
        """
        results = [{'bibcode': u'1971ATsir.615....4D',
                    'link_type': u'ASSOCIATED',
                    'link_sub_type': '',
                    'title': [u'Part 11'],
                    'url': [u'1971ATsir.615....4D', u'1971ATsir.624....1D', u'1976Afz....12..665D', u'1983Ap.....19..134D', u'1983Afz....19..229D', u'1974ATsir.809....2D', u'1984Afz....20..525D', u'1974Afz....10..315D', u'1984Ap.....20..290D', u'1973ATsir.759....6D', u'1974ATsir.837....2D', u'1974ATsir.809....1D', u'1971ATsir.621....7D'],
                    'itemCount': 0,
                    }]
        response = LinkRequest(bibcode='1971ATsir.615....4D', link_type='ASSOCIATED').request_link_type_associated(results)
        self.assertEqual(response._status_code, 400)
        self.assertEqual(eval(response.response[0]), {"error": "requested information for bibcode=1971ATsir.615....4D and link_type=ASSOCIATED is missing"})


    def test_link_esource_KeyError(self):
        """
        return 400 from request_link_type_esource where there is KeyError
        :return:
        """
        results = [{'bibcode': u'2013MNRAS.435.1904M',
                    'link_type': u'ESOURCE',
                    'link_sub_type': u'EPRINT_HTML',
                    'title': [u''],
                    'url_KeyError': [u'http://arxiv.org/abs/1307.6556'],
                    'itemCount': 0}]
        response = LinkRequest(bibcode='2013MNRAS.435.1904', link_type='ESOURCE').request_link_type_esource(results)
        self.assertEqual(response._status_code, 400)
        self.assertEqual(eval(response.response[0]), {"error": "requested information for bibcode=2013MNRAS.435.1904 and link_type=ESOURCE is missing"})


    def test_link_no_url_esource(self):
        """
        return 404 from request_link_type_esource when there is IndexError
        :return:
        """
        results = [{'bibcode': u'2013MNRAS.435.1904M',
                    'link_type': u'ESOURCE',
                    'link_sub_type': u'EPRINT_HTML',
                    'title': [u''],
                    'url': [],
                    'itemCount': 0}]
        response = LinkRequest(bibcode='2013MNRAS.435.1904', link_type='ESOURCE').request_link_type_esource(results)
        self.assertEqual(response._status_code, 404)
        self.assertEqual(eval(response.response[0]), {"error": "did not find any records"})

    def test_link_esource_multiple_urls(self):
        """
        return multiple escourse
        :return:
        """
        results = [{'bibcode': u'22020AANv....1..199K',
                    'link_type': u'ESOURCE',
                    'link_sub_type': u'PUB_PDF',
                    'title': [u''],
                    'url': ['http://astronomianova.org/pdf/AAN1_2020.pdf',
                            'http://uavso.org.ua/ila/2020AANv....1..199K.pdf',
                            'http://www.oa.uj.edu.pl/pbl/AAN/AAN6.pdf'''],
                    'itemCount': 0}]
        response = LinkRequest(bibcode='2020AANv....1..199K', link_type='ESOURCE').request_link_type_esource(results)
        response_json = {'action': 'display', 'service': '',
                         'links': {'count': 1,
                                   'records': [{'url': 'http://astronomianova.org/pdf/AAN1_2020.pdf', 'link_type': 'ESOURCE|PUB_PDF', 'title': 'http://astronomianova.org/pdf/AAN1_2020.pdf'},
                                               {'url': 'http://uavso.org.ua/ila/2020AANv....1..199K.pdf', 'link_type': 'ESOURCE|PUB_PDF', 'title': 'http://uavso.org.ua/ila/2020AANv....1..199K.pdf'},
                                               {'url': 'http://www.oa.uj.edu.pl/pbl/AAN/AAN6.pdf', 'link_type': 'ESOURCE|PUB_PDF', 'title': 'http://www.oa.uj.edu.pl/pbl/AAN/AAN6.pdf'}],
                                   'bibcode': '2020AANv....1..199K', 'link_type': 'ESOURCE'}}
        self.assertEqual(response._status_code, 200)
        self.assertEqual(eval(response.response[0]), response_json)

    def test_link_data_KeyError(self):
        """
        return 400 from request_link_type_data where there is KeyError
        :return:
        """
        results = [{'bibcode': u'2013MNRAS.435.1904M',
                    'link_type': u'DATA',
                    'link_sub_type': u'MAST',
                    'title': [u'MAST References (GALEX EUVE HST)'],
                    'url_KeyError': [u'http://archive.stsci.edu/mastbibref.php?bibcode=2013MNRAS.435.1904M'],
                    'itemCount': 3}]
        response = LinkRequest(bibcode='2013MNRAS.435.1904', link_type='PUB_PDF').request_link_type_data(results)
        self.assertEqual(response._status_code, 400)
        self.assertEqual(eval(response.response[0]), {"error": "requested information for bibcode=2013MNRAS.435.1904 and link_type=ESOURCE is missing"})


    def test_link_data_IndexError(self):
        """
        return 404 from request_link_type_data when there is IndexError
        :return:
        """
        results = [{'bibcode': u'2013MNRAS.435.1904M',
                    'link_type': u'DATA',
                    'link_sub_type': u'MAST',
                    'title': [u'MAST References (GALEX EUVE HST)'],
                    'url': [],
                    'itemCount': 3}]
        response = LinkRequest(bibcode='2013MNRAS.435.1904M', link_type='MAST').request_link_type_data(results)
        self.assertEqual(response._status_code, 404)
        self.assertEqual(eval(response.response[0]), {"error": "did not find any records"})


    def test_process_request_no_payload(self):
        """
        return 400 for payload of None
        :return:
        """
        response = PopulateRequest().process_request(None)
        self.assertEqual(response._status_code, 400)
        self.assertEqual(eval(response.response[0]), {"error": "no data received"})


    def test_process_request_error_msg_code_payload(self):
        """
        return 400 for payload with unrecognizable msg-type
        :return:
        """
        response = PopulateRequest().process_request('empty')
        self.assertEqual(response._status_code, 400)
        self.assertEqual(eval(response.response[0]), {"error": "unable to extract data from protobuf structure -- Failed to parse datalinks_records field: repeated field datalinks_records must be in [] which is empty.."})


    def test_process_request_empty_msg_payload(self):
        """
        return 400 for payload with empty msg structure
        :return:
        """
        response = PopulateRequest().process_request(MessageToDict(DataLinksRecordList(), True, True))
        self.assertEqual(response._status_code, 400)
        self.assertEqual(eval(response.response[0]), {"error": "unable to extract data from protobuf structure -- Failed to parse datalinks_records field: repeated field datalinks_records must be in [] which is {\'datalinks_records\': [], \'status\': \'active\'}.."})


    def test_link_indentifications(self):
        """
        returning a url for either DOI or arXiv link types
        :return:
        """
        response = LinkRequest(bibcode='2010ApJ...713L.103B', link_type='DOI', id='10.1088/2041-8205/713/2/L103').process_request()
        self.assertEqual(response._status_code, 200)
        self.assertDictEqual(eval(response.response[0]), {"action": "redirect", "link": "https://doi.org/10.1088/2041-8205/713/2/L103", "link_type": "DOI", "service": "https://doi.org/10.1088/2041-8205/713/2/L103"})

        response = LinkRequest(bibcode='2018arXiv180303598K', link_type='ARXIV', id='1803.03598').process_request()
        self.assertEqual(response._status_code, 200)
        self.assertDictEqual(eval(response.response[0]), {"action": "redirect", "link": "http://arxiv.org/abs/1803.03598", "link_type": "ARXIV", "service": "http://arxiv.org/abs/1803.03598"})


    def test_datalinks(self):
        """
        verify DataLinks class functions properly
        :return:
        """
        data_link = DataLinks(bibcode='2013MNRAS.435.1904M',
                              link_type='ESOURCE',
                              link_sub_type='EPRINT_PDF',
                              url={'http://arxiv.org/pdf/1307.6556'},
                              title={''},
                              item_count=0)
        self.assertEqual(data_link.toJSON(), {'bibcode': '2013MNRAS.435.1904M',
                                              'title': set(['']),
                                              'url': set(['http://arxiv.org/pdf/1307.6556']),
                                              'link_sub_type': 'EPRINT_PDF',
                                              'itemCount': 0,
                                              'link_type': 'ESOURCE'})



class test_with_no_database_required_new(TestCase):

    def create_app(self):
        self.current_app = app.create_app()
        return self.current_app

    def test_add_records_no_data(self):
        """
        return False and text explanation when an empty DocumentRecords is passed to add_records
        :return:
        """
        status, text = add_records_new(DocumentRecords())
        self.assertEqual(status, False)
        self.assertEqual(text, 'unable to add records to the database')

    def test_process_request_no_bibcode_error(self):
        """
        return 400 for bibcode of length 0
        :return:
        """
        response = LinkRequest(bibcode='', link_type='PRESENTATION').process_request_new()
        self.assertEqual(response._status_code, 400)
        self.assertEqual(eval(response.response[0]), {"error": "no bibcode received"})

    def test_link_no_url(self):
        """
        return 404 for not finding any records
        :return:
        """
        response = LinkRequest(bibcode='2017MNRAS.467.3556B', link_type='PRESENTATION').request_link_type_single_url(None)
        self.assertEqual(response._status_code, 404)
        self.assertEqual(eval(response.response[0]), {"error": "did not find any records"})


    def test_link_url_KeyError(self):
        """
        return 400 from request_link_type_single_url where there is KeyError
        :return:
        """
        results = [{'bibcode': u'2017MNRAS.467.3556B',
                    'link_type': u'PRESENTATION',
                    'link_sub_type': '',
                    'title': [u''],
                    'url_KeyError': ['http://www.astro.lu.se/~alexey/animations.html'],
                    'itemCount': 0,
                    }]
        response = LinkRequest(bibcode='2017MNRAS.467.3556B', link_type='PRESENTATION').request_link_type_single_url(results)
        self.assertEqual(response._status_code, 400)
        self.assertEqual(eval(response.response[0]), {"error": "requested information for bibcode=2017MNRAS.467.3556B and link_type=PRESENTATION is missing"})


    def test_link_url_IndexError(self):
        """
        return 400 from request_link_type_single_url when there is IndexError
        :return:
        """
        results = [{'bibcode': u'2017MNRAS.467.3556B',
                    'link_type': u'PRESENTATION',
                    'link_sub_type': '',
                    'title': [u''],
                    'url': [],
                    'itemCount': 0,
                    }]
        response = LinkRequest(bibcode='2017MNRAS.467.3556B', link_type='PRESENTATION').request_link_type_single_url(results)
        self.assertEqual(response._status_code, 400)
        self.assertEqual(eval(response.response[0]), {"error": "requested information for bibcode=2017MNRAS.467.3556B and link_type=PRESENTATION is missing"})


    def test_link_type_single_url(self):
        """
        return a url from request_link_type_single_url when results passed in is correct and complete
        :return:
        """
        results = [{'bibcode': u'2017MNRAS.467.3556B',
                    'link_type': u'PRESENTATION',
                    'link_sub_type': '',
                    'title': [u''],
                    'url': ['http://www.astro.lu.se/~alexey/animations.html'],
                    'itemCount': 0,
                    }]
        response = LinkRequest(bibcode='2017MNRAS.467.3556B', link_type='PRESENTATION').request_link_type_single_url(results)
        self.assertEqual(response._status_code, 200)
        self.assertDictEqual(eval(response.response[0]), {"action": "redirect", "link": "http://www.astro.lu.se/~alexey/animations.html", "link_type": "PRESENTATION", "service": "http://www.astro.lu.se/~alexey/animations.html"})


    def test_link_presentation_error_link_type(self):
        """
        return 400 for unrecognizable link type
        :return:
        """
        response = LinkRequest(bibcode='2017MNRAS.467.3556B', link_type='errorlinktype').process_request_new()
        self.assertEqual(response._status_code, 400)

    def test_link_associated_KeyError(self):
        """
        return 400 from request_link_type_associated where there is KeyError
        :return:
        """
        results = [{'bibcode': u'1971ATsir.615....4D',
                    'link_type': u'ASSOCIATED',
                    'link_sub_type': '',
                    'title': [u'Part 11', u'Part 10', u'Part 13', u'Part 12', u'Part  8', u'Part  9', u'Part  2', u'Part  3', u'Part  1', u'Part  6', u'Part  7', u'Part  4', u'Part  5'],
                    'url_KeyError': [u'1971ATsir.615....4D', u'1971ATsir.624....1D', u'1976Afz....12..665D', u'1983Ap.....19..134D', u'1983Afz....19..229D', u'1974ATsir.809....2D', u'1984Afz....20..525D', u'1974Afz....10..315D', u'1984Ap.....20..290D', u'1973ATsir.759....6D', u'1974ATsir.837....2D', u'1974ATsir.809....1D', u'1971ATsir.621....7D'],
                    'itemCount': 0,
                    }]
        response = LinkRequest(bibcode='1971ATsir.615....4D', link_type='ASSOCIATED').request_link_type_associated(results)
        self.assertEqual(response._status_code, 400)
        self.assertEqual(eval(response.response[0]), {"error": "requested information for bibcode=1971ATsir.615....4D and link_type=ASSOCIATED is missing"})


    def test_link_associated_IndexError(self):
        """
        return 400 from request_link_type_associated when there is IndexError
        :return:
        """
        results = [{'bibcode': u'1971ATsir.615....4D',
                    'link_type': u'ASSOCIATED',
                    'link_sub_type': '',
                    'title': [u'Part 11'],
                    'url': [u'1971ATsir.615....4D', u'1971ATsir.624....1D', u'1976Afz....12..665D', u'1983Ap.....19..134D', u'1983Afz....19..229D', u'1974ATsir.809....2D', u'1984Afz....20..525D', u'1974Afz....10..315D', u'1984Ap.....20..290D', u'1973ATsir.759....6D', u'1974ATsir.837....2D', u'1974ATsir.809....1D', u'1971ATsir.621....7D'],
                    'itemCount': 0,
                    }]
        response = LinkRequest(bibcode='1971ATsir.615....4D', link_type='ASSOCIATED').request_link_type_associated(results)
        self.assertEqual(response._status_code, 400)
        self.assertEqual(eval(response.response[0]), {"error": "requested information for bibcode=1971ATsir.615....4D and link_type=ASSOCIATED is missing"})


    def test_link_esource_KeyError(self):
        """
        return 400 from request_link_type_esource where there is KeyError
        :return:
        """
        results = [{'bibcode': u'2013MNRAS.435.1904M',
                    'link_type': u'ESOURCE',
                    'link_sub_type': u'EPRINT_HTML',
                    'title': [u''],
                    'url_KeyError': [u'http://arxiv.org/abs/1307.6556'],
                    'itemCount': 0}]
        response = LinkRequest(bibcode='2013MNRAS.435.1904', link_type='ESOURCE').request_link_type_esource(results)
        self.assertEqual(response._status_code, 400)
        self.assertEqual(eval(response.response[0]), {"error": "requested information for bibcode=2013MNRAS.435.1904 and link_type=ESOURCE is missing"})


    def test_link_no_url_esource(self):
        """
        return 404 from request_link_type_esource when there is IndexError
        :return:
        """
        results = [{'bibcode': u'2013MNRAS.435.1904M',
                    'link_type': u'ESOURCE',
                    'link_sub_type': u'EPRINT_HTML',
                    'title': [u''],
                    'url': [],
                    'itemCount': 0}]
        response = LinkRequest(bibcode='2013MNRAS.435.1904', link_type='ESOURCE').request_link_type_esource(results)
        self.assertEqual(response._status_code, 404)
        self.assertEqual(eval(response.response[0]), {"error": "did not find any records"})

    def test_link_esource_multiple_urls(self):
        """
        return multiple escourse
        :return:
        """
        results = [{'bibcode': u'22020AANv....1..199K',
                    'link_type': u'ESOURCE',
                    'link_sub_type': u'PUB_PDF',
                    'title': [u''],
                    'url': ['http://astronomianova.org/pdf/AAN1_2020.pdf',
                            'http://uavso.org.ua/ila/2020AANv....1..199K.pdf',
                            'http://www.oa.uj.edu.pl/pbl/AAN/AAN6.pdf'''],
                    'itemCount': 0}]
        response = LinkRequest(bibcode='2020AANv....1..199K', link_type='ESOURCE').request_link_type_esource(results)
        response_json = {'action': 'display', 'service': '',
                         'links': {'count': 1,
                                   'records': [{'url': 'http://astronomianova.org/pdf/AAN1_2020.pdf', 'link_type': 'ESOURCE|PUB_PDF', 'title': 'http://astronomianova.org/pdf/AAN1_2020.pdf'},
                                               {'url': 'http://uavso.org.ua/ila/2020AANv....1..199K.pdf', 'link_type': 'ESOURCE|PUB_PDF', 'title': 'http://uavso.org.ua/ila/2020AANv....1..199K.pdf'},
                                               {'url': 'http://www.oa.uj.edu.pl/pbl/AAN/AAN6.pdf', 'link_type': 'ESOURCE|PUB_PDF', 'title': 'http://www.oa.uj.edu.pl/pbl/AAN/AAN6.pdf'}],
                                   'bibcode': '2020AANv....1..199K', 'link_type': 'ESOURCE'}}
        self.assertEqual(response._status_code, 200)
        self.assertEqual(eval(response.response[0]), response_json)

    def test_link_data_KeyError(self):
        """
        return 400 from request_link_type_data where there is KeyError
        :return:
        """
        results = [{'bibcode': u'2013MNRAS.435.1904M',
                    'link_type': u'DATA',
                    'link_sub_type': u'MAST',
                    'title': [u'MAST References (GALEX EUVE HST)'],
                    'url_KeyError': [u'http://archive.stsci.edu/mastbibref.php?bibcode=2013MNRAS.435.1904M'],
                    'itemCount': 3}]
        response = LinkRequest(bibcode='2013MNRAS.435.1904', link_type='PUB_PDF').request_link_type_data(results)
        self.assertEqual(response._status_code, 400)
        self.assertEqual(eval(response.response[0]), {"error": "requested information for bibcode=2013MNRAS.435.1904 and link_type=ESOURCE is missing"})


    def test_link_data_IndexError(self):
        """
        return 404 from request_link_type_data when there is IndexError
        :return:
        """
        results = [{'bibcode': u'2013MNRAS.435.1904M',
                    'link_type': u'DATA',
                    'link_sub_type': u'MAST',
                    'title': [u'MAST References (GALEX EUVE HST)'],
                    'url': [],
                    'itemCount': 3}]
        response = LinkRequest(bibcode='2013MNRAS.435.1904M', link_type='MAST').request_link_type_data(results)
        self.assertEqual(response._status_code, 404)
        self.assertEqual(eval(response.response[0]), {"error": "did not find any records"})


    def test_process_request_no_payload(self):
        """
        return 400 for payload of None
        :return:
        """
        response = PopulateRequest().process_request_new(None)
        self.assertEqual(response._status_code, 400)
        self.assertEqual(eval(response.response[0]), {"error": "no data received"})


    def test_process_request_error_msg_code_payload(self):
        """
        return 400 for payload with unrecognizable msg-type
        :return:
        """
        response = PopulateRequest().process_request_new('empty')
        self.assertEqual(response._status_code, 400)
        self.assertEqual(eval(response.response[0]), {"error": "unable to extract data from protobuf structure -- Failed to parse document_records field: repeated field document_records must be in [] which is empty.."})


    def test_process_request_empty_msg_payload(self):
        """
        return 400 for payload with empty msg structure
        :return:
        """
        response = PopulateRequest().process_request_new(MessageToDict(DocumentRecords(), True, True))
        self.assertEqual(response._status_code, 400)
        self.assertEqual(eval(response.response[0]), {"error": "unable to extract data from protobuf structure -- Failed to parse document_records field: repeated field document_records must be in [] which is {\'document_records\': [], \'status\': \'active\'}.."})


    def test_link_indentifications(self):
        """
        returning a url for either DOI or arXiv link types
        :return:
        """
        response = LinkRequest(bibcode='2010ApJ...713L.103B', link_type='DOI', id='10.1088/2041-8205/713/2/L103').process_request_new()
        self.assertEqual(response._status_code, 200)
        self.assertDictEqual(eval(response.response[0]), {"action": "redirect", "link": "https://doi.org/10.1088/2041-8205/713/2/L103", "link_type": "DOI", "service": "https://doi.org/10.1088/2041-8205/713/2/L103"})

        response = LinkRequest(bibcode='2018arXiv180303598K', link_type='ARXIV', id='1803.03598').process_request_new()
        self.assertEqual(response._status_code, 200)
        self.assertDictEqual(eval(response.response[0]), {"action": "redirect", "link": "http://arxiv.org/abs/1803.03598", "link_type": "ARXIV", "service": "http://arxiv.org/abs/1803.03598"})


    def test_datalinks(self):
        """
        verify DataLinks class functions properly
        :return:
        """
        data_link = DataLinks(bibcode='2013MNRAS.435.1904M',
                              link_type='ESOURCE',
                              link_sub_type='EPRINT_PDF',
                              url={'http://arxiv.org/pdf/1307.6556'},
                              title={''},
                              item_count=0)
        self.assertEqual(data_link.toJSON(), {'bibcode': '2013MNRAS.435.1904M',
                                              'title': set(['']),
                                              'url': set(['http://arxiv.org/pdf/1307.6556']),
                                              'link_sub_type': 'EPRINT_PDF',
                                              'itemCount': 0,
                                              'link_type': 'ESOURCE'})

if __name__ == '__main__':
    unittest.main()
