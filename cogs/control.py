import discord
from discord.ext import commands
import json
import os
import bot as main


class Control(commands.Cog):
    def __int__(self, bot):
        self.bot = bot
        print("Control initialised")

    @commands.command(name="set-prefix",
                      alias="set_prefix", help="Sets custom prefix for your "
                                               "server")
    async def set_prefix(self, ctx, prefix):
        if not os.path.exists('data_files'):
            os.makedirs('data_files')

        if not os.path.exists(f'data_files/prefixes.json'):
            os.mknod(f'data_files/prefixes.json')

            with open(f"data_files/prefixes.json", "w") as f:
                data = {}
                json.dump(data, f)

        # Open the prefixes file and read the data to `data`
        with open(f"data_files/prefixes.json") as f:
            data = json.load(f)
            # # checks if there's an entry for this guild in the data
            if ctx.guild.id not in data:
                data[f"{ctx.guild.id}"] = {"prefix": {}}

            data[f"{ctx.guild.id}"]["prefix"] = prefix

            with open(f"data_files/prefixes.json", "w") as file:
                json.dump(data, file)

        embed = main.embed_func(ctx, "Custom prefix", "Your custom prefix has"
                                                      f" been set as {prefix}")
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Control(bot))
