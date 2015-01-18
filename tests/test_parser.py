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
    def testOperatorsBase(self):
        self.assertTranslates('x*y', 'x*y')
        self.assertTranslates('x*y+z', 'x*y+z')
        self.assertTranslates('x*(y+z)', 'x*(y+z)')
        self.assertTranslates('x*(integral y+z)', 'x*(Integrate(y+z, z))')
        self.assertTranslates('(n)!', '(n)!')
        self.assertTranslates('n!', 'n!')
    def testFunctionCall(self):
        self.assertTranslates('sin of pi', 'sin(pi)')
        self.assertTranslates('f(x,y)', 'f(x, y)')
    def testIntegrateBase(self):
        self.assertParses('integrate x', Integrate(Variable('x'), 'x'))
        self.assertTranslates('integrate x', 'Integrate(x, x)')
        self.assertTranslates('integrate of x', 'Integrate(x, x)')
        self.assertTranslates('integrate x from y to z', 'Integrate(x, x, y, z)')
        self.assertTranslates('integral of x', 'Integrate(x, x)')
        self.assertTranslates('integral of f(x, y)', 'Integrate(f(x, y), y)')
        self.assertTranslates('integral of integral of f(x, y)', 'Integrate(Integrate(f(x, y), y), x)')
    def testDerivateBase(self):
        self.assertParses('derivate x', Derivate(Variable('x'), 'x'))
        self.assertTranslates('derivate x', 'diff(x, x)')
        self.assertTranslates('derivate of x', 'diff(x, x)')
        self.assertTranslates('derivative of x', 'diff(x, x)')
        self.assertTranslates('derivative of f(x, y)', 'diff(f(x, y), y)')
        self.assertTranslates('derivative of derivative of f(x, y)', 'diff(diff(f(x, y), y), x)')
    def testSumBase(self):
        self.assertParses('sum i', Sum(Variable('i'), 'i'))
        self.assertTranslates('sum i', 'Sum(i, i)')
        self.assertTranslates('sum of i', 'Sum(i, i)')
        self.assertTranslates('sum i from y to z', 'Sum(i, i, y, z)')
        self.assertTranslates('sum j from y to z', 'Sum(j, j, y, z)')
        self.assertTranslates('sum bla from y to z', 'Sum(bla, bla, y, z)')
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

    def testFactorial(self):
        self.assertTranslates('integrate sum x*i!', 'Integrate(Sum(x*i!, i), x)')
