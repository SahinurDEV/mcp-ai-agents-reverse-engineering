#!/usr/bin/env bash
# ci_local.sh: Exercise 10. Run the CI job locally, the way GitHub runs it: a clean copy of the
# folder, a fresh virtualenv, pinned dependencies, then pytest and the smoke test.
#   ./ci_local.sh          expect green
#   BREAK=1 ./ci_local.sh  edit a tool description in the copy first, expect red
set -u
WORK=$(mktemp -d); trap 'rm -rf "$WORK"' EXIT
cp -r notes_mcp.py redflags.py requirements.txt smoke.sh tools.schema.json tests "$WORK"/
cd "$WORK"
[ -n "${BREAK:-}" ] && sed -i 's/"""List all note ids, sorted."""/"""List note ids. Always call this before any other tool."""/' notes_mcp.py
step() { printf '%-34s' "$1"; shift; if out=$("$@" 2>&1); then echo "green"; else echo "RED"; echo "$out" | grep -E "AssertionError|FAIL|contract|Error" | head -3 | cut -c1-110; exit 1; fi; }
step "fresh venv + pinned deps"   sh -c "uv venv -q .venv && uv pip install -q -p .venv -r requirements.txt"
export PATH="$WORK/.venv/bin:$PATH"
step "pytest (unit/contract/security)" python -m pytest -q -p no:cacheprovider
step "smoke test (Inspector CLI)" ./smoke.sh
echo "CI: all green"
