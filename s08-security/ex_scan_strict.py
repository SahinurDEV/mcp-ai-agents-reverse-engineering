"""ex_scan_strict.py: Exercise 8 scanner upgrade. Keyword flags miss reworded attacks, so also
flag any description that tells the model to read, send or append data, or that is unusually long."""
import json, os, re, sys
import anyio
from mcp import Client, StdioServerParameters
from scan_tools import RED_FLAGS

STRICT = {**RED_FLAGS,
          "data-moving verb": r"\b(read|append|send|upload|include|attach)\b.{0,40}\b(file|contents?|folder|home)\b",
          "home-dir reference": r"home|~/|id_rsa|dot-s",
          "too long (>200 chars)": r"^.{201,}$"}


async def main(cmd):
    async with Client(StdioServerParameters(command=cmd[0], args=cmd[1:], env=dict(os.environ))) as c:
        for t in (await c.list_tools()).tools:
            text = (t.description or "") + " " + json.dumps(t.input_schema)
            hits = [n for n, rx in STRICT.items() if re.search(rx, text, re.I | re.S)]
            print(f"{'FLAG' if hits else 'ok  '} {t.name:10} {', '.join(hits)}")

anyio.run(main, sys.argv[1:])
