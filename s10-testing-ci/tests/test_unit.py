"""10.2 in-process unit tests: the server object runs inside pytest, no subprocess, no network."""
import pytest
from mcp import Client

pytestmark = pytest.mark.anyio


async def test_create_then_get(server):
    async with Client(server) as c:
        r = await c.call_tool("notes_create", {"title": "Ghidra tips", "body": "Press L to rename."})
        assert r.structured_content == {"id": "ghidra-tips", "uri": "note://ghidra-tips"}
        r = await c.call_tool("notes_get", {"note_id": "ghidra-tips"})
        assert "Press L" in r.content[0].text


async def test_duplicate_is_a_tool_error(server):
    async with Client(server) as c:
        await c.call_tool("notes_create", {"title": "a", "body": "1"})
        r = await c.call_tool("notes_create", {"title": "a", "body": "2"})
        assert r.is_error and "already exists" in r.content[0].text


@pytest.mark.parametrize("bad", ["../etc/passwd", "..", "a/b", "/etc/passwd", "UPPER", ""])
async def test_traversal_rejected(server, bad):
    async with Client(server) as c:
        r = await c.call_tool("notes_get", {"note_id": bad})
        assert r.is_error and "invalid id" in r.content[0].text


async def test_read_tools_are_marked_read_only(server):
    async with Client(server) as c:
        tools = {t.name: t for t in (await c.list_tools()).tools}
    assert tools["notes_get"].annotations.read_only_hint is True
    assert tools["notes_create"].annotations.read_only_hint is False
