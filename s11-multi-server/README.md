# Section 11: multi-server agents

`hub.py` is a small MCP client that connects to several servers at once (`servers.json`):
our notes server, `team_notes.py` (a second server with clashing tool names),
the official filesystem server (inbox only) and the official git server (one repository).

    ./setup.sh                                   # fresh work/notes (git) and work/inbox
    python3 hub.py tools --flat                  # see the collisions
    python3 hub.py --policy policy.json tools    # allow-listed, prefixed tools
    python3 hub.py --only notes,files,git run plan_inbox.json
    python3 hub.py --only notes,files,git --policy policy.json agent "..."   # local Ollama model
    ./check_lab.sh                               # lab checks (policy_lab.json, plan_lab.json)

The agent uses an OpenAI-compatible API (default: local Ollama, model course-qwen); set LLM_BASE_URL / LLM_MODEL.

See the top-level [README](../README.md) and [ETHICS.md](../ETHICS.md).
