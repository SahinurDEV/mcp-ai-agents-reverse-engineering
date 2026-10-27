/* Course CrackMe L1 — plaintext password check (educational).
 * Build: make l1
 */
#include <stdio.h>
#include <string.h>

int main(void) {
    char buf[64];
    if (!fgets(buf, sizeof buf, stdin)) return 1;
    buf[strcspn(buf, "\n")] = 0;
    if (strcmp(buf, "MCP_ROCKS") == 0) {
        puts("Correct! Welcome, agent.");
        return 0;
    }
    puts("Nope.");
    return 1;
}
