import sys
from pathlib import Path

import os
import tempfile

import pytest

os.environ["NOTES_DIR"] = tempfile.mkdtemp(prefix="notes-test-")   # importing notes_mcp must not create ./notes

sys.path.insert(0, str(Path(__file__).parent.parent))       # import notes_mcp and redflags from the project root


@pytest.fixture
def anyio_backend():
    return "asyncio"


@pytest.fixture
def server(tmp_path, monkeypatch):
    """The real notes server, in-process, with an empty temporary notes folder."""
    import notes_mcp
    monkeypatch.setattr(notes_mcp, "ROOT", tmp_path)
    return notes_mcp.mcp
