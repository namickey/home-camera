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

トークンはコミットせず、環境変数で渡す。

```bash
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


