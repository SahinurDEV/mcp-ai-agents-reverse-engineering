@mcp.tool(annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=True, openWorldHint=False))
def notes_delete(note_id: str) -> str:
    """Delete one note by id."""
    path = ROOT / f"{note_id}.md"          # lab bug: no safe_path()
    if not path.exists():
        raise ToolError(f"no note '{note_id}'")
    path.unlink()
    return f"deleted {note_id}"


