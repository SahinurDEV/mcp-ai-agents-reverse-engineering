#!/bin/sh
# up.sh: (re)start our own toy servers on localhost only: toyapi 8717, toyproto 8718
cd "$(dirname "$0")"; pkill -f "s17/toy(api|proto).py" 2>/dev/null; sleep 0.3
nohup python3 "$PWD/toyapi.py" >/dev/null 2>&1 & nohup python3 "$PWD/toyproto.py" >/dev/null 2>&1 &
sleep 0.7; echo "toyapi http://127.0.0.1:8717  toyproto tcp 127.0.0.1:8718"
