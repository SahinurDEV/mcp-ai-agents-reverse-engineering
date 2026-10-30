#!/bin/sh
# site.sh: local stand-in for a CrackMe download site (127.0.0.1:8716), serving vendor/out + an index page
cd "$(dirname "$0")" && vendor/build_release.sh >/dev/null && cp vendor/out/trackb-easy-1.0.tar.gz site/
H=$(sha256sum site/trackb-easy-1.0.tar.gz | cut -d' ' -f1)
cat > site/index.html <<H2
<h1>Track B easy CrackMes</h1>
<p>Release 1.0, author: the course team. Licence: free to analyse and write up for learning; do not redistribute modified binaries.</p>
<p><a href="trackb-easy-1.0.tar.gz">trackb-easy-1.0.tar.gz</a> sha256: $H</p>
H2
pkill -f "http.server 8716" 2>/dev/null; sleep 0.3
nohup python3 -m http.server 8716 --bind 127.0.0.1 --directory site >/dev/null 2>&1 &
sleep 0.7; echo "site up: http://127.0.0.1:8716/"
