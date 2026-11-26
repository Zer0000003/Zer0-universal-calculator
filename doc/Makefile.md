# Makefile — literal English interpretation

Source blob: `4da98ddb183dda2723350ae508b1e08c6a024591` ([source](../Makefile)). Read from top to bottom; each entry preserves the original line number, exact code and meaning. Directives are assembler/build instructions, labels mark addresses, and runtime instructions act only when reached.

### Line 1

```makefile
CC ?= gcc
```

Assign gcc to the CC make variable only if it has not already been defined; GNU Make commonly predefines CC as cc.

### Line 2

```makefile
.PHONY: all clean test
```

Declare all, clean and test as phony targets, not files to check for timestamps.

### Line 3

```makefile
all: calculator libinteger_math.so
```

Define the default target all as depending on calculator and libinteger_math.so.

### Line 4

```makefile
calculator: calculator.s
```

Define the calculator executable target as depending on calculator.s.

### Line 5

```makefile
	$(CC) -o $@ $<
```

Run the selected compiler, specifying the target name with -o and the first prerequisite as the input; $@ expands to calculator and $< to calculator.s.

### Line 6

```makefile
libinteger_math.so: integer_math.s
```

Define the shared library target as depending on integer_math.s.

### Line 7

```makefile
	$(CC) -shared -fPIC -o $@ $<
```

Run the selected compiler/linker with -shared to make a shared object, -fPIC to request position-independent code, -o followed by the target name and then the input source. The assembly itself uses position-independent instructions; the flag does not rewrite it.

### Line 8

```makefile
test: all
```

Define the test target to depend on all so both binaries are built first.

### Line 9

```makefile
	python3 test_engine.py
```

Run the Python interpreter on the unit test file.

### Line 10

```makefile
clean:
```

Define the clean target.

### Line 11

```makefile
	rm -f calculator libinteger_math.so
```

Run rm with -f to remove the two generated binaries without prompting or failing merely because they are absent.

