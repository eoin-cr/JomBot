# wordle.py
import time
import discord
from discord.ext import commands, tasks
import time
from datetime import timedelta

class Wordle(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        self.loops = 0
        print("Wordle initialised")

#     @tasks.loop(seconds=60)
    @tasks.loop(seconds=2)
    async def timer(self, ctx):
        self.loops += 1
        if self.loops == 4:
            await ctx.send("You only have one minute to make a guess before the game stops.  Use !time to extend this time")
        elif self.loops == 5:
            await ctx.send("Timer ran out, game stopped.")
            started = False
            self.loops = 0
            self.timer.stop()

    @commands.command(name="wordle", help="!wordle start to begin")
    async def wordle(self, ctx, guess):
        if started:
            if ctx.message.author == user:
                print("beep") # word checking logic
            else:
                ctx.send("Hey!  Wait your turn <:point:829423251163578398>")
        elif guess == "start":
            await ctx.send("Game started!  Use !wordle [guess] to play")
            timer()
            started = True
            user = ctx.message.author
#         else:
#             await ctx.send("Invalid command.

    @commands.command()
    async def time(self, ctx):
        self.loops = 0
        self.timer.restart(ctx)

    @commands.command()
    async def time_test(self, ctx):
        await ctx.send("Started")
        self.loops = 0
        if self.timer.is_running():
            self.timer.restart(ctx)
        else:
            self.timer.start(ctx)


def setup(bot):
    bot.add_cog(Wordle(bot))
