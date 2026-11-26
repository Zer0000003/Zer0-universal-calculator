# Zer0 Math — prototype CAS for x86-64 Linux

A GNU assembler (Intel syntax) command-line interface and checked native signed 64-bit integer addition, subtraction and multiplication, backed by a Python/SymPy symbolic engine. No LLM or network service is required at runtime. This is not a pure-Assembly CAS.

## Build on Arch Linux

```sh
sudo pacman -S --needed base-devel python python-sympy
make
make test
./calculator
```

Run from this directory so the executable can find `engine.py`. Enter `quit` or `exit` to leave. Use GNU as through GCC, not NASM.

## Example inputs

| Area | Input |
|---|---|
| Arithmetic | `2+3*4`, `1/3+1/6`, `5!` |
| Algebra | `2x+7=19`, `x^2-5x+6=0`, `factor(x^2-9)` |
| Systems | `x+y=10;x-y=2` |
| Inequalities | `2x+1>5` |
| Calculus | `diff(x^3+2x,x)`, `integrate(x^2,x,0,3)`, `limit(sin(x)/x,x,0)` |
| Trigonometry | `sin(pi/2)` (radians) |
| Linear algebra | `det([[1,2],[3,4]])`, `inverse([[1,2],[3,4]])`, `eigenvalues([[2,0],[0,3]])` |
| Vector calculus | `gradient(x^2+y^2,[x,y])` |
| Discrete math | `binomial(10,3)`, `sum(x,x,1,100)` |
| Number theory | `gcd(48,18)`, `factorint(360)`, `isprime(97)` |
| Statistics | `mean([2,4,6])`, `variance([2,4,6])` (population variance) |
| Probability | `binomial_pmf(5,2,1/2)`, `normal_cdf(0)` |
| Numerical approximation | `approx(pi,50)` |

Use parentheses and explicit `*` for ambiguous multiplication. For example, `xy` means a single variable, not `x*y`; `1/2x` means `(1/2)*x`. Single-variable equations default to complex solutions; inequalities use real ordering. Decimals are parsed as exact rationals. Use `approx` for decimal output. Unsupported operations or malformed input can report an error or return unevaluated expressions. Advanced operations may require explicit function calls. This is not a natural-language word-problem solver, theorem prover, graphing calculator or step-by-step derivation engine. Eager symbolic simplification can erase domain restrictions (e.g. canceled denominators); verify domain-sensitive results. No general solution is guaranteed for arbitrary equations or inequalities. Input length and a 15-second solver alarm are basic safeguards, not a security sandbox; use only trusted local input. Tested on Linux x86-64 with GNU compiler tooling and SymPy 1.14.0, not directly on Arch Linux.

## Components

- `calculator.s`: Assembly REPL; uses libc to read input, starts Python with an argument vector (no shell), waits for the child, and loops.
- `integer_math.s`: native integer arithmetic, overflow flagged via `jo`; exact symbolic arithmetic handles overflow.
- `engine.py`: restricted grammar, symbolic calculations and dispatch.
- `test_engine.py`: unit tests.
- `Makefile`: build, test, clean.

## Literal English Pseudocode (LEP)

Read the [complete LEP program](doc/README.md) and the [LEP translation standard](doc/LEP-Standard.md). All repository-owned Assembly, Python, tests and build instructions are translated into literal English, preserving program structure. Line-by-line annotations are optional reference material.
