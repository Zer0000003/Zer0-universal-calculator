# engine.py — literal English interpretation

Source blob: `fa9427b42c69c70d5e5680a9df4b470c86eaa3a7` ([source](../engine.py)). Every physical source line is preserved below. Python indentation determines which block executes. Definitions create functions or classes; their bodies execute when called, not merely when defined. Multiline expressions form one statement; their individual lines are still annotated separately. Blank lines are identified explicitly. SymPy library internals are external dependencies, not code implemented in this repository.

### Line 1

```python
"""Restricted mathematical grammar; no eval, exec, or shell interpolation."""
```

Declare the module docstring describing the restricted mathematical grammar; this is documentation, not an enforcement mechanism.

### Line 2

```python
import ctypes
```

Import ctypes to call compiled C-ABI functions from Python.

### Line 3

```python
import re
```

Import the regular-expression module.

### Line 4

```python
import signal
```

Import the operating-system signal interface.

### Line 5

```python
import sys
```

Import sys to access command-line arguments, standard error and process exit.

### Line 6

```python
from pathlib import Path
```

Import the Path class from pathlib for filesystem path construction.

### Line 7

```python
import sympy as s
```

Import SymPy and bind the module to the shorter name s.

### Line 8

```python

```

Blank line; separates code visually and performs no operation.

### Line 9

```python
try:
```

Begin a block that catches a failure to load the shared library.

### Line 10

```python
    native = ctypes.CDLL(str(Path(__file__).with_name('libinteger_math.so').resolve()))
```

Construct the path to libinteger_math.so beside this Python file, resolve it to an absolute path, convert it to a string, load it as a shared library and assign the handle to native.

### Line 11

```python
    for name in ('math_add', 'math_sub', 'math_mul'):
```

For each of the three listed native function names, execute the indented block.

### Line 12

```python
        fn = getattr(native, name)
```

Retrieve the named function from the loaded library and assign it to fn.

### Line 13

```python
        fn.argtypes = [ctypes.c_int64, ctypes.c_int64, ctypes.POINTER(ctypes.c_int64)]
```

Set the foreign-function argument types to two signed 64-bit integers and a pointer to a signed 64-bit integer.

### Line 14

```python
        fn.restype = ctypes.c_int
```

Set the function's return type to a C int, which holds the success or overflow status.

### Line 15

```python
except OSError:
```

If an OSError occurs in the try block, execute this handler.

### Line 16

```python
    native = None
```

Set native to None, disabling native dispatch and allowing symbolic fallback.

### Line 17

```python

```

Blank line; separates code visually and performs no operation.

### Line 18

```python

```

Blank line; separates code visually and performs no operation.

### Line 19

```python
def arithmetic(op, a, b):
```

Define arithmetic with parameters op (operator), a (left operand) and b (right operand).

### Line 20

```python
    if op in ('+', '-', '*') and native and isinstance(a, s.Integer) and isinstance(b, s.Integer):
```

Enter the native branch only when the operator is addition, subtraction or multiplication, the library handle is truthy and both operands are SymPy Integer objects.

### Line 21

```python
        if all(-(1 << 63) <= int(v) < (1 << 63) for v in (a, b)):
```

Convert each operand to a Python integer and check that every value is at least negative 2 to the power of 63 and strictly less than positive 2 to the power of 63; 1 shifted left by 63 computes that power.

### Line 22

```python
            result = ctypes.c_int64()
```

Allocate a signed 64-bit ctypes integer initialized to zero as the result storage.

### Line 23

```python
            fn = getattr(native, {'+':'math_add', '-':'math_sub', '*':'math_mul'}[op])
```

Look up the Assembly function name for op in the dictionary, retrieve that function from native and assign it to fn.

### Line 24

```python
            if fn(int(a), int(b), ctypes.byref(result)) == 0:
```

Call fn with the converted integer operands and a reference to result; enter the next block only if its return status equals zero.

### Line 25

```python
                return s.Integer(result.value)
```

Read the stored result.value, construct a SymPy Integer from it and return immediately.

