#!/bin/sh
# sandbox.sh BINARY [ARGS...]: run a crackme in a throwaway container: no network, read-only, no capabilities, nobody user, limits
b=$(realpath "$1"); shift
"$(dirname "$0")/re_gate.sh" "$b" >/dev/null || { "$(dirname "$0")/re_gate.sh" "$b"; exit 1; }
exec docker run --rm -i --network none --read-only --cap-drop ALL --security-opt no-new-privileges \
  --user 65534:65534 --pids-limit 32 --memory 128m --cpus 0.5 --tmpfs /tmp:size=8m,noexec \
  -v "$b":/target/bin:ro python:3.13-slim timeout 10 /target/bin "$@"
