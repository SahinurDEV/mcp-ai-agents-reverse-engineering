import pytest
from mcp import Client


@pytest.fixture
def anyio_backend():
    return "asyncio"


@pytest.fixture
def server(tmp_path, monkeypatch):
    import notes_mcp
    monkeypatch.setattr(notes_mcp, "ROOT", tmp_path)
    return notes_mcp.mcp


@pytest.mark.anyio
async def test_create_get_search(server):
    async with Client(server) as c:
        r = await c.call_tool("notes_create", {"title": "Ghidra tips", "body": "Press L to rename."})
        assert r.structured_content["id"] == "ghidra-tips"
        r = await c.call_tool("notes_search", {"query": "rename"})
        assert r.structured_content["result"][0]["id"] == "ghidra-tips"


@pytest.mark.anyio
@pytest.mark.parametrize("bad", ["../etc/passwd", "..", "a/b", "/etc/passwd", "UPPER", ""])
async def test_traversal_rejected(server, bad):
    async with Client(server) as c:
        r = await c.call_tool("notes_get", {"note_id": bad})
        assert r.is_error
        assert "invalid id" in r.content[0].text


@pytest.mark.anyio
async def test_symlink_escape_rejected(server, tmp_path):
    (tmp_path / "linked.md").symlink_to("/etc/os-release")
    async with Client(server) as c:
        r = await c.call_tool("notes_get", {"note_id": "linked"})
        assert r.is_error
        assert "escapes the notes folder" in r.content[0].text
