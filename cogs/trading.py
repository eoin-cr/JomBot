# trading.py
import os
import re
import discord
import requests
from dotenv import load_dotenv
from discord.ext import commands
import cryptocompare
import json
from discord.utils import find

# bot = commands.Bot(command_prefix='!')

class Trading(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        print("Trading initialised")

    @commands.command()
    async def price(self,message,ctx):
        coin = str(ctx)
        crypto_price = self.bot.get_cog('Crypto_Price')
#         print(await crypto_price.get_usd_crypto_price(coin))
        uprice = float(await crypto_price.get_usd_crypto_price(coin))
        price = "${}".format(uprice)
        dprice = float(await crypto_price.get_day_price(coin))
        daily_change = uprice / dprice * 100 - 100
        embed = discord.Embed(title="{} price".format(coin.upper()), description=price, color=discord.Color.blue())
        embed.set_author(name=message.author.display_name, icon_url=message.author.avatar_url)
        embed.add_field(name="Daily change", value='{}%'.format(round(daily_change)))
        embed.set_footer(text="Trade wisely")
        embed.set_thumbnail(url="https://uploads.tradestation.com/uploads/2017/12/Crypto-1024x1024.jpg")
        await message.channel.send(embed=embed)
        return

    @commands.command()
    async def chelp(self,message):
    # if message.content.startswith('!chelp') or message.content.startswith("<@!820065836139675668> help"):
        embed=discord.Embed(title="Help", color=discord.Color.blue())
        embed.set_author(name=message.author.display_name, icon_url=message.author.avatar_url)
        embed.add_field(name="Commands", value="""Ban/Allow the among us words \
        (sus, vented, etc) [allowed by default - enabling may result in messages \
        with legitimate words containing words like sus getting removed.] - `!1984 \
        start/stop` [must have manage server perms] \n Buy crypto - `!cbuy [coin] \
        [price in usd/all]` \n Sell crypto - `!csell [coin] [price in usd/all]` \
        \n Price of a coin - `!price [coin]` \n View wallet - `!wallet`""")
        await message.channel.send(embed=embed)
        return

    # @commands.command()
    # async def cbuy(self,message,ctx):
    #     try:
    #         coin, amount = message.content.split()[1:3]
    #         everything = False
    #         auth = message.author.id
    #         if not os.path.exists(f"../users/{auth}.json"):
    #             with open(f"../users/{auth}.json", "w") as f:
    #                 json.dump({}, f)
    #         with open(f"../users/{auth}.json", "r") as f:
    #           data = json.load(f)
    #         if amount == "all":
    #             everything = True
    #             amount = data["USD"]
    #
    #         else:
    #             amount = float(amount)
    #         uprice = get_usd_crypto_price(coin)
    #         # btc_price = get_usd_crypto_price("btc")
    #         cprice = float(amount)/float(uprice)
    #         # with open(f"users/{auth}.json", "r") as f:
    #         #   data = json.load(f)
    #         if data.get(coin) is None:
    #           data[coin] = 0.0
    #         if data.get("USD") is None:
    #           data["USD"] = 10000.0
    #         if amount > data.get("USD"):
    #             await message.channel.send("""Warning: Could not complete trade, \
    #             coin balance too low.  Your current USD balance is {:0.2f}""".format(data.get("USD")))
    #             return
    #         if everything:
    #             data[coin] += cprice
    #             all = data["USD"]
    #             data["USD"] = 0
    #             await message.channel.send("Successfully traded ${:0.2f} for {:0.2f}{}".format(all, cprice, coin.upper()))
    #         else:
    #             data[coin] += cprice
    #             data["USD"] -= amount
    #             await message.channel.send("Successfully traded ${:0.2f} for {:0.2f}{}".format(amount, cprice, coin.upper()))
    #         with open(f"users/{auth}.json", "w") as f:
    #           json.dump(data, f)
    #         return
    #     except:
    #         return await message.channel.send("""Looks like there may have been \
    #         a mistake, make sure the command is \n `!cbuy [coin] [amount in usd/all]`""")
    #
    # @commands.command()
    # async def csell(self,message,ctx):
    #     try:
    #         coin, amount = message.content.split()[1:3]
    #         uprice = get_usd_crypto_price(coin)
    #         everything = False
    #         auth = message.author.id
    #         # print(amount)
    #         # print(uprice)
    #         # print(amount*uprice)
    #         if not os.path.exists(f"users/{auth}.json"):
    #             with open(f"users/{auth}.json", "w") as f:
    #                 json.dump({}, f)
    #         with open(f"users/{auth}.json", "r") as f:
    #           data = json.load(f)
    #
    #         # print(data[coin])
    #         if amount == "all":
    #             everything = True
    #             amount = data[coin] * uprice
    #         else:
    #             amount = float(amount)
    #         # btc_price = get_usd_crypto_price("btc")
    #         cprice = float(amount)/float(uprice)
    #         auth = message.author.id
    #         # with open(f"users/{auth}.json", "r") as f:
    #         #   data = json.load(f)
    #         if data.get(coin) is None:
    #           data[coin] = 0.0
    #         if data.get("USD") is None:
    #           data["USD"] = 10000.0
    #         if amount > data.get(coin):
    #           await message.channel.send("""Warning: Could not complete trade, \
    #           coin balance too low.  Your current {} balance is {}""".format(coin, data.get(coin)))
    #           return
    #         if everything:
    #             data["USD"] += amount
    #             all = data[coin]
    #             data[coin] = 0
    #             await message.channel.send("Successfully traded {:0.2f}{} for ${:0.2f}".format(cprice, coin.upper(), all))
    #         else:
    #             data[coin] -= cprice
    #             data["USD"] += amount
    #             await message.channel.send("Successfully traded {:0.2f}{} for ${:0.2f}".format(cprice, coin.upper(), amount))
    #         with open(f"users/{auth}.json", "w") as f:
    #           json.dump(data, f)
    #         return
    #     except:
    #         return await message.channel.send("""Looks like there may have been \
    #         a mistake, make sure the command is  \n `!csell [coin] [amount in usd/all]`""")
    #
    # @commands.command()
    # async def wallet(self,message,*ctx):
    #     # print(message.content)
    #     # cont = message.content.split(' ')
    #     # if len(cont) > 1:
    #     if ctx is not None:
    #         print(ctx)
    #         ctx_str = str(ctx)
    #         auth = ctx_str.strip('@,<>,!')
    #         #await client.fetch_user(auth)
    #         memb = await guild.fetch_user(auth)
    #         if not os.path.exists(f"users/{auth}.json"):
    #             with open(f"users/{auth}.json", "w") as f:
    #                 json.dump({}, f)
    #         with open(f"users/{auth}.json", "r") as f:
    #           data = json.load(f)
    #         total = 0
    #         embed=discord.Embed(title="{}'s wallet".format(memb.display_name), color=discord.Color.blue())
    #         embed.set_author(name=memb.display_name, icon_url=memb.avatar_url)
    #         for coin, value in data.items():
    #           if value != 0:
    #             embed.add_field(name=coin, value="{:0.2f}".format(value))
    #           # print(get_usd_crypto_price(coin))
    #             total += float(get_usd_crypto_price(coin)) * value
    #         embed.add_field(name="Total", value="Total: ${:0.2f}".format(total))
    #         await ctx.send(embed=embed)
    #         return
    #     else:
    #         auth = message.author.id
    #         if not os.path.exists(f"users/{auth}.json"):
    #             with open(f"users/{auth}.json", "w") as f:
    #                 json.dump({}, f)
    #         with open(f"users/{auth}.json", "r") as f:
    #           data = json.load(f)
    #         total = 0
    #         embed=discord.Embed(title="{}'s wallet".format(message.author.display_name), color=discord.Color.blue())
    #         embed.set_author(name=message.author.display_name, icon_url=message.author.avatar_url)
    #         for coin, value in data.items():
    #           if value != 0:
    #             embed.add_field(name=coin.upper(), value="{:0.2f}".format(value))
    #             total += float(get_usd_crypto_price(coin)) * value
    #         embed.add_field(name="Total", value="Total: ${:0.2f}".format(total))
    #         await ctx.send(embed=embed)
    #         return

def setup(bot):
    bot.add_cog(Trading(bot))
