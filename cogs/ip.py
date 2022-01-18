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

    # Creates a task loop that runs every 60 seconds to check if the IP
    # has changed
    @tasks.loop(seconds=60)
    async def checkIP(self, message, old_IP):
        # Gets the IP
        result = subprocess.run(['curl', 'ifconfig.co'], stdout=subprocess.PIPE)
        IP = str(result).split(' ')

        # Strips other information
        IP = IP[3]
        IP = IP[9:-4]

        # Checks if IP has changed, and if so sends a message and updates
        # the old IP value
        if IP != old_IP:
            await message.channel.send("Your IP changed!  It is now {}".format(IP))
            old_IP = IP

    # Command to display IP
    @commands.command()
    async def sendIP(self,message):
        # Checks if it was requested in my own server
        if message.guild.id == 786732353098743930:
            # Gets the IP
            result = subprocess.run(['curl', 'ifconfig.co'], stdout=subprocess.PIPE)
            IP = str(result).split(' ')

            # Strips other stuff
            IP = IP[3]
            IP = IP[9:-4]

            # Only tries start the loop if it's not already running to prevent
            # issues
            if not self.checkIP.is_running():
                self.checkIP.start(message, IP)
            return await message.channel.send(IP)

def setup(bot):
    bot.add_cog(IP(bot))
