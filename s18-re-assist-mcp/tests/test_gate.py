"""Scope-gate tests for re-assist-mcp: run with  pytest -q s18/tests"""
import os, shutil, sys, pytest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "re_assist"))
import server
from mcp.server.mcpserver.exceptions import ToolError

def test_pinned_course_binary_allowed():
    assert server.gate("cm_strcmp").name == "cm_strcmp"

@pytest.mark.parametrize("bad", ["../s16-crackmes-b/inbox/trackb-easy-1.0/tb_lic", "/bin/ls", "..", ".hidden", "cm_strcmp/../../x", ""])
def test_paths_refused(bad):
    with pytest.raises(ToolError, match="refused"): server.gate(bad)

def test_unpinned_copy_refused(tmp_path, monkeypatch):
    d = tmp_path / "bin"; d.mkdir(); shutil.copy(server.BIN_DIR / "cm_strcmp", d / "cm_strcmp")
    with open(d / "cm_strcmp", "ab") as f: f.write(b"\0")          # one extra byte: new hash
    monkeypatch.setattr(server, "BIN_DIR", d.resolve())
    with pytest.raises(ToolError, match="not pinned"): server.gate("cm_strcmp")

def test_symlink_out_of_folder_refused(tmp_path, monkeypatch):
    # link to a binary that IS pinned (Section 16's tb_lic) but lives outside the folder: only containment can stop it
    d = tmp_path / "bin"; d.mkdir(); (d / "evil").symlink_to(server.S / "s16/inbox/trackb-easy-1.0/tb_lic")
    monkeypatch.setattr(server, "BIN_DIR", d.resolve())
    with pytest.raises(ToolError, match="no binary"): server.gate("evil")
