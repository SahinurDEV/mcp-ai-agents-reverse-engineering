/* Course CrackMe L2 — XOR-obfuscated password (educational).
 */
#include <stdio.h>
#include <string.h>

static const unsigned char enc[] = {
    'A'^0x13, 'G'^0x13, 'E'^0x13, 'N'^0x13,
    'T'^0x13, '4'^0x13, '2'^0x13, 0
};

int check(const char *s) {
    size_t n = strlen((const char *)enc);
    if (strlen(s) != n) return 0;
    for (size_t i = 0; i < n; i++) {
        if ((unsigned char)(s[i] ^ 0x13) != enc[i]) return 0;
    }
    return 1;
}

int main(void) {
    char buf[64];
    if (!fgets(buf, sizeof buf, stdin)) return 1;
    buf[strcspn(buf, "\n")] = 0;
    if (check(buf)) { puts("Correct! XOR defeated."); return 0; }
    puts("Nope.");
    return 1;
}
