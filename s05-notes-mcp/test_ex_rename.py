"""Exercise 5 tests: rename works, and every escape attempt is refused."""
import pytest
from mcp import Client

pytestmark = pytest.mark.anyio


@pytest.fixture
def anyio_backend():
    return "asyncio"


@pytest.fixture
def server(tmp_path, monkeypatch):
    import ex_rename, notes_mcp
    monkeypatch.setattr(notes_mcp, "ROOT", tmp_path)
    (tmp_path / "a.md").write_text("# A\n")
    (tmp_path / "b.md").write_text("# B\n")
    return ex_rename.mcp


async def test_rename(server, tmp_path):
    async with Client(server) as c:
        assert not (await c.call_tool("notes_rename", {"note_id": "a", "new_id": "alpha"})).is_error
    assert (tmp_path / "alpha.md").exists() and not (tmp_path / "a.md").exists()


async def test_no_overwrite(server):
    async with Client(server) as c:
        r = await c.call_tool("notes_rename", {"note_id": "a", "new_id": "b"})
        assert r.is_error and "already exists" in r.content[0].text


@pytest.mark.parametrize("bad", ["../escape", "/etc/passwd", "..", "A-Upper", "x/../../y"])
async def test_traversal_refused(server, tmp_path, bad):
    async with Client(server) as c:
        r = await c.call_tool("notes_rename", {"note_id": "a", "new_id": bad})
        assert r.is_error and "invalid id" in r.content[0].text
    assert (tmp_path / "a.md").exists()