### Line 26

```python
    if op == '+': return a + b
```

If op is plus, return the sum of a and b using their Python/SymPy arithmetic behavior.

### Line 27

```python
    if op == '-': return a - b
```

If op is minus, return a minus b.

### Line 28

```python
    if op == '*': return a * b
```

If op is multiplication, return a multiplied by b.

### Line 29

```python
    if op == '/': return a / b
```

If op is division, return a divided by b.

### Line 30

```python
    if op == '^': return a ** b
```

If op is caret, return a raised to the power b using Python's exponentiation operator.

### Line 31

```python
    if op == '=': return s.Eq(a, b, evaluate=False)
```

If op is equals, construct and return a SymPy equality between a and b without automatically evaluating it to a Boolean.

### Line 32

```python
    if op in ('<', '>', '<=', '>=', '!='):
```

If op is any of the five listed comparison operators, enter the following block.

### Line 33

```python
        return {'<': s.Lt, '>': s.Gt, '<=': s.Le, '>=': s.Ge, '!=': s.Ne}[op](a, b, evaluate=False)
```

Select the corresponding SymPy comparison constructor (less than, greater than, less than or equal, greater than or equal, not equal), call it with a, b and evaluate=False, then return the relation.

### Line 34

```python
    raise ValueError('Unknown operator')
```

If no earlier branch returned a value, raise a ValueError with the given message.

### Line 35

```python

```

Blank line; separates code visually and performs no operation.

### Line 36

```python

```

Blank line; separates code visually and performs no operation.

### Line 37

```python
def solve(*args):
```

Define solve with a variable number of positional arguments, collected into args.

### Line 38

```python
    return s.solve(*args)
```

Unpack args as separate positional arguments to SymPy solve and return its result.

### Line 39

```python

```

Blank line; separates code visually and performs no operation.

### Line 40

```python

```

Blank line; separates code visually and performs no operation.

### Line 41

```python
def determinant(a): return s.Matrix(a).det()
```

Define determinant with argument a; convert a into a SymPy Matrix, call its determinant method and return the result.

### Line 42

```python
def inverse(a): return s.Matrix(a).inv()
```

Define inverse with argument a; construct a Matrix from a, call its inverse method and return the result.

### Line 43

```python
def eigenvalues(a): return s.Matrix(a).eigenvals()
```

Define eigenvalues with argument a; construct a Matrix, call eigenvals and return its eigenvalue-to-multiplicity mapping.

### Line 44

```python
def rref(a): return s.Matrix(a).rref()
```

Define rref with argument a; construct a Matrix, call its reduced-row-echelon-form method and return the matrix and pivot-column indices.

### Line 45

```python
def approx(a, digits=15): return s.N(a, int(digits))
```

Define approx with a and an optional digits parameter defaulting to 15; convert digits to int and call SymPy N to request that many significant decimal digits, then return the approximation.

### Line 46

```python
def summation(a, var, low, high): return s.summation(a, (var, low, high))
```

Define summation with expression a, variable var and lower and upper bounds; pass the expression and a tuple containing the variable and bounds to SymPy summation, then return the result.

### Line 47

```python
def product(a, var, low, high): return s.product(a, (var, low, high))
```

Define product with the same four arguments; pass expression and bounds tuple to SymPy product and return the result.

### Line 48

```python
def mean(values): return sum(values) / s.Integer(len(values))
```

Define mean with a sequence values; sum its elements with Python sum, divide by its length converted to a SymPy Integer and return the arithmetic mean.

### Line 49

```python
def variance(values):
```

Define variance with parameter values.

### Line 50

```python
    m = mean(values)
```

Call mean on values and bind the returned mean to m.

### Line 51

```python
    return sum((v-m)**2 for v in values) / s.Integer(len(values))
```

For each v in values compute the square of v minus m, sum those squares, divide by the number of values as a SymPy Integer and return the population variance.

### Line 52

```python
def binomial_pmf(n, k, p): return s.binomial(n, k)*p**k*(1-p)**(n-k)
```

