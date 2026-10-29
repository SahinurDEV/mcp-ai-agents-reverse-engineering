"""Section 2 demo server: one tool, one resource, one prompt.

python calc.py          -> stdio transport
python calc.py http     -> Streamable HTTP on http://127.0.0.1:9123/mcp
"""
import sys
from mcp.server import MCPServer

mcp = MCPServer("calc")

@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two integers and return the sum."""
    return a + b

@mcp.resource("calc://constants")
def constants() -> str:
    """Named constants the app may load into context."""
    return "pi=3.14159\ne=2.71828\nanswer=42"

@mcp.prompt()
def explain(expression: str) -> str:
    """Ask the model to explain an arithmetic expression step by step."""
    return f"Explain, step by step, how to evaluate: {expression}"

if __name__ == "__main__":
    if sys.argv[1:] == ["http"]:
        mcp.run("streamable-http", host="127.0.0.1", port=9123)
    else:
        mcp.run()
