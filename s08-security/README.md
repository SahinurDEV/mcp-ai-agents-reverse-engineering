# Section 8: MCP security demos

**Read WARNING.md first.** Several files here are deliberately insecure teaching code
(`poisoned_server.py`, `rugpull_server.py`, `inject_note.sh`, `hijacked_llm.py`).
They target only this folder; `secrets.txt` holds a fake token. Run `./reset.sh` for a clean state.

| File | Lecture | What it shows |
|---|---|---|
| inject_note.sh | 8.2, 8.8 | plants a note with injected instructions |
| hijacked_llm.py | 8.2, 8.8 | **simulated** model on :11500 that always obeys the injection (worst case; not a real LLM) |
| agent.py | 8.2, 8.5, 8.8 | Section 6 agent + `ALLOW_TOOLS` (offered *and* enforced), `SPOTLIGHT=1`, `--approve`, `--log` |
| list_tools.py | 8.1, 8.3 | `MCP_SERVER="cmd args"` overrides the server (default: ../s05-notes-mcp) |
| poisoned_server.py | 8.3, 8.6 | tool-poisoning description, file read, network probe |
| scan_tools.py | 8.3 | regex red-flag scan of descriptions and full schemas (no flags != safe) |
| rugpull_server.py, pin_tools.py | 8.5 | tool-definition change (`RUGPULL=1`), detected by SHA-256 lock file |
| sandboxed.sh | 8.5, 8.6 | bubblewrap sandbox: no network, read-only system, only ./notes mounted at /data |

Honesty notes: the recorded local model (Qwen2.5 1.5B via Ollama) ignored the poisoned description
and did not call the injected tool, though it falsely claimed it had. The worst case is shown with
`hijacked_llm.py`, labelled as a simulation, and the poisoned call is made by hand with the MCP Inspector CLI.
Docker was not installed on the recording machine, so isolation is shown with bubblewrap; the equivalent
`docker run -i --rm --network none --read-only --cap-drop ALL --user 1000:1000 -v "$PWD/notes:/data"` form is in 8.6.
