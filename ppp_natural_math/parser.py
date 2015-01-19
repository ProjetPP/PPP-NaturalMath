from collections import namedtuple
from ply import lex, yacc

reserved = {
    'sum': 'SUM',
    'sums': 'SUM',
    'product': 'PRODUCT',
    'products': 'PRODUCT',
    'integral': 'INTEGRATE',
    'integrals': 'INTEGRATE',
    'integrate':  'INTEGRATE',
    'antiderivate': 'INTEGRATE',
    'antiderivative': 'INTEGRATE',
    'antiderivatives': 'INTEGRATE',
    'derivate': 'DERIVATE',
    'derivative': 'DERIVATE',
    'derivatives': 'DERIVATE',
    'differential': 'DERIVATE',
    'differentials': 'DERIVATE',
    'differentiate':  'DERIVATE',
    'from': 'FROM',
    'to': 'TO',
    'of': 'OF',
    'left': 'LEFT',
    'right': 'RIGHT',
    'limit': 'LIMIT',
    'lim': 'LIMIT',
    'at': 'AT',
    'when': 'WHEN',
    'approaches': 'APPROACHES',
    'approx': 'APPROX',
    'approximate': 'APPROX',
    'approximates': 'APPROX',
    'approximation': 'APPROX',
    'eval': 'APPROX',
    'evaluate': 'APPROX',
    'evaluates': 'APPROX',
    'numeric': 'APPROX',
    'numerics': 'APPROX',
    }

tokens = (
    'SUM',
    'PRODUCT',
    'INTEGRATE',
    'DERIVATE',
    'FROM',
    'TO',
    'OF',
    'INFIX',
    'POSTFIX',
    'LEFT_PAREN',
    'RIGHT_PAREN',
    'NAME',
    'NATURAL',
    'NUMBER',
    'UNDERSCORE',
    'COMMA',
    'RIGHT',
    'LEFT',
    'LIMIT',
    'AT',
    'WHEN',
    'APPROACHES',
    'APPROX',
    )

t_LEFT_PAREN = r'\('
t_RIGHT_PAREN = r'\)'
def t_NAME(t):
    r'(?i)[a-z][a-z0-9]*'
    t.type = reserved.get(t.value.lower(), 'NAME')
    return t
t_NATURAL = r'[1-9][0-9]*'
t_NUMBER = r'-?([0-9]*[.,])?[0-9]+'
t_POSTFIX = r'[!]'
t_INFIX = r'[-+*/^]'
t_UNDERSCORE = r'_'
t_COMMA = r','

t_ignore = r' '

def t_error(t):
    raise ParserException('Illegal string `%s`' % t.value)

lexer = lex.lex()

class ParserException(Exception):
    pass
class CannotGuessVariable(ParserException):
    pass

def guess_variable(expression, hint):
    free_vars = expression.free_vars()
    if len(free_vars) == 1:
        return list(free_vars)[0]
    for name in hint:
        if name in free_vars:
            return name
    raise CannotGuessVariable(expression, hint)


class Variable(namedtuple('_Variable', 'name')):
    def free_vars(self):
        return {self.name}

    def __repr__(self):
        return 'Variable(%r)' % self.name

    def output(self):
        return self.name

class Paren(namedtuple('_Paren', 'expr')):
    def free_vars(self):
        return self.expr.free_vars()

    def __repr__(self):
        return 'Paren(%r)' % self.expr

    def output(self):
        return '(%s)' % self.expr.output()

class Call(namedtuple('_Call', 'function arguments')):
    def free_vars(self):
        return set.union(*[x.free_vars() for x in self.arguments])

    def __repr__(self):
        return 'Variable(%r, %r)' % (self.function, self.arguments)

    def output(self):
        return '%s(%s)' % (self.function,
                ', '.join(x.output() for x in self.arguments))

class Postfix(namedtuple('_Postfix', 'left op')):
    def free_vars(self):
        return self.left.free_vars()

    def __repr__(self):
        return 'Infix(%r, %r)' % \
                (self.left, self.op)

    def output(self):
        return '%s%s' % (self.left.output(), self.op)

class Infix(namedtuple('_Infix', 'left op right')):
    def free_vars(self):
        return self.left.free_vars() | self.right.free_vars()

    def __repr__(self):
        return 'Infix(%r, %r, %r)' % \
                (self.left, self.op, self.right)

    def output(self):
        return '%s%s%s' % (self.left.output(), self.op, self.right.output())

