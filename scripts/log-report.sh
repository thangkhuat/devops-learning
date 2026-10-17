#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 1 ]]; then
    echo "Usage: $0 <log_file>" >&2
    exit 1
fi

log_file="$1"

if [[ ! -f "$log_file" ]]; then
    echo "File '$log_file' is not a regular file" >&2
    exit 1
fi

if [[ ! -r "$log_file" ]]; then
    echo "File '$log_file' is not readable" >&2
    exit 1
fi

if [[ ! -s "$log_file" ]]; then
    echo "File '$log_file' is empty" >&2
    exit 1
fi

reports_dir="$HOME/devops-learning/reports"
report_file="$reports_dir/report-$(date '+%F_%H%M').txt"
mkdir -p "$reports_dir"
max_error_rate=20

{
    echo "=== Log report: $log_file ==="
    printf "Generated: %s\n" "$(date '+%F %T')"
    echo ""

    awk '$9 >= 400 {error++} {byte += $10}
        END {
            printf "%-20s %d\n", "Total requests:", NR
            printf "%-20s %d\n", "Errors (4xx+5xx):", error
            printf "%-20s %.1f%%\n", "Error rate:", error/NR * 100
            printf "%-20s %d\n\n", "Total bytes:", byte
        }' "$log_file"

    echo "--- Status codes ---"
    awk '{code[$9]++} END {for (c in code) print code[c], c}' "$log_file" | sort -nr
    echo ""

    echo "--- Top 5 IPs ---"
    awk '{address[$1]++} END {for (a in address) print address[a], a}' "$log_file" | sort -nr | head -n 5
    echo ""
} | tee "$report_file"

echo "Report saved to $report_file" >&2


error_rate=$(awk '$9 >= 400 {e++} END {printf "%d", e / NR * 100}' "$log_file")

if (( error_rate > max_error_rate )); then
    echo "Error rate ($error_rate%) exceeds threshold ($max_error_rate%)" >&2
    exit 2
fi