Define binomial_pmf with trials n, successes k and success probability p; return the binomial coefficient n choose k multiplied by p to the k and (1-p) to the (n-k). The wrapper does not validate the probability or count domain.

### Line 53

```python
def normal_cdf(x, mu=0, sigma=1): return (1+s.erf((x-mu)/(sigma*s.sqrt(2))))/2
```

Define normal_cdf with x, mean mu defaulting to zero and standard deviation sigma defaulting to one; return one plus the error function of (x-mu) divided by sigma times square root of two, all divided by two. No positive-sigma check is made here.

### Line 54

```python
def gradient(expr, variables): return s.Matrix([s.diff(expr, v) for v in variables])
```

Define gradient; for each variable v differentiate expr with respect to v, collect the results in a list, convert the list into a column Matrix and return it.

### Line 55

```python
def jacobian(expressions, variables): return s.Matrix(expressions).jacobian(variables)
```

Define jacobian; convert expressions into a Matrix, call its jacobian method with variables and return the resulting matrix of partial derivatives.

### Line 56

```python
def integral(a, var, *bounds):
```

Define integral with expression a, variable var and any additional positional arguments collected in bounds.

### Line 57

```python
    if not bounds: return s.integrate(a, var)
```

If bounds is empty, call SymPy integrate on a and var and return the indefinite integral (no arbitrary constant is appended).

### Line 58

```python
    if len(bounds) == 2: return s.integrate(a, (var, *bounds))
```

If there are exactly two bounds, create the tuple (var, lower, upper) by unpacking bounds, call integrate with a and that tuple, and return the definite integral.

### Line 59

```python
    raise ValueError('integrate(expr, variable[, lower, upper])')
```

Otherwise raise ValueError with the supported input signature.

### Line 60

```python

```

Blank line; separates code visually and performs no operation.

### Line 61

```python
FUNCTIONS = {n: getattr(s, n) for n in (
```

Start a dictionary comprehension: for each function name n in the following tuple, use n as the key and getattr(s,n) as the value, retrieving the corresponding SymPy callable.

### Line 62

```python
    'sin', 'cos', 'tan', 'asin', 'acos', 'atan', 'sinh', 'cosh', 'tanh',
```

Include sine, cosine, tangent, their listed inverse trigonometric functions, and hyperbolic sine, cosine and tangent in the allowed name tuple.

### Line 63

```python
    'sqrt', 'exp', 'log', 'Abs', 'factorial', 'binomial', 'simplify',
```

Include square root, exponential, logarithm, absolute value, factorial, binomial coefficient and simplification in that tuple.

### Line 64

```python
    'factor', 'expand', 'cancel', 'together', 'apart', 'diff', 'limit',
```

Include factoring, expansion, cancellation, common-denominator combination, partial fractions, differentiation and limits.

### Line 65

```python
    'series', 'gcd', 'lcm', 'isprime', 'factorint', 'dsolve', 'laplace_transform',
```

Include series expansion, greatest common divisor, least common multiple, primality testing, integer factorization, differential-equation solving and Laplace transforms.

### Line 66

```python
    'inverse_laplace_transform', 'linsolve', 'nonlinsolve', 'nsolve', 'floor', 'ceiling',
```

Include inverse Laplace transforms, linear and nonlinear system solvers, numerical solving, floor and ceiling.

### Line 67

```python
    're', 'im', 'conjugate', 'gamma', 'erf', 'zeta', 'mod_inverse', 'root')}
```

Include real and imaginary part extraction, conjugation, gamma, error and zeta functions, modular inverse and roots; close the tuple and dictionary comprehension.

### Line 68

```python
FUNCTIONS.update(solve=solve, integrate=integral, matrix=s.Matrix, det=determinant,
```

Begin updating FUNCTIONS with named wrapper callables and the Matrix constructor: solve, integrate, matrix and det.

### Line 69

```python
    inverse=inverse, eigenvalues=eigenvalues, rref=rref, approx=approx,
```

Register inverse, eigenvalues, rref and approx under their corresponding input names.

### Line 70

