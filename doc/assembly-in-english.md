# Assembly — English-language program

Source: calculator.s (bfa1b3746586bba921f6ea3c052078b982c1245b) and integer_math.s (272ef313e106c265122f122dc6e7c62c7afe5592).

The following is the program expressed in English words. Indentation preserves its structure; labels retain their names so jumps remain unambiguous.

## calculator.s

~~~text
Use Intel assembly syntax without register prefixes.

Begin read-only data section.
    Define prompt as the zero-terminated text "math> ".
    Define intro as the zero-terminated text "Zer0 Math | enter an expression or equation; quit to exit."
    Define quitword as the zero-terminated text "quit".
    Define exitword as the zero-terminated text "exit".
    Define python as the zero-terminated text "python3".
    Define backend as the zero-terminated text "engine.py".
    Define error as the zero-terminated text "Could not start Python solver."
    Define forkerror as the zero-terminated text "Could not create solver process."

Begin zero-initialized data section.
    Align to eight bytes.
    Reserve eight bytes for line.
    Reserve eight bytes for capacity.
    Reserve thirty-two bytes for argument vector.

Begin executable text section.
Make main globally visible.
Declare main as a function.

Function main:
    Push base pointer onto stack.
    Move stack pointer into base pointer.
    Load address of intro into first argument register.
    Call put string.

Label read_loop:
    Load address of prompt into first argument register.
    Exclusive OR the low thirty-two bits of accumulator with themselves.
    Call print formatted.
    Exclusive OR the low thirty-two bits of first argument register with themselves.
    Call flush file streams.
    Load address of line into first argument register.
    Load address of capacity into second argument register.
    Move the address of standard input variable from the global offset table into third argument register.
    Move the value stored at the third argument register's address into third argument register.
    Call get line.
    Test accumulator against itself.
    Jump to done if sign flag is set.
    Move the pointer stored in line into first argument register.
    Compare the byte at first argument register plus accumulator minus one with ten.
    Jump to trimmed if not equal.
    Decrement accumulator.
    Write zero to the byte at first argument register plus accumulator.

Label trimmed:
    Compare accumulator with zero.
    Jump to read_loop if equal.
    Load address of quitword into second argument register.
    Call compare strings.
    Test low thirty-two bits of accumulator against themselves.
    Jump to done if zero.
    Move the pointer stored in line into first argument register.
    Load address of exitword into second argument register.
    Call compare strings.
    Test low thirty-two bits of accumulator against themselves.
    Jump to done if zero.
    Load address of python into accumulator.
    Store accumulator into argument vector at byte offset zero.
    Load address of backend into accumulator.
    Store accumulator into argument vector at byte offset eight.
    Move the pointer stored in line into accumulator.
    Store accumulator into argument vector at byte offset sixteen.
    Store sixty-four-bit zero into argument vector at byte offset twenty-four.
    Call fork process.
    Test low thirty-two bits of accumulator against themselves.
    Jump to fork_failed if sign flag is set.
    Jump to child if zero.
    Move low thirty-two bits of accumulator into low thirty-two bits of first argument register.
    Exclusive OR low thirty-two bits of second argument register with themselves.
    Exclusive OR low thirty-two bits of third argument register with themselves.
    Call wait for process identifier.
    Jump to read_loop.

Label child:
    Load address of python into first argument register.
    Load address of argument vector into second argument register.
    Call execute program with argument vector and PATH search.
    Load address of error into first argument register.
    Call print system error.
    Move one hundred twenty-seven into low thirty-two bits of first argument register.
    Call immediate process exit.

Label fork_failed:
    Load address of forkerror into first argument register.
    Call print system error.
    Jump to read_loop.

Label done:
    Move the pointer stored in line into first argument register.
    Call free memory.
    Exclusive OR low thirty-two bits of accumulator with themselves.
    Pop base pointer from stack.
    Return.

Set size of main to current address minus address of main.
Declare non-executable GNU stack note.
~~~

## integer_math.s

~~~text
Use Intel assembly syntax without register prefixes.
Begin executable text section.

Make math_add, math_sub and math_mul globally visible.

Declare math_add as a function.
Function math_add:
    Move first argument register into accumulator.
    Add second argument register to accumulator.
    Jump to overflow if signed overflow flag is set.
    Move accumulator into memory at address held by third argument register.
    Exclusive OR low thirty-two bits of accumulator with themselves.
    Return.

Declare math_sub as a function.
Function math_sub:
    Move first argument register into accumulator.
    Subtract second argument register from accumulator.
    Jump to overflow if signed overflow flag is set.
    Move accumulator into memory at address held by third argument register.
    Exclusive OR low thirty-two bits of accumulator with themselves.
    Return.

Declare math_mul as a function.
Function math_mul:
    Move first argument register into accumulator.
    Signed multiply accumulator by second argument register.
    Jump to overflow if signed overflow flag is set.
    Move accumulator into memory at address held by third argument register.
    Exclusive OR low thirty-two bits of accumulator with themselves.
    Return.

Label overflow:
    Move one into low thirty-two bits of accumulator.
    Return.

Declare non-executable GNU stack note.
~~~

## Function and instruction words

| Source word | English word or phrase |
|---|---|
| mov | move source value into destination |
| lea | load effective address |
| push | push onto stack |
| pop | pop from stack |
| call | call function |
| ret | return |
| add | add |
| sub | subtract |
| imul | signed multiply |
| xor | exclusive OR |
| test | test bits and set flags |
| cmp | compare and set flags |
| dec | decrement |
| jo | jump if overflow |
| js | jump if sign flag set |
| jz / je | jump if zero / equal |
| jne | jump if not equal |
| jmp | jump |
| rax / eax | accumulator / low thirty-two bits of accumulator |
| rdi / edi | first argument register / its low thirty-two bits |
| rsi / esi | second argument register / its low thirty-two bits |
| rdx / edx | third argument register / its low thirty-two bits |
| rbp | base pointer |
| rsp | stack pointer |
| rip | instruction pointer |
| puts | put string and newline |
| printf | print formatted |
| fflush | flush file streams |
| getline | get line |
| strcmp | compare strings |
| fork | fork process |
| waitpid | wait for process identifier |
| execvp | execute program with argument vector and PATH search |
| perror | print system error |
| _exit | immediate process exit |
| free | free memory |
| .asciz | store zero-terminated string |
| .zero | reserve zero bytes |
| .align | align storage |
| .global | make symbol globally visible |
| .type | declare symbol type |
| .section | begin section |
| .size | declare symbol size |
