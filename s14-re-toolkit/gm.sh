#!/bin/sh
# gm.sh BINARY [ghidra-mcp args]: GhidraMCP 2.0 headless on one in-scope binary, MCP over stdio
here=$(cd "$(dirname "$0")" && pwd); . "$here/env.sh"
b=$(realpath "$1"); shift
"$here/../s13-ethics/re_gate.sh" "$b" >&2 || exit 1
exec ghidra-mcp --headless --extension-jar "$GHIDRAMCP_JAR" --ghidra-install-dir "$GHIDRA_INSTALL_DIR" --binary "$b" "$@"
