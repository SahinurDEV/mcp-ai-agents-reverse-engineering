"""Exercise 5: notes_rename on top of notes-mcp. Both ids go through safe_path."""
import notes_mcp
from notes_mcp import WRITE, mcp, safe_path
from mcp.server.mcpserver.exceptions import ToolError


@mcp.tool(annotations=WRITE)
def notes_rename(note_id: str, new_id: str) -> str:
    """Rename a note's id. Refuses to overwrite an existing note."""
    src, dst = safe_path(note_id), safe_path(new_id)
    if not src.exists():
        raise ToolError(f"no note '{note_id}'; call notes_list to see ids")
    if dst.exists():
        raise ToolError(f"'{new_id}' already exists; pick another id")
    src.rename(dst)
    return f"renamed {note_id} -> {new_id}"


if __name__ == "__main__":
    mcp.run()
