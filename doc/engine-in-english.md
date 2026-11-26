# Symbolic engine — Literal English Pseudocode (LEP)

Translation convention: [Literal English Pseudocode (LEP) standard](LEP-Standard.md).

Source: engine.py (fa9427b42c69c70d5e5680a9df4b470c86eaa3a7). This is the entire repository-owned Python engine rewritten as English pseudocode. Calls into SymPy retain their meaning; their external implementations are not reproduced.

~~~text
Import C-compatible foreign-function interface.
Import regular expressions.
Import operating-system signals.
Import system interface.
Import filesystem Path.
Import symbolic mathematics as s.

Try:
    Set native to load shared library at the resolved absolute path
        of libinteger_math.so beside this source file.
    For each name in math_add, math_sub, math_mul:
        Set function to attribute of native named name.
        Set function argument types to:
            signed sixty-four-bit integer,
            signed sixty-four-bit integer,
            pointer to signed sixty-four-bit integer.
        Set function return type to C integer.
If operating-system error:
    Set native to nothing.

Function arithmetic with operator, a, b:
    If operator is addition, subtraction or multiplication,
        and native exists,
        and a is a symbolic integer,
        and b is a symbolic integer:
        If every operand is at least negative two to the sixty-third power
            and less than positive two to the sixty-third power:
            Create result as a C signed sixty-four-bit integer.
            Set function to native attribute selected by operator:
                addition means math_add;
                subtraction means math_sub;
                multiplication means math_mul.
            If calling function with integer a, integer b
                and reference to result returns zero:
                Return symbolic integer of result value.
    If operator is addition: return a plus b.
    If operator is subtraction: return a minus b.
    If operator is multiplication: return a multiplied by b.
    If operator is division: return a divided by b.
    If operator is exponentiation: return a raised to b.
    If operator is equality: return unevaluated equality of a and b.
    If operator is less than, greater than, less than or equal,
        greater than or equal, or not equal:
        Select the corresponding symbolic relation constructor.
        Return that constructor called with a, b and evaluation disabled.
    Raise value error "Unknown operator".

Function solve with any number of arguments:
    Return symbolic solve called with all arguments unpacked.

Function determinant with a:
    Return determinant of matrix constructed from a.

Function inverse with a:
    Return inverse of matrix constructed from a.

Function eigenvalues with a:
    Return eigenvalues of matrix constructed from a.

Function rref with a:
    Return reduced row echelon form and pivot indices of matrix constructed from a.

Function approx with a and digits defaulting to fifteen:
    Return numerical approximation of a to integer digits significant digits.

Function summation with a, variable, lower bound, upper bound:
    Return symbolic summation of a over the tuple of variable and both bounds.

Function product with a, variable, lower bound, upper bound:
    Return symbolic product of a over the tuple of variable and both bounds.

Function mean with values:
    Return sum of values divided by symbolic integer of number of values.

Function variance with values:
    Set m to mean of values.
    Return sum of the squares of each value minus m
        divided by symbolic integer of number of values.

Function binomial_pmf with n, k, p:
    Return binomial coefficient of n and k multiplied by p raised to k
        multiplied by the quantity one minus p raised to the power of
        the quantity n minus k.

Function normal_cdf with x, mu defaulting to zero, sigma defaulting to one:
    Return the quantity one plus the error function of
        the quantity x minus mu divided by the product of sigma and square root of two,
        all divided by two.

Function gradient with expression and variables:
    Return matrix constructed from the list of derivatives of expression
        with respect to each variable in variables.

Function jacobian with expressions and variables:
    Return Jacobian with respect to variables of matrix constructed from expressions.

Function integral with a, variable, and any additional bounds:
    If bounds is empty: return symbolic integral of a with respect to variable.
    If length of bounds equals two:
        Return symbolic integral of a over tuple of variable and unpacked bounds.
    Raise value error "integrate(expr, variable[, lower, upper])".

Create FUNCTIONS as a dictionary:
    For each name in the following list,
        assign the symbolic mathematics attribute named name to key name:
        sin, cos, tan, asin, acos, atan, sinh, cosh, tanh,
        sqrt, exp, log, Abs, factorial, binomial, simplify,
        factor, expand, cancel, together, apart, diff, limit,
        series, gcd, lcm, isprime, factorint, dsolve, laplace_transform,
        inverse_laplace_transform, linsolve, nonlinsolve, nsolve, floor, ceiling,
        re, im, conjugate, gamma, erf, zeta, mod_inverse, root.

