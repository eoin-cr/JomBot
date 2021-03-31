# bot.py
import os
import random
import time
import re
import discord
import requests
from dotenv import load_dotenv
from discord.ext import commands
from discord.ext.commands import has_permissions
from bs4 import BeautifulSoup
import cryptocompare
import json


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()
#
# class Crypto(commands.cog):
#     with open('userCash.txt', 'r') as file:
#         # read a list of lines into data
#         cash = file.readlines()
#
#     async def buy(self, member, money: int):
#         for user in Cash:
#             if user == member:
#                 cash[i+1] = '{}\n'.format(cash[i+1] - money)
#                 cash[i+2] = '{}\n'.format(cash[i+2] + money)
#                 return
#             else:
#                 i =+ 1
#
# bot = commands.Bot(command_prefix='$')
#
# @bot.command()
# async def test(ctx, arg1, arg2, arg3, arg4):
#     if arg1 == "price":
#         return
#     elif arg1 == "crypto":
#         if arg2 == trade:
#             buy(ctx.author.id, arg3)


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    # if message.content == "!offline" and message.author.id == 484444017489084416:
    #     await client.change_presence(status=discord.status.offline)
    # if message.content == "!online" and message.author.id == 484444017489084416:
    #     await client.change_presence(status=discord.status.online)
    # if message.content == "!offline" and message.author.id == 484444017489084416:
    #     await client.change_presence(status=discord.status.offline)
    # if message.content == "!online" and message.author.id == 484444017489084416:
    #     await client.change_presence(status=discord.status.online)
    #
    # if client.status == discord.Status.offline:
    #     return

    def get_usd_crypto_price(coin):
        usd_crypto_price = str(cryptocompare.get_price(coin, currency='USD')).strip('{}:')
        f = usd_crypto_price.split(' ')
        # print(f)
        usd_price = f[2]
        return usd_price

    def get_day_price(coin):
        usd_crypto_price = str(cryptocompare.get_historical_price_day(coin, currency='USD')).strip('{}:')
        f = usd_crypto_price.split(' ')
        # print(len(f))
        # print(f)
        day_price = f[-11]
        day_price = day_price.strip(',')
        # print(day_price)
        # print(f[25918:25938])
        return day_price

    if message.content.startswith('!price'):

        message_split = message.content.split(' ')
        coin = message_split[1]
        # price = get_crypto_price(coin)
        # if len(message_split) <= 1:
        uprice = float(get_usd_crypto_price(coin))
        price = "${}".format(uprice)

        # if len(message_split) > 3 and message_split[2] == day:
        # day_price = cryptocompare.get_historical_price_day(coin, currency='USD')
        # print(day_price)
        dprice = float(get_day_price(coin))
        print(dprice)
        print(uprice)
        daily_change = uprice / dprice * 100 - 100
        print(daily_change)

        # elif message_split[2] == "eur":
        #     eprice = get_eur_crypto_price(coin)
        #     price = "€{}".format(eprice)

        #
        embed = discord.Embed(title="{} price".format(coin.upper()), description=price, color=discord.Color.blue())
        embed.set_author(name=message.author.display_name, icon_url=message.author.avatar_url)
        embed.add_field(name="Daily change", value='{}%'.format(round(daily_change)))
        embed.set_footer(text="Trade wisely")
        embed.set_thumbnail(url="https://uploads.tradestation.com/uploads/2017/12/Crypto-1024x1024.jpg")
        await message.channel.send(embed=embed)

    if message.content.startswith('!cbuy'):
        coin, amount = message.content.split()[1:3]
        everything = False
        auth = message.author.id
        if not os.path.exists(f"users/{userid}.json"):
            with open(f"users/{userid}.json", "w") as f:
                json.dump({}, f)
        with open(f"users/{auth}.json", "r") as f:
          data = json.load(f)
        if amount == "all":
            everything = True
            amount = data["USD"]

        else:
            amount = int(amount)
        uprice = get_usd_crypto_price(coin)
        # btc_price = get_usd_crypto_price("btc")
        btc = float(amount)/float(uprice)
        # with open(f"users/{auth}.json", "r") as f:
        #   data = json.load(f)
        if data.get(coin) is None:
          data[coin] = 0.0
        if data.get("USD") is None:
          data["USD"] = 10000.0
        if amount > data.get("USD"):
            await message.channel.send("Warning: Could not complete trade, coin balance too low.  Your current USD balance is {}".format(data.get("USD")))
            return
        if everything:
            data[coin] += data["USD"]
            all = data["USD"]
            data["USD"] = 0
            await message.channel.send("Successfully traded ${} for {}btc".format(all, btc))
        else:
            data[coin] += amount
            data["USD"] -= amount
            await message.channel.send("Successfully traded ${} for {}btc".format(amount, btc))
        with open(f"users/{auth}.json", "w") as f:
          json.dump(data, f)

    if message.content.startswith('!csell'):
        coin, amount = message.content.split()[1:3]
        everything = False
        auth = message.author.id
        if not os.path.exists(f"users/{userid}.json"):
            with open(f"users/{userid}.json", "w") as f:
                json.dump({}, f)
        with open(f"users/{auth}.json", "r") as f:
          data = json.load(f)
        #checks if all money is selected, and if so, sets amount to current usd balance
        if amount == "all":
            everything = True
            amount = data[coin]
        else:
            amount = int(amount)
        uprice = get_usd_crypto_price(coin)
        btc_price = get_usd_crypto_price("btc")
        btc = float(amount)/float(btc_price)
        auth = message.author.id
        # with open(f"users/{auth}.json", "r") as f:
        #   data = json.load(f)
        if data.get(coin) is None:
          data[coin] = 0.0
        if data.get("USD") is None:
          data["USD"] = 10000.0
        if amount > data.get(coin):
          await message.channel.send("Warning: Could not complete trade, coin balance too low.  Your current {} balance is {}".format(coin, data.get(coin)))
          return
        if everything:
            data["USD"] += data[coin]
            all = data[coin]
            data[coin] = 0
            await message.channel.send("Successfully traded ${} for {}btc".format(all, btc))
        else:
            data[coin] -= amount
            data["USD"] += amount
            await message.channel.send("Successfully traded ${} for {}btc".format(amount, btc))
        with open(f"users/{auth}.json", "w") as f:
          json.dump(data, f)

