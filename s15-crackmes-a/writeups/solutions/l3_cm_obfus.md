# Writeup: cm_obfus (L3) — SPOILER
- SHA-256: b7f602667f137a11919adf9e5142d6d070f586606d7baa378f211ed9dfe5422e (in ../s13-ethics/scope.txt)
- Origin / licence: course binary, src/cm_obfus.c, -O0
## 1. Triage (evidence)
- decoy string "hunter2_admin" @ 00102079; imports strlen, strcmp, puts
## 2. Check logic
- main @ 00101180: `if ((((iVar3 + 1) * iVar3) % 2 == 1) && (iVar4 = strcmp(pcVar7,"hunter2_admin"), iVar4 == 0)) {` — x(x+1) is always even: dead branch
- junk() decompiles to `return 0;`; length check `if (iVar4 + 0x10 == iVar3) {` -> 16
- `iVar5 + iVar4 + local_20 * -3 != (int)pcVar7[local_20]` with `-1 < iVar3 * iVar3` always true
- tbl @ 00102020 (LEA after index*4), 16 x int32
## 3. Solution
- char i = tbl[i] - 3*i (solve/obfus_decode.py)
- Password: junk_hides_logic
## 4. Verification
- `./bin/cm_obfus junk_hides_logic` -> "Correct! L3 solved."; `hunter2_admin` -> "Wrong password."
## 5. What the agent got right / wrong
- Wrong every run: reported the decoy; one run cited an address that matches no Ghidra result
