"""notes_lab.py: Lab 5 solution. notes-mcp plus tags and soft delete."""
import re

from notes_mcp import ROOT, WRITE, mcp, safe_path
from mcp.server.mcpserver.exceptions import ToolError
from mcp.types import ToolAnnotations

TRASH = ROOT / ".trash"
DELETE = ToolAnnotations(readOnlyHint=False, destructiveHint=True, idempotentHint=True, openWorldHint=False)


@mcp.tool(annotations=WRITE)
def notes_tag(note_id: str, tag: str) -> list[str]:
    """Add a tag to a note. Returns the note's tags."""
    if not re.fullmatch(r"[a-z0-9-]{1,32}", tag):
        raise ToolError(f"invalid tag '{tag}': use 1-32 lowercase letters, digits or dashes")
    path = safe_path(note_id)
    if not path.exists():
        raise ToolError(f"no note '{note_id}'; call notes_list to see ids")
    lines = path.read_text().splitlines()
    tags = sorted(set(lines[-1][len("tags: "):].split(", ")) | {tag}) if lines[-1].startswith("tags: ") else [tag]
    body = lines[:-1] if lines[-1].startswith("tags: ") else lines
    path.write_text("\n".join(body + [f"tags: {', '.join(tags)}"]) + "\n")
    return tags


@mcp.tool(annotations=DELETE)
def notes_delete(note_id: str) -> str:
    """Soft-delete a note: move it to .trash so notes_restore can bring it back."""
    path = safe_path(note_id)
    if not path.exists():
        if (TRASH / path.name).exists():
            return f"{note_id} is already in trash"
        raise ToolError(f"no note '{note_id}'; call notes_list to see ids")
    TRASH.mkdir(exist_ok=True)
    path.rename(TRASH / path.name)
    return f"moved {note_id} to trash"


@mcp.tool(annotations=WRITE)
def notes_restore(note_id: str) -> str:
    """Restore a soft-deleted note from .trash."""
    target = safe_path(note_id)
    src = TRASH / target.name
    if not src.exists():
        raise ToolError(f"'{note_id}' is not in the trash")
    if target.exists():
        raise ToolError(f"a live note '{note_id}' already exists")
    src.rename(target)
    return f"restored {note_id}"


if __name__ == "__main__":
    mcp.run()
