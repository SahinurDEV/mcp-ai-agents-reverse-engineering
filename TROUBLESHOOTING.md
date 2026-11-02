# Troubleshooting

- **Server not showing in the host:** use absolute paths in the config, restart the host fully, and read the host's MCP log. On stdio, `print()` to stdout corrupts the protocol, so log to stderr.
- **`spawn uv ENOENT` / `command not found`:** hosts do not load your shell PATH. Put the full path to `uv`/`node` in the config.
- **The Inspector connects but lists no tools:** check that the server advertised the `tools` capability, and run `npx @modelcontextprotocol/inspector --cli ... --method tools/list`.
- **Streamable HTTP 401/403:** check the `Authorization: Bearer` header and the token scopes (Section 9), and that the clock is in sync for expiring tokens.
- **Ghidra headless fails:** you need JDK 21+. Set `GHIDRA_INSTALL_DIR`, and close the GUI project first because the lock files block headless runs.
- **GhidraMCP times out:** the first auto-analysis is slow. Wait for it to finish before you call `decompile`.
- **The agent invents functions or keys:** confirm every claim in Ghidra or by running the binary in the sandbox (see 15.5 and 15.7).
- **Docker permission denied on the volume:** match the container UID to the volume owner, or `chown` the data directory.
- **`git log` or another tool hangs in scripts:** set `GIT_PAGER=cat PAGER=cat`.
