# wordle.py
import time
import discord
from discord.ext import commands, tasks
import time
from datetime import timedelta
from numpy import loadtxt
import random

class Wordle(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        self.loops = 0
        self.started = False
        print("Wordle initialised")

    # This task loop acts as a timer
    @tasks.loop(seconds=60)
#     @tasks.loop(seconds=2)
    async def timer(self, ctx):
        self.loops += 1
        # Here loops are the same as minutes
        if self.loops == 4:
            await ctx.send("You only have one minute to make a guess before the game stops.  Use !time to extend this time")
        elif self.loops == 5:
            await ctx.send("Timer ran out, game stopped.")
            # Changes game start and resets time and stops timer
            self.started = False
            self.loops = 0
            self.timer.stop()

    @commands.command(name="wordle", help="!wordle start to begin")
    async def wordle(self, ctx, guess):
        # Checks if a game has already started
        if self.started:
            # Checks to make sure the person who started the game is the one
            # that's trying to guess
            if ctx.message.author == self.user:
                exists = False
                # Makes sure the guess is only 5 letters long
                if len(guess) != 5:
                    await ctx.send("The word must be 5 letters long!")

                # Checks if the guess matches the selected word
                elif guess == self.word:
                    self.message = self.message + "🟩 🟩 🟩 🟩 🟩 \n You win!"
                    await ctx.send(self.message)

                    # Changes game state and stops timer
                    self.started = False
                    self.timer.stop()

                else:
                    # Searches through the words list to check if the guess
                    # is in it
                    for word in self.words:
                        if guess == word:
                            exists = True
                            break
                    if not exists:
                        await ctx.send("That is not a valid word!")
                    else:
                        message = ""

                        # Checks which letters of the guess are in the word
                        # and whether they're in the right position
                        for i in range(5):
                            result = self.word.find(guess[i])
                            if result >= 0:
                                if result == i:
                                    message += "🟩"
                                else:
                                    message += "🟨"
                            else:
                                message += "⬛"
                        self.message = self.message + message + "\n"
                        await ctx.send(self.message)

                        # Adds to the number of guesses and checks whether the
                        # user has ran out of guesses
                        self.guesses += 1
                        if self.guesses >= 6:
                            await ctx.send("Game over - You have run out of guesses!  The word was {}".format(self.word))

                            # Changes game state and stops timer
                            self.started = False
                            self.timer.stop()

            # If the wrong user is trying to play, ignores their guess
            else:
                await ctx.send("Hey!  Wait your turn <:point:829423251163578398>")

        # If the game hasn't started and the user says start, start the game
        elif guess == "start":
            await ctx.send("Game started!  Use !wordle [guess] to play")

            # Checks if the timer is already running to avoid errors when
            # attempting to start a running task
            if self.timer.is_running():
                self.timer.restart(ctx)
            else:
                self.timer.start(ctx)

            # Changes game state, and notes who is playing
            self.started = True
            self.user = ctx.message.author

            # Opens word list and selects a word
            text_file = open("wiki-100k.txt", "r")
            self.words = text_file.read()
            self.words = self.words.split('\n')
            index = random.randint(0,3301)
            self.word = self.words[index]
            self.message = ""
            self.guesses = 0

    @commands.command(name="time", help="Extends your wordle time")
    async def time(self, ctx):
        # Checks if the person requesting more time is the player
        if ctx.message.author == self.user:
            self.loops = 0
            self.timer.restart(ctx)
            await ctx.send("Time extended")
        else:
            await ctx.send("You cannot extend someone else's time!")

    @commands.command(name="quit", help="Stops your wordle game")
    async def quit(self, ctx):
        # Checks if the person trying to quit is the player
        if ctx.message.author == self.user:
            # Resets time, stops timer, changes game state
            self.loops = 0
            self.timer.stop()
            self.started = False
            await ctx.send("Stopped game")
        else:
            await ctx.send("You cannot stop someone elses game!")


def setup(bot):
    bot.add_cog(Wordle(bot))
