#!/usr/bin/env bash
set -euo pipefail

state_file="$HOME/.cache/log-report/last-alert"
mkdir -p "$(dirname "$state_file")"

now=$(date +%s)
cooldown=1800

if [[ -f "$state_file" ]]; then
    last=$(cat "$state_file")
    if [[ ! "$last" =~ ^[0-9]+$ ]]; then
        echo "State file corrupt, ignoring it" >&2
    elif (( now - last < cooldown )); then
        echo "Alert suppressed (cooldown)" >&2
        exit 0
    fi
fi

echo "ALERT: log-report failed at $(date '+%F %T')"
echo "$now" > "$state_file"