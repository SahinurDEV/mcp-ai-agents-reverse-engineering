#!/bin/sh
# build.sh: copy the tested server files into the build context, then build notes-mcp-auth:1.0.0
cd "$(dirname "$0")" && rm -rf app && mkdir -p app/s05 app/s09
cp ../../s05-notes-mcp/notes_mcp.py app/s05/ && cp ../../s09-auth/http_notes.py ../../s09-auth/tokens.py app/s09/
docker build --network host -q -t notes-mcp-auth:1.0.0 . >/dev/null && echo "built notes-mcp-auth:1.0.0 from $(ls app/s05 app/s09 | grep -c py) files"
