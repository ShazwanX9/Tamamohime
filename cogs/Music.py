import os
import sys
import discord
import youtube_dl
from dotenv import load_dotenv
from discord.ext import commands

##################################################################################################################################
load_dotenv()

BOT_NAME = os.getenv("bot_name")
youtube_dl.utils.bug_reports_message = lambda: ''

YTDL_OPTS =  {
    'format': 'bestaudio/best',
    'extractaudio': True,
    'audioformat': 'mp3',
    'outtmpl': 'music_download1.mp3',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0',
}

class Music(commands.Cog):
    f"Wish for {BOT_NAME} to entertain your  boring talk?"

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name = "join", help = f"Invite {BOT_NAME} to Voice Channel")
    async def join(self, ctx):
        channel = ctx.author.voice.channel
        await channel.connect()

    @commands.command(name = "leave", help = f"Expel {BOT_NAME} from Voice Channel")
    async def leave(self, ctx):
        await ctx.voice_client.disconnect()

    @commands.command(name = "play", help = "Play the song", aliases = ["p"])
    async def play(self, ctx, url):

        voice_client = self.bot.voice_clients[0]
 
        ytdl = youtube_dl.YoutubeDL(YTDL_OPTS)
        info = ytdl.extract_info(url, download=False)
        asrc = discord.FFmpegOpusAudio(info['formats'][0]['url'], before_options="-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5")
        voice_client.play(asrc)

        await ctx.send(f"**Now playing:** {url}")

    @commands.command(name = "pause", help = "Pauses the song")
    async def pause(self, ctx):
        voice_client = ctx.message.guild.voice_client
        if voice_client.is_playing():
            await voice_client.pause()
        else:
            await ctx.send(f"{BOT_NAME} is not playing anything at the moment.")

    @commands.command(name = "resume", help = "Resumes the song")
    async def resume(self, ctx):
        voice_client = ctx.message.guild.voice_client
        if voice_client.is_paused():
            await voice_client.resume()
        else:
            await ctx.send(f"{BOT_NAME} was not playing anything before this. Use play command")

    @commands.command(name = "stop", help = "Stops the song")
    async def stop(self, ctx):
        voice_client = ctx.message.guild.voice_client
        if voice_client.is_playing():
            await voice_client.stop()
        else:
            await ctx.send(f"{BOT_NAME} is not playing anything at the moment.")

def setup(bot):
    bot.add_cog(Music(bot))