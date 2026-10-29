# Section 13 — Ethics, Law & Lab Hygiene

- `ethics/attestation.template.md` + `./sign.sh "Your Name"` (Exercise 13: sign before Section 14)
- `scope.txt`: allowed binaries pinned by SHA-256; `./re_gate.sh FILE` refuses anything else
- `./sandbox.sh FILE`: runs an in-scope binary with no network, read-only, no capabilities, nobody user, pids/memory/CPU limits
- `probe/probe.c`: harmless "unknown binary" stand-in (`gcc -O1 -o probe/probe probe/probe.c`, then regenerate its scope line)
- `./faq.sh`: the live crackmes.one FAQ as text

crackmes.one binaries are never stored in this repo (their FAQ: non-commercial use, credit authors, no mirroring).

See the top-level [README](../README.md) and [ETHICS.md](../ETHICS.md).
