#!/bin/sh
# check_lab.sh: three Inspector CLI assertions for the Lab 5 server
cd "$(dirname "$0")" && ./reset_notes.sh >/dev/null
I="npx --yes @modelcontextprotocol/inspector --cli -e NOTES_DIR=notes python3 notes_lab.py"
fail=0
check() { if [ "$2" = "$3" ]; then echo "PASS $1"; else echo "FAIL $1: got '$2' want '$3'"; fail=1; fi; }
check "tag returns tags" "$($I --method tools/call --tool-name notes_tag --tool-arg note_id=mcp-sync --tool-arg tag=todo 2>/dev/null | jq -c .structuredContent.result)" '["todo"]'
$I --method tools/call --tool-name notes_delete --tool-arg note_id=mcp-sync >/dev/null 2>&1
check "deleted note hidden from list" "$($I --method tools/call --tool-name notes_list 2>/dev/null | jq -c .structuredContent.result)" '["crackme-log","ghidra-tips"]'
check "delete is marked destructive" "$($I --method tools/list 2>/dev/null | jq -r '.tools[] | select(.name=="notes_delete") | .annotations.destructiveHint')" 'true'
exit $fail
