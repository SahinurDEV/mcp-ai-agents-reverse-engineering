#include <stdio.h>
#include <string.h>
#include <ctype.h>
/* L4: serial "AAAA-NNNN"; NNNN = (sum of the four letters * 31 + 7) % 10000.
   Built with -O2 and stripped. Many valid serials: write a keygen. */
static int check(const char *s) {
    if (strlen(s) != 9 || s[4] != '-') return 0;
    int sum = 0;
    for (int i = 0; i < 4; i++) { if (!isupper((unsigned char)s[i])) return 0; sum += s[i]; }
    char want[5]; snprintf(want, sizeof want, "%04d", (sum * 31 + 7) % 10000);
    return memcmp(s + 5, want, 4) == 0;
}
int main(int argc, char **argv) {
    if (argc != 2) { puts("usage: cm_strip SERIAL"); return 2; }
    if (check(argv[1])) { puts("Correct! L4 solved."); return 0; }
    puts("Invalid serial."); return 1;
}
