# test_engine.py — literal English interpretation

Source blob: `854e1567ed8fcbd7bcd0ba75af6bba894e7ecb06` ([source](../test_engine.py)). The assertions below state what the tests check, not evidence that they have passed. Run make test to obtain current results.

### Line 1

```python
import unittest
```

Import Python's unittest testing framework.

### Line 2

```python
import sympy as s
```

Import SymPy under the local name s.

### Line 3

```python
from engine import evaluate, native
```

Import the evaluate function and the native shared-library handle from engine.

### Line 4

```python

```

Blank line; no executable operation.

### Line 5

```python
x, y = s.symbols('x y')
```

Create two symbolic variables named x and y and assign them to the two Python names x and y.

### Line 6

```python
class EngineTests(unittest.TestCase):
```

Define EngineTests as a subclass of unittest.TestCase; methods whose names start with test_ can be discovered as tests.

### Line 7

```python
    def test_native(self):
```

Define the native arithmetic test method.

### Line 8

```python
        self.assertIsNotNone(native)
```

Assert that the native shared-library handle is not None; fail if the library was not loaded.

### Line 9

```python
        self.assertEqual(evaluate('2+3*4'), 14)
```

Evaluate the string 2+3*4 and assert equality with 14, checking multiplication precedence.

### Line 10

```python
        self.assertEqual(evaluate('7-9'), -2)
```

Evaluate 7-9 and assert equality with negative two.

### Line 11

```python
        self.assertEqual(evaluate('9223372036854775807+1'), 2**63)
```

Evaluate the maximum signed 64-bit integer plus one and assert equality with two raised to the 63rd power; check overflow fallback.

### Line 12

```python
        self.assertEqual(evaluate('3037000500*3037000500'), 3037000500**2)
```

Evaluate the product of two copies of 3037000500 and assert equality with its exact Python integer square; check multiplication overflow fallback.

### Line 13

```python
    def test_arithmetic(self):
```

Define the arithmetic test method.

### Line 14

```python
        self.assertEqual(evaluate('-2^2'), -4)
```

Evaluate negative two squared and assert negative four; check that exponentiation binds more tightly than unary minus.

### Line 15

```python
        self.assertEqual(evaluate('2^3^2'), 512)
```

Evaluate two raised to three raised to two and assert 512; check right-associative exponentiation.

### Line 16

```python
        self.assertEqual(evaluate('1/3+1/6'), s.Rational(1,2))
```

Evaluate one third plus one sixth and assert equality with the exact rational one half.

### Line 17

```python
        self.assertEqual(evaluate('0.1+0.2'), s.Rational(3,10))
```

Evaluate decimal 0.1 plus decimal 0.2 and assert equality with the exact rational three tenths.

### Line 18

```python
        self.assertEqual(evaluate('5!'), 120)
```

Evaluate five factorial and assert equality with 120.

### Line 19

```python
    def test_algebra(self):
```

Define the algebra test method.

### Line 20

```python
        self.assertEqual(evaluate('2x+7=19'), s.FiniteSet(6))
```

Evaluate 2x+7=19 and assert equality with the finite solution set containing six.

### Line 21

```python
        self.assertEqual(evaluate('x^2-5x+6=0'), s.FiniteSet(2,3))
```

Evaluate the quadratic equation x squared minus five x plus six equals zero and assert the finite set containing two and three.

### Line 22

```python
        self.assertEqual(evaluate('x+y=10;x-y=2'), [{x:6,y:4}])
```

Evaluate the two simultaneous equations separated by a semicolon and assert equality with a one-element list containing a dictionary mapping x to six and y to four.

### Line 23

```python
        self.assertEqual(evaluate('factor(x^2-9)'), (x-3)*(x+3))
```

Evaluate the factorization of x squared minus nine and assert structural equality with the product (x-3)(x+3).

### Line 24

```python
        self.assertEqual(evaluate('x^2+1=0'), s.FiniteSet(-s.I,s.I))
```

