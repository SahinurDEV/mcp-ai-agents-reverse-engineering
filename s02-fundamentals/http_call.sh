#!/usr/bin/env bash
# http_call.sh A B — call calc's add tool over Streamable HTTP with curl (2026-07-28 style).
BODY=$(jq -nc --argjson a "$1" --argjson b "$2" '{jsonrpc:"2.0",id:7,method:"tools/call",
  params:{name:"add",arguments:{a:$a,b:$b},_meta:{"io.modelcontextprotocol/protocolVersion":"2026-07-28",
  "io.modelcontextprotocol/clientInfo":{name:"curl",version:"1"},"io.modelcontextprotocol/clientCapabilities":{}}}}')
curl -s -i http://127.0.0.1:9123/mcp \
  -H 'Content-Type: application/json' -H 'Accept: application/json, text/event-stream' \
  -H 'Mcp-Protocol-Version: 2026-07-28' -H 'Mcp-Method: tools/call' -H 'Mcp-Name: add' \
  -d "$BODY"
echo
