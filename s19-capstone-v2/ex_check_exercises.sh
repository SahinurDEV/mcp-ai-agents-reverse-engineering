#!/bin/sh
# ex_check_exercises.sh: Exercise 19. One command that proves every section exercise still works,
# in the same PASS/FAIL style as check_all.sh. Run it before you call the capstone done.
cd "$(dirname "$0")/.."; fail=0
t() { name=$1; shift; if sh -c "$*" >/tmp/ex19.log 2>&1; then echo "PASS $name"; else echo "FAIL $name (see /tmp/ex19.log)"; fail=1; fi; }
t " 3 convert_units + units://{system}"  "cd s03-python-sdk && python3 -m pytest -q test_ex_units.py"
t " 5 notes_rename refuses traversal"     "cd s05-notes-mcp && python3 -m pytest -q test_ex_rename.py"
t " 7 VS Code config starts from any cwd" "cd /tmp && python3 $PWD/s07-hosts/check_config.py $PWD/s07-hosts/ex/.vscode/mcp.json | grep -q ' OK '"
t " 8 pin catches the sneaky update"      "cd s08-security && python3 pin_tools.py pin python3 ex_sneaky_server.py && ! SNEAKY=1 python3 pin_tools.py check python3 ex_sneaky_server.py; r=\$?; rm -f tools.lock; exit \$r"
t "10 local CI green, broken CI red"      "cd s10-testing-ci && ./ci_local.sh && ! BREAK=1 ./ci_local.sh"
t "12 container hardening audit"          "cd s12-deployment && ./ex_audit.sh"
t "16 keygen on 12 names in the sandbox"  "cd s16-crackmes-b && python3 ex_keygen_check.py"
t "18 who_calls is gated and read-only"   "cd s18-re-assist-mcp && python3 -m pytest -q tests/test_ex_xrefs.py"
exit $fail
