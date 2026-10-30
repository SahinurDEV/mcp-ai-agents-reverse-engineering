#!/bin/sh
# mint.sh SCOPES [TTL]: mint a token with the container's key (read from .env, not shown)
cd "$(dirname "$0")"; set -a; . ./.env; set +a; python3 app/s09/tokens.py mint "$@"
