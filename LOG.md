# Learning Log

## Week 1 (12–18 Oct) — Linux & Bash log analyser

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
- Next: networking basics (ip, ss -tulpn = which process is listening on which port, curl) — links processes to the network
**Week total:**