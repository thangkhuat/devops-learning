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
            "bytes" : int(fields[9]),
        }
    except (IndexError, ValueError):
        return None

if __name__ == "__main__":
    print(parse_line('10.0.0.1 - - [17/Oct/2026:00:30:00 +1100] "GET /health HTTP/1.1" 201 372'))