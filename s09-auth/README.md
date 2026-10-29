# Section 9: auth for remote (Streamable HTTP) MCP servers

| File | Lecture | What it shows |
|---|---|---|
| setup.sh | all | fresh notes + a random signing key in `.env` (mode 600, gitignored) |
| tokens.py | 9.3 | **stand-in authorization server**: HMAC-signed, short-lived tokens with scope + audience. Use a real OAuth server and a JWT library in production |
| http_notes.py | 9.3 | notes tools over Streamable HTTP; SDK `TokenVerifier` + `AuthSettings` (401/403), per-tool `notes:write` check |
| http_client.py | 9.3 | SDK client with `Authorization: Bearer $NOTES_TOKEN` |
| probe.sh | 9.1–9.6 | prints HTTP status + `WWW-Authenticate` for an initialize request |
| discover.py | 9.4 | 401 -> protected resource metadata -> authorization server -> PKCE -> authorize URL (stops before login; no auth server runs locally) |
| open_notes.py, check_lab.sh | 9.6 | lab starter with no auth, and the five checks it must pass |

```sh
./setup.sh && set -a && . ./.env && set +a
python3 http_notes.py &        # 127.0.0.1:8765
./check_lab.sh
NOTES_TOKEN=$(python3 tokens.py mint "notes:read notes:write") python3 http_client.py list
```
