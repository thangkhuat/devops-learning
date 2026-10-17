#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 1 ]]; then
    echo "Usage: $0 <name>" >&2
    exit 1
fi

name="$1"
echo "Hello, $name"
