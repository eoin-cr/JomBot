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
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.channel.id == 824766240589086761:
        print("Yup")
        if message.content.startswith("!send"):
            print("sending")
            channel = client.get_channel(829349688197120052)
            characters = len(message.content)
            async with channel.typing():
                timer = characters / 300 * 60
                time.sleep(timer)
                response = message.content.replace('!send', '')
                return await channel.send(response)

    # print(message.content)
    #
    # if message.content.startswith("?") and len(message.content.split(' ')) == 2 and message.author.guild_permissions.kick_members:
    #     print("kicking")
    #     cont = message.content.split(' ')
    #     auth = int(cont[1].strip('@,<>,!'))
    #     memb = await message.guild.fetch_member(auth)
    #     if message.author.id == auth:
    #         return await message.channel.send("You can't kick yourself I'm afraid!")
    #     await memb.kick(reason="You were inactive and have been footed")
    #     return await message.channel.send("Goodbye goofball <:pixellice:829423250361679922>")

    if message.guild is not None and message.guild.id == 829349685667430460:

        # print(message.content)
        # print(len(message.content.split(' ')))
        # print(message.author.guild_permissions)
        # print(message.author.guild_permissions.kick_members)
        if message.content.startswith("?") and len(message.content.split(' ')) == 2 and message.author.guild_permissions.kick_members:
            print("kicking")
            cont = message.content.split(' ')
            auth = int(cont[1].strip('@,<>,!'))
            memb = await message.guild.fetch_member(auth)
            if message.author.id == auth:
                return await message.channel.send("You can't kick yourself I'm afraid!")
            await memb.kick(reason="You were inactive and have been footed")
            return await message.channel.send("Goodbye goofball <:pixellice:829423250361679922>")

        if message.content == "!reply":
            return await message.reply('Hello')

        if message.content == "!short":
            return await message.channel.send("Ha lark is short")

        if message.content == "!introduce":
            return await message.channel.send("Hey there and welcome to the server!  Just a few quick questions to start off: \n 1. Are you british?  And if not what country are you from? \n 2. Do you use Linux? \n 3. Are you religious? \n 4. How old are you? \n 5. What are your preferred pronouns?\n 6. If you are political, what is your political ideology? \n Our answers start here: https://discord.com/channels/829349685667430460/829349688197120052/829674411337973770 \n Also when enabled I will delete every message containing sus, vented, etc.  So if your messages are getting removed, that might be why")

        if message.author.id == 85400548534145024 and message.content == "!enable ban":
            response = "!disable ban"
            await message.channel.send(response)
            return
        # print("yee")
        if message.mention_everyone:
            # print("Introducing!")
            return await message.channel.send("This seems important <:flosh:701774266894647338>")

        if message.content == "test":
            embed=discord.Embed(title="testing", url="https://google.com", description="test", color=discord.Color.blue())
            embed.set_author(name=message.author.display_name, url="https://bing.com", icon_url=message.author.avatar_url)
            embed.add_field(name="field 2", value="testing 2", inline=False)
            embed.set_footer(text="Test")
            embed.set_thumbnail(url="https://3.bp.blogspot.com/-vdcxPhqYdWM/UTSJzMfhUlI/AAAAAAAACyU/Vp5x5zqjf84/s1600/smiley-facess.jpg")
            await message.channel.send(embed=embed)
            return

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
            return
          else:
            response = "Uh oh there's been a fucky wucky"
            await message.channel.send(response)
            return

    # print("haw")
    # server = message.guild.id
    # if not os.path.exists(f"servers/{server}.json"):
    #     with open(f"servers/{server}.json", "w") as f:
    #         json.dump({}, f)
    # with open(f"servers/{server}.json", "r") as f:
    #     global server_data
    #     server_data = json.load(f)

    comment = message.content.lower()
    com = comment.strip().replace("*", "")
    # print(com)
    banned_words = ["sus","vented","amongus","amogus","imposter","impostor"]
    jesus = "jesus"
    sushi = "sushi"
    # print("1")
    # print(message.content)


    # print("74")
    if message.content.startswith("!1984") and message.author.guild_permissions.manage_guild:
        content = message.content.split(' ')
        variants = str(message.content).strip(' ').split('-')
        print(len(variants))
        server = message.guild.id
        start_response = ""
        server = message.guild.id
        if not os.path.exists(f"servers/{server}.json"):
            with open(f"servers/{server}.json", "w") as f:
                json.dump({}, f)
        with open(f"servers/{server}.json", "r") as f:
            server_data = json.load(f)
        if content[1] == "start":
            if len(variants) > 1 and variants[1] == "c":
                start_response = "(But only in this channel)"
                server_data[server] = True
            elif len(variants) > 1 and variants[1] == "ow":
                start_response = "And other presets have been overwritten."
                for channel in server_data.keys():
                  # if value != True:
                  server_data[channel] = True
            else:
                server_data["SBanned"] = True
            await message.channel.send("1984 time.  {}".format(start_response))
        elif content[1] == "stop":
            if len(variants) > 1 and variants[1] == "c":
                start_response = "(But only in this channel)"
                server_data[server] = False
            elif len(variants) > 1 and variants[1] == "ow":
                start_response = "And other presets have been overwritten."
                for channel in server_data.keys():
                  # if value != True:
                  server_data[channel] = False
            else:
                server_data["SBanned"] = False
            await message.channel.send("Amogus time.  {}".format(start_response))
            # print(start_response)
        with open(f"servers/{server}.json", 'w') as f:
            return json.dump(server_data, f)
    # print("87")
    for word in banned_words:
        server = message.guild.id
        if not os.path.exists(f"servers/{server}.json"):
            with open(f"servers/{server}.json", "w") as f:
                json.dump({}, f)
        with open(f"servers/{server}.json", "r") as f:
            server_data = json.load(f)
        if server_data.get("SBanned") is None:
            pass
        if server_data.get(message.channel.id) is not None and server_data[message.channel.id] == False:
            break
        elif server_data["SBanned"] and word in com:
            if message.author.id != 484444017489084416 and jesus not in com or sushi not in com:
                # break
            #
            # elif jesus in com or sushi in com:
            #     break
            #
            # await message.delete()
                return json.dump(server_data, f)
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

    # print("2")
    def get_usd_crypto_price(coin):
        usd_crypto_price = str(cryptocompare.get_price(coin, currency='USD')).strip('{}:')
        f = usd_crypto_price.split(' ')
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
    # print("3")
    if message.content.lower().startswith('!price'):

        message_split = message.content.split(' ')
        coin = message_split[1]
        # price = get_crypto_price(coin)
        # if len(message_split) <= 1:
        uprice = float(get_usd_crypto_price(coin))
        price = "${}".format(uprice)
        dprice = float(get_day_price(coin))
        # print(dprice)
        # print(uprice)
        daily_change = uprice / dprice * 100 - 100
        # print(daily_change)
        # elif message_split[2] == "eur":
        #     eprice = get_eur_crypto_price(coin)
        #     price = "?{}".format(eprice)

        #
        embed = discord.Embed(title="{} price".format(coin.upper()), description=price, color=discord.Color.blue())
        embed.set_author(name=message.author.display_name, icon_url=message.author.avatar_url)
        embed.add_field(name="Daily change", value='{}%'.format(round(daily_change)))
        embed.set_footer(text="Trade wisely")
        embed.set_thumbnail(url="https://uploads.tradestation.com/uploads/2017/12/Crypto-1024x1024.jpg")
        await message.channel.send(embed=embed)
        return
    # print(message.content)
    # print("4")
    if message.content.startswith('!chelp') or message.content.startswith("<@!820065836139675668> help"):
        embed=discord.Embed(title="Help", color=discord.Color.blue())
        embed.set_author(name=message.author.display_name, icon_url=message.author.avatar_url)
        embed.add_field(name="Commands", value="Ban/Allow the among us words (sus, vented, etc) [allowed by default - enabling may result in messages with legitimate words containing words like sus getting removed.] - `!1984 start/stop` [must have manage server perms] \n Buy crypto - `!cbuy [coin] [price in usd/all]` \n Sell crypto - `!csell [coin] [price in usd/all]` \n Price of a coin - `!price [coin]` \n View wallet - `!wallet`")
        await message.channel.send(embed=embed)
        return

    # print("5")
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
                await message.channel.send("Warning: Could not complete trade, coin balance too low.  Your current USD balance is {:0.2f}".format(data.get("USD")))
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
            return await message.channel.send("Looks like there may have been a mistake, make sure the command is \n `!cbuy [coin] [amount in usd/all]`")

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
              await message.channel.send("Warning: Could not complete trade, coin balance too low.  Your current {} balance is {}".format(coin, data.get(coin)))
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
            return await message.channel.send("Looks like there may have been a mistake, make sure the command is  \n `!csell [coin] [amount in usd/all]`")

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
        # with open('userCash.txt', 'r') as file:
        #     # read a list of lines into data
        #     cash = file.readlines()
        # for user in cash:
        #     print(user)
        #     print(message.author.id)
        #     if user == message.author.id:
        #         cash[i+1] = '{}\n'.format(cash[i+1] - amount)
        #         print(cash[i+1])
        #         cash[i+2] = '{}\n'.format(cash[i+2] + btc)
        #         with open('userCash.txt', 'w') as file:
        #             file.writelines( coin )
        #         await message.channel.send("Successfully traded ${} for {}btc".format(amount, btc))
        #         return
        #     else:
        #         i =+ 1
        #         print("users don't match")

# #doing shit with reactions
# @client.event
# # @has_permissions(manage_messages=True)
# async def on_reaction_add(reaction, user):
#     # print(reaction.emoji.encode())
#     # print("{} does have the perms manage_messages".format(user))
#     async for user in reaction.users():
#
#         # channel = client.get_channel(823243464212873226)
#         if user != None and user != client.user and user.guild_permissions.manage_messages:
#             # print(user)
#             # if user.permissions_for(manage_messages) == True and reaction.emoji == "?":
#             if reaction.emoji == "\N{CLAPPING HANDS SIGN}":
#                 # response = "{} deleted the message \"{}\" by {}".format(user, reaction.message.content, reaction.message.author)
#                 # audit = "audit-zone"
#                 # await channel.send(response)
#                 await reaction.message.delete()
#                 return
#
# # @has_permissions(manage_messages=False)
# # async def on_reaction_add(reaction, user):
#     # print("{} does not have the perms manage_messages".format(user))
#     # channel = reaction.channel
#     # print(reaction.emoji)
#         elif len(reaction.message.embeds) > 0:
#             embed = reaction.message.embeds[0]
#             if reaction.message.author == client.user and reaction.emoji == "?":
#                 await reaction.message.delete()
#                 return

client.run(TOKEN)
