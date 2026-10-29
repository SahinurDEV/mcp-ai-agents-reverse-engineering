#!/bin/sh
# faq.sh: fetch the live crackmes.one FAQ and print it as plain text, one question per paragraph
curl -s https://crackmes.one/faq | python3 -c '
import sys, re, html
t = sys.stdin.read()
t = re.sub(r"<(script|style).*?</\1>", "", t, flags=re.S)
t = re.sub(r"<h[1-6][^>]*>", "\n\n## ", t)
t = html.unescape(re.sub(r"<[^>]+>", " ", t))
print(re.sub(r"[ \t\r]+", " ", re.sub(r"\n\s*\n+", "\n\n", t)).replace(" #", ""))'
