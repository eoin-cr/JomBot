# bot.py
import os
import discord
from dotenv import load_dotenv
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# The prefix is either ! or a little chicken emoji.  How fun :)
bot = commands.Bot(command_prefix=["!", '<:chigmn2:829382748631203901> '])


# Code that checked who sent an invite link whenever someone new joins
# @bot.event
# async def on_member_join(member):
#     # This code automatically invites someone to the server.  It was made
#     # redundant with the introduction of requiring filling out introduction qs
#     # await channel.send("""Hello {} and welcome to the server!  A lot of people \
#     # seem to join and then just never say anything so please don\'t do that thanks.  \
#     # Anyway be sure to answer the questions in <#830565670805962822> and then check \
#     # out <#830565732001644555> and <#830565778654887958> for more information!  \
#     # Also when enabled I will delete every message containing sus, vented, etc.  \
#     # So if your messages are getting removed, that might be why""".format(member.name))
#
#     # Gets general channel invites
#     channel = client.get_channel(829349688197120052)
#     invite_list = await member.guild.invites()
#
#     secret = client.get_channel(850459809324597288)
#     # print(invite_list[2].uses)
#     for i in range(0, len(invite_list)):
#         # for x in invite_list:
#         num_list = []
#         # invite =
#         # with is like your try .. finally block in this case
#         with open('invites.txt', 'r') as file:
#         # read a list of lines into data
#             data = file.readlines()
#
#         # checks if a new invite has been made, and sends message to the secret
#         # channel
#         if invite_list[i].uses is not data[i]:
#             await secret.send("{} was invited to the server by {}".format(member.name, invite_list[i].inviter))
#             data[i] = invite_list[i].uses
#             break
#
#     # updates invites list
#     invites_list = await member.guild.invites()
#     list = []
#     for i in range (0, len(invites_list)):
#         # print(invites_list[i].uses)
#         list.append(invites_list[i].uses)
#     with open('invites.txt', 'w') as file:
#         file.write('\n'.join([str(x) for x in list]))

# @bot.event
# async def on_message(message):

# Legacy code for debugging invites checker
#     if message.content == "inv_txt":
#         invites_list = await message.guild.invites()
#         list = []
#         for i in range (0, len(invites_list)):
#             # print(invites_list[i].uses)
#             list.append(invites_list[i].uses)
#         # Array =  numpy.array(list)
#         # file = open("test.txt", "w+")
#         # content = str(Array)
#         # file.write(content)
#         # file.close()
#         # return print("File closed")
#         with open('test.txt', 'w') as file:
#             file.write('\n'.join([str(x) for x in list]))
#     await bot.process_commands(message)

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
bot.load_extension("cogs.error")

# Runs the bot using a .env stored bot token
bot.run(TOKEN)
