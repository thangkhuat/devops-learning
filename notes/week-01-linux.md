# Learning Log

## Week 1 (11–18 Oct) — Linux & Bash log analyser

### Sun 11 Oct — Setup (~1 h)
- Done: WSL Ubuntu, Git + SSH to GitHub, repo moved to ~/, nginx logging
- Hard: git push failed (HTTPS remote) → switched to SSH
- Learned: cd, mv, &&, git status, /mnt/c vs ~
- Next: make test log, create feature branch

### Thursday 15 Oct - Linux basics (1h + 1h)
1st hour:
- Done: Navigate the file system (absolute vs relative path), learn about the linux folder, create, copy, move, rename and delete files safely
- Hard: remember the linux folder and their dedicated functions (do 5 practice drill questions a day)
- Learned: cd, mv, cp, rm, rmdir, mkdir, ls

2nd hour:
- Done: Learn about how to read directory and file permission using ls -ld, change permission, understand umask, pipe
- Hard: creating complex pipes (practice building pipe block by block)
- Learned: grep, wc, cut, sort, uniq, head, tail, ls -ld, chmod, find, umask, redirects (>, >>, 2>/dev/null), chmod u+x + ./script.sh, $PATH, ./, ~/.local/bin, .profile
- Next: processes and services

### Friday 16 Oct - Processes & services (3h)
Warm-up:
- Folder drill 4/5 (missed /proc = live view of kernel & running processes, one folder per PID)
- Pipe: cut -d: -f7 /etc/passwd | sort | uniq -c | sort -rn (sort -rn = numeric, biggest first; tail -n 1 was wrong because uniq -c output is alphabetical)

1st hour:
- Done: PID/PPID and the process tree, inspect processes via ps and /proc, foreground/background jobs, signals, find and stop a runaway CPU process with top/ps/pgrep/pkill, read load average
- Hard: why SIGTERM before SIGKILL (TERM = process can clean up; KILL = kernel removes it instantly, risk of corrupted data/stale lock files); signal names; reading load average trends. Which kill to use
- Learned: echo $$, $!, ps, ps -ef, ps -eo ... --sort=-%cpu, pstree -p, /proc/<PID>/status, process states (R running, S sleeping), PID 1 = systemd (/sbin/init symlink), PPID 0 = kernel, commands run as children of the shell, jobs, Ctrl+Z, bg, fg %n, &, kill, kill -9, kill -l, Ctrl+C = SIGINT, Ctrl+Z = SIGTSTP, SIGHUP = reload config, top (P/M/q), load average (1/5/15 min, compare against nproc), pgrep -a, pkill -x, pkill -u
- Rule: preview with pgrep -a before pkill; TERM first, KILL only if ignored. Know the PID → kill <PID>. Know only the name → pgrep -a to preview, then pkill -x <name>. Ignored for ~10 sec → add -9.

