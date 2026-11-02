# Security report (practice): agent.py --replay re-runs tool calls the user denied
- Product / version: MCP course agent, demos/v2/s06/agent.py, course repo commit at time of testing
- Found: 2026-11-02, Asia/Dhaka (UTC+6), while doing Exercise 6
- Impact: replaying a session log performs write actions (e.g. notes_create) that the user explicitly refused.
## Steps to reproduce (local, harmless)
1. python3 ex_chat_log.py --approve --log ex.jsonl, ask it to create a note, answer n at the prompt
2. python3 agent.py --replay ex.jsonl
3. ls notes  ->  the refused note now exists
## Suggested fix
- Log a denied flag per tool event and skip denied events on replay (see ex_replay.py)
## Disclosure
- Reported privately to the maintainers; nothing published until a fix ships or 90 days pass
