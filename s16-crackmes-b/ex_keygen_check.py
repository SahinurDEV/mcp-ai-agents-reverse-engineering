"""ex_keygen_check.py [N]: Exercise 16. Two examples prove little; test the keygen against the
real binary on many names, including the edge cases (3 and 16 letters), all inside the sandbox.
Also check that a key off by one bit is rejected, so a "pass" is not just a binary that accepts anything."""
import random
import string
import subprocess
import sys

KEYGEN = __import__("os").environ.get("KEYGEN", "work/keygen_tb_lic.py")
B = "inbox/trackb-easy-1.0/tb_lic"
N = int(sys.argv[1]) if len(sys.argv) > 1 else 12
random.seed(16)
names = ["abc", "zzzzzzzzzzzzzzzz", "reverseengineer"] + \
        ["".join(random.choices(string.ascii_lowercase, k=random.randint(3, 16))) for _ in range(N - 3)]


def run(name, key):
    return subprocess.run(["../s13-ethics/sandbox.sh", B, name, key], capture_output=True, text=True).returncode


ok = bad = 0
for n in names:
    key = subprocess.check_output(["python3", KEYGEN, n], text=True).strip()
    flipped = f"{int(key, 16) ^ 1:08X}"
    good, neg = run(n, key), run(n, flipped)
    passed = good == 0 and neg != 0
    ok += passed
    bad += not passed
    print(f"{'PASS' if passed else 'FAIL'}  {n:17} key={key} exit={good}  flipped={flipped} exit={neg}")
print(f"{ok}/{len(names)} names: real key accepted and flipped key rejected")
sys.exit(1 if bad else 0)
