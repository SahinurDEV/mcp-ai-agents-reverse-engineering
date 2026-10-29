#!/usr/bin/env bash
# legacy.sh — the pre-2026 stateful handshake: initialize, initialized, then a call.
cd "$(dirname "$0")"
{
  echo '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-06-18","capabilities":{},"clientInfo":{"name":"legacy.sh","version":"1"}}}'
  echo '{"jsonrpc":"2.0","method":"notifications/initialized"}'
  echo '{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"add","arguments":{"a":1,"b":1}}}'
  sleep 1.5
} | python calc.py 2>/dev/null | jq -c 'if .result.serverInfo then {id, protocolVersion: .result.protocolVersion, serverInfo: .result.serverInfo} else {id, text: .result.content[0].text} end'
