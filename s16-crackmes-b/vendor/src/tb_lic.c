#include <stdio.h>
#include <string.h>
#include <stdint.h>
/* Track B #1: name/key licence check. key = %08X of (djb2(name) ^ 0xC0FFEE11) */
static uint32_t mix(const char *s) {
    uint32_t h = 5381;
    while (*s) h = h * 33 + (unsigned char)*s++;
    return h ^ 0xC0FFEE11u;
}
static int valid_name(const char *n) {
    size_t l = strlen(n);
    if (l < 3 || l > 16) return 0;
    for (; *n; n++) if (*n < 'a' || *n > 'z') return 0;
    return 1;
}
int main(int argc, char **argv) {
    if (argc != 3) { puts("usage: tb_lic NAME KEY"); return 2; }
    if (!valid_name(argv[1])) { puts("Name must be 3-16 lowercase letters."); return 1; }
    char want[9]; snprintf(want, sizeof want, "%08X", mix(argv[1]));
    if (strcmp(argv[2], want) == 0) { printf("Licensed to %s. Thank you!\n", argv[1]); return 0; }
    puts("Invalid licence key."); return 1;
}
