# Zer0 Universal Calculator — function-to-word translation

Read the program as English, not as a series of explanations. The translated programs preserve function boundaries, statement order, indentation, conditional branches and labels, using English words in place of source instructions and syntax. Literal strings and names used to connect functions remain unchanged where necessary.

## English-language source

| Program | Translation |
|---|---|
| Assembly interface and native arithmetic | [Assembly in English](assembly-in-english.md) |
| Symbolic mathematics and parser | [Engine in English](engine-in-english.md) |
| Compiler rules and tests | [Build and tests in English](build-and-tests-in-english.md) |

For example, the native addition function reads:

~~~text
Function math_add:
    Move first argument register into accumulator.
    Add second argument register to accumulator.
    Jump to overflow if signed overflow flag is set.
    Move accumulator into memory at address held by third argument register.
    Exclusive OR low thirty-two bits of accumulator with themselves.
    Return.
~~~

Each translation also includes a word dictionary. These are English pseudocode, not executable source. External libraries are represented by their calls, not by translations of their internal implementations.

## Optional technical reference

The previous line-by-line annotations remain available for reference only:

- [Assembly interface](calculator.s.md)
- [Native arithmetic](integer_math.s.md)
- [Symbolic engine](engine.py.md)
- [Tests](test_engine.py.md)
- [Makefile](Makefile.md)
- [Usage and execution](usage-and-execution.md)
