"""protoclient.py [PORT] NAME KEY...: toyproto client (frame = type:1, length:2 big-endian, payload)."""
import socket, struct, sys
a = sys.argv[1:]; port = int(a.pop(0)) if a[0].isdigit() else 8718
s = socket.create_connection(("127.0.0.1", port))
def rx():
    t, n = struct.unpack(">BH", s.recv(3)); p = s.recv(n) if n else b""; return t, p
def tx(t, p=b""): s.sendall(struct.pack(">BH", t, len(p)) + p); t, p = rx(); print(f"got type=0x{t:02x} len={len(p)} {p!r}")
tx(0x01, a[0].encode())
for k in a[1:]: tx(0x02, k.encode())
tx(0x03)
