#!/bin/sh
# ex_portfolio.sh [OUT]: Exercise 20. Turn your course work into a portfolio page built from EVIDENCE:
# every line comes from a command that just ran, not from memory. Default OUT: PORTFOLIO.md
cd "$(dirname "$0")/.."; OUT=${1:-s20-wrap-v2/PORTFOLIO.md}
count() { (cd "$1" && python3 -m pytest -q --co $2 2>/dev/null | grep -cE '::'); }
{
echo "# MCP + reverse engineering portfolio"
echo
echo "Generated $(date '+%Y-%m-%d %H:%M %Z') by s20-wrap-v2/ex_portfolio.sh. Every number below was measured just now."
echo
echo "## What I built"
echo "- notes-mcp server: $(count s10-testing-ci tests) automated tests (unit, contract, security) + Inspector smoke test"
echo "- re-assist-mcp: $(count s18-re-assist-mcp tests) gate tests; refuses paths, unpinned copies and symlink escapes"
echo "- Exercise extensions: convert_units ($(count s03-python-sdk test_ex_units.py) tests), notes_rename ($(count s05-notes-mcp test_ex_rename.py) tests), who_calls"
echo
echo "## Capstone proof (s19-capstone-v2/check_all.sh)"
s19-capstone-v2/check_all.sh A B C D E 2>/dev/null | sed 's/^/- /'
echo
echo "## Exercise proof (s19-capstone-v2/ex_check_exercises.sh)"
s19-capstone-v2/ex_check_exercises.sh 2>/dev/null | sed 's/^/- /'
echo
echo "## Reverse-engineering writeups"
for w in s15-crackmes-a/writeups/l1_cm_strcmp.md s16-crackmes-b/writeups/tb_lic.md; do echo "- $w: $(sed -n 1p $w | sed 's/^# //')"; done
echo
echo "## Rules I work by"
echo "- Only binaries pinned in scope.txt: $(grep -c . s13-ethics/scope.txt) hashes, attestation $(grep -q '^Signed: [A-Za-z]' s13-ethics/ethics/attestation.md && echo signed || echo NOT signed)"
} > "$OUT"
echo "wrote $OUT ($(grep -c 'PASS' "$OUT") PASS, $(grep -c 'FAIL' "$OUT") FAIL)"
