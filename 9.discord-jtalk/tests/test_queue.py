import asyncio

import pytest

import home


def test_clear_youtube_queue_empties_queue():
    home.youtube_queue.put_nowait("https://www.youtube.com/watch?v=1")
    home.youtube_queue.put_nowait("https://www.youtube.com/watch?v=2")

    home.clear_youtube_queue()

    assert home.youtube_queue.empty()


@pytest.mark.asyncio
async def test_youtube_worker_plays_queued_urls_in_order(monkeypatch):
    played = []
    monkeypatch.setattr(home, "play_youtube", lambda url: played.append(url))

    home.youtube_queue.put_nowait("https://www.youtube.com/watch?v=1")
    home.youtube_queue.put_nowait("https://www.youtube.com/watch?v=2")

    worker = asyncio.create_task(home.youtube_worker())
    try:
        async def wait_until_played(count):
            while len(played) < count:
                await asyncio.sleep(0.01)

        await asyncio.wait_for(wait_until_played(2), timeout=2)
    finally:
        worker.cancel()
        with pytest.raises(asyncio.CancelledError):
            await worker

    assert played == [
        "https://www.youtube.com/watch?v=1",
        "https://www.youtube.com/watch?v=2",
    ]
