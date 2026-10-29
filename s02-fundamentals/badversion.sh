#!/usr/bin/env bash
# badversion.sh VERSION — send tools/list claiming an arbitrary protocol version, show the server's answer.
REQ='{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{"_meta":{"io.modelcontextprotocol/protocolVersion":"'"$1"'","io.modelcontextprotocol/clientInfo":{"name":"badversion.sh","version":"1"},"io.modelcontextprotocol/clientCapabilities":{}}}}'
(echo "$REQ"; sleep 1.5) | python "$(dirname "$0")/calc.py" 2>/dev/null | jq -C .
