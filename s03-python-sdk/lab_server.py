"""Lab 3.8 solution: calculator tools plus quote resources."""
import random
from mcp.server import MCPServer
from mcp.server.mcpserver.exceptions import ToolError

mcp = MCPServer("calc-quotes")

QUOTES = [
    "Programs must be written for people to read. - Harold Abelson",
    "Simplicity is prerequisite for reliability. - Edsger Dijkstra",
    "Trust, but verify. - Russian proverb",
]

@mcp.tool()
def multiply(a: float, b: float) -> float:
    """Multiply two numbers."""
    return a * b

@mcp.tool()
def divide(a: float, b: float) -> float:
    """Divide a by b. Fails clearly when b is zero."""
    if b == 0:
        raise ToolError("cannot divide by zero; ask the user for a non-zero divisor")
    return a / b

@mcp.resource("quote://random")
def random_quote() -> str:
    """A random programming quote."""
    return random.choice(QUOTES)

@mcp.resource("quote://{index}")
def quote_by_index(index: int) -> str:
    """Quote number index (0-based) from the list."""
    return QUOTES[index]

if __name__ == "__main__":
    mcp.run()