```python
    sum=summation, product=product, ln=s.log, abs=s.Abs, mean=mean, variance=variance,
```

Register summation as sum, product as product, natural log as ln, absolute value as abs, and the mean and variance wrappers.

### Line 71

```python
    binomial_pmf=binomial_pmf, normal_cdf=normal_cdf, gradient=gradient, jacobian=jacobian)
```

Register binomial_pmf, normal_cdf, gradient and jacobian; close the update call.

### Line 72

```python
CONSTANTS = {'pi': s.pi, 'e': s.E, 'E': s.E, 'I': s.I, 'i': s.I, 'oo': s.oo, 'inf': s.oo}
```

Build a dictionary mapping the input names pi, e/E, I/i and oo/inf to SymPy's pi, Euler's number, imaginary unit and infinity objects.

### Line 73

```python
TOKEN = re.compile(r'\s*(?:(\d+(?:\.\d*)?|\.\d+)(?:([eE][+-]?\d+))?|([A-Za-z_][A-Za-z_0-9]*)|(\*\*|<=|>=|!=|[+\-*/^=<>(),;\[\]!]))')
```

Compile a regular expression for tokenization: skip whitespace, then match a decimal/integer number with optional scientific exponent, or an identifier beginning with an ASCII letter or underscore followed by letters/digits/underscores, or one supported operator or delimiter. The four capture groups hold the number, exponent, identifier and operator respectively. Longer operators such as ** and <= are checked before single-character ones.

### Line 74

```python

```

Blank line; separates code visually and performs no operation.

### Line 75

```python

```

Blank line; separates code visually and performs no operation.

### Line 76

```python
class Parser:
```

Define a class named Parser to hold tokens and the current reading position.

### Line 77

```python
    def __init__(self, source):
```

Define the constructor taking the instance self and input string source.

### Line 78

```python
        source = source.strip().replace('−', '-').replace('×', '*').replace('÷', '/').replace('π', 'pi').replace('∞', 'oo').replace('²', '^2').replace('³', '^3')
```

Strip leading/trailing whitespace, then sequentially replace Unicode minus, multiplication, division, pi, infinity, superscript two and superscript three with their listed ASCII forms; assign the normalized string back to source.

### Line 79

```python
        if len(source) > 4096: raise ValueError('Input too long')
```

If the normalized string contains more than 4096 characters, raise ValueError.

### Line 80

```python
        self.tokens = []
```

Create an empty list on this instance named tokens.

### Line 81

```python
        pos = 0
```

Initialize local character position pos to zero.

### Line 82

```python
        while pos < len(source):
```

Repeat while pos is less than the length of source.

### Line 83

```python
            m = TOKEN.match(source, pos)
```

Attempt to match the compiled token pattern at pos and store the match object or None in m.

### Line 84

```python
            if not m: raise ValueError(f'Invalid character at position {pos+1}')
```

If no match exists, raise ValueError reporting the one-based current position.

### Line 85

```python
            num, exponent, name, op = m.groups()
```

Unpack the four regex capture groups into num, exponent, name and op.

### Line 86

```python
            if num: self.tokens.append(('num', num + (exponent or '')))
```

If num is truthy, append a pair containing the kind num and the number text concatenated with the exponent text or an empty string when no exponent exists.

### Line 87

```python
            elif name: self.tokens.append(('name', name))
```

Otherwise, if name is truthy, append a pair containing kind name and the identifier text.

### Line 88

```python
            else: self.tokens.append(('op', '^' if op == '**' else op))
```

Otherwise append a pair containing kind op and the operator text, normalizing double asterisk to caret.

### Line 89

```python
            pos = m.end()
```

Set pos to the end index of the match so the next iteration scans the next token.

### Line 90

```python
        self.tokens.append(('end', ''))
```

Append a special end token with an empty value after all input has been scanned.

### Line 91

```python
        self.i = 0
```

Set the instance token index i to zero.

### Line 92

```python

```

Blank line; separates code visually and performs no operation.

### Line 93

```python
    def peek(self): return self.tokens[self.i]
```

