# crypto.py
import os
import discord
from discord.ext import commands
import cryptocompare
import json


# Function uses cryptocompare API to get the price of a certain coin
# in USD.
def get_usd_crypto_price(coin):
    usd_crypto_price = str(cryptocompare.get_price(coin, currency='USD')).strip('{}:')
    f = usd_crypto_price.split(' ')
    # Just removing some unnecessary info
    usd_price = f[2]
    return usd_price


# Function gets the price at the start of the day with a cryptocompare API
# call.  This way info can be used to compare with the current price to see
# the change
def get_day_price(coin):
    usd_crypto_price = str(cryptocompare.get_historical_price_day(coin, currency='USD')).strip('{}:')
    # Just removing some unnecessary info
    f = usd_crypto_price.split(' ')
    day_price = f[-11]
    day_price = day_price.strip(',')
    return day_price


def open_json(auth):
    # Creates a json file (if it doesn't already exist) to store the details
    # of the user's coins.  This acts as a database so even if the bot is
    # restarted, these values will remain
    if not os.path.exists(f"users/{auth}.json"):
        with open(f"users/{auth}.json", "w") as f:
            json.dump({}, f)

    # Opens and loads the user's coins file
    with open(f"users/{auth}.json", "r") as f:
        data = json.load(f)

    # Returns the data
    return data


