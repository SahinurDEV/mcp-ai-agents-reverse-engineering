#!/bin/sh
# prep.sh: everything the capstone checks need, from a clean shell (no env leaks from earlier demos)
unset NOTES_DIR; cd "$(dirname "$0")"
(cd ../s15-crackmes-a && make -s) && ../s16-crackmes-b/prep.sh >/dev/null 2>&1
./deploy/build.sh >/dev/null && ./deploy/up.sh >/dev/null && echo "prep ok: binaries built, notes-auth up"
