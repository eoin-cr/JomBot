# IP.py
import os
import asyncio
import time
import discord
from discord.ext import commands, tasks
import subprocess

class IP(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        print("IP initialised")

    @tasks.loop(seconds=60)
    async def checkIP(self, message, old_IP):
        result = subprocess.run(['curl', 'ifconfig.co'], stdout=subprocess.PIPE)
        IP = str(result).split(' ')
        IP = IP[3]
        IP = IP[9:-4]
        if IP != old_IP:
            await message.channel.send("Your IP changed!  It is now {}".format(IP))
            old_IP = IP

    @commands.command()
    async def sendIP(self,message):
        if message.guild.id == 786732353098743930:
            result = subprocess.run(['curl', 'ifconfig.co'], stdout=subprocess.PIPE)
            IP = str(result).split(' ')
            IP = IP[3]
            IP = IP[9:-4]
            self.checkIP.start(message, IP)
            return await message.channel.send(IP)

def setup(bot):
    bot.add_cog(IP(bot))
