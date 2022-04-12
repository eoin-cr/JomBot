import discord
from discord.ext import commands
import json
import os
import random
import bot as main_bot

intents = discord.Intents.default()
intents.members = True


# Function to open the json file and return the data
def open_json(guild_id):
    if not os.path.exists('data_files'):
        os.makedirs('data_files')

    if not os.path.exists(f'data_files/{guild_id}.json'):
        os.mknod(f'data_files/{guild_id}.json')

        # if not os.path.exists(f"data_files/{guild_id}.json"):
        with open(f"data_files/{guild_id}.json", "w") as f:
            data = {}
            json.dump(data, f)

    # Open the netsoc_xp.json file and read the data to `data`
    with open(f"data_files/{guild_id}.json") as f:
        data = json.load(f)

    return data


class Netsoc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.invites_disabled = False
        self.server_id = 481106476060901406
        self.welcome_channel = 546797615551873054
        # self.level_channel = 688143673791479858
        self.level_channel = 820432713160851466
        self._cd = commands.CooldownMapping.from_cooldown(1.0, 1.0, commands.BucketType.user)
        print("Netsoc initialised")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        # print("Hi")
        print(member.guild.id)
        if member.guild.id == self.server_id:
            channel = member.guild.get_channel(self.welcome_channel)
            await channel.send(f"""Hello World! Welcome to the UCD Netsoc Discord {member.mention}! 💻 \n
Please make sure to read the rules in <#687431174200492100> , get your pronouns and stage in \
<#728418690323972176> and then introduce yourself in <#699759673460654122>
            """)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        # print("Hello")
        # print(member.guild.id)
        if member.guild.id == self.server_id:
            channel = member.guild.get_channel(self.welcome_channel)
            await channel.send(
                f"**{member.name}#{member.discriminator}** just left the server, press F to pay respects.")

    @commands.command(name="enable-level", aliases=["enable-levelling", "enable-levels", "enable_level",
                                                    "enable_levelling", "enable_levels"],
                      brief="Enables server levelling", help="!enable-level [channel to post level up messages]")
    @commands.has_guild_permissions(manage_guild=True)
    async def enable_level(self, ctx, *channel):
        if len(channel) != 0:
            # print(f"channel: {channel}")
            # print(f"ch0: {channel[0]}")
            ch = channel[0].replace("<#", "").replace(">", "")
        else:
            ch = ctx.channel.id

        main = open_json(ctx.guild.id)
        # print(f"main: {main}")
        if "settings" not in main:
            main["settings"] = {}
            with open(f"data_files/{ctx.guild.id}.json", "w") as f:
                json.dump(main, f)

            # if "enabled" not in main["settings"]:
        main["settings"]["levelling_enabled"] = True
        main["settings"]["levelling_channel"] = ch
        with open(f"data_files/{ctx.guild.id}.json", "w") as f:
            json.dump(main, f)

        embed = main_bot.embed_func(ctx, "Enabled levelling", "Levelling has been enabled on this server")
        await ctx.send(embed=embed)

    @commands.command(name="disable-level", aliases=["disable-levelling", "disable-levels", "disable_level",
                                                     "disable_levelling", "disable_levels"],
                      help="Disables server levelling")
    @commands.has_guild_permissions(manage_guild=True)
    async def disable_level(self, ctx):
        main = open_json(ctx.guild.id)
        # print(f"main: {main}")
        if "settings" not in main:
            main["settings"] = {}
            with open(f"data_files/{ctx.guild.id}.json", "w") as f:
                json.dump(main, f)

        else:
            # if "enabled" not in main["settings"]:
            main["settings"]["levelling_enabled"] = False
            with open(f"data_files/{ctx.guild.id}.json", "w") as f:
                json.dump(main, f)

            embed = main_bot.embed_func(ctx, "Disabled levelling", "Levelling has been disabled on this server")
            await ctx.send(embed=embed)

    @commands.Cog.listener()
    # @commands.cooldown(1, 60, commands.BucketType.user)
    async def on_message(self, ctx):
        # calls the function to open the json file
        main = open_json(ctx.guild.id)
        # print(f"main: {main}")
        # print(main["settings"]["enabled"])
        if "settings" not in main:
            main["settings"] = {}
            with open(f"data_files/{ctx.guild.id}.json", "w") as f:
                json.dump(main, f)

        elif not ctx.author.bot and "levelling_enabled" in main["settings"] and main["settings"]["levelling_enabled"]:
            bucket = self._cd.get_bucket(ctx)
            retry_after = bucket.update_rate_limit()
            if not retry_after:
                # you're not rate limited

                # print("hi")

                # # gets channel to send level up message in
                # channel = ctx.guild.get_channel(self.level_channel)
                # await channel.send(ctx.author.mention)
                # print(f"mainch: {main['settings']['levelling_channel']}")
                channel = ctx.guild.get_channel(int(main["settings"]["levelling_channel"]))
                # print(f"ch2: {channel}")

                if "data" not in main:
                    main["data"] = {}

                uuid = ctx.author.id

                # if there isn't a uuid struct, create one
                if f"{uuid}" not in main["data"]:
                    main["data"][f"{uuid}"] = {}

                # if there isn't a value for a user's XP in the uuid struct,
                # set the value to 0
                if "xp" not in main["data"][f"{uuid}"]:
                    main["data"][f'{uuid}']['xp'] = 0

                # if there isn't a value for a user's level in the uuid struct,
                # set the value to 0
                if "level" not in main["data"][f"{uuid}"]:
                    main["data"][f'{uuid}']['level'] = 0

                xp = main["data"][f'{uuid}']['xp']
                level = main["data"][f"{uuid}"]['level']
                new_xp = random.randint(15, 25)

                # print(f"xp: {xp} level: {level} new_xp: {new_xp}")

                amount_to_next = 5 * (level ** 2) + (50 * level) + 100 - xp

                if amount_to_next - new_xp <= 0:
                    # print(f"channel.send: {channel}")
                    await channel.send("The results of hard work and dedication "
                                       "always look like luck to saps. But you "
                                       "know you've earned every ounce of your "
                                       f"success. GG {ctx.author.mention}, you just advanced to "
                                       f"level {level + 1}")
                    main["data"][f"{uuid}"]["level"] += 1
                    xp = 0 - amount_to_next

                main["data"][f"{uuid}"]["xp"] = xp + new_xp
                with open(f"data_files/{ctx.guild.id}.json", "w") as f:
                    json.dump(main, f)


def setup(bot):
    bot.add_cog(Netsoc(bot))
