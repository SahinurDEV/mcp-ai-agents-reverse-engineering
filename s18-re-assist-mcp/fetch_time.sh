#!/bin/sh
# fetch_time.sh: shallow, sparse clone of modelcontextprotocol/servers (only src/time) into ext/, plus a private venv
cd "$(dirname "$0")" && rm -rf ext && mkdir ext && cd ext
git clone -q --depth 1 --filter=blob:none --sparse https://github.com/modelcontextprotocol/servers && cd servers
git sparse-checkout set src/time && echo "commit $(git log -1 --format='%h %cs')"
cd src/time && uv venv -q .venv && uv pip install -q --python .venv/bin/python -e . && echo "installed: $(.venv/bin/python -m pip --version >/dev/null 2>&1; ls .venv/bin/mcp-server-time)"