Define peek to return the token at self.i without advancing the index.

### Line 94

```python
    def take(self):
```

Define take to retrieve and consume the next token.

### Line 95

```python
        token = self.peek()
```

Call peek and store the current token in the local variable token.

### Line 96

```python
        self.i += 1
```

Add one to the instance token index.

### Line 97

```python
        return token
```

Return the previously saved token.

### Line 98

```python
    def accept(self, value):
```

Define accept with the expected token text value.

### Line 99

```python
        if self.peek()[1] == value:
```

Read the current token's second tuple element and compare it to value.

### Line 100

```python
            self.take()
```

If equal, call take to advance past the matching token; discard its return value.

### Line 101

```python
            return True
```

Return True to report the successful match.

### Line 102

```python
        return False
```

If the comparison was false, return False without consuming the token.

### Line 103

```python
    def expect(self, value):
```

Define expect with a required token text value.

### Line 104

```python
        if not self.accept(value): raise ValueError(f'Expected {value}')
```

Call accept; if it returns False, raise ValueError containing the missing expected token text.

### Line 105

```python
    def sequence(self, end):
```

Define sequence with the closing delimiter text end.

### Line 106

```python
        items = []
```

Create an empty local list named items.

### Line 107

```python
        if not self.accept(end):
```

Try consuming the closing delimiter immediately; only if it is absent, enter the nonempty-list branch.

### Line 108

```python
            items.append(self.expr())
```

Parse one expression and append the returned value to items.

### Line 109

```python
            while self.accept(','): items.append(self.expr())
```

While a comma can be consumed, parse another expression and append it.

### Line 110

```python
            self.expect(end)
```

Require and consume the closing delimiter by calling expect.

### Line 111

```python
        return items
```

Return the collected items list (possibly empty).

### Line 112

```python
    def expr(self, min_bp=0):
```

Define expr with optional minimum binding power min_bp defaulting to zero; this is the recursive precedence parser.

### Line 113

```python
        kind, val = self.take()
```

Consume the next token and unpack its kind and value into kind and val.

### Line 114

```python
        if kind == 'num':
```

If the token kind is num, enter the numeric branch.

### Line 115

```python
            left = s.Rational(val)
```

Convert the token text to a SymPy Rational and assign it as the current left operand; this preserves exact decimal arithmetic.

### Line 116

```python
        elif kind == 'name':
```

Otherwise, if the token kind is name, enter the identifier branch.

### Line 117

```python
            if val in FUNCTIONS and self.accept('('):
```

Check that val is an allowed function name and then attempt to consume an opening parenthesis; enter the call branch only if both conditions succeed.

### Line 118

```python
                left = FUNCTIONS[val](*self.sequence(')'))
```

Parse the argument sequence through its closing parenthesis, unpack the list into positional arguments to the selected function, execute the function and bind its result to left.

### Line 119

```python
            else:
```

Otherwise enter the constant-or-symbol branch.

### Line 120

```python
                left = CONSTANTS.get(val, s.Symbol(val))
```

Construct a Symbol named val as the default argument to the dictionary lookup; return the mapped constant if present or that symbol otherwise, and assign it to left.

### Line 121

```python
        elif val in ('+', '-'):
```

Otherwise, if val is unary plus or minus, enter the prefix sign branch.

### Line 122

```python
            left = self.expr(25)
```

Recursively parse an expression with minimum binding power 25 and store its result as left; exponentiation at power 30 binds more tightly than the unary sign.

### Line 123

```python
            if val == '-': left = -left
```

If the original sign was minus, negate left and reassign it; unary plus leaves left unchanged.

### Line 124

```python
        elif val == '(':
```

Otherwise, if val is an opening parenthesis, enter the grouped-expression branch.

### Line 125

```python
            left = self.expr()
```

Recursively parse the inner expression with default minimum binding power and assign its result to left.

### Line 126

```python
            self.expect(')')
```

Require and consume a closing parenthesis.

### Line 127

```python
        elif val == '[':
```

Otherwise, if val is an opening square bracket, enter the list branch.

