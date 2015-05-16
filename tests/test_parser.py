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
        self.assertTranslates('5*y', '5*y')
        self.assertTranslates('-5*y', '-5*y')
        self.assertTranslates('.5*y', '0.5*y')
        self.assertTranslates('1,5*y', '1.5*y')
        self.assertTranslates('x*y', 'x*y')
        self.assertTranslates('x*y+z', 'x*y+z')
        self.assertTranslates('x*(y+z)', 'x*(y+z)')
        self.assertTranslates('x*(integral y+z)', 'x*(Integrate(y+z, z))')
        self.assertTranslates('(n)!', '(n)!')
        self.assertTranslates('n!', 'n!')
        self.assertTranslates('5!', '5!')
    def testFunctionCall(self):
        self.assertTranslates('sin of pi', 'sin(pi)')
        self.assertTranslates('f(x,y)', 'f(x, y)')
        self.assertTranslates('probability of x', 'P(x)')
        self.assertTranslates('probability(x)', 'P(x)')
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
        self.assertParses('sum i', Sum(Variable('i'), 'i', Number(1), Variable('Infinity')))
        self.assertTranslates('sum i', 'Sum(i, i, 1, Infinity)')
        self.assertTranslates('sum of i', 'Sum(i, i, 1, Infinity)')
        self.assertTranslates('sum i from y to z', 'Sum(i, i, y, z)')
        self.assertTranslates('sum j from y to z', 'Sum(j, j, y, z)')
        self.assertTranslates('sum bla from y to z', 'Sum(bla, bla, y, z)')
    def testMultipleSums(self):
        self.assertTranslates('sum sum i^j', 'Sum(Sum(i^j, j, 1, Infinity), i, 1, Infinity)')
    def testProductBase(self):
        self.assertParses('product i', Product(Variable('i'), 'i', Number(1), Variable('Infinity')))
        self.assertTranslates('product i', 'Product(i, i, 1, Infinity)')
        self.assertTranslates('product g(i)', 'Product(g(i), i, 1, Infinity)')
        self.assertTranslates('product of i', 'Product(i, i, 1, Infinity)')
        self.assertTranslates('product i from y to z', 'Product(i, i, y, z)')
        self.assertTranslates('product j from y to z', 'Product(j, j, y, z)')

    def testSumIntegrate(self):
        self.assertTranslates('integrate sum i*x', 'Integrate(Sum(i*x, i, 1, Infinity), x)')
        self.assertTranslates('sum integrate i*x', 'Sum(Integrate(i*x, x), i, 1, Infinity)')
        self.assertTranslates('sum integrate i*f(x)', 'Sum(Integrate(i*f(x), x), i, 1, Infinity)')

    def testFactorial(self):
        self.assertTranslates('integrate sum x*i!', 'Integrate(Sum(x*i!, i, 1, Infinity), x)')

    def testLimitBase(self):
        self.assertTranslates('limit 1/x', 'Limit(1/x, x, Infinity)')
        self.assertTranslates('right limit 1/x', 'RLimit(1/x, x, Infinity)')
        self.assertTranslates('left limit 1/x', 'LLimit(1/x, x, Infinity)')
        self.assertTranslates('limit of 1/x', 'Limit(1/x, x, Infinity)')
        self.assertTranslates('right limit of 1/x', 'RLimit(1/x, x, Infinity)')
        self.assertTranslates('left limit of 1/x', 'LLimit(1/x, x, Infinity)')
        self.assertTranslates('limit of 1/x at 0', 'Limit(1/x, x, 0)')
        self.assertTranslates('right limit of 1/x at 0', 'RLimit(1/x, x, 0)')
        self.assertTranslates('left limit of 1/x at 0', 'LLimit(1/x, x, 0)')

    def testLimitApproach(self):
        self.assertTranslates('limit of y/x at 0', 'Limit(y/x, y, 0)')
        self.assertTranslates('limit of y/x when x approaches 0', 'Limit(y/x, x, 0)')
        self.assertTranslates('right limit of y/x when x approaches 0', 'RLimit(y/x, x, 0)')
        self.assertTranslates('left limit of y/x when x approaches 0', 'LLimit(y/x, x, 0)')

    def testApprox(self):
        self.assertTranslates('approximate 4/5', 'Approx(4/5)')
