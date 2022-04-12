import typing
import asyncio
import discord
import youtube_dl
from discord.ext import tasks, commands
import cogs.pond as pond
import bot as main
from collections import namedtuple

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

# How this cog works: Basically what happens is we have a `servers` array containing
# namedTuples (a form of structure).  Each namedTuple stores the guild id,
# pretty playlist, raw playlist, current song playing, whether the song has
# been paused, and ctx.  This means that each server that calls JomBot for
# music will have its own playlist, rather than having one shared playlist
# between all servers using JomBot.  Then we have a task loop which runs once
# per second. This loop goes through every element of the servers array and
# checks if a song is currently playing, and if not it plays the next item
# in the queue.  This is also the reason we need the ctx item in the tuple,
# as this task loop is simply running every second, rather than being directly
# called, and it accounts for every server, it needs to know where to send
# messages stating that it's playing the next song and the like.

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


async def queue_func(ctx, playlist):
    if len(playlist) == 0:
        embed = main.embed_func(ctx, "Playlist", "The queue is empty", discord.Color.red())
        await ctx.message.channel.send(embed=embed)
        # await ctx.message.channel.send("The queue is empty")
    else:
        response = ""
        i = 1
        for i, x in enumerate(playlist):
            response += f"{i + 1:<5}{x}" + "\n"
        # await ctx.message.channel.send(response)
        embed = main.embed_func(ctx, "Playlist", response)
        await ctx.message.channel.send(embed=embed)