Evaluate x squared plus one equals zero and assert equality with the finite set containing negative i and positive i.

### Line 25

```python
        self.assertEqual(evaluate('2x+1>5').as_set(), s.Interval.open(2,s.oo))
```

Evaluate the inequality 2x+1>5, convert the returned relation to a set, and assert equality with the open interval from two to positive infinity.

### Line 26

```python
    def test_calculus(self):
```

Define the calculus test method.

### Line 27

```python
        self.assertEqual(evaluate('diff(x^3+2x,x)'), 3*x*x+2)
```

Evaluate the derivative of x cubed plus two x with respect to x and assert equality with three x squared plus two.

### Line 28

```python
        self.assertEqual(evaluate('integrate(x^2,x,0,3)'), 9)
```

Evaluate the definite integral of x squared with respect to x from zero to three and assert nine.

### Line 29

```python
        self.assertEqual(evaluate('limit(sin(x)/x,x,0)'), 1)
```

Evaluate the limit of sine of x divided by x as x approaches zero and assert one.

### Line 30

```python
        self.assertEqual(evaluate('sum(x,x,1,100)'), 5050)
```

Evaluate the sum of x from one through one hundred and assert 5050.

### Line 31

```python
        self.assertEqual(evaluate('gradient(x^2+y^2,[x,y])'), s.Matrix([2*x,2*y]))
```

Evaluate the gradient of x squared plus y squared with respect to the ordered variables x and y; assert equality with the column matrix of two x and two y.

### Line 32

```python
    def test_linear_algebra(self):
```

Define the linear algebra test method.

### Line 33

```python
        self.assertEqual(evaluate('det([[1,2],[3,4]])'), -2)
```

Evaluate the determinant of the two-by-two matrix with rows [1,2] and [3,4] and assert negative two.

### Line 34

```python
        self.assertEqual(evaluate('matrix([[1,2],[3,4]])*matrix([[1,0],[0,1]])'), s.Matrix([[1,2],[3,4]]))
```

Evaluate that matrix times the two-by-two identity matrix and assert equality with the original matrix.

### Line 35

```python
    def test_other(self):
```

Define the test method for other mathematical functions.

### Line 36

```python
        self.assertEqual(evaluate('sin(pi/2)'), 1)
```

Evaluate sine of pi divided by two radians and assert one.

### Line 37

```python
        self.assertEqual(evaluate('gcd(48,18)'), 6)
```

Evaluate the greatest common divisor of 48 and 18 and assert six.

### Line 38

```python
        self.assertEqual(evaluate('mean([2,4,6])'), 4)
```

Evaluate the arithmetic mean of two, four and six and assert four.

### Line 39

```python
        self.assertEqual(evaluate('binomial_pmf(5,2,1/2)'), s.Rational(5,16))
```

Evaluate the probability of exactly two successes in five Bernoulli trials with success probability one half and assert the rational five sixteenths.

### Line 40

```python
        self.assertEqual(evaluate('normal_cdf(0)'), s.Rational(1,2))
```

Evaluate the standard normal cumulative distribution at zero and assert the rational one half.

### Line 41

```python
        self.assertTrue(evaluate('isprime(97)'))
```

Evaluate whether 97 is prime and assert that the returned value is truthy.

### Line 42

```python
    def test_reject(self):
```

Define the invalid-input test method.

### Line 43

```python
        with self.assertRaises(ValueError): evaluate('__import__("os")')
```

Enter a context that expects a ValueError; attempt to evaluate the literal text containing an import call and quotes. The test passes only if the expected exception is raised.

### Line 44

```python
        with self.assertRaises(ValueError): evaluate('2+')
```

Enter another context expecting ValueError; evaluate the incomplete expression 2+ to check malformed-input rejection.

### Line 45

```python
if __name__ == '__main__': unittest.main()
```

If this file is executed directly, call unittest.main to discover and run the tests and report the results.

