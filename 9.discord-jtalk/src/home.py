import discord, subprocess, tempfile, os, asyncio, threading, re
from datetime import datetime

CHANNEL_ID = 1547749134495383685

# スケジュールファイル: 1行 = "yyyy/mm/dd hh:mm:ss|メッセージ|true/false"。
# `#` で始まる行・カラム数が合わない行は無視する。
SCHEDULE_FILE = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "schedule.txt")
SCHEDULE_POLL_INTERVAL_SEC = 60

# スマホのYouTubeアプリの共有機能では www. が付かない youtube.com や
# m.youtube.com、短縮URLの youtu.be で共有されることがあるため、
# それらもYouTube URLとして認識する。
YOUTUBE_URL_RE = re.compile(r"^https://(www\.|m\.)?youtube\.com/|^https://youtu\.be/")

client = discord.Client(intents=discord.Intents(messages=True, message_content=True, guilds=True))

PRIORITY_YOUTUBE = 0
PRIORITY_JTALK = 1

proc_lock = threading.Lock()
current_proc = None
current_priority = None

def stop():
    global current_proc, current_priority
    with proc_lock:
        if current_proc and current_proc.poll() is None:
            current_proc.terminate()
            current_proc.wait()
        current_proc = None
        current_priority = None

def run_and_wait(cmd, priority):
    global current_proc, current_priority
    with proc_lock:
        if current_proc and current_proc.poll() is None:
            if priority < current_priority:
                # 優先度が低い（jtalk再生中のyoutubeなど）ので割り込ませない
                return
            current_proc.terminate()
            current_proc.wait()
        current_proc = subprocess.Popen(cmd)
        current_priority = priority
        proc = current_proc
    proc.wait()
    with proc_lock:
        if current_proc is proc:
            current_proc = None
            current_priority = None

def play_youtube(url):
    run_and_wait(["mpv", "--no-video", url], PRIORITY_YOUTUBE)

def speak(text):
    with tempfile.NamedTemporaryFile(suffix=".wav") as f:
        subprocess.run(
            ["open_jtalk",
             "-x", "/var/lib/mecab/dic/open-jtalk/naist-jdic",
             "-m", "/usr/share/hts-voice/mei/mei_normal.htsvoice",
             "-ow", f.name],
            input=text.encode("utf-8"))
        run_and_wait(["aplay", f.name], PRIORITY_JTALK)

def parse_schedule_line(line):
    line = line.strip()
    if not line or line.startswith("#"):
        return None
    parts = line.split("|")
    if len(parts) != 3:
        return None
    dt_str, message, enabled_str = (p.strip() for p in parts)
    try:
        dt = datetime.strptime(dt_str, "%Y/%m/%d %H:%M:%S")
    except ValueError:
        return None
    return dt, message, enabled_str.lower() == "true"

def load_schedule_entries(path=None):
    entries = []
    path = path or SCHEDULE_FILE
    if not os.path.exists(path):
        return entries
    with open(path, encoding="utf-8") as f:
        for line in f:
            parsed = parse_schedule_line(line)
            if parsed:
                entries.append(parsed)
    return entries

def due_schedule_messages(entries, since, until):
    return [message for dt, message, enabled in entries
            if enabled and since < dt <= until]

async def schedule_worker():
    last_checked = datetime.now()
    while True:
        await asyncio.sleep(SCHEDULE_POLL_INTERVAL_SEC)
        now = datetime.now()
        entries = load_schedule_entries()
        for message in due_schedule_messages(entries, last_checked, now):
            await asyncio.to_thread(speak, message)
        last_checked = now

youtube_queue = asyncio.Queue()
youtube_worker_started = False
schedule_worker_started = False

def clear_youtube_queue():
    while not youtube_queue.empty():
        try:
            youtube_queue.get_nowait()
        except asyncio.QueueEmpty:
            break

async def youtube_worker():
    while True:
        url = await youtube_queue.get()
        await asyncio.to_thread(play_youtube, url)

@client.event
async def on_ready():
    global youtube_worker_started, schedule_worker_started
    if not youtube_worker_started:
        youtube_worker_started = True
        client.loop.create_task(youtube_worker())
    if not schedule_worker_started:
        schedule_worker_started = True
        client.loop.create_task(schedule_worker())

@client.event
async def on_message(msg):
    if msg.channel.id != CHANNEL_ID or msg.author.bot:
        return
    if msg.content == "停止":
        clear_youtube_queue()
        await asyncio.to_thread(stop)
        return
    if YOUTUBE_URL_RE.match(msg.content):
        for url in msg.content.splitlines():
            url = url.strip()
            if url:
                youtube_queue.put_nowait(url)
        return
    await asyncio.to_thread(speak, msg.content)

if __name__ == "__main__":
    TOKEN = os.environ["DISCORD_TOKEN"]
    client.run(TOKEN)
