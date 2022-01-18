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
from discord.utils import find

intents = discord.Intents.default()
intents.members = True



load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# client = discord.Client(intents=intents)
# prefix = "!"
bot = commands.Bot(command_prefix=("!","<:chigmn2:829382748631203901>"))

@bot.event
async def on_member_join(member):
    channel = client.get_channel(829349688197120052)
    invite_list = await member.guild.invites()
    # await channel.send("""Hello {} and welcome to the server!  A lot of people \
    # seem to join and then just never say anything so please don\'t do that thanks.  \
    # Anyway be sure to answer the questions in <#830565670805962822> and then check \
    # out <#830565732001644555> and <#830565778654887958> for more information!  \
    # Also when enabled I will delete every message containing sus, vented, etc.  \
    # So if your messages are getting removed, that might be why""".format(member.name))
    secret = client.get_channel(850459809324597288)
    # print(invite_list[2].uses)
    for i in range(0, len(invite_list)):
        # for x in invite_list:
        num_list = []
        # invite =
        # with is like your try .. finally block in this case
        with open('invites.txt', 'r') as file:
        # read a list of lines into data
            data = file.readlines()
        if invite_list[i].uses is not data[i]:
            await secret.send("{} was invited to the server by {}".format(member.name, invite_list[i].inviter))
            data[i] = invite_list[i].uses
            break
            # print(data)
        # with open('invites.txt', 'w') as file:
        #     file.write('\n'.join(data))

    invites_list = await member.guild.invites()
    list = []
    for i in range (0, len(invites_list)):
        # print(invites_list[i].uses)
        list.append(invites_list[i].uses)
    with open('invites.txt', 'w') as file:
        file.write('\n'.join([str(x) for x in list]))

@bot.event
async def on_message(message):

