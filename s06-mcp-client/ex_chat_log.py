"""Exercise 6: the Lab 6 chat CLI plus a JSONL session log and a summary line.

python ex_chat_log.py --approve --log session.jsonl
The log uses the same event format as agent.py, so `agent.py --replay session.jsonl` works on it.
"""
import json
import sys

import anyio
from mcp import Client

from agent import SYSTEM, approved, chat, log, result_text
from list_tools import SERVER, to_openai

ASK = "--approve" in sys.argv
LOG = sys.argv[sys.argv.index("--log") + 1] if "--log" in sys.argv else None


async def main():
    stats = {"calls": 0, "denied": 0, "errors": 0}
    async with Client(SERVER) as mcp:
        listed = (await mcp.list_tools()).tools
        tools = [to_openai(t) for t in listed]
        read_only = {t.name: bool(t.annotations and t.annotations.read_only_hint) for t in listed}
        messages = [{"role": "system", "content": SYSTEM}]
        while True:
            print("you> ", end="", flush=True)
            line = sys.stdin.readline()
            if not sys.stdin.isatty():
                print(line.strip())
            if not line or line.strip() == "quit":
                break
            messages.append({"role": "user", "content": line.strip()})
            log(LOG, kind="task", task=line.strip())
            for _ in range(6):
                msg = chat(messages, tools)
                messages.append(msg)
                calls = msg.get("tool_calls") or []
                if not calls:
                    log(LOG, kind="answer", text=msg.get("content"))
                    print("bot>", msg.get("content"))
                    break
                for call in calls:
                    name, args = call["function"]["name"], json.loads(call["function"]["arguments"] or "{}")
                    print(f"  [tool] {name} {json.dumps(args)}")
                    stats["calls"] += 1
                    if approved(name, args, read_only, ASK):
                        res = await mcp.call_tool(name, args)
                        stats["errors"] += res.is_error
                        out = ("ERROR: " if res.is_error else "") + result_text(res)
                    else:
                        stats["denied"] += 1
                        out = "ERROR: the user denied this tool call. Do not retry it; tell the user."
                    log(LOG, kind="tool", name=name, args=args, result=out, denied=out.startswith("ERROR: the user denied"))
                    messages.append({"role": "tool", "tool_call_id": call["id"], "content": out})
    print(f"bye: {stats['calls']} tool calls, {stats['denied']} denied, {stats['errors']} errors")


if __name__ == "__main__":
    anyio.run(main)
