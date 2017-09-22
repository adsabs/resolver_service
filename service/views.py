#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import request, Blueprint, Response
from flask_discoverer import advertise

from linksRequest import *

bp = Blueprint('resolver_service', __name__)

def __returnResponse(response, status):
    r = Response(response=response, status=status)
    r.headers['content-type'] = 'application/json'
    return r

@advertise(scopes=[], rate_limit=[1000, 3600 * 24])
@bp.route('/resolver/<bibcode>/<linkType>', methods=['GET'])
def resolver(bibcode, linkType):
    if (len(bibcode) == 0) or (len(linkType) == 0):
        return __returnResponse('error: not all the needed information received', 400)

    [response, status] = processRequest(bibcode, linkType.upper(), request.referrer)
    return __returnResponse(response, status)