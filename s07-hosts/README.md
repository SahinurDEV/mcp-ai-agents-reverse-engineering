# Section 7 — Hosts

`./setup.sh` writes host config files with absolute paths for your machine:

| File | Format | Real location in that host |
|---|---|---|
| `claude_desktop_config.json` | `mcpServers` | macOS `~/Library/Application Support/Claude/`, Windows `%APPDATA%\Claude\` |
| `proj/.cursor/mcp.json` | `mcpServers`, `${workspaceFolder}` | project `.cursor/mcp.json` or `~/.cursor/mcp.json` |
| `proj/.vscode/mcp.json` | `servers` + `"type": "stdio"` | workspace `.vscode/mcp.json` or user profile `mcp.json` |
| `host.json` | `mcpServers` | filesystem server (scoped to `sandbox/`) + Context7 |
| `broken/*.json` | — | four broken configs for lecture 7.6 |

`check_config.py FILE` starts every stdio server in any of these formats and lists its tools.

The course recordings run these files live in [MCPHost](https://github.com/mark3labs/mcphost) (open source, v0.34.0)
with a local Ollama model, not in Claude, Cursor or VS Code:

```sh
mcphost --config claude_desktop_config.json -m ollama:course-qwen -p "List my notes."
```
