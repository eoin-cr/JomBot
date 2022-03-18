# time.py
import discord
from discord.ext import commands
from datetime import datetime
import bot as main
import json
import os


# TODO: use better file stuff than just a txt file - json file perhaps

class Time(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print("Time initialised")

    @commands.command(name="time", help="Displays current time in certain timezones")
    async def time(self, ctx, area):
        now = datetime.now()
        area = area.lower()
        if area == "us" or area == "america":
            hour = int(now.strftime("%H")) - 8
            if hour < 0:
                hour += 24
            time = "" + str(hour) + ":" + str(now.strftime("%M:%S"))
            await ctx.send(time)

        elif area == "uk" or area == "england" or area == "ireland":
            time = str(now.strftime("%H:%M:%S"))
            await ctx.send(time)

        elif area == "serbia":
            hour = int(now.strftime("%H")) + 1
            if hour >= 24:
                hour -= 24
            time = "" + str(hour) + str(now.strftime(":%M:%S"))
            await ctx.send(time)

        elif area == "canada":
            hour = int(now.strftime("%H")) - 5
            if hour < 0:
                hour += 24
            time = "" + str(hour) + str(now.strftime(":%M:%S"))
            await ctx.send(time)

        else:
            # print(area)
            area = int(area.strip('@,<>,!,()'))
            print(area)

            if not os.path.exists("timezones.json"):
                with open("timezones.json", "w") as f:
                    json.dump({}, f)

            with open("timezones.json") as f:
                data = json.load(f)

            print(area)
            print(data)
            print(data.get(f'{area}'))
            if data.get(f'{area}') is None:
                memb = await ctx.guild.fetch_member(area)
                embed = discord.Embed(color=discord.Color.purple())
                embed.add_field(name="Time", value="No timezone found for that user", inline=False)
                embed.set_author(name=memb.display_name, icon_url=memb.avatar_url)
                return await ctx.send(embed=embed)

            # Else statement isn't necessary due to the return in the if but it's more obvious
            # what the code means when quickly glancing at the code
            else:
                print("hi")
                hour = int(now.strftime("%H")) + int(data.get(f'{area}'))
                print(hour)
                if hour >= 24:
                    hour -= 24
                elif hour < 0:
                    hour += 24
                time = "" + str(hour) + str(now.strftime(":%M:%S"))
                memb = await ctx.guild.fetch_member(area)
                embed = discord.Embed(color=discord.Color.blue())
                embed.add_field(name="Time", value=f"The time for {memb.mention} is {time}", inline=False)
                embed.set_author(name=memb.display_name, icon_url=memb.avatar_url)
                print("hello")
                return await ctx.send(embed=embed)
                # return await message.channel.send(time)

    @commands.command(name="set-time", aliases=["set time", "time-set"],
                      help="Sets a user's timezone (use UTC+/-X)")
    async def set_time(self, message, zone, *user):
        if user is None:
            user = message.author.id
            # print("NONE!")
        else:
            temp = user
            user = zone
            zone = temp
            user = int(user.strip('@,<>,!,()'))

        zone = ''.join(zone)
        zone = zone.lower().replace("utc", "")
        if int(zone) < -12 or int(zone) > 12:
            embed = main.embed_func(message, "Set time", "Invalid timezone!  Set a time in the "
                                                         "format UTC+/-X.", discord.Color.red())
            return await message.channel.send(embed=embed)

        if not os.path.exists("timezones.json"):
            with open("timezones.json", "w") as f:
                json.dump({}, f)

        with open("timezones.json") as f:
            data = json.load(f)

        data[user] = zone

        with open("timezones.json", "w") as f:
            json.dump(data, f)

        memb = await message.guild.fetch_member(user)
        embed = main.embed_func(message, "Set time", f"{memb.mention}'s timezone has been set as UTC{zone}!")
        await message.channel.send(embed=embed)


def setup(bot):
    bot.add_cog(Time(bot))
