# Agent vs manual (Section 15, course-qwen + 6 read-only GhidraMCP tools)
| Level | Agent answer (prep runs, Oct 30)            | Correct? | Manual result                      |
|-------|---------------------------------------------|----------|------------------------------------|
| L1    | open_sesame_42 (4 of 4 runs)                | yes      | strcmp literal, 1 decompile        |
| L2    | no password; filler, once the fail message  | no       | key 0x5a + read_memory + decode    |
| L3    | hunter2_admin decoy (6 of 6 runs)           | no       | opaque predicates proven, table    |
| L4    | no answer within the 5-minute limit         | no       | entry -> main, rename, keygen      |
