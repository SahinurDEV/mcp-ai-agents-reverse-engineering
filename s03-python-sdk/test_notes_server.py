"""In-process tests for notes_server.py: no subprocess, no network."""
import pytest
from mcp import Client
from notes_server import mcp

pytestmark = pytest.mark.anyio

@pytest.fixture
def anyio_backend():
    return "asyncio"

async def test_add_returns_structured_result():
    async with Client(mcp) as c:
        r = await c.call_tool("add", {"a": 2, "b": 3})
        assert not r.is_error
        assert r.structured_content == {"result": 5}

async def test_add_rejects_bad_types():
    async with Client(mcp) as c:
        r = await c.call_tool("add", {"a": 2, "b": "three"})
        assert r.is_error

async def test_template_resource_reads_note():
    async with Client(mcp) as c:
        r = await c.read_resource("notes://ghidra")
        assert "decompiler" in r.contents[0].text

async def test_prompt_mentions_uri():
    async with Client(mcp) as c:
        p = await c.get_prompt("summarize_note", {"name": "mcp"})
        assert "notes://mcp" in p.messages[0].content.text
