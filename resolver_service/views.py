#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import request, Blueprint
from flask import current_app
from requests.utils import quote


bp = Blueprint('resolver_service', __name__)

        
@advertise(scopes=[], rate_limit=[1000, 3600 * 24])
@bp.route('/<bibcode>/<linkType>', methods=['GET'])
def resolver(bibcode, link_type):
    current_app.logger.info('received request with bibcode={bibcode} and link_type={link_type}'.format(bibcode=bibcode, link_type=link_type))
    # this must always return JSON
    # linktype should be optional - to request everytihng we have/know about the bibcode
    return LinkRequest(bibcode, link_type.upper()).processRequest()


        
class LinkRequest():

    # we have 8 link types that are created on the fly and do not need to go to db
    # as of now, 8/27/2017, we are to eliminate the COMMENTS and CUSTOM links
    onTheFly = {
        'ABSTRACT' : '{baseurl}/#abs/{bibcode}/abstract',
        'CITATIONS': '{baseurl}/#abs/{bibcode}/citations',
        'REFERENCES': '{baseurl}/#abs/{bibcode}/references',
        'COREADS': '{baseurl}/#abs/{bibcode}/coreads',
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

    def __init__(self, bibcode, linkType):
        
        self.config = current_app.config
        self.baseurl = self.config.get('ADS_BASEURL', 'https://ui.adsabs.harvard.edu') # configurable because it may change (for debugging/sandbox)
        self.logger = current_app.logger
        self.bibcode = bibcode
        self.__setMajorMinorLinkTypes(linkType)
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




    # for these link types, we only need to format the deterministic link and return it
    def __processRequestOnTheFlyLinks(self):
        return self.onTheFly[self.linkType].format(bibcode=self.bibcode)


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
            response['service'] = '{baseurl}/#abs/{}/associated'.format(self.bibcode)
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


    def _get_url(self, data):
        """Finds the destination for the bibcode and the data we know about it."""
        pass # TODO - modify the logic
    
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
                                                         self.config['RESOLVER_GATEWAY_URL'])

        # for BBB we have defined more specifically the source of full text resources and
        # have divided them into 7 sub types, defined in Solr field eSource
        if (self.linkType == 'ARTICLE'):
            return self.returnResponseLinkTypeArticle(getURL(bibcode=self.bibcode, linkType=self.linkType, linkSubType=self.linkSubType))

        # for BBB we have defined more specifically the type of data and
        # have divided them into 30+ sub types, defined in Solr field data
        if (self.linkType == 'DATA'):
            return self.returnResponseLinkTypeData(getURLandTitle(bibcode=self.bibcode, linkType=self.linkType, linkSubType=self.linkSubType),
                                                   self.config['RESOLVER_GATEWAY_URL'])


    
    def processRequest(self):
        
        # the logic should be as follows:
        
        # load information about the bibcode/subtype combination
            # return 404 if no record exists
            # return 404 if no record&subtype exists
        
        # format all links
        
        # return JSON with 200 status
        
        try:
            data = self._load_record()
        except BibcodeNotFound, e:
            return 404, {"msg": 'Bibcode {bibcode} cannot be resolved (not exists)'.format(bibcode=self.bibcode)}
        except SutypeNotFound, e:
            return 404, {"msg": 'Bibcode {bibcode} found, but the {link_type} cannot be resolved'.format(
                                                           bibcode=self.bibcode, link_type=self.link_type)}
        
        out = {'bibcode': self.bibcode, 'links': []}
        pointer = out['links']
        
        for row in data:
            row['url'] = self._get_url(row)
            pointer.append(row)
            
        return 200, out
        