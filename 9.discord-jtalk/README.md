# discord + jtalk

## やりたいこと

- 外出先から家族に急な連絡があるが、家族がスマホを部屋に置いて、リビングでテレビを見ているため、つながらない。
- 外出先から送信したテキストメッセージを、自宅リビングで再生して伝えたい。

## コンセプト

- テキストメッセージを外出先から、自宅へ送信する
  - `Discord`を使う
  - `Discord`の`BOT`を使う
  - `Discord`のPythonクライアントライブラリを使う
- テキストメッセージを音声ファイルに変換する
  - `jtalk`を使う
- 音声ファイルを再生する
- `Raspberry Pi`+`Linux OS`を使う

## jtalk

### jtalkインストール
```bash
sudo apt install open-jtalk open-jtalk-mecab-naist-jdic
```

### 音声モデルのダウンロード
```bash
# 1. 作業用ディレクトリで、MMDAgentのサンプルパッケージをダウンロード
cd /tmp
wget https://sourceforge.net/projects/mmdagent/files/MMDAgent_Example/MMDAgent_Example-1.8/MMDAgent_Example-1.8.zip

# 2. 解凍（unzipが無ければ sudo apt install unzip）
unzip MMDAgent_Example-1.8.zip

# 3. 中身を確認 — Voice/mei/ フォルダに音声モデル（声のデータ）が入っている
ls MMDAgent_Example-1.8/Voice/mei/
# mei_angry.htsvoice  mei_bashful.htsvoice  mei_happy.htsvoice
# mei_normal.htsvoice  mei_sad.htsvoice  などが見えるはず

# 4. システムの音声フォルダを作成して、コピー配置
sudo mkdir -p /usr/share/hts-voice/mei
sudo cp MMDAgent_Example-1.8/Voice/mei/*.htsvoice /usr/share/hts-voice/mei/
```

### 疎通
```bash
# テキストから、wavファイルの生成
echo "こんにちは、きこえますか" | open_jtalk \
  -x /var/lib/mecab/dic/open-jtalk/naist-jdic \
  -m /usr/share/hts-voice/mei/mei_normal.htsvoice \
  -ow ./tmp/test.wav

# wavファイルの再生
aplay ./tmp/test.wav
```

## discord

### インストール

```bash
# 1.  このプロジェクトのディレクトリに移動する
cd ~/home-camera/9.discord-jtalk

# 2. venv作成(初回のみ)
python3 -m venv .venv

# 3. 有効化(ターミナルを開くたびに必要)
source .venv/bin/activate

# 4. モジュールをインストール
pip install -r requirements.txt
```

### 最小限の実装イメージ

```python
client = discord.Client(intents=discord.Intents(messages=True, message_content=True, guilds=True))

@client.event
async def on_message(msg):
    # 「指定チャネル」かつ「人が投稿したメッセージ（ボット以外）」であること
    if msg.channel.id != CHANNEL_ID or msg.author.bot:
        return
    with tempfile.NamedTemporaryFile(suffix=".wav") as f:
        subprocess.run(
            ["open_jtalk",
             "-x", "/var/lib/mecab/dic/open-jtalk/naist-jdic",
             "-m", "/usr/share/hts-voice/mei/mei_normal.htsvoice",
             "-ow", f.name],
            input=msg.content.encode("utf-8"))
        subprocess.run(["aplay", f.name])

client.run(TOKEN)
```

### コマンド起動

- サービス起動ではなく、手動でコマンドでの起動を行う場合
- DiscordのBOT用トークンはソースコード内に記載せず、環境変数で渡す。
- 「変数名=値」という構文で実行すると、環境変数に登録される。後続に通常コマンドを記載することも可能。

```bash
DISCORD_TOKEN="xxxxxxxxxx" python3 src/home.py
```

### サービス起動

- RaspberryPiのOS起動時に、サービスとして自動起動させる
- BOT用トークンはリポジトリに含めず、`discord-jtalk.env` にトークン値を書いて受け渡す(`.gitignore`済み)。

```bash
cd ~/home-camera/9.discord-jtalk

# 1. トークンファイルを作成(自分だけ読めるように)
cp discord-jtalk.env.example discord-jtalk.env
nano discord-jtalk.env   # DISCORD_TOKEN=実際のトークン に書き換える
chmod 600 discord-jtalk.env

# 2. venvがまだなら作成しておく(上記参照)
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt

# 3. discord-jtalk.service の User= / WorkingDirectory= / ExecStart= / EnvironmentFile=
#    のパスを自分の環境(ユーザー名・配置場所)に合わせて書き換える

# 4. サービスとして登録
sudo cp discord-jtalk.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now discord-jtalk

# 5. 状態確認・ログ確認
sudo systemctl status discord-jtalk
journalctl -u discord-jtalk -f
```

音が出ない場合は `User=` で指定したユーザーが `audio` グループに入っているか確認する(`sudo usermod -aG audio <ユーザー名>` の上、再ログインまたは再起動)。


## その他

### youtubeを再生したい

```bash
sudo apt install mpv

# 古いyoutube-dlが入っていれば削除
sudo apt remove youtube-dl

# yt-dlpを最新版でインストール
sudo apt install python3-pip
pip3 install --break-system-packages -U yt-dlp

# パスが通っているか確認（~/.local/bin に入る）
yt-dlp --version

mpv --no-video https://www.youtube.com/xxxxxxxxxxxxxxxxxxx
```

### 指定日時にメッセージを読み上げたい(スケジュール機能)

- プロジェクト直下に `schedule.txt` を置くと、bot が60秒間隔でファイルを読み込み、
  指定日時になったタイミングでメッセージを読み上げる。
- `schedule.txt` は `.gitignore` 済み(個人のスケジュールのため)。
  `schedule.txt.example` をコピーして使う。
- 1行のフォーマット: `yyyy/mm/dd hh:mm:ss|メッセージ|true(有効)/false(無効)`
- `#` で始まる行、カラム数が合わない行、日時が不正な行は無視される。
- 指定日時を過ぎたエントリは、有効フラグが `true` のままでも再度読み上げられることはない
  (ファイルは書き換えない。起動中に一度だけ読み上げ判定の対象になる仕組み)。

```bash
cp schedule.txt.example schedule.txt
nano schedule.txt
```
