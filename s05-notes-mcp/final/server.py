"""notes-mcp final — sandboxed notes tools/resources/prompts."""
from __future__ import annotations

import json
import re
import uuid
from datetime import datetime, timezone
from pathlib import Path

from mcp.server import MCPServer

ROOT = Path(__file__).resolve().parent / "notes_data"
ROOT.mkdir(exist_ok=True)

mcp = MCPServer(
    "notes-mcp",
    instructions="Sandboxed personal notes. Paths never escape notes_data/.",
)

_ID_RE = re.compile(r"^[a-zA-Z0-9_-]{1,64}$")


def _safe_path(note_id: str) -> Path:
    if not _ID_RE.match(note_id):
        raise ValueError("invalid note id")
    path = (ROOT / f"{note_id}.json").resolve()
    if not str(path).startswith(str(ROOT.resolve())):
        raise ValueError("path escape blocked")
    return path


@mcp.tool()
def create_note(title: str, body: str, tags: list[str] | None = None) -> dict:
    """Create a note. Returns id, title, created_at."""
    note_id = uuid.uuid4().hex[:12]
    path = _safe_path(note_id)
    data = {
        "id": note_id,
        "title": title.strip()[:200],
        "body": body,
        "tags": tags or [],
        "created_at": datetime.now(timezone.utc).isoformat(),
        "deleted": False,
    }
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")
    return {"id": note_id, "title": data["title"], "created_at": data["created_at"]}


@mcp.tool()
def get_note(note_id: str) -> dict:
    """Fetch one note by id."""
    path = _safe_path(note_id)
    if not path.exists():
        raise ValueError(f"note not found: {note_id}")
    return json.loads(path.read_text(encoding="utf-8"))


@mcp.tool()
def list_notes() -> list[dict]:
    """List non-deleted notes (id, title, tags)."""
    out = []
    for p in sorted(ROOT.glob("*.json")):
        d = json.loads(p.read_text(encoding="utf-8"))
        if d.get("deleted"):
            continue
        out.append({"id": d["id"], "title": d["title"], "tags": d.get("tags", [])})
    return out


@mcp.tool()
def search_notes(query: str) -> list[dict]:
    """Case-insensitive search over title and body."""
    q = query.lower().strip()
    hits = []
    for p in ROOT.glob("*.json"):
        d = json.loads(p.read_text(encoding="utf-8"))
        if d.get("deleted"):
            continue
        blob = f"{d.get('title','')} {d.get('body','')}".lower()
        if q in blob:
            hits.append({"id": d["id"], "title": d["title"], "tags": d.get("tags", [])})
    return hits


@mcp.resource("note://{note_id}")
def note_resource(note_id: str) -> str:
    """Read a note as markdown."""
    d = get_note(note_id)
    tags = ", ".join(d.get("tags") or [])
    return f"# {d['title']}\n\nTags: {tags}\n\n{d['body']}\n"


@mcp.prompt()
def weekly_review() -> str:
    """Prompt template: summarize this week's notes."""
    return (
        "Review my notes from this week. Group by tag, call out action items, "
        "and suggest three follow-ups. Use list_notes and get_note tools."
    )


@mcp.prompt()
def meeting_prep(topic: str) -> str:
    """Prompt template: prep for a meeting on a topic."""
    return (
        f"Prepare me for a meeting about {topic}. Search my notes, pull the most "
        f"relevant ones, and draft a one-page brief with open questions."
    )


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()
