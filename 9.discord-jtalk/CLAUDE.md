# discord-jtalk

Raspberry Pi 上で動く Discord bot。家族用チャンネルに投稿されたテキストを
open_jtalk で読み上げ、YouTube URL が投稿されたら mpv で音声再生する。

## エントリーポイント

- **`src/home.py`** — 本体。これが実際に動かすファイル。
  - `DISCORD_TOKEN` 環境変数からトークンを取得(ハードコード禁止)
  - 優先度付きプロセス管理(`PRIORITY_JTALK` > `PRIORITY_YOUTUBE`)により、
    YouTube 再生中でも読み上げが割り込める
  - YouTube URL は `asyncio.Queue` でキューイングして順に再生
  - `"停止"` というメッセージでキュー全クリア+再生中プロセスを止める
- `src/discordjtalk.py` — 初期プロトタイプ。トークン/チャンネルIDがプレースホルダーの
  ままで `home.py` に置き換えられた旧版。参照用として残っているだけで実行対象ではない。

## 起動

```bash
DISCORD_TOKEN="xxxxxxxxxx" python3 src/home.py
```

## 依存する外部コマンド(Pi 側にインストール済み前提)

- `open_jtalk` + naist-jdic 辞書、音声モデルは `/usr/share/hts-voice/mei/mei_normal.htsvoice`
  にシステムインストールされているものを使う(リポジトリ直下の `mei_normal.htsvoice` は
  疎通確認用のローカルコピーで、本体コードからは参照していない)
- `aplay`(wav再生)
- `mpv --no-video`(YouTube音声再生)
- `yt-dlp`(mpv が内部で使用)

## 運用スクリプト

- `shutdown.sh` — `sudo poweroff`
- `volume.sh` — `alsamixer` を開くだけ

## 注意点

- トークンやチャンネルIDなど秘匿情報は環境変数経由で渡し、コードにハードコードしない。
- `home.py` を変更した場合、`discordjtalk.py` は追従させなくてよい(廃止予定の参照コード)。
- 実機(Pi + スピーカー + Discord)がないと `speak`/`play_youtube` の実際の音声出力は
  ローカルで検証できない。ロジック(優先度制御・キュー処理)をテストする場合は
  `subprocess.Popen` / `subprocess.run` をモックする。
