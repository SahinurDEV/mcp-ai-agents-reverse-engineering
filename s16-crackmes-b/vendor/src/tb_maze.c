#include <stdio.h>
#include <string.h>
/* Track B #2: walk the maze with u/d/l/r from S to E without touching a wall. */
static const char maze[8][9] = {
    "########",
    "#S..#..#",
    "##.##.##",
    "#..#...#",
    "#.##.#.#",
    "#....#E#",
    "####...#",
    "########"};
int main(int argc, char **argv) {
    if (argc != 2) { puts("usage: tb_maze MOVES   (u d l r)"); return 2; }
    int r = 1, c = 1;
    for (const char *m = argv[1]; *m; m++) {
        if (*m == 'u') r--; else if (*m == 'd') r++; else if (*m == 'l') c--; else if (*m == 'r') c++;
        else { puts("Bad move."); return 1; }
        if (maze[r][c] == '#') { printf("Hit a wall after %ld moves.\n", (long)(m - argv[1]) + 1); return 1; }
    }
    if (maze[r][c] == 'E') { puts("You escaped!"); return 0; }
    puts("Still inside the maze."); return 1;
}
