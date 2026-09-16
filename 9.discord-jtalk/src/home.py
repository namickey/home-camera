import discord, subprocess, tempfile, os, asyncio, threading

CHANNEL_ID = 1547749134495383685

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

youtube_queue = asyncio.Queue()
youtube_worker_started = False

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
    global youtube_worker_started
    if not youtube_worker_started:
        youtube_worker_started = True
        client.loop.create_task(youtube_worker())

@client.event
async def on_message(msg):
    if msg.channel.id != CHANNEL_ID or msg.author.bot:
        return
    if msg.content == "停止":
        clear_youtube_queue()
        await asyncio.to_thread(stop)
        return
    if msg.content.startswith("https://www.youtube.com/"):
        for url in msg.content.splitlines():
            url = url.strip()
            if url:
                youtube_queue.put_nowait(url)
        return
    await asyncio.to_thread(speak, msg.content)

if __name__ == "__main__":
    TOKEN = os.environ["DISCORD_TOKEN"]
    client.run(TOKEN)
