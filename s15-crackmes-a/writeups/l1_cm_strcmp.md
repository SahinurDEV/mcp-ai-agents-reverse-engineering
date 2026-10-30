# Writeup: cm_strcmp (L1)
- SHA-256: 749e95b66d8bbf092f34c256c80f441519de6e84d1e10ffe401cef8f58288a9b (in ../s13-ethics/scope.txt)
- Origin / licence: course binary, built from src/cm_strcmp.c by `make` (-O0, not stripped)
- Tools: Ghidra 12.1.4 + GhidraMCP 2.0 headless; agent log logs/l1.jsonl
## 1. Triage (evidence)
- list_imports: strcmp, puts -> a direct string comparison is likely
- list_strings: "open_sesame_42" @ 0010201e, next to "Correct! L1 solved." @ 0010202d
## 2. Check logic
- main @ 00101149: `iVar1 = strcmp(*(char **)(param_2 + 8),"open_sesame_42");`
- param_2 + 8 is argv[1]; result 0 prints "Correct! L1 solved."
## 3. Solution
- Password: open_sesame_42 (read directly from the strcmp argument)
## 4. Verification
- `./bin/cm_strcmp open_sesame_42` -> "Correct! L1 solved.", exit 0
- `./bin/cm_strcmp guess` -> "Wrong password.", exit 1
## 5. What the agent got right / wrong
- Right: named the password, after calling list_strings, list_imports, decompile_function(main)
- Missing: quoted no code line and no address; the evidence above comes from the log, not its prose
