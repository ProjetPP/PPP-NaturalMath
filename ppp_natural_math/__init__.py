"""Natural language processing for math questions for the Projet Pensées
Profondes."""

from ppp_libmodule import HttpRequestHandler
from .requesthandler import RequestHandler

def app(environ, start_response):
    """Function called by the WSGI server."""
    return HttpRequestHandler(environ, start_response, RequestHandler) \
            .dispatch()
