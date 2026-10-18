from logstat import parse_line

LINE = '10.0.0.1 - - [17/Oct/2026:00:30:00 +1100] "GET /health HTTP/1.1" 201 372'


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