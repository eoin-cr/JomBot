# pond.py
import os
import re
import discord
import requests
from discord.ext import commands
import json
from discord.utils import find
import random
from numpy import loadtxt
import asyncio

class Pond(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        print("Pond initialised")

    @commands.Cog.listener()
    async def on_message(self,ctx):
        if ctx.author.id == 234395307759108106:
            voice_state = ctx.member.voice
            await asyncio.sleep(5)

            if voice_state is None:
                await ctx.send('Shut the fuck up groovy')
                return await ctx.remove


    @commands.Cog.listener()
    async def on_message(self,message):
        if message.guild is not None and message.guild.id == 829349685667430460:
            if message.channel.id == 830565670805962822:
                role1 = discord.utils.get((await message.guild.fetch_roles()), name='tadpoles')
                role2 = discord.utils.get((await message.guild.fetch_roles()), name='froglet')
                role3 = discord.utils.get((await message.guild.fetch_roles()), name='froggers')
                if role1 in message.author.roles or role2 in message.author.roles or role3 in message.author.roles:
                    print("ignoring")
                else:
#                     await bot.add_roles(user, role)
                    ch = message.guild.get_channel(829349688197120052)
                    # print(message.guild.roles)
                    await message.author.add_roles(role1)
                    # await message.author.add_roles(message.author, role)
                    return await ch.send(f"Welcome to the pond {message.author.mention}")

            if message.mention_everyone:
                return await message.channel.send("This seems important <:flosh:701774266894647338>")

    @commands.command(name="foot", alias="🦶", help="Kicks someone")
    async def foot(self, ctx, user):
        if ctx.message.guild is not None and ctx.message.guild.id == 829349685667430460 and ctx.message.author.guild_permissions.kick_members:
#             if message.content.startswith("🦶") and len(message.content.split(' ')) == 2 and message.author.guild_permissions.kick_members:
#                 print("kicking")
            auth = int(user.strip('@,<>,!'))
            memb = await ctx.message.guild.fetch_member(auth)
            if ctx.message.author.id == auth:
                return await ctx.send("You can't kick yourself I'm afraid!")
            await memb.kick(reason="You were inactive and have been footed")
            return await ctx.send("Goodbye goofball <:pixellice:829423250361679922>")

    @commands.command(name="Q", help="Formats Jom's questions")
    async def Q(self, ctx, *, cont):
        if ctx.message.author.id == 484444017489084416 and ctx.message.guild is not None and ctx.message.guild.id == 829349685667430460:
            split = cont.split('\n')
            for i in range(len(split)):
                if split[i].startswith("Q"):
                    split[i] = split[i].replace(".", ":", 1)
                elif '/' not in split[i]:
                    split[i] = f"- {split[i]}"

            qsChannel = message.guild.get_channel(834198286310047784)
#             qsChannel = ctx.message.guild.get_channel(829358413065486376)
            joined = '\n'.join(split)
            full_message = str(f"```yaml\n{joined} \n```")
            return await qsChannel.send(full_message)

    @commands.command()
    async def jomwheel(self,message,ctx, *arg):
        with open("wheel_speak.txt", "r") as file:
            lines = file.readlines()
            for l in lines:
                wheel_speak = l.split(", ")
        with open("wheel.txt", "r") as file:
            lines = file.readlines()
            for l in lines:
                wheel = l.split(", ")
        if arg == ('s',):
            num = random.randint(0,6)
            await message.channel.send("*clickclickclickclick1*")
            return await message.channel.send(wheel_speak[num])
        else:
            num = random.randint(0,6)
            await message.channel.send("*clickclickclickclick*")
            return await message.channel.send(wheel[num])

    @commands.command()
    async def reply(self,ctx):
        return await ctx.reply('Hello')

    @commands.command()
    async def print(self,ctx,message):
        return print(message)

    @commands.command()
    async def short(self,ctx):
        return await ctx.send("Ha lark is short")

    @commands.command()
    async def introduce(self,ctx):
        return await ctx.send("""Hey there and welcome to the server!
Be sure to answer the questions in <#830565670805962822> and then check
out <#830565732001644555> and <#830565778654887958> for more information!
Also when enabled I will delete every message containing sus, vented, etc.
So if your messages are getting removed, that might be why""")

    @commands.command()
    async def test(self,message):
        embed=discord.Embed(title="testing", url="https://google.com", description="test", color=discord.Color.blue())
        embed.set_author(name=message.author.display_name, url="https://bing.com", icon_url=message.author.avatar_url)
        embed.add_field(name="field 2", value="testing 2", inline=False)
        embed.set_footer(text="Test")
        embed.set_thumbnail(url="https://3.bp.blogspot.com/-vdcxPhqYdWM/UTSJzMfhUlI/AAAAAAAACyU/Vp5x5zqjf84/s1600/smiley-facess.jpg")
        await message.channel.send(embed=embed)
        return

    @commands.command()
    async def ls(self,ctx,message):
        if message == "invites":
            invite_list = await ctx.guild.invites()
            for i in range (0, len(invite_list)):
                print(invite_list[i].uses)

    @commands.command()
    async def alias(self,message):
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

def setup(bot):
    bot.add_cog(Pond(bot))
