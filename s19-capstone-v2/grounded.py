"""grounded.py LOG: is the agent's final answer backed by a successful tool result in its own log?
Rule: some 6-word run of the answer must appear in a non-error tool result. Prints the verdict."""
import json, re, sys
rows = [json.loads(l) for l in open(sys.argv[1])]
tools = [r for r in rows if r["kind"] == "tool"]
ok = [r for r in tools if r["result"] and not r["result"].startswith("ERROR")]
ans = next((r["text"] for r in rows if r["kind"] == "answer"), "")
for r in tools:
    print(f"tool {r['name']:<11} {json.dumps(r['args']):<22} {'ERROR' if r['result'].startswith('ERROR') else ('empty' if not r['result'] else 'ok')}")
w = re.findall(r"\w+", ans.lower())
src = " ".join(re.findall(r"\w+", " ".join(r["result"] for r in ok).lower()))
hit = any(" ".join(w[i:i+6]) in src for i in range(max(0, len(w) - 5))) if src else False
print("GROUNDED" if hit else "NOT GROUNDED: no 6-word run of the answer appears in a successful tool result")
sys.exit(0 if hit else 1)
