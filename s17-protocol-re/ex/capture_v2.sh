#!/bin/sh
# ex/capture_v2.sh OUT.flows: mitmdump reverse proxy 127.0.0.1:8729 -> toyapi 0.4, run the official v2 client through it
cd "$(dirname "$0")/.."; mkdir -p caps
mitmdump -q --listen-host 127.0.0.1 -p 8729 --mode reverse:http://127.0.0.1:8719 -w "$1" & p=$!; sleep 2
python3 ex/toyclient_v2.py http://127.0.0.1:8729; sleep 0.5; kill $p; wait $p 2>/dev/null; echo "saved $1"
