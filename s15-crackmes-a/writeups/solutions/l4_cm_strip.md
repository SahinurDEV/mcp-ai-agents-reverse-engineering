# Writeup: cm_strip (L4) — SPOILER
- SHA-256: 7dafd59a04029a260586018ebcea32101f575ed3966567f4b178ef2f5c128c8d (in ../s13-ethics/scope.txt)
- Origin / licence: course binary, src/cm_strip.c, -O2 -s
## 1. Triage (evidence)
- entry: `__libc_start_main(FUN_00101080, ...)` -> main @ 00101080; "Invalid serial." @ 00102034 xref'd only from it
- imports strlen, snprintf, __ctype_b_loc
## 2. Check logic
- `if ((sVar3 == 9) && (__s[4] == '-')) {`; four chars must be upper case (ctype table bit), summed
- `snprintf((char *)&local_d,5,"%04d",(long)(iVar2 * 0x1f + 7) % 10000 & 0xffffffff);` compared with s+5; every early exit jumps to the failure path @ 001010a0
## 3. Solution
- keygen: solve/keygen_l4.py
- Serial: ABCD-8253
## 4. Verification
- `./bin/cm_strip ABCD-8253` -> "Correct! L4 solved."; random keygen serials pass; ABCD-8254 fails
## 5. What the agent got right / wrong
- No answer within the 5-minute request limit (before max_tokens was added); solved by hand
