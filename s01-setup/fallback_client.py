"""Course fallback client: launch any stdio MCP server and call one tool.

Usage: python s01/fallback_client.py TOOL key=value ... -- server command
No Claude or Cursor account needed.
"""
import asyncio, sys
from mcp import Client, StdioServerParameters

async def main(argv):
    i = argv.index("--")
    tool, kv, cmd = argv[0], argv[1:i], argv[i + 1:]
    args = dict(p.split("=", 1) for p in kv)
    params = StdioServerParameters(command=cmd[0], args=cmd[1:])
    async with Client(params) as client:
        tools = await client.list_tools()
        print("server offers:", ", ".join(t.name for t in tools.tools))
        result = await client.call_tool(tool, args)
        print(f"{tool} ->", result.content[0].text)

if __name__ == "__main__":
    asyncio.run(main(sys.argv[1:]))
