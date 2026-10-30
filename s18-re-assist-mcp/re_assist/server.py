"""re-assist-mcp: our own RE helper server. Wraps headless GhidraMCP (via ../s14-re-toolkit/gm.sh) and the Docker sandbox.
Only binaries inside BIN_DIR (default ../s15-crackmes-a/bin) whose SHA-256 is pinned in ../s13-ethics/scope.txt can be touched.
Tools: list_binaries, list_functions, decompile, strings, run_crackme. All read-only for the host."""
import hashlib, json, os, re, subprocess
from pathlib import Path
from mcp import Client, StdioServerParameters
from mcp.server.mcpserver import MCPServer
from mcp.server.mcpserver.exceptions import ToolError
from mcp.types import ToolAnnotations

HERE = Path(__file__).resolve().parent
S = HERE.parent.parent                                        # demos/v2
BIN_DIR = Path(os.environ.get("RE_BIN_DIR", S / "s15/bin")).resolve()
SCOPE = Path(os.environ.get("RE_SCOPE", S / "s13/scope.txt"))
GM = os.environ.get("RE_GM", str(S / "s14/gm.sh"))
SANDBOX = os.environ.get("RE_SANDBOX", str(S / "s13/sandbox.sh"))
LOG = os.environ.get("RE_LOG", "/tmp/re_assist.log")
PROJECT = os.environ.get("RE_PROJECT", "/tmp/re_assist_proj")
STUBS = re.compile(r"^(_init|_fini|_start|FUN_00101020|deregister_tm_clones|register_tm_clones|__do_global_dtors_aux|frame_dummy|_DT_INIT|_DT_FINI|_INIT_0|_FINI_0|entry)$")
mcp = MCPServer("re-assist-mcp", log_level="WARNING")
RO = ToolAnnotations(readOnlyHint=True, openWorldHint=False)

def gate(binary: str) -> Path:
    """Scope gate: a bare file name inside BIN_DIR, pinned in scope.txt. Anything else is refused."""
    if not re.fullmatch(r"[A-Za-z0-9_.-]{1,64}", binary) or binary.startswith("."):
        raise ToolError(f"refused: '{binary}' is not a plain file name (no paths allowed)")
    p = (BIN_DIR / binary).resolve()
    if not p.is_relative_to(BIN_DIR) or not p.is_file():
        raise ToolError(f"refused: no binary '{binary}' in the course binaries folder")
    h = hashlib.sha256(p.read_bytes()).hexdigest()
    if not any(l.startswith(h + " ") for l in SCOPE.read_text().splitlines()):
        raise ToolError(f"refused: {binary} ({h[:12]}...) is not pinned in scope.txt")
    return p

async def ghidra(p: Path, tool: str, args: dict) -> str:
    os.makedirs(PROJECT, exist_ok=True)
    # Ghidra logs to stderr; keep it out of the MCP host's view, in RE_LOG
    params = StdioServerParameters(command="sh", args=["-c", 'exec "$0" "$1" --project "$2" --save 2>>"$3"', GM, str(p), PROJECT, LOG],
                                   env={"PATH": os.environ["PATH"], "HOME": os.environ["HOME"]})
    async with Client(params) as c:
        r = await c.call_tool(tool, args)
    text = "\n".join(getattr(x, "text", "") for x in r.content)
    if r.is_error: raise ToolError(f"ghidra {tool} failed: {text[:300]}")
    return text

@mcp.tool(annotations=RO)
def list_binaries() -> list[str]:
    """Names of the course binaries this server may analyse (in scope and pinned)."""
    out = []
    for f in sorted(BIN_DIR.iterdir()):
        try: gate(f.name); out.append(f.name)
        except ToolError: pass
    return out

@mcp.tool(annotations=RO)
async def list_functions(binary: str, author_only: bool = True) -> list[dict]:
    """Functions in BINARY as {name, address}. author_only drops imports and GCC/libc startup stubs."""
    items = json.loads(await ghidra(gate(binary), "list_functions", {})).get("items", [])
    return [{"name": i["name"], "address": i.get("address")} for i in items
            if not author_only or ("EXTERNAL" not in i["name"] and not STUBS.match(i["name"]))]

@mcp.tool(annotations=RO)
async def decompile(binary: str, function: str) -> str:
    """Decompiled C for one function, by name (e.g. main or FUN_00101080)."""
    if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]{0,63}", function): raise ToolError("function must be a plain identifier")
    t = await ghidra(gate(binary), "decompile_function", {"name": function})
    try: t = json.loads(t).get("code", t)
    except ValueError: pass
    return t.strip()[:6000]

@mcp.tool(annotations=RO)
async def strings(binary: str, min_len: int = 6) -> list[dict]:
    """Defined strings of at least min_len characters, as {address, value}. Skips section names and the
    loader/dynamic-symbol area below 0x101000 (library and symbol names, not program text)."""
    items = json.loads(await ghidra(gate(binary), "list_strings", {})).get("items", [])
    return [{"address": i["address"], "value": i["value"]} for i in items
            if len(i.get("value", "")) >= min_len and re.fullmatch(r"[0-9a-f]{8}", str(i["address"])) and int(i["address"], 16) >= 0x101000][:80]

@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True, openWorldHint=False, destructiveHint=False))
def run_crackme(binary: str, args: list[str]) -> dict:
    """Run BINARY with ARGS inside the sandbox container (no network, read-only, nobody, 10 s). Returns exit code and output."""
    p = gate(binary)
    if len(args) > 4 or any(len(a) > 64 for a in args): raise ToolError("at most 4 arguments of up to 64 characters")
    r = subprocess.run([SANDBOX, str(p), *args], capture_output=True, text=True, timeout=60)
    return {"exit_code": r.returncode, "stdout": r.stdout[-1000:], "stderr": r.stderr[-300:]}

if __name__ == "__main__":
    mcp.run()
