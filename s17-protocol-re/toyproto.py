"""toyproto.py: toy TCP protocol server WE own, 127.0.0.1:8718. Frame = 1 byte type, 2 bytes big-endian length, payload.
Types: 0x01 HELLO(name) -> 0x81 WELCOME(session id, 4 bytes)   0x02 GET(key) -> 0x82 VALUE(text) | 0xEE ERROR(text)
       0x03 BYE -> 0x83 BYE.   Frames longer than 512 bytes are rejected."""
import socketserver, struct, os
DATA = {b"motd": b"hello from toyproto", b"version": b"0.2"}
def frame(t, p): return struct.pack(">BH", t, len(p)) + p
class H(socketserver.BaseRequestHandler):
    def recvn(self, n):
        b = b""
        while len(b) < n:
            c = self.request.recv(n - len(b))
            if not c: raise EOFError
            b += c
        return b
    def handle(self):
        hello = False
        try:
            while True:
                t, n = struct.unpack(">BH", self.recvn(3))
                if n > 512: self.request.sendall(frame(0xEE, b"frame too long")); return
                p = self.recvn(n)
                if t == 0x01: hello = True; self.request.sendall(frame(0x81, os.urandom(4)))
                elif not hello: self.request.sendall(frame(0xEE, b"say HELLO first"))
                elif t == 0x02: self.request.sendall(frame(0x82, DATA[p]) if p in DATA else frame(0xEE, b"no such key"))
                elif t == 0x03: self.request.sendall(frame(0x83, b"")); return
                else: self.request.sendall(frame(0xEE, b"unknown type"))
        except EOFError: pass
if __name__ == "__main__":
    socketserver.ThreadingTCPServer.allow_reuse_address = True
    socketserver.ThreadingTCPServer(("127.0.0.1", 8718), H).serve_forever()
