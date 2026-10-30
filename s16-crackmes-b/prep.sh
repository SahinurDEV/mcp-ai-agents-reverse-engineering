#!/bin/sh
# prep.sh: silent setup for Section 16 recordings: site up, release in inbox/, binaries pinned
cd "$(dirname "$0")" && ../s13-ethics/sign.sh "Demo Student" >/dev/null && ./site.sh >/dev/null
[ -f inbox/trackb-easy-1.0/tb_lic ] || { mkdir -p inbox && curl -so inbox/trackb-easy-1.0.tar.gz http://127.0.0.1:8716/trackb-easy-1.0.tar.gz && tar -C inbox -xzf inbox/trackb-easy-1.0.tar.gz; }
./pin.sh inbox/trackb-easy-1.0 "trackb-1.0(course-team)" >/dev/null