class Song(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.Queue = namedtuple('Queue', ['id', 'pretty', 'raw', 'current', 'paused', 'ctx'])
        self.servers = []
        print("Song initialised")

    # Returns the index of the of the array element in the servers array which contains
    # the id that matches the guild id of a message
    def return_index(self, guild_id, ctx):
        for i in range(len(self.servers)):
            # print(f'servers[{i}].id = {self.servers[i].id} guild_id: {guild_id}')
            if self.servers[i].id == guild_id:
                # if a server with the needed id is found, then replace the ctx with
                # the ctx of the last message, and return the index of that element
                self.servers[i] = self.servers[i]._replace(ctx=ctx)
                return i

        # print(len(self.servers))
        # otherwise, if there's no element for that server, create one and return the
        # new length of the servers array - 1
        self.servers.append(
            self.Queue(id=guild_id, pretty=[], raw=[], current=None, paused=False, ctx=ctx))
        return len(self.servers) - 1

    async def join_func(self, ctx):
        voice_channel = ctx.author.voice.channel
        # If the bot isn't in a vc, join the one the user is in
        if ctx.voice_client is None:
            await voice_channel.connect()
        #         elif not ctx.voice_channel.is_playing() and ctx.voice.channel != ctx.author.voice.channel:
        # If it's not in the user's vc, move to it
        elif ctx.voice_client.channel != ctx.author.voice.channel:
            await ctx.voice_client.move_to(voice_channel)

        # Starts the playlist task if it's not already started
        if not self.audio_player_task.is_running():
            self.audio_player_task.start()

    # Task loop goes through the playlist playing the next song
    @tasks.loop(seconds=1.0)
    # async def audio_player_task(self, guild, ctx):
    async def audio_player_task(self):
        # for each server "structure" in the array, check if music is currently playing,
        # and if not, then play the next song in the queue
        for i in range(len(self.servers)):
            guild_id = self.servers[i].id
            ctx = self.servers[i].ctx
            # Ensures it doesn't move onto the next track when it's already playing
            # music, or is paused, or if there's nothing in the playlist
            index = self.return_index(guild_id, ctx)
            # print(f"idx: {index}")
            # print(f"servers {self.servers}")
            # print(f"ind paused? {self.servers[index].paused}")
            if not ctx.voice_client.is_playing() and not self.servers[index].paused \
                    and self.servers[index].raw is not None and len(self.servers[index].raw) > 0:
                async with ctx.typing():
                    player = await YTDLSource.from_url(
                        self.servers[index].raw[0], loop=self.bot.loop, stream=True, timestamp=0
                    )
                    # Plays the next song
                    ctx.voice_client.play(
                        player, after=lambda e: print("Player error: %s" % e) if e else None
                    )

                # await ctx.send("Now playing: {}".format(player.title))
                embed = main.embed_func(ctx, "Play", f"Now playing: {player.title}")
                await ctx.send(embed=embed)

                # Changes current to be the current song
                # self.current = self.playlist[0]
                self.servers[index] = self.servers[index]._replace(current=
                                                                   self.servers[index].pretty[0])

                # Removes first item in the playlists
                # self.playlist.pop(0)
                self.servers[index].raw.pop(0)
                # self.pretty_playlist.pop(0)
                self.servers[index].pretty.pop(0)

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
            self.audio_player_task.start()

        # Either moves or joins a new vc
        if ctx.voice_client is None:
            await voice_channel.connect()
        else:
            await ctx.voice_client.move_to(voice_channel)

        embed = main.embed_func(ctx, "Join", "I have joined your voice channel!")
        await ctx.send(embed=embed)

    @commands.command(
        name="leave", aliases=["disconnect", "dc"], help="Leaves a voice channel"
    )
    async def leave(self, ctx):
        # Leaves the vc and stops the playlist task
        await ctx.voice_client.disconnect()
        self.audio_player_task.stop()

        embed = main.embed_func(ctx, "Disconnect", "I have left your voice channel!", discord.Color.purple())
        await ctx.send(embed=embed)

    @commands.command(name="play", aliases=["p"], help="Adds a song to the queue")
    async def play(self, ctx, timestamp: typing.Optional[int] = 0, *, url):
        await self.join_func(ctx)
        # If there's stuff in the playlist or if it's already playing, add the
        # song to the playlist
        index = self.return_index(ctx.guild.id, ctx)
        if len(self.servers[index].raw) > 0 or ctx.voice_client.is_playing():
            player = await YTDLSource.from_url(
                url
            )
            # self.playlist.append(url)
            self.servers[index].raw.append(url)
            # self.pretty_playlist.append(player.title)
            self.servers[index].pretty.append(player.title)
            embed = main.embed_func(ctx, "Play", f"{player.title} has been added to the queue")
            await ctx.send(embed=embed)

        # Otherwise, immediately start playing the song
        else:
            async with ctx.typing():
                player = await YTDLSource.from_url(
                    url, loop=self.bot.loop, timestamp=timestamp
                )
                ctx.voice_client.play(
                    player, after=lambda e: print(f"Player error: {e}") if e else None
                )

            # self.current = url
            self.servers[index] = self.servers[index]._replace(current=url)
            embed = main.embed_func(ctx, "Play", f"Now playing: {player.title}")
            await ctx.send(embed=embed)

    @commands.command(name="piss", aliases=["pissing"], hidden=True)
    @pond.pond_check()
    async def piss(self, ctx):
        await self.join_func(ctx)

        index = self.return_index(ctx.guild.id, ctx)
        player = await YTDLSource.from_url(
            "Momentary bliss", loop=self.bot.loop, timestamp=0
        )
        if len(self.servers[index].raw) > 0 or ctx.voice_client.is_playing():
            self.servers[index].raw.append("Momentary bliss")
            self.servers[index].pretty.append(player.title)

            embed = main.embed_func(ctx, "Play", f"Momentary bliss has been added to the queue")
            await ctx.send(embed=embed)
        else:
            async with ctx.typing():
                ctx.voice_client.play(
                    player, after=lambda e: print("Player error: %s" % e) if e else None
                )
            # self.current = "Momentary bliss"
            self.servers[index] = self.servers[index]._replace(current="Momentary Bliss")
            embed = main.embed_func(ctx, "Play", f"Now playing: {player.title}")
            await ctx.send(embed=embed)

    @commands.command(name="pause", help="Pauses the song")
    async def pause(self, ctx):
        index = self.return_index(ctx.guild.id, ctx)
        if ctx.voice_client.is_playing():
            ctx.voice_client.pause()
            self.servers[index] = self.servers[index]._replace(paused=True)
            # self.servers[index].paused = True
            embed = main.embed_func(ctx, "Pause", "The song has been paused!")
            await ctx.send(embed=embed)
        else:
            embed = main.embed_func(ctx, "Pause", "The bot is not playing any music!", discord.Color.red())
            await ctx.send(embed=embed)

    @commands.command(name="resume", help="Resumes the song")
    async def resume(self, ctx):
        index = self.return_index(ctx.guild.id, ctx)
        if ctx.voice_client.is_paused():
            ctx.voice_client.resume()
            self.servers[index] = self.servers[index]._replace(paused=False)
            embed = main.embed_func(ctx, "Resume", "The song has been resumed!")
            await ctx.send(embed=embed)
        else:
            embed = main.embed_func(ctx, "Resume", "No music has been paused!", discord.Color.red())
            await ctx.send(embed=embed)

    @commands.command(name="queue", aliases=["q"], help="Displays the queue")
    async def queue(self, ctx):
        index = self.return_index(ctx.guild.id, ctx)
        await queue_func(ctx, self.servers[index].pretty)

    @commands.command(name="raw_queue", help="Displays the raw queue for debugging")
    async def raw_queue(self, ctx):
        index = self.return_index(ctx.guild.id, ctx)
        await queue_func(ctx, self.servers[index].raw)

    @commands.command(name="skip", help="Skips the current song")
    async def skip(self, ctx):
        if ctx.voice_client.is_playing():
            ctx.voice_client.pause()
            embed = main.embed_func(ctx, "Skip", "The song has been skipped!")
            await ctx.send(embed=embed)
        else:
            embed = main.embed_func(ctx, "Skip", "No music is currently playing!", discord.Color.red())
            await ctx.send(embed=embed)

    @commands.command(name="seek", help="Seeks (in seconds) to a certain part of the song")
    async def seek(self, ctx, timestamp):
        index = self.return_index(ctx.guild.id, ctx)
        # If the bot is playing, pauses the music, and sets self.paused to true
        # so the playlist task doesn't start playing the next song
        if ctx.voice_client.is_playing():
            ctx.voice_client.pause()
            self.servers[index].paused = True
        if self.servers[index].current is None:
            embed = main.embed_func(ctx, "Seek", "No music is currently playing!", discord.Color.red())
            await ctx.send(embed=embed)

        # Then as whenever (in the original code, I've fixed it for just adding
        # stuff) a song is paused, you can start playing another one, it now
        # starts playing the same song, but this time it passes the timestamp
        # variable, so it will essentially resume the song at the desired time.
        else:
            async with ctx.typing():
                player = await YTDLSource.from_url(
                    self.servers[index].current, loop=self.bot.loop, stream=True, timestamp=timestamp
                )
                ctx.voice_client.play(
                    player, after=lambda e: print(f"Player error: {e}") if e else None
                )
            self.servers[index].paused = False
            embed = main.embed_func(ctx, "Seek", f"Seeked to {timestamp}s")
            await ctx.send(embed=embed)

    @commands.command(name="current", help="Displays the currently playing song")
    async def current(self, ctx):
        index = self.return_index(ctx.guild.id, ctx)
        if self.servers[index].current is not None and ctx.voice_client.is_playing():
            player = await YTDLSource.from_url(
                self.servers[index].current
            )
            embed = main.embed_func(ctx, "Current", f"Currently playing: {player.title}")
            # print(player.url)
            await ctx.send(embed=embed)
        else:
            embed = main.embed_func(ctx, "Current", "No music is currently playing!", discord.Color.red())
            await ctx.send(embed=embed)

    @commands.command(name="remove", aliases=["r", "rm", "del", "delete"], help="Removes an item from the queue")
    async def remove(self, ctx, num):
        index = self.return_index(ctx.guild.id, ctx)
        if int(num) > len(self.servers[index].raw):
            embed = main.embed_func(ctx, "Remove", "There is no item in the queue "
                                                   "with this value!", discord.Color.red())
            await ctx.send(embed=embed)
        else:
            embed = main.embed_func(ctx, "Remove", "Removed "
                                                   "{} from the queue".format(self.servers[index].pretty[int(num) - 1]))
            await ctx.send(embed=embed)
            self.servers[index].raw.pop(int(num) - 1)
            self.servers[index].pretty.pop(int(num) - 1)

    @commands.command(name="move", aliases=["m", "mv"], help="Moves an item in the queue")
    async def move(self, ctx, old, new):
        index = self.return_index(ctx.guild.id, ctx)
        if int(old) > len(self.servers[index].raw):
            embed = main.embed_func(ctx, "Remove", "There is no item in"
                                                   " the queue with this value!", discord.Color.red())
            await ctx.send(embed=embed)
        elif int(new) > len(self.servers[index].raw):
            embed = main.embed_func(ctx, "Move", "Please enter a new queue position within the bounds"
                                                 " of the queue!", discord.Color.red())
            await ctx.send(embed=embed)
        else:
            self.servers[index].raw.insert(int(new) - 1, self.servers[index].raw.pop(int(old) - 1))
            self.servers[index].pretty.insert(int(new) - 1, self.servers[index].pretty.pop(int(old) - 1))
            embed = main.embed_func(ctx, "Move", "Moved {} to number {} in the "
                                                 "queue".format(self.servers[index].pretty[int(new) - 1], new))
            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Song(bot))
