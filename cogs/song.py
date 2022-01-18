import typing
import asyncio
import discord
import youtube_dl
from discord.ext import tasks, commands

# Suppress noise about console usage from errors
youtube_dl.utils.bug_reports_message = lambda: ""

# Sets some ytdl options
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

# Note on the pretty_playlist and playlist: The playlist is the one the bot uses
# to select the next song in the queue.  However, the pretty_playlist is
# displayed to the user.  The reason for this is as follows:
# Imagine we have song - abc and song - def.  Now the user wants to play
# song - def, however, song - abc is the first result in the yt search, then it
# will start playing that one instead.  So the user then specifies song - def
# so now the correct song is in the playlist.  Imagine now however, that the yt
# title of song - def is just song.  If we just use the title (what
# pretty_playlist displays) to search the song when the bot eventually gets
# to that place on the queue it will search for the title of the song, however,
# as the song title is just song, the first result will be song - abc.  Thereby
# playing the wrong song.  pretty_playlist is displayed to the user as it looks
# much nicer, and playlist is entirely used on the backend for searching and
# the like

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data
        self.title = data.get("title")
        self.url = data.get("url")

    # Sets up function to play yt videos
    @classmethod
    async def from_url(cls, url, *, loop=None, stream=True, timestamp=0):
        # moved the options from outside the class to inside the method.
        # this allows the use of variables in the options

        # Timestamp format allows use of seek functions and the like
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
#         self.audio_player_task.start(ctx.guild)
        print("Song initialised")

    def cog_unload(self):
        self.audio_player_task.cancel()

    # Task loop goes through the playlist playing the next song
    @tasks.loop(seconds=1.0)
    async def audio_player_task(self, guild, ctx):
        # Ensures it doesn't move onto the next track when it's already playing
        # music, or is paused, or if there's nothing in the playlist
        if not ctx.voice_client.is_playing() and not self.paused and len(self.playlist) > 0:
            async with ctx.typing():
                player = await YTDLSource.from_url(
                    self.playlist[0], loop=self.bot.loop, stream=True, timestamp=0
                )
                # Plays the next song
                ctx.voice_client.play(
                    player, after=lambda e: print("Player error: %s" % e) if e else None
                )

            await ctx.send("Now playing: {}".format(player.title))

            # Changes current to be the current song
            self.current = self.playlist[0]

            # Removes first item in the playlists
            self.playlist.pop(0)
            self.pretty_playlist.pop(0)

    @commands.command(name="join", aliases=["j"], help="Joins a voice channel")
    async def join(self, ctx):
        # Checks if user is in a vc
        if ctx.author.voice is None or ctx.author.voice.channel is None:
            return await ctx.send(
                "You need to be in a voice channel to use this command!"
            )

        voice_channel = ctx.author.voice.channel

        # Checks if the playlist task is running, if not it starts it
        if not self.audio_player_task.is_running():
            self.audio_player_task.start(ctx.guild, ctx)

        # Either moves or joins a new vc
        if ctx.voice_client is None:
            vc = await voice_channel.connect()
        else:
            await ctx.voice_client.move_to(voice_channel)
            vc = ctx.voice_client

    @commands.command(
        name="leave", aliases=["disconnect", "dc"], help="Leaves a voice channel"
    )
    async def leave(self, ctx):
        # Leaves the vc and stops the playlist task
        await ctx.voice_client.disconnect()
        self.audio_player_task.stop()

    @commands.command(name="play", aliases=["p"], help="Adds a song to the queue")
    async def play(self, ctx, timestamp: typing.Optional[int] = 0, *, url):

        voice_channel = ctx.author.voice.channel

        # If the bot isn't in a vc, join the one the user is in
        if ctx.voice_client is None:
            vc = await voice_channel.connect()
#         elif not ctx.voice_channel.is_playing() and ctx.voice.channel != ctx.author.voice.channel:
        # If it's not in the user's vc, move to it
        elif ctx.voice_client.channel != ctx.author.voice.channel:
            await ctx.voice_client.move_to(voice_channel)
            vc = ctx.voice_client

        # Starts the playlist task if it's not already started
        if not self.audio_player_task.is_running():
            self.audio_player_task.start(ctx.guild, ctx)

        # If there's stuff in the playlist or if it's already playing, add the
        # song to the playlist
        if len(self.playlist) > 0 or ctx.voice_client.is_playing():
            player = await YTDLSource.from_url(
                url
            )
            self.playlist.append(url)
            self.pretty_playlist.append(player.title)
            await ctx.send("{} has been added to the queue".format(player.title))

        # Otherwise, immediately start playing the song
        else:
            async with ctx.typing():
                player = await YTDLSource.from_url(
                    url, loop=self.bot.loop, timestamp=timestamp
                )
                ctx.voice_client.play(
                    player, after=lambda e: print(f"Player error: {e}") if e else None
                )

            self.current = url
            await ctx.send("Now playing: {}".format(player.title))

    @commands.command(name="piss", aliases=["pissing"])
    async def piss(self, ctx):
        # Same logic as the play function for the most part
        voice_channel = ctx.author.voice.channel
        if ctx.voice_client is None:
            vc = await voice_channel.connect()
