# -*- coding: utf-8 -*-

from builtins import str
from builtins import range
import json
import urllib.parse
import re

from flask import current_app, request, Blueprint
from flask_discoverer import advertise
from flask import Response
from requests.utils import quote

# keep these two lines until adsmsg is fixed 3/30/2021
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
from adsmsg import DataLinksRecordList
from google.protobuf.json_format import Parse, ParseError

from resolversrv.utils import get_records, add_records, del_records


bp = Blueprint('resolver_service', __name__)

class LinkRequest(object):

    re_bibcode = re.compile(r"^([12]\d\d\d[A-Za-z\.&]{5}[A-Za-z0-9\.]{9}[A-Z])$")

    def __init__(self, bibcode, link_type='', id=None):
        """

        :param bibcode:
        :param link_type: this can be either link_type or link_sub_type
        :param gateway_redirect_url: for link types that have more than one link, we create this link so that
                                    when user clicks on it, it would go to the gateway so that the click can be logged
        :return:
        """
        self.__init_default()
        self.bibcode = bibcode
        self.__set_major_minor_link_types(link_type)
        self.__backward_compatibility(link_type)
        self.gateway_redirect_url = current_app.config['RESOLVER_GATEWAY_URL']
        self.id = id


    def __init_default(self):
        """

        :return:
        """
        self.baseurl = current_app.config['RESOLVER_DETERMINISTIC_LINKS_BASEURL']

        # we have 8 link types that are created on the fly and do not need to go to db
        # as of now, 8/27/2017, we are to eliminate the COMMENTS and CUSTOM links
        self.on_the_fly = {
            'ABSTRACT': '{baseurl}/{bibcode}/abstract',
            'CITATIONS': '{baseurl}/{bibcode}/citations',
            'REFERENCES': '{baseurl}/{bibcode}/references',
            'COREADS': '{baseurl}/{bibcode}/coreads',
            # 'COMMENTS': '???',
            'TOC': '{baseurl}/{bibcode}/toc',
            'OPENURL': '{baseurl}/{bibcode}/openurl',
            # 'CUSTOM': '???',
            'GRAPHICS':  '{baseurl}/{bibcode}/graphics',
            'METRICS': '{baseurl}/{bibcode}/metrics',
            'SIMILAR': '{baseurl}/{bibcode}/similar',
        }

        # electronic journal sub types
        self.esource = [
            'PUB_PDF', 'EPRINT_PDF', 'AUTHOR_PDF', 'ADS_PDF',
            'PUB_HTML', 'EPRINT_HTML', 'AUTHOR_HTML', 'ADS_SCAN'
        ]

        # data sub types
        # case discrepancy for some of the types, hence a dict, to get a match from db
        self.data = current_app.config['RESOLVER_DATA_TYPES']

        # identification link type
        self.identification = {
            'DOI': current_app.config['RESOLVER_DOI_LINK_BASEURL'],
            'ARXIV': current_app.config['RESOLVER_ARXIV_LINK_BASEURL'],
        }
        
        self.link_types = list(self.on_the_fly.keys()) + ['ESOURCE', 'DATA', 'INSPIRE', 'LIBRARYCATALOG', 'PRESENTATION', 'ASSOCIATED'] + list(self.identification.keys())


    def __backward_compatibility(self, link_type):
        """
        GIF, EJOURNAL, and PREPRINT are classics' types
        for backward compatibility we are recognizing them

        :param link_type:
        :return:
        """
        if (link_type == 'GIF'):
            self.link_type = 'ESOURCE'
            self.link_sub_type = 'ADS_SCAN'
        elif (link_type == 'PREPRINT'):
            self.link_type = 'ESOURCE'
            self.link_sub_type = 'EPRINT_HTML'
        elif (link_type == 'EJOURNAL'):
            self.link_type = 'ESOURCE'
            self.link_sub_type = 'PUB_HTML'
        elif (link_type == 'ARTICLE'):
            self.link_type = 'ESOURCE'
            self.link_sub_type = '%_PDF'


    def __set_major_minor_link_types(self, link_type):
        """
        figure out what are the link type and sub link type
        from one input param

        :param link_type:
        :return:
        """
        # if link_type has been specified
        if (link_type in self.link_types):
            self.link_type = link_type
            self.link_sub_type = None
        # see if link_sub_type has been passed in,
        # we have two sets of link sub types, so figure out which one, if any, it belongs to
        elif (link_type in self.esource):
            self.link_type = 'ESOURCE'
            self.link_sub_type = link_type
        elif (link_type.upper() in list(self.data.keys())):
            self.link_type = 'DATA'
            self.link_sub_type = self.data[link_type.upper()]
        elif ('|' in link_type):
            # init to unknown, then if found valid types, reset it
            self.link_type = '?'
            self.link_sub_type = '?'
            parts = link_type.split('|')
            if len(parts) == 2:
                if (parts[0] == 'ESOURCE' and parts[1] in self.esource) or \
                   (parts[0] == 'DATA' and parts[1] in list(self.data.keys())):
                    self.link_type = parts[0]
                    self.link_sub_type = parts[1]
        # if link_type is empty treated as we are having only a bibcode and shall return all records for
        # for the bibcode
        elif len(link_type) == 0:
            self.link_type = None
            self.link_sub_type = None
        # but if non empty and we could not resolve the type then it is error
        else:
            self.link_type = '?'
            self.link_sub_type = '?'


    def __get_url_hostname_with_protocol(self, url):
        """
        
        :param url:
        :return: the hostname from the url, it includes protocol
        """
        slashparts = url.split('/')
        # Now join back the first three sections 'http:', '' and 'example.com'
        return '/'.join(slashparts[:3]) + '/'


    def __get_url_hostname(self, url):
        """

        :param url:
        :return: the hostname only, which is used to update some of the urls from db
        """
        return self.__get_url_hostname_with_protocol(url).split('://', 1)[-1].rstrip('/')


    def __get_data_source_title_url(self, link_sub_type, default_url):
        """
        for link type DATA we include the source url and title first and under it list the resources for requested bibcode
        this would get the list from config and returns the info if found, otherwise builds a generic title

        :param link_sub_type:
        :param default_url:
        :return:
        """
        data_resources = current_app.config['RESOLVER_DATA_SOURCES']
        if link_sub_type in data_resources:
            title = data_resources[link_sub_type].get('name', 'Resource at ' + default_url)
            url = data_resources[link_sub_type].get('url', default_url)
        else:
            title = 'Resource at ' + default_url
            url = default_url
        return [title,url]


    def __update_data_type_hostname(self, data_source_url, link_sub_type, link_url):
        """
        update link_url with hostname from data source url for particular links sub types

        :param data_source_url: data source url for the link sub type
        :param link_sub_type:
        :param link_url:
        :return:
        """
        if (link_sub_type == 'NED') or (link_sub_type == 'SIMBAD'):
            return link_url.replace('${}$'.format(link_sub_type), self.__get_url_hostname(data_source_url))
        if (link_sub_type == 'Vizier') or (link_sub_type == 'CDS'):
            _, url = self.__get_data_source_title_url(link_sub_type='Vizier', default_url='')
            return link_url.replace('$VIZIER$', self.__get_url_hostname(url))
        return link_url


    def __get_associated_redirect_url(self, url):
        """
        
        :param url: 
        :return: 
        """
        link_format_str = self.on_the_fly['ABSTRACT']
        if self.re_bibcode.match(url):
            bibcode = url
            encodeURL = ':' + quote(link_format_str.format(baseurl=self.baseurl, bibcode=bibcode), safe='')
            redirectURL = self.gateway_redirect_url.format(bibcode=self.bibcode, link_type=self.link_type.lower(), url=encodeURL)
        else:
            # this is an outside link, so display it as is
            bibcode = self.bibcode
            encodeURL = ':' + quote(url, safe='')
            redirectURL = self.gateway_redirect_url.format(bibcode=self.bibcode, link_type=self.link_type.lower(), url=encodeURL)

        return bibcode, redirectURL

    def __return_response(self, results, status):
        """
        
        :param results: results in a dict
        :param status: status code
        :return: 
        """
        response = json.dumps(results)

        current_app.logger.info('sending response status=%s' % (status))
        current_app.logger.info('sending response text=%s' % (response))

        r = Response(response=response, status=status)
        r.headers['content-type'] = 'application/json'
        return r


    def __get_link_type_count(self, link_type):
        """

        :param link_type:
        :return:
        """
        # on the fly links or identification links are only 1
        if (link_type != 'TOC' and link_type in list(self.on_the_fly.keys())) or link_type in list(self.identification.keys()):
            return 1
        # query db
        results = get_records(bibcode=self.bibcode, link_type=link_type)
        if (results is None):
            return 0
        if link_type == 'DATA':
            count = 0
            for result in results:
                count += result['itemCount']
            return count
        if link_type in ['ESOURCE', 'ASSOCIATED']:
            count = 0
            for result in results:
                count += len(result['url'])
            return count
        count = 0
        for result in results:
            # get the maximum of
            count += max(1, result['itemCount'] if 'itemCount' in result else 0)
        return count


    def request_link_type_deterministic_single_url_toJSON(self, url):
        """
        single url to JSON code transformation

        :param url:
        :return:
        """
        if (len(url) > 0):
            response = {}
            response['service'] = url
            response['action'] = 'redirect'
            response['link'] = url
            response['link_type'] = self.link_type + ('' if self.link_sub_type == None else '|' + self.link_sub_type)
            return self.__return_response(response, 200)
        return self.__return_response({'error': 'did not find any records'}, 404)


    def request_link_type_single_url(self, results):
        """
        for link types = INSPIRE or  LIBRARYCATALOG or PRESENTATION we have a single url
        which shall be wrapped in a JSON code before returning

        :param results: result from the query
        :return:
        """
        if (results is None):
            return self.__return_response({'error': 'did not find any records'}, 404)

        try:
            return self.request_link_type_deterministic_single_url_toJSON(results[0]['url'][0])
        except (KeyError, IndexError):
            error_message = 'requested information for bibcode=%s and link_type=%s is missing' % (self.bibcode, self.link_type)
            return self.__return_response({'error': error_message}, 400)


    def request_link_type_identification_single_url_toJSON(self, url):
        """
        single url to JSON code transformation

        :param url:
        :return:
        """
        if (len(url) > 0):
            response = {}
            response['service'] = url
            response['action'] = 'redirect'
            response['link'] = url
            response['link_type'] = self.link_type + ('' if self.link_sub_type == None else '|' + self.link_sub_type)
            return self.__return_response(response, 200)
        return self.__return_response({'error': 'did not find any records'}, 404)



    def request_link_type_all(self):
        """
        
        :return: all the link types for the requested bibcode
        """
        links = {}
        links['count'] = len(self.link_types)
        links['link_type'] = 'all'
        records = []
        for link_type in self.link_types:
            bibcode = self.bibcode
            redirectURL = self.gateway_redirect_url.format(bibcode=bibcode, link_type=link_type, url='')
            redirectURL = redirectURL[:-1]
            record = {}
            count = self.__get_link_type_count(link_type)
            if count > 0:
                record['bibcode'] = bibcode
                record['title'] = link_type + ' (' + str(count) + ')'
                record['url'] = redirectURL
                record['type'] = link_type.lower()
                record['count'] = count
                records.append(record)
        links['records'] = records
        response = {}
        # when we have multiple sources of links elements there is no url to log (no service)
        response['service'] = ''
        response['action'] = 'display'
        response['links'] = links
        return self.__return_response(response, 200)


    def request_link_type_on_the_fly(self):
        """
        for these link types, we only need to format the deterministic link and return it

        :return:
        """
        # as of 3/27/2019 we should have bibcodes with TOC in db, so check to see if for this bibcode
        # there is an entry, and return accordingly
        if self.link_type == 'TOC':
            results = get_records(bibcode=self.bibcode, link_type=self.link_type)
            if (results is None):
                return self.__return_response({'error': 'did not find any records'}, 404)
        url = self.on_the_fly[self.link_type].format(baseurl=self.baseurl, bibcode=self.bibcode)
        return self.request_link_type_deterministic_single_url_toJSON(url)


    def request_link_type_esource(self, results):
        """
        for link type = article, we can have one or many urls

        :param results: result from the query
        :return:
        """
        try:
            if (results is not None):
                # we have all the esources of type PDF
                if self.link_sub_type == '%_PDF':
                    # check in the following order for any _PDF esources
                    for esource in ['ADS_PDF', 'PUB_PDF', 'AUTHOR_PDF', 'EPRINT_PDF']:
                        for result in results:
                            if (result['link_sub_type'] == esource) and (len(result['url']) == 1):
                                self.link_sub_type = esource
                                return self.request_link_type_deterministic_single_url_toJSON(result['url'][0])
                    return self.__return_response({'error': 'did not find any records'}, 404)

                if (len(results) == 1):
                    result = results[0]
                    if (len(result['url']) == 1):
                        return self.request_link_type_deterministic_single_url_toJSON(result['url'][0])

                # we could go here if the length is 1, but there are multiple urls here
                if (len(results) >= 1):
                    links = {}
                    links['count'] = len(results)
                    links['bibcode'] = self.bibcode
                    links['link_type'] = self.link_type
                    records = []
                    for result in results:
                        for idx in range(len(result['url'])):
                            record = {}
                            record['title'] = result['url'][idx]
                            record['url'] = result['url'][idx]
                            record['link_type'] = '%s|%s'%(self.link_type, result['link_sub_type'])
                            records.append(record)
                    if len(records) > 0:
                        links['records'] = records
                        response = {}
                        # when we have multiple sources of electronic journal, there is no url to log (no service)
                        response['service'] = ''
                        response['action'] = 'display'
                        response['links'] = links
                        return self.__return_response(response, 200)
            return self.__return_response({'error': 'did not find any records'}, 404)
        except (KeyError, IndexError):
            error_message = 'requested information for bibcode=%s and link_type=%s is missing' % (
            self.bibcode, self.link_type)
            return self.__return_response({'error': error_message}, 400)

    def request_link_type_associated(self, results):
        """
        for link type = associated

        :param results: result from the query
        :return:
        """
        try:
            if (results is not None):
                for result in results:
                    links = {}
                    links['count'] = len(result['url'])
                    links['link_type'] = self.link_type
                    records = []
                    for idx in range(len(result['url'])):
                        bibcode, redirectURL = self.__get_associated_redirect_url(result['url'][idx])
                        record = {}
                        record['bibcode'] = bibcode
                        record['title'] = result['title'][idx]
                        record['url'] = redirectURL
                        records.append(record)
                    records = sorted(records, key=lambda k: k['title'])
                links['records'] = records
                response = {}
                response['service'] = '{baseurl}/{bibcode}/associated'.format(baseurl=self.baseurl, bibcode=self.bibcode)
                response['action'] = 'display'
                response['links'] = links
                return self.__return_response(response, 200)
            return self.__return_response({'error': 'did not find any records'}, 404)
        except (KeyError, IndexError):
            error_message = 'requested information for bibcode=%s and link_type=%s is missing' %(self.bibcode, self.link_type)
            return self.__return_response({'error': error_message}, 400)


    def request_link_type_data(self, results):
        """
        for link type = data, we can have one or many urls

        :param results: result from the query
        """
        try:
            if (results is not None):
                if (len(results) == 1):
                    result = results[0]
                    if (len(result['url']) == 1):
                        title, url = self.__get_data_source_title_url(result['link_sub_type'],
                                                                      self.__get_url_hostname_with_protocol(result['url'][0]))
                        revised_url = self.__update_data_type_hostname(url, result['link_sub_type'], result['url'][0])
                        return self.request_link_type_deterministic_single_url_toJSON(revised_url)
                # we could go here if the length is 1, but there are multiple urls here
                if (len(results) >= 1):
                    domain = {}
                    records = []
                    url = ''
                    data = []
                    for result in results:
                        for idx in range(len(result['url'])):
                            if (url != result['url'][idx]):
                                if (domain):
                                    domain['data'] = data
                                    records.append(domain)
                                    data = []
                                url = result['url'][idx]
                                domain = {}
                                domain_title,domain_url = self.__get_data_source_title_url(result['link_sub_type'],
                                                                                           self.__get_url_hostname_with_protocol(url))
                                domain['title'] = domain_title
                                domain['url'] = domain_url
                            complete_link_type = '%s|%s'%(self.link_type, result['link_sub_type'])
                            complete_url = self.__update_data_type_hostname(domain_url, result['link_sub_type'], result['url'][idx])
                            encodeURL = quote(complete_url, safe='')
                            redirectURL = self.gateway_redirect_url.format(bibcode=self.bibcode, link_type=complete_link_type, url=encodeURL)
                            record = {}
                            record['title'] = result['title'][idx] if result['title'][idx] else complete_url
                            record['url'] = redirectURL
                            record['link_type'] = complete_link_type
                            data.append(record)
                    if len(data) > 0:
                        domain['data'] = data
                        records.append(domain)
                        links = {}
                        links['count'] = len(results)
                        links['bibcode'] = self.bibcode
                        links['records'] = records
                        response = {}
                        # when we have multiple sources of links elements there is no url to log (no service)
                        response['service'] = ''
                        response['action'] = 'display'
                        response['links'] = links
                        return self.__return_response(response, 200)
            return self.__return_response({'error': 'did not find any records'}, 404)
        except (KeyError, IndexError):
            error_message = 'requested information for bibcode=%s and link_type=%s is missing' % (self.bibcode, self.link_type)
            return self.__return_response({'error': error_message}, 400)


    def request_link_type_identification(self):
        """
        for these link types, we only need to format the deterministic link, attach the id to it, and return it

        :return:
        """
        url = self.identification[self.link_type].format(id=self.id)
        return self.request_link_type_identification_single_url_toJSON(url)


    def process_request(self):
        """
        process the request

        :return: json code of the result or error
        """
        current_app.logger.info('received request with bibcode=%s, link_type=%s and link_sub_type=%s' %
                                (self.bibcode,
                                 self.link_type if self.link_type is not None else '*',
                                 self.link_sub_type if self.link_sub_type is not None else '*'))

        if (len(self.bibcode) == 0):
            return self.__return_response({'error': 'no bibcode received'}, 400)

        # return all the link types
        if self.link_type is None:
            return self.request_link_type_all()

        # for these link types, we only need to format the deterministic link and return it
        if (self.link_type in list(self.on_the_fly.keys())):
            return self.request_link_type_on_the_fly()

        # the rest of the link types query the db

        # for the following link types we have a single url, and shall be wrapped in a JSON code as well
        if (self.link_type == 'INSPIRE') or (self.link_type == 'LIBRARYCATALOG') or (self.link_type == 'PRESENTATION'):
            return self.request_link_type_single_url(get_records(bibcode=self.bibcode, link_type=self.link_type))

        # for the following link type the return value is specific to the type
        if (self.link_type == 'ASSOCIATED'):
            return self.request_link_type_associated(get_records(bibcode=self.bibcode, link_type=self.link_type))

        # for BBB we have defined more specifically the source of full text resources and
        # have divided them into 7 sub types, defined in Solr field esource
        if (self.link_type == 'ESOURCE'):
            return self.request_link_type_esource(get_records(bibcode=self.bibcode, link_type=self.link_type, link_sub_type=self.link_sub_type))

        # for BBB we have defined more specifically the type of data and
        # have divided them into 30+ sub types, defined in Solr field data
        if (self.link_type == 'DATA'):
            return self.request_link_type_data(get_records(bibcode=self.bibcode, link_type=self.link_type, link_sub_type=self.link_sub_type))

        # for these link types, we only need to format the deterministic link, attach the id to it, and return it
        if (self.link_type in list(self.identification.keys())):
            return self.request_link_type_identification()

        # we did not recognize the link_type, so return an error
        return self.__return_response({'error': 'unrecognizable link type:`{link_type}`'.format(link_type=self.link_type)}, 400)


    def check(self):
        """
        verify that link_type is valid

        :return:
        """
        if self.link_type is not None and self.link_type != '?':
            return self.__return_response({'status': 'OK'}, 200)
        return self.__return_response({'error': 'unrecognizable link_type'}, 400)


    def verify_url_not_in_db(self, domain):
        """
        there are urls that the domain is not in database, we have placeholder for the domain in db,
        ie, $SIMBAD$, then look them, and use the provider's domain, replace the placeholder with that
        so check to see if we have one of those, and compare with provider's domain name

        :param domain:
        :return:
        """
        data_resources = current_app.config['RESOLVER_DATA_SOURCES']
        for name, info in data_resources.items():
            if name in ["SIMBAD", "NED", "Vizier", "CDS"]:
                if info["url"].split('://', 1)[-1] == domain:
                    return True
        return False


    def verify_url(self, url):
        """
        verify that url is in db

        :param bibcode:
        :param url:
        :return:
        """
        parsed_url = urllib.parse.urlparse(url)
        if (self.verify_url_not_in_db(parsed_url.netloc)):
            return self.__return_response({'link': 'verified'}, 200)
        results = get_records(bibcode=self.bibcode)
        for result in results:
            for a_url in result['url']:
                parsed_url_db = urllib.parse.urlparse(a_url)
                if parsed_url.netloc == parsed_url_db.netloc:
                    return self.__return_response({'link': 'verified'}, 200)
        return self.__return_response({'link': 'not found'}, 200)



