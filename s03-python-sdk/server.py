"""Section 3 demo — first MCPServer + @tool (add)."""
from mcp.server import MCPServer

mcp = MCPServer("demo-calc")

@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b

if __name__ == "__main__":
    mcp.run()
