#!/bin/bash
trap 'echo "got SIGTERM, cleaning up"; exit 0' TERM
while true; do
  echo "heartbeat $(date '+%H:%M:%S') load=$(cut -d' ' -f1 /proc/loadavg)"
  sleep 10
done