class PopulateRequest(object):
    def __init__(self):
        """
        """
        pass

    def __return_response(self, results, status):
        """

        :param results: results in a dict
        :param status: status code
        :return:
        """
        response = json.dumps(results)

        current_app.logger.info('sending response status=%s' % (status))
        current_app.logger.info('sending response text=%s' % (response))

        r = Response(response=response, status=status)
        r.headers['content-type'] = 'application/json'
        return r


    def process_request(self, records):
        """
        process the request

        :param records:
        :return: json code of the result or error
        """
        if not records:
            return self.__return_response({'error': 'no data received'}, 400)

        if len(records) == 0:
            return self.__return_response({'error': 'no records received'}, 400)

        if len(records) > current_app.config['RESOLVER_MAX_RECORDS_ADD']:
            return self.__return_response({'error': 'too many records to add to db at one time, received %s records while the limit is %s'%(len(records), current_app.config['RESOLVER_MAX_RECORDS_ADD'])}, 400)

        current_app.logger.info('received request to populate db with %d records' % (len(records)))

        try:
            data = Parse(json.dumps({"status": 2, "datalinks_records": records}), DataLinksRecordList())
        except ParseError as e:
            return self.__return_response({'error': 'unable to extract data from protobuf structure -- %s' % (e)}, 400)

        status, text = add_records(data)
        if status == True:
            current_app.logger.info('completed request to populate db with %d records' % (len(records)))
            return self.__return_response({'status': text}, 200)
        current_app.logger.info('failed to populate db with %d records' % (len(records)))
        return self.__return_response({'error': text}, 400)