class Crypto(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print("Crypto initialised")

    @commands.command(name="price", help="Returns the price of a crypto")
    async def price(self, message, ctx):
        coin = str(ctx)
        # Gets usd price of the coin
        usd_price = float(get_usd_crypto_price(coin))
        price = "${}".format(usd_price)

        # Gets the price of the coin at the start of the day
        # then calculate the percent change with current.
        day_price = float(get_day_price(coin))
        daily_change = usd_price / day_price * 100 - 100

        # Creates a discord embed to look nicer
        embed = discord.Embed(title="{} price".format(coin.upper()), description=price, color=discord.Color.blue())
        embed.set_author(name=message.author.display_name, icon_url=message.author.avatar_url)
        embed.add_field(name="Daily change", value='{}%'.format(round(daily_change)))
        embed.set_footer(text="Trade wisely")
        embed.set_thumbnail(url="https://uploads.tradestation.com/uploads/2017/12/Crypto-1024x1024.jpg")
        await message.channel.send(embed=embed)
        return

    @commands.command(name="chelp", help="Returns a little help embed")
    async def chelp(self, message):
        # Creates and sends a help embed
        embed = discord.Embed(title="Help", color=discord.Color.blue())
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
        everything = False
        auth = ctx.message.author.id

        # Calls function to open json file
        data = open_json(auth)

        # Checks if the user wants to spend all their USD to buy a coin.  If
        # so, sets everything to true
        if amount == "all":
            everything = True
            amount = data["USD"]
        else:
            amount = float(amount)

        # Divides the amount of money the user is spending by the price of one
        # coin to determine how many coins the user is getting
        usd_price = get_usd_crypto_price(coin)
        coin_price = float(amount) / float(usd_price)

        # If the user has not already bought this coin, add it to the db
        if data.get(coin) is None:
            data[coin] = 0.0

        # If they haven't traded before, gives them 10k USD
        if data.get("USD") is None:
            data["USD"] = 10000.0

        # Doesn't allow buying more than you can afford
        if amount > data.get("USD"):
            return await ctx.send("""Warning: Could not complete trade,
coin balance too low.  Your current USD balance is {:0.2f}""".format(data.get("USD")))

        # Calculation for spending all your USD
        elif everything:
            data[coin] += coin_price
            amount = data["USD"]
            data["USD"] = 0
            await ctx.send("Successfully traded ${:0.2f} for {:0.2f}{}".format(amount, coin_price, coin.upper()))

        # Calculation for only spending a certain amount of money
        else:
            data[coin] += coin_price
            data["USD"] -= amount
            await ctx.send("Successfully traded ${:0.2f} for {:0.2f}{}".format(amount, coin_price, coin.upper()))

        # Opens the json file and dumps all the new variables
        with open(f"users/{auth}.json", "w") as f:
            json.dump(data, f)

    @commands.command(name="csell", help="Sell a certain crypto")
    async def csell(self, ctx, coin, amount):
        usd_price = get_usd_crypto_price(coin)
        everything = False
        auth = ctx.message.author.id

        # Opens the users json file
        data = open_json(auth)

        # Checks if the user wants to sell all of a coin, if so works out USD
        # value by multiplying the amount of coins by the current USD price
        if amount == "all":
            everything = True
            amount = data[coin] * usd_price
        else:
            amount = float(amount)

        # Coin amount is just used to tell the user how many coins they sold
        coin_amount = float(amount) / float(usd_price)
        auth = ctx.message.author.id

        # If the coin hasn't been traded by the user yet, initialise the amount
        # to 0
        if data.get(coin) is None:
            data[coin] = 0.0

        # If the user hasn't traded before give them 10k USD
        if data.get("USD") is None:
            data["USD"] = 10000.0

        # Doesn't allow the user to spend more than they have
        if amount > data.get(coin):
            await ctx.send("""Warning: Could not complete trade,
coin balance too low.  Your current {} balance is {}""".format(coin, data.get(coin)))
            return

        # Calculation for selling all of a coin
        elif everything:
            data["USD"] += amount
            amount_all = data[coin]
            data[coin] = 0
            await ctx.send("Successfully traded {:0.2f}{} for ${:0.2f}".format(coin_amount, coin.upper(), amount_all))

        # Calculation for calculating a certain amount of a coin
        else:
            data[coin] -= coin_amount
            data["USD"] += amount
            await ctx.send("Successfully traded {:0.2f}{} for ${:0.2f}".format(coin_amount, coin.upper(), amount))
        with open(f"users/{auth}.json", "w") as f:
            json.dump(data, f)

    @commands.command(name="wallet", help="Displays crypto wallet")
    async def wallet(self, ctx, *user):
        # Checks if the user gave a second input (i.e. to check someone
        # else's wallet
        if len(user) != 0:

            # When you tag a user it automatically displays something like
            # @<!12345> so we want to remove that extra stuff and just get
            # the id
            user = int(user[0].strip('@,<>,!,()'))
            memb = await ctx.guild.fetch_member(user)

            # Opens the user's json file
            data = open_json(user)

            # Sets running total as 0
            total = 0

            # Creates an embed
            embed = discord.Embed(title="{}'s wallet".format(memb.display_name), color=discord.Color.blue())
            embed.set_author(name=memb.display_name, icon_url=memb.avatar_url)

            # For each coin the user has, work out the USD value of the amount
            # they have
            for coin, value in data.items():
                if value != 0:
                    embed.add_field(name=coin, value="{:0.2f}".format(value))
                    total += float(get_usd_crypto_price(coin)) * value

            # Adds a total field to the embed
            embed.add_field(name="Total", value="Total: ${:0.2f}".format(total))
            await ctx.send(embed=embed)

        else:

            # Otherwise, just display the user's own wallet
            auth = ctx.message.author.id

            # Opens the user's json file
            data = open_json(auth)

            # Sets total as 0
            total = 0

            # Creates an embed
            embed = discord.Embed(title="{}'s wallet".format(ctx.message.author.display_name),
                                  color=discord.Color.blue())
            embed.set_author(name=ctx.message.author.display_name, icon_url=ctx.message.author.avatar_url)

            # Works out the USD value of each coin in your wallet, adds this to
            # the embed and the total
            for coin, value in data.items():
                if value != 0:
                    embed.add_field(name=coin.upper(), value="{:0.2f}".format(value))
                    total += float(get_usd_crypto_price(coin)) * value
            embed.add_field(name="Total", value="Total: ${:0.2f}".format(total))
            await ctx.send(embed=embed)
            return

        # Not entirely sure what this does?  I don't remember writing it, seems
        # like some old version of the trading stuff


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
