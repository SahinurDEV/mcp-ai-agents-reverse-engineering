#!/bin/sh
# capture.sh OUT.flows: run mitmdump as a reverse proxy on 127.0.0.1:8727 -> toyapi 8717, run the client through it
cd "$(dirname "$0")"; mkdir -p caps
mitmdump -q --listen-host 127.0.0.1 -p 8727 --mode reverse:http://127.0.0.1:8717 -w "$1" & p=$!; sleep 2
python3 toyclient.py http://127.0.0.1:8727; sleep 0.5; kill $p; wait $p 2>/dev/null; echo "saved $1"
