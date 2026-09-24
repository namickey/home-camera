import pytest

import home


def test_parse_youtube_list_line_valid():
    result = home.parse_youtube_list_line("true|https://www.youtube.com/watch?v=1")

    assert result == (True, "https://www.youtube.com/watch?v=1")


def test_parse_youtube_list_line_disabled():
    result = home.parse_youtube_list_line("false|https://www.youtube.com/watch?v=1")

    assert result == (False, "https://www.youtube.com/watch?v=1")


@pytest.mark.parametrize("line", [
    "",
    "   ",
    "# コメント行",
    "true",  # カラム数不足
    "true|https://www.youtube.com/watch?v=1|余分",  # カラム数超過
    "true|",  # URLが空
])
def test_parse_youtube_list_line_invalid_returns_none(line):
    assert home.parse_youtube_list_line(line) is None


def test_load_youtube_list_entries_skips_invalid_lines(tmp_path):
    list_file = tmp_path / "youtube.txt"
    list_file.write_text(
        "# コメント\n"
        "true|https://www.youtube.com/watch?v=1\n"
        "不正な行\n"
        "false|https://www.youtube.com/watch?v=2\n",
        encoding="utf-8")

    entries = home.load_youtube_list_entries(str(list_file))

    assert entries == [
        (True, "https://www.youtube.com/watch?v=1"),
        (False, "https://www.youtube.com/watch?v=2"),
    ]


def test_load_youtube_list_entries_missing_file_returns_empty_list(tmp_path):
    entries = home.load_youtube_list_entries(str(tmp_path / "not-exist.txt"))

    assert entries == []


def test_enabled_youtube_urls_filters_and_preserves_order():
    entries = [
        (True, "https://www.youtube.com/watch?v=1"),
        (False, "https://www.youtube.com/watch?v=2"),
        (True, "https://www.youtube.com/watch?v=3"),
    ]

    assert home.enabled_youtube_urls(entries) == [
        "https://www.youtube.com/watch?v=1",
        "https://www.youtube.com/watch?v=3",
    ]
