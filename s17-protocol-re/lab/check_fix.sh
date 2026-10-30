#!/bin/sh
# check_fix.sh: restart toyapi from YOUR edited toyapi.py and test the owner check (bob must not read alice's note 1)
cd "$(dirname "$0")/.." && ./up.sh >/dev/null
out=$(python3 myclient.py bob builder /notes/3 /notes/1 /notes/99)
echo "$out"
echo "$out" | grep -q "^/notes/3 200" || { echo "FAIL: bob can no longer read his own note"; exit 1; }
echo "$out" | grep -q "^/notes/1 200" && { echo "FAIL: bob can read alice's note 1 (IDOR still there)"; exit 1; }
echo "PASS: owner check works"
