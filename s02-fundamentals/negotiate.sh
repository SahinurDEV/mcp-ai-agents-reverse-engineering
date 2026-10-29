#!/usr/bin/env bash
# negotiate.sh VERSION - legacy initialize proposing VERSION; print the version the server picks.
REQ='{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"'"$1"'","capabilities":{},"clientInfo":{"name":"negotiate.sh","version":"1"}}}'
(echo "$REQ"; sleep 1.5) | python "$(dirname "$0")/calc.py" 2>/dev/null | jq -c '{proposed: "'"$1"'", server_picked: .result.protocolVersion}'
