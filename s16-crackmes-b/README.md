# Section 16: CrackMe Track B (course-built "external" release)
Binaries written by the course team (NOT from crackmes.one), shipped as a release and treated as untrusted.
- `vendor/build_release.sh` builds the reproducible release; `site.sh` serves it on http://127.0.0.1:8716 (local stand-in for a CrackMe site)
- `prep.sh`: sign ethics, start site, download, `pin.sh` verifies SHA256SUMS and pins hashes in ../s13-ethics/scope.txt
- Run binaries ONLY via `../s13-ethics/sandbox.sh` (Docker container: no network, read-only, nobody; not a VM)
- `work/keygen_tb_lic.py`, `writeups/` (TEMPLATE_external.md, tb_lic.md, check_ext.py)
- Lab: tb_maze (solution intentionally not included)
