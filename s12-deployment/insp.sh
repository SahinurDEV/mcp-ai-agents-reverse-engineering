#!/bin/sh
# insp.sh [rw|ro] ARGS...: Inspector CLI against the notes-mcp image over stdio.
# The container gets no network, a read-only root filesystem, no capabilities, and the notes-data volume.
MODE=$1; shift
VOL=notes-data:/data; [ "$MODE" = ro ] && VOL=notes-data:/data:ro
exec npx --yes @modelcontextprotocol/inspector@2.13.0 --cli \
  docker run -i --rm --network none --read-only --cap-drop ALL --security-opt no-new-privileges \
  -v "$VOL" --entrypoint notes-mcp notes-mcp:1.0.0 "$@"