class Number(namedtuple('_Number', 'value')):
    def free_vars(self):
        return set()

    def __repr__(self):
        return 'Number(%r)' % self.value

    def output(self):
        return str(self.value)

class TwoBounds:
    def __init__(self, expr, var=None, from_=None, to=None):
        self._expr = expr
        self._var = var or guess_variable(expr, self._variable_hint)
        self._from = from_
        self._to = to
        if not isinstance(self.var, str):
            raise ValueError('%r is not a string' % self.var)

    def add_fromto(self, from_, to):
        return self.__class__(self.expr, self.var, from_=from_, to=to)

    @property
    def expr(self):
        return self._expr
    @property
    def var(self):
        return self._var
    @property
    def from_(self):
        return self._from
    @property
    def to(self):
        return self._to

    def free_vars(self):
        return self.expr.free_vars() - {self.var}

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return (self.expr, self.var, self.from_, self.to) == \
                (other.expr, other.var, other.from_, other.to)

    def __hash__(self):
        return hash((other.expr, other.var, other.from_, other.to))

    def __repr__(self):
        return '%s(%r, %r, %r, %r)' % (self.__class__.__name__,
                self.expr, self.var, self.from_, self.to)

    def output(self):
        if self.from_ and self.to:
            return '%s(%s, %s, %s, %s)' % (self.__class__.__name__,
                    self.expr.output(), self.var,
                    self.from_.output(), self.to.output())
        else:
            return '%s(%s, %s)' % (self.__class__.__name__,
                    self.expr.output(), self.var)

class Integrate(TwoBounds):
    _variable_hint = 'wvutzyx'
class Sum(TwoBounds):
    _variable_hint = 'lkjimn'
class Product(TwoBounds):
    _variable_hint = 'lkjimn'

class Derivate:
    _variable_hint = 'tzyx'
    def __init__(self, expr, var=None):
        self._expr = expr
        self._var = var or guess_variable(expr, self._variable_hint)
        if not isinstance(self.var, str):
            raise ValueError('%r is not a string' % self.var)

    @property
    def expr(self):
        return self._expr
    @property
    def var(self):
        return self._var

    def free_vars(self):
        return self.expr.free_vars() - {self.var}

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return (self.expr, self.var) == \
                (other.expr, other.var)

    def __hash__(self):
        return hash((other.expr, other.var))

    def __repr__(self):
        return '%s(%r, %r, %r, %r)' % (self.__class__.__name__,
                self.expr, self.var)

    def output(self):
        return 'diff(%s, %s)' % (self.expr.output(), self.var)

class Limit(namedtuple('_Limit', 'expression variable point')):
    def free_vars(self):
        # XXX Maybe add point?
        return self.expression.free_vars() - {self.variable}

    def __repr__(self):
        return '%s(%r, %r, %r)' % (self.__class__.__name__,
                self.expression, self.variable, self.point)

    def output(self):
        return '%s(%s, %s, %s)' % (self.__class__.__name__,
                self.expression.output(),
                self.variable, self.point.output())
class RLimit(Limit):
    pass
class LLimit(Limit):
    pass

class Approx(namedtuple('_Approx', 'expression')):
    def free_vars(self):
        return self.expression.free_vars()

    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__,
                self.expression)

    def output(self):
        return '%s(%s)' % (self.__class__.__name__,
                self.expression.output())

###################################################
# Variables
def p_variable_name(t):
    '''variable : NAME'''
    t[0] = Variable(t[1])
def p_variable_underscore(t):
    '''variable : variable UNDERSCORE NATURAL'''
    t[0] = Variable('%s_%d' % (t[1].name, t[3]))
def p_expression_variable(t):
    '''expression : variable'''
    t[0] = t[1] 

###################################################
# Misc
def p_number(t):
    '''number : NUMBER'''
    v = t[1]
    if '.' in v:
        t[0] = Number(float(v))
    elif ',' in v:
        t[0] = Number(float(v.replace(',', '.')))
    else:
        t[0] = Number(int(v))
def p_expression_number(t):
    '''expression : number'''
    t[0] = t[1]
def p_expression_postfix_base(t):
    '''expression : number POSTFIX
                  | variable POSTFIX'''
    t[0] = Postfix(t[1], t[2])
def p_expression_postfix_paren(t):
    '''expression : LEFT_PAREN expression RIGHT_PAREN POSTFIX'''
    t[0] = Postfix(Paren(t[2]), t[4])
def p_expression_infix(t):
    '''expression : expression INFIX expression'''
    t[0] = Infix(t[1], t[2], t[3])
