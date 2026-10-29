#!/usr/bin/env bash
# rpc.sh METHOD [PARAMS_JSON] — send one modern (2026-07-28) JSON-RPC request to calc.py over stdio.
META='"_meta":{"io.modelcontextprotocol/protocolVersion":"2026-07-28","io.modelcontextprotocol/clientInfo":{"name":"rpc.sh","version":"1"},"io.modelcontextprotocol/clientCapabilities":{}}'
P=${2:-'{}'}; P=$(jq -c ". + {$META}" <<<"$P")
REQ="{\"jsonrpc\":\"2.0\",\"id\":1,\"method\":\"$1\",\"params\":$P}"
echo ">>> $REQ" | cut -c1-160
(echo "$REQ"; sleep 1.5) | python "$(dirname "$0")/calc.py" 2>/dev/null | jq -C 'del(.result._meta?)'
