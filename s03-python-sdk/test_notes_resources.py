"""Tests for notes_resources.py, including the error path."""
import pytest
from mcp import Client, MCPError
from notes_resources import mcp

pytestmark = pytest.mark.anyio

@pytest.fixture
def anyio_backend():
    return "asyncio"

async def test_word_count_template():
    async with Client(mcp) as c:
        r = await c.read_resource("notes://uv/words")
        assert r.contents[0].text == "7"

async def test_missing_note_has_helpful_error():
    async with Client(mcp) as c:
        with pytest.raises(MCPError, match="read notes://index"):
            await c.read_resource("notes://nope")
