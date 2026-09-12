import discord, subprocess, tempfile

TOKEN = "YOUR_BOT_TOKEN"
CHANNEL_ID = 123456789  # 家族用チャンネル

client = discord.Client(intents=discord.Intents(messages=True, message_content=True, guilds=True))

@client.event
async def on_message(msg):
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

