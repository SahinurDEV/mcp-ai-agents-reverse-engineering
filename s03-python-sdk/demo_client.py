"""In-process client proof for lecture 3.2."""
import asyncio
from server import mcp
from mcp.client import Client

async def main():
    async with Client(mcp) as c:
        tools = await c.list_tools()
        names = [t.name for t in tools.tools]
        print("tools:", names)
        r = await c.call_tool("add", {"a": 2, "b": 3})
        print("add(2,3) =>", r.content[0].text)

if __name__ == "__main__":
    asyncio.run(main())
