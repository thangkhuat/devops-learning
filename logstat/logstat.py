from collections import Counter
import argparse
import sys


def parse_line(line):
    #Extract parts of the log line
    fields = line.split()

    #Construct result dictionary
    try:
        return {
            "ip" : fields[0],
            "method" : fields[5].lstrip('"'),
            "path" : fields[6],
            "status" : int(fields[8]),
            "bytes" : int(fields[9]) if fields[9] != "-" else 0, #"-" means nobody, so we return 0
        }
    except (IndexError, ValueError):
        return None

def count_field(lines, field):
    counts = Counter()
    for line in lines:
        result = parse_line(line)
        if result is None:
            continue
        counts[result[field]] += 1
    return counts

def count_statuses(lines):
    return count_field(lines, "status")

def top_ips(lines, n):
    return count_field(lines, "ip").most_common(n)

def positive_integer(value):
    try:
        ivalue = int(value)
        if ivalue <= 0:
            raise ValueError
        return ivalue
    except ValueError:
        raise argparse.ArgumentTypeError(f"Top N must be a positive number, got {value}")
    
def main(argv=None):
    parser = argparse.ArgumentParser(description="Summarise an access log")
    parser.add_argument("logfile")                       
    parser.add_argument("--top", type=positive_integer, default=5)    
    args = parser.parse_args(argv)

    try:
        with open(args.logfile) as f:
            lines = f.readlines()
    except FileNotFoundError:
        sys.exit(f"logstat: {args.logfile}: no such file")

    statuses = count_statuses(lines)
    ips = top_ips(lines, args.top)

    print(f"Status codes:")
    for status, count in sorted(statuses.items()):
        print(f"{status:<15}  {count:>5}")

    print(f"\nTop {len(ips)} IPs:")
    for ip, count in ips:
        print(f"{ip:<15}  {count:>5}")

if __name__ == "__main__":
    main()