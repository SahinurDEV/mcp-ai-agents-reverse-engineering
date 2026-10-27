# Build AI Agents with MCP + Reverse Engineering with AI & Ghidra

Companion source code for the Udemy course. One folder per section.

| Folder | Contents |
|---|---|
| `s03-python-sdk/` | First `MCPServer` + `@tool`, in-process client |
| `s05-notes-mcp/` | `notes-mcp` project: `starter/` and `final/` |
| `s15-crackmes/` | Course CrackMes L1–L4 (source + Makefile, no solutions) |
| `s01`…`s20` | Filled in as lectures are released |

## Requirements
Linux, Python 3.11+, [uv](https://docs.astral.sh/uv/), Node 22.19+, `mcp[cli]` 2.x, Ghidra 12.1.4 + JDK 21 for the RE sections, gcc + make.

```bash
cd s03-python-sdk && uv run --with "mcp[cli]" python demo_client.py
cd s15-crackmes && make
```

Read [ETHICS.md](ETHICS.md) before the reverse engineering sections. License: [MIT](LICENSE).
