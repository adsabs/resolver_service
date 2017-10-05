#!/usr/bin/python
# -*- coding: utf-8 -*-

import json

from flask import Response
from flask import current_app
from requests.utils import quote

from linksData import *
from adsputils import load_config, setup_logging

logger = None
config = {}

class LinkRequest():

    # we have 8 link types that are created on the fly and do not need to go to db
    # as of now, 8/27/2017, we are to eliminate the COMMENTS and CUSTOM links
    onTheFly = {
        'ABSTRACT' : 'https://ui.adsabs.harvard.edu/#abs/{bibcode}/abstract',
        'CITATIONS': 'https://ui.adsabs.harvard.edu/#abs/{bibcode}/citations',
        'REFERENCES': 'https://ui.adsabs.harvard.edu/#abs/{bibcode}/references',
        'COREADS': 'https://ui.adsabs.harvard.edu/#abs/{bibcode}/coreads',
        #'COMMENTS': '???',
        'TOC': 'http://ui.adsabs.harvard.edu/#abs/{bibcode}/toc',
        'OPENURL': 'http://ui.adsabs.harvard.edu/#abs/{bibcode}/openurl',
        #'CUSTOM': '???'
    }

    # electronic journal sub types
    eSource = [
        'PUB_PDF', 'EPRINT_PDF', 'AUTHOR_PDF', 'ADS_PDF',
        'PUB_HTML', 'EPRINT_HTML', 'AUTHOR_HTML', 'ADS_SCAN'
    ]

    # data sub types
    data =  [
        'ARI', 'SIMBAD', 'NED', 'CDS', 'Vizier', 'GCPD', 'Author', 'PDG', 'MAST', 'HEASARC', 'INES', 'IBVS', 'Astroverse',
        'ESA', 'NExScI', 'PDS', 'AcA', 'ISO', 'ESO', 'CXO', 'NOAO', 'XMM', 'Spitzer', 'PASA', 'ATNF', 'KOA', 'Herschel',
        'GTC', 'BICEP2', 'ALMA', 'CADC', 'Zenodo', 'TNS', ''
    ]

    linkTypes = onTheFly.keys() + ['ARTICLE', 'DATA', 'INSPIRE', 'LIBRARYCATALOG', 'PRESENTATION', 'ASSOCIATED']

    bibcode = ''
    linkType = ''
    linkSubType = ''
    referreredURL = ''

    logger = None
    config = {}

    def __init__(self, bibcode, linkType, referreredURL=''):
        self.config.update(load_config())
        self.logger = setup_logging('resolver_service', config.get('LOG_LEVEL', 'INFO'))

        self.bibcode = bibcode
        self.__setMajorMinorLinkTypes(linkType)
        self.referreredURL = referreredURL
        self.__backwardCompatibility(linkType)


    def __backwardCompatibility(self, linkType):
        # GIF, EJOURNAL, and PREPRINT are classics' types
        # for backward compatibility we are recognizing them
        if (linkType == 'GIF'):
            self.linkType = 'ARTICLE'
            self.linkSubType = 'ADS_SCAN'
        elif (linkType == 'PREPRINT'):
            self.linkType = 'ARTICLE'
            self.linkSubType = 'EPRINT_HTML'
        elif (linkType == 'EJOURNAL'):
            self.linkType = 'ARTICLE'
            self.linkSubType = 'PUB_HTML'


    def __setMajorMinorLinkTypes(self, linkType):
        # figure out what are the linkType and subLinkType
        # from one input param
        if (linkType in self.linkTypes):
            self.linkType = linkType
            self.linkSubType = ''
        else:
            # we have two sets of sub link type, figure out which one it is
            if (linkType in self.eSource):
                self.linkType = 'ARTICLE'
                self.linkSubType = linkType
            elif (linkType in self.data) :
                self.linkType = 'DATA'
                self.linkSubType = linkType
            else:
                self.linkType = '?'
                self.linkSubType = '?'


    def __returnResponseError(self, response, status):
        self.logger.info('sending response status={status}'.format(status=status))
        self.logger.debug('sending response text={response}'.format(response=response))

        r = Response(response=response, status=status)
        r.headers['content-type'] = 'text/html; charset=UTF-8'
        return r


    def __returnResponse(self, contentType, response):
        self.logger.info('sending response status={status}'.format(status=200 if (len(response) > 0) else 404))
        self.logger.debug('sending response text={response}'.format(response=response))

        if (len(response) != 0):
            r = Response(response=response, status=200)
            r.headers['content-type'] = contentType
            return r
        r = Response(response='', status=404)
        r.headers['content-type'] = contentType
        return r


    # for these link types, we only need to format the deterministic link and return it
    def __processRequestOnTheFlyLinks(self):
        linkURL = self.onTheFly[self.linkType].format(bibcode=self.bibcode)
        return self.__returnResponse('text/html; charset=UTF-8', linkURL)

    # for link type = article, we can have one or many urls
    # if there is only one url we return it, otherwise, we return a json code
    def returnResponseLinkTypeArticle(self, result):
        if (len(result) > 0):
            if (len(result) == 1):
                return self.__returnResponse('text/html; charset=UTF-8', result[0])
            else:
                links = {}
                links['count'] = len(result)
                links['bibcode'] = self.bibcode
                links['linkType'] = self.linkType
                records = []
                for url in result:
                    record = {}
                    record['title'] = url
                    record['url'] = url
                    records.append(record)
                links['records'] = records
                response = {}
                # when we have multiple sources of electronic journal, there is no url to log
                response['service'] = ''
                response['action'] = 'display'
                response['links'] = links
                return self.__returnResponse('application/json', json.dumps(response))
        return self.__returnResponseError("error: did not find any records for bibcode:'{bibcode}' with "
                                          "link type: '{link_type}' and link sub type: '{link_sub_type}'!"
                                          .format(bibcode=self.bibcode, link_type=self.linkType,
                                                  link_sub_type=self.linkSubType if (len(self.linkSubType) > 0) else 'any value'), 404)


    # for link type = associated, we return a JSON code
    def returnResponseLinkTypeAssociated(self, result, redirectFormatStr):

        if (len(result) > 0):
            links = {}
            links['count'] = len(result)
            links['linkType'] = self.linkType
            records = []
            linkFormatStr = self.onTheFly['ABSTRACT']
            for row in result:
                encodeURL = quote(linkFormatStr.format(bibcode=row[0]), safe='')
                redirectURL = redirectFormatStr.format(bibcode=row[0], linkType=self.linkType.lower(), URL=encodeURL)
                record = {}
                record['bibcode'] = row[0]
                record['title'] = row[1]
                record['url'] = redirectURL
                records.append(record)
            records = sorted(records, key=lambda k: k['title'])
            links['records'] = records
            response = {}
            response['service'] = 'https://ui.adsabs.harvard.edu/#abs/{}/associated'.format(self.bibcode)
            response['action'] = 'display'
            response['links'] = links
            return self.__returnResponse('application/json', json.dumps(response))
        return self.__returnResponseError("error: did not find any records for bibcode:'{bibcode}' with link type: '{link_type}'!"
                                          .format(bibcode=self.bibcode, link_type=self.linkType), 404)


    def __getURLBaseName(self, URL):
        slashparts = URL.split('/')
        # Now join back the first three sections 'http:', '' and 'example.com'
        return '/'.join(slashparts[:3]) + '/'

    # for link type = data, we can have one or many urls
    # if there is only one url we return it, otherwise, we return a json code
    def returnResponseLinkTypeData(self, result, redirectFormatStr):
        if (len(result) > 0):
            if (len(result) == 1):
                return self.__returnResponse('text/html; charset=UTF-8', result[0])
            else:
                rows = zip(*result)
                url = ''
                domain = {}
                data = []
                count = 0
                records = []
                for i in range(len(result)):
                    if (url != rows[0][i]):
                        count += 1
                        if (domain):
                            domain['data'] = data
                            records.append(domain)
                            data = []
                        url = rows[0][i]
                        domain = {}
                        baseName = self.__getURLBaseName(url)
                        domain['title'] = 'Resource at ' + baseName
                        domain['url'] = baseName
                    encodeURL = quote(rows[0][i], safe='')
                    redirectURL = redirectFormatStr.format(bibcode=self.bibcode, linkType=self.linkType.lower(), URL=encodeURL)
                    record = {}
                    record['title'] = rows[1][i] if len(rows[1][i]) > 0 else rows[0][i]
                    record['url'] = redirectURL
                    data.append(record)
                domain['data'] = data
                records.append(domain)
                links = {}
                links['count'] = count
                links['bibcode'] = self.bibcode
                links['records'] = records
                response = {}
                # when we have multiple sources of links elements there is no url to log
                response['service'] = ''
                response['action'] = 'display'
                response['links'] = links
                return self.__returnResponse('application/json', json.dumps(response))
        return self.__returnResponseError("error: did not find any records for bibcode:'{bibcode}' with "
                                          "link type: '{link_type}' and link sub type: '{link_sub_type}'!"
                                          .format(bibcode=self.bibcode, link_type=self.linkType,
                                                  link_sub_type=self.linkSubType if (len(self.linkSubType) > 0) else 'any value'), 404)


    def processRequest(self):
        if (len(self.bibcode) == 0) or (len(self.linkType) == 0):
            return self.__returnResponseError('error: not all the needed information received', 400)

        # for these link types, we only need to format the deterministic link and return it
        if (self.linkType in self.onTheFly.keys()):
            return self.__processRequestOnTheFlyLinks()

        # the rest of the link types query the db

        # for the following link types the return value is a url
        if (self.linkType == 'INSPIRE') or (self.linkType == 'LIBRARYCATALOG') or (self.linkType == 'PRESENTATION'):
            return self.__returnResponse('text/html; charset=UTF-8', getURL(bibcode=self.bibcode, linkType=self.linkType))

        # for the following link type the return value is a JSON code
        if (self.linkType == 'ASSOCIATED'):
            return self.returnResponseLinkTypeAssociated(getURLandTitle(bibcode=self.bibcode, linkType=self.linkType),
                                                         current_app.config['RESOLVER_GATEWAY_URL'])

        # for BBB we have defined more specifically the source of full text resources and
        # have divided them into 7 sub types, defined in Solr field eSource
        if (self.linkType == 'ARTICLE'):
            return self.returnResponseLinkTypeArticle(getURL(bibcode=self.bibcode, linkType=self.linkType, linkSubType=self.linkSubType))

        # for BBB we have defined more specifically the type of data and
        # have divided them into 30+ sub types, defined in Solr field data
        if (self.linkType == 'DATA'):
            return self.returnResponseLinkTypeData(getURLandTitle(bibcode=self.bibcode, linkType=self.linkType, linkSubType=self.linkSubType),
                                                   current_app.config['RESOLVER_GATEWAY_URL'])

        # we did not recognize the linkType, so return an error
        return self.__returnResponseError("error: unrecognizable linkType:'{linkType}'!".format(linkType=self.linkType), 400)

