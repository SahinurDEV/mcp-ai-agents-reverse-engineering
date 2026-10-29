"""pin_tools.py: pin a server's tool definitions by hash, then detect changes.
  python3 pin_tools.py pin   CMD...   writes tools.lock
  python3 pin_tools.py check CMD...   exits 1 if any tool was added, removed or changed"""
import hashlib
import json
import os
import sys

import anyio
from mcp import Client, StdioServerParameters


def digest(tool) -> str:
    spec = {"name": tool.name, "description": tool.description, "inputSchema": tool.input_schema}
    return hashlib.sha256(json.dumps(spec, sort_keys=True).encode()).hexdigest()[:16]


async def main(mode: str, cmd: list[str]):
    async with Client(StdioServerParameters(command=cmd[0], args=cmd[1:], env=dict(os.environ))) as c:
        now = {t.name: digest(t) for t in (await c.list_tools()).tools}
    if mode == "pin":
        json.dump(now, open("tools.lock", "w"), indent=1)
        print("pinned:", ", ".join(f"{n}={h}" for n, h in now.items()))
        return
    pinned = json.load(open("tools.lock"))
    bad = 0
    for name in sorted(pinned.keys() | now.keys()):
        state = "same" if pinned.get(name) == now.get(name) else \
            "ADDED" if name not in pinned else "REMOVED" if name not in now else "CHANGED"
        bad += state != "same"
        print(f"{state:8} {name}  {pinned.get(name, '-')} -> {now.get(name, '-')}")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    anyio.run(main, sys.argv[1], sys.argv[2:])
