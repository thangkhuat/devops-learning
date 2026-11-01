from logstat import parse_line, count_statuses

LINE = '10.0.0.1 - - [17/Oct/2026:00:30:00 +1100] "GET /health HTTP/1.1" 201 372'

LINES = [
    '10.0.0.1 - - [17/Oct/2026:00:30:00 +1100] "GET /health HTTP/1.1" 200 372',
    '192.168.1.20 - - [17/Oct/2026:14:43:00 +1100] "GET / HTTP/1.1" 200 338',
    '10.0.0.3 - - [17/Oct/2026:16:58:00 +1100] "GET /api/users HTTP/1.1" 404 1732',
    '10.0.0.1 - - [17/Oct/2026:16:51:00 +1100] "GET /admin HTTP/1.1" OK 3536'
    ]

def test_parse_line_extracts_fields():
    result = parse_line(LINE)
    assert result["ip"] == "10.0.0.1"
    assert result["method"] == "GET"
    assert result["path"] == "/health"
    assert result["status"] == 201
    assert result["bytes"] == 372

def test_parse_line_returns_none_for_bad_lines():
    assert parse_line("garbage") is None
    assert parse_line('10.0.0.1 - - [17/Oct/2026:00:30:00 +1100] "GET / HTTP/1.1" OK 338') is None

def test_count_statuses_counts_codes():
    result = count_statuses(LINES)
    assert result == {200: 2, 404: 1}