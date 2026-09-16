from types import SimpleNamespace

import pytest

import home


def make_message(content, channel_id=home.CHANNEL_ID, bot=False):
    return SimpleNamespace(
        content=content,
        channel=SimpleNamespace(id=channel_id),
        author=SimpleNamespace(bot=bot),
    )


@pytest.mark.asyncio
async def test_stop_message_clears_queue_and_stops(monkeypatch):
    home.youtube_queue.put_nowait("https://www.youtube.com/watch?v=1")
    stop_calls = []
    monkeypatch.setattr(home, "stop", lambda: stop_calls.append(True))

    await home.on_message(make_message("停止"))

    assert home.youtube_queue.empty()
    assert stop_calls == [True]


@pytest.mark.asyncio
async def test_youtube_url_is_queued_not_spoken(monkeypatch):
    speak_calls = []
    monkeypatch.setattr(home, "speak", lambda text: speak_calls.append(text))

    await home.on_message(make_message("https://www.youtube.com/watch?v=abc"))

    assert home.youtube_queue.get_nowait() == "https://www.youtube.com/watch?v=abc"
    assert speak_calls == []


@pytest.mark.asyncio
async def test_multiple_youtube_urls_are_queued_one_by_one(monkeypatch):
    speak_calls = []
    monkeypatch.setattr(home, "speak", lambda text: speak_calls.append(text))
    content = "https://www.youtube.com/watch?v=1\nhttps://www.youtube.com/watch?v=2\nhttps://www.youtube.com/watch?v=3"

    await home.on_message(make_message(content))

    assert home.youtube_queue.get_nowait() == "https://www.youtube.com/watch?v=1"
    assert home.youtube_queue.get_nowait() == "https://www.youtube.com/watch?v=2"
    assert home.youtube_queue.get_nowait() == "https://www.youtube.com/watch?v=3"
    assert home.youtube_queue.empty()
    assert speak_calls == []


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "url",
    [
        "https://youtu.be/abc123",
        "https://youtube.com/watch?v=abc123",
        "https://m.youtube.com/watch?v=abc123",
        "https://youtube.com/shorts/abc123",
    ],
)
async def test_mobile_app_shared_youtube_url_is_queued_not_spoken(monkeypatch, url):
    speak_calls = []
    monkeypatch.setattr(home, "speak", lambda text: speak_calls.append(text))

    await home.on_message(make_message(url))

    assert home.youtube_queue.get_nowait() == url
    assert speak_calls == []


@pytest.mark.asyncio
async def test_other_text_is_spoken(monkeypatch):
    speak_calls = []
    monkeypatch.setattr(home, "speak", lambda text: speak_calls.append(text))

    await home.on_message(make_message("こんにちは"))

    assert speak_calls == ["こんにちは"]


@pytest.mark.asyncio
async def test_message_from_other_channel_is_ignored(monkeypatch):
    speak_calls = []
    monkeypatch.setattr(home, "speak", lambda text: speak_calls.append(text))

    await home.on_message(make_message("こんにちは", channel_id=home.CHANNEL_ID + 1))

    assert speak_calls == []
    assert home.youtube_queue.empty()


@pytest.mark.asyncio
async def test_message_from_bot_is_ignored(monkeypatch):
    speak_calls = []
    monkeypatch.setattr(home, "speak", lambda text: speak_calls.append(text))

    await home.on_message(make_message("こんにちは", bot=True))

    assert speak_calls == []
    assert home.youtube_queue.empty()
