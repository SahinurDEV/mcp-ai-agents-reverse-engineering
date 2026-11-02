# Hands-on exercises (one per section)

Each exercise has a goal, steps and a "done when" check. Do them after the section's lab. Solutions are in the matching section folder, or you can check your work with the tests that are already there.

| § | Exercise | Done when |
|---|---|---|
| 1 | Run the course-client fallback against `s01-setup` without any host login. | `tools/list` prints at least one tool. |
| 2 | Hand-write `initialize` → `notifications/initialized` → `tools/list` over stdio with `printf` piped into a server. | You get a valid JSON-RPC response for every request id. |
| 3 | Add a `convert_units(value, from, to)` tool and a `units://{system}` resource to the calculator lab. | The in-process `Client` test passes, and the Inspector shows both. |
| 4 | Port `convert_units` to the TypeScript server, using a Zod enum for the units. | Bad units return a schema error, not a crash. |
| 5 | Add `rename_note` to notes-mcp. Block `../` and absolute paths. | The traversal tests stay green, and a new test covers the rename. |
| 6 | Make the chat CLI ask for approval before every *write* tool, and log calls to JSONL. | Replaying the log reproduces the session. |
| 7 | Wire notes-mcp into one host **and** the course client. Break the path on purpose, then fix it using the 7.6 checklist. | Both clients list the same tools. |
| 8 | Write a poisoned tool description and a result-injection payload against your own server, then defend with the 8.5 allowlist and hash pin. | The pinned hash rejects the changed tool. |
| 9 | Put notes-mcp behind a bearer token over Streamable HTTP, and give read and write tokens different scopes. | A read token calling a write tool gets 403. |
| 10 | Add a CI job that runs the protocol tests on every push. | A deliberately broken test turns CI red. |
| 11 | Run notes-mcp with a second server and prefix the tool names to avoid collisions. | No tool shadowing appears in `tools/list`. |
| 12 | Build the least-privilege image as non-root with a read-only filesystem. | `docker run` works, and writes outside the volume fail. |
| 13 | Fill in the rules-of-engagement template for your own lab. | Every binary you use has a written source and licence. |
| 14 | Use GhidraMCP to rename three functions in `hello`, then re-decompile. | The decompiler output uses your names. |
| 15 | Solve L2 alone first, then compare with what the agent claims. Write down one thing the agent got wrong. | Your write-up includes an "agent errors" line. |
| 16 | Solve `tb_maze` and validate it inside the sandbox only. | The sandboxed run prints success. Nothing runs on the host. |
| 17 | Add a new auth quirk to the toy API, then re-derive it from captures alone. | Your minimal client authenticates. |
| 18 | Add a `xrefs(addr)` tool to re-assist-mcp, restricted to the course binaries folder. | Paths outside the folder are refused. |
| 19 | Score yourself against the capstone rubric, then fix the lowest item. | Every rubric row is at least "meets". |
| 20 | Publish your capstone repo with a README demo GIF and the attestation. | A stranger can run it from the README. |
