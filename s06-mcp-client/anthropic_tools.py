"""anthropic_tools.py: the same MCP tools in Anthropic Messages API format.

Prints the request body; sends it only if ANTHROPIC_API_KEY is set (the key is never printed).
"""
import json
import os
import sys

import anyio
import httpx
from mcp import Client

from list_tools import SERVER


def to_anthropic(tool) -> dict:
    return {"name": tool.name, "description": tool.description or "", "input_schema": tool.input_schema}


async def main(task: str):
    async with Client(SERVER) as c:
        tools = [to_anthropic(t) for t in (await c.list_tools()).tools]
    body = {"model": os.environ.get("ANTHROPIC_MODEL", "claude-sonnet-4-5"), "max_tokens": 512,
            "system": "You manage the user's notes with the notes_* tools.",
            "messages": [{"role": "user", "content": task}], "tools": tools}
    print(json.dumps({**body, "tools": [t["name"] for t in tools]}, indent=1))
    key = os.environ.get("ANTHROPIC_API_KEY")
    if not key:
        print("ANTHROPIC_API_KEY not set: request not sent")
        return
    r = httpx.post("https://api.anthropic.com/v1/messages", json=body, timeout=60,
                   headers={"x-api-key": key, "anthropic-version": "2023-06-01"})
    for block in r.json().get("content", []):
        print(block.get("type"), block.get("name", ""), json.dumps(block.get("input", block.get("text", ""))))


if __name__ == "__main__":
    anyio.run(main, " ".join(sys.argv[1:]) or "List my notes.")
