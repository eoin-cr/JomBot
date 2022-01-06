# IP.py
import os
import asyncio
import time
import discord
from discord.ext import commands
from dotenv import load_dotenv
import subprocess
import time
from timeloop import Timeloop
from datetime import timedelta

class IP(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        print("IP initialised")

    @commands.command()
    async def sendIP(self,message):
#         print("hello")
#         print(message.guild.id)
        if message.guild.id == 786732353098743930:
#             print("IP sending")
            result = subprocess.run(['curl', 'ifconfig.co'], stdout=subprocess.PIPE)
            IP = str(result).split(' ')
            IP3 = IP[3]
            IP3 = IP3[9:-4]
            return await message.channel.send(IP3)
            
#     tl = Timeloop()

#     @tl.job(interval=timedelta(seconds=3600)
#     async def ip_check():
#         result = subprocess.run(['curl', 'ifconfig.co'], stdout=subprocess.PIPE)
#         IP = str(result).split(' ')
#         IP3 = IP[3]
#         IP3 = IP3[9:-4]
            
def setup(bot):
    bot.add_cog(IP(bot))
       
       
