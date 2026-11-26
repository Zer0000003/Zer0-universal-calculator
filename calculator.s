.intel_syntax noprefix
.section .rodata
prompt: .asciz "math> "
intro: .asciz "Zer0 Math | enter an expression or equation; quit to exit."
quitword: .asciz "quit"
exitword: .asciz "exit"
python: .asciz "python3"
backend: .asciz "engine.py"
error: .asciz "Could not start Python solver."
forkerror: .asciz "Could not create solver process."
.section .bss
.align 8
line: .zero 8
capacity: .zero 8
argv: .zero 32
.section .text
.global main
.type main, @function
main:
    push rbp
    mov rbp, rsp
    lea rdi, [rip+intro]
    call puts@PLT
read_loop:
    lea rdi, [rip+prompt]
    xor eax, eax
    call printf@PLT
    xor edi, edi
    call fflush@PLT
    lea rdi, [rip+line]
    lea rsi, [rip+capacity]
    mov rdx, [rip+stdin@GOTPCREL]
    mov rdx, [rdx]
    call getline@PLT
    test rax, rax
    js done
    mov rdi, [rip+line]
    cmp byte ptr [rdi+rax-1], 10
    jne trimmed
    dec rax
    mov byte ptr [rdi+rax], 0
trimmed:
    cmp rax, 0
    je read_loop
    lea rsi, [rip+quitword]
    call strcmp@PLT
    test eax, eax
    jz done
    mov rdi, [rip+line]
    lea rsi, [rip+exitword]
    call strcmp@PLT
    test eax, eax
    jz done
    lea rax, [rip+python]
    mov [rip+argv], rax
    lea rax, [rip+backend]
    mov [rip+argv+8], rax
    mov rax, [rip+line]
    mov [rip+argv+16], rax
    mov qword ptr [rip+argv+24], 0
    call fork@PLT
    test eax, eax
    js fork_failed
    jz child
    mov edi, eax
    xor esi, esi
    xor edx, edx
    call waitpid@PLT
    jmp read_loop
child:
    lea rdi, [rip+python]
    lea rsi, [rip+argv]
    call execvp@PLT
    lea rdi, [rip+error]
    call perror@PLT
    mov edi, 127
    call _exit@PLT
fork_failed:
    lea rdi, [rip+forkerror]
    call perror@PLT
    jmp read_loop
done:
    mov rdi, [rip+line]
    call free@PLT
    xor eax, eax
    pop rbp
    ret
.size main, .-main
.section .note.GNU-stack,"",@progbits
