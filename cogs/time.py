# time.py
import os
import discord
from discord.ext import commands
from numpy import loadtxt
from datetime import datetime

class Time(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        print("Time initialised")

    @commands.command(name="time", help="Displays current time in certain timezones")
    async def time(self,message,area):
        now = datetime.now()
        area = area.lower()
        if area == "us" or area == "america":
            hour  = int(now.strftime("%H")) - 8
            if hour < 0:
                hour += 24
            time = "" + str(hour) + ":" + str(now.strftime("%M:%S"))
            await message.channel.send(time)

        elif area == "uk" or area == "england" or area == "ireland":
            time = str(now.strftime("%H:%M:%S"))
            await message.channel.send(time)

        elif area == "serbia":
            hour = int(now.strftime("%H")) + 1
            if hour > 24:
                hour -= 24
            time = "" + str(hour) + str(now.strftime(":%M:%S"))
            await message.channel.send(time)

        elif area == "canada":
            hour = int(now.strftime("%H")) - 5
            if hour < 0:
                hour += 24
            time = "" + str(hour) + str(now.strftime(":%M:%S"))
            await message.channel.send(time)

        else:
#             print(area)
            area = int(area.strip('@,<>,!,()'))
#             print(area)
            with open('timezones.txt') as f:
#                 data = f.read()

#                 print(f'data: {data}')
#                 print(f'data1: {data[1]}')
                for line in f:
                    print(f'line: {line}')
                    line = line.split(" ")
                    print(f'line0: {line[0]}')
                    print(f'area: {area}')
                    if line[0] == str(area):
                        print("Entering!")
                        hour = int(now.strftime("%H")) + int(line[1])
                        if hour > 24:
                            hour -= 24
                        elif hour < 0:
                            hour += 24
                        time = "" + str(hour) + str(now.strftime(":%M:%S"))
                        return await message.channel.send(time)

                await message.channel.send("No timezone found for that user")


    @commands.command(name="set-time", aliases=["set time", "set_time", "time-set"], help="Sets your timezone")
    async def settime(self, message, zone):
        user = message.author.id
        zone = zone.lower().replace("utc", "")
        with open('timezones.txt', 'a') as f:
            f.write(f'\n{user} {zone}')
        await message.channel.send("Timezone set!")

def setup(bot):
    bot.add_cog(Time(bot))
