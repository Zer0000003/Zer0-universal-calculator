# Zer0 Universal Calculator — literal English source manual

This manual translates the repository's implementation into literal English, in the exact order of the original source. Each numbered entry includes the source line followed by its English interpretation. It distinguishes a declaration, a memory operation, a conditional branch, a function call and an actual mathematical calculation. Blank lines inside source files are marked. A trailing end-of-file newline is not counted as an extra source line.

## Source translations

| Document | Source | Lines |
|---|---|---:|
| [Command-line Assembly interface](calculator.s.md) | [calculator.s](../calculator.s) | 89 |
| [Native integer Assembly arithmetic](integer_math.s.md) | [integer_math.s](../integer_math.s) | 33 |
| [Python mathematical engine](engine.py.md) | [engine.py](../engine.py) | 184 |
| [Automated test suite](test_engine.py.md) | [test_engine.py](../test_engine.py) | 45 |
| [Build and compiler instructions](Makefile.md) | [Makefile](../Makefile) | 11 |

Total: 362 physical source/build lines, including internal blank lines. Every document records the exact source blob SHA it describes. The [original README](../README.md) is already English; its terminal commands and mathematical notation are explained in [the usage and execution guide](usage-and-execution.md).

## How to read the Assembly

- RAX: 64-bit accumulator and integer/pointer return register.
- EAX: low 32 bits of RAX; writing EAX clears the upper 32 bits of RAX.
- RDI, RSI, RDX: first, second and third integer/pointer argument registers under the System V AMD64 ABI.
- RSP: stack pointer. RBP: conventional frame pointer. RIP: instruction pointer.
- Brackets denote a memory operand; LEA computes an effective address without reading the memory at that address.
- MOV copies bits; ADD, SUB and IMUL calculate and update arithmetic flags.
- TEST and CMP update flags without storing an arithmetic result.
- ZF: zero flag. SF: sign flag. OF: signed overflow flag.
- JZ/JE: jump if zero/equal. JNE: jump if not equal. JS: jump if sign flag set. JO: jump if signed overflow. JMP: unconditional jump.
- CALL transfers control while saving a return address. RET restores that return address.
- PLT: procedure linkage table. GOT: global offset table. These support linking to external library symbols.
- A label is an address marker, not an instruction. A directive tells the assembler how to produce an object file.

## Scope and limitations

The mathematical engine delegates advanced algorithms to SymPy; this manual documents the repository's own code, not the entire Python runtime, libc or SymPy implementation. The current program is a hybrid Assembly/Python prototype. The manual describes code behavior, not a proof of mathematical correctness. Run the actual test suite to establish current test status. Domain restrictions can be lost by eager simplification; the timeout is not a security sandbox. Documentation should be revised whenever any source blob changes.