#     if message.author.id == 484444017489084416 and message.content.startswith("!"):
#         await message.channel.send("Yes")

    if message.content == "inv_txt":
        invites_list = await message.guild.invites()
        list = []
        for i in range (0, len(invites_list)):
            # print(invites_list[i].uses)
            list.append(invites_list[i].uses)
        # Array =  numpy.array(list)
        # file = open("test.txt", "w+")
        # content = str(Array)
        # file.write(content)
        # file.close()
        # return print("File closed")
        with open('test.txt', 'w') as file:
            file.write('\n'.join([str(x) for x in list]))
                # with open(f"servers/{server}.json", 'w') as f:
                #
            #     return json.dump(server_data, f)
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

    if message.content.lower().startswith('!cbuy'):
        try:
            coin, amount = message.content.split()[1:3]
            everything = False
            auth = message.author.id
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
            uprice = get_usd_crypto_price(coin)
            # btc_price = get_usd_crypto_price("btc")
            cprice = float(amount)/float(uprice)
            # with open(f"users/{auth}.json", "r") as f:
            #   data = json.load(f)
            if data.get(coin) is None:
              data[coin] = 0.0
            if data.get("USD") is None:
              data["USD"] = 10000.0
            if amount > data.get("USD"):
                await message.channel.send("""Warning: Could not complete trade, \
                coin balance too low.  Your current USD balance is {:0.2f}""".format(data.get("USD")))
                return
            if everything:
                data[coin] += cprice
                all = data["USD"]
                data["USD"] = 0
                await message.channel.send("Successfully traded ${:0.2f} for {:0.2f}{}".format(all, cprice, coin.upper()))
            else:
                data[coin] += cprice
                data["USD"] -= amount
                await message.channel.send("Successfully traded ${:0.2f} for {:0.2f}{}".format(amount, cprice, coin.upper()))
            with open(f"users/{auth}.json", "w") as f:
              json.dump(data, f)
            return
        except:
            return await message.channel.send("""Looks like there may have been \
            a mistake, make sure the command is \n `!cbuy [coin] [amount in usd/all]`""")

    if message.content.lower().startswith('!csell'):
        try:
            coin, amount = message.content.split()[1:3]
            uprice = get_usd_crypto_price(coin)
            everything = False
            auth = message.author.id
            # print(amount)
            # print(uprice)
            # print(amount*uprice)
            if not os.path.exists(f"users/{auth}.json"):
                with open(f"users/{auth}.json", "w") as f:
                    json.dump({}, f)
            with open(f"users/{auth}.json", "r") as f:
              data = json.load(f)

            # print(data[coin])
            if amount == "all":
                everything = True
                amount = data[coin] * uprice
            else:
                amount = float(amount)
            # btc_price = get_usd_crypto_price("btc")
            cprice = float(amount)/float(uprice)
            auth = message.author.id
            # with open(f"users/{auth}.json", "r") as f:
            #   data = json.load(f)
            if data.get(coin) is None:
              data[coin] = 0.0
            if data.get("USD") is None:
              data["USD"] = 10000.0
            if amount > data.get(coin):
              await message.channel.send("""Warning: Could not complete trade, \
              coin balance too low.  Your current {} balance is {}""".format(coin, data.get(coin)))
              return
            if everything:
                data["USD"] += amount
                all = data[coin]
                data[coin] = 0
                await message.channel.send("Successfully traded {:0.2f}{} for ${:0.2f}".format(cprice, coin.upper(), all))
            else:
                data[coin] -= cprice
                data["USD"] += amount
                await message.channel.send("Successfully traded {:0.2f}{} for ${:0.2f}".format(cprice, coin.upper(), amount))
            with open(f"users/{auth}.json", "w") as f:
              json.dump(data, f)
            return
        except:
            return await message.channel.send("""Looks like there may have been \
            a mistake, make sure the command is  \n `!csell [coin] [amount in usd/all]`""")

    if message.content.lower().startswith('!wallet'):
        # print("YES!")
        cont = message.content.split(' ')
        # print(len(cont))
        if len(cont) > 1:
            # print(cont[1])
            auth = int(cont[1].strip('@,<>,!'))
            # await client.fetch_user(auth)
            memb = await client.fetch_user(auth)
            # print(auth.nick)
            # print(memb)
            # print(memb.nick)
            # print(auth)
            if not os.path.exists(f"users/{auth}.json"):
                with open(f"users/{auth}.json", "w") as f:
                    json.dump({}, f)
            with open(f"users/{auth}.json", "r") as f:
              data = json.load(f)
            total = 0
            embed=discord.Embed(title="{}'s wallet".format(memb.display_name), color=discord.Color.blue())
            embed.set_author(name=memb.display_name, icon_url=memb.avatar_url)
            for coin, value in data.items():
              if value != 0:
                embed.add_field(name=coin, value="{:0.2f}".format(value))
              # print(get_usd_crypto_price(coin))
                total += float(get_usd_crypto_price(coin)) * value
            embed.add_field(name="Total", value="Total: ${:0.2f}".format(total))
            await message.channel.send(embed=embed)
            return
        else:
            auth = message.author.id
            if not os.path.exists(f"users/{auth}.json"):
                with open(f"users/{auth}.json", "w") as f:
                    json.dump({}, f)
            with open(f"users/{auth}.json", "r") as f:
              data = json.load(f)
            total = 0
            embed=discord.Embed(title="{}'s wallet".format(message.author.display_name), color=discord.Color.blue())
            embed.set_author(name=message.author.display_name, icon_url=message.author.avatar_url)
            for coin, value in data.items():
              if value != 0:
                embed.add_field(name=coin.upper(), value="{:0.2f}".format(value))
              # print(get_usd_crypto_price(coin))
                total += float(get_usd_crypto_price(coin)) * value
            embed.add_field(name="Total", value="Total: ${:0.2f}".format(total))
            await message.channel.send(embed=embed)
            return
        with open('userCash.txt', 'r') as file:
            # read a list of lines into data
            cash = file.readlines()
        for user in cash:
#             print(user)
#             print(message.author.id)
            if user == message.author.id:
                cash[i+1] = '{}\n'.format(cash[i+1] - amount)
#                 print(cash[i+1])
                cash[i+2] = '{}\n'.format(cash[i+2] + btc)
                with open('userCash.txt', 'w') as file:
                    file.writelines( coin )
                await message.channel.send("Successfully traded ${} for {}btc".format(amount, btc))
                return
            else:
                i =+ 1
#                 print("users don't match")
    await bot.process_commands(message)

@bot.command()
async def hello(ctx):
    hello = "Hello!"
    await ctx.send(hello)


bot.load_extension("cogs.trading")
bot.load_extension("cogs.crypto_price")
bot.load_extension("cogs.pond")
# bot.load_extension("cogs.remove")
# bot.load_extension("cogs.join")
# bot.load_extension("cogs.binder_check")
# bot.load_extension("cogs.jokes")
bot.load_extension("cogs.ip")
# bot.load_extension("cogs.music")
bot.load_extension("cogs.song")
bot.load_extension("cogs.wordle")

bot.run(TOKEN)
