#!/usr/bin/env bash
set -euo pipefail 

if [[ $# -ne 1 ]]; then
	echo "Usage: $0 <service>" >&2
	exit 1
fi

service="$1"

if ! systemctl cat "$service" &>/dev/null; then
    echo "Service $service does not exist" >&2
    exit 2
fi

if systemctl is-enabled --quiet "$service"; then
    echo "Service $service is enabled"
else
    echo "Service $service is not enabled"
fi

if systemctl is-active --quiet "$service"; then
	echo "Service $service is active"
    exit 0
else
	echo "Service $service is not active"
    exit 1
fi

