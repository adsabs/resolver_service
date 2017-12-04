#!/usr/bin/python
# -*- coding: utf-8 -*-

from werkzeug.serving import run_simple

from flask_restful import Api
from flask_discoverer import Discoverer

from adsmutils import ADSFlask

from resolversrv.views import bp

def create_app(**config):
    """
    Create the application and return it to the user
    :return: flask.Flask application
    """

    # todo: figure out why getting this warning 'Sorry, cant find the proj home; returning the location of the caller'
    if config:
        app = ADSFlask(__name__, static_folder=None, local_config=config)
    else:
        app = ADSFlask(__name__, static_folder=None)

    app.url_map.strict_slashes = False

    # Register extensions
    api = Api(app)
    Discoverer(app)

    app.register_blueprint(bp)
    return app

if __name__ == '__main__':
    run_simple('0.0.0.0', 5000, create_app(), use_reloader=False, use_debugger=False)