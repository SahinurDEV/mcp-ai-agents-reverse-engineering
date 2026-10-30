#include <stdio.h>
#include <string.h>
/* L2: password stored XOR-ed with a one-byte key; no plaintext in the binary. */
static const unsigned char enc[] = {0x22,0x35,0x28,0x05,0x33,0x29,0x05,0x34,0x35,0x2e,0x05,0x39,0x28,0x23,0x2a,0x2e,0x35};
#define KEY 0x5a
int main(int argc, char **argv) {
    if (argc != 2) { puts("usage: cm_xor PASSWORD"); return 2; }
    const char *p = argv[1];
    if (strlen(p) != sizeof enc) { puts("Wrong password."); return 1; }
    for (size_t i = 0; i < sizeof enc; i++)
        if ((unsigned char)(p[i] ^ KEY) != enc[i]) { puts("Wrong password."); return 1; }
    puts("Correct! L2 solved."); return 0;
}
