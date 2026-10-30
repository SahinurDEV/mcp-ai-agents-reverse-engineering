# Section 19 capstone: proof, not claims

Six parts, each with a check that runs on your machine:

| Part | What | Proof |
|---|---|---|
| A | notes-mcp tests + CI | `pytest` in s10 and `smoke.sh` (Inspector CLI); same steps in `.github/workflows/s10-notes-ci.yml` |
| B | client / agent | `grounded.py LOG`: answer must quote a successful tool result from its own log |
| C | deploy | `deploy/` packages the Section 9 token-gated server on the Section 12 image; 401 without token, scope refusal, read-only non-root |
| D | re-assist-mcp | Section 18 gate tests |
| E | writeups | three CrackMe writeups pass `s15/lab/check_writeup.py`; signed `s13/ethics/attestation.md` |
| F | demo | `demo_checklist.md` fully ticked (7 items) |

    ./prep.sh          # build CrackMes, build + start notes-auth (random key in deploy/.env, gitignored)
    ./check_all.sh     # or: ./check_all.sh C E
    B_LOG=logs/agent_vague.jsonl ./check_all.sh B   # an ungrounded run, fails
    CHECKLIST=my_checklist.md ./check_all.sh F

`lab/check_all_v1.sh` is the first version, kept on purpose: its Part F passed an empty checklist.
Targets are only our own CrackMes and our own servers.

In this repository the paths point at the sibling folders (s05-notes-mcp, s09-auth, s10-testing-ci, s13-ethics, s15-crackmes-a, s18-re-assist-mcp).
Part E needs your own signed attestation: run `../s13-ethics/sign.sh "Your Name"` first.
