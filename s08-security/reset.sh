#!/bin/sh
# reset.sh: clean state for Section 8 demos
cd "$(dirname "$0")" && ./reset_notes.sh >/dev/null && rm -f leaked.txt tools.lock
echo "API_TOKEN=demo-not-a-real-token-1234" > secrets.txt
pkill -f hijacked_llm.py 2>/dev/null; echo "reset"
