#!/bin/sh
# build_release.sh: builds the Track B release the way a CrackMe author would publish it:
# binaries + README + LICENSE + SHA256SUMS in a zip. Sources stay here and are not in the zip.
set -e; cd "$(dirname "$0")"; rm -rf out && mkdir -p out/trackb-easy-1.0
gcc -O0 -o out/trackb-easy-1.0/tb_lic src/tb_lic.c
gcc -O0 -o out/trackb-easy-1.0/tb_maze src/tb_maze.c
cat > out/trackb-easy-1.0/README.txt <<'R'
Track B easy CrackMes 1.0 (Linux x86-64 ELF)
tb_lic  NAME KEY   find a valid key for any name (keygen welcome)
tb_maze MOVES      escape the maze
Difficulty: easy. No packing, no anti-debug. Do not patch; solve.
R
cat > out/trackb-easy-1.0/LICENSE.txt <<'L'
Copyright 2026 the course team. Written for this course; free to analyse, solve and
write up for learning. Do not redistribute modified binaries. Do not publish ready-made keys
for anything that is not a CrackMe.
L
(cd out/trackb-easy-1.0 && sha256sum tb_lic tb_maze > SHA256SUMS)
(cd out && tar --sort=name --mtime=@1793318400 --owner=0 --group=0 --numeric-owner -cf - trackb-easy-1.0 | gzip -n > trackb-easy-1.0.tar.gz)
sha256sum out/trackb-easy-1.0.tar.gz
