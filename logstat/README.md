# logstat

Python port of `scripts/log-report.sh`: counts status codes and top IPs in an access log. Built to practise Python, pytest and argparse.

## Setup

From the repo root:

```bash
python3 -m venv logstat/.venv
source logstat/.venv/bin/activate
pip install pytest
```

## Run it

```bash
python logstat/logstat.py access.log            # top 5 IPs (default)
python logstat/logstat.py access.log --top 3
python logstat/logstat.py --help
echo $?    # exit code, see below
```

Example output:

```
Status codes:
200                208
404                 73

Top 5 IPs:
192.168.1.20       105
10.0.0.2            88
```

`--top` must be a positive whole number. `0`, `-3` and `abc` are rejected.

## Exit codes

| Code | Meaning |
|------|---------|
| 0 | Report printed |
| 1 | Log file not found |
| 2 | Bad usage, e.g. `--top 0` (set by argparse) |

> Not the same as log-report.sh, where 2 means "error rate too high". Here argparse owns 2.

## Log format notes

- Lines that can't be parsed are skipped and not counted.
- A bytes field of `-` (no body, e.g. a 304 Not Modified) counts as 0 bytes, the same as awk in log-report.sh. Without this, valid 304 lines were dropped as bad.

## Tests

```bash
pytest logstat     # from the repo root
pytest             # from inside logstat/
```

Bare `pytest` from the repo root fails with `ModuleNotFoundError`. pytest only looks for its config (`logstat/pyproject.toml`) in the current folder and upwards, so it never finds it from the root. Passing `logstat` makes pytest start its search there, and `pythonpath = ["."]` adds the folder with `logstat.py` to `sys.path`.