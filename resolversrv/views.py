#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import inspect
import json

from flask import request, Blueprint
from flask_discoverer import advertise
from flask import Response
from requests.utils import quote

from adsmutils import load_config, setup_logging

import resolversrv
from resolversrv.models import *


bp = Blueprint('resolver_service', __name__)

class LinkRequest():

    baseurl = 'https://ui.adsabs.harvard.edu/#abs'

    # we have 8 link types that are created on the fly and do not need to go to db
    # as of now, 8/27/2017, we are to eliminate the COMMENTS and CUSTOM links
    on_the_fly = {
        'ABSTRACT' : '{baseurl}/{bibcode}/abstract',
        'CITATIONS': '{baseurl}/{bibcode}/citations',
        'REFERENCES': '{baseurl}/{bibcode}/references',
        'COREADS': '{baseurl}/{bibcode}/coreads',
        #'COMMENTS': '???',
        'TOC': '{baseurl}/{bibcode}/toc',
        'OPENURL': '{baseurl}/{bibcode}/openurl',
        #'CUSTOM': '???'
    }

    # electronic journal sub types
    esource = [
        'PUB_PDF', 'EPRINT_PDF', 'AUTHOR_PDF', 'ADS_PDF',
        'PUB_HTML', 'EPRINT_HTML', 'AUTHOR_HTML', 'ADS_SCAN'
    ]

    # data sub types
    data =  [
        'ARI', 'SIMBAD', 'NED', 'CDS', 'Vizier', 'GCPD', 'Author', 'PDG', 'MAST', 'HEASARC', 'INES', 'IBVS', 'Astroverse',
        'ESA', 'NExScI', 'PDS', 'AcA', 'ISO', 'ESO', 'CXO', 'NOAO', 'XMM', 'Spitzer', 'PASA', 'ATNF', 'KOA', 'Herschel',
        'GTC', 'BICEP2', 'ALMA', 'CADC', 'Zenodo', 'TNS', ''
    ]

    link_types = on_the_fly.keys() + ['ARTICLE', 'DATA', 'INSPIRE', 'LIBRARYCATALOG', 'PRESENTATION', 'ASSOCIATED']

    bibcode = ''
    link_type = ''
    link_sub_type = ''

    logger = None
    config = {}

    def __init__(self, bibcode, link_type):
        self.config = {}
        self.config.update(load_config(proj_home=os.path.dirname(inspect.getsourcefile(resolversrv))))

        self.logger = setup_logging('resolver_service', self.config.get('LOG_LEVEL', 'INFO'))

        self.bibcode = bibcode
        self.__set_major_minor_link_types(link_type)
        self.__backward_compatibility(link_type)


    def __backward_compatibility(self, link_type):
        """
        GIF, EJOURNAL, and PREPRINT are classics' types
        for backward compatibility we are recognizing them

        :param link_type:
        """
        if (link_type == 'GIF'):
            self.link_type = 'ARTICLE'
            self.link_sub_type = 'ADS_SCAN'
        elif (link_type == 'PREPRINT'):
            self.link_type = 'ARTICLE'
            self.link_sub_type = 'EPRINT_HTML'
        elif (link_type == 'EJOURNAL'):
            self.link_type = 'ARTICLE'
            self.link_sub_type = 'PUB_HTML'


    def __set_major_minor_link_types(self, link_type):
        """
        figure out what are the link type and sub link type
        from one input param

        :param link_type:
        """
        if (link_type in self.link_types):
            self.link_type = link_type
            self.link_sub_type = ''
        else:
            # we have two sets of sub link type, figure out which one it is
            if (link_type in self.esource):
                self.link_type = 'ARTICLE'
                self.link_sub_type = link_type
            elif (link_type in self.data) :
                self.link_type = 'DATA'
                self.link_sub_type = link_type
            else:
                self.link_type = '?'
                self.link_sub_type = '?'


    def __process_request_on_the_fly_links(self):
        """
        for these link types, we only need to format the deterministic link and return it
        """
        linkURL = self.on_the_fly[self.link_type].format(baseurl=self.baseurl, bibcode=self.bibcode)
        return self.return_response_single_url(linkURL)


    def __get_url_basename(self, url):
        slashparts = url.split('/')
        # Now join back the first three sections 'http:', '' and 'example.com'
        return '/'.join(slashparts[:3]) + '/'


    def __return_response_error(self, response, status):
        self.logger.info('sending response status={status}'.format(status=status))
        self.logger.debug('sending response text={response}'.format(response=response))

        r = Response(response=response, status=status)
        r.headers['content-type'] = 'text/plain; charset=UTF-8'
        return r


    def __return_response(self, response, content_type):
        self.logger.info('sending response status={status}'.format(status=200))
        self.logger.debug('sending response text={response}'.format(response=response))

        r = Response(response=response, status=200)
        r.headers['content-type'] = content_type
        return r


    def return_response_single_url(self, url):
        response = self.config['RESOLVER_GATEWAY_URL_TEST'].format(bibcode=self.bibcode, link_type=self.link_type, url=url)
        return self.__return_response(response, 'text/plain; charset=UTF-8')


    def __return_response_JSON(self, response):
        return self.__return_response(response, 'application/json')


    def response_single_url(self, results):
        """
        for link types = INSPIRE or  LIBRARYCATALOG or PRESENTATION return a url

        :param result: result from the query
        """
        if (len(results) == 1):
            return self.return_response_single_url(results[0].get_url())
        return self.__return_response_error("error: did not find any records for bibcode:'{bibcode}' with "
                                          "link type: '{link_type}' and link sub type: '{link_sub_type}'!"
                                          .format(bibcode=self.bibcode, link_type=self.link_type,
                                                  link_sub_type=self.link_sub_type if (len(self.link_sub_type) > 0) else 'any value'), 404)


    def response_link_type_article(self, results):
        """
        for link type = article, we can have one or many urls
        if there is only one url we return it, otherwise, we return a json code

        :param results: result from the query
        """

        if (len(results) > 0):
            if (len(results) == 1):
                return self.return_response_single_url(results[0].get_url())
            else:
                links = {}
                links['count'] = len(results)
                links['bibcode'] = self.bibcode
                links['link_type'] = self.link_type
                records = []
                for result in results:
                    record = {}
                    record['title'] = result.get_url()
                    record['url'] = result.get_url()
                    records.append(record)
                links['records'] = records
                response = {}
                # when we have multiple sources of electronic journal, there is no url to log
                response['service'] = ''
                response['action'] = 'display'
                response['links'] = links
                return self.__return_response_JSON(json.dumps(response))
        return self.__return_response_error("error: did not find any records for bibcode:'{bibcode}' with "
                                          "link type: '{link_type}' and link sub type: '{link_sub_type}'!"
                                          .format(bibcode=self.bibcode, link_type=self.link_type,
                                                  link_sub_type=self.link_sub_type if (len(self.link_sub_type) > 0) else 'any value'), 404)


    def response_link_type_associated(self, results, redirect_format_str):
        """
        for link type = associated, we return a JSON code

        :param results: result from the query
        :param redirect_format_str:
        """
        if (len(results) > 0):
            link_format_str = self.on_the_fly['ABSTRACT']
            for result in results:
                links = {}
                links['count'] = result.get_count()
                links['link_type'] = self.link_type
                records = []
                for idx in range(result.get_count()):
                    bibcode = result.get_url_elem(idx)
                    encodeURL = quote(link_format_str.format(baseurl=self.baseurl, bibcode=bibcode), safe='')
                    redirectURL = redirect_format_str.format(bibcode=bibcode, link_type=self.link_type.lower(),
                                                             url=encodeURL)
                    record = {}
                    record['bibcode'] = bibcode
                    record['title'] = result.get_title_elem(idx)
                    record['url'] = redirectURL
                    records.append(record)
                records = sorted(records, key=lambda k: k['title'])
            links['records'] = records
            response = {}
            response['service'] = '{baseurl}/{bibcode}/associated'.format(baseurl=self.baseurl, bibcode=self.bibcode)
            response['action'] = 'display'
            response['links'] = links
            return self.__return_response_JSON(json.dumps(response))
        return self.__return_response_error("error: did not find any records for bibcode:'{bibcode}' with link type: '{link_type}'!"
                                          .format(bibcode=self.bibcode, link_type=self.link_type), 404)


    def response_link_type_data(self, results, redirect_format_str):
        """
        for link type = data, we can have one or many urls
        if there is only one url we return it, otherwise, we return a json code

        :param results: result from the query
        :param redirect_format_str:
        """
        if (len(results) > 0):
            if (len(results) == 1):
                return self.return_response_single_url(results[0].get_url())
            else:
                domain = {}
                records = []
                url = ''
                data = []
                for result in results:
                    for idx in range(result.get_count()):
                        if (url != result.get_url_elem(idx)):
                            if (domain):
                                domain['data'] = data
                                records.append(domain)
                                data = []
                            url = result.get_url_elem(idx)
                            domain = {}
                            baseName = self.__get_url_basename(url)
                            domain['title'] = 'Resource at ' + baseName
                            domain['url'] = baseName
                        encodeURL = quote(result.get_url_elem(idx), safe='')
                        redirectURL = redirect_format_str.format(bibcode=self.bibcode, link_type=self.link_type.lower(), url=encodeURL)
                        record = {}
                        record['title'] = result.get_title_elem(idx) if result.get_title_elem(idx) else result.get_url_elem(idx)
                        record['url'] = redirectURL
                        data.append(record)
                domain['data'] = data
                records.append(domain)
                links = {}
                links['count'] = len(results)
                links['bibcode'] = self.bibcode
                links['records'] = records
                response = {}
                # when we have multiple sources of links elements there is no url to log
                response['service'] = ''
                response['action'] = 'display'
                response['links'] = links
                return self.__return_response_JSON(json.dumps(response))
        return self.__return_response_error("error: did not find any records for bibcode:'{bibcode}' with "
                                          "link type: '{link_type}' and link sub type: '{link_sub_type}'!"
                                          .format(bibcode=self.bibcode, link_type=self.link_type,
                                                  link_sub_type=self.link_sub_type if (len(self.link_sub_type) > 0) else 'any value'), 404)


    def process_request(self):
        """

        :return:
        """
        self.logger.info('received request with bibcode={bibcode} and link_type={link_type}'.format(
                bibcode=self.bibcode,
                link_type=self.link_type))

        if (len(self.bibcode) == 0) or (len(self.link_type) == 0):
            return self.__return_response_error('error: not all the needed information received', 400)

        # for these link types, we only need to format the deterministic link and return it
        if (self.link_type in self.on_the_fly.keys()):
            return self.__process_request_on_the_fly_links()

        # the rest of the link types query the db

        # for the following link types the return value is a url
        if (self.link_type == 'INSPIRE') or (self.link_type == 'LIBRARYCATALOG') or (self.link_type == 'PRESENTATION'):
            return self.response_single_url(get_records(bibcode=self.bibcode, link_type=self.link_type))

        # for the following link type the return value is a JSON code
        if (self.link_type == 'ASSOCIATED'):
            return self.response_link_type_associated(get_records(bibcode=self.bibcode, link_type=self.link_type),
                                                      self.config['RESOLVER_GATEWAY_URL'])

        # for BBB we have defined more specifically the source of full text resources and
        # have divided them into 7 sub types, defined in Solr field esource
        if (self.link_type == 'ARTICLE'):
            return self.response_link_type_article(get_records(bibcode=self.bibcode, link_type=self.link_type, link_sub_type=self.link_sub_type))

        # for BBB we have defined more specifically the type of data and
        # have divided them into 30+ sub types, defined in Solr field data
        if (self.link_type == 'DATA'):
            return self.response_link_type_data(get_records(bibcode=self.bibcode, link_type=self.link_type, link_sub_type=self.link_sub_type),
                                                self.config['RESOLVER_GATEWAY_URL'])

        # we did not recognize the link_type, so return an error
        return self.__return_response_error("error: unrecognizable link type:'{link_type}'!".format(link_type=self.link_type), 400)



@advertise(scopes=[], rate_limit=[1000, 3600 * 24])
@bp.route('/v1/resolver/<bibcode>/<link_type>', methods=['GET'])
def resolver(bibcode, link_type):
    """

    :param bibcode:
    :param link_type: 
    :return:
    """
    return LinkRequest(bibcode, link_type.upper()).process_request()
