# Literal English Pseudocode (LEP)

Version 1.0 — Zer0 Universal Calculator

## Definition

Literal English Pseudocode is a human-readable translation of an existing program into English words, preserving its computational structure and semantics. It is a study and documentation notation, not an executable language.

## Translation rules

1. Preserve the original statement and execution order, including explicit jumps and branches.
2. Preserve indentation, function boundaries and logical scope.
3. Translate instructions, operators, keywords and register names into literal English.
4. Preserve variable identities, parameter order, labels and function relationships.
5. Preserve conditional logic, loops, memory operations, return values and error handling.
6. Do not summarize, simplify or omit computational operations.
7. Separate explanations and technical commentary from the translated program.
8. Keep literal data, strings and identifiers unchanged when translating them would change program behavior or identity.
9. Preserve grouping and operand order; use unambiguous English phrases to express precedence.
10. Translate external calls as calls; do not invent the implementation of an external dependency.

## Example: native integer addition

Assembly:

~~~asm
math_add:
    mov rax, rdi
    add rax, rsi
    jo overflow
    mov [rdx], rax
    xor eax, eax
    ret
~~~

LEP:

~~~text
Function math_add:
    Move first argument register into accumulator.
    Add second argument register to accumulator.
    Jump to overflow if signed overflow flag is set.
    Move accumulator into memory at address held by third argument register.
    Exclusive OR low thirty-two bits of accumulator with themselves.
    Return.
~~~

The overflow label and return status are part of the complete translation in [Assembly LEP](assembly-in-english.md).

## Example: Python function

Python:

~~~python
def mean(values):
    return sum(values) / s.Integer(len(values))
~~~

LEP:

~~~text
Define function mean with values:
    Return sum of values divided by symbolic integer of length of values.
~~~

## Verification checklist

- Every repository-owned executable statement is represented.
- Every translated branch has the same condition and destination.
- Every translated call preserves the argument order.
- Every memory address, register width and operand order retains its meaning.
- No new operations or assumptions have been inserted.
- The source blob identifiers identify the versions being translated.

Use this standard whenever updating the LEP documents. This is a project-specific convention, not a formal industry standard.
