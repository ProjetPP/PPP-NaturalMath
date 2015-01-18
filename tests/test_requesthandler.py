from ppp_datamodel import Sentence
from ppp_datamodel.communication import Request, TraceItem, Response
from ppp_libmodule.tests import PPPTestCase
from ppp_natural_math import app

class TestFollowing(PPPTestCase(app)):
    config_var = 'PPP_NATURALMATH'
    config = ''
    def testBasics(self):
        q = Request('1', 'en', Sentence('integral of x^y'))
        r = self.request(q)
        self.assertEqual(len(r), 1, r)
        self.assertEqual(r[0].tree, Sentence('Integrate(x^y, y)'))

        q = Request('1', 'en', Sentence('x'))
        r = self.request(q)
        self.assertEqual(r, [])

        q = Request('1', 'en', Sentence('*$$!-|'))
        r = self.request(q)
        self.assertEqual(r, [])
