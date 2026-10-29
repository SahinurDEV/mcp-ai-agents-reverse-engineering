#!/bin/sh
# smoke.sh: black-box checks of the real server process with the MCP Inspector CLI (10.3). Exit 1 on any failure.
set -u
export NOTES_DIR="$(mktemp -d)"
I="npx --yes @modelcontextprotocol/inspector@2.13.0 --cli -e NOTES_DIR=$NOTES_DIR python3 notes_mcp.py"
fail=0
check() { if eval "$2" >/dev/null 2>&1; then echo "ok   $1"; else echo "FAIL $1"; fail=1; fi; }
check "server starts and lists 4 tools" "[ \$($I --method tools/list | jq '.tools | length') -eq 4 ]"
check "create returns structured id"    "$I --method tools/call --tool-name notes_create --tool-arg title=smoke --tool-arg body=hi | jq -e '.structuredContent.id == \"smoke\"'"
check "traversal is a tool error"       "$I --method tools/call --tool-name notes_get --tool-arg note_id=../etc/passwd | jq -e '.isError == true'"
check "note written inside NOTES_DIR only" "[ \$(ls \$NOTES_DIR) = smoke.md ] && [ ! -e notes ]"
rm -rf "$NOTES_DIR"; exit $fail