def p_expression_paren(t):
    '''expression : LEFT_PAREN expression RIGHT_PAREN'''
    t[0] = Paren(t[2])
def p_fromto(t):
    '''fromto : FROM expression TO expression'''
    t[0] = (t[2], t[4])

###################################################
# Functions
def p_call_begin(t):
    '''call : NAME LEFT_PAREN expression'''
    t[0] = Call(t[1], [t[3]])
def p_call_continue(t):
    '''call : call COMMA expression'''
    t[0] = Call(t[1].function, t[1].arguments + [t[3]])
def p_call_end(t):
    '''expression : call RIGHT_PAREN'''
    t[0] = t[1]
def p_expression_call2(t):
    '''expression : NAME OF expression'''
    t[0] = Call(t[1], [t[3]])

###################################################
# Sum
def p_sum_base(t):
    '''sum : SUM expression'''
    t[0] = Sum(t[2], from_=Number(1), to=Variable('Infinity'))
def p_sum_base2(t):
    '''sum : SUM OF expression'''
    t[0] = Sum(t[3], from_=Number(1), to=Variable('Infinity'))
# TODO: Shift/reduce conflict
def p_expression_sum(t):
    '''expression : sum'''
    t[0] = t[1]
def p_expression_sum_fromto(t):
    '''expression : sum fromto'''
    t[0] = t[1].add_fromto(*t[2])

###################################################
# Product
def p_product_base(t):
    '''product : PRODUCT expression'''
    t[0] = Product(t[2], from_=Number(1), to=Variable('Infinity'))
def p_product_base2(t):
    '''product : PRODUCT OF expression'''
    t[0] = Product(t[3], from_=Number(1), to=Variable('Infinity'))
# TODO: Shift/reduce conflict
def p_expression_product(t):
    '''expression : product'''
    t[0] = t[1]
def p_expression_product_fromto(t):
    '''expression : product fromto'''
    t[0] = t[1].add_fromto(*t[2])

###################################################
# Integrate
def p_integrate_base(t):
    '''integrate : INTEGRATE expression'''
    t[0] = Integrate(t[2])
def p_integrate_base2(t):
    '''integrate : INTEGRATE OF expression'''
    t[0] = Integrate(t[3])
# TODO: Shift/reduce conflict
def p_expression_integrate(t):
    '''expression : integrate'''
    t[0] = t[1]
def p_expression_integrate_fromto(t):
    '''expression : integrate fromto'''
    t[0] = t[1].add_fromto(*t[2])

###################################################
# Derivate
def p_derivate_base(t):
    '''derivate : DERIVATE expression'''
    t[0] = Derivate(t[2])
def p_derivate_base2(t):
    '''derivate : DERIVATE OF expression'''
    t[0] = Derivate(t[3])
def p_expression_derivate(t):
    '''expression : derivate'''
    t[0] = t[1]


###################################################
# Limit
def p_expression_limit(t):
    '''expression : limit'''
    t[0] = t[1]
def p_expression_right_limit(t):
    '''expression : RIGHT limit'''
    t[0] = RLimit(*t[2])
def p_expression_left_limit(t):
    '''expression : LEFT limit'''
    t[0] = LLimit(*t[2])
def p_unboundedlimit_base(t):
    '''unboundedlimit : LIMIT expression'''
    t[0] = Limit(t[2], guess_variable(t[2], 'tzyxlkjimn'),
            Variable('Infinity'))
def p_unboundedlimit_base2(t):
    '''unboundedlimit : LIMIT OF expression'''
    t[0] = Limit(t[3], guess_variable(t[3], 'tzyxlkjimn'),
            Variable('Infinity'))
def p_limit_base(t):
    '''limit : unboundedlimit'''
    t[0] = t[1]
def p_limit_at(t):
    '''limit : unboundedlimit AT expression'''
    t[0] = Limit(t[1].expression, t[1].variable, t[3])
def p_limit_approache_at(t):
    '''limit : unboundedlimit WHEN variable APPROACHES expression'''
    t[0] = Limit(t[1].expression, t[3].name, t[5])

###################################################
# Approximation
def p_expression_approximation(t):
    '''expression : APPROX expression'''
    t[0] = Approx(t[2])



def p_error(t):
    if t is None:
        raise ParserException('Unknown PLY error.')
    else:
        raise ParserException("Syntax error at '%s' (%s)" % 
                (t.value, t.type))

parser = yacc.yacc(start='expression', debug=0, write_tables=0)

def build_tree(s):
    return parser.parse(s, lexer=lexer)

def translate(s):
    return build_tree(s).output()
