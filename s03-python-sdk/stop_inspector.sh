#!/usr/bin/env bash
# Stop any MCP Inspector web server listening on localhost:6274.
for pid in $(ss -ltnpH 'sport = :6274' | grep -o 'pid=[0-9]*' | cut -d= -f2 | sort -u); do kill "$pid"; done
sleep 1; echo "inspector stopped"
