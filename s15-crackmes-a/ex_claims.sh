#!/bin/sh
# ex_claims.sh BINARY CANDIDATE...: Exercise 15. Never trust a password an agent "found":
# run every candidate in the Section 13 sandbox and keep only what the binary itself accepts.
b=$1; shift
for c in "$@"; do
  out=$(../s13-ethics/sandbox.sh "$b" "$c" 2>&1 | tail -1)
  if echo "$out" | grep -qiE "correct|accepted|granted|welcome"; then v=ACCEPTED; else v=rejected; fi
  printf "%-22s %-10s %s\n" "$c" "$v" "$out"
done
