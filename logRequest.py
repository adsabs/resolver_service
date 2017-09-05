#!/usr/bin/python
# -*- coding: utf-8 -*-

import watchtower, logging
import datetime
from linksData import *
import os, socket

def sendLog(bibcode, linkType, linkURL, referrerURL):

    hostname = socket.gethostname()
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    handler = watchtower.CloudWatchLogHandler(stream_name=str(hostname) + "-" + str(os.getpid()) + "-app",
                                              log_group="production-resolver-app")
    logger.addHandler(handler)
    logger.info('"{dateUTC}" "{mirror}" "{server}" "{host}" "{user}" "{db}" "{link}" "{bibcode}" "{service}" "{referer}"'.format(
        dateUTC=datetime.datetime.utcnow().isoformat(),
        mirror="",
        server=str(hostname),
        host=str(socket.gethostbyname(hostname)),
        user="",
        db="",
        link=getLinkTag(linkType),
        bibcode=bibcode,
        service=linkURL,
        referer=referrerURL))
