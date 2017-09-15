#!/usr/bin/python
# -*- coding: utf-8 -*-

import watchtower, logging
import datetime
import os

loggers = {}

def sendLog(bibcode, linkType, linkURL, referrerURL):

    global loggers
    logger = logging.getLogger(__name__)
    if not len(logger.handlers):
        logging.basicConfig(level=logging.INFO)
        handler = watchtower.CloudWatchLogHandler(stream_name=str(os.uname()[1]) + "-" + str(os.getpid()) + "-app",
                                                  log_group="production-resolver-app")
        logger.addHandler(handler)

    logger.info('"{dateUTC}" "{server}" "{host}" "{user}" "{link}" "{bibcode}" "{service}" "{referer}"'.format(
        dateUTC=datetime.datetime.utcnow().isoformat(),
        server=str(os.uname()[1]),
        host=str(os.uname()[1]),
        user="",
        link=linkType,
        bibcode=bibcode,
        service=linkURL,
        referer=referrerURL))

