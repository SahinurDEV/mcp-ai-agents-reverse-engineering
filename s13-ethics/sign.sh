#!/bin/sh
# sign.sh "Your Name": copy the template to ethics/attestation.md with name and date filled in
[ -n "$1" ] || { echo "usage: ./sign.sh \"Your Name\"" >&2; exit 2; }
sed -e "s/^Signed: NAME/Signed: $1/" -e "s/^Date: DATE/Date: $(date +%F)/" ethics/attestation.template.md > ethics/attestation.md
echo "signed: $(grep -E '^(Signed|Date):' ethics/attestation.md | tr '\n' ' ')"
