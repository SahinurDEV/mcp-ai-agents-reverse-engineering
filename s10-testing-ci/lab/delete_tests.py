"""10.7 lab: notes_delete must never delete anything outside the notes folder."""
import pytest
from mcp import Client

pytestmark = pytest.mark.anyio


async def test_delete_own_note(server):
    async with Client(server) as c:
        await c.call_tool("notes_create", {"title": "Old", "body": "x"})
        r = await c.call_tool("notes_delete", {"note_id": "old"})
        assert not r.is_error and (await c.call_tool("notes_get", {"note_id": "old"})).is_error


async def test_delete_cannot_escape(server, tmp_path):
    victim = tmp_path.parent / "victim.md"       # a file just outside the notes folder
    victim.write_text("keep me")
    async with Client(server) as c:
        r = await c.call_tool("notes_delete", {"note_id": "../victim"})
    assert r.is_error and "invalid id" in r.content[0].text
    assert victim.exists(), "notes_delete removed a file outside NOTES_DIR"
