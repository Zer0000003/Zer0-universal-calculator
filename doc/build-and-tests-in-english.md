# Build and tests — Literal English Pseudocode (LEP)

Translation convention: [Literal English Pseudocode (LEP) standard](LEP-Standard.md).

Sources: Makefile (4da98ddb183dda2723350ae508b1e08c6a024591), test_engine.py (854e1567ed8fcbd7bcd0ba75af6bba894e7ecb06).

## Makefile

~~~text
If compiler variable is not defined:
    Set compiler to GCC.

Declare all, clean and test as phony targets.

Target all:
    Require calculator and libinteger_math.so.

Target calculator:
    Require calculator.s.
    Call compiler with output named current target
        and first prerequisite as input.

Target libinteger_math.so:
    Require integer_math.s.
    Call compiler with shared library and position-independent-code options,
        output named current target and first prerequisite as input.

Target test:
    Require all.
    Execute Python three with test_engine.py.

Target clean:
    Remove calculator and libinteger_math.so without prompting
        or error for nonexistent files.
~~~

## test_engine.py

~~~text
Import unit testing.
Import symbolic mathematics as s.
From engine import evaluate and native.

Set x and y to symbolic variables named x and y.

Class EngineTests inherits unit testing TestCase:

    Function test_native with self:
        Assert native is not nothing.
        Assert evaluate of "2+3*4" equals fourteen.
        Assert evaluate of "7-9" equals negative two.
        Assert evaluate of "9223372036854775807+1" equals two to the sixty-third power.
        Assert evaluate of "3037000500*3037000500" equals 3037000500 squared.

    Function test_arithmetic with self:
        Assert evaluate of "-2^2" equals negative four.
        Assert evaluate of "2^3^2" equals five hundred twelve.
        Assert evaluate of "1/3+1/6" equals symbolic rational one half.
        Assert evaluate of "0.1+0.2" equals symbolic rational three tenths.
        Assert evaluate of "5!" equals one hundred twenty.

    Function test_algebra with self:
        Assert evaluate of "2x+7=19" equals finite set containing six.
        Assert evaluate of "x^2-5x+6=0" equals finite set containing two and three.
        Assert evaluate of "x+y=10;x-y=2" equals list containing
            dictionary mapping x to six and y to four.
        Assert evaluate of "factor(x^2-9)" equals
            product of x minus three and x plus three.
        Assert evaluate of "x^2+1=0" equals finite set of negative imaginary unit
            and positive imaginary unit.
        Assert set of evaluate of "2x+1>5" equals open interval
            from two to positive infinity.

    Function test_calculus with self:
        Assert evaluate of "diff(x^3+2x,x)" equals three x squared plus two.
        Assert evaluate of "integrate(x^2,x,0,3)" equals nine.
        Assert evaluate of "limit(sin(x)/x,x,0)" equals one.
        Assert evaluate of "sum(x,x,1,100)" equals five thousand fifty.
        Assert evaluate of "gradient(x^2+y^2,[x,y])" equals column matrix
            containing twice x and twice y.

    Function test_linear_algebra with self:
        Assert evaluate of "det([[1,2],[3,4]])" equals negative two.
        Assert evaluate of "matrix([[1,2],[3,4]])*matrix([[1,0],[0,1]])"
            equals matrix with rows one and two, three and four.

    Function test_other with self:
        Assert evaluate of "sin(pi/2)" equals one.
        Assert evaluate of "gcd(48,18)" equals six.
        Assert evaluate of "mean([2,4,6])" equals four.
        Assert evaluate of "binomial_pmf(5,2,1/2)" equals symbolic rational five sixteenths.
        Assert evaluate of "normal_cdf(0)" equals symbolic rational one half.
        Assert evaluate of "isprime(97)" is true.

    Function test_reject with self:
        Within context requiring a value error:
            Evaluate the literal string '__import__("os")'.
        Within context requiring a value error:
            Evaluate the literal string "2+".

If this file is the main script:
    Call unit testing main.
~~~

## Function and build words

| Source | English |
|---|---|
| assertEqual | assert equality |
| assertIsNotNone | assert not nothing |
| assertTrue | assert truth |
| assertRaises | require exception |
| with | within context |
| TestCase | test case |
| unittest.main | run unit tests |
| CC | compiler command |
| ?= | assign only if undefined |
| .PHONY | declare non-file target |
| $@ | current target |
| $< | first prerequisite |
| -o | output filename |
| -shared | produce shared library |
| -fPIC | request position-independent code |
| rm -f | remove without prompting or missing-file error |
