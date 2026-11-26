# integer_math.s — literal English interpretation

Source blob: `272ef313e106c265122f122dc6e7c62c7afe5592` ([source](../integer_math.s)). Read from top to bottom; each entry preserves the original line number, exact code and meaning. Directives are assembler/build instructions, labels mark addresses, and runtime instructions act only when reached.

### Line 1

```asm
.intel_syntax noprefix
```

Select Intel assembly syntax without register prefixes.

### Line 2

```asm
.section .text
```

Switch to the executable text section.

### Line 3

```asm
# System V AMD64 ABI: RDI=a, RSI=b, RDX=pointer to output.
```

Comment: under the System V AMD64 calling convention the first integer is in RDI, the second in RSI and the result pointer is in RDX.

### Line 4

```asm
# Return EAX=0 on success, EAX=1 on signed 64-bit overflow.
```

Comment: return zero in EAX on success or one on signed 64-bit overflow.

### Line 5

```asm
.global math_add, math_sub, math_mul
```

Expose the three arithmetic symbols to the linker.

### Line 6

```asm
.type math_add, @function
```

Mark math_add as a function.

### Line 7

```asm
math_add:
```

Define the entry address for addition.

### Line 8

```asm
    mov rax, rdi
```

Copy the first operand from RDI into RAX.

### Line 9

```asm
    add rax, rsi
```

Add the second operand in RSI to RAX, retaining the low 64 bits and setting arithmetic flags.

### Line 10

```asm
    jo overflow
```

Jump to overflow if the signed overflow flag is set.

### Line 11

```asm
    mov [rdx], rax
```

Write the eight-byte result in RAX into memory at the address in RDX.

### Line 12

```asm
    xor eax, eax
```

Clear EAX to return success (also clears the upper half of RAX).

### Line 13

```asm
    ret
```

Return to the caller.

### Line 14

```asm
.type math_sub, @function
```

Mark math_sub as a function.

### Line 15

```asm
math_sub:
```

Define the entry address for subtraction.

### Line 16

```asm
    mov rax, rdi
```

Copy the first operand from RDI into RAX.

### Line 17

```asm
    sub rax, rsi
```

Subtract the second operand in RSI from RAX and update arithmetic flags.

### Line 18

```asm
    jo overflow
```

Jump to overflow if the signed result cannot fit in 64 bits.

### Line 19

```asm
    mov [rdx], rax
```

Write the result to the address in RDX.

### Line 20

```asm
    xor eax, eax
```

Clear EAX to report success.

### Line 21

```asm
    ret
```

Return to the caller.

### Line 22

```asm
.type math_mul, @function
```

Mark math_mul as a function.

### Line 23

```asm
math_mul:
```

Define the entry address for multiplication.

### Line 24

```asm
    mov rax, rdi
```

Copy the first operand from RDI into RAX.

### Line 25

```asm
    imul rax, rsi
```

Multiply signed RAX by signed RSI, storing the low 64 bits in RAX and setting overflow when the product cannot fit in signed 64 bits.

### Line 26

```asm
    jo overflow
```

Jump to overflow when the overflow flag is set.

### Line 27

```asm
    mov [rdx], rax
```

Write the result to memory at the address in RDX.

### Line 28

```asm
    xor eax, eax
```

Clear EAX to report success.

### Line 29

```asm
    ret
```

Return to the caller.

### Line 30

```asm
overflow:
```

Define the shared overflow branch.

### Line 31

```asm
    mov eax, 1
```

Write one into EAX to report overflow; the output memory is not written on this path.

### Line 32

```asm
    ret
```

Return to the caller.

### Line 33

```asm
.section .note.GNU-stack,"",@progbits
```

Emit a non-executable GNU stack note.

