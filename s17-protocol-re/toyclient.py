"""toyclient.py [BASE]: the 'official' client for toyapi (ours). Logs in as alice, lists notes, reads each one."""
import hashlib, json, sys, time, urllib.request
B = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8717"
def call(path, body=None, tok=None):
    h = {"Content-Type": "application/json"}
    if tok:
        ts = str(int(time.time())); h |= {"Authorization": "Toy " + tok, "X-Toy-Ts": ts,
             "X-Toy-Sig": hashlib.sha256((tok + ts + path).encode()).hexdigest()[:8]}
    r = urllib.request.Request(B + path, data=json.dumps(body).encode() if body else None, headers=h)
    return json.load(urllib.request.urlopen(r))
tok = call("/login", {"user": "alice", "pw": "wonderland"})["token"]
for i in call("/notes", tok=tok)["ids"]: print(call(f"/notes/{i}", tok=tok)["text"])
