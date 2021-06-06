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
import numpy

intents = discord.Intents.default()
intents.members = True



load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client(intents=intents)

@client.event
async def on_member_join(member):
    # print("Joined!")
    channel = client.get_channel(829349688197120052)
    invite_list = await member.guild.invites()
    # print(invite_list)
    # for i in invite_list:
    #     print(i.inviter)
    # general = find(lambda x: x.name == 'general',  guild.text_channels)
    # print(general)
    # await channel.send('Hello {} and welcome to the server!  A lot of people seem to join and then just never say anything so please don\'t do that thanks.  Anyway be sure to answer the questions in <#830565670805962822> and then check out <#830565732001644555> and <#830565778654887958> for more information!  Also when enabled I will delete every message containing sus, vented, etc.  So if your messages are getting removed, that might be why'.format(member.name))
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

    if message.guild is not None and message.guild.id == 829349685667430460:

        wheel_speak = ["Fucking windows man.  Literal spyware.  Stop using that shit and switch to Linux.  Imagine having to download stuff from the internet.  Cringe as fuck","Capitalism is not a sustainable system.  It is one that grants immense power to those born rich, and does nothing but harm everyone else.  Literally fucking killing the planet and can't do shit about it as all the politicians are paid off. man.","Dude chrome is literally logging every single thing you type and selling that shit to advertisers.  Please switch to hardened firefox or brave.  There is literally no need for companies to know so much about you.  Privacy is genuinely important.","Ok but honestly colemak is so much nicer than qwerty.  Everything is done in the name of maximum comfort and typing efficiency.  I don't know why you'd use a keyboard layout that's literally worse in every way.","Imagine not having nearly 4TB of storage space.  Cringe.  And cookie for the love of god will you implement some sort of naming convention please <:sadtownload:829423251214041148>","oyunarsoyun","Vim is so much better than other IDEs honestly.  And god.  Fucking nano.  Man why would you do that when vim is genuinely so much better"]

        wheel = ["Man let me tell you about Linux...","Fucking Chrome man, please switch...","Data collection is kinda cool ig","Stop using other IDEs when vim is just better...","Ok colemak is genuinely better because...","Oh boy you're boutta be converted to socialism.  Our numbers must grow...","oyaunrsoyun"]

        if message.content.lower() == "!jomwheel spin -s":
            num = random.randint(0,6)
            await message.channel.send("*clickclickclickclick*")
            return await message.channel.send(wheel_speak[num])

        if message.content.lower() == "!jomwheel spin":
            num = random.randint(0,6)
            await message.channel.send("*clickclickclickclick*")
            return await message.channel.send(wheel[num])

        # print(message.content)
        # print(len(message.content.split(' ')))
        # print(message.author.guild_permissions)
        # print(message.author.guild_permissions.kick_members)
        if message.content.startswith("🦶") and len(message.content.split(' ')) == 2 and message.author.guild_permissions.kick_members:
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

        if message.content.startswith("!print"):
            return print(message.content)

        if message.content == "!short":
            return await message.channel.send("Ha lark is short")

        if message.content == "!introduce":
            return await message.channel.send("Hey there and welcome to the server!  Be sure to answer the questions in <#830565670805962822> and then check out <#830565732001644555> and <#830565778654887958> for more information!  Also when enabled I will delete every message containing sus, vented, etc.  So if your messages are getting removed, that might be why")

        if message.author.id == 85400548534145024 and message.content == "!enable ban":
            response = "!disable ban"
            await message.channel.send(response)
            return
        # print("yee")
        if message.mention_everyone:
            # print("Introducing!")
            return await message.channel.send("This seems important <:flosh:701774266894647338>")


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


    comment = message.content.lower()
    com = comment.strip().replace("*", "")
    # print(com)
    banned_words = ["sus","vented","amongus","amogus","imposter","impostor"]
    jesus = "jesus"
    sushi = "sushi"
    # print("1")
    # print(message.content)
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


    if message.content == "ls invites":
        invite_list = await message.guild.invites()
        for i in range (0, len(invite_list)):
            print(invite_list[i].uses)
        # secret = client.get_channel(850459809324597288)
        # # print(invite_list[2].uses)
        # for i in invite_list:
        #     num_list = []
        #     # with is like your try .. finally block in this case
        #     with open('invite.txt', 'r') as file:
        #     # read a list of lines into data
        #         data = file.readlines()
        #     if invite_list[i].uses is not data[1]:
        #         await secret.send("{} was invited to the server by {}".format(guild.name, i.inviter.user))
        #         data[1] = invite_list[i]
        #         with open('stats.txt', 'w') as file:
        #             file.writelines( data )



        # for i in invite_list:
        #     print(i.inviter)
        # await message.channel.send(invite_list)

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
        channel  = str(message.channel.id)
        if not os.path.exists(f"servers/{server}.json"):
            with open(f"servers/{server}.json", "w") as f:
                json.dump({}, f)
        with open(f"servers/{server}.json", "r") as f:
            server_data = json.load(f)
        # print(server_data[channel])
        if server_data.get(channel) is not None and server_data[channel] == False:
            break
        if server_data["SBanned"] and word in com:
            # if message.author.id != 484444017489084416 or jesus not in com or sushi not in com:
            if message.author.id == 484444017489084416:
                break
            #
            elif jesus in com or sushi in com:
                break
            #
            await message.delete()
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

client.run(TOKEN)
#Client.load_extension("invites")
