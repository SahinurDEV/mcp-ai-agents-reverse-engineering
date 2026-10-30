"""sigtest.py CAPTURE.txt: test candidate X-Toy-Sig formulas against every captured request. A formula wins only if it matches ALL of them."""
import hashlib, hmac, re, sys
reqs = re.findall(r"> GET (\S+)\n(?:>   .*\n)*?>   Authorization: Toy (\w+)\n>   X-Toy-Ts: (\d+)\n>   X-Toy-Sig: (\w+)", open(sys.argv[1]).read())
H = lambda s: hashlib.sha256(s.encode()).hexdigest()[:8]
C = {"hmac(ts, path)  [agent's guess]": lambda p, t, ts: hmac.new(ts.encode(), p.encode(), "sha256").hexdigest()[:8],
     "hmac(ts, token)  [agent's guess]": lambda p, t, ts: hmac.new(ts.encode(), t.encode(), "sha256").hexdigest()[:8],
     "sha256(path)": lambda p, t, ts: H(p), "sha256(token+ts)": lambda p, t, ts: H(t + ts),
     "sha256(ts+token+path)": lambda p, t, ts: H(ts + t + p), "sha256(token+ts+path)": lambda p, t, ts: H(t + ts + p),
     "md5(token+ts+path)": lambda p, t, ts: hashlib.md5((t + ts + p).encode()).hexdigest()[:8]}
print(f"{len(reqs)} signed requests")
for name, f in C.items(): print(f"{sum(f(p, t, ts) == s for p, t, ts, s in reqs)}/{len(reqs)}  {name}")
