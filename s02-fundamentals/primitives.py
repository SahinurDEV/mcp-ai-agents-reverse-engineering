"""primitives.py - list every tool, resource and prompt calc.py exposes, then use one of each."""
import anyio
from mcp import Client, StdioServerParameters

async def main():
    async with Client(StdioServerParameters(command="python", args=["calc.py"])) as c:
        print("tools:    ", [t.name for t in (await c.list_tools()).tools])
        print("resources:", [str(r.uri) for r in (await c.list_resources()).resources])
        print("prompts:  ", [p.name for p in (await c.list_prompts()).prompts])
        print("call add  ->", (await c.call_tool("add", {"a": 2, "b": 40})).structured_content)
        print("read      ->", (await c.read_resource("calc://constants")).contents[0].text.split())
        msg = (await c.get_prompt("explain", {"expression": "2*(3+4)"})).messages[0]
        print("prompt    ->", msg.role, "|", msg.content.text)

anyio.run(main)
