# hh.py
import discord
from discord.ext import commands, tasks
import bot as main
import datetime
import json
import os


# Check to see if the message was sent in the right server (doesn't seem
# to work on @commands.Cog.listener() for some reason
def hh_check():
    def predicate(ctx):
        return ctx.guild.id == 574368093636395018
    return commands.check(predicate)


# Function to open the json file and return the data
def open_json():
    if not os.path.exists("hh_messages.json"):
        with open("hh_messages.json", "w") as f:
            data = {}
            json.dump(data, f)

    # Open the timezones.json file and read the data to `data`
    with open("hh_messages.json") as f:
        data = json.load(f)

    return data


class HH(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print("HH initialised")

    # Every day the value for that day from last week is wiped.  This way only
    # the messages sent in the last week are counted
    @tasks.loop(seconds=86400)
    async def clear_message_task(self):
        now = datetime.datetime.now()
        day = str(now.strftime('%A'))
        data = open_json()

        # for user id in the data struct, if today's day is in the uuid struct
        # set it to 0
        for uuid in data:
            if f"{day}" in data[f"{uuid}"]:
                data[f'{uuid}'][f'{day}'] = 0

        # then write that data to the file
        with open("hh_messages.json", "w") as f:
            json.dump(data, f)

    @commands.Cog.listener()
    @hh_check()
    async def on_message(self, ctx):
        # if ctx.guild.id == 829349685667430460:  # Pond
        if ctx.guild.id == 574368093636395018:  # HH
            uuid = ctx.author.id
            now = datetime.datetime.now()
            day = str(now.strftime('%A'))
            messages = 0

            # calls the function to open the json file
            data = open_json()

            # if the clear message task isn't running, start it
            if not self.clear_message_task.is_running():
                self.clear_message_task.start()

            # if there isn't a uuid struct, create one
            if f"{uuid}" not in data:
                data[f"{uuid}"] = {}

            # if there isn't a value for today's day in the uuid struct,
            # set the value to 0
            if f"{day}" not in data[f"{uuid}"]:
                data[f'{uuid}'][f'{day}'] = 0

            data[f'{uuid}'][f'{day}'] += 1

            # for all the days in the uuid struct, add the value to the messages variable
            for days in data[f"{uuid}"]:
                messages += data[f"{uuid}"][f"{days}"]

            # fetch the role we want to assign
            regular = discord.utils.get((await ctx.guild.fetch_roles()), name='Regular')
            # regular = discord.utils.get((await ctx.guild.fetch_roles()), name='tadpoles')

            # if they have sent over 125 messages in the last week, and do not already
            # have the regular role, give it to them
            if messages > 125 and regular not in ctx.author.roles:
                await ctx.author.add_roles(regular)

            elif messages < 125 and regular in ctx.author.roles:
                await ctx.author.remove_roles(regular)

            # write the json data to the file
            with open("hh_messages.json", "w") as f:
                json.dump(data, f)


def setup(bot):
    bot.add_cog(HH(bot))
