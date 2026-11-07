all: hello hello_s
hello: hello.c
	gcc -g -O0 -fdebug-prefix-map=$(CURDIR)=. -o $@ $<
hello_s: hello.c
	gcc -O1 -s -o $@ $<
