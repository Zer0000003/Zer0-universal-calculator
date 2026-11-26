"""Restricted mathematical grammar; no eval, exec, or shell interpolation."""
import ctypes
import re
import signal
import sys
from pathlib import Path
import sympy as s

try:
    native = ctypes.CDLL(str(Path(__file__).with_name('libinteger_math.so').resolve()))
    for name in ('math_add', 'math_sub', 'math_mul'):
        fn = getattr(native, name)
        fn.argtypes = [ctypes.c_int64, ctypes.c_int64, ctypes.POINTER(ctypes.c_int64)]
        fn.restype = ctypes.c_int
except OSError:
    native = None


def arithmetic(op, a, b):
    if op in ('+', '-', '*') and native and isinstance(a, s.Integer) and isinstance(b, s.Integer):
        if all(-(1 << 63) <= int(v) < (1 << 63) for v in (a, b)):
            result = ctypes.c_int64()
            fn = getattr(native, {'+':'math_add', '-':'math_sub', '*':'math_mul'}[op])
            if fn(int(a), int(b), ctypes.byref(result)) == 0:
                return s.Integer(result.value)
    if op == '+': return a + b
    if op == '-': return a - b
    if op == '*': return a * b
    if op == '/': return a / b
    if op == '^': return a ** b
    if op == '=': return s.Eq(a, b, evaluate=False)
    if op in ('<', '>', '<=', '>=', '!='):
        return {'<': s.Lt, '>': s.Gt, '<=': s.Le, '>=': s.Ge, '!=': s.Ne}[op](a, b, evaluate=False)
    raise ValueError('Unknown operator')


def solve(*args):
    return s.solve(*args)


def determinant(a): return s.Matrix(a).det()
def inverse(a): return s.Matrix(a).inv()
def eigenvalues(a): return s.Matrix(a).eigenvals()
def rref(a): return s.Matrix(a).rref()
def approx(a, digits=15): return s.N(a, int(digits))
def summation(a, var, low, high): return s.summation(a, (var, low, high))
def product(a, var, low, high): return s.product(a, (var, low, high))
def mean(values): return sum(values) / s.Integer(len(values))
def variance(values):
    m = mean(values)
    return sum((v-m)**2 for v in values) / s.Integer(len(values))
def binomial_pmf(n, k, p): return s.binomial(n, k)*p**k*(1-p)**(n-k)
def normal_cdf(x, mu=0, sigma=1): return (1+s.erf((x-mu)/(sigma*s.sqrt(2))))/2
def gradient(expr, variables): return s.Matrix([s.diff(expr, v) for v in variables])
def jacobian(expressions, variables): return s.Matrix(expressions).jacobian(variables)
def integral(a, var, *bounds):
    if not bounds: return s.integrate(a, var)
    if len(bounds) == 2: return s.integrate(a, (var, *bounds))
    raise ValueError('integrate(expr, variable[, lower, upper])')

FUNCTIONS = {n: getattr(s, n) for n in (
    'sin', 'cos', 'tan', 'asin', 'acos', 'atan', 'sinh', 'cosh', 'tanh',
    'sqrt', 'exp', 'log', 'Abs', 'factorial', 'binomial', 'simplify',
    'factor', 'expand', 'cancel', 'together', 'apart', 'diff', 'limit',
    'series', 'gcd', 'lcm', 'isprime', 'factorint', 'dsolve', 'laplace_transform',
    'inverse_laplace_transform', 'linsolve', 'nonlinsolve', 'nsolve', 'floor', 'ceiling',
    're', 'im', 'conjugate', 'gamma', 'erf', 'zeta', 'mod_inverse', 'root')}
FUNCTIONS.update(solve=solve, integrate=integral, matrix=s.Matrix, det=determinant,
    inverse=inverse, eigenvalues=eigenvalues, rref=rref, approx=approx,
    sum=summation, product=product, ln=s.log, abs=s.Abs, mean=mean, variance=variance,
    binomial_pmf=binomial_pmf, normal_cdf=normal_cdf, gradient=gradient, jacobian=jacobian)
CONSTANTS = {'pi': s.pi, 'e': s.E, 'E': s.E, 'I': s.I, 'i': s.I, 'oo': s.oo, 'inf': s.oo}
TOKEN = re.compile(r'\s*(?:(\d+(?:\.\d*)?|\.\d+)(?:([eE][+-]?\d+))?|([A-Za-z_][A-Za-z_0-9]*)|(\*\*|<=|>=|!=|[+\-*/^=<>(),;\[\]!]))')


