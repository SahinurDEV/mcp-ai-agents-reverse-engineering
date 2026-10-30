#!/bin/sh
# pin.sh DIR ORIGIN: verify DIR/SHA256SUMS, then pin every listed binary in ../s13-ethics/scope.txt with ORIGIN
cd "$(dirname "$0")"; d=$1; o=$2
(cd "$d" && sha256sum -c SHA256SUMS) || { echo "REFUSED: checksum mismatch"; exit 1; }
while read h f; do grep -q "^$h " ../s13-ethics/scope.txt || echo "$h $o ../s16-crackmes-b/$d/$f" >> ../s13-ethics/scope.txt; echo "pinned $f ($o)"; done < "$d/SHA256SUMS"
