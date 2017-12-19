#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Flask
import logging.config
from flask_restful import Api
from flask_discoverer import Discoverer
from .models import Record
from .views import bp
from sqlalchemy.orm import load_only

def create_app(config=None):
    """
    Create the application and return it to the user
    :return: flask.Flask application
    """

    app = FlaskApp(__name__, static_folder=None)
    app.url_map.strict_slashes = False

    # Load config and logging
    load_config(app, config)
    logging.config.dictConfig(
        app.config['RESOLVER_SERVICE_LOGGING']
    )

    # Register extensions
    api = Api(app)
    Discoverer(app)

    app.register_blueprint(bp)
    return app


def FlaskApp(Flask):

    def __init__(self, *args, **kwargs):
        super(Flask, self).__init__(*args, **kwargs)

    
    def get_record(self, bibcode, link_type, link_subtype='', db='nonbib', fields=None):
        """
        TODO: documentation docstring
        """
        with self.db_session() as session:
            if not link_subtype:
                query = session.query(Record).filter(and_(Record.db == db, Record.link_type == link_type))
            else:
                query = session.query(Record).filter(and_(Record.db == db, Record.link_type == link_type, Record.link_subtype == link_subtype))
                
            if fields:
                query = query.options(load_only(*fields)) # otherwise it loads everything
            r = query.first()
            
            if r:
                return r.toJSON()
            else:
                return None # or decide what to do when rec doesn't exist, raise exception?
            
    


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, use_reloader=False)