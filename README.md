# Build AI Agents with MCP + Reverse Engineering with AI & Ghidra

Companion source code for the Udemy course. One folder per section.

| Folder | Contents |
|---|---|
| `s01-setup/` | Cold-open headless Ghidra MCP server, lab machine checklist |
| `s02-fundamentals/` | Raw JSON-RPC / stdio examples, capability negotiation |
| `s03-python-sdk/` | First `MCPServer` + `@tool`, resources, prompts, in-process `Client` tests, lab |
| `s04-typescript-sdk/` | The same server in TypeScript (Zod schemas, stdio transport), lab |
| `s05-notes-mcp/` | `notes-mcp` project: tools, path sandbox + traversal tests, `note://{id}`, prompts |
| `s06-mcp-client/` | Your own stdio client and agent loop, consent policy |
| `s07-hosts/` | `setup.sh` writes host configs (Claude/Cursor/VS Code format) for your paths, config checker, broken-config lab |
| `s08-security/` | Prompt injection, tool poisoning, shadowing demos; pinning and sandboxing |
| `s09-auth/` | Streamable HTTP notes server behind a signed, scoped, expiring token |
| `s10-testing-ci/` | Unit, contract and security tests, Inspector smoke test, GitHub Actions workflow |
| `s11-multi-server/` | `hub.py`: several servers behind one client, name clashes, policy lab |
| `s12-deployment/` | Packaging (wheel, `uvx`), hardened container, versioning |
| `s13-ethics/` | Rules of engagement: attestation, hash-pinned scope file, gate, sandbox container |
| `s14-re-toolkit/` | Ghidra 12.1.4 + GhidraMCP 2.0 toolkit, headless scripts |
| `s15-crackmes-a/` | CrackMe Track A: course binaries from source, writeups, writeup checker |
| `s16-crackmes-b/` | CrackMe Track B: course-built release (`tb_lic`, `tb_maze`), hash pinning, sandbox validation |
| `s17-protocol-re/` | Toy HTTP API + TCP protocol we run ourselves, captures, signature test, IDOR lab |
| `s18-re-assist-mcp/` | Review of an official MCP server, then `re-assist-mcp` with an in-server scope gate |
| `s19-capstone-v2/` | Capstone: `check_all.sh` parts A–F, grounded-answer check, token-gated container deploy |
| `s20-wrap-v2/` | Wrap-up notes |
| `ghidra_scripts/` | Ghidra headless scripts used across the RE sections |

`s15-crackmes/` holds the original L1–L4 CrackMe sources used in the Section 1 cold open.
`s14-ghidra-toolkit/`, `s16-crackmes-one/`, `s19-capstone/` and `s20-wrap/` belong to an earlier draft of the course and are kept only for reference; the recorded lectures use the folders in the table. Every binary analysed in the course was written for the course; no third-party CrackMes are included.

## Requirements
Linux, Python 3.11+, [uv](https://docs.astral.sh/uv/), Node 22.19+, `mcp[cli]` 2.x, Ghidra 12.1.4 + JDK 21 for the RE sections, gcc + make.

```bash
cd s03-python-sdk && uv run --with "mcp[cli]" python demo_client.py
cd s15-crackmes && make
```

Read [ETHICS.md](ETHICS.md) before the reverse engineering sections. License: [MIT](LICENSE).

## Practice
- [Hands-on exercises for every section](EXERCISES.md)
- [Troubleshooting](TROUBLESHOOTING.md)