Update FUNCTIONS:
    solve means solve.
    integrate means integral.
    matrix means symbolic Matrix.
    det means determinant.
    inverse means inverse.
    eigenvalues means eigenvalues.
    rref means reduced row echelon form.
    approx means numerical approximation.
    sum means summation.
    product means product.
    ln means symbolic logarithm.
    abs means symbolic absolute value.
    mean means mean.
    variance means variance.
    binomial_pmf means binomial probability mass function.
    normal_cdf means normal cumulative distribution function.
    gradient means gradient.
    jacobian means Jacobian.

Create CONSTANTS as a dictionary:
    pi means symbolic pi.
    e and E mean Euler's number.
    I and i mean imaginary unit.
    oo and inf mean positive infinity.

Compile TOKEN as regular expression:
    Match zero or more whitespace characters, then one of:
        Capture a number:
            one or more digits optionally followed by a decimal point
            and zero or more digits,
            or a decimal point followed by one or more digits.
            Optionally capture a scientific exponent:
                e or E followed by optional plus or minus and one or more digits.
        Or capture an identifier:
            ASCII letter or underscore followed by zero or more
            ASCII letters, digits or underscores.
        Or capture an operator:
            double asterisk, less than or equal, greater than or equal, not equal,
            or one character from plus, minus, asterisk, slash, caret,
            equals, less than, greater than, parentheses, comma,
            semicolon, square brackets, exclamation mark.

Class Parser:

    Constructor with self and source:
        Set source to source stripped of surrounding whitespace,
            replacing Unicode minus with hyphen,
            multiplication sign with asterisk,
            division sign with slash,
            pi symbol with pi,
            infinity symbol with oo,
            superscript two with caret two,
            superscript three with caret three.
        If length of source is greater than four thousand ninety-six:
            Raise value error "Input too long".
        Set self.tokens to empty list.
        Set pos to zero.
        While pos is less than length of source:
            Set match to TOKEN matched against source beginning at pos.
            If match does not exist:
                Raise value error with "Invalid character at position"
                    followed by pos plus one.
            Unpack match groups into number, exponent, name, operator.
            If number is present:
                Append tuple of "num" and number plus exponent or empty string
                    to self.tokens.
            Otherwise if name is present:
                Append tuple of "name" and name to self.tokens.
            Otherwise:
                Append tuple of "op" and caret if operator is double asterisk,
                    otherwise operator, to self.tokens.
            Set pos to ending index of match.
        Append tuple of "end" and empty string to self.tokens.
        Set self.i to zero.

    Function peek with self:
        Return self.tokens at index self.i.

    Function take with self:
        Set token to the result of calling self.peek.
        Increase self.i by one.
        Return token.

    Function accept with self and value:
        If second element of the result of calling self.peek equals value:
            Call self.take.
            Return true.
        Return false.

    Function expect with self and value:
        If self.accept called with value returns false:
            Raise value error "Expected" followed by value.

    Function sequence with self and end:
        Set items to empty list.
        If self.accept called with end returns false:
            Append result of calling self.expr to items.
            While self.accept called with comma returns true:
                Append result of self.expr to items.
            Call self.expect with end.
        Return items.

    Function expr with self and minimum binding power defaulting to zero:
        Unpack result of calling self.take into kind and value.

        If kind equals "num":
            Set left to symbolic rational of value.
        Otherwise if kind equals "name":
            If value exists in FUNCTIONS and self.accept opening parenthesis:
                Set left to function in FUNCTIONS at key value,
                    called with unpacked result of self.sequence
                    ending at closing parenthesis.
            Otherwise:
                Set left to CONSTANTS at key value,
                    with symbolic variable named value as default.
        Otherwise if value is plus or minus:
            Set left to self.expr with minimum binding power twenty-five.
            If value equals minus: set left to negative left.
        Otherwise if value equals opening parenthesis:
            Set left to the result of calling self.expr.
            Call self.expect with closing parenthesis.
        Otherwise if value equals opening square bracket:
            Set left to self.sequence ending with closing square bracket.
        Otherwise:
            Raise value error "Expected mathematical expression, found"
                followed by representation of value.

        Repeat indefinitely:
            Unpack result of calling self.peek into kind and value.
            If value equals exclamation mark:
                If forty is less than minimum binding power: break.
                Call self.take.
                Set left to factorial of left.
                Continue to next repetition.

            Set implicit to whether kind is "num" or "name"
                or value equals opening parenthesis.
            Set operator to multiplication if implicit, otherwise value.
            Look up binding in the following dictionary:
                equality: left two, right three.
                less than: left two, right three.
                greater than: left two, right three.
                less than or equal: left two, right three.
                greater than or equal: left two, right three.
                not equal: left two, right three.
                addition: left ten, right eleven.
                subtraction: left ten, right eleven.
                multiplication: left twenty, right twenty-one.
                division: left twenty, right twenty-one.
                exponentiation: left thirty, right thirty.
                No matching operator: nothing.
            If binding does not exist or its left power is less than
                minimum binding power: break.
            If not implicit: call self.take.
            Set right to self.expr with minimum binding power
                equal to binding's right power.
            Set left to arithmetic called with operator, left and right.
        Return left.

    Function parse with self:
        Set items to list containing result of calling self.expr.
        While self.accept semicolon returns true:
            Append result of self.expr to items.
        If first element of the result of calling self.peek is not "end":
            Raise value error "Unexpected token" followed by
                second element of self.peek.
        Return items.

