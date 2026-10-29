import pytest
from mcp import Client


@pytest.fixture
def anyio_backend():
    return "asyncio"


@pytest.fixture
def server(tmp_path, monkeypatch):
    import notes_lab
    import notes_mcp
    monkeypatch.setattr(notes_mcp, "ROOT", tmp_path)
    monkeypatch.setattr(notes_lab, "TRASH", tmp_path / ".trash")
    (tmp_path / "a.md").write_text("# A\n\nbody\n")
    return notes_lab.mcp


@pytest.mark.anyio
async def test_delete_is_idempotent(server):
    async with Client(server) as c:
        first = await c.call_tool("notes_delete", {"note_id": "a"})
        second = await c.call_tool("notes_delete", {"note_id": "a"})
        assert not first.is_error and not second.is_error
        assert (await c.call_tool("notes_list", {})).structured_content["result"] == []


@pytest.mark.anyio
async def test_restore_refuses_to_overwrite(server, tmp_path):
    async with Client(server) as c:
        await c.call_tool("notes_delete", {"note_id": "a"})
        (tmp_path / "a.md").write_text("# A again\n")
        r = await c.call_tool("notes_restore", {"note_id": "a"})
        assert r.is_error and "already exists" in r.content[0].text
