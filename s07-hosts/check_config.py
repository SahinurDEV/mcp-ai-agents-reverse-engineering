"""check_config.py: start every stdio server in an MCP host config file and list its tools.
Reads Claude Desktop / Claude Code / Cursor files (top-level "mcpServers")
and VS Code files (top-level "servers"), expanding ${workspaceFolder} and ${env:NAME}."""
import json
import os
import re
import sys

import anyio
from mcp import Client, StdioServerParameters


def expand(value: str, workspace: str) -> str:
    value = value.replace("${workspaceFolder}", workspace)
    return re.sub(r"\$\{env:(\w+)\}", lambda m: os.environ.get(m.group(1), ""), value)


def load(path: str) -> dict:
    with open(path) as f:
        cfg = json.load(f)                       # a JSON syntax error stops here, with line and column
    servers = cfg.get("mcpServers") or cfg.get("servers")
    if not servers:
        sys.exit(f"{path}: no 'mcpServers' (Claude, Cursor) or 'servers' (VS Code) key")
    return servers


async def check(name: str, entry: dict, workspace: str):
    if entry.get("type", "stdio") != "stdio" or "command" not in entry:
        print(f"{name:8} skipped: not a stdio server ({entry.get('url', '?')})")
        return
    params = StdioServerParameters(
        command=expand(entry["command"], workspace),
        args=[expand(a, workspace) for a in entry.get("args", [])],
        env={**os.environ, **{k: expand(str(v), workspace) for k, v in entry.get("env", {}).items()}},
    )
    try:
        with anyio.fail_after(30):
            async with Client(params) as c:
                tools = [t.name for t in (await c.list_tools()).tools]
        print(f"{name:8} OK   {len(tools)} tools: {', '.join(tools)}"[:110])
    except BaseException as e:
        while isinstance(e, BaseExceptionGroup):
            e = e.exceptions[0]
        print(f"{name:8} FAIL {type(e).__name__}: {e}"[:110])


async def main(path: str):
    workspace = os.path.dirname(os.path.dirname(os.path.abspath(path)))   # proj/.cursor/mcp.json -> proj
    for name, entry in load(path).items():
        await check(name, entry, workspace)


if __name__ == "__main__":
    anyio.run(main, sys.argv[1])
