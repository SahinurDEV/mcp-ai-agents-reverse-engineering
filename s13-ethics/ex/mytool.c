/* mytool.c - Exercise 13: a program you wrote yourself, so analysing it is clearly in scope.
   Licence: MIT. Author: you. */
#include <stdio.h>
#include <string.h>

int check(const char *s) { return strlen(s) == 6 && s[0] == 'm' && s[5] == 'p'; }

int main(int argc, char **argv) {
    if (argc < 2) { puts("usage: mytool CODE"); return 2; }
    puts(check(argv[1]) ? "accepted" : "rejected");
    return 0;
}
