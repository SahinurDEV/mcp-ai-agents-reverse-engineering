# Section 14 — AI-assisted RE toolkit (Ghidra 12.1.4 + GhidraMCP 2.0, optional r2mcp)
- `make` builds `hello` (-g -O0) and `hello_s` (-O1 -s). Hashes in ../s13-ethics/scope.txt match gcc 14 on Debian; re-pin if yours differ.
- `source env.sh` (override GHIDRA_INSTALL_DIR / JAVA_HOME / GHIDRAMCP_JAR), sign the attestation in ../s13-ethics, then:
  - `python3 call.py hello decompile_function name=main`
  - `GM_ARGS="--project /tmp/gp --save" python3 call.py hello_s rename_function_by_address function_address=00101159 new_name=main`
  - `R2=1 python3 call.py hello_s analyze level=2 -- list_functions` (r2mcp, sandboxed to this folder)
- `re_agent.py` gives a local model only six read-only tools and logs every call (`--log`).