Function evaluate with source:
    Set items to result of parsing a new Parser constructed from source.
    If any item in items is a symbolic relation but not a symbolic equality:
        If not every item in items is a symbolic relation:
            Raise value error "Enter only relations in an inequality system".
        Set variables to union of free symbols of every item,
            sorted by string representation.
        Return symbolic reduce inequalities with items and variables.
    If length of items is greater than one or first item is a symbolic equality:
        If not every item in items is a symbolic equality:
            Raise value error "Semicolon-separated inputs must all be equations".
        Set variables to union of free symbols of every item,
            sorted by string representation.
        If variables is empty:
            Return whether for every item the simplified difference
                of its left side and right side equals zero.
        If length of items equals one and length of variables equals one:
            Return symbolic solve set of first item for first variable
                in the complex number domain.
        Return symbolic solve with items, variables and dictionary output enabled.
    Return first item.

Function timeout with signal number and frame:
    Raise timeout error "Computation exceeded time limit".

If this file is the main script:
    Register timeout as handler for alarm signal.
    Set alarm for fifteen seconds.
    Try:
        If length of command-line arguments is not two:
            Raise value error "Supply one expression".
        Print evaluate called with command-line argument at index one.
    If an exception occurs, named exc:
        Print "Error:" followed by exc to standard error.
        Exit with status one.
    Finally:
        Set alarm to zero.
~~~

## Function name to English word

| Function | English |
|---|---|
| arithmetic | perform arithmetic |
| solve | solve equations |
| determinant | calculate determinant |
| inverse | invert matrix |
| eigenvalues | calculate eigenvalues and multiplicities |
| rref | reduce to row echelon form |
| approx | approximate numerically |
| summation | sum over bounds |
| product | multiply over bounds |
| mean | calculate arithmetic mean |
| variance | calculate population variance |
| binomial_pmf | calculate binomial probability mass |
| normal_cdf | calculate normal cumulative probability |
| gradient | calculate vector of partial derivatives |
| jacobian | calculate matrix of partial derivatives |
| integral | integrate |
| Parser | parse mathematical notation |
| __init__ | initialize instance |
| peek | inspect next token without consuming |
| take | consume next token |
| accept | conditionally consume matching token |
| expect | require matching token |
| sequence | read delimited sequence |
| expr | read expression according to precedence |
| parse | parse entire token stream |
| evaluate | evaluate input |
| timeout | raise timeout error |
| def | define function |
| return | return result |
| if | if |
| elif | otherwise if |
| else | otherwise |
| for | for each |
| while | while condition holds |
| break | leave loop |
| continue | begin next iteration |
| try | attempt |
| except | if exception occurs |
| finally | regardless of outcome |
| raise | raise exception |
| and / or / not | and / or / not |
| in | belongs to |
| is / is not | is identical to / is not identical to |
| None | nothing |
| True / False | true / false |
