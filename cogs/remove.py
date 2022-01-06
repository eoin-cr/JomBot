# remove.py
import os
import re
import discord
import requests
from dotenv import load_dotenv
from discord.ext import commands
import json
from discord.utils import find


class Remove(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        print("1984 initialised")

    @commands.command(name='1984')
    async def nineteen(self, message, arg, *arg2):
            # async def 1984(self,message):
    # if message.content.startswith("!1984") and message.author.guild_permissions.manage_guild and message.guild.id is not None:
        if message.author.guild_permissions.manage_guild and message.guild.id is not None:
            # content = message.content.split(' ')
            # variants = str(message.content).strip(' ').split('-')
            # print(len(variants))
            server = message.guild.id
            start_response = ""
            server = message.guild.id
            if not os.path.exists(f"servers/{server}.json"):
                with open(f"servers/{server}.json", "w") as f:
                    json.dump({}, f)
            with open(f"servers/{server}.json", "r") as f:
                server_data = json.load(f)
            if arg == "start":
                if arg2 == "c":
                    start_response = "(But only in this channel)"
                    server_data[server] = True
                elif arg2 == "ow":
                    start_response = "And other presets have been overwritten."
                    for channel in server_data.keys():
#                         print(channel)
                      # if value != True:
                        server_data[channel] = True
                else:
                    server_data["SBanned"] = True
                await message.channel.send("1984 time.  {}".format(start_response))
            elif arg == "stop":
                if arg2 == "c":
                    start_response = "(But only in this channel)"
                    server_data[server] = False
                elif arg2 == "ow":
                    start_response = "And other presets have been overwritten."
                    for channel in server_data.keys():
                      # if value != True:
                      server_data[channel] = False
                else:
                    server_data["SBanned"] = False
                await message.channel.send("Amogus time.  {}".format(start_response))
                # print(start_response)
            with open(f"servers/{server}.json", 'w') as f:
                return json.dump(server_data, f)

    @commands.Cog.listener()
    async def on_message(self,message):
        comment = message.content.lower()
        com = comment.strip().replace("*", "")
#         print(com)
        banned_words = ["sus","vented","amongus","amogus","imposter","impostor"]
        jesus = "jesus"
        sushi = "sushi"
        for word in banned_words:
            if message.guild is not None:
                server = message.guild.id
                channel  = str(message.channel.id)
                if not os.path.exists(f"servers/{server}.json"):
                    with open(f"servers/{server}.json", "w") as f:
                        json.dump({}, f)
                with open(f"servers/{server}.json", "r") as f:
                    server_data = json.load(f)
                # print(server_data[channel])
                if server_data.get(channel) is not None and server_data[channel] == False:
#                     print(server_data.get(channel))
#                     print(server_data[channel])
#                     print("Break 1")
                    break
                if server_data["SBanned"] and word in com:
                    # if message.author.id != 484444017489084416 or jesus not in com or sushi not in com:
                    if message.author.id == 484444017489084416 or jesus in com or sushi in com:
#                         print("Break 2")
                        break
                    # elif jesus in com or sushi in com:
                    #     break
                    #
                    await message.delete()

def setup(bot):
    bot.add_cog(Remove(bot))
