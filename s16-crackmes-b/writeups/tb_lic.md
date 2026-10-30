# Writeup: tb_lic (external CrackMe, Track B release 1.0)
- Source URL: http://127.0.0.1:8716/trackb-easy-1.0.tar.gz (local stand-in for a CrackMe site)
- Archive SHA-256: 88aacb41e42ab438d497fa27b32d66aa1f94d800c0dad59f0bfe14d9c601cae2 (matches index page)
- Binary SHA-256: 455301f3f905415f98ba9fb2b844364e7493796266b41ea63f6b88c8c6a0f6e9 (pinned, origin trackb-1.0)
- Author / credit: the course team (LICENSE.txt in the release)
- Licence notes: free to analyse and write up for learning; no redistribution of modified binaries; no keys for non-CrackMe software
- Run environment: ../s13-ethics/sandbox.sh (docker: --network none, --read-only, --cap-drop ALL, uid 65534)
## 1. Triage (evidence)
- author functions: mix @ 00101179, valid_name @ 001011c1, main @ 00101226 (agent wrongly named _init, FUN_00101020, deregister_tm_clones)
- imports: strlen, snprintf, strcmp, printf, puts
## 2. Check logic
- main: `uVar2 = mix(*(undefined8 *)(param_2 + 8));` then `snprintf(local_11,9,"%08X",(ulong)uVar2);` and `strcmp(*(char **)(param_2 + 0x10),local_11)`
- mix: `local_c = 0x1505;` ... `local_c = (uint)*local_20 + local_c * 0x21;` ... `return local_c ^ 0xc0ffee11;` = djb2 (5381, *33) XOR 0xC0FFEE11
- valid_name: length 3..16 (`0x10 < sVar1`), only 'a'..'z'
## 3. Solution
- keygen: work/keygen_tb_lic.py
- Input: alice CFE8A3D2
## 4. Verification (sandbox only)
- `../s13-ethics/sandbox.sh inbox/trackb-easy-1.0/tb_lic alice CFE8A3D2` -> "Licensed to alice. Thank you!", exit 0
## 5. What the agent got right / wrong
- Wrong: author functions (named compiler stubs, 3 of 3 runs); never identified djb2 (0 of 3 runs)
- Right: read back the constants 0x1505, 0x21, 0xc0ffee11 when asked about mix() alone
- Wrong: described the update step as XOR instead of add in some runs; called 0xc0ffee11 a "common hash constant" (it is not)
## 6. Publishing check
- [x] no binary attached  - [x] no keys for non-CrackMe software  - [x] author credited
