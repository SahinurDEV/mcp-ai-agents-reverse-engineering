"""In-process client: exercise every primitive of notes_server.py."""
import asyncio
from mcp import Client
from notes_server import mcp

async def main():
    async with Client(mcp) as c:
        print("tools:     ", [t.name for t in (await c.list_tools()).tools])
        print("resources: ", [str(r.uri) for r in (await c.list_resources()).resources])
        print("templates: ", [t.uri_template for t in (await c.list_resource_templates()).resource_templates])
        r = await c.read_resource("notes://ghidra")
        print("read ghidra ->", r.contents[0].text)
        p = await c.get_prompt("summarize_note", {"name": "mcp", "style": "five words"})
        print("prompt ->", p.messages[0].content.text)

asyncio.run(main())
