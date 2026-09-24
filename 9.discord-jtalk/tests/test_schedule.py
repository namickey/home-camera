import asyncio
from datetime import datetime

import pytest

import home


def test_parse_schedule_line_valid():
    result = home.parse_schedule_line("2026/09/25 08:00:00|true|おはよう")

    assert result == (datetime(2026, 9, 25, 8, 0, 0), "おはよう", True)


@pytest.mark.parametrize("enabled_str,expected", [
    ("true", True),
    ("True", True),
    ("TRUE", True),
    ("false", False),
    ("False", False),
    ("", False),
])
def test_parse_schedule_line_enabled_flag_case_insensitive(enabled_str, expected):
    dt, message, enabled = home.parse_schedule_line(
        f"2026/09/25 08:00:00|{enabled_str}|おはよう")

    assert enabled is expected


@pytest.mark.parametrize("line", [
    "",
    "   ",
    "# コメント行",
    "2026/09/25 08:00:00|true",  # カラム数不足
    "2026/09/25 08:00:00|true|おはよう|余分",  # カラム数超過
    "2026/13/99 99:99:99|true|おはよう",  # 不正な日時
])
def test_parse_schedule_line_invalid_returns_none(line):
    assert home.parse_schedule_line(line) is None


def test_load_schedule_entries_skips_invalid_lines(tmp_path):
    schedule_file = tmp_path / "schedule.txt"
    schedule_file.write_text(
        "# コメント\n"
        "2026/09/25 08:00:00|true|おはよう\n"
        "不正な行\n"
        "2026/09/26 20:00:00|false|おやすみ\n",
        encoding="utf-8")

    entries = home.load_schedule_entries(str(schedule_file))

    assert entries == [
        (datetime(2026, 9, 25, 8, 0, 0), "おはよう", True),
        (datetime(2026, 9, 26, 20, 0, 0), "おやすみ", False),
    ]


def test_load_schedule_entries_missing_file_returns_empty_list(tmp_path):
    entries = home.load_schedule_entries(str(tmp_path / "not-exist.txt"))

    assert entries == []


def test_due_schedule_messages_filters_by_window_and_enabled_flag():
    entries = [
        (datetime(2026, 1, 1, 11, 59, 0), "有効(範囲外)", True),
        (datetime(2026, 1, 1, 12, 0, 0), "有効(範囲内)", True),
        (datetime(2026, 1, 1, 12, 0, 0), "無効(範囲内だが無効)", False),
        (datetime(2026, 1, 1, 12, 0, 1), "有効(範囲外)", True),
    ]

    due = home.due_schedule_messages(
        entries,
        since=datetime(2026, 1, 1, 11, 59, 30),
        until=datetime(2026, 1, 1, 12, 0, 0))

    assert due == ["有効(範囲内)"]


class SeqDateTime:
    """home.datetime を差し替えて now() の戻り値を制御するテストダブル。"""

    def __init__(self, times):
        self._times = list(times)

    def now(self):
        if len(self._times) > 1:
            return self._times.pop(0)
        return self._times[0]

    def strptime(self, *args, **kwargs):
        return datetime.strptime(*args, **kwargs)


@pytest.mark.asyncio
async def test_schedule_worker_speaks_due_message(monkeypatch):
    entry_dt = datetime(2026, 1, 1, 12, 0, 0)
    before = datetime(2026, 1, 1, 11, 59, 0)
    after = datetime(2026, 1, 1, 12, 0, 1)

    monkeypatch.setattr(home, "datetime", SeqDateTime([before, after]))
    monkeypatch.setattr(home, "SCHEDULE_POLL_INTERVAL_SEC", 0.01)
    monkeypatch.setattr(
        home, "load_schedule_entries",
        lambda *a, **kw: [(entry_dt, "おはよう", True)])

    spoken = []
    monkeypatch.setattr(home, "speak", lambda text: spoken.append(text))

    worker = asyncio.create_task(home.schedule_worker())
    try:
        async def wait_until_spoken():
            while not spoken:
                await asyncio.sleep(0.01)

        await asyncio.wait_for(wait_until_spoken(), timeout=2)
    finally:
        worker.cancel()
        with pytest.raises(asyncio.CancelledError):
            await worker

    assert spoken == ["おはよう"]
