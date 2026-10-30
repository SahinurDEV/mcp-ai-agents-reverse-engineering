#include <stdio.h>
#include <string.h>
/* L1: plain strcmp against a literal. */
int main(int argc, char **argv) {
    if (argc != 2) { puts("usage: cm_strcmp PASSWORD"); return 2; }
    if (strcmp(argv[1], "open_sesame_42") == 0) { puts("Correct! L1 solved."); return 0; }
    puts("Wrong password."); return 1;
}
