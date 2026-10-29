"""tokens.py: tiny signed, short-lived bearer tokens for the Section 9 demo (HMAC-SHA256, JWT-like).
A real deployment gets tokens from an OAuth authorization server; this stands in for it locally.
  python3 tokens.py mint SCOPES [TTL_SECONDS] [AUDIENCE]   ->  prints a token
The signing key comes from the environment (NOTES_TOKEN_KEY), never from the code."""
import base64, hashlib, hmac, json, os, sys, time

AUDIENCE = "http://127.0.0.1:8765/mcp"


def _b64(b: bytes) -> str:
    return base64.urlsafe_b64encode(b).rstrip(b"=").decode()


def _key() -> bytes:
    k = os.environ.get("NOTES_TOKEN_KEY")
    if not k:
        raise SystemExit("set NOTES_TOKEN_KEY first (see setup.sh)")
    return k.encode()


def mint(scopes: str, ttl: int = 300, aud: str = AUDIENCE, sub: str = "student") -> str:
    body = _b64(json.dumps({"sub": sub, "scope": scopes, "aud": aud, "exp": int(time.time()) + ttl}).encode())
    return body + "." + _b64(hmac.new(_key(), body.encode(), hashlib.sha256).digest())


def verify(token: str) -> dict | None:
    """Return the claims if the signature, expiry and audience are all valid, else None."""
    try:
        body, sig = token.split(".")
        good = _b64(hmac.new(_key(), body.encode(), hashlib.sha256).digest())
        if not hmac.compare_digest(sig, good):
            return None
        claims = json.loads(base64.urlsafe_b64decode(body + "=" * (-len(body) % 4)))
    except ValueError:
        return None
    if claims["exp"] < time.time() or claims["aud"] != AUDIENCE:
        return None
    return claims


if __name__ == "__main__" and sys.argv[1:2] == ["mint"]:
    a = sys.argv[2:]
    print(mint(a[0], int(a[1]) if len(a) > 1 else 300, a[2] if len(a) > 2 else AUDIENCE))

if __name__ == "__main__" and sys.argv[1:2] == ["claims"]:      # decode without verifying, for teaching
    b = sys.argv[2].split(".")[0]
    print(base64.urlsafe_b64decode(b + "=" * (-len(b) % 4)).decode())
