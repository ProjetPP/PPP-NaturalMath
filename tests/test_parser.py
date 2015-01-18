import unittest

from ppp_natural_math.parser import *

class ParserTestCase(unittest.TestCase):
    def assertParses(self, in_, out):
        self.assertEqual(build_tree(in_), out)
    def assertTranslates(self, in_, out):
        self.assertEqual(translate(in_), out)

    def testVariableBase(self):
        self.assertParses('x', Variable('x'))
        self.assertTranslates('x', 'x')
    def testIntegrateBase(self):
        self.assertParses('integrate x', Integrate(Variable('x'), 'x'))
        self.assertTranslates('integrate x', 'Integrate(x, x)')
        self.assertTranslates('integrate of x', 'Integrate(x, x)')
        self.assertTranslates('integrate x from y to z', 'Integrate(x, x, y, z)')
        self.assertTranslates('integral of x', 'Integrate(x, x)')
    def testSumBase(self):
        self.assertParses('sum i', Sum(Variable('i'), 'i'))
        self.assertTranslates('sum i', 'Sum(i, i)')
        self.assertTranslates('sum of i', 'Sum(i, i)')
        self.assertTranslates('sum i from y to z', 'Sum(i, i, y, z)')
        self.assertTranslates('sum j from y to z', 'Sum(j, j, y, z)')
    def testMultipleSums(self):
        self.assertTranslates('sum sum i^j', 'Sum(Sum(i^j, j), i)')
    def testProductBase(self):
        self.assertParses('product i', Product(Variable('i'), 'i'))
        self.assertTranslates('product i', 'Product(i, i)')
        self.assertTranslates('product g(i)', 'Product(g(i), i)')
        self.assertTranslates('product of i', 'Product(i, i)')
        self.assertTranslates('product i from y to z', 'Product(i, i, y, z)')
        self.assertTranslates('product j from y to z', 'Product(j, j, y, z)')

    def testSumIntegrate(self):
        self.assertTranslates('integrate sum i*x', 'Integrate(Sum(i*x, i), x)')
        self.assertTranslates('sum integrate i*x', 'Sum(Integrate(i*x, x), i)')
        self.assertTranslates('sum integrate i*f(x)', 'Sum(Integrate(i*f(x), x), i)')
