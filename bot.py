# bot.py
import os
import discord
from dotenv import load_dotenv
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GOOGLE_KEY = os.getenv('GOOGLE_API')
GOOGLE_ID = os.getenv('GOOGLE_ID')

# The prefix is either ! or a little chicken emoji.  How fun :)
# You can also simply mention JomBot in order to run a command.  This is
# helpful in case you forget what the prefix is
bot = commands.Bot(command_prefix=["!", '<:chigmn2:829382748631203901> ', "<@820065836139675668> "],
                   intents=intents)


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


# Loads certain cogs stored in the cogs directory
bot.load_extension("cogs.crypto")
bot.load_extension("cogs.pond")
# bot.load_extension("cogs.remove")
# bot.load_extension("cogs.join")
# bot.load_extension("cogs.binder_check")
# bot.load_extension("cogs.jokes")
bot.load_extension("cogs.ip")
bot.load_extension("cogs.song")
bot.load_extension("cogs.wordle")
bot.load_extension("cogs.time")
# bot.load_extension("cogs.error")
# bot.load_extension("cogs.embed_test")
bot.load_extension("cogs.netsoc")
bot.load_extension("cogs.hh")
# bot.load_extension("cogs.test")
bot.load_extension("cogs.translate")

# Runs the bot using a .env stored bot token
bot.run(TOKEN)
