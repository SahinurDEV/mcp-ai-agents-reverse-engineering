"""ex/myclient_v2.py USER PW PATH...: our client for toyapi 0.4, rebuilt from captures.
REPLAY=1 sends every request twice with the same nonce, to prove the server refuses replays."""
import hashlib, json, os, secrets, sys, time, urllib.request, urllib.error
B = "http://127.0.0.1:8719"
def req(path, body=None, tok=None, nonce=None):
    h = {"Content-Type": "application/json"}
    if tok:
        ts, n = str(int(time.time())), nonce or secrets.token_hex(4)
        h |= {"Authorization": "Toy " + tok, "X-Toy-Ts": ts, "X-Toy-Nonce": n,
              "X-Toy-Sig": hashlib.sha256((tok + ts + n + path).encode()).hexdigest()[:8]}
    try: r = urllib.request.urlopen(urllib.request.Request(B + path, json.dumps(body).encode() if body else None, h)); return r.status, json.load(r)
    except urllib.error.HTTPError as e: return e.code, json.load(e)
u, pw, *paths = sys.argv[1:]
code, j = req("/login", {"user": u, "pw": pw}); print("login", code)
for p in paths:
    n = secrets.token_hex(4)
    print(p, *req(p, tok=j.get("token"), nonce=n))
    if os.environ.get("REPLAY"): print(p, "(replayed nonce)", *req(p, tok=j.get("token"), nonce=n))
