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
  - プロジェクト直下の `schedule.txt`(`.gitignore`済み、`schedule.txt.example`参照)を
    60秒間隔でポーリングし、指定日時(`yyyy/mm/dd hh:mm:ss|メッセージ|true/false`)を
    過ぎた有効なエントリを読み上げる(`schedule_worker`)
- `src/discordjtalk.py` — 初期プロトタイプ。トークン/チャンネルIDがプレースホルダーの
  ままで `home.py` に置き換えられた旧版。参照用として残っているだけで実行対象ではない。

## 起動

```bash
DISCORD_TOKEN="xxxxxxxxxx" python3 src/home.py
```

## 依存する外部コマンド(Pi 側にインストール済み前提)

- `open_jtalk` + naist-jdic 辞書、音声モデルは `/usr/share/hts-voice/mei/mei_normal.htsvoice`
  にシステムインストールされているものを使う(導入手順は README.md 参照)
- `aplay`(wav再生)
- `mpv --no-video`(YouTube音声再生)
- `yt-dlp`(mpv が内部で使用)

## テスト方針

Raspberry Pi 実機用のコードを Windows/CI 上でもテストできるよう、OS・ハードウェアに依存する
部分(`subprocess.Popen`/`subprocess.run` による `open_jtalk`/`aplay`/`mpv` の実行、実際の
Discord 接続)は全てモックし、依存しない部分(優先度プリエンプション・キュー処理・
`on_message` の分岐ロジック)だけを検証する。`client.run(TOKEN)` は `if __name__ == "__main__":`
に隔離してあるため `import home` してもDiscordには接続しない。実際の音声出力・Discord疎通は
テストでは保証されず、実機での確認が必要(上記「テストコマンド」参照)。

## テストコマンド

- AI(Claude)が自律的に実行してよいコマンド — モックで完結し、外部システム(実機のDiscord/
  スピーカー/Pi)に影響しない
  - `pip install -r requirements.txt`(テスト依存関係のインストール。初回のみ)
  - `python -m pytest tests/`(ユニットテスト一式の実行)
  - `python -m pytest tests/<ファイル名> -v`(個別ファイルの実行)
- 人が実行するコマンド — 実機・実際の Discord/スピーカーに依存するため AI は自動実行しない
  - `DISCORD_TOKEN="xxxxxxxxxx" python3 src/home.py`(実際に Discord へ接続して bot を起動)
  - README.md の「疎通」コマンド(`open_jtalk` + `aplay` によるスピーカーの実音出力確認)
  - `shutdown.sh` / `volume.sh`(Pi 実機の電源操作・音量調整)

## 運用スクリプト

- `shutdown.sh` — `sudo poweroff`
- `volume.sh` — `alsamixer` を開くだけ

## 注意点

- トークンやチャンネルIDなど秘匿情報は環境変数経由で渡し、コードにハードコードしない。
- `home.py` を変更した場合、`discordjtalk.py` は追従させなくてよい(廃止予定の参照コード)。
- 実機(Pi + スピーカー + Discord)がないと `speak`/`play_youtube` の実際の音声出力は
  ローカルで検証できない。ロジック(優先度制御・キュー処理)をテストする場合は
  `subprocess.Popen` / `subprocess.run` をモックする。
