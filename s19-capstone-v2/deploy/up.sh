#!/bin/sh
# up.sh: fresh random signing key in deploy/.env (mode 600, never printed), run the container hardened
cd "$(dirname "$0")"; docker rm -f notes-auth >/dev/null 2>&1
umask 077; echo "NOTES_TOKEN_KEY=$(head -c 24 /dev/urandom | base64)" > .env
docker run -d --name notes-auth --network host --read-only --cap-drop ALL --security-opt no-new-privileges \
  --env-file .env -v notes-auth-data:/data notes-mcp-auth:1.0.0 >/dev/null
for i in 1 2 3 4 5 6 7 8 9 10; do curl -s -o /dev/null http://127.0.0.1:8765/mcp && break; sleep 0.5; done
docker ps --filter name=notes-auth --format '{{.Names}}  {{.Status}}'
