"""keygen_l4.py [LETTERS]: serial = LETTERS + '-' + %04d of (sum(LETTERS)*31+7) % 10000 (from FUN_00101080)."""
import sys, random, string
def serial(p): return f"{p}-{(sum(map(ord, p)) * 31 + 7) % 10000:04d}"
p = sys.argv[1] if len(sys.argv) > 1 else "".join(random.choices(string.ascii_uppercase, k=4))
assert len(p) == 4 and p.isupper(), "need four upper-case letters"
print(serial(p))
