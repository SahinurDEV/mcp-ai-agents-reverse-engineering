"""notes-mcp: a small notes server. Notes are Markdown files inside NOTES_DIR.
Run: notes-mcp (stdio) or notes-mcp --http [--host H] [--port P] (Streamable HTTP at /mcp)."""
import argparse
import functools
import json
import logging
import os
import sys
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
__version__ = "1.0.0"
mcp = MCPServer("notes-mcp", version=__version__)
log = logging.getLogger("notes_mcp")


class JsonFormatter(logging.Formatter):
    """One JSON object per line on stderr (stdout belongs to the stdio protocol)."""
    def format(self, r):
        return json.dumps({"ts": self.formatTime(r, "%Y-%m-%dT%H:%M:%S%z"), "level": r.levelname.lower(),
                           "msg": r.getMessage(), **getattr(r, "fields", {})})


def logged(fn):
    """Log every tool call: name, outcome, duration. Never log note bodies."""
    @functools.wraps(fn)
    def wrapper(*a, **kw):
        t0 = time.perf_counter()
        fields = {"tool": fn.__name__, "args": sorted(kw)}
        try:
            out = fn(*a, **kw)
            log.info("tool_call", extra={"fields": {**fields, "ok": True, "ms": round((time.perf_counter() - t0) * 1000, 1)}})
            return out
        except ToolError as e:
            log.warning("tool_call", extra={"fields": {**fields, "ok": False, "error": str(e)[:120]}})
            raise
        except Exception as e:                      # a bug or an OS problem: log the type, then let the SDK report it
            log.error("tool_call", extra={"fields": {**fields, "ok": False, "error": type(e).__name__, "detail": str(e)[:120]}})
            raise
    return wrapper

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
@logged
def notes_create(title: str, body: str) -> Created:
    """Create a note. Returns its id. Fails if a note with the same id exists."""
    note_id = slug(title)
    path = safe_path(note_id)
    if path.exists():
        raise ToolError(f"note '{note_id}' already exists; pick another title or call notes_get")
    path.write_text(f"# {title}\n\n{body}\n")
    return {"id": note_id, "uri": f"note://{note_id}"}


@mcp.tool(annotations=READ)
@logged
def notes_get(note_id: str) -> str:
    """Return the full Markdown text of one note."""
    path = safe_path(note_id)
    if not path.exists():
        close = [i for i in notes_list() if note_id in i or i in note_id][:3]
        raise ToolError(f"no note '{note_id}'" + (f"; did you mean {', '.join(close)}?" if close else "; call notes_list to see ids"))
    return path.read_text()


@mcp.tool(annotations=READ)
@logged
def notes_list() -> list[str]:
    """List all note ids, sorted."""
    return sorted(p.stem for p in ROOT.glob("*.md"))


@mcp.tool(annotations=READ)
@logged
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

@mcp.custom_route("/healthz", methods=["GET"])
async def healthz(request):
    from starlette.responses import JSONResponse
    return JSONResponse({"status": "ok", "version": __version__, "notes": len(notes_list())})


def main(argv=None):
    p = argparse.ArgumentParser(prog="notes-mcp")
    p.add_argument("--http", action="store_true", help="serve Streamable HTTP instead of stdio")
    p.add_argument("--host", default=os.environ.get("NOTES_HOST", "127.0.0.1"))
    p.add_argument("--port", type=int, default=int(os.environ.get("NOTES_PORT", "8000")))
    p.add_argument("--version", action="version", version=f"notes-mcp {__version__}")
    a = p.parse_args(argv)
    h = logging.StreamHandler(sys.stderr)
    h.setFormatter(JsonFormatter())
    log.addHandler(h)
    log.propagate = False                    # only our JSON line, not a second plain copy
    log.setLevel(os.environ.get("LOG_LEVEL", "INFO"))
    log.info("start", extra={"fields": {"version": __version__, "transport": "http" if a.http else "stdio", "notes_dir": str(ROOT)}})
    if a.http:
        mcp.run("streamable-http", host=a.host, port=a.port)
    else:
        mcp.run()


if __name__ == "__main__":
    main()
