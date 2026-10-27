/* Course CrackMe L4 — nested checks + decoy (educational, not stripped by default).
 */
#include <stdio.h>
#include <string.h>

static int stage1(const char *s) {
    return strlen(s) == 10;
}
static int stage2(const char *s) {
    return s[0] == 'G' && s[6] == '_';
}
static int stage3(const char *s) {
    const char *real = "GHIDRA_MCP";
    const char *decoy = "WRONG_PASS";
    (void)decoy; /* present in .rodata as distraction */
    return strcmp(s, real) == 0;
}

int main(void) {
    char buf[64];
    if (!fgets(buf, sizeof buf, stdin)) return 1;
    buf[strcspn(buf, "\n")] = 0;
    if (stage1(buf) && stage2(buf) && stage3(buf)) {
        puts("Correct! Nested gates cleared.");
        return 0;
    }
    puts("Nope.");
    return 1;
}
