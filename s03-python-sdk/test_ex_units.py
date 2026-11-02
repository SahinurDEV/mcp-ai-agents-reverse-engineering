"""Exercise 3 tests: convert_units and units://{system} through the in-process Client."""
import pytest
from mcp import Client, MCPError
from ex_units import mcp

pytestmark = pytest.mark.anyio

@pytest.fixture
def anyio_backend():
    return "asyncio"

async def test_marathon_in_miles():
    async with Client(mcp) as c:
        r = await c.call_tool("convert_units", {"value": 42.195, "from_unit": "km", "to_unit": "mi"})
        assert r.structured_content == {"result": 26.2188}

async def test_unknown_unit_is_rejected_by_schema():
    async with Client(mcp) as c:
        r = await c.call_tool("convert_units", {"value": 1, "from_unit": "yard", "to_unit": "m"})
        assert r.is_error

async def test_negative_length_is_a_tool_error():
    async with Client(mcp) as c:
        r = await c.call_tool("convert_units", {"value": -1, "from_unit": "m", "to_unit": "cm"})
        assert r.is_error and "negative" in r.content[0].text

async def test_units_resource():
    async with Client(mcp) as c:
        assert (await c.read_resource("units://imperial")).contents[0].text == "mi, ft"
        with pytest.raises(MCPError, match="unknown system"):
            await c.read_resource("units://nautical")

async def test_old_tools_still_there():
    async with Client(mcp) as c:
        names = {t.name for t in (await c.list_tools()).tools}
        assert {"multiply", "divide", "convert_units"} <= names
