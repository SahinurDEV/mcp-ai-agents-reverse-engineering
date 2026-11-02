"""ex/toyapi_v2.py: Exercise 17. Version 0.4 of OUR toy API on port 8719 adds one quirk:
every signed request carries X-Toy-Nonce (8 hex), the nonce is part of the signature, and a nonce
can be used only once (replay protection). The owner check from the Lab 17 fix is included."""
import hashlib, sys, time
sys.path.insert(0, __import__("os").path.dirname(__file__) + "/..")
from http.server import ThreadingHTTPServer
import toyapi

SEEN = set()


class H2(toyapi.H):
    server_version = "ToyAPI/0.4"

    def auth(self):
        a = self.headers.get("Authorization", "")
        if not a.startswith("Toy "): return None, "missing Authorization: Toy <token>"
        t, ts, n = a[4:], self.headers.get("X-Toy-Ts", ""), self.headers.get("X-Toy-Nonce", "")
        if t not in toyapi.TOKENS: return None, "unknown token"
        if not ts.isdigit() or abs(time.time() - int(ts)) > 60: return None, "stale or missing X-Toy-Ts"
        if len(n) != 8: return None, "missing X-Toy-Nonce"
        if self.headers.get("X-Toy-Sig") != hashlib.sha256((t + ts + n + self.path).encode()).hexdigest()[:8]: return None, "bad X-Toy-Sig"
        if n in SEEN: return None, "nonce already used"
        SEEN.add(n)
        return toyapi.TOKENS[t], None

    def do_GET(self):
        u, err = self.auth()
        if err: return self.send(401, {"error": err})
        if self.path.startswith("/notes/") and self.path[7:].isdigit():
            n = toyapi.NOTES.get(int(self.path[7:]))
            if not n or n[0] != u: return self.send(404, {"error": "no such note"})
            return self.send(200, {"id": int(self.path[7:]), "text": n[1]})
        if self.path == "/notes":
            return self.send(200, {"ids": [i for i, (o, _) in toyapi.NOTES.items() if o == u]})
        self.send(404, {"error": "not found"})


ThreadingHTTPServer(("127.0.0.1", 8719), H2).serve_forever()
