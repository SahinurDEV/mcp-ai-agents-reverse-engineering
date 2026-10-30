all: hello hello_s
hello: hello.c
	gcc -g -O0 -o $@ $<
hello_s: hello.c
	gcc -O1 -s -o $@ $<
