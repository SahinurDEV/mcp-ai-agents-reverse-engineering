"""xor_decode.py HEX... KEY: XOR each byte with KEY (from read_memory output) and print the text."""
import sys
*bs, key = sys.argv[1:]
print("".join(chr(int(b, 16) ^ int(key, 0)) for b in bs))
