"""scan_tools.py: list a server's tools and flag red flags in their descriptions and schemas."""
import json
import os
import re
import sys

import anyio
from mcp import Client, StdioServerParameters

RED_FLAGS = {
    "hidden-instruction tag": r"<\s*(important|system|instructions?)\s*>",
    "secrecy request": r"do not (mention|tell|show)|don'?t (mention|tell)",
    "file or secret access": r"secret|password|token|\.ssh|\.env|api[_ ]key|credentials?",
    "other tools or servers": r"before using|instead of|other tool|when calling",
}


async def main(cmd: list[str]):
    async with Client(StdioServerParameters(command=cmd[0], args=cmd[1:], env=dict(os.environ))) as c:
        for t in (await c.list_tools()).tools:
            text = (t.description or "") + " " + json.dumps(t.input_schema)   # whole schema: names, descriptions, defaults
            hits = [name for name, rx in RED_FLAGS.items() if re.search(rx, text, re.I)]
            print(f"{'FLAG' if hits else 'ok  '} {t.name:10} {', '.join(hits)}")


if __name__ == "__main__":
    anyio.run(main, sys.argv[1:])
