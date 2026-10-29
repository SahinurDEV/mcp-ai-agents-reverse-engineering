"""discover.py: walk the first steps a desktop MCP client takes before OAuth login, and stop before any login.
No authorization server runs on this box; the script says so when it reaches that step."""
import re
import sys
from urllib.parse import urlencode

import httpx2
from mcp.client.auth.oauth2 import PKCEParameters
from mcp.client.auth.utils import is_valid_client_metadata_url

MCP_URL = "http://127.0.0.1:8765/mcp"
CLIENT_ID = "https://example.com/oauth/course-client.json"     # CIMD: the client id is a URL to a metadata document
REDIRECT = "http://127.0.0.1:33418/callback"                   # desktop apps receive the code on a loopback port

r = httpx2.post(MCP_URL, json={}, headers={"Accept": "application/json, text/event-stream"})
print("1. POST without token ->", r.status_code)
meta_url = re.search(r'resource_metadata="([^"]+)"', r.headers["www-authenticate"]).group(1)
meta = httpx2.get(meta_url).json()
print("2. resource metadata  ->", meta["resource"], "| scopes:", meta["scopes_supported"])
issuer = meta["authorization_servers"][0]
print("3. authorization server:", issuer)
try:
    httpx2.get(f"{issuer}/.well-known/oauth-authorization-server", timeout=2)
except httpx2.ConnectError:
    print(f"4. {issuer}/.well-known/oauth-authorization-server -> connection refused (none runs on this box)")
pkce = PKCEParameters.generate()
print("5. PKCE: verifier stays in the client, challenge =", pkce.code_challenge[:16] + "...")
print("   CIMD client_id valid?", is_valid_client_metadata_url(CLIENT_ID), "| http:// id valid?",
      is_valid_client_metadata_url("http://example.com/c.json"))
q = urlencode({"response_type": "code", "client_id": CLIENT_ID, "redirect_uri": REDIRECT, "scope": " ".join(meta["scopes_supported"]),
               "code_challenge": pkce.code_challenge, "code_challenge_method": "S256", "resource": meta["resource"], "state": "x1"})
print("6. the browser would open (not opened here):")
print("  ", f"{issuer}/authorize?{q}"[:150] + "...")
