#crypto.py
import os
import re
import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
import cryptocompare
import json

class Crypto(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        print("Crypto initialised")

#     @commands.command()
    def get_usd_crypto_price(self,coin):
        usd_crypto_price = str(cryptocompare.get_price(coin, currency='USD')).strip('{}:')
        f = usd_crypto_price.split(' ')
        usd_price = f[2]
        return usd_price

#     @commands.command()
    def get_day_price(self,coin):
        usd_crypto_price = str(cryptocompare.get_historical_price_day(coin, currency='USD')).strip('{}:')
        f = usd_crypto_price.split(' ')
        # print(len(f))
        # print(f)
        day_price = f[-11]
        day_price = day_price.strip(',')
        # print(day_price)
        # print(f[25918:25938])
        return day_price

    @commands.command()
    async def price(self,message,ctx):
        coin = str(ctx)
        crypto_price = self.bot.get_cog('Crypto_Price')
#         print(await crypto_price.get_usd_crypto_price(coin))
        usd_price = float(await crypto_price.get_usd_crypto_price(coin))
        price = "${}".format(usd_price)
        day_price = float(await crypto_price.get_day_price(coin))
        daily_change = usd_price / day_price * 100 - 100
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

    @commands.command(name="cbuy", help="Buys a certain crypto")
    async def cbuy(self, ctx, coin, amount):
#         try:
#             coin, amount = message.content.split()[1:3]
        everything = False
        auth = ctx.message.author.id

        if not os.path.exists(f"users/{auth}.json"):
            with open(f"users/{auth}.json", "w") as f:
                json.dump({}, f)
        with open(f"users/{auth}.json", "r") as f:
          data = json.load(f)

        if amount == "all":
            everything = True
            amount = data["USD"]
        else:
            amount = float(amount)

        usd_price = self.get_usd_crypto_price(coin)
        coin_price = float(amount)/float(usd_price)
        if data.get(coin) is None:
          data[coin] = 0.0
        if data.get("USD") is None:
          data["USD"] = 10000.0
        if amount > data.get("USD"):
            return await ctx.send("""Warning: Could not complete trade,
coin balance too low.  Your current USD balance is {:0.2f}""".format(data.get("USD")))

        elif everything:
            data[coin] += coin_price
            all = data["USD"]
            data["USD"] = 0
            await ctx.send("Successfully traded ${:0.2f} for {:0.2f}{}".format(all, coin_price, coin.upper()))

        else:
            data[coin] += coin_price
            data["USD"] -= amount
            await ctx.send("Successfully traded ${:0.2f} for {:0.2f}{}".format(amount, coin_price, coin.upper()))
        with open(f"users/{auth}.json", "w") as f:
            json.dump(data, f)
#         except:
#             await ctx.send("""Looks like there may have been
# a mistake, make sure the command is \n `!cbuy [coin] [amount in usd/all]`""")

    @commands.command(name="csell", help="Sell a certain crypto")
    async def csell(self, ctx, coin, amount):
#         try:
        usd_price = self.get_usd_crypto_price(coin)
        everything = False
        auth = ctx.message.author.id

        if not os.path.exists(f"users/{auth}.json"):
            with open(f"users/{auth}.json", "w") as f:
                json.dump({}, f)
        with open(f"users/{auth}.json", "r") as f:
          data = json.load(f)

        if amount == "all":
            everything = True
            amount = data[coin] * usd_price
        else:
            amount = float(amount)

        coin_price = float(amount)/float(usd_price)
        auth = ctx.message.author.id

        if data.get(coin) is None:
          data[coin] = 0.0
        if data.get("USD") is None:
          data["USD"] = 10000.0
        if amount > data.get(coin):
          await ctx.send("""Warning: Could not complete trade,
coin balance too low.  Your current {} balance is {}""".format(coin, data.get(coin)))
          return

        elif everything:
            data["USD"] += amount
            all = data[coin]
            data[coin] = 0
            await ctx.send("Successfully traded {:0.2f}{} for ${:0.2f}".format(coin_price, coin.upper(), all))
        else:
            data[coin] -= coin_price
            data["USD"] += amount
            await ctx.send("Successfully traded {:0.2f}{} for ${:0.2f}".format(coin_price, coin.upper(), amount))
        with open(f"users/{auth}.json", "w") as f:
            json.dump(data, f)
#         except:
#             await ctx.send("""Looks like there may have been
# a mistake, make sure the command is  \n `!csell [coin] [amount in usd/all]`""")

    @commands.command(name="wallet", help="Displays crypto wallet")
    async def wallet(self, ctx, *user):
#         print(user)
        if len(user) != 0:
#         if user != "()":
#         if user is not None:
#             member = await bot.fetch_user(user)
            user= int(user[0].strip('@,<>,!,()'))
            memb = await ctx.guild.fetch_member(user)

#             auth = ctx.message.author.id
            if not os.path.exists(f"users/{user}.json"):
                with open(f"users/{user}.json", "w") as f:
                    json.dump({"USD": 10000.0}, f)
            with open(f"users/{user}.json", "r") as fh:
                data = json.load(fh)

            total = 0
            embed=discord.Embed(title="{}'s wallet".format(memb.display_name), color=discord.Color.blue())
            embed.set_author(name=memb.display_name, icon_url=memb.avatar_url)
            for coin, value in data.items():
                if value != 0:
                    embed.add_field(name=coin, value="{:0.2f}".format(value))
                    total += float(self.get_usd_crypto_price(coin)) * value

            embed.add_field(name="Total", value="Total: ${:0.2f}".format(total))
            await ctx.send(embed=embed)

        else:
            auth = ctx.message.author.id
            if not os.path.exists(f"users/{auth}.json"):
                with open(f"users/{auth}.json", "w") as f:
                    json.dump({}, f)
            with open(f"users/{auth}.json", "r") as f:
                data = json.load(f)

            total = 0
            embed=discord.Embed(title="{}'s wallet".format(ctx.message.author.display_name), color=discord.Color.blue())
            embed.set_author(name=ctx.message.author.display_name, icon_url=ctx.message.author.avatar_url)
            for coin, value in data.items():
                if value != 0:
                    embed.add_field(name=coin.upper(), value="{:0.2f}".format(value))
                    total += float(self.get_usd_crypto_price(coin)) * value
            embed.add_field(name="Total", value="Total: ${:0.2f}".format(total))
            await ctx.send(embed=embed)
            return

#         with open('userCash.txt', 'r') as file:
#             cash = file.readlines()
#         for user in cash:
#             if user == ctx.message.author.id:
#                 cash[i+1] = '{}\n'.format(cash[i+1] - amount)
# #                 print(cash[i+1])
#                 cash[i+2] = '{}\n'.format(cash[i+2] + btc)
#                 with open('userCash.txt', 'w') as file:
#                     file.writelines( coin )
#                 await ctx.send("Successfully traded ${} for {}btc".format(amount, btc))
#             else:
#                 i =+ 1
# #                 print("users don't match")
#     await bot.process_commands(message)


def setup(bot):
    bot.add_cog(Crypto(bot))
