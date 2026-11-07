#!/bin/sh
# build.sh: copy the tested server files into the build context, then build notes-mcp-auth:1.0.0
# Folder names match the repo, because http_notes.py imports notes_mcp from ../s05-notes-mcp.
cd "$(dirname "$0")" && rm -rf app && mkdir -p app/s05-notes-mcp app/s09-auth
cp ../../s05-notes-mcp/notes_mcp.py app/s05-notes-mcp/ && cp ../../s09-auth/http_notes.py ../../s09-auth/tokens.py app/s09-auth/
docker build --network host -q -t notes-mcp-auth:1.0.0 . >/dev/null && echo "built notes-mcp-auth:1.0.0 from $(ls app/s05-notes-mcp app/s09-auth | grep -c py) files"
