import discord
from discord.ext import commands
import json
# import os
import bot as main


class Control(commands.Cog):
    def __int__(self, bot):
        self.bot = bot
        print("Control initialised")

    @commands.command(name="set-prefix",
                      alias="set_prefix", help="Sets custom prefix for your "
                                               "server")
    @commands.has_guild_permissions(manage_guild=True)
    async def set_prefix(self, ctx, prefix):
        # Open the prefixes file and read the data to `data`
        with open(f"data_files/prefixes.json") as f:
            data = json.load(f)
            # # checks if there's an entry for this guild in the data
            if f"{ctx.guild.id}" not in data:
                data[f"{ctx.guild.id}"] = {"prefix": {}}

            data[f"{ctx.guild.id}"]["prefix"] = prefix

            with open(f"data_files/prefixes.json", "w") as file:
                json.dump(data, file)

        embed = main.embed_func(ctx, "Custom prefix", "Your custom prefix has"
                                                      f" been set as {prefix}")
        await ctx.send(embed=embed)

    @commands.command(name="prefix", alias="prefix?", help="Sends the prefix "
                                                           "currently set on "
                                                           "your server")
    async def prefix(self, ctx):
        # Open the prefixes file and read the data to `data`
        with open(f"data_files/prefixes.json") as f:
            data = json.load(f)

        # checks if there's an entry for this guild in the data
        if ctx.guild.id not in data:
            # if there's no custom prefix, the server must be using the
            # default prefix, so return that
            prefix = "!"

        else:
            # otherwise, return the prefix they have stored
            prefix = data[f"{ctx.guild.id}"]["prefix"]

        embed = main.embed_func(ctx, "Custom prefix", "Your custom prefix is"
                                                      f" {prefix}")
        await ctx.send(embed=embed)

    @commands.command(name="del-prefix", aliases=["delete-prefix", "del_prefix",
                                                                   "delete_prefix"],
                      help="Deletes the custom prefix for your server")
    @commands.has_guild_permissions(manage_guild=True)
    async def del_prefix(self, ctx):
        # Open the prefixes file and read the data to `data`
        with open(f"data_files/prefixes.json") as f:
            data = json.load(f)

        # checks if there's an entry for this guild in the data
        # print(f"id: {ctx.guild.id}, data: {data}")
        if f"{ctx.guild.id}" not in data:
            embed = main.embed_func(ctx, "Delete prefix",
                                    "Your server has no custom prefix to"
                                    " delete",
                                    discord.Color.red())
            return await ctx.send(embed=embed)

        else:
            # otherwise, delete the prefix they have stored
            data[f"{ctx.guild.id}"]["prefix"] = ""

        with open(f"data_files/prefixes.json", "w") as f:
            # print(f"data2: {data}")
            json.dump(data, f)

        embed = main.embed_func(ctx, "Deleted prefix", "Your custom prefix"
                                                       " has been deleted.")
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Control(bot))
