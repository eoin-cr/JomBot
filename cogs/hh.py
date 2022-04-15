# hh.py
import discord
from discord.ext import commands, tasks
import bot as main_bot
import datetime
import json
import random
import os
from cogs.netsoc import open_json


# Check to see if the message was sent in the right server (doesn't seem
# to work on @commands.Cog.listener() for some reason
def hh_check():
    def predicate(ctx):
        return ctx.guild.id == 574368093636395018

    return commands.check(predicate)


class HH(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.enabled_servers = []
        print("HH initialised")

    # Every day the value for that day from last week is wiped.  This way only
    # the messages sent in the last week are counted
    @tasks.loop(seconds=86400)
    async def clear_message_task(self):
        # does the loop for every server in the enabled servers list
        for element in self.enabled_servers:
            now = datetime.datetime.now()
            day = str(now.strftime('%A'))
            data = open_json(element)

            # for user id in the data struct, if today's day is in the uuid struct
            # set it to 0
            for uuid in data:
                if f"{day}" in data[f"{uuid}"]:
                    data[f'{uuid}'][f'{day}'] = 0

            # then write that data to the file
            with open(f"data_files/{element}.json", "w") as f:
                json.dump(data, f)

    @commands.command(name="enable-regular", aliases=["enable-weekly-messages", "enable-weekly",
                                                      "enable_regular",
                                                      "enable_weekly_messages", "enable_weekly",
                                                      "enable_weekly_message_counter"],
                      brief="Enables automated regular role function", help="!enable-regular "
                                                                            "[Role name] (amount "
                                                                            "of messages required—"
                                                                            "default 125/week)")
    @commands.has_guild_permissions(manage_guild=True)
    async def enable_regular(self, ctx, role, *amount):
        # checks if it's already been enabled
        if ctx.guild.id in self.enabled_servers:
            embed = main_bot.embed_func(ctx, "Regular", "Regular checker is already enabled", discord.Color.red)
            await ctx.send(embed=embed)
        else:
            self.enabled_servers.append(ctx.guild.id)

            main = open_json(ctx.guild.id)
            # print(f"main: {main}")
            if "settings" not in main:
                main["settings"] = {}
                with open(f"data_files/{ctx.guild.id}.json", "w") as f:
                    json.dump(main, f)

                # if "enabled" not in main["settings"]:
            main["settings"]["regular_enabled"] = True
            main["settings"]["regular_role"] = role
            if len(amount) != 0:
                main["settings"]["regular_amount"] = amount[0]
            else:
                main["settings"]["regular_amount"] = 125

            with open(f"data_files/{ctx.guild.id}.json", "w") as f:
                json.dump(main, f)

            embed = main_bot.embed_func(ctx, "Enabled regular", "Regular checker has been enabled on this server")
            await ctx.send(embed=embed)

    @commands.command(name="disable-regular", aliases=["disable-weekly-messages", "disable-weekly",
                                                       "disable_regular",
                                                       "disable_weekly_messages", "disable_weekly",
                                                       "disable_weekly_message_counter"],
                      help="Disables automated regular role function")
    @commands.has_guild_permissions(manage_guild=True)
    async def disable_regular(self, ctx):
        if ctx.guild.id not in self.enabled_servers:
            embed = main_bot.embed_func(ctx, "Regular", "Regular checker is not enabled", discord.Color.red)
            await ctx.send(embed=embed)
        else:
            index = self.enabled_servers.index(ctx.guild.id)
            self.enabled_servers.pop(index)

            main = open_json(ctx.guild.id)
            # print(f"main: {main}")
            if "settings" not in main:
                main["settings"] = {}
                with open(f"data_files/{ctx.guild.id}.json", "w") as f:
                    json.dump(main, f)

                # if "enabled" not in main["settings"]:
            main["settings"]["regular_enabled"] = False

            with open(f"data_files/{ctx.guild.id}.json", "w") as f:
                json.dump(main, f)

            embed = main_bot.embed_func(ctx, "Disabled regular", "Regular checker has been disabled on this server")
            await ctx.send(embed=embed)

    @commands.Cog.listener()
    @hh_check()
    async def on_message(self, ctx):
        # if ctx.guild.id == 829349685667430460:  # Pond
        # if ctx.guild.id == 574368093636395018:  # HH
        main = open_json(ctx.guild.id)
        if "settings" not in main:
            main["settings"] = {}
            with open(f"data_files/{ctx.guild.id}.json", "w") as f:
                json.dump(main, f)

        elif (not ctx.author.bot and "regular_enabled" in main["settings"] and
                main["settings"]["regular_enabled"]):
            uuid = ctx.author.id
            now = datetime.datetime.now()
            day = str(now.strftime('%A'))
            messages = 0

            # calls the function to open the json file
            data = open_json(ctx.guild.id)

            # if the clear message task isn't running, start it
            if not self.clear_message_task.is_running():
                self.clear_message_task.start()

            # if there is no data key, create one
            if "data" not in main:
                main["data"] = {}

            # if there isn't a uuid struct, create one
            if f"{uuid}" not in main["data"]:
                main["data"][f"{uuid}"] = {}

            # if there isn't a value for today's day in the uuid struct,
            # set the value to 0
            if f"{day}" not in main["data"][f"{uuid}"]:
                main["data"][f'{uuid}'][f'{day}'] = 0

            main["data"][f'{uuid}'][f'{day}'] += 1

            # for all the days in the uuid struct, add the value to the messages variable
            for days in main["data"][f"{uuid}"]:
                messages += main["data"][f"{uuid}"][f"{days}"]

            # fetch the role we want to assign
            regular = discord.utils.get((await ctx.guild.fetch_roles()),
                                        name=main["settings"]["regular_role"])
            # regular = discord.utils.get((await ctx.guild.fetch_roles()), name='tadpoles')

            # if they have sent over 125 messages in the last week, and do not already
            # have the regular role, give it to them
            if messages > main["settings"]["regular_amount"] and regular not in ctx.author.roles:
                await ctx.author.add_roles(regular)

            elif messages < main["settings"]["regular_amount"] and regular in ctx.author.roles:
                await ctx.author.remove_roles(regular)

            # write the json data to the file
            with open(f"data_files/{ctx.guild.id}.json", "w") as f:
                json.dump(main, f)

    @commands.command(name="flip", help="Flips a coin.  That's it.")
    async def flip(self, ctx):
        num = random.randint(1, 2)
        # print(num)
        if num == 1:
            await ctx.send("Heads")
        else:
            await ctx.send("Tails")

    @commands.command(name="vibe-check", alias="vibe_check", help="Checks someones"
                                                                  " vibes.")
    async def vibe_check(self, ctx, user):
        user = int(user.strip('@,<>,!,()'))
        vibes = ["hellish", "awful", "horrendous", "atrocious", "mediocre",
                 "acceptable", "decent", "ok", "good", "great", "fantastic",
                 "really good", "the best", "immaculate"]

        num = random.randint(0, len(vibes))
        memb = await ctx.guild.fetch_member(user)
        embed = discord.Embed(color=discord.Color.blue())
        embed.add_field(name="Vibe check", value=f"{memb.mention} has {vibes[num]} vibes!")
        embed.set_author(name=memb.display_name, icon_url=memb.avatar_url)
        await ctx.send(embed=embed)



def setup(bot):
    bot.add_cog(HH(bot))
