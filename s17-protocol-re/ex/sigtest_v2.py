"""ex/sigtest_v2.py CAPTURE.txt: which order of token, ts, nonce and path makes X-Toy-Sig?
Every permutation is tried against every captured request; only a formula matching ALL counts."""
import hashlib, itertools, re, sys
reqs = re.findall(r"> GET (\S+)\n(?:>   .*\n)*?>   Authorization: Toy (\w+)\n>   X-Toy-Ts: (\d+)\n>   X-Toy-Nonce: (\w+)\n>   X-Toy-Sig: (\w+)",
                  open(sys.argv[1]).read())
print(f"{len(reqs)} signed requests")
for order in itertools.permutations(["token", "ts", "nonce", "path"]):
    hits = 0
    for p, t, ts, n, sig in reqs:
        parts = {"token": t, "ts": ts, "nonce": n, "path": p}
        hits += hashlib.sha256("".join(parts[k] for k in order).encode()).hexdigest()[:8] == sig
    if hits:
        print(f"{hits}/{len(reqs)}  sha256({'+'.join(order)})")
