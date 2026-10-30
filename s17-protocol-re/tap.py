"""tap.py: a tiny logging TCP relay we wrote (this box has no tcpdump). Listens 127.0.0.1:8728, forwards to 8718,
prints every chunk as hex with direction, so we can see the raw frames."""
import socket, threading, sys
def pump(a, b, tag):
    while (d := a.recv(4096)):
        print(f"{tag} {len(d):3d}B  {d.hex(' ')}", flush=True); b.sendall(d)
    b.close()
s = socket.socket(); s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1); s.bind(("127.0.0.1", 8728)); s.listen()
while True:
    c, _ = s.accept(); u = socket.create_connection(("127.0.0.1", 8718))
    threading.Thread(target=pump, args=(c, u, "C->S"), daemon=True).start(); threading.Thread(target=pump, args=(u, c, "S->C"), daemon=True).start()
