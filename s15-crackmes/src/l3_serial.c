/* Course CrackMe L3 — serial of form AAA-#### where digits sum to 42.
 */
#include <stdio.h>
#include <string.h>
#include <ctype.h>

int valid(const char *s) {
    if (strlen(s) != 8) return 0;
    if (strncmp(s, "MCP-", 4) != 0) return 0;
    int sum = 0;
    for (int i = 4; i < 8; i++) {
        if (!isdigit((unsigned char)s[i])) return 0;
        sum += s[i] - '0';
    }
    return sum == 20;
}

int main(void) {
    char buf[64];
    printf("CrackMe L3 — enter serial (MCP-####): ");
    if (!fgets(buf, sizeof buf, stdin)) return 1;
    buf[strcspn(buf, "\n")] = 0;
    if (valid(buf)) { puts("Correct! Serial accepted."); return 0; }
    puts("Nope.");
    return 1;
}
