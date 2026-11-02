"""Exercise 6 fix: replay a session log, but never re-run a call the user denied."""
import json
import sys

import anyio
from mcp import Client

from agent import result_text
from list_tools import SERVER


async def replay(path: str):
    async with Client(SERVER) as mcp:
        for line in open(path):
            e = json.loads(line)
            if e["kind"] != "tool":
                continue
            if e.get("denied"):
                print(f"skip  {e['name']} {json.dumps(e['args'])}  (denied by the user)")
                continue
            res = await mcp.call_tool(e["name"], e["args"])
            now = ("ERROR: " if res.is_error else "") + result_text(res)
            print(f"{'same' if now == e['result'] else 'DIFF'}  {e['name']} {json.dumps(e['args'])}")

anyio.run(replay, sys.argv[1])
