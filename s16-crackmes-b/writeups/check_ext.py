"""check_ext.py WRITEUP BINARY: grade an external-CrackMe writeup without revealing anything.
Adds provenance checks (URL, archive hash, licence, credit) and runs the stated Input ONLY in the sandbox."""
import hashlib, re, subprocess, sys, os
w, b = open(sys.argv[1]).read(), sys.argv[2]
ok = True
def check(name, cond):
    global ok; ok &= bool(cond); print(("PASS " if cond else "FAIL ") + name)
for f in ["Source URL", "Archive SHA-256", "Licence notes", "Author / credit", "Run environment"]:
    check(f"field: {f}", re.search(rf"^- {re.escape(f)}: (?!<)\S", w, re.M))
check("binary sha256 matches", hashlib.sha256(open(b, "rb").read()).hexdigest() in w)
check("cites >= 3 addresses", len(set(re.findall(r"\b00[0-9a-f]{6}\b", w))) >= 3)
check("publishing checklist ticked", w.count("[x]") == 3)
m = re.search(r"^- Input: (.+)$", w, re.M)
sb = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../s13-ethics/sandbox.sh")
run = subprocess.run([sb, b, *m.group(1).split()], capture_output=True, text=True) if m and "<" not in m.group(1) else None
check("stated input passes (in sandbox)", run is not None and run.returncode == 0)
sys.exit(0 if ok else 1)
