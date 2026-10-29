"""open_notes.py: LAB STARTER, deliberately unprotected. The same notes tools over HTTP with no auth at all.
Your task (9.6): add a token verifier and AuthSettings so check_lab.sh passes. Solution: http_notes.py."""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "s05-notes-mcp"))
import notes_mcp
from mcp.server.mcpserver import MCPServer

mcp = MCPServer("notes-open")
mcp.tool(annotations=notes_mcp.READ)(notes_mcp.notes_list)
mcp.tool(annotations=notes_mcp.WRITE)(notes_mcp.notes_create)

if __name__ == "__main__":
    mcp.run("streamable-http", host="127.0.0.1", port=int(os.environ.get("PORT", "8765")))
