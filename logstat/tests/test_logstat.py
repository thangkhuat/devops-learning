import pytest

from logstat import parse_line, count_statuses, top_ips, main

LINE = '10.0.0.1 - - [17/Oct/2026:00:30:00 +1100] "GET /health HTTP/1.1" 201 372'

NOBODY_LINE = '10.0.0.1 - - [02/Nov/2026:10:00:00 +0000] "GET /index.html HTTP/1.1" 304 -'

LINES = [
    '10.0.0.1 - - [17/Oct/2026:00:30:00 +1100] "GET /health HTTP/1.1" 200 372',
    '192.168.1.20 - - [17/Oct/2026:14:43:00 +1100] "GET / HTTP/1.1" 200 338',
    '10.0.0.1 - - [17/Oct/2026:16:58:00 +1100] "GET /api/users HTTP/1.1" 404 1732',
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

def test_parse_line_returns_values_for_nobody_line():
    result = parse_line(NOBODY_LINE)
    assert result["ip"] == "10.0.0.1"
    assert result["method"] == "GET"
    assert result["path"] == "/index.html"
    assert result["status"] == 304
    assert result["bytes"] == 0

def test_count_statuses_counts_codes():
    result = count_statuses(LINES)
    assert result == {200: 2, 404: 1}

def test_top_ip_return_most_common_ip():
    result = top_ips(LINES, 2)
    assert result == [('10.0.0.1',2),('192.168.1.20',1)]

def test_top_ip_with_more_than_available_ips():
    result = top_ips(LINES, 5)
    assert result == [('10.0.0.1',2), ('192.168.1.20',1)]

def test_main_rejects_nonexistent_file():
    with pytest.raises(SystemExit) as exc_info: 
        main(["nonexistent.log"])
    assert exc_info.value.code == 'logstat: nonexistent.log: no such file'

@pytest.mark.parametrize("test_input", (-3, 0))
def test_main_rejects_non_positive(test_input):
    with pytest.raises(SystemExit) as exc_info: 
        main(["access.log", "--top", str(test_input)])
    assert exc_info.value.code == 2