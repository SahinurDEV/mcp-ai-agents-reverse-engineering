#!/bin/sh
# check_lab.sh: Section 11 lab checks (run after your lab plan)
cd "$(dirname "$0")"; P=${1:-policy_lab.json}; ok=0
H="python3 hub.py --servers servers.json --policy $P"
say() { if [ "$2" = 0 ]; then echo "ok   $1"; else echo "FAIL $1"; ok=1; fi; }
v=$($H --only notes,files,git tools 2>/dev/null)
echo "$v" | grep -q "^files__" ; say "no files tools visible" $((1-$?))
echo "$v" | grep -q "git__git_reset" ; say "git_reset not visible" $((1-$?))
git -C work/notes log --format=%s | grep -q "^Add standup note" ; say "commit 'Add standup note' exists" $?
grep -q "ship v2 on Friday" work/notes/standup.md 2>/dev/null; say "note holds the team standup text" $?
exit $ok