2nd hour:
- Done: inspect a service with systemctl, active vs enabled, enable/disable and the .wants/ symlinks, read a unit file, watch systemd restart a crashed service, write + enable my own service (heartbeat.service)
- Hard: active vs enabled (active = running now, enabled = starts at next boot); how WantedBy connects to .wants/; unit file comments must be on their own line (inline # broke WantedBy). Connect the pieces i have learned together.
- Learned: systemctl list-units --type=service --state=running, systemctl status/start/stop/restart, is-active, is-enabled, enable, enable --now, disable, systemctl cat, systemctl show -p MainPID --value, daemon-reload, systemd-analyze verify, unit file sections [Unit]/[Service]/[Install], ExecStart (absolute path), Restart=on-failure, User=, WantedBy=multi-user.target, /usr/lib/systemd/system (package units) vs /etc/systemd/system (my units), services have PPID 1
- Rule: kill -9 = failure → systemd restarts it; systemctl stop = intended → no restart. Least privilege: set User=, never run a user-editable script as root

3rd hour:
- Done: connect processes to services (systemd = parent + supervisor), catch SIGTERM with trap, read service logs with journalctl, watch a crash + auto-restart live, on-call drills (count crashes, broken ExecStart path, missing execute permission)
- Hard: why trap doesn't run on kill -9 (SIGKILL never reaches the process); start limit (5 fails in 10s → stops retrying); exit 203/EXEC = couldn't run ExecStart (check the journal for why)
- Learned: journalctl -u, -n, -f, --since "10 min ago"/today, -p err, -b, --no-pager, logger -p user.err, trap '...' TERM, systemctl stop = SIGTERM to the whole CGroup, Failed with result 'signal'/'exit-code'/'timeout', restart counter, Start request repeated too quickly, reset-failed, grep -c, pgrep -af, grep [h]eartbeat trick
- Rule: grep "Failed with result" for any crash; status shows what, journal shows why
- Next: bash scripting basics + awk, then build the log-analysis script + cron

### Saturday 17 Oct - Bash scripting, awk & cron (3h)
Warm-up:
- Recall 2.5/5: /proc missed "live/virtual"; mixed up journalctl vs systemctl status; forgot reset-failed for start limit; kill only takes PIDs (names → pgrep/pkill)
- Pipe: sort -r is text order (9 > 12) → use sort -rn for counts
- Installed tealdeer (tldr). Ubuntu dropped the old tldr package → apt search <name> to find the right one

1st hour:
- Done: run scripts 3 ways, shebang, set -euo pipefail, arguments + usage check, exit codes, svc-check.sh
- Hard: remembering flags; which set flag does what; $? only holds the LAST command's exit code. Rembering the flag for each command line (install tldr for quicksearch)
- Learned: ./ needs +x, bash file.sh only needs read; ./ because current dir isn't in $PATH; $0 $1 $# $?; scripts inherit env vars (WSL sets NAME=hostname); VAR=value cmd = env var for that one command; set -e (exit on fail) / -u (unset var = error) / -o pipefail (any pipe stage fails); >&2 = stderr; 2>/dev/null; [[ $# -ne 1 ]]; if <command> tests its exit code; systemctl is-active/is-enabled --quiet; exit codes 0 / 1 / 127 / 203
- Rule: every script starts with #!/usr/bin/env bash + set -euo pipefail. UPPERCASE = env vars, lowercase = my vars. Always quote "$var". cmd; echo $? to check a result
- Flags I looked up: cut -d -f, sort -rn, uniq -c, pgrep -a, pkill -x

2nd hour:
- Done: generated a 500-line access.log with a bash loop + arrays, awk fields, patterns, counting with END + arrays, split(), printf, error-rate summary
- Hard: quoting text in awk (bare words are variables → silent 0 results); >= 400 not >= 404 / > 400 (write the rule I mean, not one that fits today's data); building printf correctly
- Learned: bash arrays ips=(...), ${#arr[@]}, $RANDOM, %; awk 'pattern {action}' file; $0 $1 $NF NF NR; access.log fields $1 IP / $4 time / $7 path / $9 status / $10 bytes; patterns ==, >=, &&, /regex/, \. = literal dot; END runs once after the last line, BEGIN once before the first; count[$x]++ then for (k in count) | sort -rn; sum += $10; total/NR = average; -F: for /etc/passwd; split($4, t, ":"); printf %d %s %-8s %.1f %% \n
- Rule: a suspicious 0 means check the command (drop wc -l, look at the matched lines). Text goes in "quotes" in awk. printf: fixed template, values as arguments. Check results against what I expect (~20% 5xx)
- Flags I looked up: awk -F, sort -nr
- Next: build log-report.sh + schedule it with cron

3rd hour:
- Done: built log-report.sh in 4 stages (input checks → report → save to dated file → alert exit code), scheduled it with cron, investigated a gap in cron runs
- Hard: spaces around = (log_file = "$1" → "command not found"); $9 > 400 instead of >= 400 again (3rd time); remembering to quote "$log_file" everywhere; testing BOTH the pass and fail paths
- Learned: [[ -f / -r / -s ]] and ! to negate; validate inputs BEFORE changing anything (mkdir after checks); $HOME instead of hardcoded paths; { ... } | tee file = save + show; (( )) for whole-number maths (no $ needed); awk printf "%d" to hand bash an integer; exit codes 0 healthy / 1 script failed / 2 alert; cron fields m h dom mon dow, */2, crontab -e/-l; absolute paths in cron; >> file 2>&1; journalctl -u cron shows CMD lines; realpath
- Investigation: runs stopped 19:38–20:34 → laptop slept (PIDs continued = resumed, not rebooted); on wake, cron ran the job once at an odd time, no catch-up. Cron reports were 25 bytes bigger = absolute path in the header. Cron's files had different permissions = different environment (umask)
- Rule: cron only logs that a job STARTED, never whether it succeeded. Exit 2 is silently ignored → the alerting has to come from the script or monitoring. Cron skips runs while asleep (use anacron or systemd timers with Persistent=true for laptops)
- Flags I looked up: date +%F %T %H%M, tee, mkdir -p
- Next: systemd timer version of log-report (compare with cron), make the script send a real alert, then git basics to put ~/devops-learning under version control

### Sunday 18 Oct - systemd timers, alerting & Git PRs (2.5h)
Week 1 complete ✅ (Linux & Bash → log-analysis script, scheduled + alerting, README, merged via PR)

Warm-up:
- Recall 3/5 (up from 2.5): missed -u (unset variable = error); cron failures = different environment (cwd is $HOME, minimal PATH, different umask), not just "file failed"; catch-up tools = anacron / systemd timer Persistent=true
- Got $9 >= 400 right first time ✅. print count+0 so 0 matches prints 0 not blank
- systemctl is-system-running → running (systemd works in WSL)
- Git habit to fix: I'd been committing straight to main → from today every piece of work goes on a branch + PR

1st hour:
- Done: branch systemd-timer, wrote log-report.service (oneshot) + log-report.timer, installed, enabled, confirmed it fires by itself, removed the cron job
- Hard: "Unit not found" → forgot systemd only reads /etc/systemd/system, not my repo; skipped my predictions 3 times; [Install] reasoning ("start time" is OnCalendar, not [Install])
- Learned: Type=oneshot (runs, finishes, exits); oneshot healthy = inactive (dead), problem = failed; any non-zero exit → unit failed, exit code + output kept in journal (cron kept neither); status=2/INVALIDARGUMENT is just systemd's label for code 2, read the number; exit 1 and 2 both show "failed"; timer starts the service with the same name; OnCalendar format DayOfWeek Y-M-D H:M:S, *:0/2 = every 2 min; normalized form shows the full meaning; AccuracySec default 1min (sub-minute timers not precise); Persistent=true catches up missed runs; [Install] + enable = start at boot → enable the timer, not the service; list-timers shows NEXT / LEFT / LAST / ACTIVATES
- Rule: repo copy = source of truth, /etc copy = what runs → after any edit: cp, daemon-reload, restart (drift). Remove the old scheduler before adding a new one (both would write the same HHMM filename and overwrite). Predict BEFORE running
- Flags I looked up: systemd-analyze calendar --iterations=3, systemctl enable --now, systemctl list-timers, journalctl -n 20 --no-pager, journalctl -xeu (noisy)

2nd hour:
- Done: designed alerting against alert fatigue, wrote alert.sh with 30 min cooldown + state file, tested all paths (missing / recent / expired / corrupt), fixed corrupt-file crash, refactored to elif + regression tested, wired OnFailure=log-report-alert.service, watched it alert then suppress, timer switched to hourly
- Hard: predicting the garbage state file (crash via -u: bare word in (( )) = variable name); thought running as root would error (it works silently in /root/.cache = 2 separate cooldowns); OnCalendar 0/1:*:* = every SECOND
- Learned: alert fatigue → rate limit / cooldown (other options: run less often, alert on state change, require sustained failure); date +%s = epoch seconds; state file pattern; [[ "$x" =~ ^[0-9]+$ ]] to validate numbers; fail open (when unsure, alert) vs fail closed (silent = worst case); last=$now would have suppressed forever; OnFailure= in [Unit]; $HOME depends on User=; journalctl -f follows live; * means "every", not "any one"; hourly = *:00:00
- Rule: validate any input read from a file. Alerting fails open: a duplicate alert beats a missed one. After a refactor, re-run every test path. Always set User= and check where state files land. Pin smaller fields for "once per X" + check with systemd-analyze calendar
- Flags I looked up: date +%s, dirname, mkdir -p, journalctl -f

Last 30 min:
- Done: README (files, run by hand, exit codes, install, alerting, why timer vs cron), PR #1 merged; PR #2 .gitignore for generated files
- Hard: README template prompts left in; markdown tables/code blocks not rendering; first draft overclaimed ("prevent malicious attempts") and described old code
- Learned: README at repo root shows on GitHub; scripts don't go in /etc/systemd/system, only units; markdown tables need |---| row, commands need ```bash fences; push output 946baa3..8d41fd6 = branch already existed (vs * [new branch]); -u sets upstream tracking; PR → review Files changed → merge → delete branch → git switch main + git pull; git fetch --prune removes stale remote branches; generated output stays out of Git (.gitignore); git rm --cached = untrack but keep on disk
- Rule: main only changes through PRs; every session starts with git switch -c <topic>. A README that describes old code is worse than none. Commit what I write, not what my code produces
- Flags I looked up: git push -u, git branch -a, git fetch --prune, git rm -r --cached

Next:
- Week 2: Python CLI with pytest
- Optional: real push alert (curl to a push service) instead of journal only
- Optional warm-up: retention policy for reports/ (find -mtime, delete > 7 days)

**Week total:**