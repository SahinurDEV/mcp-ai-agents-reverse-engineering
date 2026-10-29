"""smoke_client.py: connect to notes-mcp over Streamable HTTP and check it answers (the compose sidecar)."""
import os
import sys

import anyio
from mcp import Client

URL = os.environ.get("MCP_URL", "http://127.0.0.1:8000/mcp")


async def main():
    async with Client(URL) as c:
        tools = sorted(t.name for t in (await c.list_tools()).tools)
        r = await c.call_tool("notes_get", {"note_id": "../etc/passwd"})
        print(f"server {c.server_info.name} {c.server_info.version}: {len(tools)} tools; traversal refused={r.is_error}")
        sys.exit(0 if len(tools) == 4 and r.is_error else 1)

anyio.run(main)
