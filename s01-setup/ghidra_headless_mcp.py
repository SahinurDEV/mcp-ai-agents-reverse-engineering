"""ghidra-headless MCP server (course lecture 1.1).

Wraps Ghidra's analyzeHeadless so any MCP host or agent can list and
decompile functions in a binary. Only course CrackMes are allowed.
"""
import os, re, subprocess, tempfile
from pathlib import Path
from mcp.server import MCPServer
from mcp.server.mcpserver.exceptions import ToolError
GHIDRA = Path(os.environ.get("GHIDRA_HOME", "/workspace/tools/ghidra/ghidra_12.1.4_PUBLIC"))
SCRIPTS = Path(__file__).resolve().parent.parent / "ghidra_scripts"
ALLOWED = Path(os.environ.get("CRACKME_DIR", "/workspace/mcp-course/crackme/bin")).resolve()

mcp = MCPServer("ghidra-headless")

def _run(binary: str, script: str, *args: str) -> str:
    path = (ALLOWED / binary).resolve()
    if path.parent != ALLOWED or not path.is_file():
        raise ToolError(f"{binary!r} is not a course CrackMe in {ALLOWED}")
    with tempfile.TemporaryDirectory() as proj:
        out = subprocess.run(
            [str(GHIDRA / "support/analyzeHeadless"), proj, "p", "-import", str(path),
             "-scriptPath", str(SCRIPTS), "-postScript", script, *args, "-deleteProject"],
            capture_output=True, text=True, timeout=300).stdout
    m = re.search(r"BEGIN_C.*?\n(.*?)\n[^\n]*END_C", out, re.S)
    if not m:
        raise ToolError("Ghidra produced no output")
    return m.group(1).strip()

@mcp.tool()
def list_functions(binary: str) -> str:
    """List user functions (address and name) in a course CrackMe binary."""
    return _run(binary, "ListFns.java")

@mcp.tool()
def decompile(binary: str, function: str) -> str:
    """Decompile one function of a course CrackMe to C pseudocode with Ghidra."""
    return _run(binary, "DecompileFn.java", function)

if __name__ == "__main__":
    mcp.run()
