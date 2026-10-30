# Writeup: cm_xor (L2) — SPOILER
- SHA-256: 4a00ed5241bbe49617354ad8a97065524ffa3380b0cb6557d7762fe28791c546 (in ../s13-ethics/scope.txt)
- Origin / licence: course binary, src/cm_xor.c, -O0
## 1. Triage (evidence)
- no password in strings (`grep -c xor_is bin/cm_xor` = 0); imports strlen, puts
## 2. Check logic
- main @ 00101149: `if (sVar2 == 0x11) {` length 17
- `if ((byte)(__s[local_10] ^ 0x5aU) != (&enc)[local_10]) {` key 0x5a
- disassembly: `XOR EAX,0x5a` then `LEA RCX,[0x102010]` -> enc @ 00102010
## 3. Solution
- read_memory 00102010 len 17, XOR 0x5a (solve/xor_decode.py)
- Password: xor_is_not_crypto
## 4. Verification
- `./bin/cm_xor xor_is_not_crypto` -> "Correct! L2 solved.", exit 0; "Correct! L2 solved." @ 00102048
## 5. What the agent got right / wrong
- Described the XOR loop; never produced the password; invented details (compiler version, "hexadecimal" password); one run named the failure message as the password
