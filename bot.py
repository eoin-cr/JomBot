# bot.py
import os
import random
import time
import re
import discord
import requests
from dotenv import load_dotenv
from discord.ext import commands
from discord.ext.commands import has_permissions
from bs4 import BeautifulSoup
import cryptocompare
import json
from discord.utils import find

intents = discord.Intents.default()
intents.members = True



load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# client = discord.Client(intents=intents)
# prefix = "!"
bot = commands.Bot(command_prefix=("!","<:chigmn2:829382748631203901>"))

@bot.event
async def on_member_join(member):
    channel = client.get_channel(829349688197120052)
    invite_list = await member.guild.invites()
    # await channel.send("""Hello {} and welcome to the server!  A lot of people \
    # seem to join and then just never say anything so please don\'t do that thanks.  \
    # Anyway be sure to answer the questions in <#830565670805962822> and then check \
    # out <#830565732001644555> and <#830565778654887958> for more information!  \
    # Also when enabled I will delete every message containing sus, vented, etc.  \
    # So if your messages are getting removed, that might be why""".format(member.name))
    secret = client.get_channel(850459809324597288)
    # print(invite_list[2].uses)
    for i in range(0, len(invite_list)):
        # for x in invite_list:
        num_list = []
        # invite =
        # with is like your try .. finally block in this case
        with open('invites.txt', 'r') as file:
        # read a list of lines into data
            data = file.readlines()
        if invite_list[i].uses is not data[i]:
            await secret.send("{} was invited to the server by {}".format(member.name, invite_list[i].inviter))
            data[i] = invite_list[i].uses
            break
            # print(data)
        # with open('invites.txt', 'w') as file:
        #     file.write('\n'.join(data))

    invites_list = await member.guild.invites()
    list = []
    for i in range (0, len(invites_list)):
        # print(invites_list[i].uses)
        list.append(invites_list[i].uses)
    with open('invites.txt', 'w') as file:
        file.write('\n'.join([str(x) for x in list]))

@bot.event
async def on_message(message):

#     if message.author.id == 484444017489084416 and message.content.startswith("!"):
#         await message.channel.send("Yes")

    if message.content == "inv_txt":
        invites_list = await message.guild.invites()
        list = []
        for i in range (0, len(invites_list)):
            # print(invites_list[i].uses)
            list.append(invites_list[i].uses)
        # Array =  numpy.array(list)
        # file = open("test.txt", "w+")
        # content = str(Array)
        # file.write(content)
        # file.close()
        # return print("File closed")
        with open('test.txt', 'w') as file:
            file.write('\n'.join([str(x) for x in list]))
    await bot.process_commands(message)

@bot.command()
async def hello(ctx):
    hello = "Hello!"
    await ctx.send(hello)


# bot.load_extension("cogs.trading")
bot.load_extension("cogs.crypto")
bot.load_extension("cogs.pond")
# bot.load_extension("cogs.remove")
# bot.load_extension("cogs.join")
# bot.load_extension("cogs.binder_check")
# bot.load_extension("cogs.jokes")
bot.load_extension("cogs.ip")
# bot.load_extension("cogs.music")
bot.load_extension("cogs.song")
bot.load_extension("cogs.wordle")

bot.run(TOKEN)
