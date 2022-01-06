import asyncio

import discord
import youtube_dl

from discord.ext import commands

# Suppress noise about console usage from errors
youtube_dl.utils.bug_reports_message = lambda: ""


ytdl_format_options = {
    "format": "bestaudio/best",
    "outtmpl": "%(extractor)s-%(id)s-%(title)s.%(ext)s",
    "restrictfilenames": True,
    "noplaylist": True,
    "nocheckcertificate": True,
    "ignoreerrors": False,
    "logtostderr": False,
    "quiet": True,
    "no_warnings": True,
    "default_search": "auto",
    "source_address": "0.0.0.0",  # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {"options": "-vn"}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)


class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get("title")
        self.url = data.get("url")

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(
            None, lambda: ytdl.extract_info(url, download=not stream)
        )

        if "entries" in data:
            # take first item from a playlist
            data = data["entries"][0]

        filename = data["url"] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)


class Song(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print("Song initialised")
        self.bot.playlists = {}

    @commands.command(name="join", aliases=["j"], help="Joins a voice channel")
    async def join(self, ctx):
        if ctx.author.voice is None or ctx.author.voice.channel is None:
            return await ctx.send(
                "You need to be in a voice channel to use this command!"
            )

        voice_channel = ctx.author.voice.channel
        if ctx.voice_client is None:
            vc = await voice_channel.connect()
        else:
            await ctx.voice_client.move_to(voice_channel)
            vc = ctx.voice_client

    @commands.command(
        name="leave", aliases=["disconnect"], help="Leaves a voice channel"
    )
    async def leave(self, ctx):
        await ctx.voice_client.disconnect()

    @commands.command(name="piss", aliases=["pissing"])
    async def piss(self, ctx):
        serverid = ctx.guild

        if self.bot.playlists.get(serverid) is None:
            self.bot.playlists[serverid] = list()

        else:
            self.bot.playlists[serverid].append("Momentary bliss")
            print(self.bot.playlists[serverid])

        async with ctx.typing():
            player = await YTDLSource.from_url("Momentary bliss", loop=self.bot.loop, stream=True)
            ctx.voice_client.play(
                player, after=lambda e: print("Player error: %s" % e) if e else None
            )
        await ctx.send("Now playing: {}".format(player.title))

    @commands.command(name="play", aliases=["p"], help="Streams music")
    async def play(self, ctx, *, url):
        #     async def play(self, ctx, url):
        #         print(ctx)
        #         print(url)
        #         if ctx.voice_client.is_playing():
        serverid = ctx.guild

        if self.bot.playlists.get(serverid) is None:
            self.bot.playlists[serverid] = list()

        else:
            self.bot.playlists[serverid].append(url)
            print(self.bot.playlists[serverid])

        async with ctx.typing():
            player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
            ctx.voice_client.play(
                player, after=lambda e: print("Player error: %s" % e) if e else None
            )
        await ctx.send("Now playing: {}".format(player.title))

    @commands.command(name="pause", help="Pauses the song")
    async def pause(self, ctx):
        if ctx.voice_client.is_playing():
            ctx.voice_client.pause()
        else:
            await ctx.message.channel.send("The bot is not playing any music")

    @commands.command(name="resume", help="Resumes the song")
    async def resume(self, ctx):
        if ctx.voice_client.is_paused():
            ctx.voice_client.resume()
        else:
            await ctx.message.channel.send("No music has been paused")


def setup(bot):
    bot.add_cog(Song(bot))
