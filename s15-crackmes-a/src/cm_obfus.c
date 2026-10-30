#include <stdio.h>
#include <string.h>
/* L3: opaque predicates, junk arithmetic and a decoy password.
   x*(x+1) is always even, so the decoy branch can never run. */
static const int tbl[] = {106,120,116,116,107,119,123,121,125,142,125,141,147,142,147,144};
static int junk(int v) { int a = v * 7 + 3; a ^= a << 2; return a & 0; }   /* always 0 */
int main(int argc, char **argv) {
    if (argc != 2) { puts("usage: cm_obfus PASSWORD"); return 2; }
    const char *p = argv[1];
    volatile int x = (int)strlen(p);
    if ((x * (x + 1)) % 2 == 1) {                     /* opaque: never true */
        if (strcmp(p, "hunter2_admin") == 0) { puts("Correct! L3 solved."); return 0; }
    }
    if (x != (int)(sizeof tbl / sizeof tbl[0]) + junk(x)) { puts("Wrong password."); return 1; }
    int ok = 1;
    for (int i = 0; i < x; i++) {
        int t = tbl[i] - 3 * i + junk(i);
        if ((x * x) >= 0 && p[i] != t) ok = 0;        /* opaque: always true */
    }
    puts(ok ? "Correct! L3 solved." : "Wrong password.");
    return !ok;
}
