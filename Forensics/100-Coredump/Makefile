all: core

core: segfault
	rm -f core
	echo "not~the~answer" | ./segfault || true
	strings core | head -40 | grep -q 't#hean;SW\.er' || (echo "Try again, the answer is not in the first 40 lines." && rm core)

segfault: segfault.c
	gcc -static -O0 -g -o segfault segfault.c

clean:
	rm -f segfault core

.PHONY: all clean