class Parser:
    def __init__(self, source):
        source = source.strip().replace('−', '-').replace('×', '*').replace('÷', '/').replace('π', 'pi').replace('∞', 'oo').replace('²', '^2').replace('³', '^3')
        if len(source) > 4096: raise ValueError('Input too long')
        self.tokens = []
        pos = 0
        while pos < len(source):
            m = TOKEN.match(source, pos)
            if not m: raise ValueError(f'Invalid character at position {pos+1}')
            num, exponent, name, op = m.groups()
            if num: self.tokens.append(('num', num + (exponent or '')))
            elif name: self.tokens.append(('name', name))
            else: self.tokens.append(('op', '^' if op == '**' else op))
            pos = m.end()
        self.tokens.append(('end', ''))
        self.i = 0

    def peek(self): return self.tokens[self.i]
    def take(self):
        token = self.peek()
        self.i += 1
        return token
    def accept(self, value):
        if self.peek()[1] == value:
            self.take()
            return True
        return False
    def expect(self, value):
        if not self.accept(value): raise ValueError(f'Expected {value}')
    def sequence(self, end):
        items = []
        if not self.accept(end):
            items.append(self.expr())
            while self.accept(','): items.append(self.expr())
            self.expect(end)
        return items
    def expr(self, min_bp=0):
        kind, val = self.take()
        if kind == 'num':
            left = s.Rational(val)
        elif kind == 'name':
            if val in FUNCTIONS and self.accept('('):
                left = FUNCTIONS[val](*self.sequence(')'))
            else:
                left = CONSTANTS.get(val, s.Symbol(val))
        elif val in ('+', '-'):
            left = self.expr(25)
            if val == '-': left = -left
        elif val == '(':
            left = self.expr()
            self.expect(')')
        elif val == '[':
            left = self.sequence(']')
        else:
            raise ValueError(f'Expected mathematical expression, found {val!r}')
        while True:
            kind, val = self.peek()
            if val == '!':
                if 40 < min_bp: break
                self.take()
                left = s.factorial(left)
                continue
            implicit = kind in ('num', 'name') or val == '('
            op = '*' if implicit else val
            binding = {'=':(2,3), '<':(2,3), '>':(2,3), '<=':(2,3), '>=':(2,3), '!=':(2,3), '+':(10,11), '-':(10,11), '*':(20,21), '/':(20,21), '^':(30,30)}.get(op)
            if not binding or binding[0] < min_bp: break
            if not implicit: self.take()
            right = self.expr(binding[1])
            left = arithmetic(op, left, right)
        return left
    def parse(self):
        items = [self.expr()]
        while self.accept(';'): items.append(self.expr())
        if self.peek()[0] != 'end': raise ValueError('Unexpected token: ' + self.peek()[1])
        return items


def evaluate(source):
    items = Parser(source).parse()
    if any(isinstance(v, s.core.relational.Relational) and not isinstance(v, s.Equality) for v in items):
        if not all(isinstance(v, s.core.relational.Relational) for v in items):
            raise ValueError('Enter only relations in an inequality system')
        variables = sorted(set().union(*(v.free_symbols for v in items)), key=str)
        return s.reduce_inequalities(items, variables)
    if len(items) > 1 or isinstance(items[0], s.Equality):
        if not all(isinstance(v, s.Equality) for v in items):
            raise ValueError('Semicolon-separated inputs must all be equations')
        variables = sorted(set().union(*(v.free_symbols for v in items)), key=str)
        if not variables:
            return all(s.simplify(v.lhs-v.rhs) == 0 for v in items)
        if len(items) == 1 and len(variables) == 1:
            return s.solveset(items[0], variables[0], domain=s.S.Complexes)
        return s.solve(items, variables, dict=True)
    return items[0]


def timeout(signum, frame): raise TimeoutError('Computation exceeded time limit')

if __name__ == '__main__':
    signal.signal(signal.SIGALRM, timeout)
    signal.alarm(15)
    try:
        if len(sys.argv) != 2: raise ValueError('Supply one expression')
        print(evaluate(sys.argv[1]))
    except Exception as exc:
        print(f'Error: {exc}', file=sys.stderr)
        sys.exit(1)
    finally:
        signal.alarm(0)
