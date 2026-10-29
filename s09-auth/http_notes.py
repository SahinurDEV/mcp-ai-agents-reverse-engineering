"""http_notes.py: the Section 5 notes tools served over Streamable HTTP, behind a bearer-token gate.
Every request needs a valid token (signature, expiry, audience); writes also need the notes:write scope."""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "s05-notes-mcp"))
import notes_mcp                                   # reuse the tested tool functions from Section 5
import tokens
from mcp.server.auth.middleware.auth_context import get_access_token
from mcp.server.auth.provider import AccessToken
from mcp.server.auth.settings import AuthSettings
from mcp.server.mcpserver import MCPServer
from mcp.server.mcpserver.exceptions import ToolError


class HmacVerifier:
    async def verify_token(self, token: str) -> AccessToken | None:
        c = tokens.verify(token)
        if c is None:
            return None                            # the SDK answers 401 with a WWW-Authenticate header
        return AccessToken(token=token, client_id=c["sub"], scopes=c["scope"].split(), expires_at=c["exp"],
                           resource=c["aud"], subject=c["sub"])


mcp = MCPServer(
    "notes-http",
    token_verifier=HmacVerifier(),
    auth=AuthSettings(
        issuer_url="http://127.0.0.1:9000",          # where a real OAuth server would live
        resource_server_url=tokens.AUDIENCE,
        required_scopes=["notes:read"],               # every request needs at least read
        validate_token_resource=True,                 # reject tokens minted for another server
    ),
)


def need(scope: str) -> None:
    tok = get_access_token()
    if tok is None or scope not in tok.scopes:
        raise ToolError(f"forbidden: this token lacks the '{scope}' scope")


@mcp.tool(annotations=notes_mcp.WRITE)
def notes_create(title: str, body: str) -> notes_mcp.Created:
    """Create a note. Requires the notes:write scope."""
    need("notes:write")
    return notes_mcp.notes_create(title, body)


@mcp.tool(annotations=notes_mcp.READ)
def notes_get(note_id: str) -> str:
    """Return the full Markdown text of one note."""
    return notes_mcp.notes_get(note_id)


@mcp.tool(annotations=notes_mcp.READ)
def notes_list() -> list[str]:
    """List all note ids, sorted."""
    return notes_mcp.notes_list()


if __name__ == "__main__":
    mcp.run("streamable-http", host="127.0.0.1", port=8765)
