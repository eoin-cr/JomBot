# IP.py
from discord.ext import commands, tasks
import subprocess


class IP(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print("IP initialised")
        self.old_ip = ""

    # Creates a task loop that runs every 60 seconds to check if the IP
    # has changed
    @tasks.loop(seconds=60)
    async def check_ip(self, message):
        # Gets the IP
        result = subprocess.run(['curl', 'ifconfig.co'], stdout=subprocess.PIPE)
        ip_address = str(result).split(' ')

        # Strips other information
        ip_address = ip_address[3]
        ip_address = ip_address[9:-4]

        # Checks if IP has changed, and if so sends a message and updates
        # the old IP value
        if ip_address != self.old_ip:
            await message.channel.send(f'Your IP changed!  It is now {ip_address}')
            self.old_ip = ip_address

    # Command to display IP
    @commands.command()
    async def send_ip(self, message):
        # Checks if it was requested in my own server
        if message.guild.id == 786732353098743930:
            # Gets the IP
            result = subprocess.run(['curl', 'ifconfig.co'], stdout=subprocess.PIPE)
            ip_address = str(result).split(' ')

            # Strips other stuff
            ip_address = ip_address[3]
            ip_address = ip_address[9:-4]

            # Only tries start the loop if it's not already running to prevent
            # issues
            self.old_ip = ip_address
            if not self.check_ip.is_running():
                self.check_ip.start(message)
            return await message.channel.send(ip_address)


def setup(bot):
    bot.add_cog(IP(bot))
