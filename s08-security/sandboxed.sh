#!/bin/sh
# sandboxed.sh SERVER.py: run an MCP server in a bubblewrap sandbox.
# No network, read-only system, no home or workspace; only ./notes is mounted (as /data, writable).
V="${VENV:-$(dirname "$(dirname "$(command -v python3)")")}"   # the Python env that has mcp installed
exec bwrap --ro-bind /usr /usr --ro-bind /lib /lib --ro-bind /lib64 /lib64 --ro-bind /bin /bin \
  --ro-bind "$V" "$V" --ro-bind "$1" /srv/server.py --bind "$PWD/notes" /data \
  --proc /proc --dev /dev --tmpfs /tmp --unshare-all --die-with-parent \
  --setenv NOTES_DIR /data "$V/bin/python3" /srv/server.py
