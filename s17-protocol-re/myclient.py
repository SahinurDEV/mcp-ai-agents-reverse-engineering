"""myclient.py USER PW PATH...: minimal client rebuilt from the captures (17.5). Signs each request: sha256(token+ts+path)[:8]."""
import hashlib, json, sys, time, urllib.request, urllib.error
B = "http://127.0.0.1:8717"
def req(path, body=None, tok=None, ts=None, signpath=None):   # signpath: sign a different path (negative test)
    h = {"Content-Type": "application/json"}
    if tok:
        ts = ts or str(int(time.time()))
        h |= {"Authorization": "Toy " + tok, "X-Toy-Ts": ts, "X-Toy-Sig": hashlib.sha256((tok + ts + (signpath or path)).encode()).hexdigest()[:8]}
    try: r = urllib.request.urlopen(urllib.request.Request(B + path, json.dumps(body).encode() if body else None, h)); return r.status, json.load(r)
    except urllib.error.HTTPError as e: return e.code, json.load(e)
if __name__ == "__main__":
    u, pw, *paths = sys.argv[1:]
    code, j = req("/login", {"user": u, "pw": pw}); print("login", code)
    for p in paths: print(p, *req(p, tok=j.get("token")))
