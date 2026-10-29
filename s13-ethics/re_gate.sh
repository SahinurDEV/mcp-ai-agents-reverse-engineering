#!/bin/sh
# re_gate.sh BINARY: refuse unless the attestation is signed and the binary's SHA-256 is in scope.txt
here=$(dirname "$0")
grep -q '^Signed: [^N]' "$here/ethics/attestation.md" 2>/dev/null || { echo "REFUSED: sign ethics/attestation.md first (./sign.sh \"Your Name\")"; exit 1; }
[ -f "$1" ] || { echo "REFUSED: no such file: $1"; exit 1; }
h=$(sha256sum "$1" | cut -d' ' -f1)
line=$(grep "^$h " "$here/scope.txt") || { echo "REFUSED: $1 ($h) is not in scope.txt"; exit 1; }
echo "IN SCOPE: $1 -> ${line#* }"
