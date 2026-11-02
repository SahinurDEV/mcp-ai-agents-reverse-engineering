"""ex_revoke.py: Exercise 9. The Section 9 server plus a revocation list.
A token is short-lived, but a stolen one still works until it expires. revoked.txt lists
subjects whose tokens must stop working now; it is re-read on every request.
  python3 ex_revoke.py serve            run the server on :8765
  python3 ex_revoke.py mint SUB SCOPES  mint a token for one subject (laptop, ci, ...)"""
import os
import sys
from pathlib import Path

import tokens
import http_notes

REVOKED = Path(__file__).with_name("revoked.txt")


class RevocableVerifier(http_notes.HmacVerifier):
    async def verify_token(self, token: str):
        access = await super().verify_token(token)
        revoked = REVOKED.read_text().split() if REVOKED.exists() else []
        if access and access.subject in revoked:
            print(f"refused revoked subject {access.subject}", file=sys.stderr)
            return None                                  # same 401 as an invalid token
        return access


if sys.argv[1:2] == ["mint"]:
    print(tokens.mint(sys.argv[3], sub=sys.argv[2]))
elif sys.argv[1:2] == ["serve"]:
    http_notes.mcp._token_verifier = RevocableVerifier()
    http_notes.mcp.run("streamable-http", host="127.0.0.1", port=8765)
