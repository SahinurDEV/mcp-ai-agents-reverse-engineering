#!/bin/sh
# ex/up_v2.sh: (re)start toyapi 0.4 on 127.0.0.1:8719
cd "$(dirname "$0")"; pkill -f "ex/toyapi_v2.py" 2>/dev/null; sleep 0.3
nohup python3 "$PWD/toyapi_v2.py" >/dev/null 2>&1 & sleep 0.7; echo "toyapi 0.4 http://127.0.0.1:8719"
