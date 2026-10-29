"""noisy.py - a stdio server with a classic bug: print() writes debug text to stdout."""
import sys
from mcp.server import MCPServer

mcp = MCPServer("noisy")
FIXED = "--fixed" in sys.argv

@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two integers."""
    if FIXED:
        print(f"debug: add({a}, {b})", file=sys.stderr)   # logs go to stderr
    else:
        print(f"debug: add({a}, {b})")                    # BUG: stdout is the protocol channel
    return a + b

if __name__ == "__main__":
    mcp.run()
