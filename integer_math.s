.intel_syntax noprefix
.section .text
# System V AMD64 ABI: RDI=a, RSI=b, RDX=pointer to output.
# Return EAX=0 on success, EAX=1 on signed 64-bit overflow.
.global math_add, math_sub, math_mul
.type math_add, @function
math_add:
    mov rax, rdi
    add rax, rsi
    jo overflow
    mov [rdx], rax
    xor eax, eax
    ret
.type math_sub, @function
math_sub:
    mov rax, rdi
    sub rax, rsi
    jo overflow
    mov [rdx], rax
    xor eax, eax
    ret
.type math_mul, @function
math_mul:
    mov rax, rdi
    imul rax, rsi
    jo overflow
    mov [rdx], rax
    xor eax, eax
    ret
overflow:
    mov eax, 1
    ret
.section .note.GNU-stack,"",@progbits
