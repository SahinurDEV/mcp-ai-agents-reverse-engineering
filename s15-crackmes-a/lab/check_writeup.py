"""check_writeup.py WRITEUP BINARY: checks a writeup without revealing anything.
Sections present, SHA-256 matches the binary, at least 3 addresses cited, a quoted code line,
and the input after 'Password:' or 'Serial:' really makes the binary print Correct.
Set RUNNER=../s13/sandbox.sh to run it in the Section 13 container instead of on the host."""
import hashlib, os, re, subprocess, sys
w, b = open(sys.argv[1]).read(), sys.argv[2]
ok = True
def check(name, cond):
    global ok; ok &= bool(cond); print(("PASS " if cond else "FAIL ") + name)
for s in ["Triage", "Check logic", "Solution", "Verification", "agent"]:
    check(f"section: {s}", re.search(rf"^##.*{s}", w, re.M | re.I))
check("sha256 matches binary", hashlib.sha256(open(b, "rb").read()).hexdigest() in w)
check("cites >= 3 addresses", len(set(re.findall(r"\b00[0-9a-f]{6}\b", w))) >= 3)
check("quotes a decompiled line", re.search(r"`[^`]*[;(][^`]*`", w))
m = re.search(r"(?:Password|Serial):\s*(\S+)", w)
run = subprocess.run([*os.environ.get("RUNNER", "").split(), b, m.group(1)], capture_output=True, text=True) if m else None
check("stated solution works", run and "Correct" in run.stdout)
sys.exit(0 if ok else 1)
