"""keygen_tb_lic.py NAME: key = %08X of (djb2(NAME) ^ 0xC0FFEE11), read from mix() and main() in Ghidra."""
import sys
name = sys.argv[1]
assert 3 <= len(name) <= 16 and name.isascii() and name.isalpha() and name.islower(), "valid_name(): 3-16 of a-z"
h = 5381                                  # 0x1505
for b in name.encode(): h = (h * 33 + b) & 0xFFFFFFFF   # 0x21, uint wraps at 32 bits
print(f"{h ^ 0xC0FFEE11:08X}")
