# Hands-on exercises (one per section)

Each exercise has a goal and a "done when" check. Do it after the section's lab. Every exercise has a walkthrough lecture at the end of its section (the lecture number is in the table), and the files used in the walkthrough are in the matching section folder.

| § | Walkthrough | Exercise | Done when |
|---|---|---|---|
| 1 | 1.7 | Run the lab checklist, then call a real server with `s01-setup/fallback_client.py` (no host login). Break the call on purpose and read the validation error. | The client lists the server's tools and prints a correct result. |
| 2 | 2.8 | Send four JSON-RPC requests in one stdio session with `printf` (`s02-fundamentals/session.sh`): `tools/list`, `tools/call`, `resources/read`, and an unknown method. | Every response matches its request by id, and id 4 returns error `-32601`. |
| 3 | 3.9 | Add `convert_units(value, from_unit, to_unit)` (Literal units, read-only annotations) and a `units://{system}` resource (`s03-python-sdk/ex_units.py`). | `pytest test_ex_units.py` passes (5 tests) and the Inspector shows both. |
| 4 | 4.7 | Port `convert_units` to TypeScript with `z.enum` units and `z.number().nonnegative()` (`s04-typescript-sdk/ex_units.ts`). | Same answers as Python; bad units fail the schema, not your code; `tsc` is clean. |
| 5 | 5.9 | Add `notes_rename(note_id, new_id)` to notes-mcp; both ids go through `safe_path`, never overwrite (`s05-notes-mcp/ex_rename.py`). | `pytest test_ex_rename.py` (7 tests) and the original notes-mcp tests pass. |
| 6 | 6.9 | Add a JSONL session log and a summary line to the chat CLI (`s06-mcp-client/ex_chat_log.py`). Reproduce the bug where `agent.py --replay` re-runs a call the user denied, then fix it (`ex_replay.py`). | Replay skips every event with `denied: true`; the notes folder is unchanged. |
| 7 | 7.8 | Take a config that only works from one folder (`s07-hosts/ex/broken.json`), prove it fails from `/tmp`, and fix it with `${workspaceFolder}` and an absolute interpreter (`ex/.vscode/mcp.json`; set `command` to your venv's python). | `check_config.py` reports OK from `/tmp`, and a real `notes_rename` call works. |
| 8 | 8.9 | Write a poisoned update that beats the keyword scanner (`s08-security/ex_sneaky_server.py`, `SNEAKY=1`), show the hash pin still catches it, then write a stricter scanner (`ex_scan_strict.py`). | Old scanner: ok (a miss you can explain). Pin: CHANGED, exit 1. Strict scanner flags the update and not the clean server. |
| 9 | 9.7 | Add a revocation list to the HTTP notes server, keyed by token subject (`s09-auth/ex_revoke.py`). | A revoked subject gets 401 on the next request without a restart; other subjects keep working; the log names the subject, never the token. |
| 10 | 10.8 | Run the CI job locally in a clean copy with a fresh venv (`s10-testing-ci/ci_local.sh`), then break the contract with `BREAK=1`. | Clean tree all green; `BREAK=1` turns the contract test red, exit 1; your folder is untouched. |
| 11 | 11.7 | Hub your own servers (notes + rename, units, git) with a least-privilege policy and run a rename-and-commit plan (`s11-multi-server/ex_servers.json`, `ex_policy.json`, `ex_plan.json`). | 8 of 20 tools visible, `notes_create` refused at call time, and the commit is in `git log`. |
| 12 | 12.8 | Prove the container hardening from inside the running container (`s12-deployment/ex_audit.sh`), then run it with `LOOSE=1`. | 7 PASS hardened; you can explain each FAIL in the loose run. |
| 13 | 13.7 | Compile your own program (`s13-ethics/ex/mytool.c`) and put it in scope with a written source and licence (`ex_add_scope.sh`). Rebuild with `-O2`. | The gate says IN SCOPE and quotes your provenance; the rebuild is refused until added. `ex_reset.sh` undoes it. |
| 14 | 14.9 | Put the stripped build `s14-re-toolkit/ex/mytool_s` in scope, then rename `FUN_` functions and set a prototype through GhidraMCP with `GM_ARGS="--project DIR --save"`. | A fresh session decompiles `main` calling `check_code`; a real run agrees. |
| 15 | 15.10 | Verify every password the agent claimed by running it in the sandbox (`s15-crackmes-a/ex_claims.sh BINARY CANDIDATE...`). | Each claim has a verdict from the binary itself; your write-up quotes the program's output. |
| 16 | 16.7 | Property-test your keygen on 12 names, including 3 and 16 letters, with a one-bit-flipped negative (`s16-crackmes-b/ex_keygen_check.py`); then try `KEYGEN=work/ex_keygen_nomask.py`. | 12/12 pass; the planted overflow bug is caught. |
| 17 | 17.8 | Reverse engineer toy API 0.4's nonce scheme from captures (`s17-protocol-re/ex/`): capture, test every field ordering, write your own client. | One formula explains all captured requests; `REPLAY=1` gets 401 `nonce already used`; bob's note gets 404. |
| 18 | 18.9 | Add a read-only `who_calls(binary, function)` tool to re-assist-mcp, behind the same scope gate (`s18-re-assist-mcp/ex_xrefs.py`). | `strcmp` -> `main` on `cm_strcmp`; refusals tested; all 14 tests pass. |
| 19 | 19.10 | Write one command that proves every exercise still works (`s19-capstone-v2/ex_check_exercises.sh`), then break one on purpose. | 8 PASS on a clean state; a broken exercise gives exactly one FAIL. |
| 20 | 20.6 | Generate a portfolio page from evidence only (`s20-wrap-v2/ex_portfolio.sh`). | `PORTFOLIO.md` generates with 0 FAIL and nothing typed by hand. |

Run `s19-capstone-v2/ex_check_exercises.sh` at any time to re-check exercises 3, 5, 7, 8, 10, 12, 16 and 18 in one go.
