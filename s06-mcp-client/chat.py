"""chat.py: Lab 6 solution. A multi-turn chat CLI over notes-mcp, with approval for writes."""
import json
import sys

import anyio
from mcp import Client

from agent import SYSTEM, approved, chat, result_text
from list_tools import SERVER, to_openai


ASK = "--approve" in sys.argv               # ask before non-read-only tools


async def main():
    async with Client(SERVER) as mcp:
        listed = (await mcp.list_tools()).tools
        tools = [to_openai(t) for t in listed]
        read_only = {t.name: bool(t.annotations and t.annotations.read_only_hint) for t in listed}
        messages = [{"role": "system", "content": SYSTEM}]
        print("notes chat. Type a request, or 'quit'.")
        while True:
            print("you> ", end="", flush=True)
            line = sys.stdin.readline()
            if not sys.stdin.isatty():
                print(line.strip())
            if not line or line.strip() == "quit":
                break
            messages.append({"role": "user", "content": line.strip()})
            for _ in range(6):                      # tool steps per turn
                msg = chat(messages, tools)
                messages.append(msg)
                calls = msg.get("tool_calls") or []
                if not calls:
                    print("bot>", msg.get("content"))
                    break
                for call in calls:
                    name, args = call["function"]["name"], json.loads(call["function"]["arguments"] or "{}")
                    print(f"  [tool] {name} {json.dumps(args)}")
                    if approved(name, args, read_only, ASK):
                        res = await mcp.call_tool(name, args)
                        out = ("ERROR: " if res.is_error else "") + result_text(res)
                    else:
                        out = "ERROR: the user denied this tool call."
                    messages.append({"role": "tool", "tool_call_id": call["id"], "content": out})
        print(f"bye ({len(messages)} messages in history)")


if __name__ == "__main__":
    anyio.run(main)
