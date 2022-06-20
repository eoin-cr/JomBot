# bot.py
import os
import discord
from dotenv import load_dotenv
from discord.ext import commands
import json

intents = discord.Intents.default()
intents.members = True

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GOOGLE_KEY = os.getenv('GOOGLE_API')
GOOGLE_ID = os.getenv('GOOGLE_ID')

default_prefixes = ["!", '<:chigmn2:829382748631203901> ', "<@967441591616823357> "]


# just a function to allow per-server prefixes
async def determine_prefix(bot, message):
    guild = message.guild
    # if the message was sent in a guild, continue
    if guild:
        # print("two")
        # creates the directory and file to store the prefixes if it doesn't
        # already exist
        if not os.path.exists('data_files'):
            os.makedirs('data_files')

        if not os.path.exists(f'data_files/prefixes.json'):
            os.mknod(f'data_files/prefixes.json')

            with open(f"data_files/prefixes.json", "w") as f:
                main = {}
                json.dump(main, f)
                # print("defaults")

                # if the file doesn't exist, it's impossible for there to be
                # any non-default prefixes, so just return the default ones
                return default_prefixes

        # Open the prefixes file and read the data to `main`
        with open(f"data_files/prefixes.json") as f:
            main = json.load(f)
            # print(f"main: {main}")
            # print(f"id: {guild.id}")
            # checks if there's an entry for this guild in the data
            if f"{guild.id}" in main:
                # if there is, set the prefix for that server's custom prefix
                prefix = main[f"{guild.id}"]["prefix"]
                if prefix == "":
                    return default_prefixes

                # print("yes")
                # just makes sure that pinging the bot in place of a prefix
                # works, even when a custom prefix is used
                prefix_list = [prefix, default_prefixes[2]]
                return prefix_list

            # print("nope")

            # otherwise if there is no entry for that server, just return
            # the default prefixes
            return default_prefixes

    # if a message wasn't sent in a guild, simply return the default prefixes
    else:
        # print("else")
        return default_prefixes


# The prefix is either ! or a little chicken emoji.  How fun :)
# You can also simply mention JomBot in order to run a command.  This is
# helpful in case you forget what the prefix is
bot = commands.Bot(command_prefix=determine_prefix, intents=intents)


def embed_func(ctx, title=None, text=None, colour=discord.Color.blue()):
    embed = discord.Embed(color=colour)
    embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
    if title is not None and text is not None:
        embed.add_field(name=title, value=text, inline=False)
    return embed


# Just a quick command to see how they work.  Also a good checker to see if
# the bot is online

@bot.command()
async def hello(ctx):
    hi = "Hello!"
    await ctx.send(hi)


# loads certain cogs stored in the cogs directory
# old
# bot.load_extension("cogs.remove")
# bot.load_extension("cogs.join")
# bot.load_extension("cogs.binder_check")
# bot.load_extension("cogs.jokes")
# bot.load_extension("cogs.embed_test")
# bot.load_extension("cogs.test")

# curr
# bot.load_extension("cogs.error")
# bot.load_extension("cogs.crypto")
# bot.load_extension("cogs.pond")
# bot.load_extension("cogs.ip")
# bot.load_extension("cogs.song")
# bot.load_extension("cogs.wordle")
# bot.load_extension("cogs.time")
# bot.load_extension("cogs.netsoc")
# bot.load_extension("cogs.hh")
# # bot.load_extension("cogs.translate")
# bot.load_extension("cogs.control")
# bot.load_extension("cogs.images")
# bot.load_extension("cogs.sentiment")
bot.load_extension("cogs.alex")

bot.run(TOKEN)
