import unittest
import sympy as s
from engine import evaluate, native

x, y = s.symbols('x y')
class EngineTests(unittest.TestCase):
    def test_native(self):
        self.assertIsNotNone(native)
        self.assertEqual(evaluate('2+3*4'), 14)
        self.assertEqual(evaluate('7-9'), -2)
        self.assertEqual(evaluate('9223372036854775807+1'), 2**63)
        self.assertEqual(evaluate('3037000500*3037000500'), 3037000500**2)
    def test_arithmetic(self):
        self.assertEqual(evaluate('-2^2'), -4)
        self.assertEqual(evaluate('2^3^2'), 512)
        self.assertEqual(evaluate('1/3+1/6'), s.Rational(1,2))
        self.assertEqual(evaluate('0.1+0.2'), s.Rational(3,10))
        self.assertEqual(evaluate('5!'), 120)
    def test_algebra(self):
        self.assertEqual(evaluate('2x+7=19'), s.FiniteSet(6))
        self.assertEqual(evaluate('x^2-5x+6=0'), s.FiniteSet(2,3))
        self.assertEqual(evaluate('x+y=10;x-y=2'), [{x:6,y:4}])
        self.assertEqual(evaluate('factor(x^2-9)'), (x-3)*(x+3))
        self.assertEqual(evaluate('x^2+1=0'), s.FiniteSet(-s.I,s.I))
        self.assertEqual(evaluate('2x+1>5').as_set(), s.Interval.open(2,s.oo))
    def test_calculus(self):
        self.assertEqual(evaluate('diff(x^3+2x,x)'), 3*x*x+2)
        self.assertEqual(evaluate('integrate(x^2,x,0,3)'), 9)
        self.assertEqual(evaluate('limit(sin(x)/x,x,0)'), 1)
        self.assertEqual(evaluate('sum(x,x,1,100)'), 5050)
        self.assertEqual(evaluate('gradient(x^2+y^2,[x,y])'), s.Matrix([2*x,2*y]))
    def test_linear_algebra(self):
        self.assertEqual(evaluate('det([[1,2],[3,4]])'), -2)
        self.assertEqual(evaluate('matrix([[1,2],[3,4]])*matrix([[1,0],[0,1]])'), s.Matrix([[1,2],[3,4]]))
    def test_other(self):
        self.assertEqual(evaluate('sin(pi/2)'), 1)
        self.assertEqual(evaluate('gcd(48,18)'), 6)
        self.assertEqual(evaluate('mean([2,4,6])'), 4)
        self.assertEqual(evaluate('binomial_pmf(5,2,1/2)'), s.Rational(5,16))
        self.assertEqual(evaluate('normal_cdf(0)'), s.Rational(1,2))
        self.assertTrue(evaluate('isprime(97)'))
    def test_reject(self):
        with self.assertRaises(ValueError): evaluate('__import__("os")')
        with self.assertRaises(ValueError): evaluate('2+')
if __name__ == '__main__': unittest.main()
