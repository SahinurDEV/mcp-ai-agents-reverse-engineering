"""call.py BINARY (or R2=1 for r2mcp -s HERE -e R2_TOOLS) TOOL [k=v ...] [-- TOOL k=v ...]: several GhidraMCP calls in ONE session (one import/analysis).
Values are parsed as JSON when possible. Prints each tool's text result."""
import json, os, subprocess, sys
import anyio
from mcp import Client, StdioServerParameters

R2_TOOLS = ["open_file", "analyze", "list_functions", "list_imports", "list_strings", "decompile_function", "disassemble_function"]
HERE = os.path.dirname(os.path.abspath(__file__))

def jv(v):
    try: return json.loads(v)
    except ValueError: return v

def parse(argv):
    calls, cur = [], None
    for a in argv:
        if a == "--": cur = None; continue
        if cur is None: cur = [a, {}]; calls.append(cur); continue
        k, _, v = a.partition("="); cur[1][k] = jv(v)
    return calls

async def main():
    binary, calls = sys.argv[1], parse(sys.argv[2:])
    if os.environ.get("R2") and subprocess.run([f"{HERE}/../s13-ethics/re_gate.sh", binary], stdout=sys.stderr).returncode:
        sys.exit(1)
    if os.environ.get("R2"):  # radare2's r2mcp: allow-listed tools only, files limited to this folder (-s)
        params = StdioServerParameters(command="r2mcp", args=["-s", HERE, *[x for t in R2_TOOLS for x in ("-e", t)]], env={"PATH": os.environ["PATH"], "HOME": os.environ["HOME"]})
        calls.insert(0, ["open_file", {"file_path": os.path.realpath(binary)}])
    else:
      params = StdioServerParameters(command=f"{HERE}/gm.sh", args=[binary, *os.environ.get("GM_ARGS", "").split()], env={"PATH": os.environ["PATH"], "HOME": os.environ["HOME"]})
    async with Client(params) as c:
        for name, args in calls:
            try:
                r = await c.call_tool(name, args)
            except Exception as e:  # protocol-level refusal (e.g. tool hidden in this mode)
                print(f"### {name} {json.dumps(args)}  [REFUSED] {e}"); continue
            text = "\n".join(getattr(x, "text", "") for x in r.content)
            print(f"### {name} {json.dumps(args)}{'  [ERROR]' if r.is_error else ''}")
            try: d = json.loads(text); print(d.get("code") if isinstance(d, dict) and "code" in d else json.dumps(d, indent=1)[:3000])
            except ValueError: print(text[:3000])

anyio.run(main)
