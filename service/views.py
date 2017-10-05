#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import request, Blueprint
from flask_discoverer import advertise

from adsputils import load_config, setup_logging

from linksRequest import LinkRequest

bp = Blueprint('resolver_service', __name__)

logger = None
config = {}

@advertise(scopes=[], rate_limit=[1000, 3600 * 24])
@bp.route('/v1/resolver/<bibcode>/<linkType>', methods=['GET'])
def resolver(bibcode, linkType):

    global logger
    global config

    if logger == None:
        config.update(load_config())
        logger = setup_logging('resolver_service', config.get('LOG_LEVEL', 'INFO'))

    logger.info('received request with bibcode={bibcode} and linkType={linkType}'.format(bibcode=bibcode, linkType=linkType))

    return LinkRequest(bibcode, linkType.upper(), request.referrer).processRequest()

