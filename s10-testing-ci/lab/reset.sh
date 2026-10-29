#!/bin/sh
# lab/reset.sh: put the Section 10 project back to its committed state after the lab
cd "$(dirname "$0")/.." && cp lab/.orig/notes_mcp.py lab/.orig/tools.schema.json . && rm -f tests/test_delete.py; sed -i "s/-eq 5/-eq 4/; s/lists 5 tools/lists 4 tools/" smoke.sh && echo reset
