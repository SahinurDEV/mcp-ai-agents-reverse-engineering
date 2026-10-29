#!/bin/sh
# lab/check.sh: Section 12 lab checks against the notes-mcp:1.0.1 image
cd "$(dirname "$0")/.."; ok=0
say() { if [ "$2" = 0 ]; then echo "ok   $1"; else echo "FAIL $1"; ok=1; fi; }
R="docker run -i --rm --network none --read-only --cap-drop ALL --security-opt no-new-privileges -v notes-lab:/data:ro --entrypoint notes-mcp notes-mcp:1.0.1"
I="npx --yes @modelcontextprotocol/inspector@2.13.0 --cli $R"
[ "$(docker run --rm --entrypoint notes-mcp notes-mcp:1.0.1 --version 2>/dev/null)" = "notes-mcp 1.0.1" ]; say "image notes-mcp:1.0.1 reports 1.0.1" $?
[ "$(docker run --rm --entrypoint id notes-mcp:1.0.1 -u 2>/dev/null)" = 10001 ]; say "runs as uid 10001" $?
$I --method tools/call --tool-name notes_get --tool-arg note_id=../etc/passwd 2>/dev/null | jq -e '.isError and (.content[0].text | test("invalid id"))' >/dev/null; say "traversal blocked on a read-only volume" $?
$I --method tools/call --tool-name notes_create --tool-arg title=x --tool-arg body=y 2>/dev/null | jq -e '.content[0].text | test("read-only")' >/dev/null; say "read-only save gives a clear error" $?
grep -q '^## \[1.0.1\]' CHANGELOG.md; say "CHANGELOG has a 1.0.1 entry" $?
exit $ok