#crypto wallet
    if message.content.startswith('!wallet'):
        auth = message.author.id
        with open(f"users/{auth}.json", "r") as f:
          data = json.load(f)
        total = 0
        embed=discord.Embed(title="{} wallet".format(message.author.nick), color=discord.Color.blue())
        embed.set_author(name=message.author.display_name, icon_url=message.author.avatar_url)
        for coin, value in data.items():
          embed.add_field(name=coin, value=value)
          print(get_usd_crypto_price(coin))
          total += float(get_usd_crypto_price(coin)) * value
        embed.add_field(name="Total", value=f"Total: ${total}")
        await message.channel.send(embed=embed)

#test embed
    if message.content == "test":
        embed=discord.Embed(title="testing", url="https://google.com", description="test", color=discord.Color.blue())
        embed.set_author(name=message.author.display_name, url="https://bing.com", icon_url=message.author.avatar_url)
        embed.add_field(name="field 2", value="testing 2", inline=False)
        embed.set_footer(text="Test")
        embed.set_thumbnail(url="https://3.bp.blogspot.com/-vdcxPhqYdWM/UTSJzMfhUlI/AAAAAAAACyU/Vp5x5zqjf84/s1600/smiley-facess.jpg")
        await message.channel.send(embed=embed)

#secret :flosh:
    if message.channel.id == 824766240589086761:
        if message.content.startswith("!send"):
            channel = client.get_channel(529349973998043150)
            characters = len(message.content)
            async with channel.typing():
                timer = characters / 300 * 60
                time.sleep(timer)
                response = message.content.replace('!send', '')
                await channel.send(response)

    comment = message.content.lower()
    com = comment.strip()
    banned_words = ["sus","vented","amongus","amogus","imposter","impostor"]
    jesus = "jesus"
    sushi = "sushi"

    if message.author.id == 85400548534145024 and message.content == "!enable ban":
        response = "!disable ban"
        await message.channel.send(response)

    if message.mention_everyone == True:
        await message.channel.send("This seems important <:flosh:701774266894647338>")

#deletes messages with certain words
    for word in banned_words:
        if word in com:
            if message.author.id == 484444017489084416:
                return

            elif jesus in com or sushi in com:
                return

            return await message.delete()

#returns random string of words from a wordlist
    if message.author.id == 694115623080427540:
        return
    elif message.content.lower() == 'alias' or message.content.split() == 'alias' or message.content.split() == 'Alias':
        #open text file in read mode
      text_file = open("words.txt", "r")
          #read whole file to a string
      words = text_file.read()
    # time = time.perf_counter()

      loopNum = random.randint(3,10)
      sentence = ""
      Mauth = str(message.author)
      if words is not None:
        words = words.split('\n')
        for x in range(loopNum):
          index = random.randint(0,466550)
          sentence = sentence + words[index] + " "
          # print(sentence)
        response = sentence
        await message.channel.send(response)
      else:
        response = "Uh oh there's been a fucky wucky"
        await message.channel.send(response)

#doing shit with reactions
@client.event
@has_permissions(manage_messages=True)
async def on_reaction_add(reaction, user):
    # print(reaction.emoji.encode())
    # print("{} does have the perms manage_messages".format(user))
    async for user in reaction.users():

        channel = client.get_channel(823243464212873226)
        if user != None and user != client.user and reaction.message.channel != channel:
            # print(user)
            # if user.permissions_for(manage_messages) == True and reaction.emoji == "?":
            if reaction.emoji == "\N{CLAPPING HANDS SIGN}":
                response = "{} deleted the message \"{}\" by {}".format(user, reaction.message.content, reaction.message.author)
                # audit = "audit-zone"
                await channel.send(response)
                await reaction.message.delete()

@has_permissions(manage_messages=False)
async def on_reaction_add(reaction, user):
    # print("{} does not have the perms manage_messages".format(user))
    # channel = reaction.channel
    # print(reaction.emoji)
    if len(reaction.message.embeds) > 0:
        embed = reaction.message.embeds[0]
        if reaction.message.author == client.user and reaction.emoji == "\N{CLAPPING HANDS SIGN}":
            await reaction.message.delete()

client.run(TOKEN)
