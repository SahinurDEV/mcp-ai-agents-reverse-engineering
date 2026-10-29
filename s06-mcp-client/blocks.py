"""blocks.py: how many content blocks does each read tool return?"""
import anyio
from mcp import Client

from list_tools import SERVER


async def main():
    async with Client(SERVER) as c:
        r = await c.call_tool("notes_list", {})
        print("notes_list blocks:", len(r.content), [b.text for b in r.content])
        print("first block only :", r.content[0].text)
        print("structured       :", r.structured_content)


anyio.run(main)
