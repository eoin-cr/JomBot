#crypto_price.py
import os
import re
import discord
from dotenv import load_dotenv
from discord.ext import commands
from discord.ext.commands import has_permissions
import cryptocompare

class Crypto_Price(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        print("Pricing initialised")

    @commands.command()
    async def get_usd_crypto_price(self,coin):
        usd_crypto_price = str(cryptocompare.get_price(coin, currency='USD')).strip('{}:')
        f = usd_crypto_price.split(' ')
        usd_price = f[2]
        return usd_price

    @commands.command()
    async def get_day_price(self,coin):
        usd_crypto_price = str(cryptocompare.get_historical_price_day(coin, currency='USD')).strip('{}:')
        f = usd_crypto_price.split(' ')
        # print(len(f))
        # print(f)
        day_price = f[-11]
        day_price = day_price.strip(',')
        # print(day_price)
        # print(f[25918:25938])
        return day_price

def setup(bot):
    bot.add_cog(Crypto_Price(bot))
