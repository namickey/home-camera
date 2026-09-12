import home


def test_low_priority_youtube_does_not_interrupt_jtalk(mock_popen, make_running_process):
    running = make_running_process(["aplay", "voice.wav"])
    home.current_proc = running
    home.current_priority = home.PRIORITY_JTALK

    home.run_and_wait(
        ["mpv", "--no-video", "https://www.youtube.com/watch?v=x"],
        home.PRIORITY_YOUTUBE,
    )

    assert mock_popen == []
    assert running.terminated is False
    assert home.current_proc is running
    assert home.current_priority == home.PRIORITY_JTALK


def test_high_priority_jtalk_interrupts_youtube(mock_popen, make_running_process):
    running = make_running_process(["mpv", "--no-video", "https://www.youtube.com/watch?v=x"])
    home.current_proc = running
    home.current_priority = home.PRIORITY_YOUTUBE

    home.run_and_wait(["aplay", "voice.wav"], home.PRIORITY_JTALK)

    assert running.terminated is True
    assert len(mock_popen) == 1
    assert mock_popen[0].cmd == ["aplay", "voice.wav"]
    assert home.current_proc is None
    assert home.current_priority is None


def test_starts_immediately_when_nothing_is_running(mock_popen):
    assert home.current_proc is None

    home.run_and_wait(
        ["mpv", "--no-video", "https://www.youtube.com/watch?v=x"],
        home.PRIORITY_YOUTUBE,
    )

    assert len(mock_popen) == 1
    assert mock_popen[0].cmd == ["mpv", "--no-video", "https://www.youtube.com/watch?v=x"]
    assert home.current_proc is None
    assert home.current_priority is None
