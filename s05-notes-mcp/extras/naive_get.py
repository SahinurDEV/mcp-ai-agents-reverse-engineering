"""naive_get.py: DO NOT COPY. notes_get that joins the id straight into a path."""
from pathlib import Path

from mcp.server.mcpserver import MCPServer

mcp = MCPServer("naive-notes")


@mcp.tool()
def notes_get(note_id: str) -> str:
    """Return one note (unsafe)."""
    return (Path("notes") / note_id).read_text()


if __name__ == "__main__":
    mcp.run()
