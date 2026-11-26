# Usage and execution — literal English

## Terminal commands from the root README

```sh
sudo pacman -S --needed base-devel python python-sympy
```

Run pacman with elevated privileges through sudo. Request installation or synchronization of base-devel, Python and python-sympy; skip already up-to-date packages because --needed is supplied.

```sh
make
```

Run GNU Make. Read the Makefile and build its default target, which produces the calculator executable and native arithmetic shared library.

```sh
make test
```

Request the test target. Build its prerequisites, then run python3 test_engine.py and report the result.

```sh
./calculator
```

Execute the calculator binary in the current directory. The current working directory must also contain engine.py. Type quit or exit at its prompt to terminate.

## Input notation

| Input | Literal English |
|---|---|
| `2+3*4` | Multiply three by four, then add two. |
| `1/3+1/6` | Add one third and one sixth. |
| `5!` | Calculate five factorial. |
| `2x+7=19` | Find x such that twice x plus seven equals nineteen. |
| `x^2-5x+6=0` | Find x such that x squared minus five x plus six equals zero. |
| `factor(x^2-9)` | Factor x squared minus nine. |
| `x+y=10;x-y=2` | Solve both equations simultaneously for x and y. |
| `2x+1>5` | Determine the real values of x for which twice x plus one is greater than five. |
| `diff(x^3,x)` | Differentiate x cubed with respect to x. |
| `integrate(x^2,x,0,3)` | Integrate x squared with respect to x from zero to three. |
| `limit(sin(x)/x,x,0)` | Find the limit of sine of x divided by x as x approaches zero. |
| `sin(pi/2)` | Calculate the sine of pi divided by two radians. |
| `det([[1,2],[3,4]])` | Calculate the determinant of the two-by-two matrix with the specified rows. |
| `inverse([[1,2],[3,4]])` | Find the inverse of that matrix. |
| `eigenvalues([[2,0],[0,3]])` | Find the eigenvalues and multiplicities of the given matrix. |
| `gradient(x^2+y^2,[x,y])` | Find the partial derivatives with respect to x and y, in that order. |
| `binomial(10,3)` | Calculate the number of ways to choose three items from ten without regard to order. |
| `sum(x,x,1,100)` | Add the integers from one through one hundred. |
| `gcd(48,18)` | Find the greatest common divisor of 48 and 18. |
| `factorint(360)` | Find the prime factors of 360 and their exponents. |
| `isprime(97)` | Determine whether 97 is prime. |
| `mean([2,4,6])` | Compute the arithmetic mean of two, four and six. |
| `variance([2,4,6])` | Compute their population variance. |
| `binomial_pmf(5,2,1/2)` | Compute the probability of exactly two successes in five independent Bernoulli trials, each with probability one half. |
| `normal_cdf(0)` | Compute the standard normal cumulative probability at zero. |
| `approx(pi,50)` | Approximate pi using 50 significant decimal digits. |

## Execution trace: 2+3*4

1. Assembly calls getline to read the input. It removes the terminal newline, if present.
2. Assembly compares the input against quit and exit.
3. Assembly constructs the argument vector: python3, engine.py, 2+3*4, null.
4. Assembly forks. The child replaces itself with Python via execvp. The parent waits.
5. Python loads the native library, creates the Parser, and tokenizes the input into number 2, operator +, number 3, operator *, number 4, end.
6. Parser.expr constructs the exact integer 2. It sees + and recursively parses the right operand with minimum binding power 11.
7. In that recursive call the parser reads 3, sees * with binding power 20, reads 4, and calls arithmetic for multiplication.
8. arithmetic finds two signed 64-bit SymPy integers and a loaded native library, then calls math_mul with operands 3 and 4 and a pointer to result storage.
9. math_mul copies 3 into RAX, multiplies it by 4, checks signed overflow, stores 12 at the output pointer and returns status zero.
10. Python reads 12 and wraps it as a SymPy integer. The recursive call returns 12.
11. The outer parser calls arithmetic for 2+12. math_add writes 14 and returns status zero.
12. Python returns the exact integer 14 and prints it. The Python process exits; the Assembly parent resumes its prompt loop.

## Execution trace: 2x+7=19

1. The interface launches the engine as above. The lexer recognizes the integer 2, identifier x, plus, integer 7, equals, integer 19, and end.
2. The parser treats adjacency of 2 and x as implicit multiplication. It constructs a symbolic product because x is not an integer.
3. It adds seven symbolically and constructs an unevaluated equality with nineteen.
4. evaluate collects free symbols and detects a single equation with one variable.
5. It invokes SymPy solveset over the complex numbers. For this equation the solution set is {6}.
6. Python prints the returned set. Assembly resumes the input loop.

The source contains no independent natural-language problem parser or independent symbolic solution algorithm for this equation: solving is delegated to SymPy.
