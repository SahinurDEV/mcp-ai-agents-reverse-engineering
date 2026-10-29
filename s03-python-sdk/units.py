"""units.py - a tool with a fixed set of choices (Literal -> JSON Schema enum)."""
from typing import Literal
from mcp.server import MCPServer

mcp = MCPServer("units")

@mcp.tool()
def convert_temperature(value: float, direction: Literal["c_to_f", "f_to_c"]) -> float:
    """Convert a temperature. direction is c_to_f (Celsius to Fahrenheit) or f_to_c."""
    if direction == "c_to_f":
        return round(value * 9 / 5 + 32, 2)
    return round((value - 32) * 5 / 9, 2)

if __name__ == "__main__":
    mcp.run()
