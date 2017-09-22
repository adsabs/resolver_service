#!/usr/bin/python
# -*- coding: utf-8 -*-

import json

from linksData import *
from logRequest import *

def processRequest(bibcode, linkType, referreredURL=''):

    onTheFly = {
        'ABSTRACT' : 'https://ui.adsabs.harvard.edu/#abs/{bibcode}/{linkType}',
        'CITATIONS': 'https://ui.adsabs.harvard.edu/#abs/{bibcode}/{linkType}',
        'REFERENCES': 'https://ui.adsabs.harvard.edu/#abs/{bibcode}/{linkType}',
        'COREADS': 'https://ui.adsabs.harvard.edu/#abs/{bibcode}/{linkType}',
        'ADS_SCAN': 'http://articles.adsabs.harvard.edu/full/{bibcode}',
        'COMMENTS': 'http://adsabs.harvard.edu/NOTES/{bibcode}.html',
        'TOC': '???'
    }
    # toc/all.links is the list of bibcodes which should have this link activated,
    # but as with references, citations, etc. the list of articles which should be
    # generated is computed on the fly via a SOLR search. All we have to do is add
    # TOC to the list of properties in the solr document

    eSource = {
        'ARTICLE' : '{linkURL}',
        'PUB_HTML' : '{linkURL}',
        'PUB_PDF' : '{linkURL}',
        'ADS_PDF' : '{linkURL}',
        'ADS_SCAN' : '{linkURL}',
        'ARXIV_HTML' : 'https://arxiv.org/abs/{linkURL}',
        'ARXIV_PDF' : '{linkURL}',
        'AUTHOR_HTML' : '{linkURL}',
        'AUTHOR_PDF' : '{linkURL}'
    }
    data = ['ARI','SIMBAD','NED','CDS','Vizier','GCPD','Author','PDG','MAST','HEASARC','INES','IBVS','Astroverse',
            'ESA','NExScI','PDS','AcA','ISO','ESO','CXO','NOAO','XMM','Spitzer','PASA','ATNF','KOA','Herschel','GTC',
            'BICEP2','ALMA','CADC','Zenodo','TNS']

    # backward compatibility conversation
    linkType = linkType.replace('GIF','ADS_SCAN').replace('PREPRINT','ARXIV_HTML').replace('EJOURNAL', 'PUB_HTML')

    # we have 7 link types that can be created on the fly and do not need to go to db
    # we just need to log the request
    if (linkType in onTheFly):
        if (linkType == 'COMMENTS'):
            bibcode = bibcode.replace('A&A', 'A+A')
        linkURL = onTheFly[linkType].format(bibcode=bibcode, linkType=linkType)
        return returnResponse(bibcode, linkType, linkURL, referreredURL, linkURL)

    # for the following two types also we only needs to log the request
    elif (linkType == 'LIBRARYENTRIES') or (linkType == 'CUSTOM'):
        return ['', 200]

    # the rest of the link types query the db, some return just a url, and some JSON code of pair values url and title

    # the following four link types have been defined in Solr field property:
    # INSPIRE, LIBRARYCATALOG, PRESENTATION, and ASSOCIATED
    # the first three return a url, the last type returns a JSON code
    elif (linkType == 'INSPIRE') or (linkType == 'LIBRARYCATALOG') or (linkType == 'PRESENTATION'):
        linkURL = getURL(bibcode, linkType)
        return returnResponse(bibcode, linkType, linkURL, referreredURL, linkURL)

    elif (linkType == 'ASSOCIATED'):
        # we are logging the link that send us here
        pageURL= 'https://ui.adsabs.harvard.edu/#abs/{}/associated'.format(bibcode)
        linkFormat = 'https://ui.adsabs.harvard.edu/resolver/{}/abstract'
        jsonCode = rowsToJSON(getURLandTitle(bibcode, linkType), linkFormat)
        return returnResponse(bibcode, linkType, pageURL, referreredURL, jsonCode)

    # EJOURNAL, ARTICLE, and PREPRINT are classics' link types
    # for BBB we have defined more specifically the source of full text resources and have divided them into 8
    # types, defined in Solr field eSource
    # note that for backward compatibility we are recognizing the classic types
    # they return a url
    elif (linkType in eSource):
        linkURL = getURL(bibcode, linkType)
        if (len(linkURL) > 0):
            linkURL = eSource[linkType].format(linkURL=''.join(linkURL))
        return returnResponse(bibcode, linkType, linkURL, referreredURL, linkURL)

    # the following link types have been defined in Solr field data
    # they return a url
    elif (linkType in data):
        linkURL = getURL(bibcode, linkType)
        return returnResponse(bibcode, linkType, linkURL, referreredURL, linkURL)

    # we did not recognize the linkType, so return an error
    else:
        return ["error: unrecognizable linkType:'{linkType}'".format(linkType=linkType), 400]

def rowsToJSON(rows, formatStr):

    data = []
    if (len(rows) > 0):
        data.append({'count':len(rows)})
        for i, row in enumerate(rows):
            item = {}
            item['bibcode'] = row[0]
            item['title'] = row[1]
            item['link'] = formatStr.format(row[0])
            data.append(item)
        return json.dumps(data)
    return data


def returnResponse(bibcode, linkType, linkURL, referreredURL, response):
    if (len(response) != 0):
        sendLog(bibcode, linkType, linkURL, referreredURL)
        return [response, 200]
