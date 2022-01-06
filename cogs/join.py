#join.py
import os
import re
import discord
import requests
from dotenv import load_dotenv
from discord.ext import commands


# class Join(commands.Cog):
#     def __init__(self,bot):
#         self.bot = bot
#         print("Join initialised")
#
#     @commands.Cog.listener()
#     async def on_member_join(self,member):
#         print("Joined!")
#         channel = client.get_channel(829349688197120052)
#         invite_list = await member.guild.invites()
#         # print(invite_list)
#         # for i in invite_list:
#         #     print(i.inviter)
#         # general = find(lambda x: x.name == 'general',  guild.text_channels)
#         # print(general)
#         await channel.send("""Hello {} and welcome to the server!  A lot of people \
#         seem to join and then just never say anything so please don\'t do that thanks.  \
#         Anyway be sure to answer the questions in <#830565670805962822> and then check \
#         out <#830565732001644555> and <#830565778654887958> for more information!  \
#         Also when enabled I will delete every message containing sus, vented, etc.  \
#         So if your messages are getting removed, that might be why""".format(member.name))
#         secret = client.get_channel(850459809324597288)
#         # print(invite_list[2].uses)
#         for i in range(0, len(invite_list)):
#             # for x in invite_list:
#             num_list = []
#             # invite =
#             # with is like your try .. finally block in this case
#             with open('invites.txt', 'r') as file:
#             # read a list of lines into data
#                 data = file.readlines()
#             if invite_list[i].uses is not data[i]:
#                 await secret.send("{} was invited to the server by {}".format(member.name, invite_list[i].inviter))
#                 data[i] = invite_list[i].uses
#                 break
#                 # print(data)
#             # with open('invites.txt', 'w') as file:
#             #     file.write('\n'.join(data))
#
#         invites_list = await member.guild.invites()
#         list = []
#         for i in range (0, len(invites_list)):
#             # print(invites_list[i].uses)
#             list.append(invites_list[i].uses)
#         with open('invites.txt', 'w') as file:
#             file.write('\n'.join([str(x) for x in list]))

def setup(bot):
    bot.add_cog(Join(bot))