### Line 128

```python
            left = self.sequence(']')
```

Parse a sequence ending with a closing square bracket and assign the resulting Python list to left.

### Line 129

```python
        else:
```

If none of the recognized prefix forms matched, enter the error branch.

### Line 130

```python
            raise ValueError(f'Expected mathematical expression, found {val!r}')
```

Raise ValueError reporting the unexpected token using its repr representation.

### Line 131

```python
        while True:
```

Begin an indefinite loop to process postfix and infix operators following the left operand.

### Line 132

```python
            kind, val = self.peek()
```

Inspect the current token without consuming it and unpack its kind and value.

### Line 133

```python
            if val == '!':
```

If the token text is an exclamation mark, enter the factorial branch.

### Line 134

```python
                if 40 < min_bp: break
```

If factorial's binding power 40 is less than min_bp, break out of the loop without consuming the token.

### Line 135

```python
                self.take()
```

Consume the exclamation mark.

### Line 136

```python
                left = s.factorial(left)
```

Apply SymPy factorial to left and replace left with the returned value.

### Line 137

```python
                continue
```

Continue directly to the next loop iteration, skipping infix handling.

### Line 138

```python
            implicit = kind in ('num', 'name') or val == '('
```

Set implicit to True if the next token is a number, identifier or opening parenthesis, indicating implicit multiplication.

### Line 139

```python
            op = '*' if implicit else val
```

If implicit is True, assign multiplication to op; otherwise assign the actual token text.

### Line 140

```python
            binding = {'=':(2,3), '<':(2,3), '>':(2,3), '<=':(2,3), '>=':(2,3), '!=':(2,3), '+':(10,11), '-':(10,11), '*':(20,21), '/':(20,21), '^':(30,30)}.get(op)
```

Look up op in the binding-power dictionary. Comparisons have left/right powers 2/3, addition/subtraction 10/11, multiplication/division 20/21 and exponentiation 30/30. Missing operators return None. Equal powers for exponentiation make it right-associative.

### Line 141

```python
            if not binding or binding[0] < min_bp: break
```

If no binding exists or its left binding power is below min_bp, break out of the loop.

### Line 142

```python
            if not implicit: self.take()
```

If multiplication is not implicit, consume the actual operator token; otherwise leave the next operand token for recursion.

### Line 143

```python
            right = self.expr(binding[1])
```

Recursively parse the right operand using the operator's right binding power, then assign its value to right.

### Line 144

```python
            left = arithmetic(op, left, right)
```

Call arithmetic with op, the existing left operand and right operand; store its result back into left.

### Line 145

```python
        return left
```

After the loop ends, return the accumulated left value.

### Line 146

```python
    def parse(self):
```

Define parse, the method for parsing a whole input string after tokenization.

### Line 147

```python
        items = [self.expr()]
```

Parse the first expression and initialize items as a list containing its result.

### Line 148

```python
        while self.accept(';'): items.append(self.expr())
```

While a semicolon can be consumed, parse another expression and append it to items.

### Line 149

```python
        if self.peek()[0] != 'end': raise ValueError('Unexpected token: ' + self.peek()[1])
```

If the next token's kind is not end, raise ValueError with the unconsumed token's text.

### Line 150

```python
        return items
```

Return the list of parsed values.

### Line 151

```python

```

Blank line; separates code visually and performs no operation.

### Line 152

```python

```

Blank line; separates code visually and performs no operation.

### Line 153

```python
def evaluate(source):
```

Define evaluate with a source string parameter.

### Line 154

```python
    items = Parser(source).parse()
```

Construct a Parser from source, call its parse method and assign the resulting list to items.

### Line 155

```python
    if any(isinstance(v, s.core.relational.Relational) and not isinstance(v, s.Equality) for v in items):
```

Check whether any item is a SymPy Relational object that is not an Equality; if so, enter the inequality branch.

### Line 156

```python
        if not all(isinstance(v, s.core.relational.Relational) for v in items):
```

Check whether every item is a Relational; if not, enter the error branch.

### Line 157

