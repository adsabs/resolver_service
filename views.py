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
@bp.route('/resolver', methods=['GET'])
def resolver():

    if 'bibcode' not in request.args:
        return __returnResponse('error: no bibcode found in request (parameter name is "bibcode")', 400)
    elif 'link_type' not in request.args:
        return __returnResponse('error: no link_type found in request (parameter name is "link_type")', 400)

    bibcode = request.args.get("bibcode")
    linkType = request.args.get("link_type").upper()

    if (len(bibcode) == 0) or (len(linkType) == 0):
        return __returnResponse('error: not all the needed information received', 400)

    [response, status] = processRequest(bibcode, linkType, request.referrer)
    return __returnResponse(response, status)