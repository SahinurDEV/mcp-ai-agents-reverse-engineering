#!/bin/sh
# reset.sh: back to the unsigned starting state
cd "$(dirname "$0")"; rm -f ethics/attestation.md probe/dropped