#         elif not ctx.voice_channel.is_playing() and ctx.voice.channel != ctx.author.voice.channel:
        elif ctx.voice_client.channel != ctx.author.voice.channel:
            await ctx.voice_client.move_to(voice_channel)
            vc = ctx.voice_client

        if not self.audio_player_task.is_running():
            self.audio_player_task.start(ctx.guild, ctx)

        player = await YTDLSource.from_url(
            "Momentary bliss", loop=self.bot.loop, timestamp=0
        )
        if len(self.playlist) > 0 or ctx.voice_client.is_playing():
            self.playlist.append("Momentary bliss")
            self.pretty_playlist.append(player.title)
            await ctx.send("Momentary bliss has been added to the queue")
        else:
            async with ctx.typing():
                ctx.voice_client.play(
                    player, after=lambda e: print("Player error: %s" % e) if e else None
                )
            self.current = "Momentary bliss"
            await ctx.send("Now playing: {}".format(player.title))

    @commands.command(name="pause", help="Pauses the song")
    async def pause(self, ctx):
        if ctx.voice_client.is_playing():
            ctx.voice_client.pause()
            self.paused = True
            await ctx.message.channel.send("Paused!")
        else:
            await ctx.message.channel.send("The bot is not playing any music")

    @commands.command(name="resume", help="Resumes the song")
    async def resume(self, ctx):
        if ctx.voice_client.is_paused():
            ctx.voice_client.resume()
            self.paused = False
            await ctx.message.channel.send("Resumed!")
        else:
            await ctx.message.channel.send("No music has been self.paused")

    @commands.command(name="queue", aliases=["q"], help="Displays the queue")
    async def queue(self, ctx):
        if len(self.pretty_playlist) == 0:
            await ctx.message.channel.send("The queue is empty")
        else:
            response = ""
            i = 1
            for i, x in enumerate(self.pretty_playlist):
                response += f"{i+1:<5}{x}" + "\n"
            await ctx.message.channel.send(response)

    @commands.command(name="raw_queue", help="Displays the raw queue for debugging")
    async def raw_queue(self, ctx):
        if len(self.playlist) == 0:
            await ctx.message.channel.send("The queue is empty")
        else:
            response = ""
            i = 1
            for i, x in enumerate(self.playlist):
                response += f"{i+1:<5}{x}" + "\n"
#             for x in self.playlist:
#                 response += "{} \t {} \n".format(i, x)
#                 i += 1
            await ctx.message.channel.send(response)

    @commands.command(name="skip", help="Skips the current song")
    async def skip(self, ctx):
        if ctx.voice_client.is_playing():
            ctx.voice_client.pause()
            await ctx.message.channel.send("Skipped!")
        else:
            await ctx.message.channel.send("The bot is not playing any music")

    @commands.command(name="seek", help="Seeks (in seconds) to a certain part of the song")
    async def seek(self, ctx, timestamp):
        # If the bot is playing, pauses the music, and sets self.paused to true
        # so the playlist task doesn't start playing the next song
        if ctx.voice_client.is_playing():
            ctx.voice_client.pause()
            self.paused = True
        if self.current == "":
            await ctx.message.channel.send("No song is playing")

        # Then as whenever (in the original code, I've fixed it for just adding
        # stuff) a song is paused, you can start playing another one, it now
        # starts playing the same song, but this time it passes the timestamp
        # variable, so it will essentially resume the song at the desired time.
        else:
            async with ctx.typing():
                player = await YTDLSource.from_url(
                    self.current, loop=self.bot.loop, stream=True, timestamp=timestamp
                )
                ctx.voice_client.play(
                    player, after=lambda e: print(f"Player error: {e}") if e else None
                )
            self.paused = False
            await ctx.send("Seeked to {}s".format(timestamp))

    @commands.command(name="current", help="Displays the currently playing song")
    async def current(self, ctx):
        if self.current is not None and ctx.voice_client.is_playing():
            player = await YTDLSource.from_url(
                current
            )
            await ctx.send("Currently playing: {}".format(player.title))
        else:
            await ctx.send("No music is currently playing.")

    @commands.command(name="remove", aliases=["r", "rm", "del", "delete"], help="Removes an item from the queue")
    async def remove(self, ctx, num):

        if int(num) > len(self.playlist):
            await ctx.send("No item in queue with this value")
        else:
            await ctx.send("Removed {} from the queue".format(self.pretty_playlist[int(num) - 1]))
            self.playlist.pop(int(num) - 1)
            self.pretty_playlist.pop(int(num) - 1)

    @commands.command(name="move", aliases=["m", "mv"], help="Moves an item in the queue")
    async def move(self, ctx, old, new):

        if int(old) > len(self.playlist):
            await ctx.send("No item in queue with this value")
        elif int(new) > len(self.playlist):
            await ctx.send("Please enter a number within the bounds of the queue")
        else:
            self.playlist.insert(int(new) - 1, self.playlist.pop(int(old) - 1))
            self.pretty_playlist.insert(int(new) - 1, self.pretty_playlist.pop(int(old) - 1))
            await ctx.send("Moved {} to number {} in the queue".format(self.pretty_playlist[int(new) - 1], new))


def setup(bot):
    bot.add_cog(Song(bot))
