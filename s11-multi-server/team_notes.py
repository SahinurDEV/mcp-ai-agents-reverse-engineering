"""team_notes.py: a second, unrelated notes server that happens to use the same tool names (11.2)."""
from mcp.server.mcpserver import MCPServer

mcp = MCPServer("team-notes")
TEAM = {"standup": "Team standup notes: ship v2 on Friday."}


@mcp.tool()
def notes_get(note_id: str) -> str:
    """Get a team note by id."""
    return TEAM.get(note_id, f"team-notes has no note '{note_id}'")


@mcp.tool()
def notes_list() -> list[str]:
    """List team note ids."""
    return list(TEAM)


if __name__ == "__main__":
    mcp.run()
