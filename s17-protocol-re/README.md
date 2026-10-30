# Section 17: Protocol & API RE (own apps only)
Both targets are our own toy servers on 127.0.0.1 (`./up.sh`): `toyapi.py` (HTTP, port 8717, signed requests) and `toyproto.py` (TCP 8718, type:1 len:2 payload).
- `capture.sh` + `flows2txt.py`: mitmdump reverse proxy (127.0.0.1:8727) around the official `toyclient.py`
- `ask.py`: give a capture to the local model (env LLM_BASE_URL / LLM_MODEL / LLM_API_KEY)
- `sigtest.py`: test candidate X-Toy-Sig formulas against every captured request
- `myclient.py`: client rebuilt from captures; `tap.py`: hex-printing TCP relay (stand-in for tcpdump); `protoclient.py`
- Lab: `lab/check_fix.sh` (owner check / IDOR in toyapi). Reference fix: `solutions/owner_check.diff`.
Captures (`caps/`) contain passwords and tokens and are gitignored.
