# TODO — ハーネスエンジニアリング

9.discord-jtalk配下 でハーネスエンジニアリング開発スタイルで開発を行うための作業リスト。
1件ずつ作業を行い、進捗状況を`progress.md`ファイルに反映する。
作業が完了しコミットが完了したら、`todo.md`の作業をクローズ（チェックを付ける）する。

- [x] pythonソースコードをsrcディレクトリに移動する
- [x] `TODO.md` / `PROGRESS.md` をdocsディレクトリに移動する
- [x] `mei_normal.htsvoice`　ファイルを削除する
- [x] `home.py`: トップレベルの副作用(`TOKEN = os.environ["DISCORD_TOKEN"]` の取得、
      `client.run(TOKEN)`)を `if __name__ == "__main__":` ブロックに退避する。
      ロジック本体(`stop` / `run_and_wait` / `speak` / `play_youtube` /
      `clear_youtube_queue` / `youtube_worker` / `on_message` など)には手を入れない。
- [x] `requirements.txt` を作成し、依存パッケージを固定する
      (`discord.py`, `pytest`, `pytest-asyncio`, `pytest-mock`)。
- [x] `tests/conftest.py` を作成し、`subprocess.Popen` / `subprocess.run` を
      モックする共通 fixture を用意する。
- [x] テストに使用するコマンドを整理する。AIが実行するコマンド。人が実行するコマンド。
- [x] vscodeで発生している`conftest.py`でimportエラーに対処する。`home`がimportできませんでした。
- [x] vscodeで発生している`conftest.py`でimportエラーに対処する。`pytest`がimportできませんでした。
- [x] `tests/test_priority.py` を作成し、`run_and_wait` の優先度プリエンプションを検証する。
  - jtalk 再生中に YouTube が来ても割り込まない(`PRIORITY_JTALK` > `PRIORITY_YOUTUBE`)
  - YouTube 再生中に jtalk が来たら割り込んで停止・再生する
  - 再生中のプロセスが無いときは素直に起動する
- [x] テスト結果のwarning対応を行う
- [x] `tests/test_queue.py` を作成し、YouTube キュー周りを検証する。
  - `clear_youtube_queue` がキューを空にする
  - `youtube_worker` がキューから順番に取り出して再生する
- [x] `tests/test_message_routing.py` を作成し、`on_message` の分岐を検証する。
  - `"停止"` → キュークリア + `stop()` 呼び出し
  - `https://www.youtube.com/` で始まる → キューに投入
  - それ以外 → `speak()` 呼び出し
  - 対象外チャンネル / bot 自身のメッセージは無視される
- [x] discordで、youtubeのURLが複数件投稿された場合には、1件ずつキューに入れてください。
  - youtubeのURLは改行で区切られている前提としてください。
- [x] スマホのyoutubeアプリから連携した場合、URLが`https://www.youtube.com/`で始まらないため、youtubeが再生されない。
- [x] スケジュールファイルに、指定日時（yyyy/mm/dd hh:mm:ss）とメッセージと有効フラグを記載すると、指定日時にメッセージが再生される。
- [ ] youtubeファイルに記載されたURLのリストを、特定キーワード「list」というメッセージを受領すると、再生する。ファイルにはURLと有効フラグ。
