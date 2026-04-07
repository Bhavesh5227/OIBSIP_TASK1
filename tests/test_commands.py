# Unit tests for command matching logic
# Run with: python -m pytest tests/

import datetime

# Test time command matching
def test_time_keywords():
    command = "what time is it"
    assert any(word in command for word in ["time", "clock"])

# Test date command matching
def test_date_keywords():
    command = "what is today's date"
    assert any(word in command for word in ["date", "today", "day"])

# Test search command extraction
def test_search_query_extraction():
    command = "search python tutorials"
    query = command.replace("search", "").strip()
    assert query == "python tutorials"

# Test wikipedia query extraction
def test_wikipedia_query_extraction():
    command = "wikipedia air cooler"
    query = command.replace("wikipedia", "").strip()
    assert query == "air cooler"

# Test exit keywords
def test_exit_keywords():
    command = "exit"
    assert "exit" in command or "quit" in command