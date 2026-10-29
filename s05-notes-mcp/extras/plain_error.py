"""plain_error.py: notes_get raising a plain exception instead of ToolError."""
from mcp.server.mcpserver import MCPServer

mcp = MCPServer("plain-error")


@mcp.tool()
def notes_get(note_id: str) -> str:
    """Return one note."""
    raise FileNotFoundError(f"no note '{note_id}'; call notes_list to see ids")


if __name__ == "__main__":
    mcp.run()
