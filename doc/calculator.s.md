# calculator.s — literal English interpretation

Source blob: `bfa1b3746586bba921f6ea3c052078b982c1245b` ([source](../calculator.s)). Read from top to bottom; each entry preserves the original line number, exact code and meaning. Directives are assembler/build instructions, labels mark addresses, and runtime instructions act only when reached.

### Line 1

```asm
.intel_syntax noprefix
```

Tell GNU assembler to use Intel operand order and omit register prefixes.

### Line 2

```asm
.section .rodata
```

Switch subsequent data into the read-only data section.

### Line 3

```asm
prompt: .asciz "math> "
```

At label prompt, store the characters math> followed by a space and a zero terminator.

### Line 4

```asm
intro: .asciz "Zer0 Math | enter an expression or equation; quit to exit."
```

At label intro, store the introductory message followed by a zero terminator.

### Line 5

```asm
quitword: .asciz "quit"
```

At label quitword, store quit and a zero terminator.

### Line 6

```asm
exitword: .asciz "exit"
```

At label exitword, store exit and a zero terminator.

### Line 7

```asm
python: .asciz "python3"
```

At label python, store python3 and a zero terminator.

### Line 8

```asm
backend: .asciz "engine.py"
```

At label backend, store engine.py and a zero terminator.

### Line 9

```asm
error: .asciz "Could not start Python solver."
```

At label error, store the Python startup error message and a zero terminator.

### Line 10

```asm
forkerror: .asciz "Could not create solver process."
```

At label forkerror, store the process-creation error message and a zero terminator.

### Line 11

```asm
.section .bss
```

Switch to the zero-initialized storage section.

### Line 12

```asm
.align 8
```

Align the next storage location to an eight-byte boundary.

### Line 13

```asm
line: .zero 8
```

Reserve eight zero bytes at line for the input-buffer pointer.

### Line 14

```asm
capacity: .zero 8
```

Reserve eight zero bytes at capacity for the buffer capacity.

### Line 15

```asm
argv: .zero 32
```

Reserve 32 zero bytes at argv for four eight-byte argument pointers.

### Line 16

```asm
.section .text
```

Switch to the executable instruction section.

### Line 17

```asm
.global main
```

Expose the main symbol to the linker.

### Line 18

```asm
.type main, @function
```

Mark main as a function symbol.

### Line 19

```asm
main:
```

Define the entry address of main.

### Line 20

```asm
    push rbp
```

Decrement RSP by eight and save the old RBP at that stack address.

### Line 21

```asm
    mov rbp, rsp
```

Copy the current stack pointer RSP into RBP to establish a frame pointer.

### Line 22

```asm
    lea rdi, [rip+intro]
```

Calculate the address of intro relative to RIP and put that address into RDI, the first argument register.

### Line 23

```asm
    call puts@PLT
```

Call the C library puts function through the procedure linkage table; print the string and a newline.

### Line 24

```asm
read_loop:
```

Define the address to which the input loop returns.

### Line 25

```asm
    lea rdi, [rip+prompt]
```

Load the address of prompt into RDI.

### Line 26

```asm
    xor eax, eax
```

XOR EAX with itself to set it to zero; this also clears upper RAX bits and indicates no vector arguments for the variadic printf call.

### Line 27

```asm
    call printf@PLT
```

Call printf through the procedure linkage table to print the prompt.

### Line 28

```asm
    xor edi, edi
```

XOR EDI with itself to pass a null first argument in RDI.

### Line 29

```asm
    call fflush@PLT
```

Call fflush(NULL) to flush all open output streams.

### Line 30

```asm
    lea rdi, [rip+line]
```

Load the address of the line pointer variable into RDI; getline receives a pointer to the pointer.

### Line 31

```asm
    lea rsi, [rip+capacity]
```

Load the address of capacity into RSI; getline can update the capacity through it.

### Line 32

```asm
    mov rdx, [rip+stdin@GOTPCREL]
```

Load the address of the libc stdin variable from the global offset table into RDX.

### Line 33

```asm
    mov rdx, [rdx]
```

Read the pointer stored at that address into RDX; this is the stdin FILE pointer.

### Line 34

```asm
    call getline@PLT
```

Call getline with the buffer pointer address, capacity address and stdin stream; RAX receives the byte count or -1.

### Line 35

```asm
    test rax, rax
```

Perform a bitwise AND of RAX with itself for flags only; do not change RAX.

### Line 36

```asm
    js done
```

Jump to done if the sign flag is set (a negative getline result).

### Line 37

```asm
    mov rdi, [rip+line]
```

Load the input buffer pointer stored at line into RDI.

### Line 38

```asm
    cmp byte ptr [rdi+rax-1], 10
```

Compare the byte at buffer address plus count minus one with decimal 10 (line feed).

### Line 39

```asm
    jne trimmed
```

Jump to trimmed if the final byte is not a line feed.

### Line 40

```asm
    dec rax
```

Subtract one from RAX, shortening the logical length.

### Line 41

```asm
    mov byte ptr [rdi+rax], 0
```

Store a zero byte at the new end of the input string.

### Line 42

