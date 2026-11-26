CC ?= gcc
.PHONY: all clean test
all: calculator libinteger_math.so
calculator: calculator.s
	$(CC) -o $@ $<
libinteger_math.so: integer_math.s
	$(CC) -shared -fPIC -o $@ $<
test: all
	python3 test_engine.py
clean:
	rm -f calculator libinteger_math.so
