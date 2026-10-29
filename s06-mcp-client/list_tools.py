"""list_tools.py: launch notes-mcp over stdio and print its tools as LLM function specs."""
import json
import os
import sys

import anyio
from mcp import Client, StdioServerParameters

SERVER = StdioServerParameters(
    command=sys.executable,
    args=[os.path.join(os.path.dirname(__file__), "..", "s05-notes-mcp", "notes_mcp.py")],
    env={"NOTES_DIR": os.environ.get("NOTES_DIR", "notes")},
)


def to_openai(tool) -> dict:
    """MCP tool -> OpenAI-style function spec. inputSchema is already JSON Schema."""
    return {"type": "function",
            "function": {"name": tool.name, "description": tool.description or "", "parameters": tool.input_schema}}


async def main():
    async with Client(SERVER) as c:
        print("server:", c.server_info.name, "| protocol:", c.protocol_version)
        tools = (await c.list_tools()).tools
        for t in tools:
            print(f"- {t.name:13} readOnly={t.annotations.read_only_hint if t.annotations else None}")
        if "--json" in sys.argv:
            print(json.dumps(to_openai(tools[3]), indent=1))


if __name__ == "__main__":
    anyio.run(main)
