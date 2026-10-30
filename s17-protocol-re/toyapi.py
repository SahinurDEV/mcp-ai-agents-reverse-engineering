"""toyapi.py: a deliberately quirky toy HTTP API that WE own (course demo). Port 8717, localhost only.
POST /login {"user","pw"} -> {"token"}.  Every other call needs headers:
  X-Toy-Ts: unix seconds (within 60 s)   X-Toy-Sig: first 8 hex of sha256(token + ts + path)
  Authorization: Toy <token>
GET /notes -> your note ids; GET /notes/<id> -> one note.  (Bug kept on purpose for the lab: see LAB.md)"""
import hashlib, json, secrets, time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
USERS = {"alice": "wonderland", "bob": "builder"}
NOTES = {1: ("alice", "buy milk"), 2: ("alice", "call mum"), 3: ("bob", "bob's private plan")}
TOKENS = {}
class H(BaseHTTPRequestHandler):
    server_version = "ToyAPI/0.3"; sys_version = ""
    def log_message(self, *a): pass
    def send(self, code, obj):
        b = json.dumps(obj).encode(); self.send_response(code)
        self.send_header("Content-Type", "application/json"); self.send_header("Content-Length", str(len(b))); self.end_headers(); self.wfile.write(b)
    def do_POST(self):
        if self.path != "/login": return self.send(404, {"error": "not found"})
        d = json.loads(self.rfile.read(int(self.headers.get("Content-Length", 0))) or b"{}")
        if USERS.get(d.get("user")) != d.get("pw"): return self.send(401, {"error": "bad credentials"})
        t = secrets.token_hex(8); TOKENS[t] = d["user"]; self.send(200, {"token": t})
    def auth(self):
        a = self.headers.get("Authorization", "")
        if not a.startswith("Toy "): return None, "missing Authorization: Toy <token>"
        t = a[4:]; ts = self.headers.get("X-Toy-Ts", "")
        if t not in TOKENS: return None, "unknown token"
        if not ts.isdigit() or abs(time.time() - int(ts)) > 60: return None, "stale or missing X-Toy-Ts"
        if self.headers.get("X-Toy-Sig") != hashlib.sha256((t + ts + self.path).encode()).hexdigest()[:8]: return None, "bad X-Toy-Sig"
        return TOKENS[t], None
    def do_GET(self):
        u, err = self.auth()
        if err: return self.send(401, {"error": err})
        if self.path == "/notes": return self.send(200, {"ids": [i for i, (o, _) in NOTES.items() if o == u]})
        if self.path.startswith("/notes/") and self.path[7:].isdigit():
            n = NOTES.get(int(self.path[7:]))
            if not n: return self.send(404, {"error": "no such note"})
            return self.send(200, {"id": int(self.path[7:]), "text": n[1]})   # BUG (lab): no owner check
        self.send(404, {"error": "not found"})
if __name__ == "__main__":
    ThreadingHTTPServer(("127.0.0.1", 8717), H).serve_forever()
