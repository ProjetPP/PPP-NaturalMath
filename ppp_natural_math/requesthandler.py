"""Request handler of the module."""

from ppp_datamodel import Sentence, Response, TraceItem
from ppp_libmodule.exceptions import ClientError

from . import parser

def normalize(s):
    return s.replace(' ', '').lower()

class RequestHandler:
    def __init__(self, request):
        self.request = request

    def answer(self):
        if not isinstance(self.request.tree, Sentence):
            return []
        try:
            s = Sentence(parser.translate(self.request.tree.value))
        except parser.ParserException:
            return []
        if normalize(s.value) == normalize(self.request.tree.value):
            return []
        return [Response(self.request.language, s, {},
                self.request.trace + [TraceItem('NaturalMath', s, {})])]
