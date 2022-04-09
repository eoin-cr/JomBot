import discord
from discord.ext import commands
import json
import os
import random

intents = discord.Intents.default()
intents.members = True


# Function to open the json file and return the data
def open_json():
    if not os.path.exists("netsoc_xp.json"):
        with open("netsoc_xp.json", "w") as f:
            data = {}
            json.dump(data, f)

    # Open the netsoc_xp.json file and read the data to `data`
    with open("netsoc_xp.json") as f:
        data = json.load(f)

    return data


class Netsoc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.invites_disabled = False
        self.server_id = 481106476060901406
        self.welcome_channel = 546797615551873054
        self.level_channel = 688143673791479858
        self._cd = commands.CooldownMapping.from_cooldown(1.0, 60.0, commands.BucketType.user)
        print("Netsoc initialised")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        print("Hi")
        print(member.guild.id)
        if member.guild.id == self.server_id:
            channel = member.guild.get_channel(self.welcome_channel)
            await channel.send(f"""Hello World! Welcome to the UCD Netsoc Discord {member.mention}! 💻 \n
Please make sure to read the rules in <#687431174200492100> , get your pronouns and stage in \
<#728418690323972176> and then introduce yourself in <#699759673460654122>
            """)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        print("Hello")
        print(member.guild.id)
        if member.guild.id == self.server_id:
            channel = member.guild.get_channel(self.welcome_channel)
            await channel.send(
                f"**{member.name}#{member.discriminator}** just left the server, press F to pay respects.")

    @commands.Cog.listener()
    # @commands.cooldown(1, 60, commands.BucketType.user)
    async def on_message(self, ctx):
        if ctx.guild.id == self.server_id and not ctx.author.bot:
            bucket = self._cd.get_bucket(ctx)
            retry_after = bucket.update_rate_limit()
            if not retry_after:
                print("Hello")
                # you're not rate limited
                # calls the function to open the json file
                data = open_json()

                # gets channel to send level up message in
                channel = ctx.guild.get_channel(self.level_channel)
                # await channel.send(ctx.author.mention)

                uuid = ctx.author.id

                # if there isn't a uuid struct, create one
                if f"{uuid}" not in data:
                    data[f"{uuid}"] = {}

                # if there isn't a value for a user's XP in the uuid struct,
                # set the value to 0
                if "xp" not in data[f"{uuid}"]:
                    data[f'{uuid}']['xp'] = 0

                # if there isn't a value for a user's level in the uuid struct,
                # set the value to 0
                if "level" not in data[f"{uuid}"]:
                    data[f'{uuid}']['level'] = 0

                xp = data[f'{uuid}']['xp']
                level = data[f"{uuid}"]['level']
                new_xp = random.randint(15, 25)

                print(f"xp: {xp} level: {level} new_xp: {new_xp}")

                amount_to_next = 5 * (level ** 2) + (50 * level) + 100 - xp

                if amount_to_next - new_xp <= 0:
                    await channel.send("The results of hard work and dedication "
                                       "always look like luck to saps. But you "
                                       "know you've earned every ounce of your "
                                       f"success. GG {ctx.author.mention}, you just advanced to "
                                       f"level {level + 1}")
                    data[f"{uuid}"]["level"] += 1
                    xp = 0 - amount_to_next

                data[f"{uuid}"]["xp"] = xp + new_xp
                with open("netsoc_xp.json", "w") as f:
                    json.dump(data, f)


def setup(bot):
    bot.add_cog(Netsoc(bot))
