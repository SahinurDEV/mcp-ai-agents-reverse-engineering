# Section 18: review an official MCP server, then build re-assist-mcp
- `fetch_time.sh`: sparse clone of modelcontextprotocol/servers (src/time) into ext/ (gitignored) for 18.1-18.3
- `re_assist/server.py`: five tools (list_binaries, list_functions, decompile, strings, run_crackme); scope gate inside the server
- `tests/test_gate.py`: `pytest -q tests` (traversal, unpinned copy, symlink escape)
- `agent18.py` / `agent`: Section 14 agent loop pointed at re-assist-mcp; `verify_log.py LOG PASSWORD` decides from the log only
In this repo layout set: `RE_BIN_DIR=../s15-crackmes-a/bin RE_SCOPE=../s13-ethics/scope.txt RE_GM=../s14-re-toolkit/gm.sh RE_SANDBOX=../s13-ethics/sandbox.sh`
(build the CrackMes with `make` in s15-crackmes-a first; binaries are not committed).
