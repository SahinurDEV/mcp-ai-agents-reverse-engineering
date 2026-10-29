#!/bin/sh
# reset_notes.sh: recreate ./notes with three sample notes
rm -rf notes && mkdir notes
printf '# Ghidra tips\n\nPress L to rename a symbol. Decision: use headless mode in CI.\n' > notes/ghidra-tips.md
printf '# MCP sync\n\nOpen question: do we expose search as a resource or a tool?\n' > notes/mcp-sync.md
printf '# Crackme log\n\nSolved crackme01 by patching the JNZ. Next: try crackme02.\n' > notes/crackme-log.md
echo "notes: $(ls notes | tr '\n' ' ')"
