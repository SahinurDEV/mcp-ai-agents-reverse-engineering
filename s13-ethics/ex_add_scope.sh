#!/bin/sh
# ex_add_scope.sh BINARY SOURCE LICENCE: Exercise 13. Add a binary to scope.txt only with a written
# provenance: where it came from and under what licence. Re-adding the same hash is a no-op.
cd "$(dirname "$0")"
[ $# -eq 3 ] || { echo "usage: $0 BINARY SOURCE LICENCE   (both SOURCE and LICENCE are required)"; exit 2; }
[ -f "$1" ] || { echo "no such file: $1"; exit 1; }
h=$(sha256sum "$1" | cut -d' ' -f1)
grep -q "^$h " scope.txt && { echo "already in scope: $1"; exit 0; }
echo "$h own($2,$3) $1" >> scope.txt
echo "added: $1 -> own($2,$3)"
