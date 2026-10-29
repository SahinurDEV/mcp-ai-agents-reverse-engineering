"""notes-mcp: a small notes server. Notes are Markdown files inside NOTES_DIR."""
import os
import re
import time
from pathlib import Path
from typing import TypedDict

from mcp.server.mcpserver import MCPServer
from mcp.server.mcpserver.exceptions import ResourceError, ToolError
from mcp.server.mcpserver.prompts.base import UserMessage
from mcp.types import ToolAnnotations

ROOT = Path(os.environ.get("NOTES_DIR", "notes")).resolve()
ROOT.mkdir(parents=True, exist_ok=True)
mcp = MCPServer("notes-mcp")

class Created(TypedDict):
    id: str
    uri: str


class Hit(TypedDict):
    id: str
    line: str


READ = ToolAnnotations(readOnlyHint=True, openWorldHint=False)
WRITE = ToolAnnotations(readOnlyHint=False, destructiveHint=False, idempotentHint=False, openWorldHint=False)


def safe_path(note_id: str) -> Path:
    """Map a note id to a file inside ROOT, or refuse."""
    if not re.fullmatch(r"[a-z0-9][a-z0-9-]{0,63}", note_id):
        raise ToolError(f"invalid id '{note_id}': use lowercase letters, digits and dashes")
    path = (ROOT / f"{note_id}.md").resolve()
    if not path.is_relative_to(ROOT):
        raise ToolError(f"id '{note_id}' escapes the notes folder")
    return path


def slug(title: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")[:64] or "note"


@mcp.tool(annotations=WRITE)
def notes_create(title: str, body: str) -> Created:
    """Create a note. Returns its id. Fails if a note with the same id exists."""
    note_id = slug(title)
    path = safe_path(note_id)
    if path.exists():
        raise ToolError(f"note '{note_id}' already exists; pick another title or call notes_get")
    path.write_text(f"# {title}\n\n{body}\n")
    return {"id": note_id, "uri": f"note://{note_id}"}


@mcp.tool(annotations=READ)
def notes_get(note_id: str) -> str:
    """Return the full Markdown text of one note."""
    path = safe_path(note_id)
    if not path.exists():
        close = [i for i in notes_list() if note_id in i or i in note_id][:3]
        raise ToolError(f"no note '{note_id}'" + (f"; did you mean {', '.join(close)}?" if close else "; call notes_list to see ids"))
    return path.read_text()


@mcp.tool(annotations=READ)
def notes_list() -> list[str]:
    """List all note ids, sorted."""
    return sorted(p.stem for p in ROOT.glob("*.md"))


@mcp.tool(annotations=READ)
def notes_search(query: str, limit: int = 5) -> list[Hit]:
    """Case-insensitive search over note text. Returns id and the first matching line."""
    if not query.strip():
        raise ToolError("query must not be empty")
    hits = []
    for p in sorted(ROOT.glob("*.md")):
        for line in p.read_text().splitlines():
            if query.lower() in line.lower():
                hits.append({"id": p.stem, "line": line.strip()})
                break
    return hits[:limit]


@mcp.resource("note://{note_id}", mime_type="text/markdown")
def note_resource(note_id: str) -> str:
    """One note as Markdown."""
    try:
        path = safe_path(note_id)
    except ToolError as e:
        raise ResourceError(str(e))
    if not path.exists():
        raise ResourceError(f"no note '{note_id}'")
    return path.read_text()


@mcp.resource("note://index", mime_type="text/plain")
def note_index() -> str:
    """All note ids, one per line, as note:// URIs."""
    return "\n".join(f"note://{i}" for i in notes_list())


@mcp.prompt()
def weekly_review(focus: str = "everything") -> list:
    """Review the notes changed in the last 7 days."""
    week_ago = time.time() - 7 * 86400
    ids = ", ".join(p.stem for p in sorted(ROOT.glob("*.md")) if p.stat().st_mtime >= week_ago) or "(none)"
    return [UserMessage(f"Do a weekly review focused on {focus}. Notes changed this week: {ids}. "
                        "Read each with notes_get, then list decisions, open questions and next steps.")]


@mcp.prompt()
def meeting_prep(topic: str) -> list:
    """Prepare for a meeting on a topic using matching notes."""
    hits = notes_search(topic) if topic.strip() else []
    if not hits:
        return [UserMessage(f"I have a meeting about '{topic}' and no notes on it. "
                            "Ask me three questions to build a short brief, then offer to save it with notes_create.")]
    found = ", ".join(h["id"] for h in hits)
    return [UserMessage(f"Prepare me for a meeting about '{topic}'. Relevant notes: {found}. "
                        "Read them with notes_get, summarize in five bullets and suggest three questions to ask.")]

if __name__ == "__main__":
    mcp.run()
