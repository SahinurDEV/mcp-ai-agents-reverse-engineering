# Section 6 — MCP Client & Agent Loop

A minimal agent over the Section 5 notes server (`../s05-notes-mcp/notes_mcp.py`).

| File | Lecture | What it shows |
|---|---|---|
| `list_tools.py` | 6.2–6.3 | Connect over stdio, list tools, convert to OpenAI function specs (`--json`) |
| `agent.py` | 6.4–6.7 | Tool-calling loop; `--approve` for writes, `--log run.jsonl`, `--replay run.jsonl` |
| `anthropic_tools.py` | 6.5 | Same tools in Anthropic format; only sends if `ANTHROPIC_API_KEY` is set |
| `chat.py` | 6.8 lab | Multi-turn chat CLI (`--approve`) |
| `blocks.py`, `extras/` | 6.3 | Common bugs (reading only `content[0]`, wrong server path) |

Configuration comes from the environment only: `LLM_BASE_URL` (default `http://localhost:11434/v1`, Ollama),
`LLM_MODEL` (default `course-qwen`), optional `LLM_API_KEY`. Never commit keys or run logs.

```sh
./reset_notes.sh
python3 agent.py "Find notes about ghidra and show the first one."
echo y | python3 agent.py --approve "Create a note titled todo with body buy coffee."
```
