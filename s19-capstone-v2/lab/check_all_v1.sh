#!/bin/sh
# check_all.sh [A-F...]: run the capstone proofs. Each part prints PASS/FAIL; exit 1 if any part fails.
# Parts: A tests+smoke, B grounded agent run, C hardened token-gated container, D re-assist gate tests,
#        E writeups L1-L3 + signed attestation, F demo checklist complete.
cd "$(dirname "$0")"; V=..; fail=0; parts="${*:-A B C D E F}"
res() { if [ "$2" = 0 ]; then echo "PASS part $1: $3"; else echo "FAIL part $1: $3"; fail=1; fi; }
for p in $parts; do case $p in
A) (cd $V/s10 && python3 -m pytest -q tests >/tmp/cA.log 2>&1 && sh smoke.sh >>/tmp/cA.log 2>&1); res A $? "notes-mcp unit/contract/security tests + Inspector smoke" ;;
B) python3 grounded.py ${B_LOG:-logs/agent_b.jsonl} >/tmp/cB.log 2>&1; res B $? "agent answer grounded in its own tool log (${B_LOG:-logs/agent_b.jsonl})" ;;
C) r=0; [ "$(sh $V/s09/probe.sh | cut -c1-3)" = 401 ] || r=1
   [ "$(sh $V/s09/probe.sh "$(deploy/mint.sh notes:read 120)" | cut -c1-3)" = 200 ] || r=1
   NOTES_TOKEN=$(deploy/mint.sh notes:read 120) python3 $V/s09/http_client.py create a b 2>&1 | grep -q forbidden || r=1
   [ "$(docker inspect -f '{{.HostConfig.ReadonlyRootfs}} {{.Config.User}}' notes-auth 2>/dev/null)" = "true app" ] || r=1
   res C $r "401 without token, 200 with, read token cannot write, read-only non-root container" ;;
D) (cd $V/s18 && python3 -m pytest -q tests >/tmp/cD.log 2>&1); res D $? "re-assist gate tests" ;;
E) r=0; for x in "writeups/l1_cm_strcmp.md bin/cm_strcmp" "writeups/solutions/l2_cm_xor.md bin/cm_xor" "writeups/solutions/l3_cm_obfus.md bin/cm_obfus"; do
     (cd $V/s15 && python3 lab/check_writeup.py $x >/tmp/cE.log 2>&1) || r=1; done
   grep -q '^Signed: [A-Za-z]' $V/s13/ethics/attestation.md || r=1
   res E $r "three writeups pass check_writeup, attestation signed" ;;
F) n=$(grep -c "^- \[ \]" ${CHECKLIST:-demo_checklist.md}); res F $([ "$n" = 0 ] && echo 0 || echo 1) "demo checklist: $n unticked" ;;
esac; done; exit $fail
