"""verify_log.py LOG.jsonl PASSWORD: did the agent PROVE its answer? True only if the log holds a run_crackme
call with exactly that password whose real result had exit_code 0. The answer text is never trusted."""
import json, sys
runs = [json.loads(l) for l in open(sys.argv[1]) if '"run_crackme"' in l]
for r in runs: print(f"run_crackme args={r['args'].get('args')} -> exit_code={json.loads(r['result']).get('exit_code') if not r['error'] else 'ERROR'}")
ok = any(r["args"].get("args") == [sys.argv[2]] and not r["error"] and json.loads(r["result"]).get("exit_code") == 0 for r in runs)
print("PROVEN" if ok else "NOT PROVEN: no successful run with that password in the log"); sys.exit(0 if ok else 1)
