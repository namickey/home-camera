# discord + jtalk

### jtalkインストール
```bash
sudo apt install open-jtalk open-jtalk-mecab-naist-jdic
```

### 音声ダウンロード
```bash
# 1. 作業用ディレクトリで、MMDAgentのサンプルパッケージをダウンロード
cd /tmp
wget https://sourceforge.net/projects/mmdagent/files/MMDAgent_Example/MMDAgent_Example-1.8/MMDAgent_Example-1.8.zip

# 2. 解凍（unzipが無ければ sudo apt install unzip）
unzip MMDAgent_Example-1.8.zip

# 3. 中身を確認 — Voice/mei/ フォルダに声のデータが入っている
ls MMDAgent_Example-1.8/Voice/mei/
# mei_angry.htsvoice  mei_bashful.htsvoice  mei_happy.htsvoice
# mei_normal.htsvoice  mei_sad.htsvoice  などが見えるはず

# 4. システムの音声フォルダにコピー（「配置」とはこの操作のこと）
sudo mkdir -p /usr/share/hts-voice/mei
sudo cp MMDAgent_Example-1.8/Voice/mei/*.htsvoice /usr/share/hts-voice/mei/
```

### 疎通
```bash
echo "こんにちは、きこえますか" | open_jtalk \
  -x /var/lib/mecab/dic/open-jtalk/naist-jdic \
  -m /usr/share/hts-voice/mei/mei_normal.htsvoice \
  -ow ./tmp/test.wav
aplay ./tmp/test.wav
```

### home.py / discordjtalk.py の実行

依存パッケージをインストールし、トークンはコミットせず環境変数で渡す。

```bash
sudo apt install pipx
pipx install discord.py
pipx install pytest
pipx install pytest-asyncio
pipx install pytest-mock

pip install -r requirements.txt
DISCORD_TOKEN="xxxxxxxxxx" python3 src/home.py
```

## その他

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

```
cd ~/home-camera/9.discord-jtalk   # このプロジェクトのディレクトリで

# 1. venv作成(初回のみ)
python3 -m venv .venv

# 2. 有効化(ターミナルを開くたびに必要)
source .venv/bin/activate

# 3. モジュールをインストール
pip install -r requirements.txt
```

### 電源投入時にサービスとして自動起動

トークンはリポジトリに含めず、`discord-jtalk.env` に実値を書いて渡す(`.gitignore`済み)。

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