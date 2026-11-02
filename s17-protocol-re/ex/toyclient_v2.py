"""ex/toyclient_v2.py [BASE]: the 'official' client for toyapi 0.4. We treat its source as unknown
and recover the signing rule from captures only."""
import hashlib, json, secrets, sys, time, urllib.request
B = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8719"
def call(path, body=None, tok=None):
    h = {"Content-Type": "application/json"}
    if tok:
        ts, n = str(int(time.time())), secrets.token_hex(4)
        h |= {"Authorization": "Toy " + tok, "X-Toy-Ts": ts, "X-Toy-Nonce": n,
              "X-Toy-Sig": hashlib.sha256((tok + ts + n + path).encode()).hexdigest()[:8]}
    r = urllib.request.Request(B + path, data=json.dumps(body).encode() if body else None, headers=h)
    return json.load(urllib.request.urlopen(r))
tok = call("/login", {"user": "alice", "pw": "wonderland"})["token"]
for i in call("/notes", tok=tok)["ids"]: print(call(f"/notes/{i}", tok=tok)["text"])