class DeleteRequest(object):
    def __init__(self):
        """
        """
        pass

    def __return_response(self, results, status):
        """

        :param results: results in a dict
        :param status: status code
        :return:
        """
        response = json.dumps(results)

        current_app.logger.info('sending response status=%s' % (status))
        current_app.logger.info('sending response text=%s' % (response))

        r = Response(response=response, status=status)
        r.headers['content-type'] = 'application/json'
        return r


    def process_request(self, payload):
        """
        process the request

        :param payload:
        :return: json code of the result or error
        """

        if not payload:
            return self.__return_response({'error': 'no information received'}, 400)
        if 'bibcode' not in payload:
            return self.__return_response({'error': 'no bibcode found in payload (parameter name is `bibcode`)'}, 400)

        bibcodes = payload['bibcode']

        if len(bibcodes) == 0:
            return self.__return_response({'error': 'no bibcode received'}, 400)

        if len(bibcodes) > current_app.config['RESOLVER_MAX_RECORDS_DEL']:
            return self.__return_response({'error': 'too many records to delete to db at one time, received %s records while the limit is %s'%(len(records), current_app.config['RESOLVER_MAX_RECORDS_DEL'])}, 400)

        current_app.logger.info('received request to delete from db %d bibcodes' % (len(bibcodes)))

        status, count, text = del_records(bibcodes)
        if status == True:
            current_app.logger.info('completed request to delete from db total of %d records' % (count))
            return self.__return_response({'status': text}, 200)
        current_app.logger.info('failed to delete from db %d bibcodes' % (len(bibcodes)))
        return self.__return_response({'error': text}, 400)


