#!/usr/bin/env bash
# ex_audit.sh: Exercise 12. Do not trust the Dockerfile, prove it: start the image with the
# compose hardening flags and check every property from inside the running container.
set -u
IMG=${1:-notes-mcp:1.0.0}
FLAGS="--network none --read-only --cap-drop ALL --security-opt no-new-privileges:true"
[ -n "${LOOSE:-}" ] && FLAGS=""        # what a plain docker run gives you
R="docker run --rm $FLAGS -v ex12-data:/data --entrypoint sh $IMG -c"
pass=0; fail=0
check() { if [ "$2" = "$3" ]; then echo "PASS $1 ($2)"; pass=$((pass+1)); else echo "FAIL $1: got '$2', want '$3'"; fail=$((fail+1)); fi; }
check "runs as non-root uid"          "$($R 'id -u')"                                        10001
check "root filesystem is read-only"  "$($R 'touch /usr/x 2>/dev/null && echo writable || echo blocked')" blocked
check "/tmp is read-only too"         "$($R 'touch /tmp/x 2>/dev/null && echo writable || echo blocked')" blocked
check "data volume is writable"       "$($R 'touch /data/probe && echo ok')"                ok
check "no effective capabilities"     "$($R 'grep CapEff /proc/self/status | tr -d "[:space:]"')" CapEff:0000000000000000
check "no-new-privileges is set"      "$($R 'grep NoNewPrivs /proc/self/status | tr -d "[:space:]"')" NoNewPrivs:1
check "no network inside"             "$($R 'python -c "import socket;socket.create_connection((\"1.1.1.1\",53),2)" 2>/dev/null && echo online || echo offline')" offline
docker volume rm ex12-data >/dev/null
echo "$pass passed, $fail failed"; [ $fail -eq 0 ]
