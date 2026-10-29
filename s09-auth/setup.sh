#!/bin/sh
# setup.sh: fresh notes, a random demo signing key in .env (never committed), server stopped
cd "$(dirname "$0")"
pkill -f http_notes.py 2>/dev/null; sleep 0.3
rm -rf notes && mkdir notes
printf '# Ghidra tips\n\nPress L to rename a symbol.\n' > notes/ghidra-tips.md
printf '# MCP sync\n\nDecide: resource or tool for search?\n' > notes/mcp-sync.md
rm -f .env; umask 077; echo "NOTES_TOKEN_KEY=$(head -c 24 /dev/urandom | base64)" > .env
echo "ready: notes=$(ls notes | tr '\n' ' ') key=.env (random, local only)"