```python
            raise ValueError('Enter only relations in an inequality system')
```

Raise ValueError because the inequality system contains a nonrelation.

### Line 158

```python
        variables = sorted(set().union(*(v.free_symbols for v in items)), key=str)
```

For each relation collect free_symbols, unpack those sets into a union starting from an empty set, sort the unique variables by their string representations and assign the list to variables.

### Line 159

```python
        return s.reduce_inequalities(items, variables)
```

Pass the relations and their variables to SymPy reduce_inequalities and return its result; unsupported multivariate inequalities can raise errors.

### Line 160

```python
    if len(items) > 1 or isinstance(items[0], s.Equality):
```

If there is more than one parsed item or the first item is an Equality, enter the equation-solving branch.

### Line 161

```python
        if not all(isinstance(v, s.Equality) for v in items):
```

Check whether all parsed items are Equality objects; if not, enter the error branch.

### Line 162

```python
            raise ValueError('Semicolon-separated inputs must all be equations')
```

Raise ValueError stating that semicolon-separated inputs must all be equations.

### Line 163

```python
        variables = sorted(set().union(*(v.free_symbols for v in items)), key=str)
```

Collect all free symbols from the equations into one set and sort them by their string representations.

### Line 164

```python
        if not variables:
```

If the variable list is empty, enter the constant-equation branch.

### Line 165

```python
            return all(s.simplify(v.lhs-v.rhs) == 0 for v in items)
```

For every equation subtract its right side from its left side, simplify the difference, test equality with zero and return True only if every such test succeeds.

### Line 166

```python
        if len(items) == 1 and len(variables) == 1:
```

If there is exactly one equation and exactly one variable, enter the single-variable branch.

### Line 167

```python
            return s.solveset(items[0], variables[0], domain=s.S.Complexes)
```

Call solveset with the equation, its variable and the complex-number domain; return the resulting solution set or unevaluated condition set.

### Line 168

```python
        return s.solve(items, variables, dict=True)
```

Otherwise call SymPy solve with all equations, all variables and dict=True; return its result (typically a list of solution dictionaries).

### Line 169

```python
    return items[0]
```

If no relation branch returned, return the first parsed item directly.

### Line 170

```python

```

Blank line; separates code visually and performs no operation.

### Line 171

```python

```

Blank line; separates code visually and performs no operation.

### Line 172

```python
def timeout(signum, frame): raise TimeoutError('Computation exceeded time limit')
```

Define the signal handler timeout with signal number and current frame parameters; immediately raise TimeoutError with the specified message when called.

### Line 173

```python

```

Blank line; separates code visually and performs no operation.

### Line 174

```python
if __name__ == '__main__':
```

If Python is running this file as the main script rather than importing it, execute the following command-line block.

### Line 175

```python
    signal.signal(signal.SIGALRM, timeout)
```

Register timeout as the handler for the SIGALRM signal.

### Line 176

```python
    signal.alarm(15)
```

Schedule an alarm signal after 15 seconds; it is not a hard resource sandbox.

### Line 177

```python
    try:
```

Begin the protected command-line evaluation block.

### Line 178

```python
        if len(sys.argv) != 2: raise ValueError('Supply one expression')
```

If sys.argv does not contain exactly two entries (script name and one argument), raise ValueError.

### Line 179

```python
        print(evaluate(sys.argv[1]))
```

Read the first user argument from sys.argv[1], evaluate it and print the resulting object to standard output.

### Line 180

```python
    except Exception as exc:
```

Catch an Exception raised inside the try block and bind that exception to exc.

### Line 181

```python
        print(f'Error: {exc}', file=sys.stderr)
```

Format an error string containing exc and print it to standard error rather than standard output.

### Line 182

```python
        sys.exit(1)
```

Exit the process with status code 1 by raising SystemExit through sys.exit.

### Line 183

```python
    finally:
```

Declare a finally block that executes on normal or exceptional exit from the try/except block.

### Line 184

```python
        signal.alarm(0)
```

Cancel the pending alarm by setting its remaining duration to zero.