```asm
trimmed:
```

Define the address reached after optional newline removal.

### Line 43

```asm
    cmp rax, 0
```

Compare the current input length in RAX with zero.

### Line 44

```asm
    je read_loop
```

Jump to read_loop if the length is zero.

### Line 45

```asm
    lea rsi, [rip+quitword]
```

Load the address of the string quit into RSI as the second argument.

### Line 46

```asm
    call strcmp@PLT
```

Call strcmp to compare the input string in RDI with quit in RSI; EAX receives the comparison result.

### Line 47

```asm
    test eax, eax
```

Test EAX against itself to set flags based on its value.

### Line 48

```asm
    jz done
```

Jump to done if the comparison result is zero (equal strings).

### Line 49

```asm
    mov rdi, [rip+line]
```

Reload the input pointer into RDI because the previous call may have changed argument registers.

### Line 50

```asm
    lea rsi, [rip+exitword]
```

Load the address of exit into RSI.

### Line 51

```asm
    call strcmp@PLT
```

Call strcmp to compare the input string with exit.

### Line 52

```asm
    test eax, eax
```

Test EAX against itself to determine whether the comparison returned zero.

### Line 53

```asm
    jz done
```

Jump to done if the strings were equal.

### Line 54

```asm
    lea rax, [rip+python]
```

Calculate the address of python3 and put it in RAX.

### Line 55

```asm
    mov [rip+argv], rax
```

Write that address into the first eight-byte slot of argv.

### Line 56

```asm
    lea rax, [rip+backend]
```

Calculate the address of engine.py and put it in RAX.

### Line 57

```asm
    mov [rip+argv+8], rax
```

Write that address into the second slot of argv, eight bytes after its base.

### Line 58

```asm
    mov rax, [rip+line]
```

Read the input buffer pointer into RAX.

### Line 59

```asm
    mov [rip+argv+16], rax
```

Write that pointer into the third argv slot, sixteen bytes after its base.

### Line 60

```asm
    mov qword ptr [rip+argv+24], 0
```

Write a 64-bit zero into the fourth argv slot to terminate the argument vector.

### Line 61

```asm
    call fork@PLT
```

Call fork to create a child process; EAX receives a negative error, zero in the child, or the child PID in the parent.

### Line 62

```asm
    test eax, eax
```

Test EAX against itself to set sign and zero flags.

### Line 63

```asm
    js fork_failed
```

Jump to fork_failed if the return value is negative.

### Line 64

```asm
    jz child
```

Jump to child if the return value is zero.

### Line 65

```asm
    mov edi, eax
```

Copy the child PID from EAX into EDI as waitpid's first argument.

### Line 66

```asm
    xor esi, esi
```

Clear ESI to pass a null status pointer.

### Line 67

```asm
    xor edx, edx
```

Clear EDX to pass zero wait options.

### Line 68

```asm
    call waitpid@PLT
```

Call waitpid to wait for the child to terminate; no status is collected.

### Line 69

```asm
    jmp read_loop
```

Jump unconditionally back to the input loop.

### Line 70

```asm
child:
```

Define the child process execution branch.

### Line 71

```asm
    lea rdi, [rip+python]
```

Load the address of python3 into RDI as the executable name.

### Line 72

```asm
    lea rsi, [rip+argv]
```

Load the address of argv into RSI as the argument-vector pointer.

### Line 73

```asm
    call execvp@PLT
```

Call execvp to find python3 using PATH and replace the child process with it; on success this call never returns.

### Line 74

```asm
    lea rdi, [rip+error]
```

If execvp returns, load the address of the error string into RDI.

### Line 75

```asm
    call perror@PLT
```

Call perror to print the message and the current errno description to standard error.

### Line 76

```asm
    mov edi, 127
```

Put decimal 127 into EDI as the process exit status.

### Line 77

```asm
    call _exit@PLT
```

Call _exit to terminate the child without ordinary libc exit cleanup.

### Line 78

```asm
fork_failed:
```

Define the fork failure branch.

### Line 79

```asm
    lea rdi, [rip+forkerror]
```

Load the address of the fork error message into RDI.

### Line 80

```asm
    call perror@PLT
```

Call perror to print that message and the errno description.

### Line 81

```asm
    jmp read_loop
```

Jump back to the input loop.

### Line 82

```asm
done:
```

Define the normal termination branch.

### Line 83

```asm
    mov rdi, [rip+line]
```

Load the current input buffer pointer into RDI.

### Line 84

```asm
    call free@PLT
```

Call free to release the allocation; a null pointer is allowed.

### Line 85

```asm
    xor eax, eax
```

Set EAX to zero, the integer return status of main.

### Line 86

```asm
    pop rbp
```

Restore the saved RBP from the stack and advance RSP by eight bytes.

### Line 87

```asm
    ret
```

Pop the return address from the stack into RIP and resume the caller.

### Line 88

```asm
.size main, .-main
```

Set the ELF size of main to the current location minus the address of main.

### Line 89

```asm
.section .note.GNU-stack,"",@progbits
```

Emit an empty GNU stack note without an executable flag, indicating that the object does not require an executable stack.

