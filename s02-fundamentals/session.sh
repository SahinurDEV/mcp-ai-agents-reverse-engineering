#!/usr/bin/env bash
# session.sh — Exercise 2: one stdio session, four hand-written JSON-RPC requests to calc.py.
META='"_meta":{"io.modelcontextprotocol/protocolVersion":"2026-07-28","io.modelcontextprotocol/clientInfo":{"name":"session.sh","version":"1"},"io.modelcontextprotocol/clientCapabilities":{}}'
req(){ printf '{"jsonrpc":"2.0","id":%s,"method":"%s","params":{%s%s}}\n' "$1" "$2" "$3" "$META"; }
{ req 1 tools/list ""
  req 2 tools/call '"name":"add","arguments":{"a":40,"b":2},'
  req 3 resources/read '"uri":"calc://constants",'
  req 4 tools/explode ""
  sleep 2; } | python3 "$(dirname "$0")/calc.py" 2>/dev/null
