import asyncio
import typing
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

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

playlist = []
paused = False


class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get("title")
        self.url = data.get("url")

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=True, timestamp=0):
        # moved the options from outside the class to inside the method.
        # this allows the use of variables in the options
        ffmpeg_options = {"options": f"-vn -ss {timestamp}"}
        # rest of the from_url code
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

    @commands.command
    async def on_ready():
        print('client ready')

    async def audio_player_task(self, ctx):
        while not ctx.voice_client.is_playing() and not paused and self.bot.playlists.get(serverid) is not None:
#         while not ctx.voice_client.is_playing() and not paused and len(playlist) > 1:
            async with ctx.typing():
                serverid = ctx.guild
                player = await YTDLSource.from_url(
                    self.bot.playlists[serverid][0], loop=self.bot.loop, stream=True, timestamp=0
                )
                ctx.voice_client.play(
                    player, after=lambda e: print("Player error: %s" % e) if e else None
                )

            await ctx.send("Now playing: {}".format(player.title))
#                 playlist.pop(0)
#                 playlist.pop(0)

#         while True:
#             play_next_song.clear()
#             current = await songs.get()
#             current.start()
#             await play_next_song.wait()
#
#     def toggle_next():
#         client.loop.call_soon_threadsafe(play_next_song.set)

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

    @commands.command(name="play", aliases=["p"], help="Use [timestamp in seconds] song name to start playing from a certain part of a song")
    async def play(self, ctx, timestamp: typing.Optional[int] = 0, *, url):
        voice_channel = ctx.author.voice.channel

        if ctx.voice_client is None:
            vc = await voice_channel.connect()
#         elif not ctx.voice_channel.is_playing() and ctx.voice.channel != ctx.author.voice.channel:
        elif ctx.voice.channel != ctx.author.voice.channel:
            await ctx.voice_client.move_to(voice_channel)
            vc = ctx.voice_client

        async with ctx.typing():
            player = await YTDLSource.from_url(
                url, loop=self.bot.loop, timestamp=timestamp
            )
            ctx.voice_client.play(
                player, after=lambda e: print(f"Player error: {e}") if e else None
            )

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

#             if len(playlist) == 0:
            async with ctx.typing():
                player = await YTDLSource.from_url(
                    url, loop=self.bot.loop, stream=True, timestamp=timestamp
                )
                ctx.voice_client.play(
                    player, after=lambda e: print("Player error: %s" % e) if e else None
                )
            await ctx.send("Now playing: {}".format(player.title))
#             else:
#                 playlist.append(timestamp)
#                 playlist.append(url)

    @commands.command(name="piss", aliases=["pissing"])
    async def piss(self, ctx):
        serverid = ctx.guild

        voice_channel = ctx.author.voice.channel
        if ctx.voice_client is None:
            vc = await voice_channel.connect()
#         elif not ctx.voice_channel.is_playing() and ctx.voice.channel != ctx.author.voice.channel:
        elif ctx.voice.channel != ctx.author.voice.channel:
            await ctx.voice_client.move_to(voice_channel)
            vc = ctx.voice_client

        if self.bot.playlists.get(serverid) is None:
            self.bot.playlists[serverid] = list()

        else:
            self.bot.playlists[serverid].append("Momentary bliss")
            print(self.bot.playlists[serverid])

#         if len(playlist) == 0:
        async with ctx.typing():
            player = await YTDLSource.from_url("Momentary bliss", loop=self.bot.loop, stream=True)
            ctx.voice_client.play(
                player, after=lambda e: print("Player error: %s" % e) if e else None
            )
        await ctx.send("Now playing: {}".format(player.title))
#         else:
#             playlist.append(0)
#             playlist.append("Momentary bliss")

    @commands.command(name="pause", help="Pauses the song")
    async def pause(self, ctx):
        if ctx.voice_client.is_playing():
            ctx.voice_client.pause()
            paused = True
            await ctx.message.channel.send("Paused!")
        else:
            await ctx.message.channel.send("The bot is not playing any music")

    @commands.command(name="resume", help="Resumes the song")
    async def resume(self, ctx):
        if ctx.voice_client.is_paused():
            ctx.voice_client.resume()
            paused = False
            await ctx.message.channel.send("Resumed!")
        else:
            await ctx.message.channel.send("No music has been paused")

#     @commands.command(name="remove", aliases=["r"], help="Remove an item from the queue")
#     async def remove(self, ctx, num):
#         if len(playlist) / 2 < num:
#             await ctx.message.channel.send("No queue item of that number, please try again")
#         else:
#             playlist.pop(num * 2)
#             playlist.pop(num * 2 - 1)

    @commands.command(name="queue", aliases=["q"], help="Displays the queue")
    async def queue(self, ctx):
        serverid = ctx.guild
        if self.bot.playlists.get(serverid) is None:
            await ctx.message.channel.send("The queue is empty!")
        else:
            await ctx.message.channel.send(self.bot.playlists.get(serverid))
#             response = ""
#             i = 1
#             for x in playlist:
#                 if x % 2 == 1:
#                     break
#                 response += "{} \t {} \n".format(i, playlist[x])
#             await ctx.message.channel.send(response)

    @commands.command(name="skip", help="Skips the current song")
    async def skip(self, ctx):
        if ctx.voice_client.is_playing():
            ctx.voice_client.pause()
            await ctx.message.channel.send("Skipped!")
        else:
            await ctx.message.channel.send("The bot is not playing any music")


def setup(bot):
    bot.add_cog(Song(bot))
