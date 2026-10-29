#!/bin/sh
# lab/reset.sh: back to 1.0.0 (source, pyproject, changelog); remove the lab image and volume
cd "$(dirname "$0")/.." && cp lab/.orig/server.py src/notes_mcp/server.py && cp lab/.orig/pyproject.toml lab/.orig/CHANGELOG.md . \
 && docker rmi -f notes-mcp:1.0.1 >/dev/null 2>&1; docker volume rm -f notes-lab >/dev/null 2>&1; echo reset
