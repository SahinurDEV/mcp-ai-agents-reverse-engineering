#!/bin/sh
# writeup_lint.sh WRITEUP.md: Lecture 13.3. Check a writeup follows the etiquette before you publish it:
# a pinned hash that is in scope.txt, the origin and credit, the method, and a verification step.
# A bare key is not a writeup. Exit 1 if anything is missing.
cd "$(dirname "$0")"; f=$1; miss=0
need() { if grep -qiE "$2" "$f"; then echo "ok    $1"; else echo "MISS  $1"; miss=1; fi; }
need "SHA-256 of the binary"           'SHA-256: [0-9a-f]{64}'
need "origin and licence / credit"     '^- (Origin|Author|Source)'
need "how the check works (method)"    '^## .*(logic|analysis|method)'
need "verification command + output"   '^## .*Verif'
for h in $(grep -iE '^- (Binary )?SHA-256: [0-9a-f]{64}' "$f" | grep -oE '[0-9a-f]{64}'); do
  grep -q "^$h " scope.txt && echo "ok    hash $(echo $h | cut -c1-12)... is pinned in scope.txt" || { echo "MISS  hash $(echo $h | cut -c1-12)... not in scope.txt"; miss=1; }
done
[ $miss -eq 0 ] && echo "ready to publish" || echo "not ready: fix the MISS lines"; exit $miss
