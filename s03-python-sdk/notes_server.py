"""Section 3 demo: tools, resources with URI templates, and prompts."""
from mcp.server import MCPServer

mcp = MCPServer("s03-demo")

NOTES = {
    "mcp": "MCP connects hosts to servers over JSON-RPC.",
    "ghidra": "Ghidra is a free reverse engineering suite with a decompiler.",
}

@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two integers."""
    return a + b

@mcp.resource("notes://index")
def index() -> str:
    """List of all note names, one per line."""
    return "\n".join(sorted(NOTES))

@mcp.resource("notes://{name}")
def note(name: str) -> str:
    """Read one note by name."""
    if name not in NOTES:
        raise ValueError(f"no note named {name!r}")
    return NOTES[name]

@mcp.prompt()
def summarize_note(name: str, style: str = "one sentence") -> str:
    """Ask the model to summarize a note in a given style."""
    return f"Summarize the note notes://{name} in {style}. Quote the note before you summarize it."

if __name__ == "__main__":
    mcp.run()
