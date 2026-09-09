# discord + jtalk

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

```bash
echo "こんにちは、きこえますか" | open_jtalk \
  -x /var/lib/mecab/dic/open-jtalk/naist-jdic \
  -m /usr/share/hts-voice/mei/mei_normal.htsvoice \
  -ow /tmp/test.wav
aplay /tmp/test.wav
```