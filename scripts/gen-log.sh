#!/usr/bin/env bash
set -euo pipefail

ips=(10.0.0.1 10.0.0.2 10.0.0.3 192.168.1.10 192.168.1.20 172.16.0.5)
paths=(/ /login /api/users /api/orders /health /admin)
statuses=(200 200 200 200 201 301 404 404 500 503)

for i in $(seq 1 500); do
    ip=${ips[RANDOM % ${#ips[@]}]}
    path=${paths[RANDOM % ${#paths[@]}]}
    status=${statuses[RANDOM % ${#statuses[@]}]}
    bytes=$((RANDOM % 5000 + 100))
    hour=$(printf "%02d" $((RANDOM % 24)))
    echo "$ip - - [17/Oct/2026:$hour:$((RANDOM % 60)):00 +1100] \"GET $path HTTP/1.1\" $status $bytes"
done
