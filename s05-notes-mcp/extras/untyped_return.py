"""untyped_return.py: the same create tool returning a bare dict -> no output schema."""
from mcp.server.mcpserver import MCPServer

mcp = MCPServer("untyped")


@mcp.tool()
def notes_create(title: str, body: str) -> dict:
    """Create a note (untyped return)."""
    return {"id": title.lower(), "uri": f"note://{title.lower()}"}


if __name__ == "__main__":
    mcp.run()
