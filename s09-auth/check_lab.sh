#!/bin/sh
# check_lab.sh: is the server on :8765 protected? Needs NOTES_TOKEN_KEY in the environment (from .env).
cd "$(dirname "$0")"; ok=0
t() { got=$(./probe.sh "$2" | cut -c1-3); [ "$got" = "$3" ] && echo "PASS $1 ($got)" || { echo "FAIL $1: got $got, want $3"; ok=1; }; }
t "no token is rejected"          ""                                                   401
t "tampered token is rejected"    "$(python3 tokens.py mint notes:read)x"              401
t "other server's token rejected" "$(python3 tokens.py mint notes:read 300 http://other.example/mcp)" 401
t "token without notes:read"      "$(python3 tokens.py mint notes:write)"              403
t "valid read token accepted"     "$(python3 tokens.py mint notes:read)"               200
exit $ok
