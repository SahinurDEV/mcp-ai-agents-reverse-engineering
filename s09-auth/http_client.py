"""http_client.py: call the HTTP notes server with the token in $NOTES_TOKEN (if any).
  python3 http_client.py list | get ID | create TITLE BODY"""
import os
import sys

import anyio
import httpx2
from mcp import Client
from mcp.client.streamable_http import streamable_http_client

URL = os.environ.get("NOTES_URL", "http://127.0.0.1:8765/mcp")


async def main(cmd: str, *args: str):
    tok = os.environ.get("NOTES_TOKEN")
    headers = {"Authorization": f"Bearer {tok}"} if tok else {}
    async with httpx2.AsyncClient(headers=headers, timeout=10) as http:
        async with Client(streamable_http_client(URL, http_client=http)) as c:
            if cmd == "list":
                print("tools:", ", ".join(t.name for t in (await c.list_tools()).tools))
                r = await c.call_tool("notes_list", {})
            elif cmd == "get":
                r = await c.call_tool("notes_get", {"note_id": args[0]})
            else:
                r = await c.call_tool("notes_create", {"title": args[0], "body": args[1]})
            print(("ERROR: " if r.is_error else "") + " ".join(b.text for b in r.content if hasattr(b, "text")))


try:
    anyio.run(main, *sys.argv[1:])
except Exception as e:                              # show the HTTP failure in one line, not a traceback
    while isinstance(e, BaseExceptionGroup):
        e = e.exceptions[0]
    print(f"FAILED: {type(e).__name__}: {e}"[:160])
    sys.exit(1)