@advertise(scopes=[], rate_limit=[1000, 3600 * 24])
@bp.route('/<bibcode>', defaults={'link_type': ''}, methods=['GET'])
@bp.route('/<bibcode>/<link_type>', methods=['GET'])
def resolver(bibcode, link_type):
    """
    endpoint, with required param bibcode and optional param link type, that could contain one of the link sub type values
    :param bibcode:
    :param link_type: 
    :return:
    """
    if bibcode == 'check_link_type':
        return LinkRequest('', link_type.upper()).check()
    return LinkRequest(bibcode, link_type.upper()).process_request()


@advertise(scopes=[], rate_limit=[1000, 3600 * 24])
@bp.route('/<bibcode>/<link_type>:<path:id>', methods=['GET'])
def resolver_id(bibcode, link_type, id):
    """
    endpoint for identification link types: doi and arXiv
    :param bibcode:
    :param link_type:
    :return:
    """
    return LinkRequest(bibcode, link_type.upper(), id).process_request()


@advertise(scopes=[], rate_limit=[1000, 3600 * 24])
@bp.route('/<bibcode>/<path:url>', methods=['GET'])
def verity_url(bibcode, url):
    """
    endpoint for verifying outside url
    :param bibcode:
    :param link_type:
    :return:
    """
    return LinkRequest(bibcode).verify_url(url)

@advertise(scopes=['ads:resolver-service'], rate_limit=[1000, 3600 * 24])
@bp.route('/update', methods=['PUT'])
def update():
    """
    """
    try:
        payload = request.get_json(force=True)  # post data in json
    except:
        payload = dict(request.form)  # post data in form encoding

    return PopulateRequest().process_request(payload)

@advertise(scopes=['ads:resolver-service'], rate_limit=[1000, 3600 * 24])
@bp.route('/delete', methods=['DELETE'])
def remove():
    """
    """
    try:
        payload = request.get_json(force=True)  # post data in json
    except:
        payload = dict(request.form)  # post data in form encoding

    return DeleteRequest().process_request(payload)
