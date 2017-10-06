#!/usr/bin/python
# -*- coding: utf-8 -*-


# what is the location of the ADS UI
ADS_BASEURL = 'https://ui.adsabs.harvard.edu'
SQLALCHEMY_URL = 'postgresql://postgres:postgres@localhost:15432/data_pipeline'


# This is the URL to communicate with resolver_gateway api
RESOLVER_GATEWAY_URL = 'http://localhost:5000/resolver/{bibcode}/{linkType}/{URL}'
RESOLVER_GATEWAY_URL_TEST = '/resolver/{bibcode}/{linkType}/{URL}'
