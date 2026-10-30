"""obfus_decode.py: tbl from read_memory (16 little-endian ints); char i = tbl[i] - 3*i (junk() returns 0)."""
import sys, struct
raw = bytes.fromhex("".join(sys.argv[1:]))
tbl = struct.unpack(f"<{len(raw)//4}i", raw)
print("".join(chr(t - 3 * i) for i, t in enumerate(tbl)))
