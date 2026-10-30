"""flows2txt.py FILE.flows: print each captured request/response as plain text (for reading, or for the agent)."""
import sys
from mitmproxy import io, http
for f in io.FlowReader(open(sys.argv[1], "rb")).stream():
    if not isinstance(f, http.HTTPFlow): continue
    q, r = f.request, f.response
    print(f"> {q.method} {q.path}"); [print(f">   {k}: {v}") for k, v in q.headers.items() if k.lower() not in ("host", "accept-encoding", "connection", "user-agent")]
    if q.content: print(f">   body {q.get_text()}")
    print(f"< {r.status_code} {r.get_text()}")
