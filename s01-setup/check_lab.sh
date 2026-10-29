#!/usr/bin/env bash
# check_lab.sh — verify the Linux lab machine for the MCP + RE course.
ok=0; bad=0
need() { # name, command, minimum version, actual version
  if [ -z "$4" ]; then printf '  [MISSING] %-8s install it (see s01-setup/README.md)\n' "$1"; bad=$((bad+1)); return; fi
  if [ "$(printf '%s\n%s\n' "$3" "$4" | sort -V | head -1)" = "$3" ]; then
    printf '  [ OK ]    %-8s %s (need >= %s)\n' "$1" "$4" "$3"; ok=$((ok+1))
  else printf '  [ OLD ]   %-8s %s (need >= %s)\n' "$1" "$4" "$3"; bad=$((bad+1)); fi
}
ver() { grep -oE '[0-9]+\.[0-9]+(\.[0-9]+)?' | head -1; }
echo "Lab check on $(uname -sm)"
need python 'python3' 3.11   "$(python3 --version 2>&1 | ver)"
need uv     'uv'      0.5    "$(uv --version 2>/dev/null | ver)"
need node   'node'    22.19  "$(node -v 2>/dev/null | ver)"
need gcc    'gcc'     12     "$(gcc -dumpfullversion 2>/dev/null)"
need make   'make'    4.0    "$(make --version 2>/dev/null | ver)"
need java   'java'    21     "$(java -version 2>&1 | ver)"
need jq     'jq'      1.6    "$(jq --version 2>/dev/null | ver)"
if [ -x "${GHIDRA_HOME:-/workspace/tools/ghidra/ghidra_12.1.4_PUBLIC}/support/analyzeHeadless" ]; then
  echo "  [ OK ]    ghidra   analyzeHeadless found"; ok=$((ok+1))
else echo "  [MISSING] ghidra   set GHIDRA_HOME"; bad=$((bad+1)); fi
echo "$ok ok, $bad to fix"; [ $bad -eq 0 ]
