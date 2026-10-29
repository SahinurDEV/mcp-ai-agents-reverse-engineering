"""notes_resources.py - lecture 3.5: resource templates with clear not-found errors."""
from mcp.server import MCPServer
from mcp.server.mcpserver.exceptions import ResourceError

mcp = MCPServer("notes-resources")

NOTES = {
    "mcp": "MCP connects hosts to servers over JSON-RPC.",
    "ghidra": "Ghidra is a free reverse engineering suite with a decompiler.",
    "uv": "uv manages Python versions, environments and lockfiles.",
}

@mcp.resource("notes://index", mime_type="text/plain")
def index() -> str:
    """List of all note names, one per line."""
    return "\n".join(sorted(NOTES))

@mcp.resource("notes://{name}", mime_type="text/plain")
def note(name: str) -> str:
    """Read one note by name. Names come from notes://index."""
    if name not in NOTES:
        raise ResourceError(f"no note named {name!r}; read notes://index for valid names")
    return NOTES[name]

@mcp.resource("notes://{name}/words")
def note_words(name: str) -> int:
    """Word count of one note."""
    return len(note(name).split())

if __name__ == "__main__":
    mcp.run()
