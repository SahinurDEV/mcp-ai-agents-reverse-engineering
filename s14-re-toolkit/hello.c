/* hello.c: the first binary we reverse. Built with symbols so we can check Ghidra against the source. */
#include <stdio.h>
#include <string.h>

static int greet(const char *name) {
    if (strlen(name) > 16) { puts("name too long"); return 1; }
    printf("Hello, %s!\n", name);
    return 0;
}

int main(int argc, char **argv) {
    const char *who = argc > 1 ? argv[1] : "MCP";
    return greet(who);
}
