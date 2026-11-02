"""Exercise 3: extend the lab server with convert_units and a units://{system} resource."""
from typing import Literal
from mcp.server.mcpserver.exceptions import ResourceError, ToolError
from mcp.types import ToolAnnotations
from lab_server import mcp

FACTORS = {"km": 1000.0, "m": 1.0, "cm": 0.01, "mi": 1609.344, "ft": 0.3048}
SYSTEMS = {"metric": ["km", "m", "cm"], "imperial": ["mi", "ft"]}
Unit = Literal["km", "m", "cm", "mi", "ft"]

@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True, idempotentHint=True, openWorldHint=False))
def convert_units(value: float, from_unit: Unit, to_unit: Unit) -> float:
    """Convert a length between km, m, cm, mi and ft. Rounded to 4 decimals."""
    if value < 0:
        raise ToolError("length cannot be negative")
    return round(value * FACTORS[from_unit] / FACTORS[to_unit], 4)

@mcp.resource("units://{system}")
def units(system: str) -> str:
    """The length units in one system: metric or imperial."""
    if system not in SYSTEMS:
        raise ResourceError(f"unknown system {system!r}; use metric or imperial")
    return ", ".join(SYSTEMS[system])

if __name__ == "__main__":
    mcp.run()
