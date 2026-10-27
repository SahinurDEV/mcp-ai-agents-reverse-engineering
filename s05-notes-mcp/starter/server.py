"""notes-mcp starter — fill in tools in Section 5 labs."""
from mcp.server import MCPServer

mcp = MCPServer("notes-mcp")

# TODO (Section 5): add create_note, get_note, list_notes, search_notes
# TODO: add note://{id} resource and weekly_review prompt


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()
