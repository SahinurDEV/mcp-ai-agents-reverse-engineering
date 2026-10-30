"""ask.py FILE "QUESTION": send a text file plus a question to the local model (no tools). Same endpoint as ../s14-re-toolkit/re_agent.py."""
import os, sys, httpx
BASE = os.environ.get("LLM_BASE_URL", "http://localhost:11434/v1"); MODEL = os.environ.get("LLM_MODEL", "course-qwen")
h = {"Authorization": "Bearer " + os.environ["LLM_API_KEY"]} if os.environ.get("LLM_API_KEY") else {}
msg = open(sys.argv[1]).read() + "\n\n" + sys.argv[2]
r = httpx.post(f"{BASE}/chat/completions", headers=h, timeout=300, json={"model": MODEL, "temperature": 0, "seed": 7, "max_tokens": 400, "messages": [{"role": "user", "content": msg}]})
print("[ask] model=" + MODEL); print(r.json()["choices"][0]["message"]["content"].strip())
