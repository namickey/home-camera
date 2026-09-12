# 進捗状況 — ハーネスエンジニアリング

対応する作業内容は [todo.md](./todo.md) を参照。

| 項目 | 状態 | 更新日 | メモ |
|---|---|---|---|
| pythonソースコードをsrcディレクトリに移動する | 完了 | 2026-09-13 | home.py / discordjtalk.py を `src/` へ移動(git mv)。README.md / CLAUDE.md の起動コマンドも `src/home.py` に更新 |
| TODO.md / PROGRESS.md をdocsディレクトリに移動する | 完了 | 2026-09-13 | todo.md / progress.md を `docs/` へ移動(git mv)。参照リンクは相対パスのまま維持 |
| mei_normal.htsvoice ファイルを削除する | 完了 | 2026-09-13 | git rm で削除。README.md の疎通確認コマンドをシステムパス(`/usr/share/hts-voice/mei/mei_normal.htsvoice`)参照に修正、CLAUDE.md の記述も更新 |
| home.py の副作用を `__main__` ガード化 | 進行中 | 2026-09-13 | `TOKEN` 取得と `client.run(TOKEN)` を `if __name__ == "__main__":` に移動。ロジック関数には変更なし。`DISCORD_TOKEN` 未設定でも `import home` できることを確認済み。コミット待ち |
| requirements.txt 作成 | 未着手 | 2026-09-13 | |
| tests/conftest.py 作成 | 未着手 | 2026-09-13 | |
| test_priority.py 作成 | 未着手 | 2026-09-13 | |
| test_queue.py 作成 | 未着手 | 2026-09-13 | |
| test_message_routing.py 作成 | 未着手 | 2026-09-13 | |

状態は `未着手` / `進行中` / `完了` / `保留` のいずれかを記入する。
