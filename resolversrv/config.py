#!/usr/bin/python
# -*- coding: utf-8 -*-


SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:postgres@localhost:15432/data_pipeline'
SQLALCHEMY_TRACK_MODIFICATIONS = False

# This is the URL to communicate with resolver_gateway api
RESOLVER_GATEWAY_URL = 'http://localhost:5000/resolver/{bibcode}/{link_type}/{url}'
RESOLVER_GATEWAY_URL_TEST = '/resolver/{bibcode}/{link_type}/{url}'
