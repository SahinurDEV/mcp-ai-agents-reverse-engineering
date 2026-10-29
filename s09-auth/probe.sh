#!/bin/sh
# probe.sh [TOKEN]: send an MCP initialize over HTTP and print the status and the WWW-Authenticate header
INIT='{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-11-25","capabilities":{},"clientInfo":{"name":"probe","version":"1"}}}'
curl -s -o /dev/null -w '%{http_code} %header{www-authenticate}\n' http://127.0.0.1:8765/mcp \
  -H 'Content-Type: application/json' -H 'Accept: application/json, text/event-stream' \
  ${1:+-H "Authorization: Bearer $1"} -d "$INIT"
