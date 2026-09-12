import pytest

import home


class FakeProcess:
    """subprocess.Popen の戻り値を模したテストダブル。

    デフォルトは「即座に終了したプロセス」(poll()/wait() が 0 を返す)。
    実行中のプロセスを再現したい場合は、テスト側で returncode を None にする。
    """

    def __init__(self, cmd):
        self.cmd = cmd
        self.returncode = 0
        self.terminated = False

    def poll(self):
        return self.returncode

    def wait(self):
        self.returncode = 0
        return self.returncode

    def terminate(self):
        self.terminated = True
        self.returncode = 0


@pytest.fixture(autouse=True)
def reset_home_state():
    """home モジュールのグローバル状態(実行中プロセス・キュー)をテスト間でリセットする。"""
    home.stop()
    home.clear_youtube_queue()
    yield
    home.stop()
    home.clear_youtube_queue()


@pytest.fixture
def mock_popen(monkeypatch):
    """run_and_wait が呼ぶ subprocess.Popen をモックする。

    生成した FakeProcess を呼び出し順に記録したリストを返す。
    """
    created = []

    def fake_popen(cmd, *args, **kwargs):
        proc = FakeProcess(cmd)
        created.append(proc)
        return proc

    monkeypatch.setattr(home.subprocess, "Popen", fake_popen)
    return created


@pytest.fixture
def make_running_process():
    """まだ終了していない(poll() が None を返す)FakeProcess を作るヘルパー。

    優先度プリエンプションのテストで「再生中のプロセス」を再現するために使う。
    """
    def _make(cmd):
        proc = FakeProcess(cmd)
        proc.returncode = None
        return proc

    return _make


@pytest.fixture
def mock_run(monkeypatch):
    """speak が呼ぶ subprocess.run(open_jtalk) をモックする。

    呼び出しごとの cmd/kwargs を記録したリストを返す。
    """
    calls = []

    def fake_run(cmd, *args, **kwargs):
        calls.append({"cmd": cmd, "kwargs": kwargs})
        return None

    monkeypatch.setattr(home.subprocess, "run", fake_run)
    return calls
