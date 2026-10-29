"""Lab 3.8 tests: prove multiply, divide and the quote resources."""
import pytest
from mcp import Client, MCPError
from lab_server import mcp, QUOTES

pytestmark = pytest.mark.anyio

@pytest.fixture
def anyio_backend():
    return "asyncio"

async def test_multiply():
    async with Client(mcp) as c:
        assert (await c.call_tool("multiply", {"a": 6, "b": 7})).structured_content == {"result": 42.0}

async def test_divide_by_zero_is_a_tool_error():
    async with Client(mcp) as c:
        r = await c.call_tool("divide", {"a": 1, "b": 0})
        assert r.is_error and "non-zero divisor" in r.content[0].text

async def test_random_quote_is_from_the_list():
    async with Client(mcp) as c:
        assert (await c.read_resource("quote://random")).contents[0].text in QUOTES

async def test_quote_index_out_of_range():
    async with Client(mcp) as c:
        with pytest.raises(MCPError, match="index must be 0 to 2"):
            await c.read_resource("quote://9")
