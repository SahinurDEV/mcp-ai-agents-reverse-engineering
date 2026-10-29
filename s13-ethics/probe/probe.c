/* probe.c: a harmless stand-in for "unknown binary" behaviour: phones home, writes to disk, forks. */
#include <stdio.h>
#include <unistd.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
int main(void) {
    int s = socket(AF_INET, SOCK_STREAM, 0);
    struct sockaddr_in a = { .sin_family = AF_INET, .sin_port = htons(443) };
    inet_pton(AF_INET, "1.1.1.1", &a.sin_addr);
    printf("connect 1.1.1.1:443  -> %s\n", connect(s, (void *)&a, sizeof a) == 0 ? "OPEN" : "blocked");
    FILE *f = fopen("/target/dropped", "w");
    printf("write /target/dropped -> %s\n", f ? "WRITTEN" : "blocked");
    FILE *h = fopen("/etc/cron.d/x", "w");
    printf("write /etc/cron.d/x  -> %s\n", h ? "WRITTEN" : "blocked");
    printf("uid=%d\n", getuid());
    int n = 0;
    for (; n < 100; n++) { pid_t p = fork(); if (p < 0) break; if (p == 0) { sleep(2); _exit(0); } }
    printf("forks before limit   -> %d of 100\n", n);
    fflush(stdout);
    return 0;
}
